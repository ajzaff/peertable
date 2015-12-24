from pyruntable import peer
import socket

if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('127.0.0.1', 12347))
    # x = peer.Peer(12348)
    # x.start()
