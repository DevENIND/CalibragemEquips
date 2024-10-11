


################################################################################################################################################################################
################################################################################ CONEXAO COM BANCO DE DADOS ####################################################################
################################################################################################################################################################################

from calendar import month
from email.utils import formataddr
from logging.config import ConvertingDict
from time import strptime
from tkinter.tix import Form
from xmlrpc.client import DateTime
import mysql.connector
from wtforms import form

def mysql_connection(host, user, passwd, database=None):
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd,
            database = database
        )
        return connection
    except Exception as inst:
        return False

def caputra_maior_dado(Tabela, banco_de_dados, dado):
    try:
        query = f'Select max({dado}) from {Tabela}'
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False

def caputra_maiorID(Tabela, banco_de_dados):
    try:
        query = f'Select max(id) from {Tabela}'
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False
    
def inserir_banco(Tabela, Dados, banco_de_dados):
    try: 
        query = f'INSERT INTO {Tabela} VALUES ({Dados})'
        print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        banco_de_dados.commit()
        return True
    except Exception as inst:
        return False
    
def delete_banco(Tabela, Condicao, banco_de_dados):
    try:
        query = f'DELETE FROM {Tabela} WHERE {Condicao}'
        print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        banco_de_dados.commit()
        return True
    except Exception as inst:
        return False
    
def seleciona_dados(dados, Tabela, Condicao, banco_de_dados):
    try:
        if Condicao != '':
            query = f'SELECT {dados} FROM {Tabela} WHERE {Condicao}'
        else:
            query = f'SELECT {dados} FROM {Tabela}'
        #print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False
 
def seleciona_dados_org(dados, Tabela, Condicao, colOrdem,banco_de_dados):
    try:
        query = f'SELECT {dados} FROM {Tabela} WHERE {Condicao} order by {colOrdem}'
        #print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False

def atualiza_dados(Campos_Dados, Tabela, Condicao, banco_de_dados):
    try:
        query = f"UPDATE {Tabela} SET {Campos_Dados} WHERE {Condicao}"
        print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        banco_de_dados.commit()
        return True
    except Exception as inst:
        return False

def analisa_texto(texto):
    NaoPermitidos = f"SELECT,DELETE,INSERT,',%,{chr(34)},TRUNCATE,DROP,JOIN,"
    palavras = NaoPermitidos.split(",")

    for palavra in palavras:
            if palavra in texto.upper():
                return False
    
    return True
    

################################################################################################################################################################################
################################################################################## PREPARANDO EMAILS ###########################################################################
################################################################################################################################################################################

import mimetypes

import smtplib
import getpass


from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random


import datetime

def prepara_corpo_email_Codigo(NumCod):
    agora = datetime.datetime.now()
    hora_agora = agora.time().hour
    
    if hora_agora > 0 and hora_agora <= 12:
        corpo = 'Bom Dia!'
    elif hora_agora >= 13 and hora_agora <= 18:
        corpo = 'Boa Tarde!'
    elif hora_agora > 18:
        corpo = 'Boa Noite'
    

    corpo += f"<br><br>Segue o numero para acessar a pagina de equipamentos calibraveis da ENIND: {NumCod}<br><br>"
    corpo += f"<b>E-mail automatico, utilizado apenas para envio.</b>"
    corpo += f"<br> Atenciosamente,"

    return corpo


def registra_codigo_email(email):
    try:
        codigo = ""
        for x in range(6):
            aleatorio = random.randrange(0,9)
            codigo += str(aleatorio)
        
        print (codigo)

        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        Condicao = f'EMAIL = "{email}" and App = "CalibEqto"'
        registro = delete_banco('VALIDAEMAIL',Condicao, banco_de_dados)
        
        print('dados excluidos')
        
        records = caputra_maiorID('VALIDAEMAIL', banco_de_dados)
        records = records.fetchall()

        for row in records: myID = row[0]
            
        if myID is None: 
            myID = 0 
        else:
            myID = myID+1
        
        strtoken = ""
        strtoken = gera_token_email()
        print(strtoken)
        dados = f'{myID},"{email}",{codigo},"{strtoken}","CalibEqto"'
        registro = inserir_banco('VALIDAEMAIL',dados, banco_de_dados)
        
        print('dados inseridos')
        
        corpo_email = prepara_corpo_email_Codigo(codigo)
        print(corpo_email)
        assunto = "Codigo Calibragem de Equipamentos - ENIND"
        envio, MsgErro = enviar_email(email, assunto, corpo_email)
        
        if envio:
             print('email enviado com sucesso')
             return True, ""
        else:
            print(f'houve um erro ao enviar o email:{MsgErro}')
            return False, MsgErro
        return True
    except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst
   
def valida_codigo(email, codigo):
    try:
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        records = caputra_maiorID('VALIDAEMAIL', banco_de_dados)
        records = records.fetchall()

        dados = f'CODIGO, TOKEN'
        condicao = f'EMAIL = "{email}"'
        records = seleciona_dados(dados,'VALIDAEMAIL',condicao,banco_de_dados)

        Cod_Val = ""
        for row in records:
            Cod_Val = row[0]
            strToken = row[1]
            
        if Cod_Val == "": 
            print('Nao possui codigo cadastrado')
            return False, "Cadastro na tabela nao identificado", ""
        elif int(Cod_Val) == int(codigo):
            print('codigo correto')
            return True,"", strToken
        else:
            print('codigo nao corresponde')
            return False, "Codigo nao coincide com o do email",""

    except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst, ""


def enviar_email(para, assunto, corpo):
    try:
        sender = 'NF@enind.com.br'
        password = 'Enind@2020'
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = para
        msg['Subject'] = assunto
        
        CaminhoGIF = "https://enind.com.br/wp-content/uploads/2024/03/Automacao-ENIND-4-1-1.gif"
        CorpoEmail = corpo +  f"<br><img src={chr(34)}{CaminhoGIF}{chr(34)}>" 
        
        # Corpo da mensagem
        msg.attach(MIMEText(CorpoEmail, 'html', 'utf-8'))

        raw = msg.as_string()


        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp_server:
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.starttls()  # Protege a conexao
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, para, raw)
            smtp_server.quit()


        return True, ""
    except Exception as inst:
       return False, inst
        
import string
import random

