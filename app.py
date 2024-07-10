import os
import streamlit as st
import asyncio
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from chat import setup_conversation, handle_user_input
from config import ANTHROPIC_API_KEY
from audio import transcribe_audio as start_transcription
from audio import text_to_speech_ai, text_to_speech_elevenlabs
from audiorecorder import audiorecorder
from streamlit_float import *


st.set_page_config(page_title="Symptom Extraction", page_icon="")

# Initialize floating features for the interface
float_init()

# Custom CSS to position the input elements at the bottom
st.markdown(
    """
    <style>
        .st-emotion-cache-janbn0 {
            flex-direction: row-reverse !important;
            text-align: right   !important;
            background-color: rgb(111 176 255 / 50%) !important;
        }
        .st-emotion-cache-p4micv {
            width: 4rem !important;
            height: 4rem    !important;
        }
        .stDeployButton {
            visibility: hidden;
        }
        .stStatusWidget {
            visibility: hidden;
        }
        .st-emotion-cache-1uj96rm {
            bottom: 30px !important;
        }
        .block-container.st-emotion-cache-1eo1tir.ea3mdgi5{
            padding_bottom: 4rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("HealthCompass")

os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY


if "history" not in st.session_state:
    st.session_state.history = [{"role": "context", "content": ""}]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

avatars = {
    "human": 'https://www.growcropsonline.com/assets/img/agent-2.jpg',
    "ai": 'https://img.freepik.com/premium-photo/female-nurse-with-stethoscope-cap-3d-rendering_1057-19809.jpg'
}

# Initialize the conversation
conversation = setup_conversation()

# Function to handle text input
def handle_text_input(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=avatars["human"]):
        st.write(prompt)
    with st.chat_message("assistant", avatar=avatars["ai"]):
        with st.spinner("Generating response..."):
            response = conversation.predict(human_input=prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

input_container = st.container()

# Initialize the flag at the start of your app or session
if 'process_audio' not in st.session_state:
    st.session_state['process_audio'] = False

# Create a container for the microphone and audio recording
footer_container = st.container()
with footer_container:
    audio_bytes = audiorecorder('', '')
    if audio_bytes:
        st.session_state['process_audio'] = True

# Function to handle audio input
def handle_audio_input(audio_bytes):
    if len(audio_bytes) > 0:
        audio_bytes.export("temp_audio.wav", format="wav")
        with st.spinner("Transcribing..."):
            transcript = start_transcription('temp_audio.wav')
            if transcript:
                with st.chat_message("user", avatar=avatars["human"]):
                    st.write(transcript)
                return transcript
    return None

# Display chat messages
msgs = StreamlitChatMessageHistory()
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(msg.type, avatar=avatars[msg.type]):
        st.write(msg.content)

# Process audio input if the flag is set
if st.session_state['process_audio']:
    prompt = ""
    audio_transcript = ""
    audio_transcript = handle_audio_input(audio_bytes)
    if audio_transcript and os.path.exists('temp_audio.wav'):
        prompt = audio_transcript
        with st.chat_message("assistant", avatar=avatars["ai"]):
            with st.spinner("Generating response..."):
                response = conversation.predict(human_input=prompt)
                st.write(response)
                text_to_speech_elevenlabs(response)
                st.session_state['process_audio'] = False
                os.remove('temp_audio.wav')

# Handle text input
text_prompt = st.chat_input(placeholder="How do you feel today?")

# Process input (either text or audio)
if text_prompt:
    handle_text_input(text_prompt)

footer_container.float("bottom: 0rem;background-color: var(--default-backgroundColor); padding-top: 1rem;position: fixed;z-index: 9999;")
