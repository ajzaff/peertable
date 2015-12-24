from threading import Thread
from pyruntable import routes
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

    def __init__(self, value=None, buckets=20, prefix=None, rand=None):
        if buckets <= 0:
            raise ValueError('buckets must be > 0: found %d' % buckets)
        if rand is None:
            rand = random.Random()
        if isinstance(value, int):
            buckets = value
            value = None
        if value is None:
            self._init_none(buckets, rand, prefix)
        elif isinstance(value, bytearray):
            self._init_bytearray(value, buckets)
        elif isinstance(value, bytes):
            self._init_bytes(value, buckets, prefix)
        elif isinstance(value, str):
            self._init_str(value, buckets, prefix)
        else:
            super(Key, self).__init__()
            raise TypeError(
                'value must be string or bytearray: found %s' %
                type(value).__name__)
        self._prefix = prefix if prefix else buckets * 8 - 1

    def _init_none(self, buckets, rand, prefix):
        super(Key, self).__init__(buckets)
        for i in range(buckets):
            bits = rand.getrandbits(8)
            if bits and not prefix:
                prefix = i * 8 + Key._bp(bits)
            self[i] = bits

    def _init_bytearray(self, value, buckets):
        Key._assert_length(value, buckets)
        super(Key, self).__init__(value)

    def _init_bytes(self, value, buckets, prefix):
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

    def _init_str(self, value, buckets, prefix):
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

    def __repr__(self):
        return self.raw

    def __str__(self):
        return self.raw

    def __xor__(self, other):
        Key._assert_length(self, other.buckets)
        i = min(self.prefix, other.prefix) // 4
        ba = bytearray(self.buckets)
        prefix = None
        while i < other.buckets:
            e = other[i]
            val = self[i] ^ e
            if val and not prefix:
                prefix = i * 8 + Key._bp(val)
            ba[i] = val
            i += 1
        key = Key(ba, buckets=self.buckets, prefix=prefix)
        return key

    def rprefix(self, other):
        Key._assert_length(self, other.buckets)
        i = min(self.prefix, other.prefix) // 4
        while i < self.buckets:
            e = other[i]
            val = self[i] ^ e
            if val:
                return i * 8 + Key._bp(val)
            i += 1
        return self.buckets * 8 - 1

    @property
    def raw(self):
        return hex(int(''.join(str(k) for k in self)))

    @property
    def buckets(self):
        return len(self)

    @property
    def prefix(self):
        return self._prefix

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
