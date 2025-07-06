# Step 1a: Setup text to speech - TTS model for audio generation with gTTS and ElevenLabs
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    print(f"Audio saved at: {output_filepath}")

input_text = "Hi this is AI with Komal!!"
#text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")


# Step 1b: Setup text to speech - TTS model for audio generation with ElevenLabs
import os
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = "sk_1216d2af7c7607ba20ffa884c18f5064e65b88a1e40bbb51"

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    response = client.text_to_speech.convert(
        text=input_text,
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Aria's voice ID
        output_format="mp3_22050_32",
         model_id="eleven_turbo_v2"
    )

    # Save audio to file

    elevenlabs.save(response, output_filepath)
    print(f"Audio saved at: {output_filepath}")

# Example call
#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")

#Step 2: Use the model for test output to voice of the doctor
import subprocess
import platform
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    
    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(output_filepath)
    wav_output_filepath = output_filepath.replace(".mp3", ".wav")
    sound.export(wav_output_filepath, format="wav")

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run([
            'powershell', '-c',
            f'(New-Object Media.SoundPlayer "{wav_output_filepath}").PlaySync();'
        ])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', wav_output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text = "Hi this is AI with Komal!! autoplay testing"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")



def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    response = client.text_to_speech.convert(
        text=input_text,
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Aria's voice ID
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2"
    )

    # Save audio to file
    elevenlabs.save(response, output_filepath)
    print(f"Audio saved at: {output_filepath}")
    
    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(output_filepath)
    wav_output_filepath = output_filepath.replace(".mp3", ".wav")
    sound.export(wav_output_filepath, format="wav")
    
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', wav_output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run([
            'powershell', '-c',
            f'(New-Object Media.SoundPlayer "{wav_output_filepath}").PlaySync();'
        ])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', wav_output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Example call
if __name__ == "__main__":
    text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")




