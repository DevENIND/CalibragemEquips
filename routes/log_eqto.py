from ast import Global
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import funcoes.emails

log_eqto_route = Blueprint('log_eqto', __name__)


@log_eqto_route.route('/')
def abrir_pagina():
    #Abre a página de login
        nome_btn='Enviar'
        return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "", dominioemail = "@enind.com.br")

@log_eqto_route.route('/conferencia')
def verificar_email():
    return "Validacao do Email"


@log_eqto_route.route('/', methods=['POST'])
def enviar_email():
    
    prefixoemail = request.form.get("CmplEmail")
    email = request.form.get("email")
    codigo = request.form.get("Codigo")
    nome_btn =  request.form.get("btnEnviar")

    #Verificando se a página deu algum retorno!
    if prefixoemail is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o prefixo de email", dominioemail=email)
    
    if email is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o dominio do email", dominioemail=email)
    
    if codigo is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o codigo", dominioemail=email)
    
    if nome_btn is None:
            return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o codigo", dominioemail=email)

    NaoPermitidos = f"SELECT,DELETE,INSERT,',*,%,{chr(34)},(,),TRUNCATE,DROP"
    palavras = NaoPermitidos.split(",")

    for palavra in palavras:
            if palavra in email.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, tipoalerta= "description-danger", msg=mensagem, dominioemail=email)   
             
            elif palavra in prefixoemail.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,tipoalerta= "description-danger",  msg=mensagem, dominioemail=email)
             
        
    if email != "@enind.com.br" and email != "@enindservicos.com.br":
            mensagem = 'e-mail invalido, por gentileza utilizar os disponiveis nas caixas.'
            return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, msg=mensagem, tipoalerta= "description-danger", dominioemail=email)

    
    if nome_btn == 'Enviar':
            nome_btn = "Validar"
            email_completo = prefixoemail + email
            envio, Valor_Erro = funcoes.emails.registra_codigo_email(email_completo)
            if envio == True:
                    mensagem = "Email enviado com sucesso!"
                    return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "description-success", dominioemail=email)
            else:
                    mensagem = f"Houve um erro no envido do email, erro: {Valor_Erro}" 
                    return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "description-danger", dominioemail=email)
   
    
    else:
           for palavra in palavras:
                if palavra in codigo.upper():
                    mensagem = 'Codigo invalido.'
                    return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,tipoalerta= "description-danger",  msg=mensagem, dominioemail=email)
                
           if not codigo.isnumeric():
                mensagem = 'Codigo inserido invalido'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, msg=mensagem,tipoalerta= "description-danger", dominioemail=email)


           if len(codigo) != 6:
                mensagem = 'Codigo inserido esta superior ou inferior a 6 digitos'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,  msg=mensagem, tipoalerta= "description-danger", dominioemail=email)   
            
           email_completo = prefixoemail + email
           Validacao, Valor_Erro, strtoken = funcoes.emails.valida_codigo(email_completo,codigo)
           if Validacao == True:
               return redirect(f'/Ctr_Eqto/{strtoken}')
           else:
               mensagem = f"Verifique novamente, {Valor_Erro}" 
               return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "description-danger", dominioemail=email)
           
#########################################################################################################################################################################
#################################################################### REENVIO DE E-MAIL ##################################################################################
#########################################################################################################################################################################           

@log_eqto_route.route('/reenvio')
def reenvio():
    
    prefixoemail = request.args.get('ComplEmail')
    email = request.args.get('email')
    codigo = request.args.get('codigo')

    #Verificando se a página deu algum retorno!
    if prefixoemail is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o prefixo de email", dominioemail=email)
    
    if email is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o dominio do email", dominioemail=email)
    
    if codigo is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o codigo", dominioemail=email)
    
    NaoPermitidos = f"SELECT, DELETE, INSERT,',*,%,{chr(34)},(,)"
    palavras = NaoPermitidos.split(",")

    for palavra in palavras:
            if palavra in email.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, tipoalerta= "description-danger", msg=mensagem, dominioemail=email)   
             
            elif palavra in prefixoemail.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,tipoalerta= "description-danger",  msg=mensagem, dominioemail=email)
             
        
    if email != "@enind.com.br" and email != "@enindservicos.com.br":
            mensagem = 'e-mail invalido, por gentileza utilizar os disponiveis nas caixas.'
            return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, msg=mensagem, tipoalerta= "description-danger", dominioemail=email)

   
    nome_btn = "Validar"
    email_completo = prefixoemail + email
    envio, Valor_Erro, strtoken = funcoes.emails.registra_codigo_email(email_completo)
    if envio == True:
          mensagem = "Email enviado com sucesso!"
          return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "description-success", dominioemail=email)
    else:
          mensagem = f"Houve um erro no envido do email, erro: {Valor_Erro}" 
          return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "description-danger", dominioemail=email)
    