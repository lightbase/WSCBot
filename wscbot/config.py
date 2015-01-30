
import tempfile
import configparser


def setup_config():

    global INI_FILE

    INI_FILE = 'production.ini'

    config = configparser.ConfigParser()
    config.read(INI_FILE)

    global URL_WSCSERVER
    global URL_LBBULK
    global URL_SUPER_GERENTE
    global API_KEY

    URL_WSCSERVER = config.get('WSCBot', 'url_wscserver')
    URL_LBBULK = config.get('WSCBot', 'url_lbbulk')
    URL_SUPER_GERENTE = config.get('WSCBot', 'url_super_gerente')
    API_KEY = config.get('WSCBot', 'api_key')

    global FILEPATH
    global SOURCE_NAME
    global SLEEP_TIME
    global PIDFILE_PATH
    global LOGFILE_PATH

    FILEPATH = config.get('WSCBot', 'filepath')
    SOURCE_NAME = config.get('WSCBot', 'source_name')
    SLEEP_TIME = int(config.get('WSCBot', 'sleep_time'))
    PIDFILE_PATH = config.get('Daemon', 'pidfile_path')
    LOGFILE_PATH = config.get('Daemon', 'logfile_path')
