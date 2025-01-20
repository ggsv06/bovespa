import requests as rq
from bs4 import BeautifulSoup as bs
import time
import random

# Funções
def virgula(temp_str):
    # Input str, output float, contendo ',' ou '.'
    if ',' in temp_str:
        ltemp = temp_str.split(',')
        return float('.'.join(i for i in ltemp))
    else:
        return float(temp_str)

def pregao_inst(papel):
    # Retira da internet o valor instantâneo da cotação no papel fornecido
    # Navegador config
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    # Links dos sites contento o preço
    link = f'https://statusinvest.com.br/acoes/{papel}'
    timestamp = int(time.time()) + random.randint(1, 1000)
    # Requests do conteúdo em html dos sites
    req = rq.get(link, headers=headers)
    # Tratamento do conteúdo do site
    site = bs(req.content,'html.parser')
    #Retirar valores das ações
    return virgula(site.find('strong', class_='value').get_text())

def taxa(valor1, valor2):
    # Encontra a taxa entre os dois valores de cotação
    # Float values
    output = valor1/valor2 if valor1>=valor2 else valor2/valor1
    return float(output)

if __name__ == '__main__':
    # Input do nome do ativo
    papel1 = input('Digite o nome do primeiro ativo: ')
    papel2 = input('Digite o nome do segundo ativo: ')
    comprai1 = virgula(input(f'Valor de compra da {papel1}: '))
    comprai2 = virgula(input(f'Valor de compra da {papel2}: '))
    taxa_adicional = virgula(input(f'Taxa desejada %: '))*0.01

    taxai = taxa(comprai1, comprai2)

    while True:
        final1 = pregao_inst(papel1)
        final2 = pregao_inst(papel2)
        print(final1)
        print(final2)

        # Cálculos taxa
        taxa_inst = taxa(final1, final2)

        # Condicional de parada
        if taxa_inst >= taxai + taxa_adicional:
            meta = True
            break
        else:
            meta = False
            pass
        time.sleep(60)

    if meta:
        print('Meta atingida!')
