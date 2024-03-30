from fastapi import status, Response, Query
from src.configure import app, router, db_dependency
from src.models.models import Clientes
from src.config.login.token import logado


@router.get("/clientes/me", status_code=200)
async def buscar_cliente_logado(db: db_dependency, response: Response, user: logado):
    try:
        cliente_id = user['id']
        cliente_existente = db.query(Clientes).filter(Clientes.id == cliente_id).first()
        if not cliente_existente:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'mensagem': 'Esse cliente não existe'}
        if cliente_existente.ativo == False:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'mensagem': 'Esse cliente foi desativado'}
        resposta = {
            'cliente_id': cliente_existente.id,
            'cliente_nome': cliente_existente.nome,
            'cliente_email': cliente_existente.email
        }
        return {'mensagem': 'cliente está ok', 'data': resposta}
    except Exception as e:
        print(e)


app.include_router(router)