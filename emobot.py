from __future__ import print_function
import json
import os, sys
import re
import pprint

import boto
import gcs_oauth2_boto_plugin
import shutil
import StringIO
import tempfile
import time
import subprocess

from google.cloud import storage

from models.ibm_model import ibm_eval
from models.google_model import google_eval
from models.speech2txt import transcribe_gcs

AUDIO_BUCKET = 'our_sentiment_audio'


def eval_emotion(option, input):
    """API for Evaluate emotion
    Args:
        option: ['file', 'text', 'audio']
        input: [filename, text_input, audio_input]
    Returns:
        final_response: Emotion json object
    """

    if option == 'file':
        if input.endswith('.mp3'):
            obj_name = input.split('/')[-1]
            obj_name = obj_name[:obj_name.rfind('.')] + '.flac'
            print('Convert to {:s}'.format(obj_name))
            subprocess.call(['ffmpeg', '-i', input, '-ac', '1', obj_name]) 
            input = input[:obj_name.rfind('.')] + '.flac'
            convseration_list = handle_audio(input)
        elif input.endswith('.flac'):
            convseration_list = handle_audio(input)
            #print(convseration_list)
        else: # txt file
            with open(os.path.join(input), 'r') as f:
                script = f.read()
            convseration_list = str_sep(script)
    elif option == 'text':
        convseration_list = [input]
    #elif option == 'audio':
        #convseration_list = input_audio2txt(input)
    else:
        return None

    ibm_response = ibm_eval(convseration_list)
    google_response = google_eval(convseration_list)
    #print(google_response)

    final_response = merge_response(ibm_response, google_response)
    return final_response

def handle_audio(input):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'My First Project-582d61328a94.json'
    storage_client = storage.Client()
    if not storage_client.lookup_bucket(AUDIO_BUCKET):
        bucket = storage_client.create_bucket(AUDIO_BUCKET)
        print('Bucket {} created'.format(bucket.name))
    else:
        print('Bucket {:s} Already exists'.format(AUDIO_BUCKET))

    bucket = storage_client.get_bucket(AUDIO_BUCKET)
    blobs = bucket.list_blobs()
    all_blob_name = [blob.name for blob in blobs]
    obj_name = input.split('/')[-1]
    if not (obj_name in all_blob_name):
        blob = bucket.blob(obj_name)
        blob.upload_from_filename(input)

        blob.make_public()
    else:
        print('Object {:s} Already exists'.format(obj_name))

    response = transcribe_gcs('gs://'+AUDIO_BUCKET+'/'+obj_name)

    convseration_list = [result.alternatives[0].transcript for result in response.results]
    return convseration_list


def str_sep(script):
    final_conversation_list = []
    cur_str = ''
    for line in script.split('\n'):
        #letter_line = filter(str.isalpha, line)
        #if isupper(letter_line):
        if line.isupper():
            if cur_str:
                final_conversation_list.append(cur_str)
                cur_str = ''
        else:
            cur_str += line
    if cur_str:
        final_conversation_list.append(cur_str)

    return final_conversation_list
        


def merge_response(ibm, google):
    """Return a list of dict, with key being the tone detected: (anger, disgust, fear, joy, sadness, 
                                                                analytical, confident, tentative, neutral),
    and the score being its value"""
    final_tone = [{}  for i in range(len(google))]
    for doc_id, google_score in enumerate(google):
        dict_obj = ibm[doc_id]
        all_tones = dict_obj['document_tone']['tones']
        for tone in all_tones:
            tone_name = tone['tone_id']
            tone_score = tone['score']
            if google_score > 0.5:
                # really positive for google
                if tone_name != 'joy':
                    #final_tone[doc_id]['joy'] = google_score
                    continue
            elif google_score < -0.5: 
                # really negative for google
                if tone_name == 'joy':
                    continue

            final_tone[doc_id][tone_name] = tone_score
        if len(final_tone[doc_id]) == 0:
            final_tone[doc_id]['neutral'] = 1.0

    return final_tone


if __name__ == '__main__':
    #txt_file = os.path.join('erin.txt')
    #with open(txt_file, 'r') as f:
        #txt_file = f.read()
    if len(sys.argv) != 2:
        sys.exit(1)
    #print(sys.argv[1])

    final_response = eval_emotion('file', sys.argv[1])
    #print(json.dumps(final_response,indent=2))
    #output_txt = str_sep(txt_file)
    #with open('sol_process.txt', 'wt') as f:
        #f.write(str(output_txt))


    
