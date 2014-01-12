# -*- coding: utf-8 -*-
"""Autor: Breno Rodrigues Brito"""
from requests import get

def pegachave(domain,username,senha):
    """Envia uma requisição GET HTTP para o endereço cadastrado, 
    fornecendo como parâmetros da requisição o usuário e senha informados;"""

    payload = {'user' : 'username',
               'pass' : 'senha'}

    recebe = get(domain, data=payload)
    # jsonfull = recebe.json()
    # bases = jsonfull["results"]
    chave = t_dados(recebe)


    return chave

