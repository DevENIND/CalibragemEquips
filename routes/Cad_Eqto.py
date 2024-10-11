from flask import Blueprint

Cad_Eqto_route = Blueprint('Cad_Eqto', __name__)

@Cad_Eqto_route.route('/')
def lista_eqto():
    #Lista os equipamentos
    return {"pagina": "lista_equipamento"}

@Cad_Eqto_route.route('/', methods=['POST'])
def inserir_eqto():
    #Inserir os dados do equipamento
    pass

@Cad_Eqto_route.route('/new')
def form_eqto():
    #Formulário para cadastramento de equipamentos
    return {"pagina": "formulario equipamentos"}


@Cad_Eqto_route.route('/<int:id_eqto>')
def datalhe_eqto(id_eqto):
    #Exibir detalhes do equipamento
    pass

@Cad_Eqto_route.route('/<int:id_eqto>/edit')
def form_edit_eqto(id_eqto):
     #Formulário para editar um equipamento
    pass

@Cad_Eqto_route.route('/<int:id_eqto>/update', methods=['PUT'])
def update_eqto(id_eqto):
     #Atualiza o cadastro do equipamento
    pass

@Cad_Eqto_route.route('/<int:id_eqto>/delete', methods=['DELETE'])
def deleta_eqto(id_eqto):
     #deletar o cadastro do equipamento
    pass