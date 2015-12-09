# -*- coding utf-8 -*-

import unittest
from pyruntable.peer import Key
import random


class TestPeer(unittest.TestCase):
    pass


class TestKey(unittest.TestCase):

    def testInitDefaultRandom(self):
        rand = random.Random(1773)
        key = Key(rand=rand)
        self.assertEqual(
            key, b'j6\xc2\xc2Ls\x0c\xbe\x1d'
                 b'\\B\xd1\xd5\xb6oiem\xd0\x9d')
        self.assertEqual(key.buckets, Key.N)
        self.assertEqual(key.prefix, 1)

    def testInitStr(self):
        key = Key(value='1234')
        self.assertEqual(len(key), Key.N)
        self.assertEqual(key.buckets, Key.N)
        self.assertEqual(key.prefix, 130)

    def testInitBucketsDefaultRandom(self):
        rand = random.Random(1773)
        key = Key(buckets=20, rand=rand)
        self.assertEqual(
            key, b'j6\xc2\xc2Ls\x0c\xbe\x1d'
                 b'\\B\xd1\xd5\xb6oiem\xd0\x9d')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 1)

    def testInitBytes(self):
        key = Key(value=b'1234')
        self.assertEqual(len(key), Key.N)
        self.assertEqual(key.buckets, Key.N)
        self.assertEqual(key.prefix, 130)

    def testInitStrBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            Key(value='100', buckets=2)

    def testInitBytesBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            Key(value=b'100', buckets=2)

    def testInitByteArrayBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            Key(value=bytearray(1), buckets=2)

    def testInitTypeError(self):
        with self.assertRaises(TypeError):
            Key(value=0)

    def testXor(self):
        key1 = Key(value='34')
        key2 = Key(value='12')
        res = key1 ^ key2
        expect = Key(value='\x02\x06')
        self.assertEqual(res, expect)
        self.assertEqual(len(res), Key.N)
        self.assertEqual(res.buckets, Key.N)

    def testXorDifferentBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            key1 = Key(buckets=1)
            key2 = Key(buckets=2)
            key1 ^ key2

    def testBytePrefixerStr(self):
        p = Key._bp('a')
        self.assertEqual(p, 1)

    def testBytePrefixerBytes(self):
        p = Key._bp(b'9')
        self.assertEqual(p, 2)

    def testBytePrefixerInt(self):
        p = Key._bp(0)
        self.assertEqual(p, 7)
