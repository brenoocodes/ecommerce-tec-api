from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Carrinhos
from src.config.login.token import logado
from src.function.horario.index import converter_horario

@router.get("/cliente/me/carrinhos", status_code=200)
async def buscar_carrinhos_do_cliente_logado(db: db_dependency, user: logado, response: Response):
    try:
        user_id = user['id']
        carrinhos = db.query(Carrinhos).filter(Carrinhos.cliente_id == user_id).all()
        lista_de_carrinhos = []
        for carrinho in carrinhos:
            carrinho_atual = {}
            carrinho_atual['id'] = carrinho.id
            carrinho_atual['nome'] = carrinho.nome
            carrinho_atual['cliente_id'] = carrinho.cliente_id
            carrinho_atual['cliente_nome'] = carrinho.cliente.nome
            carrinho_atual['descricao'] = carrinho.descricao
            carrinho_atual['fechado'] = carrinho.fechado
            carrinho_atual['quantidade_de_itens'] = carrinho.quantidade_itens
            carrinho_atual['valor_total'] = carrinho.valor_total
            carrinho_atual['data'] = converter_horario(carrinho.data_atualizacao)
            lista_de_produtos = []
            for produto in carrinho.itens:
                produto_atual = {}
                produto_atual['produto_estoque_id'] = produto.itemestoque_id
                produto_atual['produto_nome'] = produto.itemestoque.produto.nome
                produto_atual['preco'] = produto.valor_unitario
                produto_atual['quantidade'] = produto.quantidade
                lista_de_produtos.append(produto_atual)
            lista_de_produtos = sorted(lista_de_produtos, key=lambda x:x['produto_nome'])
            if len(lista_de_produtos) == 0:
                carrinho_atual['produtos'] = 'Ainda não foi associado nenhum produto a esse carrinho'
            if len(lista_de_produtos) > 0:
                carrinho_atual['produtos'] = lista_de_produtos
            lista_de_carrinhos.append(carrinho_atual)
        if len(lista_de_carrinhos) == 0:
            return {'mensagem': 'Esse usuário ainda não cadastrou nenhum carrinho'}
        else:
            lista_de_carrinhos = sorted(lista_de_carrinhos, key=lambda x: x['data']['dia'] + ' ' + x['data']['hora'], reverse=True)
            return {'mensagem': f'Ao todo esse usuário tem {len(lista_de_carrinhos)} carrinhos cadastrados', 'data': lista_de_carrinhos}


    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro do servidor {e}'}


app.include_router(router)