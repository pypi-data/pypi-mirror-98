"""Representation of a variable."""

import re
from dataclasses import dataclass
from typing import Any, List

from typing.re import Match

from flexi_settings.tree_data import UNDEFINED_MAGIC


@dataclass
class Variable(object):
    """A single variable representation."""

    var_name: str
    """The variable name"""
    var_type: str = None
    """The variable value type."""
    default: Any = UNDEFINED_MAGIC
    """The default value if the variable is not resolved (always a str)"""

    def __eq__(self, other):
        if isinstance(other, Variable):
            return super().__eq__(other)

        return other == self.var_name

    @classmethod
    def from_re_match(cls, match: Match):
        """Create instance from a re match"""
        return Variable(var_name=match.group(1),
                        var_type=match.group(2),
                        default=match.group(3) or UNDEFINED_MAGIC)

    @property
    def template(self):
        """Return self as a string variable template"""
        def_str = "" if self.default == UNDEFINED_MAGIC else self.default

        return '{}:{}:{}'.format(self.var_name, self.var_type, def_str)

    def __str__(self):
        return self.var_name

    def __repr__(self):
        return 'Variable: Name={}, Type={}, Default={}'.format(self.var_name,
                                                               self.var_type,
                                                               self.default)

    def apply_type_hint(self, value: str) -> Any:
        """Return the ``value`` with type hinting applied.

        A variable with type-hinting looks like "!VAR:int!" with "int" as the type hint.

        Supported hint types (type/None default):

        * str/char: ""
        * int: 0
        * float: 0.0
        * dict: {}
        * list: []
        * bool: False

        If the value is ``None`` this will set the value as shown above to a default.

        :param value: The value to (possibly) convert to a type
        :return: The ``value`` with type hinting applied
        :raises ValueError: If ``type_hint`` is not supported or can not be applied to value
        """
        # If no hinting, return the value unchanged
        if not self.var_type:
            return value

        # We only support a finite set of types (for safety)
        if self.var_type not in VariableString.supported_types:
            raise ValueError('Unsupported var substitution type hint: {}'.format(self.var_type))

        return self._apply(value=value)

    def _apply(self, value: str) -> Any:
        # Yes, "eval" is dangerous. The above test should limit our exposure
        try:
            if value is None:
                return self._apply_none()

            else:
                if self.var_type == 'str':
                    value = '{}'.format(value)
                else:
                    if self.var_type == 'bool' and value in ['false', 'true']:
                        value = value.title()
                    value = eval("{hint}({val})".format(hint=self.var_type, val=value))

            return value

        except ValueError as ex:
            raise ValueError('Error applying type hint "{}" to string "{}"'.format(
                self.var_type,
                value
            )) from ex

    def _apply_none(self) -> Any:
        value = ""
        if self.var_type in ['str', 'char']:
            value = ""
        elif self.var_type == 'int':
            value = "0"
        elif self.var_type == 'float':
            value = '0.0'
        elif self.var_type == 'dict':
            value = dict()
        elif self.var_type == 'list':
            value = []
        elif self.var_type == 'bool':
            value = False

        return value


class VariableString(object):
    """Representation and handling of embedded variables."""

    re_embedded_var = re.compile(r'!([A-Z_a-z0-9\-.]+):?([a-z]*):?([\d\s\w\\-_]*)!')
    """Regex representation of our variable format"""

    supported_types = ['int', 'str', 'float', 'char', 'dict', 'list', 'bool']
    """The finite set of supported types for embedded variables."""

    def __init__(self, string: str):
        self.string: str = string
        """The full string"""

        self.variables: List[Variable] = []
        """The list of variables found in ``string``"""

        # Parse the string, looking for embedded variables
        self._parse_variable(string)

    @property
    def has_vars(self) -> bool:
        """Return True if self has variables."""
        return len(self.variables) > 0

    @classmethod
    def str_has_vars(cls, string: str) -> bool:
        """Check a string to see if it contains variables."""
        return cls.re_embedded_var.search(string) is not None

    @property
    def first(self):
        """Helper to fetch the one-and-only variable"""
        return self.variables[0]

    def convert_to_var(self):
        """This is to convert the contents to a var"""
        self.variables.append(Variable(var_name=self.string))

    def is_single_var(self) -> bool:
        """Check to see if this string is a simple string variable only.

        .. code-block: python

            "!VAR!" == True
            "!VAR:int!" == True
            "This has an !EMBEDDED! variable" == False

        Basically, verifies that the string contains only a single variable template.

        """
        if self.has_vars:
            return len(self.variables) == 1 and self.variables[0].template == self.string

        return False

    def _parse_variable(self, string: str):
        """Parse the variable with our regex.

        :param string:
        :return:
        """
        var_matches = self.re_embedded_var.findall(string)
        if not var_matches:
            self.convert_to_var()
            return

        # Iterate the list of tuples
        for name, var_type, default in var_matches:
            self.variables.append(Variable(var_name=name,
                                           var_type=var_type or 'str',
                                           default=default or UNDEFINED_MAGIC)
                                  )

    def __iter__(self) -> Variable:
        for var in self.variables:
            yield var

    def __len__(self) -> int:
        return len(self.variables)
