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
        self.setdefault(key, default=value)

    def update(self, other=None, **kwargs):
        # TODO: register all ``other'' to the network.
        super(PeerNet, self).update(other=other, **kwargs)

    def setdefault(self, key, default=None):
        if key not in self:
            # TODO: register ``key'' to the network.
            pass
        return super(PeerNet, self).setdefault(key, default=default)

