#!/usr/bin/env python

import argparse
import os
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'

def synthesize_from_wikipedia(url_or_title, voice_suffix='F'):
    """Synthesizes speech from the a Wikipedia URL or title."""

    import wikipedia
    from google.cloud import texttospeech

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

    # Write to MP3
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Wikipedia synthesis written to file "output.mp3"')

# ================================================
# MAIN ===========================================
# ================================================
if __name__ == '__main__':
    synthesize_from_wikipedia(sys.argv[1])

