from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Categorias
from src.config.login.token import logado
from src.function.assets.firebase import buscar_url

@router.get('/cliente/me/categorias', status_code=200)
async def buscar_categorias_cliente(db: db_dependency, response: Response, user: logado):
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
                produto_atual['descrição'] = produto.descricao
                produto_atual['ativado'] = produto.ativado
                produtos_em_estoque = []

                for produto_em_estoque in produto.itens_estoque:
                    produto_em_estoque_atual = {}
                    produto_em_estoque_atual['id'] = produto_em_estoque.id
                    produto_em_estoque_atual['cor'] = produto_em_estoque.cor
                    produto_em_estoque_atual['preco'] = produto_em_estoque.preco
                    produto_em_estoque_atual['ativado'] = produto_em_estoque.ativado
                    produto_em_estoque['quantidade'] = produto_em_estoque.quantidade
                    lista_de_imagens = []

                    for imagem in produto_em_estoque.imagens:
                        url = buscar_url(imagem['caminho'])
                        lista_de_imagens.append({imagem['nome']: url})

                    produto_em_estoque_atual['imagens'] = lista_de_imagens
                    produtos_em_estoque.append(produto_em_estoque_atual)

                produtos_em_estoque = sorted(produtos_em_estoque, key=lambda x: x['cor'])
                produto_atual['produtos_em_estoque'] = produtos_em_estoque
                lista_de_produtos.append(produto_atual)
            if len(lista_de_produtos) == 0:
                categoria_atual['produtos'] = 'Ainda não temos nenhum produto associado a essa categoria'
            lista_de_produtos = sorted(lista_de_produtos,key=lambda x:x['nome'])
           
            categoria_atual['produtos'] = lista_de_produtos

            lista_de_categorias.append(categoria_atual)
        if len(lista_de_categorias) == 0:
            return {'mensagem': 'Ainda não foi cadastrado nenhuma categoria'}
        else: 
            lista_de_categorias = sorted(lista_de_categorias, key=lambda x:x['nome'])
            return {'mensagem': f'Ao todo temos {len(lista_de_categorias)} categorias cadastradas', 'data':lista_de_categorias}

            

                        


    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro interno do servidor {e}'}

app.include_router(router)
