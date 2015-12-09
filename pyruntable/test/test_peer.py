# -*- coding utf-8 -*-

import unittest
from pyruntable.peer import PeerKey
import random


class TestPeer(unittest.TestCase):
    pass


class TestPeerKey(unittest.TestCase):

    def testInitDefaultRandom(self):
        rand = random.Random(1773)
        key = PeerKey(rand=rand)
        self.assertEqual(
            key, b'j6\xc2\xc2Ls\x0c\xbe\x1d'
                 b'\\B\xd1\xd5\xb6oiem\xd0\x9d')
        self.assertEqual(key.buckets, PeerKey.N)
        self.assertEqual(key.prefix, 1)

    def testInitStr(self):
        key = PeerKey(value='1234')
        self.assertEqual(len(key), PeerKey.N)
        self.assertEqual(key.buckets, PeerKey.N)
        self.assertEqual(key.prefix, 130)

    def testInitBucketsDefaultRandom(self):
        rand = random.Random(1773)
        key = PeerKey(buckets=20, rand=rand)
        self.assertEqual(
            key, b'j6\xc2\xc2Ls\x0c\xbe\x1d'
                 b'\\B\xd1\xd5\xb6oiem\xd0\x9d')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 1)

    def testInitBytes(self):
        key = PeerKey(value=b'1234')
        self.assertEqual(len(key), PeerKey.N)
        self.assertEqual(key.buckets, PeerKey.N)
        self.assertEqual(key.prefix, 130)

    def testInitStrBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            PeerKey(value='100', buckets=2)

    def testInitBytesBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            PeerKey(value=b'100', buckets=2)

    def testInitByteArrayBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            PeerKey(value=bytearray(1), buckets=2)

    def testInitTypeError(self):
        with self.assertRaises(TypeError):
            PeerKey(value=0)

    def testXor(self):
        key1 = PeerKey(value='34')
        key2 = PeerKey(value='12')
        res = key1 ^ key2
        expect = PeerKey(value='\x02\x06')
        self.assertEqual(res, expect)
        self.assertEqual(len(res), PeerKey.N)
        self.assertEqual(res.buckets, PeerKey.N)

    def testXorDifferentBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            key1 = PeerKey(buckets=1)
            key2 = PeerKey(buckets=2)
            key1 ^ key2

    def testBytePrefixerStr(self):
        p = PeerKey._bp('a')
        self.assertEqual(p, 1)

    def testBytePrefixerBytes(self):
        p = PeerKey._bp(b'9')
        self.assertEqual(p, 2)

    def testBytePrefixerInt(self):
        p = PeerKey._bp(0)
        self.assertEqual(p, 7)




class TestPeerAddress(unittest.TestCase):
    pass
