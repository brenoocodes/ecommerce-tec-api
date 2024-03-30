from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from src.configure import app, db_dependency, router, SECRET_KEY, url, templates
from src.models import models
from src.config.email.enviar.send import enviar_email
from src.config.login.token import criar_token_acesso, verificar_token

verificador = OAuth2PasswordBearer(tokenUrl="token") 

@router.post("/verificar/{email}")
async def verificar_email(email: str, db: db_dependency):
    try:
        email_existente = db.query(models.Clientes).filter(models.Clientes.email == email).first()
        if not email_existente:
            raise HTTPException(status_code=404, detail="Email não encontrado")
        
        token = criar_token_acesso(email_existente.email, email_existente.id, timedelta(minutes=30))
        link = f"{url}/confirmar_email/{token}"
        enviar_email(ema=email, assunto='Confirme seu email', link=link, template='confirmar.html')
        novo_token = models.EmailToken(
            cliente_id = email_existente.id,
            email = email_existente.email,
            token = token,
            data_criacao = datetime.now(timezone.utc)
        )
        db.add(novo_token)
        db.commit()
        return {"messagem": "Email de verificação enviado com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de servidor: {e}")

@router.get("/confirmar_email/{token}")
async def confirmar_email(token: str, db: db_dependency, request: Request):
    try:
        resposta = verificar_token(token=token)
        if 'username' in resposta:
            token_email = db.query(models.EmailToken).filter(models.EmailToken.cliente_id == resposta['id']).all()
            if not token_email:
                return {'mensagem': 'Algum erro na verificação dos tokens'}
            for token in token_email:
                db.delete(token)
            db.commit()
            cliente = db.query(models.Clientes).filter(models.Clientes.id == resposta['id']).first()
            if not cliente:
                return {'mensagem': 'Algum erro na verificação dos tokens'}
            cliente.email_confirmado = True
            db.commit()
            return {'mensagem': 'Conta verificada com sucesso'}
        else:
            templates.TemplateResponse("tokeninspirada.html", {"request": request})
    
    except Exception as e:
        print(e)
        return templates.TemplateResponse("tokeninspirada.html", {"request": request})

app.include_router(router)

