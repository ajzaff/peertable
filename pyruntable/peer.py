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

    def log(self, message):
        ptime = time.ctime(Peer.time())
        print("[%s] Peer %s %s" % (ptime, self.address.key, message))


class PeerAddress(object):
    def __init__(self, port, pid=None, host=None):
        if host is None:
            host = 'localhost'
        if pid is None:
            pid = PeerKey()
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


class PeerKey(bytearray):

    N = 20

    def __init__(self, value=None, buckets=N, prefix=None, rand=random):
        if value is None:
            super(PeerKey, self).__init__(buckets)
            for i in range(buckets):
                bits = rand.getrandbits(8)
                if bits and not prefix:
                    prefix = i * 8 + PeerKey._bp(bits)
                self[i] = bits
        elif isinstance(value, bytearray):
            PeerKey._assert_length(value, buckets)
            super(PeerKey, self).__init__(value)
        elif isinstance(value, bytes):
            PeerKey._assert_length(value, buckets, strict=False)
            super(PeerKey, self).__init__(buckets)
            start = buckets - len(value)
            for i in range(buckets):
                if i < start:
                    self[i] = 0
                else:
                    val = value[i - start]
                    if val and not prefix:
                        prefix = i * 8 + PeerKey._bp(val)
                    self[i] = val
        elif isinstance(value, str):
            PeerKey._assert_length(value, buckets, strict=False)
            super(PeerKey, self).__init__(buckets)
            start = buckets - len(value)
            for i in range(buckets):
                if i < start:
                    self[i] = 0
                else:
                    val = ord(value[i - start])
                    if val and not prefix:
                        prefix = i * 8 + PeerKey._bp(val)
                    self[i] = val
        else:
            raise TypeError(
                'value must be string or bytearray: found %s' %
                type(value).__name__)
        self._prefix = prefix if prefix else buckets * 8 - 1

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

    def __xor__(self, other):
        PeerKey._assert_length(self, other.buckets)
        ba = bytearray(self.buckets)
        prefix = None
        for i, e in enumerate(other):
            val = self[i] ^ e
            if val and not prefix:
                prefix = i * 8 + PeerKey._bp(val)
            ba[i] = val
        key = PeerKey(ba, buckets=self.buckets, prefix=prefix)
        return key

    @property
    def buckets(self):
        return len(self)

    @property
    def prefix(self):
        return self._prefix