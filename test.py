import pandas as pd
import requests
#from bs4 import BeautifulSoup
import json

# URL base do arquivo.pt para páginas arquivadas
base_url = "https://arquivo.pt/wayback/cdx?url={url}&output=json"

# URLs arquivadas para os sites que queremos buscar informações
urls = {
    "Galp": "galp.com",
    "BP": "bp.com",
    "DGEG": "dgeg.gov.pt",
}

# Função para extrair dados de uma página específica



for nome, url in urls.items():
    print(f"Buscando dados de: {nome} com URL = {url}")
    resposta = requests.get(base_url.format(url=url))
    if resposta.status_code == 200:
        #soup = BeautifulSoup(resposta.content, 'html.parser')
        data = resposta.text
        print(data)
    else:
        print(f"Erro ao acessar {url}")


# Salvando os dados em formato JSON
with open("dados_combustiveis.json", "w") as arquivo_json:
    json.dump(data, arquivo_json, indent=4)

print("Dados salvos em 'dados_combustiveis.json'")

