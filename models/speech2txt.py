import io
import os
import argparse
import json

# Imports the Google Cloud client library
# [START migration_import]
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# [END migration_import]

def transcribe_file(file_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'My First Project-b0d38a1bb15f.json' 

    client = speech.SpeechClient()

    #file_name = os.path.join(
        #os.path.dirname(__file__),
        #'A few Good Creative Men.flac')

# Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')
    
    #response = client.recognize(config, audio)
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    #response = operation.result(timeout=90)
    response = operation.result()


    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'My First Project-b0d38a1bb15f.json' 
    print(gcs_uri)
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    #print(response)
    return response

    # Print the first alternative of all the consecutive results.
    #for result in response.results:
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
        #print('Confidence: {}'.format(result.alternatives[0].confidence))
# [END def_transcribe_gcs]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)