def gera_token_email(size=30, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
   strtoken = ''.join(random.choice(chars) for _ in range(size))
   return strtoken

def valida_token_email(strTokenEnv):
     try:
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        dados = f'EMAIL'
        condicao = f'TOKEN = "{strTokenEnv}"'
        records = seleciona_dados(dados,'VALIDAEMAIL',condicao,banco_de_dados)

        for row in records:
            email = row[0]
     
        if email == "": 
            return False, "", ""
        else:
            return True, "", email
        
     except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst, ""
     
"""
###############################################################################################################################################################################################################################
###############################################################################################################################################################################################################################
###############################################################################################################################################################################################################################
##################################################################################################### REGISTROS DOS EQUIPAMENTOS ##############################################################################################
############################################################################################################################################################################################################################### 
###############################################################################################################################################################################################################################
###############################################################################################################################################################################################################################
 """

def valida_log_edicao(email, OS):
     try:
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        dados = f'tipo_us, OS'
        condicao = f'email = "{email}"'
        records = seleciona_dados(dados,'CalEqto_Us',condicao,banco_de_dados)

        for row in records:
            tipous = row[0]
            OS_perm = row[1]
            
        if tipous == "": 
            return False, "", ""
        else:
           if tipous == 'Usuario':
                if OS_perm == OS or OS == '':
                    return True, ""
                else:
                    return False, ""
           else:
               return True, ""
        
     except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst,""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CAPITURA DAS INFORMACOES DO REGISTRO NO BANCO DE DADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def puxa_registro(ideqpto, email):

    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"

    banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)
    
    lista_retorno = []
    if ideqpto == 'new':
         #id_eqpto =  caputra_maiorID('CalEqto_Eqtos',banco_de_dados)
         lista_retorno.append({
                "id": '',
                "Desc": '',
                "Tag": '',
                "NumSerie": '',
                "Fabricante": '',
                "Status": '',
                "OS": '',
                "Certificadora": '',
                "QtdMeses": '',
                "DataCalibracao": '',
                "DataValidade": '',
                "ArqCertificacao": ''
            })
         validacao, msgerro = valida_log_edicao(email, '')
    else:
        dados = f'*'
        condicao = f'id = "{ideqpto}"'
        records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)

        for eqto in records:
            lista_retorno.append({
                "id": eqto[0],
                "Desc": eqto[1],
                "Tag": eqto[2],
                "NumSerie": eqto[3],
                "Fabricante": eqto[4],
                "Status": eqto[5],
                "OS": eqto[6],
                "Certificadora": eqto[7],
                "QtdMeses": eqto[8],
                "DataCalibracao": format(eqto[9],"%Y-%m-%d"),
                "DataValidade": format(eqto[10],"%Y-%m-%d"),
                "ArqCertificacao": eqto[11]
            })
            
        validacao, msgerro = valida_log_edicao(email, lista_retorno[0]['OS'])
    
    return lista_retorno, validacao, msgerro

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VERIFICA SE O REGISTRO ESTA PRONTO PARA SER REALIZADO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def valida_registro(registros):
    chvFal = []
    MsgErro = ""
    for chaves in registros[0].keys():
        if registros[0][chaves] == "":
            MsgErro =  MsgErro + f'{chaves} precisa ser preenchido {chr(10)}'
            
    if registros[0]['Status'] != 'Ativo' and registros[0]['Status'] != 'Inativo':
        MsgErro = MsgErro + f'Campo de Status precisa ser igual a Ativo ou Inativo  \n'
        
    if registros[0]['OS'] != '':
        if float(registros[0]['OS']) < 100:
            MsgErro = MsgErro + f'Campo OS precisa ser preenchido com valor superior a 100  \n'
        
    
        if not float(registros[0]['OS']).is_integer():
            MsgErro = MsgErro + f'Campo OS deve ser inteiro apenas  \n'
    
    
        if float(registros[0]['OS']) > 9999:
            MsgErro = MsgErro + f'Campo OS tem o limite de 4 digitos ex.: OS 50000981 colocar OS 981  \n'
        
    if registros[0]['QtdMeses'] != '':
        if float(registros[0]['QtdMeses']) < 0.033:
            MsgErro = MsgErro + f'Quantidade de meses deve ser superior a 0.033, um dia. \n'
    
    
    if registros[0]["DataCalibracao"] != '':
        DataAtual = datetime.datetime.now()
        DataCalibr = datetime.datetime.strptime(registros[0]["DataCalibracao"], "%Y-%m-%d")
        if DataCalibr > DataAtual:
            MsgErro = MsgErro + f'Data de calibracao esta superior a data atual.  \n'
        if DataCalibr.year < 2000:
            MsgErro = MsgErro + f'Ano de calibracao dever ser superior a 2000  \n'
        if DataCalibr.month <= 0:
            MsgErro = MsgErro + f'Mes de calibracao dever ser superior a 0  \n'
        if DataCalibr.day <= 0:
            MsgErro = MsgErro + f'Data de calibracao dever ser superior a 0  \n'
      
    if MsgErro == "":
       return True, ""
    else:
       return False, MsgErro
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% REALIZA REGISTROS DE ALTERACOES NO BANCO DE DADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#Registra as alteracoes realizadas no banco de dados de alteracoes    
def registra_bd_alt(Campos, Valores, idEqto, email, referencia):
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)
    
    records = caputra_maior_dado('CalEqto_Alt', banco_de_dados, 'idAlt')
    records = records.fetchall()
    
    for row in records: myIDAlt = row[0]
            
    if myIDAlt is None: 
        myIDAlt = 0 
    else:
        myIDAlt = myIDAlt+1
    
    HoraAtual = date.today()
    HoraAtual = datetime.datetime.now()
    HoraAtual = format(HoraAtual,"%H:%M:%S")
    print(f'hora atual: {HoraAtual}')

    for x in range(len(Campos)):
        campo = Campos[x]
        valor = Valores[x]
        Msg = ''
        DataAtual = date.today()
        
        DataAtual = format(DataAtual,"%Y:%m:%d")

        #Condicao = f"idEqto = {idEqto} and dataAlt = '{DataAtual}' and campo = '{campo}' and valor = '{valor}' and email = '{email}'"
        #registro = delete_banco('CalEqto_Alt',Condicao, banco_de_dados)
        
        #if registro == True:
        #    print(f'Exclusao referente ao Eqto: {idEqto} campo: {campo}, valor: {valor} {chr(10)}')
            
        records = caputra_maiorID('CalEqto_Alt', banco_de_dados)
        records = records.fetchall()
    
        for row in records: myID = row[0]
            
        if myID is None: 
            myID = 0 
        else:
            myID = myID+1
        
        
        valores_bd = f"{myID},{myIDAlt},{idEqto},'{DataAtual}', '{HoraAtual}' ,'{campo}','{valor}','{email}', '{referencia}'"

        registroBD = inserir_banco('CalEqto_Alt',valores_bd, banco_de_dados)
        
        if registroBD == False:
            Msg = Msg + f'REGISTRO DE ALTERACAO - Uma alteracao nao foi inserida corretamente, referente ao Eqto: {idEqto} campo: {campo}, valor: {valor} {chr(10)}'
            print(f'REGISTRO DE ALTERACAO - Uma alteracao nao foi inserida corretamente, referente ao Eqto: {idEqto} campo: {campo}, valor: {valor}')
            
    if Msg != '':
        return False, Msg
    else:
        return True, Msg
    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% EXECUTA O REGISTRO DO EQUIPAMENTO NO BANCO DE DADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from datetime import date, timedelta

