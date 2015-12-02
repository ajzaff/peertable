from pyruntable import defaults
import random


class PeerNet(dict):

    @classmethod
    def new_id(cls, keysize=None):
        if keysize is None:
            keysize = defaults.DEFAULT_KEY_SIZE
        return random.getrandbits(keysize)