from pydantic import BaseModel, Json
from typing import Optional, Dict

class Produto(BaseModel):
    categoria_id: str
    nome: str
    nome_estoque: str
    descricao: Dict[str, str]
