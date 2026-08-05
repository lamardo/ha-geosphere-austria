from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import GeoSphereCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry
) -> bool:


    coordinator = GeoSphereCoordinator(
        hass,
        entry.data.get(
            "latitude",
            48.23
        ),
        entry.data.get(
            "longitude",
            13.57
        ),
    )


    await coordinator.async_config_entry_first_refresh()


    hass.data.setdefault(
        DOMAIN,
        {}
    )


    hass.data[DOMAIN][entry.entry_id] = coordinator


    return True