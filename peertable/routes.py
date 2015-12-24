from pyruntable import peer


class Table(tuple):

    def __init__(self, address, buckets=20):
        super(Table, self).__init__()
        self._buckets = buckets
        self._address = address

    def __new__(cls, node, buckets=20):
        return tuple.__new__(cls, ([] for _ in range(8 * buckets)))

    def __getitem__(self, item):
        res = super(Table, self).__getitem__(item)
        return tuple(res)

    @property
    def address(self):
        return self._address

    @property
    def buckets(self):
        return self._buckets

    def update(self, contact):
        prefix = self.address.key.rprefix(contact.key)
        bucket = super(Table, self).__getitem__(prefix)
        try:
            i = bucket.index(self.address.key)
        except ValueError:
            i = None
        if i is None:
            if len(bucket) < 20:
                bucket.insert(0, contact)
            else:
                # TODO: evict old items that don't respond to a ping.
                pass
        else:
            bucket.insert(0, bucket.pop(i))
