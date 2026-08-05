import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class GeoSphereConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN
):

    VERSION = 1


    async def async_step_user(
        self,
        user_input=None
    ):

        if user_input:

            return self.async_create_entry(
                title="GeoSphere Austria",
                data=user_input
            )


        schema = vol.Schema(
            {
                vol.Required(
                    "latitude",
                    default=48.23
                ): float,

                vol.Required(
                    "longitude",
                    default=13.57
                ): float,
            }
        )


        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )