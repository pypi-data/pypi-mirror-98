import platform
import asyncio
import logging
import pyaware
from datetime import datetime
from dataclasses import dataclass
from pyaware.mqtt.models import TopologyV2, TopologyChildrenV2
from pyaware.mqtt.client import Mqtt
from pyaware import watchdog
import time

from pyaware import events

import ifaddr
from ifaddr import Adapter

log = logging.getLogger(__file__)


@events.enable
@dataclass
class GatewayIPC:
    eth_interface: str
    gateway_id: str = ""
    device_id: str = ""
    serial_number: str = ""
    include_serial: bool = False
    ip_address: str = ""
    cloud_broker: Mqtt = None
    adapter: Adapter = None

    def __post_init__(self):
        self.topologies = {}
        # Get adapter object from name
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            if adapter.nice_name == self.eth_interface:
                self.adapter = adapter
                break
        self.identify()
        if self.include_serial:
            self.topic_types = {
                "state": "state_serial",
                "topology": "topology_serial",
                "heartbeat": "gateway_heartbeat_serial",
            }
        else:
            self.topic_types = {
                "state": "state",
                "topology": "topology",
                "heartbeat": "gateway_heartbeat",
            }
        events.publish("request_topology")

    def init(self):
        if self.adapter:
            asyncio.create_task(self.send_gateway_heartbeat())
        else:
            log.warning(
                f"No valid adapter found matching the input {self.eth_interface}. Cannot start gateway"
                f"heatbeat"
            )
        asyncio.create_task(self.update_state())
        self.setup_watchdogs()

    def setup_watchdogs(self):
        try:
            self.cloud_broker.client.on_connect = watchdog.watch(
                f"ipc_cloud_comms_status_{id(self)}"
            )(self.cloud_broker.client.on_connect)
        except AttributeError:
            pass
        try:
            self.cloud_broker.client.publish = watchdog.watch(
                f"ipc_cloud_comms_status_{id(self)}"
            )(self.cloud_broker.client.publish)
        except AttributeError:
            pass
        try:
            self.cloud_broker.client.on_disconnect = watchdog.watch_starve(
                f"ipc_cloud_comms_status_{id(self)}"
            )(self.cloud_broker.client.on_disconnect)
        except AttributeError:
            pass
        dog_eth = watchdog.WatchDog(
            heartbeat_time=60,
            success_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"cloud-comms-status": True},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
            failure_cbf=lambda: events.publish(
                f"process_data/{id(self)}",
                data={"cloud-comms-status": False},
                timestamp=datetime.utcnow(),
                device_id=self.device_id,
            ),
        )
        watchdog.manager.add(f"ipc_cloud_comms_status_{id(self)}", dog_eth)
        dog_eth.start(start_fed=False)

    async def update_state(self):
        log.info("Starting gateway update state")
        version = pyaware.__version__
        state = self.identify()
        state.values["version"] = version
        events.publish(
            f"trigger_send",
            topic_type=self.topic_types["state"],
            data=state.values,
            timestamp=datetime.utcnow(),
            device_id=self.device_id,
            gateway=self.gateway_id,
            serial_number=self.serial_number,
        )

    async def send_gateway_heartbeat(self):
        log.info("Starting gateway heartbeat writes")
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing gateway heartbeat")
                return
            try:
                await asyncio.sleep(5)
                ip_address = self.fetch_ip()
                if ip_address != self.ip_address:
                    self.ip_address = ip_address
                    self.update_topology()
                    asyncio.create_task(self.update_state())
                timestamp = datetime.utcnow()
                data = {"ipAddress": ip_address, "timestamp": timestamp}
                events.publish(
                    f"trigger_send",
                    data=data,
                    timestamp=timestamp,
                    topic_type=self.topic_types["heartbeat"],
                    device_id=self.device_id,
                    gateway=self.gateway_id,
                    serial_number=self.serial_number,
                )
                events.publish(
                    f"process_data/{id(self)}",
                    data={"heartbeat": time.time()},
                    timestamp=timestamp,
                    device_id=self.device_id,
                    gateway=self.gateway_id,
                )
                await asyncio.sleep(25)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("Gateway heartbeat cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    def fetch_ip(self) -> str:
        try:
            ip_addresses = self.adapter.ips
            for ip_address in ip_addresses:
                if ip_address.is_IPv4:
                    return ip_address.ip
        except BaseException as e:
            log.exception(e)

    def identify(self) -> TopologyV2:
        data = {}
        if self.ip_address != "":
            data["ipAddress"] = self.ip_address
        return TopologyV2(
            values=data,
            timestamp=datetime.utcnow(),
            children=list(self.topologies.values()),
        )

    @events.subscribe(topic="request_topology")
    def update_topology(self):
        """
        Updates the topology for a given device and resends all the currently connected devices
        :param data: Device topology payload derived from identify method
        :param timestamp: Timestamp of the topology
        :param topic: device_topology/{device_id}
        :return:
        """
        payload = self.identify()
        log.info(f"New topology:  {payload}")
        events.publish(
            f"trigger_send",
            data=payload,
            timestamp=datetime.utcnow(),
            topic_type=self.topic_types["topology"],
            device_id=self.device_id,
            gateway=self.gateway_id,
            serial_number=self.serial_number,
        )

    @events.subscribe(topic="device_topology/#", parse_topic=True)
    def build_topology(self, data, timestamp, topic):
        """
        Updates the topology for a given device and resends all the currently connected devices
        :param data: Device topology payload derived from identify method
        :param timestamp: Timestamp of the topology
        :param topic: device_topology/{device_id}
        :return:
        """
        device_id = topic.split("/")[-1]
        self.topologies[device_id] = data
        self.update_topology()
