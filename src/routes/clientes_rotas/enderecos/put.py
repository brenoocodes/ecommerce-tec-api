from fastapi import status, Response
from src.configure import app, router, db_dependency
from src.models.models import Enderecos
from src.schemas.enderecos.index import EnderecoAlterar
from src.config.login.token import logado
from datetime import datetime, timezone

@router.put("/cliente/me/enderecos/{id}", status_code=200)
async def alterar_endereco_cliente(db: db_dependency, response: Response, id: str, user: logado, endereco: EnderecoAlterar):
    try:
        endereco_existente = db.query(Enderecos).filter(Enderecos.id == id).first()
        if not endereco_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'Não existe endereço para o ID informado'}
        if endereco_existente.cliente_id != user['id']:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'mensagem': 'Você não tem permissão para alterar esse endereço'}
        
        for atributo, valorinclasse in EnderecoAlterar.__annotations__.items():
            if getattr(endereco, atributo) is not None:
                setattr(endereco_existente, atributo, getattr(endereco, atributo))
        endereco_existente.data_atualizacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(endereco_existente)
        return {'mensagem': 'Endereço alterado com sucesso', 'data': endereco_existente}

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': 'Ocorreu um erro ao processar a solicitação', 'detalhes': str(e)}

app.include_router(router)