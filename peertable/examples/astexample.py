import ast


def pretty_ast(a, level=0, indent=True):
    def fmt(s):
        if indent and level > 0:
            s = '\t' * level + s
        return s

    if isinstance(a, ast.ImportFrom):
        names = ', '\
            .join(map(
                lambda e:
                pretty_ast(
                    e, level=level, indent=False),
                a.names))
        return fmt('from %s import %s' %
                   (a.module, names))
    elif isinstance(a, ast.Import):
        return fmt('import %s' % pretty_ast(a.names))
    elif isinstance(a, ast.Name):
        return fmt(a.id)
    elif isinstance(a, ast.alias):
        if a.asname:
            return fmt('%s as %s' % (a.name, a.asname))
        else:
            return fmt(a.name)
    elif isinstance(a, ast.If):
        test = pretty_ast(a.test,
                          level=level,
                          indent=False)
        body = pretty_ast(a.body,
                          level=level+1,
                          indent=indent)
        or_else = None
        if len(a.orelse) > 0:
            or_else = pretty_ast(a.orelse[0],
                                 level=level,
                                 indent=indent)
        s = fmt('if %s:' % test)
        s += body
        if or_else:
            s += or_else
    return None


if __name__ == '__main__':
    f = open('testast.py', 'r')
    code = ast.parse(f.read())
    for r in ast.walk(code):
        print(r, r._fields)
        for f in r._fields:
            print(f, eval('r.%s' % f))
        print(pretty_ast(r))
        print('---')
