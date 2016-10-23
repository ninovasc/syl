# -*- coding: utf-8 -*-
"""Módulo de contrelo do servidor"""
import socket
import threading
from lib.msg import Msg
from lib.user import User
from lib.log import Log

class Server(object):
    """ok"""
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = int(_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.coms_list = {
            '/quit': "com_quit",
            '/help': "com_help",
            '/msg': "com_msg",
            '/nick': "com_nick"

        }
        self.users_list = []
        self.groups_list = []
        self.last_user_key = 0
        self.log = Log("server-"+_port)

    def listen(self):
        """ok"""
        self.sock.listen(5)
        while True:
            client, addr = self.sock.accept()
            self.last_user_key = self.last_user_key+1
            user = User(
                self.last_user_key,
                client, addr,
                "new_user"+str(self.last_user_key),
                "group")
            self.users_list.append(user)
            print "New Client connected"
            #client.settimeout(60)
            threading.Thread(
                target=self.list_client,
                args=(user, )).start()

    def list_client(self, _user):
        """ok"""
        self.com_msg_of_day(_user)
        while True:
            #try:
            data = Msg().receive(_user.client)
            if data:
                if data["text"][:1] == '/':
                    #print 'entrou if'
                    self.manage_coms(data["text"], _user)
                else:
                    if _user.group == "":
                        msg = {
                            "text" : "It's necessary be into a room to " + \
                            "send a mensage",
                            "type" : "server",
                            "from" : "@server",
                            "to" : _user.nick,
                        }
                        Msg().send(_user.client, msg)
                    else:
                        msg = {
                            "text" : data["text"],
                            "type" : "server",
                            "from" : _user.nick,
                            "to" : "@all",
                        }
                        self.send_to_all(_user, msg)
            else:
                raise error('Client disconnected')

    def send_to_all(self, _user, _msg):
        """ok"""
        self.log.reg(_msg)
        for _, to_user in enumerate(self.users_list):
            if to_user.group == _user.group:
                Msg().send(to_user.client, _msg)

    def com_nick(self, _data, _user):
        """ok"""
        if _data == "description":
            return "/nick <new nick> : Change user nickname"

        new_nick = _data[1]
        old_nick = _user.nick
        setattr(_user, 'nick', new_nick)

        msg = {
            "text" : "Nickname changed, from " + old_nick + " to " + \
            new_nick,
            "type" : "server",
            "from" : "@server",
            "to" : _user.nick,
        }
        self.log.reg(msg)
        Msg().send(_user.client, msg)
        msg = {
            "text" : "User " + old_nick + " is now " + new_nick,
            "type" : "server",
            "from" : "@server",
            "to" : "@all",
        }
        self.send_to_all(_user, msg)

    def com_msg_of_day(self, _user):
        """ok"""
        msg = {
            "text" : "Welcome\n",
            "type" : "server",
            "from" : "@server",
            "to" : _user.nick,
        }
        self.log.reg(msg)
        Msg().send(_user.client, msg)
        self.com_help("", _user)

    def com_quit(self, _data, _user):
        """ok"""
        if _data == "description":
            return "Close client application"
        msg = {
            "text" : "",
            "type" : "quit",
            "from" : "@server",
            "to" : _user.nick,
        }
        Msg().send(_user.client, msg)
        _user.client.close()
        _user = None



    def com_help(self, _data, _user):
        if _data == "description":
            return "/help - Show a list with commands"

        ans = "List of commands:\n"
        for _, method in self.coms_list.items():
            method_call = getattr(self, method, lambda: "com_error")
            ans += method_call("description", _user) + "\n"

        msg = {
            "text" : "\n" + ans,
            "type" : "server",
            "from" : "@server",
            "to" : _user.nick,
        }
        self.log.reg(msg)
        Msg().send(_user.client, msg)
        #return True

    def com_msg(self, _data, _user):
        """verifica o comando recebido para chamar o respectivo método"""
        if _data == "description":
            return "/msg <nick> <mensage> - Send a private mensage to an " + \
            "specific user in same group"

        to_user = next(
            user for user in self.users_list
            if user.nick == _data[1])
        if to_user:
            if to_user.group == _user.group:
                msg = {
                    "text" : " ".join(_data[2:]),
                    "type" : "private",
                    "from" : _user.nick,
                    "to" : to_user.nick,
                }
                Msg().send(to_user.client, msg)
                Msg().send(_user.client, msg)
            else:
                msg = {
                    "text" : "The user " + _data[1] + " is not in the group.",
                    "type" : "server",
                    "from" : "@server",
                    "to" : _user.nick,
                }
                Msg().send(_user.client, msg)
        else:
            msg = {
                "text" : "The user " + _data[1] + "does not exists.",
                "type" : "server",
                "from" : "@server",
                "to" : _user.nick,
            }
            Msg().send(_user.client, msg)


    def com_error(self,_data, _user):
        """executado quando o comando enviado nao esta na coms_list"""
        msg = {
            "text" : "Unknow command, try again.",
            "type" : "server",
            "from" : "@server",
            "to" : _user.nick,
        }
        Msg().send(_user.client, msg)

    def manage_coms(self, _data, _user):
        """verifica o comando recebido para chamar o respectivo método"""
        worked_data = _data.split(' ')
        com = worked_data[0]

        method_name = self.coms_list.get(com, "com_error")

        method_call = getattr(self, method_name, lambda: "com_error")
        return method_call(worked_data, _user)
