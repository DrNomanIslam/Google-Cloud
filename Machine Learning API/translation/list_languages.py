# Imports the Google Cloud client library
from google.cloud import translate

def list_languages():
    """Lists all available languages."""
    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print(u'{name} ({language})'.format(**language))

list_languages()