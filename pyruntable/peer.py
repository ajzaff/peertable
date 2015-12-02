from pyruntable.net import PeerNet
import threading
import socket
import time


class Peer(object):
    def __init__(self, port, peer_id=None, host=None):
        """

        :param peer_id:
        :param port:
        :param host:
        :return:
        """
        if host is None:
            host = 'localhost'
        if peer_id is None:
            peer_id = PeerNet.new_id()
        self._peer_thread = threading.Thread(
            target=self._listen)
        self.host = socket.gethostbyname(host)
        self.port = port
        self.addr = (self.host, self.port)
        self.id = peer_id
        self.hex_id = hex(self.id)
        self._peer_thread.start()

    def _listen(self, backlog=5):
        sock = socket.socket()
        sock.bind(self.addr)
        sock.listen(backlog)
        Peer.log(
            "Peer %s listening on %s:%s..." %
            (self.hex_id, self.host, self.port))
        while True:
            client, addr = sock.accept()
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
    worker = Peer(port=12347)
    worker = Peer(port=12346)
