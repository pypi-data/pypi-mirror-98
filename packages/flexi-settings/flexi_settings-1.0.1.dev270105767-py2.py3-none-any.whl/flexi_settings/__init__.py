"""Var Resolvers package.

Testing references

* :py:class:`SettingsContext`
* :class:`SettingsContext`
* :class:`context.SettingsContext`
* :py:class:`context.SettingsContext`

"""
import os
import sys
from types import ModuleType

from typing import Union

from decorator import decorator


class BaseError(Exception):
    """Base class for defining our exceptions.

    This will properly format the __repr__ and __str__.

    """

    def __init__(self, message='', detail=None):
        """Construct.

        :param message: Optional message parameter
        :param detail: Optional details
        """
        self.message = message
        self.detail = detail

    def __repr__(self):
        return '<{}>: {}'.format(self.__class__.__name__, self.__str__())

    def __str__(self):
        return '{}{}'.format(self.message, ': {}'.format(self.detail) if self.detail else '')


@decorator
def to_variable(func, name: str = 'variable', *args, **kwargs):
    """Convert the ``variable`` to Variable if str.

    :param func:
    :param name: The name of the variable parameter.
    :param args:
    :param kwargs:
    :return:
    """
    import inspect
    from flexi_settings.variable import VariableString, Variable

    spec = inspect.getfullargspec(func)
    # ndx = 1 if spec.args and spec.args[0] in ['cls', 'self'] else 0
    parm_ndx = spec.args.index(name)

    # This will raise ValueError if "name" is not found in list of arguments
    variable = args[parm_ndx]
    if isinstance(variable, str):
        if VariableString.str_has_vars(string=variable):
            variable = VariableString(string=variable).first
        else:
            variable = Variable(var_name=variable)
        tmp_args = list(args)
        tmp_args[parm_ndx] = variable
        args = tuple(tmp_args)

    try:
        data = func(*args, **kwargs)

    except Exception:
        raise

    return data


def module_dir(name_or_module: Union[str, ModuleType]):
    """Get the directory of a module by name.

    To use:

    .. code-block:: python

        here = module_dir(__name__)

    :param name_or_module: Either the string module name in `sys.modules` or the module
    :return:
    """
    if isinstance(name_or_module, ModuleType):
        pwd = os.path.dirname(os.path.realpath(name_or_module.__file__))

    elif isinstance(name_or_module, str):
        pwd = os.path.dirname(os.path.abspath(sys.modules[name_or_module].__file__))

    else:
        raise ValueError('Unrecognized parameter for name_or_module: {}'.format(type(name_or_module)))

    return pwd
