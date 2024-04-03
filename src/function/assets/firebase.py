import os
import firebase_admin
from firebase_admin import credentials, storage
import imghdr
from datetime import timedelta, datetime

# Inicialize o Firebase fora das funções
def initialize_firebase():
    json_file_path = r"C:\Users\bscbr\Githubprogramacao\api\ecommerce-tec-api\src\function\assets\firebase-admin.json"
    #json_file_path = r"/etc/secrets/firebase-admin.json"

    if os.path.exists(json_file_path):
        pass
    else:
        print("O arquivo firebase-admin.json não pôde ser encontrado.")
        return None

    try:
        cred = credentials.Certificate(json_file_path)
        firebase_admin.initialize_app(cred, {
            "storageBucket": "ecoomerce-brenocodes-tec.appspot.com"
        })
        bucket = storage.bucket()
        return bucket
    except FileNotFoundError:
        print("Erro: O arquivo firebase-admin.json não pôde ser aberto.")
        return None

# Inicialize o Firebase uma vez no início do seu script
bucket = initialize_firebase()

# Função para salvar arquivo no Firebase
async def salvar_firebase(nome_arquivo_firebase, arquivo):
    if bucket is None:
        return "Erro: Não foi possível inicializar o Firebase."

    try:
        conteudo = await arquivo.read()

        # Verifica o tipo MIME do arquivo usando imghdr
        tipo_imagem = imghdr.what(None, h=conteudo)
        if tipo_imagem != 'png':
            return "Erro: O arquivo não é uma imagem PNG válida."

        blob = bucket.blob(nome_arquivo_firebase)
        blob.upload_from_string(conteudo, content_type='image/png')

        # Define o acesso público
        blob.acl.public = True
        blob.acl.save()

        # Obtém o URL público
        url_publica = blob.public_url
        return url_publica
    except Exception as e:
        print(f"Erro ao fazer upload do arquivo: {e}")
        return "Erro ao fazer upload do arquivo."


def buscar_url(caminho_arquivo_firebase):
    if bucket is None:
        return "Erro: Não foi possível inicializar o Firebase."

    blob = bucket.blob(caminho_arquivo_firebase)
    if not blob:
        return {'mensagem': 'Não foi possível encontrar o arquivo'}
    
    try:
        expires_at = datetime.now() + timedelta(weeks=1)
        url = blob.generate_signed_url(expires_at)
        return url
    except Exception as e:
        print(f"Erro ao buscar URL do arquivo: {e}")
        return "Erro ao buscar URL do arquivo."






# # Caminho local do arquivo "perfil.jpg"
# caminho_arquivo_local = r"c:\Users\bscbr\Githubprogramacao\api\api-tec-ecommerce\src\function\assets\perfil.jpg"

# # Nome do arquivo no Firebase
# nome_arquivo_firebase = "fotos/perfil8.jpg"

# # Tentar salvar a imagem no Firebase
# imagem = salvar_firebase(nome_arquivo_firebase=nome_arquivo_firebase, caminho_arquivo_local=caminho_arquivo_local)
# print(imagem)

