    # -*- coding: utf-8 -*-
"""Autor: Breno Rodrigues Brito"""
import json

from requests import put, post
import logging

from wscbot.scripts import req
from wscbot.scripts import pegachave
from wscbot.scripts import erro
from wscbot.scripts import rotinas
from wscbot.scripts.zipparser import ziphandler

def main(ip_servidor,username,senha,ip_superg,filepath,data):
    """
    Envia uma requisição GET HTTP para o endereço cadastrado,
    fornecendo como parâmetros da requisição o usuário e senha informados;
    Pega a resposta da requisição e escreve num arquivo;
    Criptografa o conteúdo do arquivo com base em uma chave compartilhada com o Super Gerente;
    Envia o arquivo criptografado para o Super Gerente;
    Registra a data do envio e o resultado da comunicação.
    """

    # Faz a requisição do arquivo zip
    zip_path = req.req(ip_servidor, filepath)

    dicionario = ziphandler(zip_path)
    for arquivo in dicionario:
        logger.debug('Inicio do envio de dados')
        coleta = json.loads(dicionario[arquivo])['results']
        for registro in coleta:
            registro = json.dumps(registro)

            f = post(ip_superg,data={'json_reg':registro})
            erro.is_error_p(f)

logger = logging.getLogger("WSCBot")
