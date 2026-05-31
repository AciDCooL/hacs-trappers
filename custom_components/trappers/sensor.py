from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

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
        self._attr_unique_id = "trappers_euro_value"
        self._attr_native_unit_of_measurement = "€"
        self._attr_icon = "mdi:currency-eur"
        self._attr_state_class = SensorStateClass.TOTAL

    @property
    def native_value(self):
        balance = self.coordinator.data.get("balance", 0)
        return round(balance / 105, 2)

class TrappersEuroEarnedThisWeekSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Trappers Euro Earned This Week"
        self._attr_unique_id = "trappers_euro_earned_this_week"
        self._attr_native_unit_of_measurement = "€"
        self._attr_icon = "mdi:piggy-bank"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        days = self.coordinator.data.get("days_this_week", 0)
        return round(days * 154 / 105, 2)

class TrappersNextPayoutProgressSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Trappers Next Payout Progress"
        self._attr_unique_id = "trappers_next_payout_progress"
        self._attr_native_unit_of_measurement = "%"
        self._attr_icon = "mdi:cash-fast"

    @property
    def native_value(self):
        balance = self.coordinator.data.get("balance", 0)
        remainder = balance % 10500
        return round((remainder / 10500) * 100, 1)
