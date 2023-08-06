"""Collection of nodes used in unittests.

PYTHONPATH will be automatically set so Python can find this package.
"""
import sys


def sum(argv=None):
    """Entrypoint used with **pymodule** runner."""
    from functools import reduce

    print(reduce(lambda x, y: x + y, [int(_) for _ in argv]) if argv is not None else 0)


def main(argv=None):
    """Entrypoint used with **python** runner."""
    sum(argv=argv)


if __name__ == "__main__":
    main(sys.argv)
