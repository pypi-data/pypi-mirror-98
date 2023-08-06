import sys
from typing import Callable


def is_class(cls):
    return isinstance(cls, type)


class classproperty:
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class staticproperty:
    """
    @property for @staticmethod
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, *a):
        return self.fget()


def join(sep, iterable, mapper: Callable[[object], str] = str, except_values=(None,)):
    return sep.join(map(
        lambda v: '' if v in except_values else mapper(v),
        iterable
    ))


def escape(s, quote=True):
    """
    # forked from html.escape
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def call_function_get_frame(func, *args, **kwargs):
    """
    https://stackoverflow.com/a/52358426/8851903
    Calls the function *func* with the specified arguments and keyword
    arguments and snatches its local frame before it actually executes.
    """

    frame = None
    trace = sys.gettrace()

    def snatch_locals(_frame, name, arg):
        nonlocal frame
        if frame is None and name == 'call':
            frame = _frame
            sys.settrace(trace)
        return trace
    sys.settrace(snatch_locals)
    try:
        result = func(*args, **kwargs)
    finally:
        sys.settrace(trace)
    return frame, result
