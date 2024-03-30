from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Categorias
from src.config.login.token import funcionario_logado


@router.get("/funcionario/categoria", status_code=200)
async def buscar_categorias_funcionarios(db:db_dependency, user: funcionario_logado, response: Response):
    try:
        categorias = db.query(Categorias).all()
        lista_de_categorias = []
        for categoria in categorias:
            categoria_atual = {}
            categoria_atual['id'] = categoria.id
            categoria_atual['nome'] = categoria.nome
            lista_de_produtos = []
            for produto in categoria.produtos:
                produto_atual = {}
                produto_atual['id'] = produto.id
                produto_atual['nome'] = produto.nome
                produto_atual['nome_estoque'] = produto.nome_estoque
                produto_atual['descricao'] = produto.descricao
                lista_de_produtos.append(produto_atual)
            if len(lista_de_produtos) == 0:
                categoria_atual['produto'] = 'Essa categoria ainda não tem produto associado a ela'
            else:
                lista_de_produtos = sorted(lista_de_produtos, key=lambda x:x['nome'])
                categoria_atual['produtos'] = lista_de_produtos
            lista_de_categorias.append(categoria_atual)
        if len(lista_de_categorias) == 0:
            return {'mensagem': 'Ainda não foi cadastrada nenhuma categoria'}
        else:
            lista_de_categorias = sorted(lista_de_categorias, key=lambda x:x['nome'])
            return {'mensagem': f'Encontramos ao todo {len(lista_de_categorias)} categorias cadastradas', 'data': lista_de_categorias}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro do servidor {e}'}


app.include_router(router)