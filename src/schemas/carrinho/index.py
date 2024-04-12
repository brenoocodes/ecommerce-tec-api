from pydantic import BaseModel, EmailStr
from typing import Optional

class Carrinho(BaseModel):
    nome: str
    descricao: str