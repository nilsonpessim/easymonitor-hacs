import logging
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.mqtt import async_subscribe

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "status": "Status",
    "tempCH1": "Temperatura CH1",
    "tempCH2": "Temperatura CH2",
    "humiCH1": "Umidade CH1",
    "humiCH2": "Umidade CH2",
    "voltageDC0": "Tensão DC0",
    "voltageDC1": "Tensão DC1",
    "voltageAC0": "Tensão AC0"
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configura a integração EasyMonitor."""
    mqtt = hass.components.mqtt
    entities = []

    for sensor_id, name in SENSORS.items():
        entities.append(EasyMonitorSensor(mqtt, name, sensor_id))

    async_add_entities(entities)

class EasyMonitorSensor(SensorEntity):
    """Representa um sensor EasyMonitor que recebe dados via MQTT."""

    def __init__(self, mqtt, name, sensor_id):
        self._mqtt = mqtt
        self._name = name
        self._state = None
        self._sensor_id = sensor_id
        self._attr_name = f"EasyMonitor {name}"
        self._attr_unique_id = f"easymonitor_{sensor_id}"
        self._attr_device_class = "temperature" if "temp" in sensor_id else "voltage"

    @property
    def icon(self):
        """Define o ícone baseado no tipo do sensor."""
        if "temp" in self._sensor_id:
            return "mdi:thermometer"
        elif "humi" in self._sensor_id:
            return "mdi:water-percent"
        elif "voltage" in self._sensor_id:
            return "mdi:flash"
        return "mdi:chip"

