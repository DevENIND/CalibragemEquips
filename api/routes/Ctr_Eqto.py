import email
import re
from typing import Type
from flask import Blueprint, redirect, render_template, request, Flask
import database.emails
from werkzeug.utils import secure_filename
from math import ceil
from datetime import date, timedelta
import os

Ctr_Eqto_route = Blueprint('Ctr_Eqto', __name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/certificados'

@Ctr_Eqto_route.route('/<idlog>', methods=['GET'])
def lista_eqtos(idlog):
    print("alimentando listagem")
    #Lista os equipamentos
    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    
    global strToken
    strToken = idlog
    
    lista_equipamentos = database.emails.Lista_Eqtos()

    if validacao == True:
        qtdTotal = len(lista_equipamentos)
        qtdLinhas = int(ceil(qtdTotal / 3))
        return render_template('Ctr_Eqto.html', email=EndEmail, qtd_linhas=qtdLinhas, qtd_total=qtdTotal, equipamentos=lista_equipamentos)
    else:
        return redirect(f'/')

@Ctr_Eqto_route.route('/<idlog>/edit/<ideqpto>')
def Editar(idlog, ideqpto):
    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    print(EndEmail)
    strToken = idlog
    if validacao == True:
        # A segunda valida��o serve para saber se o e-mail em quest�o est� apto a realizar altera��es
        listaEqtpo, validacao, msgerro = database.emails.puxa_registro(ideqpto, EndEmail)
        msg = ''
        if listaEqtpo != []: 
            ArquivoCert = listaEqtpo[0]['ArqCertificacao']
            DataVcto = listaEqtpo[0]['DataValidade']
        
        lista_Alt = database.emails.busca_alteracoes(listaEqtpo[0]['id'])

        caminho_url = f'/Ctr_Eqto/{idlog}/edit/{ideqpto}'
        
        return render_template(
                'Cad_Eqto.html', idlog = idlog, ideqpto = ideqpto ,  equipamentos = listaEqtpo, valid = True, 
                email = EndEmail, mensagem = msg, mensagemErro = msgerro, alteracoes =  lista_Alt, data_vcto = DataVcto,
                ArqCert = ArquivoCert
                )
        
        caminho_url = f'/Ctr_Eqto/{idlog}/edit/{ideqpto}'
        return render_template('Cad_Eqto.html', idlog = idlog, ideqpto = ideqpto ,  equipamentos = listaEqtpo, valid = validacao, email = EndEmail)
        
    else:
        return redirect(f'/'
                        f'')

@Ctr_Eqto_route.route('/<idlog>/delete/<ideqpto>')
def Deletar(idlog, ideqpto):
    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    print(EndEmail)
    strToken = idlog
    if validacao == True:
        # A segunda valida��o serve para saber se o e-mail em quest�o est� apto a realizar altera��es
        validacao, msg, msgerro = database.emails.deleta_registro_eqto(ideqpto, EndEmail)
        
        if validacao == True:
            pasta = f'{app.config["UPLOAD_FOLDER"]}'
        
            database.emails.deleta_arquivos_eqto(ideqpto, pasta)
        
            lista_equipamentos = database.emails.Lista_Eqtos()

            qtdTotal = len(lista_equipamentos)
            qtdLinhas = int(ceil(qtdTotal / 3))
        
        return redirect(f'/Ctr_Eqto/{idlog}')
        
    else:
        return redirect(f'/')
    
    
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@Ctr_Eqto_route.route('/<idlog>/edit/<ideqpto>', methods=['POST'])
def Registrar_Eqpto(idlog, ideqpto):
    
    dados = request.get_json

    reqID = ideqpto
    reqNome = request.form.get("txtNome")
    reqNumOS = request.form.get("txtNumOS")
    reqTag = request.form.get("txtTag")
    reqNumSerie =  request.form.get("txtNumSerie")
    reqStatus =  request.form.get("cboxStatus")
    reqMeses = request.form.get("txtMeses")
    reqCert = request.form.get("txtNomeCert")
    
    for req in request.form:
         print(f'requisicao:{req} valor: {request.form.get(req)}')
    
    # for req in request.args:
    #     print(req)
    
    # for req in request.files:
    #     print(req)
    
    # for req in request.values:
    #     print(req)
    

        
    if reqID == '':
        reqID = 'new'

    
    registro =[]
    registro.append({
        "id": reqID,
        "Desc": request.form.get("txtNome"),
        "Tag": request.form.get("txtTag"),
        "NumSerie": request.form.get("txtNumSerie"),
        "Fabricante": request.form.get("txtFabricante"),
        "Status": request.form.get("cboxStatus"),
        "OS": request.form.get("txtNumOS"),
        "Certificadora": request.form.get("txtNomeCert"),
        "QtdMeses": request.form.get("txtMeses"),
        "DataCalibracao": str(request.form.get("txtDataCalibracao")),
        "ArqCertificacao": ''
      })
    
    if 'impArqCert' in request.files:
        file = request.files['impArqCert']
        registro[0]["ArqCertificacao"] = file.filename
        novoArquivo = True

        if registro[0]["ArqCertificacao"] == '' or registro[0]["ArqCertificacao"].upper() == 'NONE':
            registro[0]["ArqCertificacao"] = request.form.get("txtArqCert")
            print(f'imgArqCert Identificado porem estava era nada modificado para:{registro[0]["ArqCertificacao"]}')
            novoArquivo = False
        print(f'pegou o arquivo: {registro[0]["ArqCertificacao"]}')
    else:
        print(f'Nao identificou o imgArqCert modificado para:{registro[0]["ArqCertificacao"]}')
        registro[0]["ArqCertificacao"] = request.form.get("txtArqCert")
        novoArquivo = False
   
    
    print('valores postados:')
    for chave in registro[0].keys():
        print (f'chave: {chave} valor: {registro[0][chave]}')
        
    print('passou pela fase do registro')

    validacao, msgerro, EndEmail = database.emails.valida_token_email(idlog)
    print(EndEmail)
    
    strToken = idlog
    if validacao == True:
      

        # A segunda valida��o serve para saber se o e-mail em quest�o est� apto a realizar altera��es
        validacao, msg, msgerro, idEqui, DataVcto, ArquivoCert = database.emails.realiza_registro(ideqpto, EndEmail, registro)
        
        print(validacao)
        print(msg)
        print(msgerro)
        
        if registro[0]['id'] == 'new':
            registro[0]['id'] = idEqui
            
        if 'Campo OS ' in msg:
            registro[0]['OS'] = ''
            
        if ' Status ' in msg:
            registro[0]['Status'] = ''
          
        if 'Quantidade de meses ' in msg:
            registro[0]['QtdMeses'] = ''
        
        if 'Data de calibracao ' in msg:
            registro[0]['DataCalibracao'] = 'dd/mm/aaaa'
        
        if 'numero de serie' in msg:
            registro[0]['NumSerie'] = ''
        
        Caminho_Salvar = './static/certificados'
        
        if msg == "Registro realizado com sucesso!":
            print(f'salvando o arquivo como o nome: {ArquivoCert}')
            
            if 'impArqCert' not in request.files:
                validacao, msg, msgerro = database.emails.deleta_registro_eqto(registro[0]['id'], EndEmail)
                msg = "Nao possui impArqCert no formulario"
                registro[0]['id'] = ''
            else:
                file = request.files['impArqCert']
                pasta = f'{app.config["UPLOAD_FOLDER"]}/{ArquivoCert}'
                
                if not os.path.isfile(pasta):
                    # if user does not select file, browser also
                    # submit an empty part without filename
                    if file.filename == '':
                        validacao, msg, msgerro = database.emails.deleta_registro_eqto(registro[0]['id'], EndEmail)
                        msg = "Arquivo anexado nao tem nome"
                        registro[0]['id'] = ''
                    
                    if file and allowed_file(file.filename):
                        file.save(pasta)
                        
        if msg == "Registro alterado com sucesso!" and novoArquivo == True:
            print(f'salvando o arquivo alterado como o nome: {ArquivoCert}')
            
            if 'impArqCert' not in request.files:
                validacao, ArquivoCert, msg = database.emails.restaura_arquivo_cert(registro[0]['id'], ArquivoCert, Caminho_Salvar)
            else:
                file = request.files['impArqCert']
                pasta = f'{app.config["UPLOAD_FOLDER"]}/{ArquivoCert}'
                
                if not os.path.isfile(pasta):
                    # if user does not select file, browser also
                    # submit an empty part without filename
                    if file.filename == '':
                        validacao, ArquivoCert, msg = database.emails.restaura_arquivo_cert(registro[0]['id'], ArquivoCert, Caminho_Salvar)
                    
                    if file and allowed_file(file.filename):
                        file.save(pasta)
               
        
        caminho_url = f'/Ctr_Eqto/{idlog}/edit/{ideqpto}'
        
        lista_Alt = database.emails.busca_alteracoes(registro[0]['id'])

        return render_template(
                'Cad_Eqto.html', idlog = idlog, ideqpto = ideqpto ,  equipamentos = registro, valid = True, 
                email = EndEmail, mensagem = msg, mensagemErro = msgerro, alteracoes =  lista_Alt, data_vcto = DataVcto,
                ArqCert = ArquivoCert
                )
        
    else:
        return redirect(f'/')