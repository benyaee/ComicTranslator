import os
import six
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\benre\\OneDrive\\Desktop\\ComicTranslator\\total-cedar-335014-5412f0edd455.json"

def translate_text(target, text):

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
        
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]


