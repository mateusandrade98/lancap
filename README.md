# #campusIV #lancap #handtalk #python #libras

O LanCap é um software open source, criado para legendar vídeos para libras e português. Usando equações matemáticas o sofware consegue reconhecer falas em um áudio, assim excluíndo ruídos e som ambiente. Após reconhecer as frequências com fala e calcular o tempo de fala limite, as frequências são compactadas em FLAC e enviado para Google Cloud Console. Usando Deep Learning com Speech-To-Text(API) para reconhecimento do texto contido nas frequências, o retorno da Google Cloud é processado baseado no tempo de fala salvo anteriormente e compactado em srt(arquivos de legendas). No final as legendas são enviadas para a Hand Talk(API), com o retorno do personagem 3D é renderizado no vídeo.
Obrigado!!!

#Vídeo de demonstrativo
