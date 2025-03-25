import json
import logging
import asyncio

from homeassistant.components import mqtt
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "tempCH1": {"name": "Temperatura CH1", "unit": "°C", "icon": "mdi:thermometer"},
    "tempCH2": {"name": "Temperatura CH2", "unit": "°C", "icon": "mdi:thermometer"},
    "humiCH1": {"name": "Umidade CH1", "unit": "%", "icon": "mdi:water-percent"},
    "humiCH2": {"name": "Umidade CH2", "unit": "%", "icon": "mdi:water-percent"},
    "voltageDC0": {"name": "Tensão DC0", "unit": "V", "icon": "mdi:flash"},
    "voltageDC1": {"name": "Tensão DC1", "unit": "V", "icon": "mdi:flash"},
    "voltageAC0": {"name": "Tensão AC0", "unit": None, "icon": "mdi:flash"},
}

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    mqtt_client = mqtt
    entities = {}

    async def device_discovered(msg):
        try:
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
                    info_payload = json.loads(info_msg.payload)
                    device_info_data.update(info_payload)
                    _LOGGER.info(f"[EasyMonitor] Info do dispositivo {device_id}: {info_payload}")
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

    await mqtt_client.async_subscribe(hass, "easymonitor/+/status", device_discovered, 1)

class EasyMonitorSensor(Entity):
    def __init__(self, hass, device_id, sensor_id, device_info):
        self._hass = hass
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._state = None

        self._attr_name = f"{SENSORS[sensor_id]['name']} ({device_id})"
        self._attr_unique_id = f"easymonitor_{device_id}_{sensor_id}"
        self._attr_device_class = None
        self._attr_native_unit_of_measurement = SENSORS[sensor_id]["unit"]
        self._attr_icon = SENSORS[sensor_id]["icon"]

        self._attr_device_info = DeviceInfo(
            identifiers={("easymonitor", device_id)},
            name=f"EasyMonitor {device_id}",
            manufacturer=device_info.get("manufacturer", "TechLabs"),
            model=device_info.get("model", "EasyMonitor"),
            sw_version=device_info.get("sw_version", "0.0.1")
        )

    async def async_added_to_hass(self):
        topic = f"easymonitor/{self._device_id}/{self._sensor_id}"

        async def message_received(msg):
            self._state = msg.payload
            self.async_write_ha_state()

        await mqtt.async_subscribe(self._hass, topic, message_received, 1)

    @property
    def state(self):
        return self._state
