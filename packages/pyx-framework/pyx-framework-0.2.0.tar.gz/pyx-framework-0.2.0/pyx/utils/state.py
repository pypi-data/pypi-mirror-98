from functools import wraps


def __wrapper__(method):
    @wraps(method)
    def __wrapped_method__(self, *args, **kwargs):
        args = (
            arg.__get__() if hasattr(arg, '__get__') else arg
            for arg in args
        )
        kwargs = {
            name:
                value.__get__() if hasattr(value, '__get__') else value
            for name, value in kwargs.items()
        }

        return method(self, *args, **kwargs)

    return __wrapped_method__


class state:
    # MAIN STATE

    _value_init = None
    _value = None

    def __init__(self, value):
        self.__set__(value)

    def __get__(self):
        return self._value

    def __set__(self, value):
        self._value = value
        if self._value_init is None:
            self._value_init = value

    def __del__(self):
        self._value = None

    def __get_init__(self):
        return self._value_init

    # END MAIN STATE

    @__wrapper__
    def __getitem__(self, key):
        return self._value.__getitem__(key)

    @__wrapper__
    def __setitem__(self, key, value):
        return self._value.__setitem__(key, value)

    @__wrapper__
    def __delitem__(self, key):
        return self._value.__delitem__(key)

    # TODO: wrap getattribute if callable,
    #  to wrap arguments with .__get__() if available,
    #  because argument can be state

    # TODO: рими в комітах, щоб привернути увагу!!1!

    def __getattr__(self, key: str):
        if key == '_value' or key in dir(self):
            return super().__getattribute__(key)

        return self._value.__getattribute__(key)

    def __setattr__(self, key: str, value: object):
        if key == '_value' or key in dir(self):
            return super().__setattr__(key, value)
        return self._value.__setattr__(key, value)

    def __delattr__(self, key: str):
        if key == '_value' or key in dir(self):
            return super().__delattr__(key)
        return self._value.__delattr__(key)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f'state({self._value})'

    def __len__(self):
        return len(self._value)
