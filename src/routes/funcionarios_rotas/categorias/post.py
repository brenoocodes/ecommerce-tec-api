from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Categorias
from src.config.login.token import funcionario_logado
from src.schemas.categoria import index


@router.post("/funcionario/categoria", status_code=201)
async def criar_nova_categoria(db: db_dependency, response: Response, user: funcionario_logado, categoria: index.Categoria):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'essa função exige o funcionário ser administrador'}
    try:
        categoria_existente = db.query(Categorias).filter(Categorias.nome == categoria.nome).first()
        if categoria_existente: 
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {'mensagem': f'A categoria {categoria_existente.nome} já está cadastrada'}
        nova_categoria = Categorias(
            nome=categoria.nome
        )
        db.add(nova_categoria)
        db.commit()
        db.refresh(nova_categoria)
        return {'mensagem': 'Nova categoria cadastrada com sucesso', 'data': nova_categoria}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro de servidor {e}'}

app.include_router(router)