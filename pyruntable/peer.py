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
            self.log("accepted connection from %s:%s..." % tuple(addr))
            self.log("received data %s" % client.recv(1024))
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
    def __init__(self, value):
        self.value = value
        self.dump = None

    def __int__(self):
        return self.value

    def __xor__(self, other):
        return self.value ^ other.value

    def __ixor__(self, other):
        return self.value ^ other.value

    def __str__(self):
        if not self.dump:
            self.dump = hex(self.value)
        return self.dump

    @classmethod
    def random(cls, bits=None):
        if bits is None:
            bits = RoutingTable.DEFAULT_BUCKETS
        bits = random.getrandbits(bits)
        return PeerKey(bits)
