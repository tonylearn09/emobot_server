from __future__ import print_function

import os, sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import json



def google_eval(dialog, sentence_level=False):
    """Evaluate emotion with ibm Waston
    Args:
        dialog: a list of conversation (document)
    Returns:
        score: a list of number between [0, 1] for each doc in dialog
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'My First Project-f4f9e8a13281.json'
    client = language.LanguageServiceClient()

    document = [types.Document(content=doc,
                               type=enums.Document.Type.PLAIN_TEXT) for doc in dialog]
    annotations = [client.analyze_sentiment(document=doc) for doc in document]
    score = [anno.document_sentiment.score for anno in annotations]

    return score
        
