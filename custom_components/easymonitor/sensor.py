from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.entity import DeviceInfo
import logging

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "tempCH1": {"name": "Temperatura CH1", "unit": "°C", "icon": "mdi:thermometer"},
    "tempCH2": {"name": "Temperatura CH2", "unit": "°C", "icon": "mdi:thermometer"},
    "humiCH1": {"name": "Umidade CH1", "unit": "%", "icon": "mdi:water-percent"},
    "humiCH2": {"name": "Umidade CH2", "unit": "%", "icon": "mdi:water-percent"},
    "voltageDC0": {"name": "Tensão DC0", "unit": "V", "icon": "mdi:flash"},
    "voltageDC1": {"name": "Tensão DC1", "unit": "V", "icon": "mdi:flash"},
    "voltageAC0": {"name": "Tensão AC0", "unit": "V", "icon": "mdi:flash"}
}

async def async_setup_entry(hass: HomeAssistantType, config_entry, async_add_entities):
    """Configura automaticamente os sensores MQTT do EasyMonitor."""
    mqtt = hass.components.mqtt
    entities = {}

    async def device_discovered(msg):
        topic_parts = msg.topic.split("/")
        if len(topic_parts) < 3:
            return

        device_id = topic_parts[1]

        if device_id not in entities:
            entities[device_id] = []
            _LOGGER.info(f"Novo dispositivo detectado: {device_id}")

            for sensor_id in SENSORS:
                entity = EasyMonitorSensor(mqtt, device_id, sensor_id)
                entities[device_id].append(entity)
                async_add_entities([entity], True)

    await mqtt.async_subscribe("easymonitor/+/status", device_discovered, 1)

class EasyMonitorSensor(Entity):
    """Representa um sensor EasyMonitor baseado em MQTT."""

    def __init__(self, mqtt, device_id, sensor_id):
        """Inicializa o sensor."""
        self._mqtt = mqtt
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._state = None
        self._attr_name = f"{SENSORS[sensor_id]['name']} ({device_id})"
        self._attr_unique_id = f"easymonitor_{device_id}_{sensor_id}"
        self._attr_device_class = None
        self._attr_native_unit_of_measurement = SENSORS[sensor_id]["unit"]
        self._attr_icon = SENSORS[sensor_id]["icon"]

        # 🔥 Adicionando Device Info para agrupar sensores em dispositivos
        self._attr_device_info = DeviceInfo(
            identifiers={(f"easymonitor_{device_id}")},
            name=f"EasyMonitor {device_id}",
            manufacturer="TechLabs",
            model="EasyMonitor",
            sw_version="1.0.1"
        )

    async def async_added_to_hass(self):
        """Subscreve ao tópico MQTT correspondente."""
        topic = f"easymonitor/{self._device_id}/{self._sensor_id}"

        async def message_received(msg):
            self._state = msg.payload
            self.async_write_ha_state()

        await self._mqtt.async_subscribe(topic, message_received, 1)

    @property
    def state(self):
        return self._state
