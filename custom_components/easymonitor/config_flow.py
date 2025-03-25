"""Fluxo de configuração para o EasyMonitor."""
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class EasyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gerencia o fluxo de configuração da integração EasyMonitor."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Passo inicial iniciado pelo usuário."""
        if user_input is not None:
            # Cria uma entrada única sem necessidade de opções
            return self.async_create_entry(title="EasyMonitor", data={})

        return self.async_show_form(step_id="user")
