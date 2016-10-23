# -*- coding: utf-8 -*-
import struct
import json
from time import gmtime, strftime

class Msg(object):
    """Classe para transito de mensagens, responsável
    pela struturação dos pacotes e chamada do log"""
    def __init__(self):
        self.data = {}

    def create(self, _type, _from, _to, _group, _text, _file):

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
        msg_json = json.dumps(
            _msg,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

    	# Inicia cada mensagem com o tamanho (em 4 bytes de comprimento)
        pack = struct.pack('>I', len(msg_json)) + msg_json
        _client.sendall(pack)

    def receive(self,_client):

    	# Le o tamanho da mensagem e faz o 'unpack' em um inteiro
        len_msg_size = self.receive_all(_client, 4)
        if not len_msg_size:
            return None
        len_msg = struct.unpack('>I', len_msg_size)[0]
        # Le os dados da mensagem
        msg = self.receive_all(_client, len_msg)

        return json.loads(msg)

    def receive_all(self,_client, size):

        # método de apoio para receber n bytes or retornar None se o EOF for
        # atingido

        data = ''
        while len(data) < size:
            pack = _client.recv(size - len(data))
            if not pack:
                return None
            data += pack
        return data
