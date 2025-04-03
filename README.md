# OpenAI Speech Services Custom Component for Home Assistant

This custom component provides integration with OpenAI's speech services for Home Assistant, offering both Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities.

## Features  

### Text-to-Speech Features

- **Text-to-Speech** conversion using OpenAI's API  
- **Support for multiple languages and voices** – No special configuration needed; the AI model auto-recognizes the language.  
- **Customizable speech model** – [Check supported voices and models](https://platform.openai.com/docs/guides/text-to-speech).  
- **Integration with Home Assistant** – Works seamlessly with assistants, automations, and scripts.  
- **Custom endpoint option** – Allows you to use your own OpenAI compatible API endpoint.
- **Chime option** – Useful for announcements on speakers. *(See Devices → OpenAI TTS → CONFIGURE button)*
- **User-configurable chime sounds** – Drop your own chime sound into  `config/custom_components/openai_tts/chime` folder (MP3).
- **Audio normalization option** – Uses more CPU but improves audio clarity on mobile phones and small speakers. *(See Devices → OpenAI TTS → CONFIGURE button)*
- **Support for new gpt-4o-mini-tts model** – A fast and powerful language model.
- **Text-to-Speech Instructions option** – Instruct the text-to-speech model to speak in a specific way (only works with newest gpt-4o-mini-tts model). [OpenAI new generation audio models](https://openai.com/index/introducing-our-next-generation-audio-models/)

### NEW: Speech-to-Text Features

- **Speech-to-Text** conversion using OpenAI's latest models
- **Support for new models** – Uses the latest GPT-4o models for transcription: `gpt-4o-mini-transcribe` (default) and `gpt-4o-transcribe`
- **Legacy model support** – Also supports the original Whisper model (`whisper-1`)
- **Multiple language support** – Automatically detects and transcribes in many languages
- **Customizable response format** – Choose between JSON or text output
- **Integration with Home Assistant** – Works with assistants, automations, and voice commands
- **Supports multiple audio formats** – Works with WAV, MP3, MP4, and OGG files
- **High accuracy** – Leverages OpenAI's state-of-the-art transcription models for superior results

### *Caution! You need an OpenAI API key and some balance available in your OpenAI account!* ###
visit: (https://platform.openai.com/docs/pricing)

## YouTube sample video (TTS demo)

[![OpenAI TTS Demo](https://img.youtube.com/vi/oeeypI_X0qs/0.jpg)](https://www.youtube.com/watch?v=oeeypI_X0qs)

## Sample Home Assistant services

### TTS Service Example

```yaml
service: tts.speak
target:
  entity_id: tts.openai_nova_engine
data:
  cache: true
  media_player_entity_id: media_player.bedroom_speaker
  message: My speech has improved now!
  options:
    chime: true                          # Enable or disable the chime
    instructions: "Speak like a pirate"  # Instructions for text-to-speach model on how to speak
```

### STT Service Example

```yaml
service: stt.start
data:
  device_id: [your_microphone_device_id]
  entity_id: stt.openai_gpt_4o_mini_transcribe
  metadata:
    language: en     # Optional, will auto-detect if not specified
  options:
    response_format: text  # Optional, defaults to text
```

## HACS installation ( *preferred!* ) 

1. Go to the sidebar HACS menu 

2. Click on the 3-dot overflow menu in the upper right and select the "Custom Repositories" item.

3. Copy/paste https://github.com/sfortis/openai_tts into the "Repository" textbox and select "Integration" for the category entry.

4. Click on "Add" to add the custom repository.

5. You can then click on the "OpenAI Speech Services" repository entry and download it. Restart Home Assistant to apply the component.

6. Add the integration via UI, provide API key and select required models. Multiple instances may be configured.

## Manual installation

1. Ensure you have a `custom_components` folder within your Home Assistant configuration directory.

2. Inside the `custom_components` folder, create a new folder named `openai_tts`.

3. Place the repo files inside `openai_tts` folder.

4. Restart Home Assistant

5. Add the integration via UI, provide API key and select required models. Multiple instances may be configured.