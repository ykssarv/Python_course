"""."""

from abc import ABCMeta, abstractmethod


class TreeNode(metaclass=ABCMeta):
    """The main node class."""

    def __init__(self, *args):
        """:param make use of *args and store them in a way that it is easy to use them."""
        if isinstance(*args, tuple):
            self.left, self.right = args[0]

    @abstractmethod
    def apply(self):
        """abstract method which should be overridden to compute the value of the given abstract tree."""
        pass

    @abstractmethod
    def class_str(self):
        """:return class string representation of the object."""
        pass

    @abstractmethod
    def __str__(self):
        """:return string representation of the object."""
        pass

    def __eq__(self, other):
        """:return True when 2 object trees have the same shape and values."""
        return False

    def __ne__(self, other):
        """:return True when 2 object trees have a different shape and/or values."""
        return False
