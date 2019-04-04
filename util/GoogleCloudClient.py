from googleapiclient.discovery import build as Google

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class traduzir(object):
    def __init__(self,sentencas,apiKey,dstLang,srcLang):
        self.sentencas  = sentencas
        self.apiKey     = apiKey
        self.dstLang    = dstLang
        self.srcLang    = srcLang

    def obterTraducaoDeUmTexto(self):
        servico     = Google('translate',version='v2',developerKey=self.apiKey)
        resultado   = servico.translations().list(
            source=self.srcLang,
            target=self.dstLang,
            q=[self.sentencas]
        ).execute()
        if 'translations' in resultado and \
                'translatedText' in resultado['translations'][0] and \
                resultado['translations'][0]['translatedText'] != '':
                    return resultado['translations'][0]['translatedText']
        else:
            print('[ - ] Texto não pode ser traduzido')
            return ''


class obterTextoDeUmFala(object):
    def __init__(self,linguagem='en',taxa=16000):
        self.linguagem  = linguagem
        self.taxa       = taxa
        self.cliente    = speech.SpeechClient.from_service_account_json('autenticacao.json')

    def call(self,data):
        audio = types.RecognitionAudio(content=data)
        configuracao = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=self.taxa,
            language_code=self.linguagem)

        resposta = self.cliente.recognize(configuracao, audio)
        for resultado in resposta.results:
            return resultado.alternatives[0].transcript
