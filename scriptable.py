#!/usr/bin/env python
"""Allows calling a python function as a command line script.
"""


import sys
import inspect
import types

USAGE = 'Usage: ./scriptable.py mypackage.myfunc'


def scriptable(func_path, *args):
    """Wrap callable named by func_path so that it's input
    comes from stdin and it's output goes to stdout.
    That makes it usable in a unix pipeline.
    """

    func_name = func_path.split('.')[-1]
    module_name = '.'.join(func_path.split('.')[:-1])
    module = __import__(module_name, globals(), locals(), func_name)
    func = getattr(module, func_name)

    argspec = inspect.getargspec(func)
    has_args = (len(argspec.args) != 0 or
                argspec.varargs or
                argspec.keywords)

    if has_args:
        input_ = [line.strip() for line in sys.stdin]
        output = func(input_, *args)
    else:
        output = func()

    if output:
        if not isinstance(output, types.StringTypes):
            try:
                output = '\n'.join([unicode(val) for val in output])
            except TypeError:
                pass
        print(output)

def main(argv=None):
    """Entry point when used from command line"""
    if not argv:
        argv = sys.argv
    if len(argv) <= 1:
        print(USAGE)
        return 1
    scriptable(*argv[1:])       # pylint: disable=W0142

if __name__ == '__main__':
    sys.exit(main())
