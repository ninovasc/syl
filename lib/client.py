# -*- coding: utf-8 -*-
"""Módulo de Cliente"""
import threading
import socket
import sys
import atexit
from lib.msg import Msg
from lib.window import Window


class Client(object):

    def __init__(self, _ip, _port):

        self.ip = _ip
        self.port = _port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, int(self.port)))
        self.window = Window()
        atexit.register(self.window.close())
        self.window.std.refresh()
        self.thread_listen = threading.Thread(target=self.listen_server)
        self.thread_send = threading.Thread(target=self.send_server)
        self.thread_listen.start()
        self.thread_send.start()



    def listen_server(self):

        while True:
            ans = Msg().receive(self.sock)
            if ans:
                if ans["from"] == "@server":
                    if ans["type"] == "quit":
                        break
                    else:
                        self.window.data.addstr("*** " + ans["text"]+"\n",)#text.encode('utf_8')
                elif ans["type"] == "private":
                    self.window.data.addstr("(" + ans["from"] + \
                    ") > " + ans["to"] + " " + ans["text"]+"\n")
                else:
                    self.window.data.addstr(ans["from"] + " > " + \
                    ans["text"]+"\n")
                self.window.data.refresh()
        #
        self.thread_send.stop()
        self.thread_listen.stop()
    def send_server(self):

        try:
            while True:
                self.window.tex.edit()
                send = self.window.tex.gather().rstrip("\n").strip()
                self.window.prompt.clear()
                self.window.prompt.refresh()
                if send:
                    msg = {
                        "text" : send,
                        "type" : "client",
                        "from" : "nick",
                        "to" : "@server",
                    }
                    Msg().send(self.sock, msg) # cliente.envia_msg(envio)
        except KeyboardInterrupt:
            self.sock.close()

def end_client(_client):
    _client.window.close()
    _client = None
    print "Client is now closed. See you later!"
    #sys.exit(0)
    exit()
