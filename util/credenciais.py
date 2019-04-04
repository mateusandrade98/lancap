import json

class apiKey:
    def __init__(self):
        with open('credenciais.json','rt') as f:
            r = f.read()
            f.close()

        self.credencial = r

    def obterAPIKeyGoogleCloud(self):
        resposta = json.loads(self.credencial)
        return resposta['apiKeyGoogleCloud']

    def obterTokenHandTalk(self):
        resposta = json.loads(self.credencial)
        return resposta['apiHandTalk']