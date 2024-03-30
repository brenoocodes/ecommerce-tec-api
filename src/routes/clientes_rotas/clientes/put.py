from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Clientes
from src.schemas.clientes import index
from src.config.login.senha import gerar_senha_criptografada
from src.config.email.verificar.verificarmail import verificar_email
from src.config.login.token import logado
from datetime import datetime, timezone

@router.put('/clientes/alterar/{id}', status_code=200)
async def alterar_cliente(db: db_dependency, response: Response, user: logado, id: str, cliente: index.ClienteAlterar):

    try:
        cliente_existente = db.query(Clientes).filter(Clientes.id == id).first()
        if not cliente_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'esse id não está associado a nenhum cliente'}
        if cliente.email is not None:
            if cliente.email != cliente_existente.email:
                email_existente = db.query(Clientes).filter(Clientes.email == cliente.email).first()
                if email_existente:
                    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
                    return {'mensagem': 'Esse e-mail no qual você está cadastrando já está associado a outro usuário'}
            cliente_existente.email = cliente.email
        if cliente.nome is not None:
            cliente_existente.nome = cliente.nome
        if cliente.senha is not None:
            senha = gerar_senha_criptografada(cliente.senha)
            cliente_existente.senha = senha
        if cliente.data_de_nascimento is not None:
            cliente_existente.data_de_nascimento = cliente.data_de_nascimento
        cliente_existente.data_atualizacao = datetime.now(timezone.utc)
        db.commit()  
        db.refresh(cliente_existente)
        return {'mensagem': f'o cliente {cliente_existente.nome} foi alterado com sucesso'}      
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}