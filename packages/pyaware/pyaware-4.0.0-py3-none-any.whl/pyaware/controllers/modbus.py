import asyncio
import typing
from datetime import datetime
from pathlib import Path

import pyaware.aggregations
import pyaware.config
import pyaware.data_types
import pyaware.triggers
import pyaware.transformations
import pyaware.meta
from pyaware import watchdog
from pyaware import events
from pyaware.mqtt.models import TopologyChildrenV2
from pyaware.protocol.modbus import (
    log,
    ModbusAsyncTcpClient,
    ModbusAsyncSerialClient,
    modbus_exception_codes,
)
from pyaware.store import memory_storage

numeric = typing.Union[int, float]


@events.enable
class ModbusDevice:
    name = "Modbus Device"
    module_type = "modbus-device"

    def __init__(
        self,
        client,
        device_id: str,
        config: Path,
        unit=0,
        address_shift=0,
        poll_intervals: typing.Optional[typing.Dict[str, numeric]] = None,
    ):
        self.client = client
        self.device_id = device_id
        if poll_intervals is None:
            self.poll_intervals = {}
        else:
            self.poll_intervals = poll_intervals
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {}
        self.unit = unit
        self.config = pyaware.config.load_config(config)
        self.address_shift = address_shift
        self.parameter_metadata = pyaware.meta.parse_metadata(self.config["parameters"])
        self.parameters = pyaware.data_types.parse_data_types(
            self.config["parameters"], {}
        )
        if address_shift:
            for param in self.parameters.values():
                try:
                    param.address += address_shift
                except KeyError:
                    continue
        self.triggers = pyaware.triggers.build_from_device_config(
            config,
            device_id=device_id,
            send_state=self.send_state,
            store_state=self.store_state,
            event_state=self.event_state,
            current_state=self.current_state,
        )
        self.transformations = pyaware.transformations.build_from_device_config(config)
        self.aggregates = pyaware.aggregations.build_from_device_config(config)
        if any(
            isinstance(self.client, x)
            for x in (ModbusAsyncTcpClient, ModbusAsyncSerialClient)
        ):
            # Use pymodbus
            self.read_handles = {
                "holding": self._read_holding_registers_pymodbus,
                "input": self._read_input_registers_pymodbus,
                "discrete": self._read_discrete_inputs_pymodbus,
                "coils": self._read_coils_pymodbus,
            }
            self.write_handles = {
                "holding": self._write_holding_registers_pymodbus,
                "coils": self._write_coils_pymodbus,
            }
        else:
            # Use aiomodbus
            self.read_handles = {
                "holding": self.client.read_holding_registers,
                "input": self.client.read_input_registers,
                "discrete": self.client.read_discrete_inputs,
                "coils": self.client.read_coils,
            }
            self.write_handles = {
                "holding": self.client.write_multiple_registers,
                "coils": self.client.write_multiple_coils,
            }

    def init(self):
        # Initialise subscriptions
        events.subscribe(self.process_data, topic=f"process_data/{id(self)}")
        events.subscribe(self.process_write, topic=f"process_write/{id(self)}")
        for name, source_config in self.config["sources"].items():
            if source_config.get("type", "poll") == "poll":
                asyncio.create_task(
                    self.trigger_poll(name, address_shift=self.address_shift)
                )
        self.setup_watchdogs()

    def setup_watchdogs(self):
        try:
            self.client.protocol_made_connection = watchdog.watch(
                f"modbus_comms_status_{id(self)}"
            )(self.client.protocol_made_connection)
        except AttributeError:
            pass
        try:
            self.read_registers = watchdog.watch(f"modbus_comms_status_{id(self)}")(
                self.read_registers
            )
        except AttributeError:
            pass
        try:
            self.client.protocol_lost_connection = watchdog.watch_starve(
                f"modbus_comms_status_{id(self)}"
            )(self.client.protocol_lost_connection)
        except AttributeError:
            pass
        dog_comms = watchdog.WatchDog(
            heartbeat_time=5,
            success_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"modbus-comms-status": True},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
            failure_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"modbus-comms-status": False},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
        )
        watchdog.manager.add(f"modbus_comms_status_{id(self)}", dog_comms)
        dog_comms.start(start_fed=False)

    # TODO remove pymodbus wrapper functions and move to aiomodbus exclusively
    async def _read_holding_registers_pymodbus(
        self, address: int, count: int, unit: int
    ):
        rr = await self.client.protocol.read_holding_registers(
            address, count, unit=unit
        )
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)
        return rr.registers

    async def _read_input_registers_pymodbus(self, address: int, count: int, unit: int):
        rr = await self.client.protocol.read_input_registers(address, count, unit=unit)
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)
        return rr.registers

    async def _read_discrete_inputs_pymodbus(self, address: int, count: int, unit: int):
        rr = await self.client.protocol.read_discrete_inputs(address, count, unit=unit)
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)
        # rr.bits returns a list of bits in multiples of 8. Just ensures required subset of data is returned.
        return rr.bits[0:count]

    async def _read_coils_pymodbus(self, address: int, count: int, unit: int):
        rr = await self.client.protocol.read_coils(address, count, unit=unit)
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)
        # rr.bits returns a list of bits in multiples of 8. Just ensures required subset of data is returned.
        return rr.bits[0:count]

    async def _write_holding_registers_pymodbus(
        self, address: int, *values: int, unit: int
    ):
        wr = await self.client.protocol.write_registers(address, values, unit=unit)
        if wr.isError():
            raise modbus_exception_codes.get(wr.exception_code, IOError)

    async def _write_coils_pymodbus(self, address: int, *values: bool, unit: int):
        wr = await self.client.protocol.write_coils(address, values, unit=unit)
        if wr.isError():
            raise modbus_exception_codes.get(wr.exception_code, IOError)

    def get_modbus_blocks(self, source, address_shift):
        if address_shift:
            modbus_blocks = []
            for start, end in self.config["sources"][source]["blocks"]:
                modbus_blocks.append([start + address_shift, end + address_shift])
        else:
            return self.config["sources"][source]["blocks"]
        return modbus_blocks

    async def trigger_poll(self, source, address_shift=0, poll_interval=None):
        modbus_blocks = self.get_modbus_blocks(source, address_shift)
        # TODO replace poll interval with config patching
        # Checks device config
        try:
            poll_interval = self.config["sources"][source]["poll_interval"]
        except KeyError:
            pass
        # Overwrites device config if poll intervals exists in gateway config
        try:
            poll_interval = self.poll_intervals[source]
        except KeyError:
            pass
        # If all fails sets to 5
        if poll_interval is None:
            poll_interval = 5

        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Waiting for connection for {self.device_id}")
        await self.client.connected.wait()
        log.info(f"Starting poll pipeline for {self.device_id}")
        register_type = self.config["sources"][source].get("handle", "holding")
        read_handle = self.read_handles[register_type]

        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing modbus device {self.device_id} polling")
                return
            try:
                start = loop.time()
                # If connection is interrupted stops reading and waits for connection to be reestablished.
                if not self.client.connected.is_set():
                    await self.client.connected.wait()
                await self.poll_pipeline(modbus_blocks, source, read_handle)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(
                        f"Modbus device {self.device_id} cancelled without stop signal"
                    )
                    continue
            except asyncio.TimeoutError as e:
                log.error(e)
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            sleep_time = start - loop.time() + poll_interval
            if sleep_time > 0:
                await asyncio.sleep(start - loop.time() + poll_interval)

    async def poll_pipeline(self, blocks, source, read_handle):
        addr_map = pyaware.data_types.AddressMapUint16()
        for start, end in blocks:
            count = len(range(start, end))
            addr_map.merge(await self.read_registers(read_handle, start, count))
        timestamp = datetime.utcnow()
        if timestamp is None:
            timestamp = datetime.utcnow()
        device_data = {}
        for k, v in self.config["parameters"].items():
            if v.get("source") == source:
                try:
                    device_data.update(self.parameters[k].decode(addr_map))
                except KeyError:
                    pass
        await events.publish(
            f"process_data/{id(self)}",
            data=device_data,
            timestamp=timestamp,
            device_id=self.device_id,
        ).all()
        self.current_state.update(device_data)

    async def read_registers(
        self, read_handle: typing.Callable, address: int, count: int
    ):
        f"""
        Read modbus registers
        :param read_handle:
        :param address:
        :param count:
        :return:
        """
        addr_map = pyaware.data_types.AddressMapUint16()
        addr_map[address : address + count] = await read_handle(
            address, count, unit=self.unit
        )
        return addr_map

    async def process_data(self, data, timestamp, device_id):
        transformed_data = pyaware.transformations.transform(data, self.transformations)
        store_data, send_data, event_data = await asyncio.gather(
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("store", {}),
                transformed_data,
                timestamp,
            ),
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("send", {}),
                transformed_data,
                timestamp,
            ),
            pyaware.triggers.process.run_triggers(
                self.triggers.get("process", {}).get("event", {}),
                transformed_data,
                timestamp,
            ),
        )
        if store_data:
            memory_storage.update(store_data, topic=f"{self.device_id}")
            self.store_state.update(store_data)
        if send_data:
            memory_storage.update(send_data, topic=f"{self.device_id}")
            cached_data = memory_storage.pop(f"{self.device_id}")
            aggregated_data = pyaware.aggregations.aggregate(
                cached_data, self.aggregates
            )
            events.publish(
                f"trigger_send",
                data=aggregated_data,
                meta=self.dict(),
                timestamp=timestamp,
                topic_type="telemetry",
                device_id=self.device_id,
            )
            self.send_state.update(cached_data)
        if event_data:
            for param, value in event_data.items():
                events.publish(
                    f"parameter_trigger/{self.device_id}/{param}",
                    data=next(iter(value.values())),
                    timestamp=timestamp,
                )
            self.event_state.update(event_data)
        return send_data

    async def process_write(self, register_type: str, data: typing.Dict[str, int]):
        """
        Processes write to a modbus device.

        :param register_type: Type of register to be written to. i.e. "holding" OR "coils".
        :param data: Data as a dictionary in the format {"param1": data, "param2": data, ...} to be written.
        """
        # Initialise write handles for registers
        addr_maps = {
            handle: pyaware.data_types.AddressMapUint16()
            for handle in self.write_handles
        }
        for param_name, val in data.items():
            # Format data to encode differently if its ParamBits
            if type(self.parameters[param_name]) == pyaware.data_types.ParamBits:
                data_to_encode = val
            else:
                data_to_encode = {param_name: val}
            try:
                # Device specific register type of each parameter
                # In this case "coils" or "holding"
                source = self.config["parameters"][param_name]["source"]
                register_type = self.config["sources"][source]["handle"]
                # Write to the right register address map
                addr_map = addr_maps[register_type]
                self.parameters[param_name].encode(data_to_encode, addr_map)
            except KeyError:
                log.warning(
                    f"Invalid device config definition for {self.device_id}. Cannot write, skipping..."
                )
        # Gets contiguous address blocks
        # In the form: blocks = [[start1, end1], [start2, end2], ...]
        for register_type, addr_map in addr_maps.items():
            # Fetches write handle for each addr map.
            write_handle = self.write_handles[register_type]
            blocks = []
            index = 0
            sorted_addr_map = sorted(addr_map._buf.items())
            for addr, val in sorted_addr_map:
                if len(blocks) != (index + 1):
                    blocks.append([addr, addr])
                if (addr + 1) not in addr_map._buf.keys():
                    blocks[index][1] = addr
                    index += 1
            # Writes block to the modbus device
            for start, end in blocks:
                values = addr_map[start : end + 1]
                await self.write_registers(write_handle, start, values)

    async def write_registers(
        self, write_handle: typing.Callable, address: int, values: typing.List[int]
    ):
        f"""
        Write to modbus registers
        :param write_handle:
        :param address:
        :param values:
        :return:
        """
        await write_handle(address, *values, unit=self.unit)

    def identify(self):
        response = TopologyChildrenV2(
            values={},
            type=self.module_type,
            serial=self.device_id,
            children=[],
        )
        return response

    def dict(self):
        response = {"type": self.module_type}
        return response
