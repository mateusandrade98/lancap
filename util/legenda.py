from progressbar import Percentage,Bar,ProgressBar,ETA
import multiprocessing
from .audio import coversaoFLAC
from .GoogleCloudClient import traduzir as tradutor
from .GoogleCloudClient import obterTextoDeUmFala
import pysrt
import six

def extraindoAudioComFalaDoAudio(regioes,audio):
    covetendo = coversaoFLAC(audio=audio)
    pool = multiprocessing.Pool(10)

    banner = ['Convertendo regiões de fala em arquivo FLAC ', Percentage(), ' ', Bar()]
    bar = ProgressBar(widgets=banner, maxval=len(regioes)).start()
    regios_extraidas = []
    for i, extraindo_regiao in enumerate(pool.imap(covetendo, regioes)):
        regios_extraidas.append(extraindo_regiao)
        bar.update(i)
    bar.finish()
    return regios_extraidas

def traduzirLegenda(texto,apiKey,dstLang,srcLang):
    traducao = tradutor(texto,apiKey=apiKey,dstLang=dstLang,srcLang=srcLang)
    return traducao

def extraindoTextoDoAudio(regios_extraidas,apiKey,dstLang,srcLang):
    reconhecimentoDeFala = obterTextoDeUmFala()
    banner = ["Precessando a transcrição do aúdio: ", Percentage(), ' ', Bar(),' Tempo: ',ETA()]
    bar = ProgressBar(widgets=banner, maxval=len(regios_extraidas)).start()
    trasquicoes = []
    progress = 0
    for regiao in regios_extraidas:
        textoDaFala = reconhecimentoDeFala.call(regiao)
        if textoDaFala == None:
            textoDaFala = ''
        else:
            textoDaFala = traduzirLegenda(textoDaFala,apiKey,dstLang,srcLang).obterTraducaoDeUmTexto()
        primeiraLetraMaiuscula = textoDaFala[:1].upper()+textoDaFala[1:]
        trasquicoes.append(primeiraLetraMaiuscula)
        progress+=1
        bar.update(progress)
    bar.finish()
    return trasquicoes

def calcularTempoDaLegenda(regioes,tranquisao):
    return [(r, t) for r, t in zip(regioes, tranquisao) if t]

def criarArquivoSRT(tempodalegenda, preenchimento_antes=0, preenchimento_depois=0):
    rip = pysrt.SubRipFile()
    for i, ((inicio, fim), text) in enumerate(tempodalegenda, start=1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = six.text_type(text)
        item.start.seconds = max(0, inicio - preenchimento_antes)
        item.end.seconds = fim + preenchimento_depois
        rip.append(item)
    legenda = '\n'.join(six.text_type(item) for item in rip)
    return legenda
