import datetime
import os
from dataclasses import dataclass, field
import logging
import jwt

import pyaware.config
import pyaware.mqtt

log = logging.getLogger(__name__)


class MQTTConfigBase:
    """
    Used to store the cloud configuration information as well as keep jwt tokens fresh
    """

    device_id: str
    authentication_required: bool
    client_id: str
    host: str
    port: str
    keepalive: int
    bind_address: str
    clean_session: bool
    private_key_path: str
    ca_certs_path: str
    ssl_algorithm: str
    _private_key: str
    _token: str
    token_exp: datetime.datetime
    parsers: dict
    subscribe_qos: int
    publish_qos: int
    token_life: int
    serial_number: str = ""
    batch: bool = False
    batch_hold_off: float = 0.0
    batch_soft_limit_characters: int = 20000000
    batch_max_size: int = 268435455
    max_message_queue_size: int = 0
    max_in_flight_messages: int = 0
    backlog_enable: bool = False

    @property
    def private_key(self):
        if not self._private_key:
            try:
                with open(self.private_key_path, "r") as f:
                    self._private_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    "Could not find the ssl private key file as specified in the cloud config"
                ) from e
        return self._private_key

    @property
    def jwt_token(self):
        if datetime.datetime.utcnow() > self.token_exp - datetime.timedelta(minutes=1):
            self._create_jwt()
        return self._token

    def _create_jwt(self):
        pass

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        return self.__dataclass_fields__


def credential_factory(cred):
    def _tmp():
        return os.path.join(pyaware.config.aware_path, "credentials", cred)

    return _tmp


def default_gcp_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v1"},
            "model": {"name": "TelemetryV1"},
            "topic": "/devices/{device_id}/events/telemetry",
        },
        "config": {"topic": "/devices/{device_id}/config"},
        "errors": {"topic": "/devices/{device_id}/errors"},
        "commands": {"topic": "/devices/{device_id}/commands/#"},
        "attach": {"topic": "/devices/{device_id}/attach"},
        "state": {"model": {"name": "StateV1"}, "topic": "/devices/{device_id}/state"},
    }


def default_local_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v2"},
            "model": {"name": "TelemetryV2"},
            "topic": "devices/{gateway_id}/{device_id}/events/telemetry",
            "batchable_backlog": True,
        },
        "telemetry_serial": {
            "factory": {"name": "telemetry_v2"},
            "transforms": [
                {"name": "remove_keys", "keys": {"raw_values"}},
            ],
            "model": {"name": "TelemetryV2"},
            "topic": "devices/{gateway_id}/{device_id}/{serial_number}/events/telemetry",
            "batchable_backlog": True,
        },
        "config": {"topic": "devices/{gateway_id}/{device_id}/config"},
        "errors": {"topic": "devices/{gateway_id}/{device_id}/errors"},
        "commands": {"topic": "devices/{device_id}/{serial_number}/commands"},
        "command_response": {
            "model": {"name": "CommandResponseV1"},
            "topic": "devices/{gateway_id}/{device_id}/events/telemetry/commands",
        },
        "topology": {
            "model": {"name": "TopologyV2"},
            "topic": "devices/{gateway_id}/{device_id}/topology",
        },
        "topology_serial": {
            "model": {"name": "TopologyV2"},
            "topic": "devices/{gateway_id}/{device_id}/{serial_number}/topology",
        },
        "gateway_heartbeat": {
            "model": {"name": "HeartbeatV1"},
            "topic": "gateways/{gateway_id}/heartbeat",
            "cache": False,
        },
        "gateway_heartbeat_serial": {
            "model": {"name": "HeartbeatV1"},
            "topic": "gateways/{gateway_id}/{serial_number}/heartbeat",
            "cache": False,
        },
        "device_heartbeat_source": {
            "model": {"name": "EmptyPayload"},
            "topic": "devices/{gateway_id}/{device_id}/heartbeat/{source}",
            "cache": False,
        },
        "device_heartbeat_serial_source": {
            "model": {"name": "EmptyPayload"},
            "topic": "devices/{gateway_id}/{device_id}/{serial_number}/heartbeat/{source}",
            "cache": False,
        },
        "state": {
            "model": {"name": "StateV1"},
            "topic": "gateways/{gateway_id}/state",
            "retain": False,
        },
        "state_serial": {
            "model": {"name": "StateV1"},
            "topic": "gateways/{gateway_id}/{serial_number}/state",
            "retain": False,
        },
        "will": {
            "model": {"name": "MqttStatusV1"},
            "topic": "gateways/{gateway_id}/mqtt",
            "retain": False,
        },
        "mqtt_status": {
            "model": {"name": "MqttStatusV1"},
            "topic": "gateways/{gateway_id}/mqtt",
            "retain": False,
        },
        "will_serial": {
            "model": {"name": "MqttStatusV1"},
            "topic": "gateways/{gateway_id}/mqtt",
            "retain": False,
        },
        "mqtt_status_serial": {
            "model": {"name": "MqttStatusV1"},
            "topic": "gateways/{gateway_id}/mqtt",
            "retain": False,
        },
    }


