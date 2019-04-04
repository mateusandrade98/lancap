#-*-coding:utf-8-*-

'''
PENSADO E DESENVOLVIDO TOTALMENTE PARA REALIZAÇÃO E ESTUDO ACADÊMICO.
Projeto desenvolvido por Joandeson Andrade com a licença MIT (Open Source).
O Lancap é uma ferramenta que tem como objetivo legendar vídeos usando Deep Learning.
O Objetivo principal é a propagação de conhecimento, onde até os deficiêntes auditivos podem ter acesso a informações de qualidade.
A Ferramenta tenta legendar o vídeo para português e para Libras(segunda língua oficial do brasil).


API de deep learning da Google Cloud usada para a tradução do texto, e a extração do texto de um aúdio
--> https://cloud.google.com

API usada para a legenda em libras foi a Hand Talk
--> https://www.handtalk.me/

-----------------------------------------------
Joandeson Andrade
https://github.com/joandesonandrade
joandesonandradesilva@gmail.com
-----------------------------------------------
'''

from util import credenciais
from util import configuracoes
from util import audio
from util import legenda
from util import renderizacao
import sys
import os

if(len(sys.argv) < 2):
    raise Exception('Especifique o local do vídeo')

config = configuracoes.config()
api    = credenciais.apiKey()

apikey  = api.obterAPIKeyGoogleCloud()
dstLang = config.obterLiguagemDeDestino()
srcLang = config.obterFonteDeLinguagem()

#vídeo usado no processo
localDoVideo = sys.argv[1]
localVideo = str(localDoVideo).split('/')[-1]

asyncAudio  = audio.asyncAudio()
localDoAudioTemporario, taxa = asyncAudio.extrairAudioDeUmVideo(video=localDoVideo)
regioes                      = asyncAudio.buscandoRegiaosDeFala(audio=localDoAudioTemporario)
extraindoAudioComFala        = legenda.extraindoAudioComFalaDoAudio(regioes=regioes,audio=localDoAudioTemporario)
reconhecimentoDeFala         = legenda.extraindoTextoDoAudio(regios_extraidas=extraindoAudioComFala,apiKey=apikey,srcLang=srcLang,dstLang=dstLang)
tempoDaLegenda               = legenda.calcularTempoDaLegenda(regioes=regioes,tranquisao=reconhecimentoDeFala)
legenda                      = legenda.criarArquivoSRT(tempodalegenda=tempoDaLegenda)

renderizar                   = renderizacao.renderizar()

if not os.path.isdir('video/'+localVideo+'/'):
    os.mkdir('video/'+localVideo+'/')

with open(localVideo,'rb') as rf:
    with open('video/'+localVideo+'/'+localDoVideo,'wb') as fw:
        fw.write(rf.read())
        fw.close()
    rf.close()

renderizar.savarLegenda(legenda=legenda,local_legenda='video/'+localVideo+'/'+localVideo+'.srt')
retorno = renderizar.criarArquivoHTML(titulo=localDoVideo,local_video=localDoVideo,local_legenda=localVideo+'.srt',token=api.obterTokenHandTalk())

if retorno[0] == True:
    print('Vídeo foi legendado com sucesso.. salvo em ->',retorno[1])