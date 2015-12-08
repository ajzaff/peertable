class RoutingTable(object):

    DEFAULT_BUCKETS = 160

    def __init__(self, buckets=None):
        if buckets is None:
            buckets = RoutingTable.DEFAULT_BUCKETS
        self._table = [[] for _ in range(buckets)]
        self._buckets = buckets

    def __len__(self):
        return self._buckets

    def __getitem__(self, item):
        return self._table[item]

    def __contains__(self, addr):
        # TODO: optimize address search
        for bucket in self._table:
            if addr in bucket:
                return True
        return False

    buckets = property(fget=__len__, fset=None, fdel=None,
                       doc='(int) size of the routing table')


if __name__ == '__main__':
    rt = RoutingTable()
    print(rt)
