"""
Platform Tools: logo-get
"""
import os
import re
from typing import Optional

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_extra_logger
from hopeit.dataobjects import BinaryDownload

from app0.admin.util.object_storage import ObjectStorage, ObjectStorageConf, ObjectStorageConnConfig

object_store: Optional[ObjectStorage] = None
logger, extra = app_extra_logger()

__steps__ = ['get_object']
__api__ = event_api(
    query_args=[
        ('doc_id', str, "Resource filename")
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
        bucket: ObjectStorageConf = context.settings(key='logo_imgs', datatype=ObjectStorageConf)
        object_store = await ObjectStorage().connect(conn_config=config, bucket=bucket.bucket)


async def get_object(payload: None, context: EventContext, *, doc_id: str) -> Optional[str]:
    """
    Retrieve file
    """
    if _valid_file_name(doc_id):
        return doc_id
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
