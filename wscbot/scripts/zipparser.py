# -*- coding: utf-8 -*-
"""Autor: Breno Rodrigues Brito"""

import zipfile
import logging
import json
import os

from wscbot.scripts.tratamento import t_dados

def ziphandler(filename, tmp_dir):
    """
    Receive a zip file and parse one file at a time, returning a collection of parsed files.
    """
    # Create the zipfile object
    z_root = zipfile.ZipFile(filename)

    # Create a temp dir and unzip file contents

    # registros = {
    #   'import_error' : [],
    #   'registros' : []
    #   }


    # cria um dicionario
    for arquivo in z_root.namelist():
        # This should be a list with a all the zip files
        #print('00000000000000000000000000000 %s' % arquivo)
        z_root.extract(arquivo,tmp_dir)

        # This is the file object for this registro
        # z = zipfile.ZipFile(os.path.join(tmp_dir,arquivo))
        filepath = (os.path.join(tmp_dir,arquivo))

        # Lê o arquivo string que vai conter o json
        with open(filepath) as f:
            string_json = f.read()

        # carrega o Json
        jsonfull = json.loads(string_json)
        jsonfull = t_dados(jsonfull)
        # cria um dicionario
        dicionario = {arquivo:jsonfull}

    return dicionario
        # lista de arquivos

logger = logging.getLogger("WSCBot")
