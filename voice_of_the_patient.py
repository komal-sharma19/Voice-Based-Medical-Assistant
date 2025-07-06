# Step 1: Setup Audio Recorder( ffmpeg or portaudio)

## ffmpeg,portaudio, pydub, speech_recognition
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO ,format='%(asctime)s - %(levelname)s - %(message)s')
def record_audio(file_path, timeout=20,phrase_time_limit=None):
    """Simplified function to record audio from the microphone ans save it as a MP3 file . 
    
    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for the recording in seconds.
        phrase_time_limit (int, optional): Maximum length of the recorded phrase in seconds.
    
    Returns:
        None
    
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start Speaking now...")
            
            # Record audio from the microphone
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorder audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3",bitrate="128k")
            logging.info(f"Audio saved to {file_path}")
            
    except Exception as e:
        logging.error("Recording timed out. Please try again.")

audio_file_path = "patient_voice_test.mp3"
record_audio(file_path=audio_file_path)


# Step 2: Setup Speech to text- STT- model for audio transcription
import os
from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")


def transcribe_with_groq(audio_file_path, stt_model="whisper-large-v3"):
    try:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return "Transcription failed."
