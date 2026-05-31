import voluptuous as vol
from homeassistant import config_entries, core
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

    @staticmethod
    @core.callback
    def async_get_options_flow(config_entry):
        return TrappersOptionsFlowHandler(config_entry)

class TrappersOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        from .const import CONF_GIFTCARD_COST, CONF_PAYOUT_GOAL, DEFAULT_GIFTCARD_COST, DEFAULT_PAYOUT_GOAL
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_GIFTCARD_COST, default=self.config_entry.options.get(CONF_GIFTCARD_COST, DEFAULT_GIFTCARD_COST)): int,
                vol.Required(CONF_PAYOUT_GOAL, default=self.config_entry.options.get(CONF_PAYOUT_GOAL, DEFAULT_PAYOUT_GOAL)): int,
            })
        )
