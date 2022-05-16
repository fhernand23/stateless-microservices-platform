"""
Platform Tools: logo-upload
"""
import os
import uuid
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PreprocessHook
from hopeit.app.logger import app_extra_logger
from hopeit.dataobjects import BinaryAttachment

from app0.admin.util.object_storage import ObjectStorage, ObjectStorageConf, ObjectStorageConnConfig
from app0.admin.file import PlatformFile

logger, extra = app_extra_logger()
object_store: Optional[ObjectStorage] = None

__steps__ = ['put_object']
__api__ = event_api(
    fields=[('attachment', BinaryAttachment)],
    responses={
        200: (PlatformFile, "Uploaded file info"),
        400: (str, "Missing or invalid fields")
    }
)


async def __init_event__(context: EventContext):
    global object_store
    if object_store is None:
        config: ObjectStorageConnConfig = context.settings(key='data_store', datatype=ObjectStorageConnConfig)
        bucket: ObjectStorageConf = context.settings(key='res_images', datatype=ObjectStorageConf)
        object_store = await ObjectStorage().connect(conn_config=config, bucket=bucket.bucket)


# pylint: disable=invalid-name
async def __preprocess__(payload: None, context: EventContext,
                         request: PreprocessHook) -> Union[str, PlatformFile]:
    assert object_store
    uploaded_file: PlatformFile = None  # type: ignore
    async for file_hook in request.files():
        _, fextension = os.path.splitext(file_hook.file_name)
        file_name = f"{str(uuid.uuid4())}{fextension}"
        logger.info(context, f"Saving {file_name}...")
        file_info = await object_store.store_streamed_file(file_name=file_name, file_hook=file_hook)
        if file_info:
            uploaded_file = PlatformFile(
                file_info.bucket, file_info.file_name, file_hook.size, file_hook.file_name, file_name)
    args = await request.parsed_args()
    if not all(x in args for x in ['attachment']):
        request.status = 400
        return "Missing required fields"
    return uploaded_file


async def put_object(payload: PlatformFile, context: EventContext) -> PlatformFile:
    return payload
