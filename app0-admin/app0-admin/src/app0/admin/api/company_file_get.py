"""
Platform Company: company-file-get
"""
import os
import re
from typing import Optional

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_extra_logger
from hopeit.dataobjects import BinaryDownload

from app0.admin.util.object_storage import ObjectStorage, ObjectStorageConf, ObjectStorageConnConfig
from app0.admin.services import ROLE_ADMIN

object_store: Optional[ObjectStorage] = None
logger, extra = app_extra_logger()

__steps__ = ['get_object']
__api__ = event_api(
    query_args=[
        ('doc_id', str, "Resource filename"),
        ('company_id', Optional[str], "Company Id (only admin)"),
    ],
    responses={
        200: (BinaryDownload, 'File contents'),
        404: (str, "File not found")
    }
)


async def __init_event__(context: EventContext):
    global object_store
    if object_store is None:
        config: ObjectStorageConnConfig = context.settings(key='data_store', datatype=ObjectStorageConnConfig)
        bucket: ObjectStorageConf = context.settings(key='company_docs', datatype=ObjectStorageConf)
        object_store = await ObjectStorage().connect(conn_config=config, bucket=bucket.bucket)


async def get_object(payload: None, context: EventContext, *, doc_id: str,
                     company_id: Optional[str] = None) -> Optional[str]:
    """
    Retrieve file
    """
    owner_id = context.auth_info['payload'].get('owner_id')
    if company_id and ROLE_ADMIN in context.auth_info['payload'].get('roles'):
        owner_id = company_id
    if _valid_file_name(doc_id):
        # filename format: company_id/filename.ext
        return f"{owner_id}/{doc_id}"
    return None


async def __postprocess__(file_name: Optional[str], context: EventContext, response: PostprocessHook) -> str:
    assert object_store
    if file_name:
        logger.info(context, f"Getting {file_name}...")
        await object_store.get_streamed_response(file_name=file_name,
                                                 context=context,
                                                 response=response)
        return "Done"
    response.status = 400
    return "Object not found"


def _valid_file_name(filename: str) -> bool:
    uuid_pattern = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
    return uuid_pattern.match(os.path.splitext(filename)[0]) is not None
