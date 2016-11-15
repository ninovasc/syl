 [![syl](https://github.com/ninovasc/syl/blob/master/readme_img/syl_logo.gif?raw=true)](https://github.com/ninovasc/syl/)

# syl - see you later

syl is a chat application made in python with in client-server approach.

The objective is a fully functional chat application like IRC protocol. The motivation to program all this is a class work for Network discipline in my graduation.

#### Run syl

To run this application you must use python 2.7 in a linux or OS X system (curses library is used on this project and don't have support to Windows). I developed in a ubuntu.

First you must start a server, to do this run this command:

```sh
python server 12000
```

* 12000 is the server port, you can used another if you want.

After start a server you can connect the clientes following this line:

```sh
python client 127.0.0.1 12000
```
* Again, 12000 is the server port, if you change this port on server start you must change this here too.
* 127.0.0.1 is you local IP, if server is remote you need to know de remote IP.

NOW YOU ARE READY TO CHAT!

Follow the screen instructions to create your group and start talk.

## Internet Relay Chat (IRC)
-------------------------------

The IRC protocol was an inspiration to this project. IRC is a application layr protocol that facilitates communucation in the form of text. The chat process works on a client/server network model (like syl). Like IRC, syl provides private messages, chat and data transfer, including file sharing.

#### Some IRCstory

IRC was created by Jarkko Oikarinen in August 1988. Jarkko intended to extend the BBS software he administered, to allow news in the Usenet style, real time discussions and similar BBS features. The first part he implemented was the chat part, which he did with borrowed parts written by his friends Jyrki Kuoppala and Jukka Pihl. The first IRC network was running on a single server named tolsun.oulu.fi. Oikarinen found inspiration in a chat system known as Bitnet Relay, which operated on the BITNET.

After some issues trhough the time only in May 1993, RFC 1459 was published and details a simple protocol for client/server operation, channels, one-to-one and one-to-many conversations. It is notable that the a significant number of extensions like CTCP, colors and formats are not included in the protocol specifications, nor is character encoding, which led various implementations of servers and clients to diverge. In fact, software implementation varied significantly from one network to the other, each network implementing their own policies and standards in their own code bases.

## Transmission Control Protocol (TCP)
-------------------------------

Syl uses a TCP sockets to comunication between server and client.

When the server is started a socket start to listen on server port and for each client who connects in the server a thread is started to bound the communication.

TCP is one of the main protocols of the Internet protocol suite. It originated in the initial network implementation in which it complemented the Internet Protocol (IP). Therefore, the entire suite is commonly referred to as TCP/IP.

TCP provides reliable, ordered, and error-checked delivery of a stream of octets between applications running on hosts communicating by an IP network. Major Internet applications such as the World Wide Web, email, remote administration, and file transfer rely on TCP.

## syl structure
-------------------------------

To implement syl was used some modules listed bellow:

**app.py**

Application main interface module, can call app in client or server mode.
From command line.

**lib/client.py**

This is syl client, this module controls conection request to server and the user interface with curses, after client is connected to the server two threads are started, one to receive server messagens and another to send mesage to server.

**lib/server.py**

Server is the heart of syl. All functions are implemented in this module. Here all server flow is implemented.

**lib/msg.py**

This module manage the messages in syl. All message transfers in converted in a JSON by this module, even files.

**lib/files_db.py**

Manages a SQLite database created in server start (if already exist the database are overwrite). This data base store the files send by users.

**lib/window.py**

This is only curses library control for client, all client window is draw by this module.

**lib/user.py**

Only an objetc structure to server manage user attributes.

## syl application in use

Commands:

* /nick <new nick>
 [![syl](https://github.com/ninovasc/syl/blob/master/readme_img/nick.png?raw=true)](https://github.com/ninovasc/syl/)
