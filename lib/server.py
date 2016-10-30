# -*- coding: utf-8 -*-
"""
This module is started by app.py when application is called as server.
"""
import socket
import threading
import random
import sys
from lib.files_db import Files_DB
from lib.msg import Msg
from lib.user import User

class Server(object):
    """
    @brief      Class for server application mode.
    """

    def __init__(self, _ip_addr, _port):
        """
        @brief      Constructs the object.

        @param      self      The object
        @param      _ip_addr  The ip address
        @param      _port     The port
        """
        self.ip_addr = _ip_addr
        self.port = int(_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip_addr, self.port))
        Files_DB().create(str(self.port))
        self.coms_list = {
            '/away': "com_away",
            '/ban': "com_ban",
            '/clear':"com_clear",
            '/create':"com_create",
            '/delete': "com_delete",
            '/file': "com_file",
            '/get_file': "com_get_file",
            '/help': "com_help",
            '/join':"com_join",
            '/kick': "com_kick",
            '/leave':"com_leave",
            '/list': "com_list",
            '/list_files': "com_list_files",
            '/msg': "com_msg",
            '/nick': "com_nick"
        }
        self.users_list = []
        self.groups_dict = {}
        self.last_user_key = 0
        self.msg = Msg("server" + _port+ "-", True)
        #self.log = Log("server-"+_port)
        self.trds_dict = {}

    def listen(self):
        """
        @brief      When app.py intances this class this method is called, this
                    method mantain an infinity loop listen socket.

        @param      self  The object

        @return     void method.
        """
        self.sock.listen(5)
        while True:
            try:
                client, addr = self.sock.accept()
                self.last_user_key = self.last_user_key+1
                user = User(
                    self.last_user_key,
                    client, addr,
                    "new_user"+str(self.last_user_key),
                    "")
                self.users_list.append(user)

                print "New Client connected"
                #client.settimeout(60)
                new_trd = threading.Thread(
                    target=self.list_client,
                    args=(user, ))
                self.trds_dict[user.key] = new_trd
                new_trd.start()
            except:
                self.sock.close()
                print "error on server! Server is dead!"
                raise

    def list_client(self, _user):
        """
        @brief      When listen method find new user this method is call as a
                    thread, this method manage the communication with users.

        @param      self   The object
        @param      _user  The user

        @return     void method.
        """
        try:
            self.msg_of_day(_user)
            while True:
                # try:
                data = self.msg.receive(_user.client)
                if data:
                    if data["text"][:1] == '/':
                        #print 'entrou if'
                        self.manage_coms(data, _user)
                    else:
                        if _user.group == "":
                            msg = {
                                "text" : "It's necessary be into a room " + \
                                "to send a mensage",
                                "type" : "server",
                                "from" : "@server",
                                "to" : _user.nick,
                            }
                            self.msg.send(_user.client, msg)
                        else:
                            msg = {
                                "text" : data["text"],
                                "type" : "server",
                                "from" : _user.nick,
                                "to" : "@all",
                            }
                            if user.away:
                                setattr(_user, 'away', False)
                                not_away = {
                                    "text" : user.nick + " is not away " + \
                                    "anymore.",
                                    "type" : "server",
                                    "from" : "@server",
                                    "to" : "@all",
                                }
                                self.send_to_all(_user, not_away)
                            self.send_to_all(_user, msg)
        except:
            #pass
            print "error on user: " + _user.nick + ", user removed " + \
            "from server."
            self.users_list.remove(_user)

    def send_to_all(self, _user, _msg):
        """
        @brief      Sends message to all users in same group as sender.

        @param      self   The object
        @param      _user  The user
        @param      _msg   The message

        @return     void method.
        """
        group_users = [u for u in self.users_list if u.group == _user.group]
        #map(lambda u: self.msg.send(u.client,_msg),group_users)
        #cant use map because an user can be dead
        for _, usr in enumerate(group_users):
            try:
                self.msg.send(usr.client, _msg)
            except:
                print "error on user: " + usr.nick + ", user removed " + \
                "from server."
                self.users_list.remove(usr)

    def server_send(self, _user, _text):
        """
        @brief      Support method to send message as server for one user

        @param      self   The object
        @param      _user  The user
        @param      _text  The text

        @return     void method.
        """
        msg = {
            "text" : _text,
            "type" : "server",
            "from" : "@server",
            "to" : _user.nick
        }
        self.msg.send(_user.client, msg)

    def msg_of_day(self, _user):
        """
        @brief      Send to user a server random initial message from a text
                    file. This call 'com_help' method too.

        @param      self   The object
        @param      _user  The user

        @return     void method.
        """
        text = "syl - version 1.0\n"
        text += "Today is a very good day to "
        motd = open("lib/motd.txt", 'r')
        lines = motd.readlines()
        motd.close()
        rnd = lines[int(random.uniform(0, len(lines)))].replace('\n', '')
        msg = {
            "group": "",
            "text" : text + rnd,
            "type" : "server",
            "from" : "@server",
            "to" : _user.nick
        }

        self.msg.send(_user.client, msg)
        #self.server_send(_user, "send '/help' to see a list of commands.")
        self.com_help("", _user)

    def manage_coms(self, _data, _user):
        """
        @brief      works like a switch case for commands in server. Verify
                    wich function user want and call right method 'com_*' to
                    manage this.

        @param      self   The object
        @param      _data  The data
        @param      _user  The user

        @return     { description_of_the_return_value }
        """
        text_split = _data["text"].split(' ')
        com = text_split[0]

        method_name = self.coms_list.get(com, "com_error")

        method_call = getattr(self, method_name, lambda: "com_error")
        return method_call(text_split, _user, _data)

    def com_error(self,_data, _user, _full_msg={}):
        """
        @brief      in case of users call a nonexistent function this method
                    returns a message informing user.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        self.server_send(_user, "Unknow command, try again. If you need: " + \
        "/help")

    def com_away(self, _data, _user, _full_msg={}):
        """
        @brief      set user status to away, in this status user can't receive
                    private messages.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/away : set your status to afk and not receive "+ \
            "private mensages."

        try:
            if _user.away:
                msg = {
                    "text" : "You already away. Send a mensage to return.",
                    "type" : "server",
                    "from" : "@server",
                    "to" : _user.nick
                }
                self.msg.send(_user.client, msg)
                return

            if _user.group == "":
                msg = {
                    "text" : "You must be in a group to be away.",
                    "type" : "server",
                    "from" : "@server",
                    "to" : _user.nick
                }
                self.msg.send(_user.client, msg)
                return

            setattr(_user, 'away', True)
            msg = {
                "text" : "User " + _user.nick + " is now away from keyboard.",
                "type" : "server",
                "from" : "@server",
                "to" : _user.nick
            }
            self.send_to_all(_user, msg)
        except:

            print "Unexpected error on /away:", sys.exc_info()[0]
            self.server_send(_user, "Error on /away. Try again. If you " + \
            "need: /help")

    def com_ban(self, _data, _user, _full_msg={}):
        """
        @brief      This method banish a user from a group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/ban <nick> : Banish user from group. Only for " + \
            "group admin."

        try:

            if _user.group == "":
                self.server_send(_user, "You must in a group and be "+ \
                "admin of group to banish anyone.")
                return

            if _user.key != self.groups_dict[_user.group]["admin"].key:
                self.server_send(_user, "You must be admin of group " + \
                "to banish anyone.")
                return

            nick_to_ban = _data[1]

            user_to_ban = next(
                user for user in self.users_list
                if user.nick == nick_to_ban)

            if not user_to_ban:
                self.server_send(_user, nick_to_ban + " does not exists.")
                return

            if user_to_ban.group != _user.group:
                self.server_send(_user, nick_to_ban + " isn't in this group")
                return

            if user_to_ban.key == _user.key:
                self.server_send(_user, "You can't bannish yourself!")
                return

            if "ban" not in self.groups_dict[_user.group]:
                self.groups_dict[_user.group]["ban"] = []

            self.groups_dict[_user.group]["ban"].append(user_to_ban)

            msg = {
                "text" : _user.nick + " has banished " + user_to_ban.nick + \
                " from group " + _user.group,
                "type" : "server",
                "from" : "@server",
                "to" : "@all"
            }
            self.send_to_all(_user, msg)

            self.server_send(user_to_ban, "You has been banished from " + \
            "group" + _user.group)
            leave = {"text": "/leave"}
            self.manage_coms(leave, user_to_ban)
            return

        except:

            print "Unexpected error on /ban:", sys.exc_info()[0]
            self.server_send(_user, "Error on /ban. Try again. If you " + \
            "need: /help")

    def com_clear(self,_data,_user, _full_msg={}):
        """
        @brief      clear client window, this could be implemented only on
                    clien side but to store a log this is managed by server.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        try:

            if _data == "description":
                return "/clear : clear mensage screen"

            msg = {
                "text" : "",
                "type" : "clear",
                "from" : "@server",
                "to" : _user.nick
            }
            self.msg.send(_user.client, msg)

        except:

            print "Unexpected error on /clear:", sys.exc_info()[0]
            self.server_send(_user, "Error on /clear. Try again. If you " + \
            "need: /help")

    def com_create(self, _data, _user, _full_msg={}):
        """
        @brief      create a group

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/create <group name> : create a chat group"

        try:

            new_group_name = _data[1]

            if (" " in new_group_name) or len(new_group_name) > 50:
                msg = {
                    "text" : "Group name must contains less than 50 " + \
                    "caracters and must not contains spaces",
                    "type" : "server",
                    "from" : "@server",
                    "to" : _user.nick,
                }
                self.msg.send(_user.client, msg)
                return

            if new_group_name in self.groups_dict:
                msg = {
                    "text" : "Group " + new_group_name + " already " + \
                    "exists. Try another name.",
                    "type" : "server",
                    "from" : "@server",
                    "to" : _user.nick,
                }
                self.msg.send(_user.client, msg)
                return

            self.groups_dict[new_group_name] = {"admin": _user}

            msg = {
                "text" : "Group " + new_group_name + " was created ",
                "type" : "server",
                "from" : "@server",
                "to" : _user.nick,
            }
            self.msg.send(_user.client, msg)
            #join = {"text" : "/join " + new_group_name}
            #self.manage_coms(join, _user)

        except:

            print "Unexpected error on /create:", sys.exc_info()[0]
            self.server_send(_user, "Error on /create. Try again. If you " + \
            "need: /help")

    def com_delete(self, _data, _user, _full_msg={}):
        """
        @brief      Delete group from server.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/delete <group name> : Delete a group. Only for group "+ \
            "admin."

        try:

            group_to_delete = _data[1]

            if group_to_delete not in self.groups_dict:
                self.server_send(_user, "Group "+  group_to_delete + \
                    " dont exist in this server.")
                return

            if _user.key != self.groups_dict[group_to_delete]["admin"].key:
                self.server_send(_user, "You must be admin of "+ \
                group_to_delete + " to delete the group.")
                return

            group_users = [u for u in self.users_list
                           if u.group == group_to_delete]
            if group_users != []:
                self.server_send(_user, group_to_delete + " must be " + \
                "empty before delete.")
                return

            del self.groups_dict[group_to_delete]
            Files_DB().delete_files_by_group(
                group_to_delete,
                str(self.port)
            )
            self.server_send(_user, group_to_delete + " was deleted")

        except:

            print "Unexpected error on /delete:", sys.exc_info()[0]
            self.server_send(_user, "Error on /delete. Try again. If you " + \
            "need: /help")

    def com_file(self, _data, _user, _full_msg):
        """
        @brief      receives a file send by user and store in database

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/file <path to file> : Send a file to group"

        try:

            if _user.group == "":
                self.server_send(_user, "You need to be in a group to " + \
                "send files.")
                return

            file_names = Files_DB().file_names_by_group(
                _user.group,
                str(self.port))

            if any(d['FILE_NAME'] == _full_msg["file_name"]
                   for d in file_names):
                self.server_send(_user, "File: " + _full_msg["file_name"] + \
                " already exist in this group.")
                return

            Files_DB().insert_file(
                _user.group,
                _full_msg["file_name"],
                _full_msg["file"],
                str(self.port)
            )
            msg = {
                "text" : _user.nick + " has send a file! File name is: " + \
                _full_msg["file_name"],
                "type" : "server",
                "from" : "@server",
                "to" : "@all"
            }
            self.send_to_all(_user, msg)

        except:

            print "Unexpected error on /file:", sys.exc_info()[0]
            self.server_send(_user, "Error on /file. Try again. " + \
            "If you need: /help")

    def com_get_file(self,_data, _user, _full_msg={}):
        """
        @brief      get a file stored in user group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/get_file <file name> : get a file of group"

        try:

            if _user.group == "":
                self.server_send(_user, "You must be in a group to get files")
                return
            file_name = _data[1]

            b64file = Files_DB().file_by_name_group(
                file_name,
                _user.group,
                str(self.port)
            )

            if not b64file:
                self.server_send(_user, "Fail to get file, check file name.")
                return

            msg = {
                "file": b64file,
                "file_name": file_name,
                "type": "file",
                "from": "@server",
                "to": _user.nick
            }
            self.msg.send(_user.client, msg)
        except:
            print "Unexpected error on /get_file:", sys.exc_info()[0]
            self.server_send(_user, "Error on /get_file. Try again. " + \
            "If you need: /help")

    def com_help(self, _data, _user, _full_msg={}):
        """
        @brief      send a list of commands and description to user. Every
                    method in 'coms_list' if receives 'description' as '_data'
                    returns a string with command description.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/help : Show a list with commands"

        try:

            ans = "List of commands:\n"
            for key in sorted(self.coms_list):
                method_call = getattr(
                    self,
                    self.coms_list[key],
                    lambda: "com_error"
                )
                ans += method_call("description", _user, "") + "\n"

            self.server_send(_user, ans)

        except:

            print "Unexpected error on /help (how???):", sys.exc_info()[0]
            self.server_send(_user, "Error on /help. Try again. If you " + \
            "need help sorry :(")

    def com_join(self, _data, _user, _full_msg={}):
        """
        @brief      join a group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/join <group name> : join a chat group"

        try:

            group = _data[1]

            if group not in self.groups_dict:
                self.server_send(_user, "Group " + group + " don't exist. " + \
                "Try again")
                return

            if _user.group != "":
                self.server_send(_user, "Before join to " + group + " you " +\
                "need leave " + _user.group)
                return

            if "ban" in self.groups_dict[group]:
                for usr in self.groups_dict[group]["ban"]:
                    if usr.key == _user.key:
                        self.server_send(_user, "You are banned from group " + \
                        group + ". You cannot join this group anymore.")
                        return

            setattr(_user, 'group', group)
            msg = {
                "group": group,
                "text" : "Your are now on group: " + group,
                "type" : "server",
                "from" : "@server",
                "to" : _user.nick
            }
            self.msg.send(_user.client, msg)
        except:

            print "Unexpected error on /join:", sys.exc_info()[0]
            self.server_send(_user, "Error on /join. Try again. If you " + \
            "need: /help")

    def com_kick(self, _data, _user, _full_msg={}):
        """
        @brief      kick user from group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/kick <nick> : Kick user from group. Only for group admin."

        try:

            if _user.group == "":
                self.server_send(_user, "You must in a group and be "+ \
                "admin of group to kick anyone.")
                return

            if _user.key != self.groups_dict[_user.group]["admin"].key:
                self.server_send(_user, "You must be admin of group " + \
                "to kick anyone.")
                return

            nick_to_kick = _data[1]

            user_to_kick = next(
                user for user in self.users_list
                if user.nick == nick_to_kick)

            if not user_to_kick:
                self.server_send(_user, nick_to_kick + " does not exists.")
                return

            if user_to_kick.group != _user.group:
                self.server_send(_user, nick_to_kick + " isn't in this group")
                return

            msg = {
                "text" : _user.nick + " has kicked " + user_to_kick.nick + \
                " from group " + _user.group,
                "type" : "server",
                "from" : "@server",
                "to" : "@all"
            }
            self.send_to_all(_user, msg)
            self.server_send(user_to_kick, "You has been kicked from " + \
            "group" + _user.group)
            leave = {"text": "/leave"}
            self.manage_coms(leave, user_to_kick)
            return

        except:

            print "Unexpected error on /kick:", sys.exc_info()[0]
            self.server_send(_user, "Error on /kick. Try again. If you " + \
            "need: /help")

    def com_leave(self,_data,_user, _full_msg={}):
        """
        @brief      leave a group or a chat if user not in a group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/leave <group name> : leave a chat group or quit chat " + \
            "when not in a group"

        try:

            if _user.group == "":

                msg = {
                    "text" : "bye!",
                    "type" : "quit",
                    "from" : "@server",
                    "to" : _user.nick
                }
                self.msg.send(_user.client, msg)
                trd = self.trds_dict[_user.key]

                del self.trds_dict[_user.key]
                self.users_list.remove(_user)
                print "Thread of user " + _user.nick + " has ended. " + \
                "User was removed from list"
                trd.join()

            else:

                old_group = _user.group
                msg = {
                    "group" : "",
                    "text" : "You leave " + old_group + " group",
                    "type" : "server",
                    "from" : "@server",
                    "to" : _user.nick
                }
                setattr(_user, 'away', False)
                setattr(_user, 'group', "")
                self.msg.send(_user.client, msg)
        except:

            print "Unexpected error on /leave:", sys.exc_info()[0]
            self.server_send(_user, "Error on /leave. Try again. If you " + \
            "need: /help")

    def com_list(self, _data, _user, _full_msg={}):
        """
        @brief      list server groups if user isn't in a group or list users
                    of user group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/list : When in a group show a list of users, " + \
            "when not show a list of groups."

        try:

            if not self.groups_dict:
                self.server_send(_user, "There are no groups in this " + \
                "server :(")
                return

            text = ""

            if _user.group == "":
                text += "List of groups in this server:\n"
                for key, _ in self.groups_dict.items():
                    text += key+"\n"
            else:
                group_users = [u for u in self.users_list
                               if u.group == _user.group]
                text += "List of users in: " + _user.group + "\n"
                for _, usr in enumerate(group_users):
                    text += usr.nick + "\n"

            self.server_send(_user, text)

        except:

            print "Unexpected error on /list:", sys.exc_info()[0]
            self.server_send(_user, "Error on /list. Try again. " + \
            "If you need: /help")

    def com_list_files(self,_data, _user, _full_msg={}):
        """
        @brief      Lists files stored on user group.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """

        if _data == "description":
            return "/list_files : List files in the group"

        try:

            if _user.group == "":
                self.server_send(_user, "You must be in a group to list files")
                return

            text = "List of files in " + _user.group + ":\n"
            file_names = Files_DB().file_names_by_group(
                _user.group,
                str(self.port))
            #print file_names

            for _, file_name in enumerate(d['FILE_NAME'] for d in file_names):
                text += file_name + "\n"

            self.server_send(_user, text)
        except:
            print "Unexpected error on /list_files:", sys.exc_info()[0]
            self.server_send(_user, "Error on /list_files. Try again. " + \
            "If you need: /help")

    def com_msg(self, _data, _user, _full_msg={}):
        """
        @brief      send a private message from one user to another.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/msg <nick> <mensage> : Send a private mensage to an " + \
            "user in same group"

        try:

            to_user = next(
                user for user in self.users_list
                if user.nick == _data[1])

            if not to_user:
                self.server_send(_user, "The user " + _data[1] + "does " + \
                "not exists.")
                return

            if to_user.group != _user.group:
                self.server_send(_user, "The user " + _data[1] + \
                " is not in the group.")
                return

            if to_user.away:
                self.server_send(_user, to_user.nick + " is away from " + \
                "keyboard and cannot receive private mensage.")
                return

            msg = {
                "text" : " ".join(_data[2:]),
                "type" : "private",
                "from" : _user.nick,
                "to" : to_user.nick,
            }
            self.msg.send(to_user.client, msg)
            self.msg.send(_user.client, msg)

        except:

            print "Unexpected error /msg:", sys.exc_info()[0]
            self.server_send(_user, "Error on /nick. Try again. If you " + \
            "need: /help")

    def com_nick(self, _data, _user, _full_msg={}):
        """
        @brief      changes user nickname.

        @param      self       The object
        @param      _data      The data
        @param      _user      The user
        @param      _full_msg  The full message

        @return     void method.
        """
        if _data == "description":
            return "/nick <new nick> : Change user nickname"

        try:

            new_nick = _data[1]
            old_nick = _user.nick

            if (" " in new_nick) or len(new_nick) > 50:

                self.server_send(_user, "Nickname must contains less " + \
                    "than 50 caracters and must not contains spaces")
                return

            new_nick_used = [u for u in self.users_list if u.nick == new_nick]

            if new_nick_used != []:
                self.server_send(_user, "You can't change your nickname " + \
                " to " + new_nick + " because this already is used.")
                return

            setattr(_user, 'nick', new_nick)

            self.server_send(_user, "Nickname changed, from " + old_nick + \
                " to " + new_nick)

            msg = {
                "text" : "User " + old_nick + " is now " + new_nick,
                "type" : "server",
                "from" : "@server",
                "to" : "@all",
            }
            self.send_to_all(_user, msg)

        except:

            print "Unexpected error /nick:", sys.exc_info()[0]
            self.server_send(_user, "Error on /nick. Try again. If you " + \
            "need: /help")
