#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import logging
import zipfile
import traceback
from wscbot import robot
from wscbot import config
from wscbot.daemon import Daemon
from requests.exceptions import *
from logging.handlers import RotatingFileHandler

config.setup_config()

# Set up log configurations
logger = logging.getLogger("WSCBot")
logger.setLevel(logging.DEBUG)
format_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(format_pattern)
#handler = logging.FileHandler(config.LOGFILE_PATH)
handler = RotatingFileHandler(config.LOGFILE_PATH, 'a', int(20*1024*1024), 10)
handler.setFormatter(formatter)
logger.addHandler(handler)


class WSCBot(Daemon):

    def run(self):
        logger.info('Iniciando modulo WSCBot')
        while True:
            logger.info('Iniciando execução')
            try:
                robot.main()
            except (ConnectionError, Timeout) as e:
                logger.critical('Não foi possivel estabelecer conexão com o servidor! %s', e.request.url)
                time.sleep(config.SLEEP_TIME)
            except Exception as erro:
                logger.critical(traceback.format_exc())
                time.sleep(config.SLEEP_TIME)


if __name__ == "__main__":

    daemon = WSCBot(config.PIDFILE_PATH)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('starting daemon ...')
            #daemon.start()
            daemon.run()
        elif 'stop' == sys.argv[1]:
            print('stopping daemon ...')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print('restarting daemon ...')
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

