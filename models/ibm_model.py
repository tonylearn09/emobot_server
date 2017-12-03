from __future__ import print_function

import os, sys
import json
from watson_developer_cloud import ToneAnalyzerV3



def ibm_eval(dialog, sentence_level=False):
    """Evaluate emotion with ibm Waston
    Args:
        dialog: a list of conversation (document)
    Returns:
        tone: a list of json object as specified in [1] with document level only
        [1]: https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/? \
        cm_mc_uid=44286270948315121962317&cm_mc_sid_50200000=1512196231&cm_mc_sid_52640000=1512196231#post-tone
    """
    tone_analyzer = ToneAnalyzerV3(
        username='a94d751d-4926-483f-8f76-8ca94160360c',
        password='j677AERkAai7',
        version='2017-09-26')
    tone = [tone_analyzer.tone(tone_input=doc, content_type='text/plain', 
                               sentences=sentence_level, tones=['emotion']) for doc in dialog]
    #print(json.dumps(tone, indent=2))
    return tone
        
