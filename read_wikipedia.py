#!/usr/bin/env python

import argparse
import os
import sys
import vlc
import wikipedia
from google.cloud import texttospeech

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------
def synthesize_from_wikipedia(url_or_title, voice_suffix='C'):
    """Synthesizes speech from the a Wikipedia URL or title."""

    text = wikipedia.summary(url_or_title)
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.types.SynthesisInput(text=text)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-'+voice_suffix)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Fetch response from Google Cloud
    response = client.synthesize_speech(input_text, voice, audio_config)

    output_path = f"/tmp/wikipedia-wavenet-tts-output-{os.getpid()}.mp3"

    # Write to MP3
    with open(output_path, 'wb') as out:
        out.write(response.audio_content)
        print('Wikipedia synthesis written to file "output.mp3"')

    # from pygame import mixer

    # mixer.init()
    # mixer.music.load(output_path)
    # mixer.music.play()

    player = vlc.MediaPlayer(f"file://{output_path}")

    player.play()

# ================================================
# MAIN ===========================================
# ================================================
if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
    synthesize_from_wikipedia(sys.argv[1])

