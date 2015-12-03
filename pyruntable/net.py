from routes import RoutingTable


class PeerNet(dict):
    def __init__(self, buckets=None):
        super(PeerNet, self).__init__()
        if buckets is None:
            buckets = RoutingTable.DEFAULT_BUCKETS
        self.buckets = buckets

    def __delitem__(self, key):
        # TODO: unregister ``key'' from the network.
        super(PeerNet, self).__delitem__(key)

    def __setitem__(self, key, value):
        # TODO: register ``value'' to the network.
        super(PeerNet, self).__setitem__(key, value)

    def update(self, other=None, **kwargs):
        # TODO: register all ``other'' to the network.
        super(PeerNet, self).update(other=other)

    def setdefault(self, key, default=None):
        raise NotImplementedError(
            'setdefault is not implemented')