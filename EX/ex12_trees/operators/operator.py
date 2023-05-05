"""."""

from abc import abstractmethod

from operators.leaf import Leaf
from tree_node import TreeNode


class Operator(TreeNode):
    """Custom operation wrapper."""

    def __init__(self, *args):
        """Store the given arguments somehow."""
        super().__init__(*args)

    def apply(self):
        """Make use of the *args to compute the value of the given subtree. Recursion is your friend."""
        combination = (self.left.apply().__class__, self.right.apply().__class__)
        if combination in self.actions.keys():
            return self.actions[combination](self.left.apply(), self.right.apply())
        return self.default_operator.__call__(self.left.apply(), self.right.apply())

    def class_str(self):
        """:return class string representation of the object."""
        return f"{self.__class__.__name__}({self.left.class_str()}, {self.right.class_str()})"

    def __str__(self):
        """:return the mathematical string representation of the tree with least amount of parenthesis."""
        left_part = str(self.left)
        right_part = str(self.right)
        if not isinstance(self.left, Leaf) and self.left.priority < self.priority:
            left_part = f"({left_part})"
        if not isinstance(self.right, Leaf) and self.right.priority < self.priority:
            right_part = f"({right_part})"
        if not isinstance(self.right, Leaf) and self.right.priority == self.priority and not self.right.associativity:
            right_part = f"({right_part})"
        return f"{left_part} {self.default_operator} {right_part}"

    def __eq__(self, other):
        """:return True when 2 object trees have the same shape and values."""
        return self.left == other.left and self.right == other.right and type(self) is type(other)

    def __ne__(self, other):
        """:return True when 2 object trees have a different shape and/or values."""
        return self.left != other.left or self.right != other.right or type(self) is not type(other)

    @property
    def associativity(self):
        """abstract method witch should be overridden to return a boolean when the node is not associative."""
        return True

    @property
    @abstractmethod
    def default_operator(self):
        """abstract method which should be overridden to return the default_operator object."""
        pass

    @property
    @abstractmethod
    def priority(self):
        """
        abstract method witch should be overridden to return priority of the node.

        Boolean whether the operation is associative or not.
        For example addition is associative but subtraction is not.
        Override this property for operations where the given operation is not associative.
        Visit: https://en.wikipedia.org/wiki/Order_of_operations
        """
        pass

    @property
    @abstractmethod
    def actions(self):
        """
        All custom implemented actions on different data structures.

        For example set - int does not exist, but we can implement it.
        :return a dictionary of functions where key is accepted parameters and value is a function which takes the
        aforementioned parameters as inputs and computes a value with them.
        """
        pass
