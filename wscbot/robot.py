
# -*- coding: utf-8 -*-

import os
import uuid
import logging
import zipfile
import requests
from wscbot import config

def main():

    """
    Envia uma requisição GET HTTP para o endereço cadastrado fornecendo
    como parâmetros da requisição o usuário e senha informados, pega a
    resposta da requisição e escreve num arquivo. Criptografa o conteúdo
    do arquivo com base em uma chave compartilhada com o Super Gerente.
    Envia o arquivo criptografado para o Super Gerente e registra a data
    do envio e o resultado da comunicação.
    """

    params = {
        #'zip' : '0', # Will return JSON
        'zip' : '1', # Will return zip
        'limit' : '100'}

    logger.debug('Baixando arquivo zip ...')
    zip_path = download_file(config.URL_WSCSERVER, params)

    if zip_path is not None:
        zip_path = os.path.abspath(zip_path)
        logger.debug('Enviando arquivo zip ...')
        upload_file(config.URL_LBBULK, zip_path, config.SOURCE_NAME)
        os.remove(zip_path)

def download_file(url, params):
    """
    Download file from url
    """
    fname = str(uuid.uuid4()) + '.zip'
    local_filename =  config.FILEPATH + '/' + fname
    req = requests.get(url, stream=True, params=params)
    try:
        req.raise_for_status()
    except:
        logger.error("""
            Erro ao tentar baixar arquivo na url %s. Resposta: %s
        """ % (url, req._content))
        return None

    if not os.path.exists(config.FILEPATH):
        os.makedirs(config.FILEPATH)

    with open(local_filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

    return local_filename

def upload_file(url, file_path, source_name):

    params = {'source_name': source_name}
    files = {'file': open(file_path, 'rb')}
    req = requests.post(url, params=params, files=files)

    try:
        req.raise_for_status()
    except:
        logger.error("""
            Erro ao tentar enviar arquivo na url %s. Resposta: %s
        """ % (url, req._content))
        return None

logger = logging.getLogger("WSCBot")
