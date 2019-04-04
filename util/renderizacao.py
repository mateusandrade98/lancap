class renderizar(object):
    def savarLegenda(self,legenda,local_legenda):
        with open(local_legenda, 'wt') as f:
            f.write(legenda)
            f.close()
        return True

    def criarArquivoHTML(self,titulo,local_video,local_legenda,token):
        with open('model/template.html','rt') as f:
            modelo = f.read()
            f.close()

        JavaScript = 'var ht = new HT({\n'\
        'token: "'+token+'",\n' \
        'videoEnabled: true\n'\
        '});'

        modelo = modelo.format(titulo=titulo,video=local_video,legenda=local_legenda,script=JavaScript)

        video = 'video/'+titulo+'/video.html'
        with open(video,'wt') as f:
            f.write(modelo)
            f.close()

        with open('model/handtalk.min.js','rt') as fr:
            with open('video/'+titulo+'/handtalk.min.js','wt') as fw:
                fw.write(fr.read())
                fw.close()
            fr.close()

        return True,video