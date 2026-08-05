import logging

from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
)

from homeassistant.const import (
    UnitOfTemperature,
    UnitOfSpeed,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            GeoSphereWeather(coordinator)
        ]
    )


class GeoSphereWeather(
    CoordinatorEntity,
    WeatherEntity
):

    _attr_has_entity_name = True

    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_HOURLY
        |
        WeatherEntityFeature.FORECAST_DAILY
    )

    _attr_native_temperature_unit = (
        UnitOfTemperature.CELSIUS
    )

    _attr_native_wind_speed_unit = (
        UnitOfSpeed.KILOMETERS_PER_HOUR
    )


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator
        )

        self._attr_unique_id = (
            "geosphere_weather"
        )

        self._attr_name = (
            "GeoSphere Austria"
        )


    @property
    def native_temperature(self):

        try:
            return (
                self.coordinator.data
                ["properties"]
                ["parameters"]
                ["t2m"]
                ["data"][0]
            )

        except Exception:
            return None


    @property
    def native_humidity(self):

        try:
            return (
                self.coordinator.data
                ["properties"]
                ["parameters"]
                ["rh2m"]
                ["data"][0]
            )

        except Exception:
            return None


    @property
    def condition(self):

        return "sunny"