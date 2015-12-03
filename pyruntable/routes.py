class RoutingTable(tuple):

    DEFAULT_BUCKETS = 128

    def __new__(cls, *args, **kwargs):
        if args:
            size = args[0]
        else:
            size = RoutingTable.DEFAULT_BUCKETS
        table = [[] for _ in range(size)]
        return tuple.__new__(cls, table)
