"""A simple, fake database"""

from __future__ import annotations

import os
from typing import Union

from flexi_settings import module_dir
from flexi_settings.tree_data import TreeData


class FakeDB(object):
    """A fake database."""

    def __init__(self, host: str, port: int, user: str, pwd: str):

        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

        print('Creating "DB" Host={}, Port={}, User={}, Pwd={}'.format(
            host, port, user, pwd
        ))

        self.data = self._load()

    @classmethod
    def _load(cls) -> TreeData:
        this_dir = module_dir(name_or_module=__name__)
        data = TreeData.load(filename=os.path.join(this_dir, 'db.yml'))

        return data

    def get(self, key: str) -> Union[dict, None]:
        """Get a record by key."""
        return self.data.jmesquery(key, safe=True)

    def put(self, key: str, data: dict):
        """Store a record (in memory only)"""
        self.data[key] = data

    def delete(self, key: str):
        try:
            del self.data[key]

        except KeyError:
            pass
