"""
Custom Enum API module
"""
from typing import Dict, Type
from dataclasses import fields, is_dataclass

from app0.app1.enums import Enum

EnumsData = Dict[str, Dict[str, Dict[str, str]]]


def enum_data(cls: Type, prefix: str = '') -> EnumsData:
    """
    Enum Data
    """
    result = {}
    if prefix:
        prefix += '.'
    for field in fields(cls):
        try:
            if issubclass(field.type, Enum):
                data = {}
                for item in field.type:
                    data[item['id']] = {k: item.get(k) for k in field.type.fieldnames()}
                result[f'{prefix}{field.name}'] = data
            elif is_dataclass(field.type):
                result.update(enum_data(field.type, prefix=prefix + field.name))
        except TypeError as e:
            print(e)
    return result
