import unittest
from pyruntable.peer import PeerKey


class TestPeer(unittest.TestCase):
    pass


class TestPeerKey(unittest.TestCase):
    def testRandom(self):
        key = PeerKey.random()


class TestPeerAddress(unittest.TestCase):
    pass
