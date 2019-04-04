import json

class config:
    def __init__(self):
        with open('config.json','rt') as f:
            r = f.read()
            f.close()

        self.configuracao = r

    def obterLiguagemDeDestino(self):
        resposta = json.loads(self.configuracao)
        return resposta['destinoLinguagem']

    def obterFonteDeLinguagem(self):
        resposta = json.loads(self.configuracao)
        return resposta['fonteLinguagem']

    def obterFormatoDoArquivoDeLegenda(self):
        resposta = json.loads(self.configuracao)
        return resposta['formatoLegenda']