# -*- coding: utf-8 -*-
"""modulo principal para chamar a aplicação em modo cliente ou servidor"""
import sys
from lib.server import Server
from lib.client import Client

def server(_port):
    """função para iniciar no modo servidor"""
    print "Application inicialized as server"
    Server('', _port).listen()

def client(_ip, _port):
    """função para iniciar no modo cliente"""
    print "Application inicialized as client"
    Client(_ip, _port)

if __name__ == "__main__":

    ERROR_MSG = "Is necessary use arguments to inicialize this application\n"
    "{server port|client ip port}"
    if len(sys.argv) == 1:
        print ERROR_MSG
    elif sys.argv[1] == "server":
        server(sys.argv[2])
    elif sys.argv[1] == "client":
        client(sys.argv[2], sys.argv[3])
    else:
        print ERROR_MSG


