from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.device_registry import async_get as async_get_dev_reg
from homeassistant.helpers.entity_registry import async_get as async_get_ent_reg, async_entries_for_device
from .const import DOMAIN
import logging

DOMAIN = "easymonitor"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Configura a integração EasyMonitor."""

    # Novo método recomendado para setups
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Serviço para remover dispositivo manualmente
    async def remover_dispositivo_service(call: ServiceCall):
        device_id = call.data.get("device_id")
        if not device_id:
            _LOGGER.warning("Nenhum device_id informado para remoção.")
            return

        dev_reg = async_get_dev_reg(hass)

        # Procura e remove o dispositivo
        for device in dev_reg.devices.values():
            identifiers = list(device.identifiers)
            if any(device_id in identifier for identifier in identifiers):
                _LOGGER.info(f"Removendo dispositivo {device.name} ({device.id})")
                dev_reg.async_remove_device(device.id)
                return

        _LOGGER.warning(f"Dispositivo com ID {device_id} não encontrado.")

    # Serviço para resetar o status do dispositivo (remove entidades e o próprio dispositivo)
    async def resetar_status_dispositivo_service(call: ServiceCall):
        device_id = call.data.get("device_id")
        if not device_id:
            _LOGGER.warning("Nenhum device_id informado para reset.")
            return

        dev_reg = async_get_dev_reg(hass)
        ent_reg = async_get_ent_reg(hass)

        # Encontra o dispositivo pelo identificador
        for device in dev_reg.devices.values():
            if device_id in {id[1] for id in device.identifiers}:
                # Remove todas as entidades do dispositivo
                for entity in async_entries_for_device(ent_reg, device.id):
                    ent_reg.async_remove(entity.entity_id)
                    _LOGGER.info(f"Entidade {entity.entity_id} removida.")

                # Remove o dispositivo
                dev_reg.async_remove_device(device.id)
                _LOGGER.info(f"Dispositivo {device.name} removido com sucesso.")
                return

        _LOGGER.warning(f"Dispositivo {device_id} não encontrado.")

    hass.services.async_register(DOMAIN, "remover_dispositivo", remover_dispositivo_service)
    hass.services.async_register(DOMAIN, "resetar_status_dispositivo", resetar_status_dispositivo_service)

    return True
