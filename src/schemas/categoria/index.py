from pydantic import BaseModel, EmailStr
from typing import Optional

class Categoria(BaseModel):
    nome: str