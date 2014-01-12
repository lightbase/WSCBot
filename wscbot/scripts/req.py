# -*- coding: utf-8 -*-
"""Autor: Breno Rodrigues Brito"""
# from requests import get
import urllib
import logging
import os

from wscbot.scripts.erro import is_error_g
from wscbot.scripts.tratamento import t_dados


def download_file(url, filepath):
    """Baixa o arquivo de coleta na url indicada"""

    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    local_filename = filepath + "coleta.zip"
    urllib.urlretrieve(url, local_filename)
    return local_filename


def req(domain,filepath): #Recebia domain e data
    """Envia uma requisição GET HTTP para o endereço cadastrado,
    fornecendo como parâmetros da requisição o usuário e senha informados;"""

    # payload = {'user' : 'username',
    #            'pass' : 'senha'}
    logger.debug('Mandando requisição')
    url = domain + 'zip/coleta'

    # values = {'data_coleta':data}

    arquivo_coleta = download_file(url,filepath) # , param=values
    arquivo_coleta = os.path.abspath(arquivo_coleta)

    # ATENCAO!!!
    # tem de se testar se o data precisa de encoding!!

    # funcionava para o módulo requests
    # Não sei como fazer para o urllib
    # is_error_g(arquivo_coleta)

    return arquivo_coleta

logger = logging.getLogger("WSCBot")

# zip para baixar e testar:
# http://10.0.0.149/api/doc/arquivos/29/download