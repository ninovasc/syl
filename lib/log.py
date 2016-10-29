# -*- coding: utf-8 -*-
"""
Log module
"""
from time import gmtime, strftime
import json

class Log(object):
    """
    @brief      Class for log.
    """

    def __init__(self, _type):
        """
        @brief      Constructs the object. Receive _type to use in file name.

        @param      self   The object
        @param      _type  The type
        """
        self.type = _type
        self.time = strftime("%Y%m%d%H%M%S", gmtime())
        log_file = open(self.type+self.time + ".log", 'w')
        log_file.write("Log\n")
        log_file.close()

    def reg(self, _reg):
        """
        @brief      Method to register each entry of log.

        @param      self  The object
        @param      _reg  The register

        @return     This is a void method, only writes a entry in log file.
        """
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
