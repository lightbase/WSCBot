# -*- coding: utf-8 -*-

import os
import uuid
import logging
import zipfile
import requests
import json
from wscbot import config
import time

logger = logging.getLogger("WSCBot")


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

    # Tenta conectar à base para pegar configurações
    saida = get_config(config.URL_SUPER_GERENTE, config.SOURCE_NAME, config.API_KEY)
    if saida is None:
        logger.error("Não foi possível baixar as configurações da URL %s para o órgão %s", config.URL_SUPER_GERENTE, config.SOURCE_NAME)
        time.sleep(int(config.SLEEP_TIME) * 3600)
        return
    else:
        if not saida['habilitar_bot']:
            horas = int(saida['coleta']) * 3600
            logger.info("COLETA DESABILITADA!!! Aguardando %d segundos ou %d horas", horas, int(saida['coleta']))
            time.sleep(horas)
            return
        elif saida.get('url') is None:
            logger.error("URL para inseração da coleta não fornecida! Por favor configure a URL")
            horas = int(saida['coleta']) * 3600
            logger.info("Próxima tentativa em %s horas", saida['coleta'])
            time.sleep(horas)
            return

    # Tenta criar a base
    result = create_base(config.URL_SUPER_GERENTE, config.SOURCE_NAME, config.API_KEY)

    logger.debug('Baixando arquivo zip ...')
    zip_path = download_file(config.URL_WSCSERVER, params)

    if zip_path is not None:
        zip_path = os.path.abspath(zip_path)
        logger.debug('Enviando arquivo zip ...')
        upload_file(saida['url'], zip_path, config.SOURCE_NAME)
        os.remove(zip_path)

        # Agora espera o tempo definido
        horas = int(saida['coleta']) * 3600
        logger.info("Aguardando %d segundos ou %d horas", horas, int(saida['coleta']))
        time.sleep(horas)


def download_file(url, params):
    """
    Download file from url
    """
    fname = str(uuid.uuid4()) + '.zip'
    local_filename = config.FILEPATH + '/' + fname
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

def create_base(url, nome_orgao, api_key):
    """
    Cria base no Super Gerente
    :param url: URL do Super Gerente
    :return:
    """
    # URL para criar o órgão
    url += '/api/' + nome_orgao
    logger.debug("criando base para o órgão %s na URL %s", nome_orgao, url)
    params = {
        'api_key': api_key
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        logger.error("Erro na criação da base ou base já existe.\n%s", response.text)
        return False
    else:
        logger.debug("Base criada com sucesso!")
        return True


def get_config(url, nome_orgao, api_key):
    """
    Busca configurações do Bot no módulo Super Gerente
    :param url: URL do Super Gerente
    :return:
    """
    url += '/api/orgaos/' + nome_orgao
    logger.debug("Buscando configurações para o órgão %s na URL %s", nome_orgao, url)
    params = {
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logger.error("Órgão não encontrado.\n%s", response.text)
        return None

    orgao = response.json()

    # TODO: Inserir notificaçõe

    return orgao