def realiza_registro(ideqpto, email, registros):

    Alteracao = False
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    campos_alt= []
    valores_alt = []
    valores_antes_alt = []
    campos_dados = ''

    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    
    Validacao, Msg = valida_registro(registros)

    if Validacao == False: return Validacao, Msg, "",'','',''
    
    lista_antes = []
    if ideqpto == 'new':
        
        validacao, msgerro = valida_log_edicao(email, registros[0]['OS'])
        
        if validacao == False:
            return False, 'Nao possui permissao para registrar nessa OS.',msgerro,'','',''
        else:
            dados = "NumSerie"
            NumSerieReg = registros[0]["NumSerie"]
            condicao = f"NumSerie = '{NumSerieReg}'"
            records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)
            
            numSerie = ""

            for eqto in records:
                numSerie = eqto[0]

            if numSerie != "": return False, 'Ja tem um equipamento com esse numero de serie.',msgerro,'','',''
            
            Alteracao = True
         
    else:
        
        dados = f'*'
        condicao = f"id = {ideqpto}"
        records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)

        for eqto in records:
            lista_antes.append({
                "id": eqto[0],
                "Desc": eqto[1],
                "Tag": eqto[2],
                "NumSerie": eqto[3],
                "Fabricante": eqto[4],
                "Status": eqto[5],
                "OS": eqto[6],
                "Certificadora": eqto[7],
                "QtdMeses": eqto[8],
                "DataCalibracao": format(eqto[9],"%Y-%m-%d"),
                "ArqCertificacao": eqto[11]
            })
        
        if lista_antes == []:
            return False, 'Equipamento nao registrado.','','','',''
         
        validacao, msgerro = valida_log_edicao(email, lista_antes[0]['OS'])
           
        if validacao == False:
            return False, 'Seu login nao pode alterar arquivos dessa OS','','','',''

        idEqui = registros[0]['id']
        if registros[0]['ArqCertificacao'][:3] != "ID_":
            DataAtual = datetime.datetime.now()
            DataAtual = format(DataAtual,"%d-%m-%Y_%H-%M-%S")
            ArquivoCert = "ID_" + str(idEqui) + "_" +  DataAtual + ".pdf"
            registros[0]['ArqCertificacao'] =  ArquivoCert
        else:
            ArquivoCert = registros[0]['ArqCertificacao']
        
        for chaves in registros[0].keys():
            if chaves.upper() != 'ID':
                if registros[0][chaves] != lista_antes[0][chaves]:
                    if chaves.upper() != 'DATACALIBRACAO' and chaves.upper() != "OS" and chaves.upper() != "QTDMESES":
                        Alteracao = True
                        campos_alt.append(chaves)
                        valores_alt.append(registros[0][chaves])
                        campos_dados = campos_dados + f"{chaves} = '{registros[0][chaves]}', "
                    elif chaves.upper() == "OS" or chaves.upper() == "QTDMESES":
                        if float(registros[0][chaves]) != float(lista_antes[0][chaves]):
                            Alteracao = True
                            campos_alt.append(chaves)
                            valores_alt.append(registros[0][chaves])
                            campos_dados = campos_dados + f"{chaves} = '{registros[0][chaves]}', "
                    else:
                        DataCalib =  datetime.datetime.strptime(registros[0]["DataCalibracao"], "%Y-%m-%d")
                        if DataCalib != lista_antes[0][chaves]:
                            Alteracao = True
                            campos_alt.append(chaves)
                            valores_alt.append(registros[0][chaves])
                            campos_dados = campos_dados +  f"{chaves} = '{registros[0][chaves]}', "
        
    if Alteracao == False:
        if validacao == False:
            return validacao, msg, msgerro,'','',''
        else:
            return False, 'O registro premaneceu com os dados anteriores.','','',''
    else:
        if ideqpto == 'new':
            records = caputra_maiorID('CalEqto_Eqtos', banco_de_dados)
            records = records.fetchall()
            ValoresBD = ''
            for row in records: myID = row[0]
            
            if myID is None: 
                myID = 0 
            else:
                myID = myID+1
            
            idEqui = myID 
            print(registros[0]["DataCalibracao"])
            DataCalib =  datetime.datetime.strptime(registros[0]["DataCalibracao"], "%Y-%m-%d")
            DiaVcto = DataCalib.day
            MesVcto = 0
            MesVcto =  int(float(DataCalib.month) + float(registros[0]["QtdMeses"]) % 12)
            
            AnoVcto = 0
            if MesVcto > 12: 
                MesVcto -= 12
                AnoVcto = 1
                
            if MesVcto < 10: MesVcto = "0" + str(MesVcto)
            if DiaVcto < 10: DiaVcto = "0" + str(DiaVcto)
                
            AnoVcto = int(AnoVcto + DataCalib.year + float(registros[0]["QtdMeses"]) // 12)
            
            DataVcto = '{}-{}-{}'.format(AnoVcto, MesVcto, DiaVcto)
            DataCalib = format(DataCalib,"%Y-%m-%d")
            
            DataAtual = datetime.datetime.now()
            DataAtual = format(DataAtual,"%d-%m-%Y_%H-%M-%S")
            
            ValoresBD = ""
            ValoresBD = ValoresBD + str(myID)
            ArquivoCert = "ID_" + str(idEqui) + "_" +  DataAtual + ".pdf"
            
            registros[0]['ArqCertificacao'] = ArquivoCert
            
            #Registrando dados no banco de dados
            for chaves in registros[0].keys():
                if chaves.upper() != 'ID' :
                    if chaves.upper() != 'DATACALIBRACAO' and chaves.upper() != 'ARQCERTIFICACAO':
                        if chaves.upper() != 'OS' and  chaves.upper() != 'QTDMESES':
                            ValoresBD = ValoresBD + f", '{registros[0][chaves]}'"
                        else:
                            ValoresBD = ValoresBD + f", {registros[0][chaves]}"
                    campos_alt.append(chaves)
                    valores_alt.append(registros[0][chaves])
            
            
            
            ValoresBD += f",'{DataCalib}', '{DataVcto}', '{ArquivoCert}'"
            print(ValoresBD)
            
    
            
            registroBD = inserir_banco('CalEqto_Eqtos',ValoresBD, banco_de_dados)
            
            if registroBD == False:
                return False, "Nao foi possivel realizar o registro desse item no banco de dados.", msgerro,'', DataVcto , ArquivoCert

            strAlt = f'Registro'
            
            registroBD = registra_bd_alt(campos_alt,valores_alt,myID,email,strAlt)
            
            if registroBD == False:
                return False, "Nao foi possivel realizar o registro de alteracoes desse item", msgerro,'', DataVcto, ArquivoCert

            msg = 'Registro realizado com sucesso!'
        else:
            strAlt = f'Alteracao'
            condicao = f'id = {registros[0]["id"]}'
            idEqui = registros[0]["id"]
            
            
            DataCalib =  datetime.datetime.strptime(registros[0]["DataCalibracao"], "%Y-%m-%d")
            DiaVcto = DataCalib.day
            MesVcto = 0
            MesVcto =  int(float(DataCalib.month) + float(registros[0]["QtdMeses"]) % 12)
            
            AnoVcto = 0
            if MesVcto > 12: 
                MesVcto -= 12
                AnoVcto = 1
                
            AnoVcto = int(AnoVcto + DataCalib.year + float(registros[0]["QtdMeses"]) // 12)
                
            if MesVcto < 10: MesVcto = "0" + str(MesVcto)
            if DiaVcto < 10: DiaVcto = "0" + str(DiaVcto)
                
            DataVcto = '{}-{}-{}'.format(AnoVcto, MesVcto, DiaVcto)
            campos_dados = campos_dados + f"DataValidade = '{DataVcto}'"

            registroBD = atualiza_dados(campos_dados,'CalEqto_Eqtos', condicao,banco_de_dados)
            
            if registroBD == False:
                return False, "Nao foi possivel deletar item", msgerro, DataVcto, ArquivoCert

            registroBD = registra_bd_alt(campos_alt,valores_alt,registros[0]["id"],email,strAlt)
            
            if registroBD == False:
                return False, "Nao realizar o registro das alteracoes desse item.", msgerro,'' ,DataVcto, ArquivoCert

            msg = 'Registro alterado com sucesso!'
            
        return validacao, msg, msgerro, idEqui, DataVcto, ArquivoCert
    
import time
import os
from pathlib import Path

def busca_alteracoes(ideqto):
    
    if ideqto == '':
        return []

    print(f'buscando alt do equipamento {ideqto}')

    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    dados = '*'
    condicao = f'idEqto = {ideqto}'
    colOrg = 'idAlt DESC'
    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    
    records = seleciona_dados_org(dados, 'CalEqto_Alt', condicao, colOrg, banco_de_dados)
    records = records.fetchall()
    lista_retorno = []
    IDsProcessadas = []
    
    for row in records:
        if not row[1] in IDsProcessadas:
            lista_retorno.append({
                "Titulo": row[8],
                "Data": datetime.datetime.strftime(row[3],"%d-%m-%Y"),
                "Hora": str(row[4]),
                "Descricao": f'o campo "{row[5]}" passou a ser "{row[6]}"',
                "Email":row[7]
                })
            IDsProcessadas.append(row[1])
        else:
            lista_retorno[-1]["Descricao"] = lista_retorno[-1]["Descricao"] + f'\n o campo "{row[5]}" passou a ser "{row[6]}"'
    
    return lista_retorno

def restaura_arquivo_cert(ideqto, NomeArqDel, PastaArquivos):
    
    #Deletando o arquivo errado
    #caminho_arquivo = Path(NomeArqDel)
    #caminho_arquivo.unlink
    
    print(f'o arquivo {NomeArqDel} foi deletado com sucesso!')
    
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    

    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    
    #Deletando a alteracao com o arquivo errado
    condicao = f"idEqto = {ideqpto} and campo = 'ArqCertificacao' and Valor = '{NomeArqDel}'"
    ValorDb = delete_banco('CalEqto_Alt',condicao, banco_de_dados)
    
    #Buscando a ultima alteracao antes da realizada
    dados = 'MAX(IDAlt)'
    condicao = f"idEqto = {ideqto} and Campo = 'ArqCertificacao'"

    records = seleciona_dados(dados,'CalEqto_Alt', condicao, banco_de_dados)
    records.fetchall
    
    for row in records: IDAlt = row[0]
    
    if IDAlt != '':
        dados = 'ArqCertificacao'
        condicao = f"idEqto = {ideqto} and Campo = 'ArqCertificacao' and idAlt = {IDAlt}"

        records = seleciona_dados(dados,'CalEqto_Alt', condicao, banco_de_dados)
        records.fetchall
        
        for row in records: NomeArqAntigo = row[0]
        
        if NomeArqAntigo != '':
            condicao = f"id = {ideqto}"
            campo_dados = f"ArqCertificacao = '{NomeArqAntigo}'"
            
            atualizacao = atualiza_dados(campo_dados,'CalEqto_Eqtos',condicao, banco_de_dados)
            return True, NomeArqAntigo, ''
        else:
            return False,'', 'Nao foi possivel identificar o arquivo anterior ao postado'
    else:
        return False,'', 'Nao tem IDs de alteracoes antes da excluida'

def Lista_Eqtos():
    lista_equipamentos = []
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"

    banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)
    
    dados = f'*'
    condicao = f''
    records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)

    for eqto in records:
        lista_equipamentos.append({
            "id": eqto[0],
            "Desc": eqto[1],
            "Tag": eqto[2],
            "NumSerie": eqto[3],
            "Fabricante": eqto[4],
            "Status": eqto[5],
            "OS": eqto[6],
            "Certificadora": eqto[7],
            "QtdMeses": eqto[8],
            "DataCalibracao": format(eqto[9],"%Y-%m-%d"),
            "DataValidade": format(eqto[10],"%d/%m/%Y"),
            "ArqCertificacao": eqto[11]
        })
    
    return lista_equipamentos

