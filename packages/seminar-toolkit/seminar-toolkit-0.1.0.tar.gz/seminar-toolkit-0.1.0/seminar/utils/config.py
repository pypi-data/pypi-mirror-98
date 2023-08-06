"""A recursive dictionary generator which allows for accessing keys via "."s .

Implementation mostly sourced from: https://stackoverflow.com/a/32107024/2714651.
"""


class Config(dict):
    """A recursive dictionary generater that allows for accessing keys via dots."""

    def __init__(self, *args, **kwargs):
        """Convert ``*args`` and ``**kwargs`` into dot-attribute dict.

        :param *args: varags
        :param **kwargs: varags
        """
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        """doctstring."""
        return self.get(attr)

    def __setattr__(self, key, value):
        """doctstring."""
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        """doctstring."""
        super().__setitem__(key, value)
        if isinstance(value, dict):
            value = Config(**value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        """doctstring."""
        self.__delitem__(item)

    def __delitem__(self, key):
        """doctstring."""
        super().__delitem__(key)
        del self.__dict__[key]
