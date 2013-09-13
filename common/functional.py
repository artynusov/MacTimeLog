empty = object()


def _method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)
    return inner


class LazyObject(object):
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.

    By subclassing, you have the opportunity to intercept and alter the
    instantiation. If you don't need to do that, use SimpleLazyObject.
    """
    def __init__(self, wrapped_cls):
        self._wrapped = empty
        self._wrapped_cls = wrapped_cls

    __getattr__ = _method_proxy(getattr)

    def __setattr__(self, name, value):
        if name in ("_wrapped", "_wrapped_cls"):
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__[name] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        self._wrapped = self._wrapped_cls()

    # introspection support:
    __members__ = property(lambda self: self.__dir__())
    __dir__ = _method_proxy(dir)