from __future__ import annotations
import struct
import typing
from collections import namedtuple, defaultdict
from dataclasses import dataclass, field
from math import log10, floor
import ruamel.yaml

from pyaware import log


def round_sig(x, sig=2):
    if x == 0:
        return x
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


class Endian:
    big = ">"
    little = "<"


c_decode = namedtuple("c_decode", ["format", "size"])
data_types = {
    "char": c_decode("c", 1),
    "schar": c_decode("b", 1),
    "uchar": c_decode("B", 1),
    "bool": c_decode("?", 1),
    "short": c_decode("h", 2),
    "ushort": c_decode("H", 2),
    "int": c_decode("i", 4),
    "uint": c_decode("I", 4),
    "long": c_decode("l", 4),
    "ulong": c_decode("L", 4),
    "longlong": c_decode("q", 8),
    "ulonglong": c_decode("Q", 8),
    "float": c_decode("f", 4),
    "double": c_decode("d", 8),
    "char[]": c_decode("s", None),
}


class AddressMap:
    def __init__(self, buffer: dict = None):
        if buffer is None:
            self._buf = {}
        else:
            self._buf = buffer

    def __getitem__(self, addr):
        """
        :param addr: Address int or slice of addresses to return
        :return:
        """
        if isinstance(addr, int):
            if addr < 0:
                raise TypeError("Address should be >= 0.")
            return self._buf[addr]
        elif isinstance(addr, slice):
            return [self._buf.get(i) for i in range(*slice_list(addr))]
        else:
            raise TypeError("Address has unsupported type")

    def __setitem__(self, key, value):
        """
        :param key: Int of the address
        :param value: Set the value of the item if the value is not None
        :return:
        """
        if isinstance(key, slice):
            for index, addr in enumerate(range(*slice_list(key))):
                if value[index] is not None:
                    self._buf[addr] = value[index]
        else:
            if value is not None:
                self._buf[key] = value

    def __delitem__(self, key):
        try:
            del self._buf[key]
        except KeyError:
            pass

    def __delslice__(self, i, j):
        for x in range(i, j):
            try:
                del self._buf[x]
            except KeyError:
                pass

    def __bool__(self):
        return bool(self._buf)

    def __eq__(self, another: AddressMap):
        """
        Used for tests to compare the buffers of two address maps.

        :param another: Address map to compare buffers with
        :returns: True if buffers are equal, False otherwise
        """
        return self._buf == another._buf

    def merge(self, addr: AddressMap):
        """
        Merges another address map into this existing address map

        :param addr: Address Map to merge into the selected map.
        :return: Merged Address Map
        """
        overlap = set(self._buf.keys()).intersection(set(addr._buf.keys()))
        if overlap:
            raise ValueError(
                "Cannot join AddressMap with overlapping addresses: {}".format(overlap)
            )

        self._buf.update(addr._buf)

    def update(self, addr: AddressMap, force: bool = False):
        """
        Updates another address map with this existing address map

        :param addr: Address Map to update the selected map with.
        :param force: If true the address map will be forced to update with the new address maps keys and values. If
        false the address map will not update if keys in the new address map did not exist in the base. Defaults to
        false.
        :return: Merged Address Map
        """
        if set(addr._buf).difference(set(self._buf)) and not force:
            raise ValueError(
                "Cannot add new keys to the address map. If you require this functionality enable the force option."
            )
        self._buf.update(addr._buf)

    def save_block(self, start_addr, values):
        for index, itm in enumerate(values):
            self._buf[start_addr + index] = itm

    def __repr__(self):
        return f"AddressMap: {self._buf}"

    def copy(self):
        return self.__class__(self._buf)


class AddressMapUint16(AddressMap):
    def __setitem__(self, key, value):
        """
        :param key: Int of the address
        :param value: Set the value of the item if the value is not None
        :return:
        """
        if isinstance(key, slice):
            if any(
                x
                for x in slice_list(key)
                if x is not None and not (0 <= x < 1 << 16) and not isinstance(x, int)
            ):
                raise OverflowError("Values provided are not UINT16 compatible")
        else:
            if (
                value is not None
                and not (0 <= value < 1 << 16)
                and not isinstance(value, int)
            ):
                raise OverflowError("Value provided is not UINT16 compatible")
        super().__setitem__(key, value)


