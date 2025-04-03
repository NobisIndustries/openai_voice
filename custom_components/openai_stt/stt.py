"""
Support for OpenAI STT as a separate component.
"""
import logging
import async_timeout
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    Provider,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_API_KEY,
    CONF_STT_MODEL,
    CONF_STT_LANGUAGE,
    CONF_STT_RESPONSE_FORMAT,
    CONF_URL,
    DEFAULT_STT_MODEL,
    DEFAULT_STT_LANGUAGE,
    DEFAULT_STT_RESPONSE_FORMAT,
    OPENAI_STT_URL,
)
from .openaistt_engine import OpenAISTTEngine

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OpenAI STT platform from a config entry."""
    api_key = config_entry.data.get(CONF_API_KEY)
    model = config_entry.data.get(CONF_STT_MODEL, DEFAULT_STT_MODEL)
    language = config_entry.data.get(CONF_STT_LANGUAGE, DEFAULT_STT_LANGUAGE)
    response_format = config_entry.data.get(CONF_STT_RESPONSE_FORMAT, DEFAULT_STT_RESPONSE_FORMAT)
    url = config_entry.data.get(CONF_URL, OPENAI_STT_URL)
    
    engine = OpenAISTTEngine(
        api_key=api_key,
        model=model,
        language=language,
        url=url,
        response_format=response_format
    )
    
    async_add_entities([OpenAISTTProvider(hass, config_entry, engine)])

class OpenAISTTProvider(Provider):
    """The OpenAI STT API provider."""

    def __init__(self, hass, config_entry, engine):
        """Initialize OpenAI STT provider."""
        self.hass = hass
        self._config_entry = config_entry
        self._engine = engine
        self._attr_unique_id = f"{config_entry.entry_id}_stt"
        model_name = self._engine._model.split("-")[-1]
        self._attr_name = f"OpenAI {model_name}"

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._engine._language

    @property
    def supported_languages(self) -> list[str]:
        """Return the list of supported languages."""
        return self._engine.get_supported_langs()

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [
            AudioFormats.WAV,
            AudioFormats.MP3,
            AudioFormats.MP4,
            AudioFormats.OGG,
        ]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [
            AudioCodecs.PCM,
            AudioCodecs.MP3,
            AudioCodecs.OPUS,
        ]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return a list of supported bitrates."""
        return [
            AudioBitRates.BITRATE_8,
            AudioBitRates.BITRATE_16,
            AudioBitRates.BITRATE_24,
        ]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return a list of supported samplerates."""
        return [
            AudioSampleRates.SAMPLERATE_8000,
            AudioSampleRates.SAMPLERATE_16000,
            AudioSampleRates.SAMPLERATE_24000,
            AudioSampleRates.SAMPLERATE_44100,
            AudioSampleRates.SAMPLERATE_48000,
        ]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return a list of supported channels."""
        return [
            AudioChannels.CHANNEL_MONO,
            AudioChannels.CHANNEL_STEREO,
        ]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream
    ) -> SpeechResult:
        """Process an audio stream for speech recognition."""
        _LOGGER.debug(
            "Processing audio stream with language: %s, model: %s",
            metadata.language,
            self._engine._model,
        )
        
        # Collect audio data from the stream
        audio_data = b""
        async for chunk in stream:
            audio_data += chunk
        
        # If a language is specified in metadata, use it
        language = metadata.language if metadata.language else self._engine._language
        
        try:
            async with async_timeout.timeout(30):
                # Process the audio with the OpenAI STT engine
                def process_job():
                    return self._engine.process_audio(audio_data, language)
                
                text = await self.hass.async_add_executor_job(process_job)
                
                if text:
                    return SpeechResult(
                        text,
                        SpeechResultState.SUCCESS,
                    )
                return SpeechResult("", SpeechResultState.ERROR)
                
        except Exception as err:
            _LOGGER.error("Error processing audio: %s", err)
            return SpeechResult("", SpeechResultState.ERROR)