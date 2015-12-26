from threading import Thread
import peertable.routes
import peertable.addr
import socket
import time


class Peer(Thread):

    def __init__(self, port, key=None, host=None):
        Thread.__init__(self)
        self._addr = peertable.addr.Address(port, key=key, host=host)
        self._routes = peertable.routes.Table(
                address=self.address,
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
