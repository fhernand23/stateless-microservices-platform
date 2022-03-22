"""
Extended Enum module
"""
import csv
import enum
from pathlib import Path
from typing import Type

from stringcase import spinalcase  # type: ignore

# module enums locations
config_path = "app0-admin/config"


class Enum(enum.Enum):
    """
    Creates an Enum class from a csv files
    """
    @classmethod
    def load_csv(cls, path: str, name: str, version: str) -> Type["Enum"]:
        """
        Loads enum class values from csv

        :param: path, str: path to folder
        :param: name, str: name of the enum, will be converted to spinal case to find the file
        :return: Enum class
        """
        path = Path(path) / (spinalcase(name) + '.csv')
        with open(path, encoding='utf8') as fb:
            reader = csv.DictReader(fb)
            data = {
                row['id']: row for row in reader
                if cls._check_version(row, version)
            }
            clazz: Type["Enum"] = cls(name, {k: k for k in data.keys()})  # type: ignore  # pylint: disable=E1121
            setattr(clazz, '_data', data)
            setattr(clazz, '_fieldnames', reader.fieldnames)
            return clazz

    def __getitem__(self, item):
        return getattr(self, '_data')[self.value][item]

    def get(self, item):
        return getattr(self, '_data')[self.value].get(item)

    @staticmethod
    def _check_version(row, version: str):
        """
        Return filtered rows by version
        """
        if version == '*':
            return True
        if 'version_from' in row:
            vfrom = row['version_from'] if row['version_from'] != '*' else '000000'
            vto = row['version_to'] if row['version_to'] != '*' else '999999'
            return vfrom <= version <= vto
        if version >= row.get("version"):
            return True
        return False

    @classmethod
    def fieldnames(cls):
        return getattr(cls, '_fieldnames')
