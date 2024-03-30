from pydantic import BaseModel, EmailStr
from typing import Optional

class Clientes(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cpf: str
    data_de_nascimento: str

class ClienteAlterar(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    cpf: Optional[str] = None
    data_de_nascimento: Optional[str] = None