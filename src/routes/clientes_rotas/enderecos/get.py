from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Clientes
from src.config.login.token import logado

@router.get("/cliente/me/enderecos", status_code=200)
async def buscar_enderecos_cliente_logado(db: db_dependency, response: Response, user: logado):
    try:
        cliente = db.query(Clientes).filter(Clientes.id == user['id']).first()
        if not cliente:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'mensagem': 'Esse cliente não existe'}
        lista_de_enderecos = []
        for endereco in cliente.enderecos:
            endereco_atual = {}
            endereco_atual['id'] = endereco.id
            endereco_atual['cep'] = endereco.cep
            endereco_atual['estado'] = endereco.estado
            endereco_atual['cidade'] = endereco.cidade
            endereco_atual['logradouro'] = endereco.logradouro
            endereco_atual['bairro'] = endereco.bairro
            endereco_atual['numero'] = endereco.numero
            endereco_atual['referencia'] = endereco.referencia
            endereco_atual['observacao'] = endereco.observacao
            lista_de_enderecos.append(endereco_atual)
        if len(lista_de_enderecos) == 0:
            return {'mensagem': f'O usuário {cliente.nome} não tem nenhum endereço associado'}
        else:
            return {'mensagem': f'foram encontrados {len(lista_de_enderecos)} associados a esse usuário', 'data': lista_de_enderecos}

    except Exception as e: 
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro de servidor {e}'}


app.include_router(router)