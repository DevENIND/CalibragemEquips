import email
import re
from flask import Blueprint, redirect, render_template, request, Flask
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from math import ceil
from datetime import date, timedelta
import os
import database.emails
from werkzeug.utils import secure_filename


Carr_Img_route = Blueprint('Carr_Img', __name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/Imagens_Eqtos'

@Carr_Img_route.route('/<idlog>/<ideqpto>', methods=['GET'])

def Carrega_Pagina(idlog, ideqpto):
    
    #Carregando a p�gina de imagens
    
    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    strToken = idlog
    
    if validacao == True:
        pasta = f'{app.config["UPLOAD_FOLDER"]}'
        validacao, listaImgs, QtdImg= database.emails.puxa_Imagens(ideqpto, EndEmail, pasta)
 
        return render_template(
                'Carr_Imagens.html', idlog = idlog, ideqpto = ideqpto,  lista_imagens = listaImgs, Validacao = validacao, QtdImg = QtdImg
                )
        
    else:
        return redirect(f'/')


    return render_template("Carr_Imagens.html")

@Carr_Img_route.route('<idlog>/<ideqpto>', methods=['Post'])
def Adiciona_Imagem(idlog, ideqpto):
    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    strToken = idlog
    
    if validacao == True:
        pasta = f'{app.config["UPLOAD_FOLDER"]}'
        validacao, listaImgs, QtdImg = database.emails.puxa_Imagens(ideqpto, EndEmail, pasta)
        #Adiciona imagens
        pasta = ''
        
        print(f' voce fez o upload de {len(request.files)}')
        
        lista = request.files.to_dict(flat=False)
        lista = lista["impImgEqto"]
    
        for file in lista:
            if file.filename != '':
                QtdImg += 1
                NomeArquivo = f'ID_{ideqpto}_Img({QtdImg + 1}).{file.filename.split(".")[-1]}'
                pasta = f'{app.config["UPLOAD_FOLDER"]}/{NomeArquivo}'
            
                print(pasta)
          
        
                if not os.path.isfile(pasta):
                    # if user does not select file, browser also
                    # submit an empty part without filename
                    file.save(pasta)
                else:
                    for i in range(50):
                        QtdImg += 1
                        NomeArquivo = f'ID_{idlog}_Img({QtdImg + 1}).{file.filename.split(".")[-1]}'
                        pasta = f'{app.config["UPLOAD_FOLDER"]}/{NomeArquivo}'
                        print(pasta)
                        if not os.path.isfile(pasta):
                            pasta = f'{app.config["UPLOAD_FOLDER"]}/{NomeArquivo}'
                            pass
       
                  
        return redirect(f'/Carr_Img/{idlog}/{ideqpto}')   
   
          
    else:
        return redirect(f'/')


@Carr_Img_route.route('<idlog>/<ideqpto>/delete/<NomeImg>', methods=['Post'])
def Deletar_Imagem(idlog, ideqpto, NomeImg):
    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    strToken = idlog
    
    if validacao == True:
        pasta = f'{app.config["UPLOAD_FOLDER"]}'
        validacao, listaImgs, QtdImg = database.emails.puxa_Imagens(ideqpto, EndEmail, pasta)

        if validacao == True:
            #Exclui imagens
            pasta = f'{app.config["UPLOAD_FOLDER"]}'
            database.emails.deleta_arquivos_img(pasta,NomeImg)

        return redirect(f'/Carr_Img/{idlog}/{ideqpto}')      
    else:
        return redirect(f'/')
   