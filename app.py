# -*- coding: utf-8 -*-
"""
Application main module, can call app in client or server mode.
From command line call 'python app.py client {ip} {port}' to start as
client or call 'python app.py server {port}' to start as server.
"""
import sys
from lib.server import Server
from lib.client import Client

def server(_port):
    """
    @brief      Starts app as server

    @param      _port  The port

    @return     return one server
    """
    print "Application inicialized as server"
    try:
        Server('', _port).listen()
    except:
        raise
def client(_ip, _port):
    """
    @brief      Starts app as client

    @param      _port  The port

    @return     return one client
    """
    print "Application inicialized as client"
    try:
        Client(_ip, _port)
    except:
        pass

if __name__ == "__main__":
    """
    Mains function of module.
    """
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


