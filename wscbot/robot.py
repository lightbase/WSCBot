# -*- coding: utf-8 -*-

import os
import uuid
import logging
import zipfile
import requests
from wscbot import config
import time


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
        # Primeiro tenta criar a base
        result = create_base(config.URL_SUPER_GERENTE, config.SOURCE_NAME)

        # Tenta conectar à base para pegar configurações
        saida = get_config(config.URL_SUPER_GERENTE, config.SOURCE_NAME)
        if saida is None:
            logger.error("Não foi possível baixar as configurações da URL %s para o órgão %s", config.URL_SUPER_GERENTE, config.SOURCE_NAME)
            return

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

logger = logging.getLogger("WSCBot")


def create_base(url, nome_orgao):
    """
    Cria base no Super Gerente
    :param url: URL do Super Gerente
    :return:
    """
    # URL para criar o órgão
    url += '/create/coleta/' + nome_orgao
    logger.debug("criando base para o órgão %s na URL %s", nome_orgao, url)
    response = requests.post(url)
    if response.status_code != '200':
        logger.error("Erro na criação da base ou base já existe.\n%s", response.text)
        return False
    else:
        logger.debug("Base criada com sucesso!")
        return True


def get_config(url, nome_orgao):
    """
    Busca configurações do Bot no módulo Super Gerente
    :param url: URL do Super Gerente
    :return:
    """
    url += '/api/orgaos/' + nome_orgao
    logger.debug("Buscando configurações para o órgão %s na URL %s", nome_orgao, url)
    response = requests.get(url)
    if response.status_code != '200':
        logger.error("Órgão não encontrado.\n%s", response.text)
        return None

    orgao = response.json()
    url_bulk = orgao['results'][0]['url']
    coleta = orgao['results'][0]['coleta']
    habilitar_bot = orgao['results'][0]['habilitar_bot']

    # TODO: Inserir notificações
    saida = {
        'url': url_bulk,
        'coleta': coleta,
        'habilitar_bot': habilitar_bot
    }

    return saida