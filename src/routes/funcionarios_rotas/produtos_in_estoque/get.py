from fastapi import status, Response, Form, File, UploadFile
from src.configure import app, router, db_dependency
from src.models.models import ItensEstoque, Produtos
from src.config.login.token import funcionario_logado
from src.function.assets.firebase import salvar_firebase
from typing import List, Optional
from .functions import verificar_files


@router.get('/teste')
def pegar_imagens(db: db_dependency):
    produto_estoque = db.query(ItensEstoque).filter(ItensEstoque.id == "rho84VRhT8pCZmyAmeTbmsP1t5jjX7Lh0omX").first()
    print(produto_estoque.produto.nome)
    print(produto_estoque.produto.categoria.nome)

app.include_router(router)