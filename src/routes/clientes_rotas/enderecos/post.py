from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Clientes, Enderecos
from src.schemas.enderecos import index
from src.function.cep.index import buscar_por_cep
from src.config.login.token import logado

@router.get('/cliente/cep/{cep}', status_code=200)
async def buscar_cep(cep: str, response: Response):
    try:
        resposta = buscar_por_cep(cep=cep)
        return resposta
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro do servidor {e}'}

@router.post('/cliente/endereco', status_code=201)
async def adicionar_endereco_ao_cliente(db: db_dependency, user: logado, response: Response, endereco: index.Endereco):
    try:
        cliente_id = user['id']
        cliente_existente = db.query(Clientes).filter(Clientes.id == cliente_id).first()
        if not cliente_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'esse id não está associado a nenhum cliente'}
        novo_endereco = Enderecos(
            cliente_id=cliente_id,
            cep = endereco.cep,
            cidade= endereco.cidade,
            estado=endereco.estado,
            logradouro= endereco.logradouro,
            bairro=endereco.bairro,
            numero=endereco.numero,
            referencia=endereco.referencia,
            observacao=endereco.observacao
        )
        db.add(novo_endereco)
        db.commit()
        db.refresh(novo_endereco)
        return {'mensagem': f'Novo endereço associado ao usuário {cliente_existente.nome}', 'data': novo_endereco}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro de servidor {e}'}

app.include_router(router)