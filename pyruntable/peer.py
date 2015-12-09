from pyruntable import routes
from threading import Thread
import socket
import random
import time


class Peer(Thread):
    def __init__(self, port, key=None, host=None):
        Thread.__init__(self)
        self._addr = Address(port, key=key, host=host)
        self._routes = routes.Table(address=self.address,
                                    buckets=self.key.buckets)

    def run(self):
        sock = socket.socket()
        sock.bind(self._addr)
        sock.listen(5)
        self.log("started listening on %s..." % self._addr)
        while True:
            client, addr = sock.accept()
            self.log("accepted connection from %s:%s..." %
                     tuple(addr))
            self.log("received data %s" %
                     client.recv(1024))
            client.close()
        self.log("shutting down...")

    @property
    def address(self):
        return self._addr

    @property
    def key(self):
        return self.address.key

    @classmethod
    def time(cls):
        return time.time()

    def log(self, message):
        ptime = time.ctime(Peer.time())
        print("[%s] Peer %s %s" % (ptime, self.address.key, message))


class Address(object):
    def __init__(self, port, key=None, host=None):
        if host is None:
            host = 'localhost'
        if key is None:
            key = Key()
        self._key = key
        self._host = socket.gethostbyname(host)
        self._port = port

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


class Key(bytearray):

    N = 20

    def __init__(self, value=None, buckets=N, prefix=None, rand=random):
        if buckets <= 0:
            raise ValueError('buckets must be > 0: found %d' % buckets)
        if value is None:
            super(Key, self).__init__(buckets)
            for i in range(buckets):
                bits = rand.getrandbits(8)
                if bits and not prefix:
                    prefix = i * 8 + Key._bp(bits)
                self[i] = bits
        elif isinstance(value, bytearray):
            Key._assert_length(value, buckets)
            super(Key, self).__init__(value)
        elif isinstance(value, bytes):
            Key._assert_length(value, buckets, strict=False)
            super(Key, self).__init__(buckets)
            start = buckets - len(value)
            for i in range(buckets):
                if i < start:
                    self[i] = 0
                else:
                    val = value[i - start]
                    if val and not prefix:
                        prefix = i * 8 + Key._bp(val)
                    self[i] = val
        elif isinstance(value, str):
            Key._assert_length(value, buckets, strict=False)
            super(Key, self).__init__(buckets)
            start = buckets - len(value)
            for i in range(buckets):
                if i < start:
                    self[i] = 0
                else:
                    val = ord(value[i - start])
                    if val and not prefix:
                        prefix = i * 8 + Key._bp(val)
                    self[i] = val
        else:
            raise TypeError(
                'value must be string or bytearray: found %s' %
                type(value).__name__)
        self._prefix = prefix if prefix else buckets * 8 - 1
        self._hex = '0x%s' % self.raw[self.prefix // 4:]

    def __repr__(self):
        return self._hex

    def __str__(self):
        return self._hex

    def __xor__(self, other):
        Key._assert_length(self, other.buckets)
        ba = bytearray(self.buckets)
        prefix = None
        for i, e in enumerate(other):
            val = self[i] ^ e
            if val and not prefix:
                prefix = i * 8 + Key._bp(val)
            ba[i] = val
        key = Key(ba, buckets=self.buckets, prefix=prefix)
        return key

    @property
    def buckets(self):
        return len(self)

    @property
    def prefix(self):
        return self._prefix

    @property
    def raw(self):
        return getattr(super(Key, self), 'hex')()

    @classmethod
    def _bp(cls, byte):
        if isinstance(byte, str):
            byte = ord(byte)
        if isinstance(byte, bytes):
            byte = byte[0]
        for i in range(8):
            if (byte >> (7 - i)) & 0x1 != 0:
                return i
        return 7

    @classmethod
    def _assert_length(cls, value, buckets, strict=True):
        if (strict and len(value) != buckets) or \
                (not strict and len(value) > buckets):
            raise ValueError(
                'cannot unpack key into %d buckets: %s' %
                (buckets, value))
