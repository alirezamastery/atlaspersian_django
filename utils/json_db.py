import json
from pathlib import Path
from enum import Enum


__all__ = [
    'jdb',
]


class JsonDBKeys(Enum):
    CARD_NUMBER = 'card_number'
    CARD_OWNER = 'card_owner'


class JsonDB:
    keys = JsonDBKeys

    def __init__(
            self,
            *args,
            path: str = './json_db.json',
            encoding: str = 'utf-8',
            **kwargs
    ):
        self.path = path
        self.encoding = encoding

        p = Path(self.path)
        if p.is_file():
            with open(self.path, 'r', encoding=self.encoding) as file:
                self.db = json.load(file)
        else:
            self.db = {}
            self._write()

    def get(self, key):
        with open(self.path, 'r', encoding=self.encoding) as file:
            self.db = json.load(file)
        return self.db.get(key)

    def set(self, key, value):
        self.db[key] = value
        self._write()

    def bulk_set(self, key_values: dict):
        for k, v in key_values.items():
            self.db[k] = v
        self._write()

    def _write(self):
        with open(self.path, 'w', encoding=self.encoding) as file:
            json.dump(self.db, file, ensure_ascii=False)


jdb = JsonDB()