def slice_list(slic):
    return [x for x in [slic.start, slic.stop, slic.step] if x is not None]


@dataclass
class Param:
    address: int
    idx: str
    scale: float = 1
    block: typing.Any = None
    significant_figures: typing.Optional[int] = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        result = addr_map[self.address] * self.scale
        if self.significant_figures:
            result = round_sig(result, self.significant_figures)
        return {self.idx: result}

    def encode(self, data, addr_map: AddressMapUint16):
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map

        value = round(value / self.scale)
        if value > 0xFFFF:
            raise OverflowError(
                f"Target value {data[self.idx]} when scaled 0x{value:02X} "
                f"is bigger than a 16 bit number"
            )
        addr_map[self.address] = value
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamStatic:
    idx: str
    value: typing.Any
    meta: dict = field(default_factory=dict)


@dataclass
class ParamBoolArray:
    address: [int]
    idx: str
    length: int
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or any(
            [True for addr in self.address if addr_map[addr] is None]
        ):
            return {}
        bin_number = ""
        for addr in self.address:
            bin_number += f"{addr_map[addr]:0>16b}"[::-1]
        bin_number = bin_number[: self.length]
        bin_arr = [int(x) for x in bin_number]
        return {self.idx: bin_arr}

    def encode(self, data, addr_map: AddressMapUint16):
        try:
            addr_map[self.address] = data[self.idx]
        except KeyError:
            pass
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamEnumBoolArray:
    address: [int]
    table: dict
    terminator: hex = None
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or any(
            [True for addr in self.address if addr_map[addr] is None]
        ):
            return {}
        params = {param: False for val, param in self.table.items()}
        for addr in self.address:
            value = addr_map[addr]
            # Assumes that values received are all 16 bit in size.
            value = struct.unpack("<H", struct.pack(">H", value))[0]
            if self.terminator is not None and value == self.terminator:
                break
            try:
                param = self.table[value]
            except KeyError:
                # Skip if value is not in enum i.e. not important
                continue
            params[param] = True
        return params

    def encode(self, data, addr_map: AddressMapUint16):
        # TODO: Implement an encode method for ParamEnumBoolArray
        raise NotImplementedError


