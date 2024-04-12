from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Carrinhos, Clientes
from src.config.login.token import logado
from src.schemas.carrinho import index


@router.post('/cliente/me/carrinhos', status_code=201)
async def criar_carrinho_cliente(db: db_dependency, response: Response, carrinho: index.Carrinho, user: logado):
    cliente_id = user['id']
    try:
        cliente_existente = db.query(Clientes).filter(Clientes.id == cliente_id).first()
        if not cliente_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'Não existe cliente cadastrado com esse id no nosso sistema'}
        carrinho_existente = db.query(Carrinhos).filter(Carrinhos.nome == carrinho.nome, Carrinhos.cliente_id == cliente_id).first()
        if carrinho_existente: 
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {'mensagem': 'Você já cadastrou um carrinho com esse nome'}
        novo_carrinho = Carrinhos(
            cliente_id= cliente_existente.id,
            nome= carrinho.nome,
            descricao= carrinho.descricao
        )
        db.add(novo_carrinho)
        db.commit()
        db.refresh(novo_carrinho)

        return {'mensagem': 'Novo carrinho adicionado com sucesso', 'data': novo_carrinho}


    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro do servidor {e}'}


app.include_router(router)