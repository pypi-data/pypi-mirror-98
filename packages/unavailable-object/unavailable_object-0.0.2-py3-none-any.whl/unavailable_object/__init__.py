"""
Optional dependency checking.
"""

__all__ = ["UnavailableObjectError", "UnavailableObject", "check_optional_object"]

import sys

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


class UnavailableObjectError(Exception):
    pass


class UnavailableObject:
    """
    An unavailable object.

    Args:
        name (str): Name of the unavailable object.
        msg (str, optional): Error message.
        none_child (bool): Return None instead of throwing an exception
            for __getattr and __getitem__.
    """

    def __init__(self, name, msg=None, none_child=False):
        self.name = name
        self.msg = msg
        self.none_child = none_child
        self._orig_exc = sys.exc_info()[1]

    def raise_(self, *_, **__):
        __tracebackhide__ = True

        msg = f"{self.name} is unavailable."
        if self.msg is not None:
            msg = f"{msg}\n\n{self.msg}"

        raise UnavailableObjectError(msg) from self._orig_exc

    __call__ = raise_

    def __getattr__(self, name):
        if self.none_child:
            return None
        self.raise_()

    def __getitem__(self, name):
        if self.none_child:
            return None

        self.raise_()


def check_available(*objects):
    """
    Check the availability of an optional object.

    This is optional but can be used to have somthing fail early.
    """
    __tracebackhide__ = True

    for obj in objects:
        if isinstance(obj, UnavailableObject):
            obj.raise_()
