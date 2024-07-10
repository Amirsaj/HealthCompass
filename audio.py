import speech_recognition as sr
from gtts import gTTS
from elevenlabs.client import ElevenLabs
from elevenlabs import stream,Voice, VoiceSettings, play
from config import ELERVEN_API_KEY
import os

client = ElevenLabs(
  api_key=ELERVEN_API_KEY
)

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as audio_file:
        audio_data = recognizer.record(audio_file)
    transcript = recognizer.recognize_google(audio_data)
    return transcript




def text_to_speech_ai(speech_file_path, api_response):
    tts = gTTS(text=api_response, lang='en')
    tts.save(speech_file_path)
    return speech_file_path  # Return the path where audio is saved

# text to speech elevenlabs
def text_to_speech_elevenlabs(api_response):
    audio = client.generate(
    text=api_response,
    voice=Voice(
        voice_id='jsCqWAovK2LkecY7zXl4',
        settings=VoiceSettings(stability=0.30, similarity_boost=0.30, style=0.3, use_speaker_boost=True)
    )
    )
    stream(audio)


