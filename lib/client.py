# -*- coding: utf-8 -*-
"""
This module is started by app.py when application is called as client.
"""
import threading
import socket
import atexit
import base64
import ntpath
import sys
from time import gmtime, strftime
from lib.msg import Msg
from lib.window import Window


class Client(object):
    """
    @brief      Class for client application mode.
    """

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
        """
        @brief      method started as thread to read/listen server.

        @param      self  The object

        @return     void method.
        """

        try:
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
                        if ans["type"] == "file":
                            file_time = strftime("%Y%m%d%H%M%S", gmtime())
                            bin_file = base64.b64decode(ans["file"])
                            new_file = open(file_time + ans["file_name"], "wb")
                            new_file.write(bin_file)
                            new_file.close()
                            ans["text"] = "file saved on: " + sys.path[0] + "/" + \
                            file_time + ans["file_name"]


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
                        ans["text"]+"\n", "text")

        finally:
            self.window.addstr_data("*** " + ans["text"]+"\n",
                                    "server")


            self.window.close()
            self.thread_send.join()
            end_client(self)


    def send_server(self):
        """
        @brief      method started as thread to send data to server.

        @param      self  The object

        @return     void method.
        """
        try:
            while True:
                self.window.tex.edit()
                send = self.window.tex.gather().rstrip("\n").strip()
                self.window.prompt.clear()
                self.window.prompt.refresh()

                if send:

                    com_test = send.split(" ")
                    if com_test[0] == "/file":
                        try:
                            bin_file = open(com_test[1], "rb")
                            b64file = base64.b64encode(bin_file.read())
                            bin_file.close()
                            head, tail = ntpath.split(com_test[1])
                            file_name = tail or ntpath.basename(head)
                            msg = {
                                "text" : send,
                                "file" : b64file,
                                "file_name" : file_name,
                                "type" : "file",
                                "from" : "nick",
                                "to":"@server"
                            }
                            self.msg.send(self.sock, msg)
                        except:
                            self.window.addstr_data("ERROR: can't load " + \
                            "file. Please verify.", "error")
                    else:
                        msg = {
                            "text" : send,
                            "type" : "client",
                            "from" : "nick",
                            "to" : "@server",
                        }
                        self.msg.send(self.sock, msg)
        except KeyboardInterrupt:
            self.thread_listen.join()
            end_client(self)
            self.thread_send.join()
            #self.sock.close()

def end_client(_client):
    """
    @brief      Ends a client. Method isn't used.

    @param      _client  The client

    @return     void method.
    """
    _client.window.close()
    _client = None
    print "Client is now closed. See you later!"
    #sys.exit(0)
    exit()
