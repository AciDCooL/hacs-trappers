import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD

class TrappersConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # We could add test authentication here, but for simplicity we'll just accept it.
            return self.async_create_entry(title="Trappers", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
