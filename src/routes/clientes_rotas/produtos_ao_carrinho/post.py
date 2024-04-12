from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Carrinhos, ItensEstoque, ItensCarrinhos
from src.config.login.token import logado
from datetime import datetime, timezone
from src.schemas.produto_ao_carrinho import index

@router.post("/cliente/me/produtos_ao_carrinho/{carrinho_id}", status_code=201)
async def adicionar_produtos_ao_carrinho(db: db_dependency, user: logado, response: Response, carrinho_id: str, produto_ao_carrinho: index.ProdutoAoCarrinho):
    user_id = user['id']
    try:
        carrinho_existente = db.query(Carrinhos).filter(Carrinhos.cliente_id == user_id, Carrinhos.id== carrinho_id).first()
        if not carrinho_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'O carrinho com esse id não está associado a esse cliente ou o carrinho_id não existe'}
        item_estoque_existente = db.query(ItensEstoque).filter(ItensEstoque.id == produto_ao_carrinho.itemestoque_id).first()
        if not item_estoque_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'O id fornecido para o produto em estoque não existe'}
        if produto_ao_carrinho.quantidade > item_estoque_existente.quantidade:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {'mensagem': f'Você não pode adicionar {produto_ao_carrinho.quantidade} ao carrinho pois a quantidade em estoque é de {item_estoque_existente.quantidade}'}
        novo_item_ao_carrinho = ItensCarrinhos(
            carrinho_id=carrinho_existente.id,
            itemestoque_id= item_estoque_existente.id,
            valor_unitario= item_estoque_existente.preco,
            quantidade=produto_ao_carrinho.quantidade
        )
        carrinho_existente.quantidade_itens += 1
        carrinho_existente.valor_total += item_estoque_existente.preco * produto_ao_carrinho.quantidade
        carrinho_existente.data_atualizacao = datetime.now(timezone.utc)

        db.add(novo_item_ao_carrinho)
        db.commit()
        db.refresh(novo_item_ao_carrinho)
        return {'mensagem': f'Novo item cadastrado com sucesso ao carrinho {carrinho_existente.nome}', 'data': novo_item_ao_carrinho}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro interno do servidor {e}'}


app.include_router(router)

