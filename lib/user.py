class User(object):

    def __init__(self, _key, _client, _addr, _nick, _group):

        self.key = _key
        self.client = _client
        self.addr = _addr
        self.nick = _nick
        self.group = _group
        self.away = False

    def json(self):
        json.dumps(self.__dict__)

