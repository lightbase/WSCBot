# -*- coding: utf-8 -*-
"""Autor: Breno Rodrigues Brito"""
import logging
import simplejson # for exception

def is_error_p(resp):
    """verifica erros do post"""
    try:
        json = resp.json()
    except simplejson.decoder.JSONDecodeError:
        msg = 'not found'
        n_err = str(resp.status_code)
        logger.error(n_err + ': ' + msg)
    else:
        try:
            a = len(json)
        except TypeError:
            id_reg = str(json)
            logger.info('Escrito com sucesso id_reg: ' + id_reg)
        else:
            msg = json['_error_message']
            n_err = str(json['_status'])
            logger.error(n_err + ': ' + msg)


def is_error_g(recebe):
    """Verifica erros do GET"""

    num_er = recebe.__dict__['status_code']
    msg = recebe.__dict__['reason']

    if num_er > 199 and num_er < 300:
        logger.debug('Recebido com sucesso.')
    else:
        logger.error(str(num_err) + ': ' + msg)


logger = logging.getLogger("WSCBot")