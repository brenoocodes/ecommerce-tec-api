from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Produtos
from src.config.login.token import funcionario_logado

@router.get("/funcionario/produtos", status_code=200)
async def buscar_produtos_funcionarios(db: db_dependency, response: Response, user: funcionario_logado):
    try:
        produtos = db.query(Produtos).all()
        lista_de_produtos = []
        for produto in produtos:
            produto_atual = {}
            produto_atual['id'] = produto.id
            produto_atual['nome'] = produto.nome
            produto_atual['nome_estoque'] = produto.nome_estoque
            produto_atual['categoria'] = produto.categoria.nome
            produto_atual['descricao'] = produto.descricao
            lista_de_produtos.append(produto_atual)
        if len(lista_de_produtos) == 0:
            return {'mensagem': 'ainda não foi cadastrado nenhum produto'}
        else:
            lista_de_produtos = sorted(lista_de_produtos, key=lambda x:x['nome'])
            return {'mensagem': f'Foram encontrados {len(lista_de_produtos)} produtos', 'data': lista_de_produtos}
    except Exception as e:
       print(e)
       response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
       return {'mensagem': f'erro interno do servidor {e}'}


app.include_router(router)