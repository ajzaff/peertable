from pyruntable import defaults


class RoutingTable(tuple):
    def __new__(cls, *args, **kwargs):
        if args:
            size = args[0]
        else:
            size = defaults.DEFAULT_KEY_SIZE
        repr = [[] for _ in range(size)]
        return tuple.__new__(cls, repr)


if __name__ == '__main__':
    rt = RoutingTable(128)
    print(rt)