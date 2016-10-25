# -*- coding: utf-8 -*-
"""modulo de criação de log"""
from time import gmtime, strftime
import json

class Log(object):
    """classe de log"""

    def __init__(self, _type):
        """método de inicialização que recebe _tipo para ser utlizado como
        parte do nome do arquivo de log"""
        self.type = _type
        self.time = strftime("%Y%m%d%H%M%S", gmtime())
        log_file = open(self.type+self.time + ".log", 'w')
        log_file.write("Log\n")
        log_file.close()

    def reg(self, _reg):
        """modulo de registro de cada entrada do log"""
        reg_time = strftime("%Y%m%d%H%M%S", gmtime())
        log_file = open(self.type+self.time + ".log", 'a')
        _reg["time"] = reg_time
        log_file.write(json.dumps(
            _reg,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )+"\n")
        log_file.close()
