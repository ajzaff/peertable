from routes import RoutingTable


class PeerNet(object):

    def __init__(self, buckets=None):
        if buckets is None:
            buckets = RoutingTable.DEFAULT_BUCKETS
        self.buckets = buckets
