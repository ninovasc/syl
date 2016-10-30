# -*- coding: utf-8 -*-
"""
The server and client uses this module to send and receive mensages.
"""
import struct
import json
from time import gmtime, strftime
from lib.log import Log


class Msg(object):
    """
    @brief      Class for transit of messages. This class structs each
                message in packs and make log call.
    """

    def __init__(self, _type, _log):
        """
        @brief      Constructs the object.

        @param      self   The object
        @param      _type  The type
        @param      _log   The log
        """
        if _log:
            self.log = Log(_type)
        else:
            self.log = None
        self.data = {}

    def create(self, _type, _from, _to, _group, _text, _file):
        """
        @brief      Un used method, can be used to create message with
                    time attribute.

        @param      self    The object
        @param      _type   The type
        @param      _from   The from
        @param      _to     The to (message receiver)
        @param      _group  The group
        @param      _text   The text
        @param      _file   The file

        @return     changes self.data dictionary of class.
        """

        self.data = {
            "time": strftime("%Y%m%d%H%M%S", gmtime()),
            "type": _type,
            "from": _from,
            "to": _to,
            "group": _group,
            "text": _text,
            "file": _file
        }


    def send(self,_client, _msg):
        """
        @brief      This method receives a message and a socket. Structs this
                    message with a 4 bytes in benning, this bytes contains the
                    size of message.

        @param      self     The object
        @param      _client  The client (socket)
        @param      _msg     The message

        @return     void method, only sends a message.
        """
        if self.log != None:
            self.log.reg(_msg)
        msg_json = json.dumps(
            _msg,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

        pack = struct.pack('>I', len(msg_json)) + msg_json
        _client.sendall(pack)

    def receive(self,_client):
        """
        @brief      This method receives a socket. Read 4 first bytes
                    with size of message. After that receive the real message.

        @param      self     The object
        @param      _client  The client (socket)

        @return     return a dictionary with message attributes
        """

        len_msg_size = self.receive_all(_client, 4)
        if not len_msg_size:
            return None
        len_msg = struct.unpack('>I', len_msg_size)[0]
        # Le os dados da mensagem
        msg = self.receive_all(_client, len_msg)
        dict_msg = json.loads(msg)

        if self.log != None:
            self.log.reg(dict_msg)

        return dict_msg

    def receive_all(self,_client, _size):
        """
        @brief      Support method for 'receive' method, works receiving
                    from socket a message by size.

        @param      self     The object
        @param      _client  The client (socket)
        @param      _size     The size

        @return     return received data.
        """
        data = ''
        while len(data) < size:
            pack = _client.recv(_size - len(data))
            if not pack:
                return None
            data += pack
        return data
