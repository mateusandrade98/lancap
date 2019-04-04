import subprocess as sp
import tempfile as tmp
import os
import wave
import math
import audioop


class coversaoFLAC(object):
    def __init__(self,audio, incluir_antes=0.25, incluir_depois=0.25):
        self.audio = audio
        self.incluir_antes = incluir_antes
        self.incluir_depois = incluir_depois

    def __call__(self,regiao):
        inicio, fim = regiao
        inicio = max(0, (inicio - self.incluir_antes))
        fim += self.incluir_depois
        temporario = tmp.NamedTemporaryFile(suffix='.flac', delete=False)
        if not os.path.isfile(self.audio):
            raise Exception('O áudio não foi encontrado.')

        comando = ["ffmpeg",
                   "-ss", str(inicio),
                   "-t", str(fim - inicio),
                   "-y", "-i", self.audio,
                   "-loglevel", "error",
                   temporario.name
                   ]

        usarShell = True if os.name == "nt" else False
        sp.check_output(comando, shell=usarShell)
        dadosDoArquivoDeFlac = temporario.read()
        temporario.close()
        os.unlink(temporario.name)
        #os.unlink(self.audio)
        return dadosDoArquivoDeFlac

class asyncAudio(object):

    def percentil(arr, porcentagem):
        arr = sorted(arr)
        index = (len(arr) - 1) * porcentagem
        floor = math.floor(index)
        ceil = math.ceil(index)
        if floor == ceil:
            return arr[int(index)]
        valor_pequeno = arr[int(floor)] * (ceil - index)
        valor_grande = arr[int(ceil)] * (index - floor)
        return valor_pequeno + valor_grande

    def buscandoRegiaosDeFala(self,audio,larguraDoFrame=4096,minTamanhoDaRegiao=0.5,maxTamanhoDaRegiao=6):
        leitor = wave.open(audio)
        larguraDaAmostra = leitor.getsampwidth()
        taxa = leitor.getframerate()
        numeroDeCanal = leitor.getnchannels()
        pedassoDaDuracao = float(larguraDoFrame) / taxa
        numeroDePedassos = int(math.ceil(leitor.getnframes() * 1.0 / larguraDoFrame))
        energias = []

        for i in range(numeroDePedassos):
            pedasso = leitor.readframes(larguraDoFrame)
            energias.append(audioop.rms(pedasso,larguraDaAmostra * numeroDeCanal))

        limite = asyncAudio.percentil(energias,0.2)
        tempoGasto = 0

        regioes = []
        regiaoDeInicio = None

        for energia in energias:
            estaEmSilencio = limite >= energia
            maxExcedido = regiaoDeInicio and tempoGasto - regiaoDeInicio >= maxTamanhoDaRegiao

            if (maxExcedido or estaEmSilencio) and regiaoDeInicio:
                if tempoGasto - regiaoDeInicio >= minTamanhoDaRegiao:
                    regioes.append((regiaoDeInicio,tempoGasto))
                    regiaoDeInicio = None
            elif (not regiaoDeInicio) and (not estaEmSilencio):
                regiaoDeInicio = tempoGasto
            tempoGasto += pedassoDaDuracao

        return regioes


    def extrairAudioDeUmVideo(self,video,canals=1,taxa=16000):
        print('[!] Tentando extrair áudio do vídeo...')
        temporario = tmp.NamedTemporaryFile(suffix='.wav',delete=False)
        if not os.path.isfile(video):
            raise Exception('O vídeo não foi encontrado.')

        comando = ['ffmpeg',
                   '-y',
                   '-i', video,
                   '-ac', str(canals),
                   '-ar', str(taxa),
                   '-loglevel', 'error',
                   temporario.name
                   ]
        usarShell = True if os.name == "nt" else False
        sp.check_output(comando,stdin=open(os.devnull),shell=usarShell)
        print('[+] áudio salvo em -->',temporario.name)
        return temporario.name,taxa
