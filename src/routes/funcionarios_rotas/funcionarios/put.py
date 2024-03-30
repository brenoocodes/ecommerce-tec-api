from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models import models
from src.schemas.funcionarios.index import FuncionarioAlterar
from src.config.login.senha import gerar_senha_criptografada
from src.config.login.token import funcionario_logado
from datetime import datetime, timezone

@router.put('/funcionarios/{matricula}', status_code=200)
async def alterar_funcionario(db: db_dependency, response: Response, user: funcionario_logado, matricula: str, funcionario: FuncionarioAlterar):
    try:
        funcionario_existente = db.query(models.Funcionarios).filter(models.Funcionarios.matricula == matricula).first()
        if not funcionario_existente:
          response.status_code = status.HTTP_404_NOT_FOUND
          return {'mensagem': 'essa matricula não está associada a nenhum funcionário'}
        if funcionario.email is not None:
            if funcionario.email != funcionario_existente.email:
                email_existente = db.query(models.Funcionarios).filter(models.Funcionarios.email == funcionario.email).first()
                if email_existente:
                    response.status_code = status.HTTP_406_NOT_ACCEPTABLE
                    return {'mensagem': 'Esse e-mail no qual você está cadastrando já está associado a outro usuário'}
                funcionario_existente.email = funcionario.email
        if funcionario.nome is not None:
            funcionario_existente.nome = funcionario.nome
        if funcionario.ativo is not None:
            funcionario_existente.ativo = funcionario.ativo
        if funcionario.administrador is not None:
            funcionario_existente.administrador = funcionario.administrador
        if funcionario.senha is not None:
            senha = gerar_senha_criptografada(funcionario.senha)
            funcionario_existente.senha = senha
        funcionario_existente.data_atualizacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(funcionario_existente)
        return {'mensagem': f'O funcionário {funcionario_existente.nome} com matricula {funcionario_existente.matricula} foi alterado com sucesso'}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}



app.include_router(router)