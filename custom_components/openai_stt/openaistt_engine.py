"""
STT Engine for OpenAI Speech-to-Text.
"""
import json
import logging
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from asyncio import CancelledError

from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

class OpenAISTTEngine:
    """Engine for OpenAI STT capabilities."""
    
    def __init__(self, api_key: str, model: str, language: str, url: str, response_format: str = "text"):
        """Initialize the OpenAI STT engine."""
        self._api_key = api_key
        self._model = model
        self._language = language
        self._url = url
        self._response_format = response_format

    def process_audio(self, audio_data: bytes, language: str = None) -> str:
        """
        Synchronous STT request using urllib.request.
        If the API call fails, waits for 1 second and retries once.
        Returns transcribed text.
        """
        if language is None:
            language = self._language

        headers = {
            "Authorization": f"Bearer {self._api_key}" if self._api_key else None,
        }
        # Remove None headers
        headers = {k: v for k, v in headers.items() if v is not None}
        
        files = {
            'file': ('audio.wav', audio_data, 'audio/wav'),
            'model': (None, self._model),
            'response_format': (None, self._response_format),
        }
        
        if language:
            files['language'] = (None, language)

        max_retries = 1
        attempt = 0
        
        # Prepare multipart form data
        boundary = '----WebKitFormBoundary' + str(int(time.time()))
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        
        body = bytearray()
        for key, value in files.items():
            body.extend(f'--{boundary}\r\n'.encode('utf-8'))
            if isinstance(value, tuple):
                filename, content, content_type = value if len(value) == 3 else (value[0], value[1], None)
                if filename:
                    body.extend(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode('utf-8'))
                else:
                    body.extend(f'Content-Disposition: form-data; name="{key}"\r\n'.encode('utf-8'))
                if content_type:
                    body.extend(f'Content-Type: {content_type}\r\n'.encode('utf-8'))
                body.extend(b'\r\n')
                if isinstance(content, str):
                    body.extend(content.encode('utf-8'))
                else:
                    body.extend(content)
            else:
                body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8'))
                body.extend(str(value).encode('utf-8'))
            body.extend(b'\r\n')
        body.extend(f'--{boundary}--\r\n'.encode('utf-8'))
        
        while True:
            try:
                req = Request(
                    self._url,
                    data=body,
                    headers=headers,
                    method="POST"
                )
                # Set a timeout of 30 seconds for the entire request.
                with urlopen(req, timeout=30) as response:
                    content = response.read()
                    if self._response_format == "json":
                        result = json.loads(content.decode('utf-8'))
                        if isinstance(result, dict) and 'text' in result:
                            return result['text']
                        return result
                    # For text format or any other
                    return content.decode('utf-8')
            except CancelledError as ce:
                _LOGGER.exception("STT request cancelled")
                raise  # Propagate cancellation.
            except (HTTPError, URLError) as net_err:
                _LOGGER.exception("Network error in synchronous process_audio on attempt %d", attempt + 1)
                if attempt < max_retries:
                    attempt += 1
                    time.sleep(1)  # Wait for 1 second before retrying.
                    _LOGGER.debug("Retrying HTTP call (attempt %d)", attempt + 1)
                    continue
                else:
                    raise HomeAssistantError("Network error occurred while processing audio") from net_err
            except Exception as exc:
                _LOGGER.exception("Unknown error in synchronous process_audio on attempt %d", attempt + 1)
                if attempt < max_retries:
                    attempt += 1
                    time.sleep(1)
                    _LOGGER.debug("Retrying HTTP call (attempt %d)", attempt + 1)
                    continue
                else:
                    raise HomeAssistantError("An unknown error occurred while processing audio") from exc

    def close(self):
        """Nothing to close in the synchronous version."""
        pass

    @staticmethod
    def get_supported_langs() -> list:
        """Return all supported languages."""
        return [
            "af", "ar", "hy", "az", "be", "bs", "bg", "ca", "zh", "hr", "cs", "da", "nl", "en",
            "et", "fi", "fr", "gl", "de", "el", "he", "hi", "hu", "is", "id", "it", "ja", "kn",
            "kk", "ko", "lv", "lt", "mk", "ms", "mr", "mi", "ne", "no", "fa", "pl", "pt", "ro",
            "ru", "sr", "sk", "sl", "es", "sw", "sv", "tl", "ta", "th", "tr", "uk", "ur", "vi", "cy"
        ]