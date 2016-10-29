# -*- coding: utf-8 -*-
"""
Create to organize users information and apart this from server module.
"""
class User(object):
    """
    Classe to store information of server users
    """

    def __init__(self, _key, _client, _addr, _nick, _group):
        """
        @brief      Constructs the object.

        @param      self     The object
        @param      _key     The key
        @param      _client  The client
        @param      _addr    The address
        @param      _nick    The nick
        @param      _group   The group

        @return     return a instance of User class
        """

        self.key = _key
        self.client = _client
        self.addr = _addr
        self.nick = _nick
        self.group = _group
        self.away = False