@dataclass
class LocalConfig(MQTTConfigBase):
    client_id: str
    device_id: str
    gateway_id: str = ""
    serial_number: str = ""
    authentication_required: bool = False
    host: str = "127.0.0.1"
    port: str = 1883
    keepalive: int = 60
    bind_address: str = ""
    clean_session: bool = False
    parsers: dict = None
    subscribe_qos: int = 1
    publish_qos: int = 1
    token_life = 0
    batch: bool = True
    batch_hold_off: float = 5.0
    batch_max_size: int = 268435455
    max_message_queue_size: int = 100
    max_in_flight_messages: int = 100
    backlog_enable: bool = False

    def __post_init__(self):
        if self.parsers is None:
            self.parsers = default_local_parsers()
        else:
            # Overwrites base default parsers with ones defined in config and retains the rest of the parsers.
            mqtt_parsers = default_local_parsers()
            mqtt_parsers.update(self.parsers)
            self.parsers = mqtt_parsers


@dataclass
class GCPCloudConfig(MQTTConfigBase):
    """
    Used to store the cloud configuration information as well as keep jwt tokens fresh
    """

    device_id: str
    serial_number: str = ""
    gateway_id: str = ""
    project_id: str = "aware-iot"
    registry_id: str = "aware-iot"
    cloud_region: str = "asia-east1"
    host: str = "mqtt.googleapis.com"
    port: str = 8883
    keepalive: int = 60
    bind_address: str = ""
    clean_session: bool = True
    private_key_path: str = field(default_factory=credential_factory("rsa_private.pem"))
    ca_certs_path: str = field(default_factory=credential_factory("google_roots.pem"))
    ssl_algorithm: str = "RS256"
    token_life: int = 60  # In Minutes
    _private_key: str = ""
    _token: str = ""
    authentication_required: bool = True
    token_exp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.utcnow()
        + datetime.timedelta(minutes=10)
    )
    parsers: dict = field(default_factory=default_gcp_parsers)
    subscribe_qos: int = 1
    publish_qos: int = 1
    max_in_flight_messages: int = 100
    batch: bool = True
    batch_hold_off: float = 3.0
    batch_max_size: int = 268435455
    max_message_queue_size: int = 100
    backlog_enable: bool = False

    @property
    def client_id(self):
        if any(
            len(x) == 1
            for x in [
                self.project_id,
                self.cloud_region,
                self.registry_id,
                self.device_id,
            ]
        ):
            raise ValueError("Cannot return client id if not all parameters are set")
        return f"projects/{self.project_id}/locations/{self.cloud_region}/registries/{self.registry_id}/devices/{self.device_id}"

    @property
    def private_key(self):
        if not self._private_key:
            try:
                with open(self.private_key_path, "r") as f:
                    self._private_key = f.read()
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    "Could not find the ssl private key file as specified in the cloud config"
                ) from e
        return self._private_key

    @property
    def jwt_token(self):
        self._create_jwt()
        return self._token

    def _create_jwt(self):
        log.info("Creating new jwt token")
        token_exp = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=self.token_life
        )
        token = {
            # The time that the token was issued at
            "iat": datetime.datetime.utcnow(),
            # The time the token expires.
            "exp": token_exp,
            # The audience field should always be set to the GCP project id.
            "aud": self.project_id,
        }
        self._token = jwt.encode(token, self.private_key, algorithm=self.ssl_algorithm)
        self.token_exp = token_exp
