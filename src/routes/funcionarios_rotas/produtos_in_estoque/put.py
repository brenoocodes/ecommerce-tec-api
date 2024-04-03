from fastapi import status, Response, Form, File, UploadFile
from src.configure import app, router, db_dependency
from src.models.models import ItensEstoque, Produtos
from src.config.login.token import funcionario_logado
from src.function.assets.firebase import salvar_firebase
from typing import List, Optional
from .functions import verificar_files
from datetime import datetime, timezone


@router.put("/funcionario/produtos/estoque", status_code=200)
async def modificar_produto_em_estoque(
    db: db_dependency,
    user: funcionario_logado,
    response: Response,
    produto_estoque_id: str = Form(...),
    preco: Optional[float] = Form(None),
    quantidade: Optional[int] = Form(None),
    ativo: Optional[bool] = Form(None),
    files: List[UploadFile] = File(None)
):
    if user['adm'] == False:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'mensagem': 'Esta função exige que o funcionário seja administrador'}
    try:
        produto_estoque_existente = db.query(ItensEstoque).filter(ItensEstoque.id == produto_estoque_id).first()
        if not produto_estoque_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
        if preco is not None:
            produto_estoque_existente.preco = preco
        if quantidade is not None:
            produto_estoque_existente.quantidade = quantidade
        if ativo is not None:
            produto_estoque_existente.ativado = ativo
        produto = str(produto_estoque_existente.produto.nome)
      
        if files is not None:
            imagens = []
            verificar = await verificar_files(files=files)
            if not "ok" in verificar:
                return verificar
            for imagem in files:
                caminho = f'produtos/{produto_estoque_existente.produto.categoria.nome}/{produto}/{produto_estoque_existente.cor}/{imagem.filename}'
                caminho = caminho.replace(' ', '')
                resposta = await salvar_firebase(nome_arquivo_firebase=caminho, arquivo=imagem)
                if not 'https:' in resposta:
                    return {'mensagem': f'Erro ao salvar a imagem {imagem.filename} no servidor'}
                imagem_atual = {'nome': imagem.filename, 'caminho': caminho}
                imagens.append(imagem_atual)
            produto_estoque_existente.imagens = imagens
        produto_estoque_existente.data_atualizacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(produto_estoque_existente)
        return {'mensagem': 'Produto em estoque alterado com sucesso', 'data': produto_estoque_existente}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'mensagem': f'Erro do servidor: {e}'}



app.include_router(router)