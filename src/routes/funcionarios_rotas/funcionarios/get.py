from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models import models
from src.config.login.token import funcionario_logado


@router.get('/funcionarios', status_code=200)
async def buscar_funcionario(db: db_dependency, response: Response, user: funcionario_logado):
    try:
        funcionarios = db.query(models.Funcionarios).all()
        lista_de_funcionarios = []
        for funcionario in funcionarios:
            funcionario_atual = {}
            funcionario_atual['matricula'] = funcionario.matricula
            funcionario_atual['nome'] = funcionario.nome
            funcionario_atual['email'] = funcionario.email
            funcionario_atual['administrador'] = funcionario.administrador
            funcionario_atual['ativo'] = funcionario.ativo
            lista_de_funcionarios.append(funcionario_atual)
        if len(lista_de_funcionarios) == 0:
            return {'mensagem': 'ainda não foi cadastrado nenhum funcionário no sistema'}
        else:
            lista_de_funcionarios = sorted(lista_de_funcionarios, key=lambda x:x['nome'])
            return {'mensagem': f'Veja todos os {len(lista_de_funcionarios)} funcionários cadastrados em data', 'data': lista_de_funcionarios}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.get('/funcionarios/logado', status_code=200)
async def buscar_funcionario_logado(db: db_dependency, response: Response, user: funcionario_logado):
    try:
        funcionario = db.query(models.Funcionarios).filter(models.Funcionarios.matricula == user['id']).first()
        if not funcionario:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'não foi encontrado funcionário com esse id'}
        funcionario_atual = {}
        funcionario_atual['matricula'] = funcionario.matricula
        funcionario_atual['nome'] = funcionario.nome
        funcionario_atual['email'] = funcionario.email
        funcionario_atual['administrador'] = funcionario.administrador
        funcionario_atual['ativo'] = funcionario.ativo

        return {'mensagem': 'funcionário encontrado, veja em data', 'data': funcionario_atual}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}

@router.get("/funcionarios/{matricula}", status_code=200)
async def buscar_funcionario_por_id(db:db_dependency, response: Response, user: funcionario_logado, matricula: str):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'essa função exige o funcionário ser administrador'}
    try:
        funcionario = db.query(models.Funcionarios).filter(models.Funcionarios.matricula == matricula).first()
        if not funcionario:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'não foi encontrado funcionário com esse id'}
        funcionario_atual = {}
        funcionario_atual['matricula'] = funcionario.matricula
        funcionario_atual['nome'] = funcionario.nome
        funcionario_atual['email'] = funcionario.email
        funcionario_atual['administrador'] = funcionario.administrador
        funcionario_atual['ativo'] = funcionario.ativo
        return {'mensagem': 'funcionário encontrado, veja em data', 'data': funcionario_atual}
    
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro de servidor {e}'}

app.include_router(router)