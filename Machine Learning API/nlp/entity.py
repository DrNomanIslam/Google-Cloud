from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()

text = u'Ahmad gone there to understand the basic concepts of AI from SalahUddin but he told me he is not gonna teach me'


document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)

response = client.analyze_entities(document=document)


for entity in response.entities:
     print('=' * 20)
     print('         name: {0}'.format(entity.name))
     print('     metadata: {0}'.format(entity.metadata))
     print('     salience: {0}'.format(entity.salience))




