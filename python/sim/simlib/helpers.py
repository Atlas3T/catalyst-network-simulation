"""helper module.

Contains any small useful bits of code that don't belong anywhere else (yet).

"""

def overrides(interface_class):
    """
        Decorator to indicate that a method is overriding one in a base class. It will check that there is a method of that name in the base class.
    """
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider