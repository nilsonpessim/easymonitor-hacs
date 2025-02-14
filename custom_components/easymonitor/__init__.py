"""Integração EasyMonitor via MQTT."""
import logging

from homeassistant.helpers.discovery import async_load_platform
from homeassistant.const import Platform

DOMAIN = "easymonitor"
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Configura a integração do EasyMonitor."""
    hass.async_create_task(async_load_platform(hass, Platform.SENSOR, DOMAIN, {}, entry))
    return True
