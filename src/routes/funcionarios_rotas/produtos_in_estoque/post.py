from fastapi import status, Response, Form, File, UploadFile
from src.configure import app, router, db_dependency
from src.models.models import Categorias, Produtos, id_generator
from src.config.login.token import funcionario_logado
from src.function.assets.firebase import salvar_firebase




@router.post("/funcionario/produtos/estoque", status_code=201)
async def criar_produto_estoque(db: db_dependency, user: funcionario_logado, response: Response,
produto_id: str = Form(...), file: UploadFile = File(...)                            
                                ):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'essa função exige o funcionário ser administrador'}
    
    try:
        print(produto_id)
        file.filename = "teste.png"
        
        resposta = await salvar_firebase(nome_arquivo_firebase=f'produtos/computador/{file.filename}', arquivo=file)


        print(resposta)


        return {'mensagem': 'Deu certo caralho'}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'erro do servidor {e}'}

app.include_router(router)