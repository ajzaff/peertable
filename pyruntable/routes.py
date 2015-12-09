class RoutingTable(tuple):
    def __new__(cls, buckets):
        return tuple.__new__(cls, ([] for _ in range(8 * buckets)))
