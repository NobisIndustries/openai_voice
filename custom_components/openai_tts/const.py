"""
Constants for OpenAI TTS custom component
"""

DOMAIN = "openai_tts"
CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_VOICE = "voice"
CONF_SPEED = "speed"
CONF_URL = "url"
UNIQUE_ID = "unique_id"

MODELS = ["tts-1", "tts-1-hd", "gpt-4o-mini-tts"]
VOICES = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]

CONF_CHIME_ENABLE = "chime"
CONF_CHIME_SOUND = "chime_sound"
CONF_NORMALIZE_AUDIO = "normalize_audio"
CONF_INSTRUCTIONS = "instructions"

# STT-specific constants
STT_DOMAIN = "openai_stt"
CONF_STT_MODEL = "stt_model"
CONF_STT_LANGUAGE = "stt_language"
STT_MODELS = ["whisper-1", "gpt-4o-mini-transcribe", "gpt-4o-transcribe"]
DEFAULT_STT_MODEL = "gpt-4o-mini-transcribe"
DEFAULT_STT_LANGUAGE = "en"
CONF_STT_RESPONSE_FORMAT = "response_format"
STT_RESPONSE_FORMATS = ["json", "text"]
DEFAULT_STT_RESPONSE_FORMAT = "text"