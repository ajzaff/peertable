class RoutingTable(tuple):

    DEFAULT_BUCKETS = 160

    def __new__(cls, buckets=None):
        if buckets is None:
            buckets = RoutingTable.DEFAULT_BUCKETS
        return tuple.__new__(cls, ([] for _ in range(8 * buckets)))
