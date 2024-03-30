from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models import models
from src.schemas.funcionarios.index import Funcionario
from src.config.login.senha import gerar_senha_criptografada
from src.config.login.token import funcionario_logado


@router.post("/funcionarios", status_code=201)
async def criar_funcionario(db: db_dependency, funcionario: Funcionario, response: Response, user: funcionario_logado):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'essa função exige o funcionário ser administrador'}
    try:
        funcionario_existente = db.query(models.Funcionarios).filter(models.Funcionarios.email == funcionario.email).first()
        if funcionario_existente:
           response.status_code = status.HTTP_406_NOT_ACCEPTABLE
           return {'mensagem': 'Funcionário já cadastrado'}
        senha = gerar_senha_criptografada(funcionario.senha)
        novo_funcionario = models.Funcionarios(
            nome = funcionario.nome,
            email=funcionario.email,
            senha=senha,
            administrador=funcionario.administrador
        )
        db.add(novo_funcionario)
        db.commit()
        db.refresh(novo_funcionario)
        return {'mensagem': 'novo funcionário cadastrado com sucesso', 'data': novo_funcionario}
   
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}
 
app.include_router(router)