@dataclass
class ParamText:
    address: int
    idx: str
    length: int
    block: typing.Any = None
    padding: typing.Union[bytes, int] = b"\x00"
    null_byte: bool = True
    swap_bytes: bool = False
    swap_words: bool = False
    strip_leading: str = ""
    strip_lagging: str = ""
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.padding, int):
            byt = bytearray(1)
            byt[0] = self.padding
            self.padding = bytes(byt)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        dec_str = bytearray()
        for x in addr_map[self.address : self.address + self.length]:
            if self.swap_bytes:
                dec_str.append((x & 0xFF00) >> 8)
                dec_str.append(x & 0xFF)
            else:
                dec_str.append(x & 0xFF)
                dec_str.append((x & 0xFF00) >> 8)
        dec_str = dec_str.strip(self.padding)
        dec_str = dec_str.replace(b"\x00", b"").decode("utf-8", "ignore")
        if self.strip_leading:
            dec_str = dec_str.lstrip(self.strip_leading)
        if self.strip_lagging:
            dec_str = dec_str.rstrip(self.strip_lagging)
        return {self.idx: dec_str}

    def encode(self, data, addr_map: AddressMapUint16):
        if len(data[self.idx]) > self.length * 2:
            raise ValueError(
                f"Invalid string length to pack into {self.idx} starting @ address: {self.address}"
            )
        addr_map[self.address : self.address + self.length * 2] = (
            [self.padding] * self.length * 2
        )
        for index, byt in data[self.idx].encode("utf-8"):
            addr_map[self.address + index // 2] += byt << (8 * index % 2)
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamDict:
    key: str
    idx: str
    table: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

    def decode(self, json_obj: dict):
        return {self.idx: self.table.get(json_obj[self.key], json_obj[self.key])}


@dataclass
class ParamBits:
    address: int
    bitmask: dict
    idx: typing.Optional[str] = None
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        parameter_value = addr_map[self.address]
        return {
            idx: bool(parameter_value & (1 << bit)) for idx, bit in self.bitmask.items()
        }

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        for idx, bit_shift in self.bitmask.items():
            try:
                data_bit = data[idx]
            except KeyError:
                # Data not relevant
                continue
            # Initialise the address map with the address if the address is not initialised already.
            # NOTE: This is required for the bit wise operations below.
            if self.address not in addr_map._buf:
                addr_map[self.address] = 0
            if data_bit:
                addr_map[self.address] |= 1 << bit_shift
            else:
                addr_map[self.address] &= ~(1 << bit_shift)
        return addr_map

    def keys(self):
        return set(self.bitmask)


@dataclass
class ParamMask:
    address: int
    idx: str
    mask: int = 0xFFFF
    rshift: int = 0
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        return {self.idx: ((addr_map[self.address] & self.mask) >> self.rshift)}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map
        if value << self.rshift > self.mask:
            raise OverflowError(
                f"Target value 0x{value:02X} when shifted 0x{value << self.rshift:02X} "
                f"is bigger than the target mask 0x{self.mask:02X}"
            )
        addr_map[self.address] &= ~self.mask
        addr_map[self.address] |= value << self.rshift
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamOffset(ParamMask):
    offset: int = 0

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        resp = super(ParamOffset, self).decode(addr_map, block)
        resp[self.idx] += self.offset
        return resp

    def encode(self, data: dict, addr_map: AddressMapUint16):
        data = data.copy()
        data[self.idx] -= self.offset
        return super(ParamOffset, self).encode(data, addr_map)

    def keys(self):
        return {self.idx}


class ParamMaskBool(ParamMask):
    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        try:
            decoded[self.idx] = bool(decoded[self.idx])
        except KeyError:
            pass
        return decoded


@dataclass
class ParamMaskScale:
    address: int
    idx: str
    mask: int = 0xFFFF
    rshift: int = 0
    block: typing.Any = None
    scale: float = 1.0
    significant_figures: typing.Optional[int] = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        result = ((addr_map[self.address] & self.mask) >> self.rshift) * self.scale
        if self.significant_figures:
            result = round_sig(result, self.significant_figures)
        return {self.idx: result}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = round(data[self.idx] / self.scale)
        except KeyError:
            return addr_map
        if value << self.rshift > self.mask:
            raise OverflowError(
                f"Target value {value} when shifted 0x{value << self.rshift:02X} "
                f"is bigger than the target mask 0x{self.mask:02X}"
            )
        addr_map[self.address] &= ~self.mask
        addr_map[self.address] |= value << self.rshift
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamLookup:
    address: int
    idx: str
    table: dict
    table_reversed: dict
    mask: int = 0xFFFF
    rshift: int = 0
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        try:
            assert block == self.block
            return {
                self.idx: self.table[
                    (addr_map[self.address] & self.mask) >> self.rshift
                ]
            }
        except (AssertionError, KeyError, TypeError):
            return {}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            if type(data[self.idx]) == bytes or type(data[self.idx]) == bytearray:
                data[self.idx] = data[self.idx].decode()
        except KeyError:
            return addr_map
        try:
            value = self.table_reversed[data[self.idx]]
        except KeyError:
            return addr_map
        # Initialise the address map with the address if the address is not initialised already.
        # NOTE: This is required for the bit wise operations below.
        if self.address not in addr_map._buf:
            addr_map[self.address] = 0
        addr_map[self.address] &= ~self.mask
        addr_map[self.address] |= value << self.rshift
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamCType:
    address: int
    idx: str
    data_type: str = "ushort"
    byte_order: str = ">"
    word_order: str = ">"
    block: typing.Any = None
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        param_type = data_types[self.data_type]
        data = addr_map[self.address : self.address + ((param_type.size + 1) // 2)]
        if any((x is None for x in data)) or block != self.block:
            return {}
        if self.word_order != ">":
            data = data[::-1]
        data_bytes = struct.pack(self.byte_order + "H" * len(data), *data)
        if self.byte_order == ">":
            data_bytes = data_bytes[len(data_bytes) - param_type.size :]
        else:
            data_bytes = data_bytes[: param_type.size]
        param = struct.unpack(f"{self.byte_order}{param_type.format}", data_bytes)[0]
        return {self.idx: param}

    def encode(self, data: dict, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map
        param_type = data_types[self.data_type]
        data_bytes = bytearray(param_type.size)
        offset = 0
        if self.byte_order == ">":
            byte_order = "<"
        else:
            byte_order = ">"
        if param_type.format == "c":
            value = bytes(value, "utf-8")
        try:
            struct.pack_into(byte_order + param_type.format, data_bytes, offset, value)
        except struct.error as e:
            log.exception(e)
            log.warning(
                f"Failed to encode ParamCType {self.idx}. Which produced this error -> {e}"
            )
        if param_type.size > 1:
            cast = "H"
        elif param_type.format == "c":
            cast = "b"
        else:
            cast = param_type.format
        param = memoryview(data_bytes).cast(cast).tolist()
        if self.word_order == ">":
            param = param[::-1]
        addr_map[self.address : self.address + ((param_type.size + 1) // 2)] = param
        return addr_map

    def get_address_range(self):
        """
        Returns the address range of the parameter

        :return: Array in the format [start_addr, end_addr]
        """
        param_type = data_types[self.data_type]
        start = self.address
        end = self.address + ((param_type.size + 1) // 2)
        return [start, end]

    def keys(self):
        return {self.idx}


@dataclass
class ParamCTypeScale(ParamCType):
    scale: float = 1.0
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        decoded[self.idx] = decoded[self.idx] * self.scale
        return decoded

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            return super().encode(
                {self.idx: int(data[self.idx] / self.scale)}, addr_map
            )
        except KeyError:
            return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamCTypeScaleModulus(ParamCType):
    modulus: int = 65535
    scale: float = 1.0
    invert_on_overflow: bool = False
    meta: dict = field(default_factory=dict)

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        val = decoded[self.idx] % self.modulus
        if val != decoded[self.idx] and self.invert_on_overflow:
            val = -val
        decoded[self.idx] = val * self.scale
        return decoded

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        return super().encode(int(data / self.scale) % self.modulus, addr_map)

    def keys(self):
        return {self.idx}


def build_from_device_config(path):
    with open(path) as f:
        parsed = ruamel.yaml.safe_load(f)
    return parse_data_types(parsed["parameters"], {})


def resolve_param(reference: dict, meta: dict) -> typing.Any:
    if reference["type"] == "value":
        return reference["value"]
    elif reference["type"] == "ref_param":
        ref = meta[reference["param"]]
        try:
            if reference["null_ref"] == ref:
                return None
        except KeyError:
            pass
        offset = reference.get("offset", 0)
        try:
            data = ref + offset
        except TypeError:
            data = ref
        return data
    else:
        raise ValueError(f"Invalid type {reference['type']} specified")


def resolve_param_dict(reference: dict, meta: dict):
    resolved = {}
    if "type" in reference:
        return resolve_param(reference, meta)
    else:
        for k, v in reference.items():
            if isinstance(v, dict):
                resolved[k] = resolve_param_dict(v, meta)
            elif isinstance(v, list):
                resolved[k] = resolve_param_list(v, meta)
            else:
                resolved[k] = v
    return resolved


def resolve_param_list(reference: list, meta: dict) -> list:
    resolved = []
    for itm in reference:
        if isinstance(itm, dict):
            resolved.append(resolve_param_dict(itm, meta))
        elif isinstance(itm, list):
            resolved.append(resolve_param_list(itm, meta))
        else:
            resolved.append(itm)
    return resolved


def parse_data_type_class(*, type: str, meta: dict, **kwargs):
    cls = globals()[type]
    form = resolve_param_dict(kwargs, meta)
    inst = cls(**form)
    return inst


def parse_data_types(parameters, meta: dict):
    params = {}
    for idx, param in parameters.items():
        try:
            params[idx] = parse_data_type_class(**param["form"], meta=meta)
        except:
            continue
    return params


def parse_data_types_by_source(parameters, meta: dict):
    params = defaultdict(dict)
    for idx, param in parameters.items():
        try:
            params[param["source"]][idx] = parse_data_type_class(
                **param["form"], meta=meta
            )
        except KeyError:
            continue
    return params


def resolve_static_data_types(parameters, meta: dict):
    params = defaultdict(dict)
    for idx, param in parameters.items():
        try:
            if param["source"] == "static":
                params[idx] = parse_data_type_class(**param["form"], meta=meta).value
        except KeyError:
            continue
    return params
