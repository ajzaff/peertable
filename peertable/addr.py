import peertable.bytekey
import socket


class Address(object):
    def __init__(self, port, key=None, host=None):
        if host is None:
            host = 'localhost'
        if key is None:
            key = peertable.bytekey.ByteKey()
        self._host = socket.gethostbyname(host)
        self._port = port
        self._key = key

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '%s@%s:%s' % (self.key, self.host, self.port)

    def __lt__(self, other):
        return self.key < other.key

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def key(self):
        return self._key