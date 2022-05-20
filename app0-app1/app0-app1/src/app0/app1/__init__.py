"""
base module
"""
import dataclasses

__all__ = ['fd']


def fd(description: str, **kwargs):
    md = kwargs.get('metadata', {})
    md['description'] = description
    kwargs['metadata'] = md
    return dataclasses.field(**kwargs)
