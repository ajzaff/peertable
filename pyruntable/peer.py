from routes import RoutingTable
from threading import Thread
import socket
import random
import time


class Peer(Thread):
    def __init__(self, port,
                 peer_id=None,
                 host=None,
                 backlog=5):
        Thread.__init__(self)
        if host is None:
            host = 'localhost'
        if peer_id is None:
            peer_id = PeerKey.random()
        self.host = socket.gethostbyname(host)
        self.port = port
        self.addr = (self.host, self.port)
        self.backlog = backlog
        self.key = peer_id

    def run(self):
        sock = socket.socket()
        sock.bind(self.addr)
        sock.listen(self.backlog)
        self.log("started listening on %s:%s..." %
                 (self.host, self.port))
        while True:
            client, addr = sock.accept()
            self.log("accepted connection from %s:%s..." %
                     tuple(addr))
            self.log("received data %s" %
                     client.recv(1024))
            client.close()
        self.log("shutting down...")

    @classmethod
    def time(cls):
        return time.time()

    def log(self, message, *args):
        ptime = time.ctime(Peer.time())
        print("[%s] Peer %s %s" %
              (ptime, self.key, message))


class PeerKey(object):
    def __init__(self, value, buckets=None):
        if buckets is None:
            self._buckets = RoutingTable.DEFAULT_BUCKETS
        self._value = value
        self._dump = None
        self._pfx = None

    def __int__(self):
        return self._value

    def __xor__(self, other):
        return self._value ^ other.value

    def __ixor__(self, other):
        return self._value ^ other.value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self._dump:
            self._dump = hex(self._value)
        return self._dump

    def __len__(self):
        return self._buckets

    def getprefix(self):
        if self._pfx is None:
            digits = str(self._value)
            for i, d in enumerate(digits):
                d = int(d)
                print(bin(d))
                print('---')
                for j in range(8):
                    if (d >> (7 - j)) & 0x1 != 0:
                        self._pfx = i * 8 + j
                        return self._pfx
            self._pfx = self._buckets * 8 - 1
        return self._pfx

    @classmethod
    def random(cls, bits=None):
        if bits is None:
            bits = RoutingTable.DEFAULT_BUCKETS
        bits = random.getrandbits(bits)
        return PeerKey(bits)

    value = property(fget=__int__, doc='(int) key value')
    buckets = property(fget=__len__, doc='(int) key length (bits)')
    dump = property(fget=__str__, doc='(str) key hex dump')
    prefix = property(fget=getprefix, doc='(int) prefix; a number of leading zeros')

if __name__ == '__main__':
    n = 10345<<1024
    key = PeerKey(n)
    print(key.prefix)