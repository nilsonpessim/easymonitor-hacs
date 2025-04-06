from homeassistant.components import mqtt
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.core import HomeAssistant

import json
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "tempCH1": {"name": "tempch1", "unit": "°C", "icon": "mdi:thermometer"},
    "tempCH2": {"name": "tempch2", "unit": "°C", "icon": "mdi:thermometer"},
    "humiCH1": {"name": "humich1", "unit": "%", "icon": "mdi:water-percent"},
    "humiCH2": {"name": "humich2", "unit": "%", "icon": "mdi:water-percent"},
    "voltageDC0": {"name": "voltagedc0", "unit": "V", "icon": "mdi:flash"},
    "voltageDC1": {"name": "voltagedc1", "unit": "V", "icon": "mdi:flash"},
    "voltageAC0": {"name": "voltageac0", "unit": "", "icon": "mdi:transmission-tower"},
}

DEVICE_CLASSES = {
    "tempCH1": "temperature",
    "tempCH2": "temperature",
    "humiCH1": "humidity",
    "humiCH2": "humidity",
    "voltageDC0": "voltage",
    "voltageDC1": "voltage",
    "voltageAC0": "voltage",
}


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    mqtt_client = mqtt
    entities = {}

    async def device_discovered(msg):
        try:
            if not msg.payload.strip():
                # _LOGGER.warning("[EasyMonitor] Payload de status vazio, ignorado.")
                return

            payload = json.loads(msg.payload)

            device_id = payload["device"]
            sensor_list = payload["sensors"]
        except Exception as e:
            _LOGGER.error(f"Erro ao processar payload MQTT de status: {e}")
            return

        if not device_id or not isinstance(sensor_list, list):
            _LOGGER.warning(f"[EasyMonitor] Payload de status inválido: {msg.payload}")
            return

        if device_id not in entities:
            entities[device_id] = []
            _LOGGER.info(f"[EasyMonitor] Novo dispositivo detectado: {device_id}")

            # Inicializa com valores padrão
            device_info_data = {
                "manufacturer": "TechLabs",
                "model": "EasyMonitor",
                "sw_version": "0.0.1"
            }

            # Aguarda info opcional publicada no tópico /info
            info_topic = f"easymonitor/{device_id}/info"
            event = asyncio.Event()

            async def info_callback(info_msg):
                try:
                    if not info_msg.payload.strip():
                       #  _LOGGER.warning(f"[EasyMonitor] Payload de info vazio para {device_id}, ignorado.")
                        return
                    
                    info_payload = json.loads(info_msg.payload)
                    device_info_data.update(info_payload)
                    _LOGGER.info(f"[EasyMonitor] Info do dispositivo {device_id}: {info_payload}")

                    device_registry = async_get_device_registry(hass)
                    device = device_registry.async_get_device(identifiers={("easymonitor", device_id)})

                    if device:
                        device_registry.async_update_device(
                            device.id,
                            name=f"{info_payload.get('name', 'EasyMonitor')} - {device_id}",
                            manufacturer=info_payload.get("manufacturer", "TechLabs"),
                            model=info_payload.get("model", "EasyMonitor"),
                            sw_version=info_payload.get("sw_version", "0.0.1"),
                            configuration_url=f"http://{info_payload.get('ip', '0.0.0.0')}"
                        )

                except Exception as e:
                    _LOGGER.warning(f"[EasyMonitor] Falha ao processar info: {e}")
                finally:
                    event.set()

            await mqtt_client.async_subscribe(hass, info_topic, info_callback, 1)

            try:
                await asyncio.wait_for(event.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                _LOGGER.warning(f"[EasyMonitor] Timeout esperando info do dispositivo {device_id}")

            for sensor_id in sensor_list:
                if sensor_id in SENSORS:
                    entity = EasyMonitorSensor(hass, device_id, sensor_id, device_info_data)
                    entities[device_id].append(entity)
                    async_add_entities([entity], True)
                else:
                    _LOGGER.warning(f"[EasyMonitor] Sensor desconhecido: {sensor_id}")

            labels_topic = f"easymonitor/{device_id}/labels"
            async def labels_callback(labels_msg):
                try:

                    if not labels_msg.payload.strip():
                        #_LOGGER.debug(f"[EasyMonitor] Payload de labels vazio para {device_id}, ignorado.")
                        return
                    
                    labels_payload = json.loads(labels_msg.payload)

                    for sensor in entities[device_id]:
                        sid = sensor._sensor_id
                        if sid in labels_payload:
                            new_name = labels_payload[sid]
                            sensor._attr_name = f"{new_name}"
                            sensor.async_write_ha_state()
                            _LOGGER.info(f"[EasyMonitor] Nome do sensor '{sid}' atualizado para '{new_name}'")
                except Exception as e:
                    _LOGGER.warning(f"[EasyMonitor] Erro ao processar labels: {e}")

            await mqtt_client.async_subscribe(hass, labels_topic, labels_callback, 1)

    await mqtt_client.async_subscribe(hass, "easymonitor/+/status", device_discovered, 1)

class EasyMonitorSensor(SensorEntity):
    def __init__(self, hass, device_id, sensor_id, device_info):
        self._hass = hass
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._state = None
        self._attr_unique_id = f"{device_id.lower()}_{SENSORS[sensor_id]['name']}"
        self.entity_id = f"sensor.{device_id.lower()}_{SENSORS[sensor_id]['name']}"
        self._attr_icon = SENSORS[sensor_id]["icon"]
        self._attr_should_poll = False
        self._attr_force_update = True

        if sensor_id != "voltageAC0":
            self._attr_device_class = DEVICE_CLASSES.get(sensor_id)
            self._attr_native_unit_of_measurement = SENSORS[sensor_id]["unit"]
        else:
            self._attr_device_class = None
            self._attr_native_unit_of_measurement = None

        self._attr_device_info = DeviceInfo(
            identifiers={("easymonitor", device_id)},
            name=f"{device_info.get('name', 'EasyMonitor')} - {device_id}",
            manufacturer=device_info.get("manufacturer", "TechLabs"),
            model=device_info.get("model", "EasyMonitor"),
            sw_version=device_info.get("sw_version", "0.0.1"),
            configuration_url=f"http://{device_info.get('ip', '0.0.0.0')}",
            connections=[(CONNECTION_NETWORK_MAC, device_info.get("mac", "BE:BA:CA:FE:C0:CA"))]
        )

    @property
    def native_value(self):
        try:
            return float(self._state)
        except (ValueError, TypeError):
            return self._state

    async def async_added_to_hass(self):
        topic = f"easymonitor/{self._device_id}/{self._sensor_id}"

        async def message_received(msg):

            payload = msg.payload.strip()
            if payload == "":
                _LOGGER.debug(f"[EasyMonitor] Payload vazio recebido para {self._attr_unique_id}, ignorando.")
                return

            self._state = msg.payload
            self.async_write_ha_state()

        await mqtt.async_subscribe(self._hass, topic, message_received, 1)

