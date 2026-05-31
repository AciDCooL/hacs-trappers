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
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            email = user_input.get(CONF_EMAIL)
            password = user_input.get(CONF_PASSWORD)
            
            import aiohttp
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "https://api.trappers.net/api/auth/v2/login",
                        json={"employeeEmail": email, "password": password},
                        headers={"Content-Type": "application/json", "User-Agent": "HomeAssistant"}
                    ) as response:
                        if response.status == 200:
                            # Update config entry data directly
                            new_data = dict(self._config_entry.data)
                            new_data[CONF_EMAIL] = email
                            new_data[CONF_PASSWORD] = password
                            self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)
                            
                            # Save the options
                            return self.async_create_entry(title="", data={
                                "giftcard_cost": user_input["giftcard_cost"],
                                "payout_goal": user_input["payout_goal"]
                            })
                        else:
                            errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "cannot_connect"

        from .const import CONF_GIFTCARD_COST, CONF_PAYOUT_GOAL, DEFAULT_GIFTCARD_COST, DEFAULT_PAYOUT_GOAL
        return self.async_show_form(
            step_id="init",
            errors=errors,
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL, default=self._config_entry.data.get(CONF_EMAIL, "")): str,
                vol.Required(CONF_PASSWORD, default=self._config_entry.data.get(CONF_PASSWORD, "")): str,
                vol.Required(CONF_GIFTCARD_COST, default=self._config_entry.options.get(CONF_GIFTCARD_COST, DEFAULT_GIFTCARD_COST)): int,
                vol.Required(CONF_PAYOUT_GOAL, default=self._config_entry.options.get(CONF_PAYOUT_GOAL, DEFAULT_PAYOUT_GOAL)): int,
            })
        )
