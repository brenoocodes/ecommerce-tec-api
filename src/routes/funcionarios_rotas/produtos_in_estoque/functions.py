import os

async def verificar_files(files):
    nomes = ['imagem-principal', 'imagem-2', 'imagem-3', 'imagem-4', 'imagem-5']
    imagem_principal_presente = False

    if len(files) < 1 or len(files) >= 6:
        return {'mensagem': 'É permitido adicionar entre 1 e 5 imagens para cada cor. Qualquer número fora desse intervalo não será permitido.'}
    
    for file in files:
        file_name = os.path.splitext(file.filename)[0]
        if file_name == 'imagem-principal':
            imagem_principal_presente = True
        
        if file_name not in nomes:
            return {"mensagem": f"A imagem {file_name} não está com nome correto, os nomes devem estar no seguinte intervalo => ['imagem-principal', 'imagem-2', 'imagem-3', 'imagem-4', 'imagem-5']. Isso acontece para padronizar o banco e melhorar a experiência"}
        if len(await file.read()) > 5000000:
            return {'mensagem': f'A imagem {file_name} é maior que 4MB e não são aceitas imagens maiores que isso'}
        
        content_type = file.content_type
        if content_type != "image/png":
            return {'mensagem': f'O arquivo {file_name} não é do tipo PNG'}
        
        # Resetar o ponteiro do arquivo após a leitura
        await file.seek(0)
    
    if not imagem_principal_presente:
        return {'mensagem': 'Falta a imagem => imagem-principal.png.'}
    
    return "ok"
