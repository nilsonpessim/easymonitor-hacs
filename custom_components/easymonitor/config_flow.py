"""Configuração do EasyMonitor no Home Assistant."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN

class EasyMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configuração da integração do EasyMonitor."""

    async def async_step_user(self, user_input=None):
        """Passo inicial da configuração via UI."""
        if user_input is not None:
            return self.async_create_entry(title="EasyMonitor", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
