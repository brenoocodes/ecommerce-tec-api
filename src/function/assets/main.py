import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime, timedelta

# Inicialize o aplicativo Firebase Admin
cred = credentials.Certificate("firebase-admin.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "ecoomerce-brenocodes-tec.appspot.com"
})

# Crie uma referência ao bucket de armazenamento
bucket = storage.bucket()

caminho_arquivo_local = "perfil.jpg"


nome_arquivo_firebase = "fotos/perfil8.jpg"

# Faz o upload do arquivo para o armazenamento do Firebase
blob = bucket.blob(nome_arquivo_firebase)
blob.upload_from_filename(caminho_arquivo_local)


blob.acl.public = True
blob.acl.save()

# Obtém a URL pública de download do arquivo
url_publica = blob.public_url

print("URL pública de download:", url_publica)
