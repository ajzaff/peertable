import socket
import time


class Peer(object):
    def __init__(self, port, host=None):
        if host is None:
            host = 'localhost'
        self.sock = socket.socket()
        self.host = socket.gethostbyname(host)
        self.port = port
        self.addr = (self.host, self.port)

    def connect(self, node):
        sock = socket.socket()
        sock.connect(node.addr)
        sock.close()

    def clear(self):
        self.sock = socket.socket()

    def listen(self, backlog=5):
        self.sock.bind(self.addr)
        self.sock.listen(backlog)
        Peer.log(
            "Worker listening on %s:%s..." %
            (self.host, self.port))
        while True:
            client, addr = self.sock.accept()
            Peer.log(
                "Accepted connection from %s:%s..." %
                tuple(addr))

            # Do something with the client connection...

            client.close()

    @classmethod
    def time(cls):
        return time.time()

    @classmethod
    def log(cls, message, *args):
        print("[%s] %s" %
              (time.ctime(Peer.time()),
               message))


if __name__ == '__main__':
    worker = Peer(12345)
    worker.listen()
