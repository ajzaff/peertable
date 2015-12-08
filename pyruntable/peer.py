from routes import RoutingTable
from threading import Thread
import socket
import random
import time


class Peer(Thread):
    def __init__(self, port,
                 pid=None,
                 host=None,
                 backlog=5):
        Thread.__init__(self)
        self._addr = PeerAddress(port, pid=pid, host=host)
        self.backlog = backlog

    def run(self):
        sock = socket.socket()
        sock.bind(self._addr)
        sock.listen(self.backlog)
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

    def log(self, message, *args):
        ptime = time.ctime(Peer.time())
        print("[%s] Peer %s %s" % (ptime, self.address.key, message))


class PeerAddress(object):
    def __init__(self, port, pid=None, host=None):
        if host is None:
            host = 'localhost'
        if pid is None:
            pid = PeerKey.random()
        self._id = pid
        self._host = socket.gethostbyname(host)
        self._port = port

    def __str__(self):
        return '%s%s' % (self.host, self.port)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def key(self):
        return self._id


class PeerKey(int):

    def __init__(self, value, buckets=None, base=10):
        super(PeerKey, self).__init__()
        if buckets is None:
            buckets = RoutingTable.DEFAULT_BUCKETS
        self._buckets = buckets
        self._prefix = None
        self._dump = None

    def __new__(cls, value, buckets=None, base=10):
        if base == 10:
            return int.__new__(cls, value)
        else:
            return int.__new__(cls, value, base=base)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.dump

    def __len__(self):
        return self._buckets

    def __xor__(self, other):
        return PeerKey(int(self) ^ int(other))

    def __ixor__(self, other):
        return PeerKey(int(self) ^ int(other))

    @property
    def buckets(self):
        return self._buckets

    @property
    def dump(self):
        if self._dump is None:
            self._dump = hex(self)
        return self._dump

    @property
    def prefix(self):
        if self._prefix is None:
            digits = str(int(self))
            for i, d in enumerate(digits):
                d = int(d)
                for j in range(8):
                    if (d >> (7 - j)) & 0x1 != 0:
                        self._prefix = i * 8 + j
                        return self._prefix
            self._prefix = self.buckets * 8 - 1
        return self._prefix

    @classmethod
    def random(cls, bits=None):
        if bits is None:
            bits = RoutingTable.DEFAULT_BUCKETS
        bits = random.getrandbits(bits)
        return PeerKey(bits)