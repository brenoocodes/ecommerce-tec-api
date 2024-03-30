from fastapi import HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from src.configure import SECRET_KEY, ALGORITHM, db_dependency
from typing import Annotated
from src.models import models

ouauth2_bearer = OAuth2PasswordBearer(tokenUrl='/login')
ouauth2_bearer_funcionario = OAuth2PasswordBearer(tokenUrl='/login/funcionario')

def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token não é mais válido')


def criar_token_acesso(email: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) 

def criar_token_acesso_funcionario(email: str, user_id: str, adm: bool, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id, 'adm': adm}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def verificar_login(db: db_dependency, token: Annotated[str, Depends(ouauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            return {'mensagem': 'usuário inválido'}
        
        cliente = db.query(models.Clientes).filter(models.Clientes.id == user_id).first()
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente não existe')
        if not cliente.ativo:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Esse cliente foi desativado')

        return {'username': username, 'id': user_id}  

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token não é mais válido')

    # except Exception as e:
    #     print(e)
 
async def verificar_funcionario(db: db_dependency, token: Annotated[str, Depends(ouauth2_bearer_funcionario)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        
        if username is None or user_id is None:
            return {'mensagem': 'usuário inválido'}
        funcionario = db.query(models.Funcionarios).filter(models.Funcionarios.matricula == user_id).first()
        if not funcionario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Funcionário não existe')
        if not funcionario.ativo:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Esse funcionário está desativado')
        adm = funcionario.administrador
        return {'username': username, 'id': user_id, 'adm': adm}


    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token não é mais válido')

funcionario_logado = Annotated[dict, Depends(verificar_funcionario)]
logado = Annotated[dict, Depends(verificar_login)]



