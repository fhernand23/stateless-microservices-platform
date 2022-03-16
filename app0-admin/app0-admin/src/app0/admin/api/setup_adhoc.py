"""
Platform Setup: setup-adhoc
"""
import os
from io import BytesIO
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.fs_storage import FileStorage

from app0.admin.db import db
from app0.admin.http import Dto, HttpRespInfo
from app0.admin.mail.test_sender import (send_test_html_email,
                                          send_test_multipart_email,
                                          send_test_plain_email)
from app0.admin.services.user_services import get_users
from app0.platform.auth import UserPassword, _password_hash
from app0.admin.util.object_storage import ObjectStorage, ObjectStorageConf, ObjectStorageConnConfig


logger = app_logger()
fs_auth: Optional[FileStorage] = None
object_store: Optional[ObjectStorage] = None

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('code', str, "Setup Code")
    ],
    responses={
        200: (Dto, "OK"),
        400: (str, "Bad request"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def __init_event__(context: EventContext):
    global fs_auth
    if fs_auth is None:
        fs_auth = FileStorage(path=str(context.env['fs']['auth_store']))

    global object_store
    if object_store is None:
        config: ObjectStorageConnConfig = context.settings(key='data_store', datatype=ObjectStorageConnConfig)
        bucket: ObjectStorageConf = context.settings(key='claims-testing', datatype=ObjectStorageConf)
        object_store = await ObjectStorage().connect(conn_config=config, bucket=bucket.bucket)


async def run(payload: None, context: EventContext, code: str) -> Union[Dto, HttpRespInfo]:
    """
    Setup AdHoc
    """
    # check if empty
    if code == 'FORCE':
        es = db(context.env)
        # get list of users
        users = await get_users(es)
        def_passwd = "123"
        for usr in users:
            await _register(usr.username, def_passwd)
            print(f"password hashed: {usr.username}")
    elif code == 'TEST_MAIL':
        send_test_plain_email()
    elif code == 'TEST_HTML_MAIL':
        send_test_html_email()
    elif code == 'TEST_ATT_FILE':
        await _send_test_att_email('FILE', context)
    elif code == 'TEST_ATT_S3':
        await _send_test_att_email('S3', context)

    return Dto(o={'msg': 'OK Run'})


async def __postprocess__(payload: Union[Dto, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[Dto, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _register(username: str, password: str) -> bool:
    """
    Register User and password
    """
    if fs_auth is None:
        return False
    auth_info = await fs_auth.get(key=username, datatype=UserPassword)

    if auth_info is not None:
        # exists user
        return False

    # register password
    await fs_auth.store(key=username, value=_password_hash(password))  # Improve process
    return True


async def _send_test_att_email(file_src: str, context: EventContext):
    """
    Sent test email
    """
    assert object_store
    subject = "mail with attachment from Claims Attendant"
    to = ["devmaster@claimsattendant.com"]
    content = """
        <html>
            <head></head>
            <h1 style='text-align:center'>Hello! This is the heading</h1>
            <p>This is an html mail with attachment from Claims Platform.</p>
            </body>
        </html>
    """
    attachments: dict[str, Union[BytesIO, bytes]] = {}

    if file_src == 'S3':
        # from file like attachment
        file0_name = "test.txt"
        file0 = b'Hello World\n'
        attachments[file0_name] = file0

        file1_name = "test_objectstore.txt"
        file1 = BytesIO()
        file1.write(b'Hello Object Store World\n')
        file1.seek(0)
        # Put to object store
        await object_store.put(file1, file1_name)
        # Get from object Store
        file_obj = BytesIO()
        await object_store.get(file1_name, file_obj)
        attachments[file1_name] = file_obj

    if file_src == 'FILE':
        file_name = "test_document.pdf"
        file_path = os.path.join("./email", file_name)
        with open(file_path, "rb") as attachment:
            attachments[file_name] = attachment.read()

    await send_test_multipart_email(to, subject, content, attachments)
