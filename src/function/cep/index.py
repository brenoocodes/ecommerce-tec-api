import requests

def buscar_por_cep(cep):
    cep = str(cep)
    cep = cep.replace('-', '').replace('.','').replace('', '')
    if len(cep) != 8:
        return {'mensagem': 'Confere o cep, parece que ele não tem oito dígitos'}
    link = f'https://viacep.com.br/ws/{cep}/json/'

    resposta = requests.get(link)
    resposta_json = resposta.json()

    if 'erro' in resposta_json:
        if resposta_json['erro']:
            return {'mensagem': 'Esse CEP não foi encontrado'}
    else:
        return {'estado': resposta_json['uf'], 'cidade': resposta_json['localidade']}

    return {'mensagem': 'CEP encontrado, mas detalhes não disponíveis'}
