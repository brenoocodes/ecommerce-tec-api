from pydantic import BaseModel, Json
from typing import Optional, Dict

class ProdutoAoCarrinho(BaseModel):
    itemestoque_id: str
    quantidade: int