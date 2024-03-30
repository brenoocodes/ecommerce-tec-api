from pydantic import BaseModel, EmailStr
from typing import Optional

class Endereco(BaseModel):
    cep: str
    cidade: str
    estado: str
    logradouro: str
    bairro: str
    numero: Optional[str]  = "Não informado"
    referencia: Optional[str] = "Não informado"
    observacao: Optional[str] = "Não informado"
 
class EnderecoAlterar(BaseModel):
    cep: Optional[str] = None,
    cidade: Optional[str] = None
    estado: Optional[str] = None
    logradouro: Optional[str] = None
    bairro: Optional[str] = None
    numero: Optional[str] = None
    referencia: Optional[str] = None
    observacao: Optional[str] = None

