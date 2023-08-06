"""For loading and interacting with Tree-data files."""

from __future__ import annotations

import json
import os
from typing import Any
import yaml
import jmespath

from flexi_settings import BaseError
from flexi_settings.visitors import TreeDataVisitor

NONE_MARKER = '__none__'
"""Placeholder for None values in dicts"""
UNDEFINED_MAGIC = '__not_defined__'
"""For variable defaults that are not defined since None could be a valid default variable value"""


class JmesNotFound(BaseError):
    """Raised if the ``jmespath.search()`` returns None, indicating the query failed to locate.

    This relates only to :class:`TreeData` searching with :meth:`~TreeData.jmesquery` queries.

    """

    def __init__(self, query_term: str):
        super().__init__(message='The jmespath failed to find: {}'.format(query_term))


class Loader(object):
    """Base class for file loaders."""

    @classmethod
    def load(cls, filename: str) -> TreeData:
        """Load the file at ``filename``."""
        raise NotImplementedError()


class YamlLoader(Loader):
    """YAML file loader."""

    @classmethod
    def load(cls, filename: str):  # noqa: D102
        with open(os.path.realpath(filename)) as fp:
            data = yaml.safe_load(fp)

        return TreeData(**data)


class JsonLoader(Loader):
    """JSON file loader."""

    @classmethod
    def load(cls, filename: str):  # noqa: D102
        with open(os.path.realpath(filename)) as fp:
            data = json.load(fp)

        return TreeData(**data)


class IniLoader(Loader):
    """Basic INI file loader."""

    @classmethod
    def load(cls, filename: str) -> TreeData:  # noqa: D102
        from configparser import ConfigParser

        parser = ConfigParser()
        parser.read(filename)

        # noinspection PyProtectedMember
        data = parser._sections  # Why the hell no parser.sections Python??

        return TreeData(**data)


class TreeData(dict):
    """For loading and interacting with tree-like files with jmespath.

    The :meth:`load` method supports loading from JSON and YAML by inspecting the
    filename extension. Supported extensions are ".json", ".yml" and ".yaml" - to load
    with a filename that is non-standard, the :meth:`load_yaml` and :meth:`load_json` can
    be called directly.

    **JMESPATH Support**

    The ``jmespath`` search returns None for both when a query is not found and when
    a value is None in the original dict - there is no easy way to determine if the query is
    valid for the data.

    This helper class provides a way to load from JSON or YAML files and do jmespath queries
    that will return None when the original value was None, and will raise a
    :class:`JmesNotFound` if the query does not find the node or is invalid
    in some way.

    This will use the NoneValueVisitor on the data to replace None with the
    NONE_MARKER, which is returned as None for :meth:`jmesquery`.

    .. seealso::

        https://github.com/jmespath/jmespath.py/issues/113

    """

    supported_extensions = ["yml", 'yaml', 'json', 'ini', 'cfg']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        NoneValueVisitor().visit(self)

    def jmesquery(self, query: str, safe: bool = False) -> Any:
        """Do jmespath query on self.

        This does a jmespath.search() on self. If the query returns None this raises
        a :class:`JmesNotFound` exception. It returns None if the original value
        for an item was None (it will have the "NONE_MARKER" placeholder for None).

        :param query: A jmespath query
        :param safe: True to return None both for not found and for None value
        :return:
        :raises JmesNotFound: If the query was not able to find the results.
        """
        value = jmespath.search(query, self)
        if value is None:
            if not safe:
                raise JmesNotFound(query_term=query)

        # Was it originally None in the YAML/JSON/dict?
        if value == NONE_MARKER:
            return None

        return value

    @classmethod
    def load(cls, filename: str) -> TreeData:
        """Load the file, inspecting the name for type.

        Supports formats/extensions:

        .. list-table:: Default Extensions
           :header-rows: 1
           :align: left

           * - Format
             - Extensions
           * - YAML
             - .yml, .yaml
           * - JSON
             - .json
           * - INI
             - .ini, .cfg

        :param filename: A JSON or YAML filename.
        """
        from pathlib import PurePath
        pp = PurePath(filename)

        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        suffix = pp.suffix.lower()

        if suffix in ['.yml', '.yaml']:
            return YamlLoader.load(filename=filename)

        elif suffix == '.json':
            return JsonLoader.load(filename=filename)

        elif suffix in ['.ini', '.cfg']:
            return IniLoader.load(filename=filename)

        raise ValueError('Filename not supported. Must be YAML or JSON ending in .yml, .yaml, or .json')


class NoneValueVisitor(TreeDataVisitor):
    """Set values that are None to the :data:`NONE_MARKER` placeholder.

    .. note::

        The excellent `jmespath <https://jmespath.org/>`_ library has one flaw: When doing
        a ``jmespath.search("find.some.key", data)``, if there is no "key" within the node
        "find.some", the library returns None. For our purposes we *must* know if the key
        is present.

        This allows us to call :meth:`TreeData.jmesquery` and know that a returned None is
        the actual value and not also an unresolved jmespath search (which will raise a
        :class:`JmesNotFound` exception).

    """

    def __init__(self, restore_none: bool = False):
        """Construct.

        :param restore_none: True to restore NONE_MARKER back to None
        """
        super().__init__()

        self.restore_none = restore_none

    # noinspection PyUnusedLocal
    def visit_dict_item(self, key, value) -> Any:
        """Return :data:`NONE_MARKER` if value is None.

        If :attr:`restore_none` is True this returns None on finding a :data:`NONE_MARKER`.

        """
        if value is None and not self.restore_none:
            return NONE_MARKER

        elif value == NONE_MARKER and self.restore_none:
            return None

        return self.visit(node=value)

    # noinspection PyMethodMayBeStatic
    def visit_scalar(self, node) -> Any:
        """Replace None with :data:`NONE_MARKER`."""
        if node is None and not self.restore_none:
            return NONE_MARKER

        elif node == NONE_MARKER and self.restore_none:
            return None

        return node
