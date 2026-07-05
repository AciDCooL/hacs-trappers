from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import (
    DOMAIN, 
    CONF_GIFTCARD_COST, 
    DEFAULT_GIFTCARD_COST,
    CONF_PAYOUT_GOAL, 
    DEFAULT_PAYOUT_GOAL
)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        TrappersSensor(coordinator, "balance", "Trappers Balance", "Trappers", "mdi:bicycle", SensorStateClass.TOTAL),
        TrappersSensor(coordinator, "workdays", "Trappers Workdays", "Days", "mdi:calendar-clock", None),
        TrappersSensor(coordinator, "total_trips", "Total Trappers Trips", "Trips", "mdi:counter", None),
        TrappersSensor(coordinator, "last_registration", "Trappers Last Registration", None, "mdi:calendar-check", None),
        TrappersSensor(coordinator, "last_reward", "Trappers Last Reward", "Trappers", "mdi:star-circle", None),
        TrappersSensor(coordinator, "days_this_week", "Trappers Days This Week", "Days", "mdi:calendar-check", None),
    ]
    
    # Custom templates
    sensors.append(TrappersEuroValueSensor(coordinator))
    sensors.append(TrappersEuroEarnedThisWeekSensor(coordinator))
    sensors.append(TrappersNextPayoutProgressSensor(coordinator))

    async_add_entities(sensors)

class TrappersSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit, icon, state_class):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        # HARDCODED: We use "trappers_" instead of entry_id to prevent breaking existing user dashboards.
        # This means users cannot currently install multiple Trappers accounts.
        self._attr_unique_id = f"trappers_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_state_class = state_class

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

class TrappersEuroValueSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Trappers Euro Value"
        # HARDCODED: Prevent breaking changes for existing users.
        self._attr_unique_id = "trappers_euro_value"
        self._attr_native_unit_of_measurement = "€"
        self._attr_icon = "mdi:currency-eur"
        self._attr_state_class = SensorStateClass.TOTAL

    @property
    def native_value(self):
        from .const import CONF_GIFTCARD_COST, DEFAULT_GIFTCARD_COST
        cost = self.coordinator.config_entry.options.get(CONF_GIFTCARD_COST, DEFAULT_GIFTCARD_COST)
        balance = self.coordinator.data.get("balance", 0)
        # 100 euro giftcard = cost trappers
        # 1 euro = cost / 100 trappers
        if cost == 0:
            return 0
        return round(balance / (cost / 100), 2)

class TrappersEuroEarnedThisWeekSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Trappers Euro Earned This Week"
        # HARDCODED: Prevent breaking changes for existing users.
        self._attr_unique_id = "trappers_euro_earned_this_week"
        self._attr_native_unit_of_measurement = "€"
        self._attr_icon = "mdi:piggy-bank"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        from .const import CONF_GIFTCARD_COST, DEFAULT_GIFTCARD_COST
        cost = self.coordinator.config_entry.options.get(CONF_GIFTCARD_COST, DEFAULT_GIFTCARD_COST)
        days = self.coordinator.data.get("days_this_week", 0)
        last_reward = self.coordinator.data.get("last_reward", 154)
        if cost == 0:
            return 0
        return round((days * last_reward) / (cost / 100), 2)

class TrappersNextPayoutProgressSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Trappers Next Payout Progress"
        # HARDCODED: Prevent breaking changes for existing users.
        self._attr_unique_id = "trappers_next_payout_progress"
        self._attr_native_unit_of_measurement = "%"
        self._attr_icon = "mdi:cash-fast"

    @property
    def native_value(self):
        goal = self.coordinator.config_entry.options.get(CONF_PAYOUT_GOAL, DEFAULT_PAYOUT_GOAL)
        balance = self.coordinator.data.get("balance", 0)
        if goal == 0:
            return 0
        remainder = balance % goal
        return round((remainder / goal) * 100, 1)
