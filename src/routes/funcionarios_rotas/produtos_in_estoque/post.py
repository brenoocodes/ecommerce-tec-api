from fastapi import status, Response, Form, File, UploadFile
from src.configure import app, router, db_dependency
from src.models.models import ItensEstoque, Produtos
from src.config.login.token import funcionario_logado
from src.function.assets.firebase import salvar_firebase
from typing import List
from .functions import verificar_files



@router.post("/funcionario/produtos/estoque", status_code=201)
async def criar_produto_estoque(
    db: db_dependency,
    user: funcionario_logado,
    response: Response,
    produto_id: str = Form(...),
    cor: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    files: List[UploadFile] = File(...)
):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'Esta função exige que o funcionário seja administrador'}
    
    try:
        produto_existente = db.query(Produtos).filter(Produtos.id == produto_id).first()
        if not produto_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'O ID informado não está relacionado a nenhuma categoria'}

        produto = db.query(ItensEstoque).filter(
            ItensEstoque.produto_id == produto_existente.id,
            ItensEstoque.cor == cor
        ).first()

        if produto:
            return {'mensagem': 'Este produto já está relacionado a esta cor. Use uma nova cor ou edite o produto existente.'}
        fotos = files
        verificacao = await verificar_files(fotos)

        if verificacao != "ok":
            return verificacao

        imagens = []
        for imagem in files:
            caminho =  f'produtos/{produto_existente.categoria.nome}/{produto_existente.nome}/{cor}/{imagem.filename}'
            caminho = caminho.replace(' ', '')
            resposta = await salvar_firebase(nome_arquivo_firebase=caminho, arquivo=imagem)
           
            if not 'https:' in resposta:
                return {'mensagem': f'Erro ao salvar a imagem {imagem.filename} no servidor'}
            imagem_atual = {'nome': imagem.filename, 'caminho': caminho}
            imagens.append(imagem_atual)
            
        novo_produto_ao_estoque = ItensEstoque(
            produto_id= produto_existente.id,
            preco=preco,
            cor = cor,
            quantidade=quantidade,
            imagens= imagens
        )
        db.add(novo_produto_ao_estoque)
        db.commit()
        db.refresh(novo_produto_ao_estoque)

        return {'mensagem': 'Novo produto cadastrado com sucesso', 'data': novo_produto_ao_estoque}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro do servidor: {e}'}



        # for file in files:
        #     file_name = os.path.splitext(file.filename)[0]

        #     file.filename = f"{file_name}.png"

        #     print(file)
            
        #     resposta = await salvar_firebase(nome_arquivo_firebase=f'produtos/computador/{file.filename}', arquivo=file)


        #     print(resposta)


        # return {'mensagem': 'Deu certo caralho'}

@router.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}

app.include_router(router)