
import json, requests

nome = input("Escreva e o nome a ser buscado: ")
resposta = requests.get('https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}')

jsonDados = json.loads(resposta.text)

print(jsonDados[0]['res'][0])