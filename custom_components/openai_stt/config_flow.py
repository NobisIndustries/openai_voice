"""
Config flow for OpenAI STT.
"""
from __future__ import annotations
from typing import Any
import voluptuous as vol
import logging
from urllib.parse import urlparse
import uuid

from homeassistant import data_entry_flow
from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.helpers.selector import selector
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_API_KEY,
    CONF_STT_MODEL,
    CONF_STT_LANGUAGE,
    CONF_STT_RESPONSE_FORMAT,
    CONF_URL,
    DOMAIN,
    STT_MODELS,
    STT_RESPONSE_FORMATS,
    DEFAULT_STT_MODEL,
    DEFAULT_STT_LANGUAGE,
    DEFAULT_STT_RESPONSE_FORMAT,
    OPENAI_STT_URL,
    UNIQUE_ID,
)

_LOGGER = logging.getLogger(__name__)

def generate_entry_id() -> str:
    return str(uuid.uuid4())

class OpenAISTTConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenAI STT."""
    VERSION = 1
    
    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors = {}
        
        data_schema = vol.Schema({
            vol.Optional(CONF_API_KEY): str,
            vol.Optional(CONF_URL, default=OPENAI_STT_URL): str,
            vol.Required(CONF_STT_MODEL, default=DEFAULT_STT_MODEL): selector({
                "select": {
                    "options": STT_MODELS,
                    "mode": "dropdown",
                    "sort": True,
                    "custom_value": True
                }
            }),
            vol.Optional(CONF_STT_LANGUAGE, default=DEFAULT_STT_LANGUAGE): str,
            vol.Optional(CONF_STT_RESPONSE_FORMAT, default=DEFAULT_STT_RESPONSE_FORMAT): selector({
                "select": {
                    "options": STT_RESPONSE_FORMATS,
                    "mode": "dropdown",
                    "sort": True,
                    "custom_value": False
                }
            }),
        })
        
        if user_input is not None:
            try:
                entry_id = generate_entry_id()
                user_input[UNIQUE_ID] = entry_id
                await self.async_set_unique_id(entry_id)
                hostname = urlparse(user_input.get(CONF_URL, OPENAI_STT_URL)).hostname
                return self.async_create_entry(
                    title=f"OpenAI STT ({hostname}, {user_input.get(CONF_STT_MODEL, DEFAULT_STT_MODEL)})",
                    data=user_input
                )
            except data_entry_flow.AbortFlow:
                return self.async_abort(reason="already_configured")
            except HomeAssistantError as e:
                _LOGGER.exception(str(e))
                errors["base"] = str(e)
            except ValueError as e:
                _LOGGER.exception(str(e))
                errors["base"] = str(e)
            except Exception as e:
                _LOGGER.exception(str(e))
                errors["base"] = "unknown_error"
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=user_input
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return OpenAISTTOptionsFlow(config_entry)

class OpenAISTTOptionsFlow(OptionsFlow):
    """Handle options flow for OpenAI STT."""
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input: dict | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
            
        # Build the options schema
        options_schema = vol.Schema({
            vol.Optional(
                CONF_STT_MODEL,
                default=self.config_entry.options.get(CONF_STT_MODEL, self.config_entry.data.get(CONF_STT_MODEL, DEFAULT_STT_MODEL))
            ): selector({
                "select": {
                    "options": STT_MODELS,
                    "mode": "dropdown",
                    "sort": True,
                    "custom_value": True
                }
            }),
            
            vol.Optional(
                CONF_STT_LANGUAGE,
                default=self.config_entry.options.get(CONF_STT_LANGUAGE, self.config_entry.data.get(CONF_STT_LANGUAGE, DEFAULT_STT_LANGUAGE))
            ): str,
            
            vol.Optional(
                CONF_STT_RESPONSE_FORMAT,
                default=self.config_entry.options.get(CONF_STT_RESPONSE_FORMAT, self.config_entry.data.get(CONF_STT_RESPONSE_FORMAT, DEFAULT_STT_RESPONSE_FORMAT))
            ): selector({
                "select": {
                    "options": STT_RESPONSE_FORMATS,
                    "mode": "dropdown",
                    "sort": True,
                    "custom_value": False
                }
            })
        })
        
        return self.async_show_form(step_id="init", data_schema=options_schema)