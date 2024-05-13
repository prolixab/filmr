from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ELEVEN_API_KEY")


def create_speech(text, path, filename):
    client = ElevenLabs(
        api_key=api_key,
    )
    print(f'Generating audio {filename}')
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    file_path = os.path.join(path, f'{filename}.mp3')
    print(f'Saving audio to {file_path}')
    save(audio, file_path)
