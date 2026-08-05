from datetime import timedelta
import logging

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


class GeoSphereCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass: HomeAssistant,
        latitude: float,
        longitude: float,
    ):

        self.latitude = latitude
        self.longitude = longitude

        self.api_url = (
            "https://api.met.no/weatherapi/"
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                minutes=15
            ),
        )


    async def _async_update_data(self):

        try:

            async with aiohttp.ClientSession() as session:

                url = (
                    "https://dataset.api.hub.geosphere.at/"
                    "v1/timeseries/forecast/"
                    "location"
                )

                params = {
                    "lat": self.latitude,
                    "lon": self.longitude,
                    "parameters": (
                        "t2m,"
                        "rh2m,"
                        "rr_acc,"
                        "sy,"
                        "u10m,"
                        "v10m"
                    )
                }


                async with session.get(
                    url,
                    params=params,
                    timeout=30
                ) as response:

                    if response.status != 200:
                        raise UpdateFailed(
                            f"HTTP Fehler {response.status}"
                        )


                    data = await response.json()


                    _LOGGER.debug(
                        "GeoSphere keys: %s",
                        data.keys()
                    )


                    return data


        except Exception as err:

            raise UpdateFailed(
                f"GeoSphere Fehler: {err}"
            ) from err