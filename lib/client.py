# -*- coding: utf-8 -*-
"""Módulo de Cliente"""
import threading
import socket
import sys
import atexit
from lib.msg import Msg
from lib.window import Window


class Client(object):

    def __init__(self, _ip_addr, _port):

        self.ip_addr = _ip_addr
        self.port = _port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip_addr, int(self.port)))
        self.window = Window()
        atexit.register(self.window.close())
        self.window.std.refresh()
        self.msg = Msg("cliente", False)
        self.thread_listen = threading.Thread(target=self.listen_server)
        self.thread_send = threading.Thread(target=self.send_server)
        self.thread_listen.start()
        self.thread_send.start()


    def listen_server(self):

        while True:
            ans = self.msg.receive(self.sock)
            if ans:

                if "group" in ans:
                    if ans["group"] == "":
                        self.window.clear_header()
                        self.window.addstr_header("Connected on host: "+ \
                        self.ip_addr +":"+ self.port + \
                        " U're not in a group")
                    else:
                        self.window.clear_header()
                        self.window.addstr_header("Connected on host: "+ \
                        self.ip_addr +":"+ self.port + \
                        " Group: " + ans["group"])

                if "type" in ans:
                    if ans["type"] == "clear":
                        self.window.clear_data()
                    if ans["type"] == "quit":
                        break

                if ans["from"] == "@server":
                    self.window.addstr_data("*** " + ans["text"]+"\n",
                                            "server")
                elif ans["type"] == "private":
                    self.window.addstr_data("(" + ans["from"] + \
                    ") > " + ans["to"] + " " + ans["text"]+"\n", "private")
                else:
                    self.window.addstr_data(ans["from"] + " > " + \
                    ans["text"]+"\n","text")
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
                    self.msg.send(self.sock, msg) # cliente.envia_msg(envio)
        except KeyboardInterrupt:
            self.sock.close()

def end_client(_client):
    _client.window.close()
    _client = None
    print "Client is now closed. See you later!"
    #sys.exit(0)
    exit()
