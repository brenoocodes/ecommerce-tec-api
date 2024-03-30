from fastapi import HTTPException, Response, status, Request, Form
from src.configure import app, db_dependency, router, SECRET_KEY, url, templates
from src.models.models import Clientes, EmailToken
from datetime import timedelta, datetime, timezone
from src.config.email.enviar.send import enviar_email
from src.config.login.token import criar_token_acesso, verificar_token
from fastapi.responses import HTMLResponse
from src.config.login.senha import gerar_senha_criptografada

@router.post("/recuperar_senha/{username}", status_code=200)
async def recuperar_senha(username: str, db: db_dependency, response: Response):
    try:    
        if '@' in username:
            cliente_existente = db.query(Clientes).filter(Clientes.email == username).first()
        else:
            cliente_existente = db.query(Clientes).filter(Clientes.cpf == username).first()   
        if not cliente_existente:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'mensagem': 'Cliente ainda não cadastrado'}
        token = criar_token_acesso(cliente_existente.email, cliente_existente.id, timedelta(minutes=10))
        link = f"{url}/verificar_token_senha/{token}"
        enviar_email(ema=cliente_existente.email, assunto='Troque sua senha', link=link, template='trocarsenha.html')

        return {'mensagem': 'Email para trocar de senha enviado com sucesso'}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de servidor: {e}")
    

@router.get("/verificar_token_senha/{token}", response_class=HTMLResponse)
async def verificar_token_de_mudanca_de_senha(token: str, request: Request):
    try:
        resposta = verificar_token(token=token)
        if 'username' in resposta:
            return templates.TemplateResponse("trocar_senha.html", {"request": request, "token": token})
        else:
            return templates.TemplateResponse("tokeninspirada.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("tokeninspirada.html", {"request": request})

@router.post("/trocar_senha/{token}", status_code=200)
async def trocar_senha( db: db_dependency, response: Response, request: Request, token: str, nova_senha: str = Form(...), confirmar_senha: str = Form(...)):
    try:
        if nova_senha != confirmar_senha:
            raise HTTPException(status_code=400, detail="As senhas não coincidem")

        resposta = verificar_token(token=token)

        if 'username' not in resposta:
            raise HTTPException(status_code=404, detail="Token inválido ou expirado")

        if '@' in resposta['username']:
            cliente = db.query(Clientes).filter(Clientes.email == resposta['username']).first()
        else:  
            cliente = db.query(Clientes).filter(Clientes.cpf == resposta['username']).first()

        if cliente:
            senha = gerar_senha_criptografada(nova_senha)
            cliente.senha = senha
            cliente.email_confirmado = True
            db.commit()
            token_email = db.query(EmailToken).filter(EmailToken.cliente_id == resposta['id']).all()
            if token_email:
                for registro in token_email:
                    db.delete(registro)
                db.commit()
            return {'mensagem': 'Senha atualizada com sucesso'}

        return {'mensagem': 'Cliente não encontrado'}

    except Exception as e:
        return templates.TemplateResponse("tokeninspirada.html", {"request": request})

app.include_router(router)

