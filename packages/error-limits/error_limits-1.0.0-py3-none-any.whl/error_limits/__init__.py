from itertools import product


class Range:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __repr__(self):
        return f'[{self.lower}, {self.upper}]'

    def __eq__(self, other):
        return self.lower == other.lower and self.upper == other.upper


def imprecise(func):
    def wrapper(*args, **kwargs):

        ranges = tuple(
            (args.lower, args.upper) if isinstance(args, Range)
            else (args, ) for args in args
        ) + tuple(
                ((k, v.lower), (k, v.upper)) if isinstance(v, Range)
                else ((k, v), ) for k, v in kwargs.items()
        )
        results = tuple(
            func(*arguments[:len(args)], **dict(arguments[len(args):]))
            for arguments in product(*ranges)
        )
        return Range(min(results), max(results))

    return wrapper
