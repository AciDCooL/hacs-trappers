import logging
import datetime
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, UPDATE_INTERVAL, CONF_EMAIL, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

class TrappersDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.email = entry.data[CONF_EMAIL]
        self.password = entry.data[CONF_PASSWORD]
        self.config_entry = entry

    async def _async_update_data(self):
        try:
            session = async_get_clientsession(self.hass)
            # 1. Login
            login_payload = {"employeeEmail": self.email, "password": self.password}
            async with session.post("https://api.trappers.net/api/auth/v2/login", json=login_payload) as resp:
                resp.raise_for_status()
                login_data = await resp.json()
                token = login_data['token']
                user_details = login_data['userDetails']

            headers = {'Authorization': f'Bearer {token}'}

            # 2. Get Events
            async with session.post("https://api.trappers.net/api/events?limit=20&offset=0", json={}, headers=headers) as resp:
                resp.raise_for_status()
                events_data = await resp.json()

            # 3. Get Transactions
            async with session.get("https://api.trappers.net/api/transactions?limit=1&offset=0", headers=headers) as resp:
                resp.raise_for_status()
                transactions_data = await resp.json()

            # Calculate days this week
            days_this_week = 0
            today = datetime.datetime.now()
            for item in events_data.get('items', []):
                if item.get('status') != 'PROCESSED':
                    continue
                try:
                    dt = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
                    if dt.isocalendar()[1] == today.isocalendar()[1] and dt.year == today.year:
                        days_this_week += 1
                except Exception:
                    pass

            last_reward = transactions_data['items'][0]['amount'] if transactions_data.get('items') else 0
            last_registration = events_data['items'][0]['date'] if events_data.get('items') else "unknown"

            return {
                "balance": user_details.get('balance', 0),
                "workdays": user_details.get('numberOfWorkdays', 0),
                "total_trips": events_data.get('total', 0),
                "last_registration": last_registration,
                "last_reward": last_reward,
                "days_this_week": days_this_week
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