def deleta_arquivos_eqto(ideqpto, PastaArquivos):
    for arquivo in os.listdir(PastaArquivos):
        if f"ID_{ideqpto}" in arquivo:
             Path(f'{PastaArquivos}/{arquivo}').unlink()



def deleta_registro_eqto(ideqpto, email):
    Alteracao = False
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    campos_alt= []
    valores_alt = []
    valores_antes_alt = []
    
    
    OS = ''
    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    dados = 'OS'
    condicao = f'id = {ideqpto}'
    records = seleciona_dados(dados,'CalEqto_Eqtos', condicao, banco_de_dados)
    records.fetchall
    
    for row in records: OS = row[0]

    if OS != '':
        validacao, msgerro = valida_log_edicao(email, OS)
           
        if validacao == False:
            return False, 'Seu login nao pode deletar itens dessa OS',''

        condicao = f"id = {ideqpto}"
        ValorDb = delete_banco('CalEqto_Eqtos', condicao, banco_de_dados)
    
        if ValorDb == False:
              return False, f'Nao foi possivel deletar a id {ideqto}',''

        condicao = f"idEqto = {ideqpto}"
        ValorDb = delete_banco('CalEqto_Alt',condicao, banco_de_dados)
    
        if ValorDb == False:
              return False, f'Nao foi possivel deletar as alteracoes dessa id',''

    
        msg = "Dado excluido com sucesso!"
        return validacao, msg, msgerro
    else:
        return False, 'Nao foi possivel identificar a OS do registro',''
    


