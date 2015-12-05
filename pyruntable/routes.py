class RoutingTable(tuple):

    DEFAULT_BUCKETS = 160

    def __new__(cls, *args, **kwargs):
        if args:
            buckets = args[0]
        else:
            buckets = RoutingTable.DEFAULT_BUCKETS
        table = [[] for _ in range(buckets)]
        return tuple.__new__(cls, table)