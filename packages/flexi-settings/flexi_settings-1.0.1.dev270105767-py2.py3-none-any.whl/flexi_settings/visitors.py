"""Base visitor and supporting classes."""
from dataclasses import dataclass
from numbers import Number
from typing import Any, List


@dataclass
class StackItem(object):
    """Base for an entry in the :class:`Stack`."""

    @property
    def value(self) -> str:
        """Returns the properly formatted stack item string label for jmespath."""
        raise NotImplementedError()


@dataclass
class StackDictItem(StackItem):
    """Stack dict item."""

    key: str
    """The key name for the dict stack item."""

    @property
    def value(self) -> str:  # noqa: D102
        return '.{}'.format(self.key)

    def __str__(self) -> str:
        return self.value


@dataclass
class StackListItem(StackItem):
    """Stack list item."""

    index: int
    """The index numeric index."""

    @property
    def value(self) -> str:
        """Get the formatted value string."""
        return "[{}]".format(self.index)

    def __str__(self) -> str:
        return self.value


@dataclass
class Stack(object):
    """Context for visitors for the current node visit.

    A visitor method may use the stack to obtain the jmespath search
    string that would return the current node in the overall dictionary.

    """

    stack: List[StackItem] = None
    """The list of stack items."""

    def __post_init__(self):
        if not self.stack:
            self.stack = []

    def push(self, item: StackItem):
        """Push a new context item."""
        self.stack.append(item)

    def pop(self):
        """Pop the stack context item."""
        self.stack.pop()

    @property
    def value(self) -> str:
        """Return the current jmespath for the stack state."""
        parts = [item.value for item in self.stack]

        _value = ''.join(parts)
        return _value.strip('.')

    def clear(self):
        """Clear all stack items."""
        self.stack.clear()

    def __len__(self) -> int:
        return len(self.stack)

    def __str__(self) -> str:
        return self.value


class TreeDataVisitor(object):
    """Base for visitors on dict/TreeData objects.

    As the visitor visits ``dict`` and ``list`` nodes, the internal :attr:`key_stack`
    is updated and may be used to perform a jmespath search in the data. See
    the :class:`OverrideVisitor` for an example of using the stack.

    .. code-block: python

        data = TreeData.load("filename.yml")

        visitor = TreeDataVisitor()
        visitor.visit(data)

    """

    def __init__(self):
        self.key_stack: Stack = Stack()

    def reset(self):
        """Reset self."""
        self.key_stack.clear()

    @property
    def key_stack_string(self):
        """The contents of :attr:`key_stack` in dot notation."""
        return self.key_stack.value

    @staticmethod
    def is_number(num) -> bool:
        """Check if ``num`` is actually a number."""
        if num is True or num is False:
            return False
        return isinstance(num, Number)

    @staticmethod
    def is_array_like(obj, string_is_array=False, tuple_is_array=True) -> bool:
        """Determine if``obj`` is "list-like".

        This looks for ``__len__`` and ``__getitem__`` to determine if it's iterable.

        :param obj: The object to test
        :param string_is_array: True to treat strings like arrays
        :param tuple_is_array: True to treat tuples like arrays
        :return: True if ``obj`` is array-like
        """
        from collections import abc

        result = hasattr(obj, "__len__") and hasattr(obj, '__getitem__')

        if result and not string_is_array and isinstance(obj, (str, abc.ByteString)):
            result = False

        if result and not tuple_is_array and isinstance(obj, tuple):
            result = False

        return result

    @staticmethod
    def is_scalar(obj: Any) -> bool:
        """Test if the ``item`` is a scalar (Number, str, bool, etc)"""
        return not TreeDataVisitor.is_array_like(obj=obj)

    def visit(self, node) -> Any:
        """Visit handler for a generic node.

        .. todo::

            Might also want to support visiting objects (does not apply to dict/list visiting)

        """
        if isinstance(node, dict):
            return self.visit_dict(node)

        elif isinstance(node, list):
            return self.visit_list(node)

        elif TreeDataVisitor.is_scalar(obj=node):
            return self.visit_scalar(node)

        return node

    def visit_dict(self, node: dict) -> Any:
        """Visit a dict node.

        By default, this will call :meth:`visit_dict_item` for each node in the dict
        and update the node dict for ``key`` with the returned value (which will
        be the same ``value`` for this default implementation).

        :param node: The dict node to visit
        :meta private:
        """
        for key, value in node.items():
            # Push the key onto the key_stack
            self.key_stack.push(StackDictItem(key=key))

            # Visit the dict value and update node with the return
            updated = self.visit_dict_item(key, value)

            # For a dict item, update rather than replace
            if isinstance(node[key], dict):
                node[key].update(updated)
            else:
                node[key] = updated

            # Pop the key from the key_stack
            self.key_stack.pop()

        return node

    # noinspection PyUnusedLocal
    def visit_dict_item(self, key, value) -> Any:
        """Handle a dict's ``key``/``value`` item.

        By default, this will call :meth:`visit` with the ``value`` and then return
        ``value``.

        :meta private:
        :param key: The key for value in the parent ``dict`` node
        :param value: The value for key in the parent ``dict`` node
        :return: The ``value`` unchanged
        """
        return self.visit(node=value)

    def visit_list(self, node: list) -> Any:
        """Handle a list node.

        This iterates the list and calls :meth:`visit` for each and adds the reply
        to an updated list that is returned. By default, this simply returns the original
        data.

        :meta private:
        """
        updated: List[Any] = []

        for ndx, item in enumerate(node):
            self.key_stack.push(StackListItem(index=ndx))

            updated.append(self.visit(node=item))

            self.key_stack.pop()

        return updated

    # noinspection PyMethodMayBeStatic
    def visit_scalar(self, node) -> Any:
        """Receives a scalar value with no (real) context.

        By default, this simply returns the node.

        Note: An implementing Visitor class can determine the actual context by
        referencing the :attr:`key_stack` value if necessary.

        :meta private:
        """
        return node


class HasVariablesVisitor(TreeDataVisitor):
    """Visitor to check for the existence of embedded variables.

    The by-product of the call to :meth:`visit` is:

    * :attr:`has_variables` : Set to True if any variables found
    * :attr:`count`         : Set to the count of variables found

    Examples of use:

    .. code-block:: python

        # A one-liner quick test
        flag = HasVariablesVisitor().check("This is false")

        # Check the flag and/or count
        checker = HasVariablesVisitor()
        checker.check("!SOME_VARIABLE!")  # Returns True

        checker.has_variables  # True
        checker.count  # 1

        # A reusable visitor
        checker = HasVariablesVisitor()
        while SomeFlag:
            checker.visit(some_data)
            checker.has_variables
            checker.reset()

    """

    def __init__(self):
        super().__init__()

        self.has_variables: bool = False
        """True if we found variables"""
        self.count: int = 0

    def reset(self):
        """Reset self."""
        self.has_variables = False
        self.count = 0

    def check(self, node: Any):
        """Check node for variables recursively."""
        self.visit(node)
        return self.has_variables

    def visit_scalar(self, node) -> Any:
        """Set :data:`has_variables` True if scalar is/has variables.

        :meta private:
        :param node:
        :return:
        """
        from flexi_settings.var_resolver import VariableResolver

        if isinstance(node, str) and VariableResolver.has_variable(node=node):
            self.has_variables = True
            self.count += 1

        return node