def puxa_Imagens(ideqpto, email, PastaArquivos):
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    OS = ''
    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    dados = 'OS'
    condicao = f'id = {ideqpto}'
    records = seleciona_dados(dados,'CalEqto_Eqtos', condicao, banco_de_dados)
    records.fetchall
    
    for row in records: OS = row[0]

    if OS != '':
        validacao, msgerro = valida_log_edicao(email, OS)
    else:
        validacao = False

    listaImgs = []
    contagem = 0
    for arquivo in os.listdir(PastaArquivos):
        if f"ID_{ideqpto}" in arquivo:
             listaImgs.append(arquivo)
             contagem += 1
    
    return validacao, listaImgs, contagem
 
def deleta_arquivos_img(Pasta,Nome):
    Path(f'{Pasta}/{Nome}').unlink()
             

if __name__ == '__main__':
   registro = []
   
   registro.append({
        "id": 0,
        "Desc": 'NomeEqto',
        "Tag": 'Tag',
        "NumSerie": 'NumSerie',
        "Fabricante": 'Nome Fabricante',
        "Status": 'Ativo',
        "OS": 981,
        "Certificadora": 'CertificadoraEqto',
        "QtdMeses":-1,
        "DataCalibracao": "2024-10-01",
        "ArqCertificacao": 'Arquivo.pdf'
    })
   
   validacao, msg, msgerro, idEqui, DataVcto, ArquivoCert = realiza_registro(registro[0]['id'], 'wagner.barreiro@enind.com.br', registro)
   #lista_retorno, validacao, msgerro = deleta_registro_eqto(registro[0]['id'], 'wagner.barreiro@enind.com.br')
   #lista_retorno = busca_alteracoes(0)
   #lista_retorno, validacao, msgerro  = puxa_registro(0,'wagner.barreiro@enind.com.br')
   #deleta_arquivos_eqto(0)
   #validacao, listaImgs, contagem = puxa_Imagens(0, 'wagner.barreiro@enind.com.br', pasta)

   #print(lista_retorno)
   print(validacao)
   print(msg)
   print(msgerro)