from fastapi import status, Response, Query
from src.configure import app, router, db_dependency
from src.models.models import Produtos, ItensEstoque
from src.config.login.token import logado
from src.function.assets.firebase import buscar_url
from sqlalchemy import desc

@router.get('/cliente/me/produtos/{id}', status_code=200)
async def buscar_o_produto_cliente(
db: db_dependency,
id: str,
user: logado,
response: Response,
cor: str = Query(None, description="Busque por uma cor ", example="Vermelho, Branco ou Amarelo")
):
    try:
        produto = db.query(Produtos).filter(Produtos.id == id).first()
        
        produto_atual = {}
        produto_atual['id'] = produto.id
        produto_atual['nome'] = produto.nome
        produto_atual['descrição'] = produto.descricao
        produto_atual['ativado'] = produto.ativado
        lista_de_cor = []
        for item_estoque in produto.itens_estoque:
            lista_de_cor.append(item_estoque.cor)
        produto_atual['cores'] = lista_de_cor
        if cor: 
            produto_em_estoque = db.query(ItensEstoque).filter(ItensEstoque.cor == cor).first()
            if not produto_em_estoque:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'mensagem': 'Não existe produto em estoque com essa cor'}
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

        if not cor:
            produto_em_estoque = db.query(ItensEstoque).order_by(desc(ItensEstoque.quantidade_vendida)).first()
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

        produto_atual['produtos_em_estoque'] = produto_em_estoque_atual

       

        return {'mensagem': f'Segue o produto selecionado', 'data': produto_atual}
    
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro interno de servidor {e}'}


app.include_router(router)