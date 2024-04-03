from fastapi import status, Response, Query
from src.configure import app, router, db_dependency
from src.models.models import Produtos
from src.config.login.token import logado
from src.function.assets.firebase import buscar_url

@router.get('/cliente/me/produtos', status_code=200)
async def buscar_o_produto_cliente(
db: db_dependency,
user: logado,
response: Response,
# cor: str = Query(None, description="Busque por uma cor ", example="Vermelho, Branco ou Amarelo")
):
    try:
        produtos = db.query(Produtos).all()
        lista_de_produtos = []
        for produto in produtos:
            produto_atual = {}
            produto_atual['id'] = produto.id
            produto_atual['nome'] = produto.nome
            produto_atual['descrição'] = produto.descricao
            produto_atual['ativado'] = produto.ativado
            produtos_em_estoque = []

            for produto_em_estoque in sorted(produto.itens_estoque, key=lambda x: x.quantidade_vendida, reverse=True):
                produto_em_estoque_atual = {}
                produto_em_estoque_atual['id'] = produto_em_estoque.id
                produto_em_estoque_atual['cor'] = produto_em_estoque.cor
                produto_em_estoque_atual['preco'] = produto_em_estoque.preco
                produto_em_estoque_atual['ativado'] = produto_em_estoque.ativado
                produto_em_estoque_atual['quantidade_vendida'] = produto_em_estoque.quantidade_vendida
                produto_em_estoque_atual['quantidade'] = produto_em_estoque.quantidade

                lista_de_imagens = []

                for imagem in produto_em_estoque.imagens:
                    url = buscar_url(imagem['caminho'])
                    lista_de_imagens.append({imagem['nome']: url})

                produto_em_estoque_atual['imagens'] = lista_de_imagens
                produtos_em_estoque.append(produto_em_estoque_atual)

            produto_atual['produtos_em_estoque'] = produtos_em_estoque

            lista_de_produtos.append(produto_atual)
        if len(lista_de_produtos) == 0:
            return {'mensagem': 'Nenhum produto cadastrado'}
        
        lista_de_produtos = sorted(lista_de_produtos, key=lambda x:x['nome'])

        return {'mensagem': f'Ao todo temos {len(lista_de_produtos)}', 'data': lista_de_produtos}
    
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro interno de servidor {e}'}


app.include_router(router)