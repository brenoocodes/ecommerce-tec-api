from fastapi import status, Response, Query
from src.configure import app, router, db_dependency
from src.models import models
from src.config.login.token import funcionario_logado
from fuzzywuzzy import process
from datetime import datetime
from sqlalchemy import and_


def criar_dicionario_cliente(cliente):
    cliente_atual = {
        'id': cliente.id,
        'nome': cliente.nome,
        'cpf': cliente.cpf,
        'email': cliente.email,
        'email_confirmado': cliente.email_confirmado,
        'ativo': cliente.ativo
    }
    return cliente_atual

@router.get('/funcionario/clientes', status_code=200)
async def buscar_clientes(db: db_dependency, response: Response, user: funcionario_logado,
cliente_id: str = Query(None, description="Digite o id do cliente: "),
cpf: str = Query(None, description="Digite o cpf no qual você deseja filtar, somente números"),
email: str = Query(None, description="Digite o email do cliente"),
nome: str = Query(None, description="Digite o nome no qual você deseja filtar"),
data_inicio: datetime = Query(None, description="Data de início cadastro do intervalo, formato americano ", example='2022-03-25 || dia 25 de março de 2022'),
data_fim: datetime = Query(None, description="Data de fim cadastro do intervalo, formato americano", example='2022-03-25 || dia 25 de março de 2022')
                          ):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'essa função exige o funcionário ser administrador'}
    try:
        query = db.query(models.Clientes)
        if cpf:
            cliente = query.filter(models.Clientes.cpf == cpf).first()
            if not cliente:
                return {'mensagem': 'Não foram encontrados clientes para esse filtro'}
            cliente = criar_dicionario_cliente(cliente=cliente)
            return {'mensagem': 'Foram encontrados o(s) seguinte(s) cliente(s) para esse filtro', 'data': cliente}
        if email:
            cliente = query.filter(models.Clientes.email == email).first()
            if not cliente:
                return {'mensagem': 'Não foram encontrados clientes para esse filtro'}
            cliente = criar_dicionario_cliente(cliente=cliente)
            return {'mensagem': 'Foram encontrados o(s) seguinte(s) cliente(s) para esse filtro', 'data': cliente}
        if cliente_id:
            cliente = query.filter(models.Clientes.id == cliente_id).first()
            if not cliente:
                return {'mensagem': 'Não foram encontrados clientes para esse filtro'}
            cliente = criar_dicionario_cliente(cliente=cliente)
            return {'mensagem': 'Foram encontrados o(s) seguinte(s) cliente(s) para esse filtro', 'data': cliente}
        if nome:
            nomes_clientes = [cliente.nome for cliente in db.query(models.Clientes).all()]

            nome_correspondente, pontuacao = process.extractOne(nome, nomes_clientes)
            
            if pontuacao >= 70:

                clientes = db.query(models.Clientes).filter(models.Clientes.nome == nome_correspondente).all()
                cliente = criar_dicionario_cliente(cliente=cliente)
                return {'mensagem': 'Foram encontrados o(s) seguinte(s) cliente(s) para esse filtro', 'data': cliente}
            else:
                return {'mensagem': f'Nenhum cliente encontrado para o nome fornecido. Você quis dizer {nome_correspondente}?'}
        
        if data_inicio and data_fim:
            clientes = query.filter(
                and_(
                    models.Clientes.data_criacao >= data_inicio,
                    models.Clientes.data_criacao <= data_fim
                )
            ).all()
            lista_de_clientes = [criar_dicionario_cliente(cliente) for cliente in clientes]

            if len(lista_de_clientes) == 0:
                return {'mensagem': 'Nenhum cliente encontrado no intervalo de data especificado'}
            else:
                lista_de_clientes = sorted(lista_de_clientes, key=lambda x:x['nome'])
                return {'mensagem': 'Clientes encontrados no intervalo de data especificado', 'data': lista_de_clientes}
        
        clientes = db.query(models.Clientes).all()
        lista_de_clientes = [criar_dicionario_cliente(cliente) for cliente in clientes]

        if len(lista_de_clientes) == 0:
            return {'mensagem': 'ainda não tem nenhum cliente cadastrado'}
        else:
            lista_de_clientes = sorted(lista_de_clientes, key=lambda x:x['nome'])
            return {'mensagem': 'clientes encontrados em data', 'data': lista_de_clientes}


    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}




app.include_router(router)
