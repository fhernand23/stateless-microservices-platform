"""
CLI useradmin commands
"""
import asyncio
import uuid

import click
from hopeit.fs_storage import FileStorage
from app0.platform.auth import ContextUserInfoAuth


# from hopeit.testing.apps import config


@click.group()
def useradmin():
    pass


@useradmin.command()
@click.option('--user', prompt='User name',
              help='User name, has to be something@something like user@test.org')
@click.option('--password', prompt='password',
              help='password for the username')
@click.option('--path', default="./", help='Path for read store user data store, default "./"')
def run(user: str, password: str, path: str):
    """
    Create user or modify user password
    """
    # app_config = config(config_file)
    fs = FileStorage(path=path)
    credentials: ContextUserInfoAuth = asyncio.run(fs.get(key=user.lower(), datatype=ContextUserInfoAuth))
    if credentials is None:
        new_usr = ContextUserInfoAuth(
            id=str(uuid.uuid4()),
            user=user.lower(),
            email=user.lower(),
            password=password)
        asyncio.run(fs.store(key=user.lower(), value=new_usr))
        print(f'user {user} created')
    else:
        credentials.password = password
        asyncio.run(fs.store(key=user.lower(), value=credentials))
        print(f'user {user} updated')


cli = click.CommandCollection(sources=[useradmin])

if __name__ == '__main__':
    cli()
