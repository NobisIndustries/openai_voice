"""
Constants for OpenAI STT custom component
"""

DOMAIN = "openai_stt"
CONF_API_KEY = "api_key"
CONF_STT_MODEL = "model"
CONF_STT_LANGUAGE = "language"
CONF_URL = "url"
CONF_STT_RESPONSE_FORMAT = "response_format"
UNIQUE_ID = "unique_id"

STT_MODELS = ["whisper-1", "gpt-4o-mini-transcribe", "gpt-4o-transcribe"]
DEFAULT_STT_MODEL = "gpt-4o-mini-transcribe"
DEFAULT_STT_LANGUAGE = "en"
STT_RESPONSE_FORMATS = ["json", "text"]
DEFAULT_STT_RESPONSE_FORMAT = "text"

# Default endpoint for OpenAI transcriptions
OPENAI_STT_URL = "https://api.openai.com/v1/audio/transcriptions"