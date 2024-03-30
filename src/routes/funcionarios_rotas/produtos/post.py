from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Categorias, Produtos
from src.config.login.token import funcionario_logado
from src.schemas.produto import index

@router.post("/funcionario/produtos", status_code=201)
async def criar_produto(db: db_dependency, response: Response, user: funcionario_logado, produto: index.Produto):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'essa função exige o funcionário ser administrador'}
    try:
        categoria_existente = db.query(Categorias).filter(Categorias.id == produto.categoria_id).first()
        if not categoria_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'O id informado na categoria_id não existe'}
        novo_produto = Produtos(
            categoria_id=categoria_existente.id,
            nome=produto.nome,
            nome_estoque=produto.nome_estoque,
            descricao=produto.descricao
        )
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return {'mensagem': 'Novo produto cadastrado com sucesso', 'data': novo_produto}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro do servidor {e}'}
    



app.include_router(router)