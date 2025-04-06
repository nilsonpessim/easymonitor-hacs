import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import device_registry as dr
from homeassistant.components import mqtt

_LOGGER = logging.getLogger(__name__)
DOMAIN = "easymonitor"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    return unload_ok

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    # Registrar serviço para remover dispositivo
    async def remover_dispositivo_service(call: ServiceCall):
        device_id = call.data.get("device_id")
        if not device_id:
            _LOGGER.warning("[EasyMonitor] device_id não fornecido para remoção.")
            return

        device_registry = dr.async_get(hass)
        for device in dr.async_entries_for_config_entry(device_registry, entry.entry_id):
            identifiers = list(device.identifiers)[0]
            if identifiers[1] == device_id:
                device_registry.async_remove_device(device.id)
                _LOGGER.info(f"[EasyMonitor] Dispositivo {device_id} removido do registro.")

        # Tópicos MQTT retidos a serem limpos
        topics = [
            f"easymonitor/{device_id}/voltageAC0",
            f"easymonitor/{device_id}/voltageDC0",
            f"easymonitor/{device_id}/voltageDC1",
            f"easymonitor/{device_id}/tempCH1",
            f"easymonitor/{device_id}/humiCH1",
            f"easymonitor/{device_id}/tempCH2",
            f"easymonitor/{device_id}/humiCH2",
            f"easymonitor/{device_id}/labels",
            f"easymonitor/{device_id}/status",
            f"easymonitor/{device_id}/info"
        ]

        for topic in topics:
            await mqtt.async_publish(hass, topic, "", retain=True)
            _LOGGER.info(f"[EasyMonitor] Tópico MQTT limpo: {topic}")

    hass.services.async_register(DOMAIN, "remover_dispositivo", remover_dispositivo_service)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_remove_config_entry_device(hass, config_entry: ConfigEntry, device_entry: DeviceEntry) -> bool:
    identifiers = device_entry.identifiers
    for domain, device_id in identifiers:
        if domain == "easymonitor":
            try:
                topics_to_clear = [
                    f"easymonitor/{device_id}/voltageAC0",
                    f"easymonitor/{device_id}/voltageDC0",
                    f"easymonitor/{device_id}/voltageDC1",
                    f"easymonitor/{device_id}/tempCH1",
                    f"easymonitor/{device_id}/humiCH1",
                    f"easymonitor/{device_id}/tempCH2",
                    f"easymonitor/{device_id}/humiCH2",
                    f"easymonitor/{device_id}/labels",
                    f"easymonitor/{device_id}/status",
                    f"easymonitor/{device_id}/info"
                ]
                for topic in topics_to_clear:
                    await mqtt.async_publish(hass, topic, "", retain=True)
                _LOGGER.info(f"[EasyMonitor] Tópicos MQTT limpos para {device_id}")
            except Exception as e:
                _LOGGER.error(f"[EasyMonitor] Falha ao limpar tópicos MQTT para {device_id}: {e}")
            return True
    return False

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle reload of an entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)