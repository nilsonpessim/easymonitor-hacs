"""Integração EasyMonitor via MQTT."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "easymonitor"
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Configura a integração do EasyMonitor."""
    _LOGGER.info("Iniciando integração EasyMonitor")

    # Encaminha a configuração para o sensor.py
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True
