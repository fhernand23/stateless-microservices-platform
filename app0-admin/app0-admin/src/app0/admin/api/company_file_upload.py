"""
Platform Company: company-file-upload
"""
import os
import uuid
from typing import Optional, Union
from bson.objectid import ObjectId  # type: ignore

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PreprocessHook
from hopeit.app.logger import app_extra_logger
from hopeit.dataobjects import BinaryAttachment
from hopeit.dataobjects.payload import Payload

from app0.admin.util.object_storage import ObjectStorage, ObjectStorageConf, ObjectStorageConnConfig
from app0.admin.util.company_util import get_file_description, get_file_field_date_resource
from app0.admin.db import db
from app0.admin.file import PlatformFile
from app0.admin.http import HttpRespInfo
from app0.admin.notification import Notification
from app0.admin.company import CompanyConfig
from app0.admin.services.notification_services import save_notification
from app0.admin.services import IDX_COMPANY_CONFIG, ROLE_ADMIN
from app0.admin.util import company_util

logger, extra = app_extra_logger()
object_store: Optional[ObjectStorage] = None

__steps__ = ['put_object']
__api__ = event_api(
    query_args=[
        ('company_id', Optional[str], "Company id"),
        ('tag', Optional[str], "Tag"),
    ],
    fields=[('attachment', BinaryAttachment)],
    responses={
        200: (Notification, "Uploaded file info embedded in notification"),
        400: (HttpRespInfo, "Missing or invalid fields")
    }
)


async def __init_event__(context: EventContext):
    global object_store
    if object_store is None:
        config: ObjectStorageConnConfig = context.settings(key='data_store', datatype=ObjectStorageConnConfig)
        bucket: ObjectStorageConf = context.settings(key='company_docs', datatype=ObjectStorageConf)
        object_store = await ObjectStorage().connect(conn_config=config, bucket=bucket.bucket)


# pylint: disable=invalid-name
async def __preprocess__(payload: None, context: EventContext, request: PreprocessHook, *,
                         company_id: Optional[str], tag: Optional[str] = None) -> Union[str, PlatformFile]:
    assert object_store
    uploaded_file: PlatformFile = None  # type: ignore

    owner_id = context.auth_info['payload'].get('owner_id')
    if company_id and ROLE_ADMIN in context.auth_info['payload'].get('roles'):
        owner_id = company_id

    async for file_hook in request.files():
        _, fextension = os.path.splitext(file_hook.file_name)
        # filename format: company_id/filename.ext
        file_name = f"{str(uuid.uuid4())}{fextension}"
        object_id = f"{owner_id}/{file_name}"
        logger.info(context, f"Saving {file_name}...")
        file_info = await object_store.store_streamed_file(file_name=object_id, file_hook=file_hook)
        if file_info:
            uploaded_file = PlatformFile(
                bucket=file_info.bucket,
                filename=file_name,
                size=file_hook.size,
                src_filename=file_hook.file_name,
                object_id=object_id)
    args = await request.parsed_args()
    if not all(x in args for x in ['attachment']):
        request.status = 400
        return "Missing required fields"
    return uploaded_file


async def put_object(payload: PlatformFile, context: EventContext, *,
                     company_id: Optional[str], tag: Optional[str] = None) -> Union[Notification, HttpRespInfo]:
    """
    Upload file and create notification
    """
    logger.info(context, "File uploaded...", extra=extra(file_id=payload.filename, size=payload.size))

    owner_id = context.auth_info['payload'].get('owner_id')
    if company_id and ROLE_ADMIN in context.auth_info['payload'].get('roles'):
        owner_id = company_id
    # agregar el log
    content = f"File uploaded {get_file_description(tag)}"
    assert payload.creation_date
    new_log = Notification(creation_date=payload.creation_date,
                           type=company_util.TYPE_UPLOAD,
                           user_id=context.auth_info['payload'].get('user'),
                           user_name=context.auth_info['payload'].get('fullname'),
                           owner_id=owner_id,
                           owner_name=context.auth_info['payload'].get('owner_name'),
                           content=content,
                           file_resource=payload,
                           app_name=company_util.APP_ATTENDANT,
                           object_type=company_util.OBJECT_COMPANY,
                           object_id=owner_id,
                           tags=tag if tag else "")
    es = db(context.env)
    await save_notification(es, new_log)
    # guarda log
    logger.info(context, f"Added File Notificacion {new_log}")
    # update field in company config
    await _update_company_config(es, owner_id, tag, payload)  # type: ignore

    return new_log


async def _update_company_config(es, company_id: str, tag: str, platform_file: PlatformFile):
    """
    Update company config
    """
    # get company config id
    doc = await es[IDX_COMPANY_CONFIG].find_one({'owner_id': {'$eq': company_id}})
    if doc:
        company_config = Payload.from_obj(doc, CompanyConfig)
        field_date, field_resource = get_file_field_date_resource(tag)
        assert platform_file.creation_date
        if field_date and field_resource:
            await es[IDX_COMPANY_CONFIG].update_one({'_id': ObjectId(company_config.id)},
                                                    {'$set': {field_date: platform_file.creation_date.isoformat(),
                                                              field_resource: Payload.to_obj(platform_file)}})
