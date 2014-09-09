#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import time
import os
import ConfigParser

from daemon import runner


from app import main

#exceptions
from requests.exceptions import *
import zipfile
import lockfile
import tempfile

# absolute path to .ini file
#ini_path='/srv/super-gerente/WSCBot/development.ini'
ini_path='/srv/bot-super-gerente/WSCBot/production.ini'



def setconfig(config_file):
    """Função que conecta o modulo ao arquivo de configurações"""

    config_file = os.path.abspath(config_file)
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    user = {}
    user['url_wscserver'] = config.get('WSCBot', 'url_wscserver')
    user['filepath'] = config.get('WSCBot', 'filepath')
    if config.has_option('WSCBot', 'tmp_dir'):
        user['tmp_dir'] = config.get('WSCBot', 'tmp_dir')
    else:
        user['tmp_dir'] = tempfile.mkdtemp()
    user['username'] = config.get('WSCBot', 'username')
    user['senha'] = config.get('WSCBot', 'senha')
    user['data'] = config.get('WSCBot', 'data')
    user['ip_superg'] = config.get('WSCBot', 'ip_superg')
    user['source_name'] = config.get('WSCBot', 'source_name')
    user['sleep_time'] = int(config.get('WSCBot', 'sleep_time'))
    user['stdin_path'] = config.get('Daemon', 'stdin_path')
    user['stdout_path'] = config.get('Daemon', 'stdout_path')
    user['stderr_path'] = config.get('Daemon', 'stderr_path')
    user['pidfile_path'] = config.get('Daemon', 'pidfile_path')
    user['logfile_path'] = config.get('Daemon', 'logfile_path')
    user['pidfile_timeout'] = int(config.get('Daemon', 'pidfile_timeout'))
    return user

class App():

    def __init__(self):
        self.stdin_path = user['stdin_path']
        self.stdout_path = user['stdout_path']
        self.stderr_path = user['stderr_path']
        self.pidfile_path =  user['pidfile_path']
        self.pidfile_timeout = user['pidfile_timeout']

    def run(self):
        logger.info ('Iniciando modulo WSCBot')
        while True:
            timeron = time.time()
            logger.info ('Iniciando execução')
            try:
                main(ip_servidor,username,senha,ip_superg,filepath,data,tmp_dir,source_name)
            except (ConnectionError, Timeout):
                logger.error ('Não foi possivel estabelecer conexão com o servidor! ' + domain)
            except zipfile.BadZipfile:
                logger.error ('Arquivo zip gerado pelo WSCServer invalido ou corrompido')
            except Exception as erro:
                logger.error (erro)
            timeronff = time.time()
            tempo = (timeronff - timeron)
            m, s = divmod(sleep_time, 60)
            h, m = divmod(m, 60)
            next = "%d:%02d:%02d" % (h, m, s)
            logger.debug ('Execução durou ' + str(tempo) + ' segundos.')
            logger.info ('Proxima execução em: ' + next)
            time.sleep(sleep_time)

user = setconfig(ini_path)
ip_servidor = user['url_wscserver']
senha = user['senha']
ip_superg = user['ip_superg']
sleep_time = user['sleep_time']
source_name = user['source_name']
username = user['username']
filepath = user['filepath']
tmp_dir = user['tmp_dir']
data = user['data']
app = App()
logger = logging.getLogger("WSCBot")
logger.setLevel(logging.INFO) # Alterar para logging.INFO em produção
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(user['logfile_path'])
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
try:
    daemon_runner.do_action()
except (KeyboardInterrupt, SystemExit):
    raise
except lockfile.LockTimeout:
    print("\nErro: Já existe uma instância desse modulo em execução\n")
except runner.DaemonRunnerStopFailureError:
    print("\nErro: Não existe nenhuma instância desse módulo em execução\n")
