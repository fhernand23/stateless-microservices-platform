"""
Storage/persistence asynchronous stores and gets files from object storage.

"""

from typing import Optional
import aioboto3  # type: ignore
import botocore  # type: ignore
from hopeit.dataobjects import dataclass, dataobject
from hopeit.dataobjects.payload import Payload
from hopeit.app.context import EventContext, PreprocessFileHook, PostprocessHook, PostprocessStreamResponseHook

OBJECT_STORAGE_SERVICE = "s3"

__all__ = ['ObjectStorage']


@dataclass
class FileInfo:
    """
    File info
    """
    bucket: str
    file_name: str
    size: int


@dataobject
@dataclass
class ObjectStorageConf:
    bucket: str
    chunk_size: Optional[int]


@dataobject
@dataclass
class ObjectStorageConnConfig:
    aws_access_key_id: str
    aws_secret_access_key: str
    endpoint_url: str
    use_ssl: bool = False


class ObjectStorage():
    """
        Stores and retrieves dataobjects from filesystem
    """
    def __init__(self):
        """
        Stores and retrieves files from an Object Store
        This class must be initialized with the method connect
        Example:
            ```
            object_store = await ObjectStorage().connect(conn_config, bucket)
            ```
        """
        self._conn: Optional[aioboto3.Session] = None

    async def connect(self, *, conn_config: ObjectStorageConnConfig, bucket: str, create_bucket: bool = False):
        """
        Creates a ObjectStorage connection pool

        :param config: ObjectStorageConnConfig
        :param bucket: str
        """
        self._conn_config = Payload.to_obj(conn_config)
        self._bucket = bucket
        self._conn = aioboto3.Session()
        if create_bucket:
            async with self._conn.client(OBJECT_STORAGE_SERVICE, **self._conn_config) as object_store:
                try:
                    await object_store.create_bucket(Bucket=bucket)
                except botocore.exceptions.ClientError:
                    pass
        return self

    async def get_streamed_response(self,
                                    file_name: str,
                                    context: EventContext,
                                    response: PostprocessHook,
                                    content_disposition: Optional[str] = None,
                                    content_type: Optional[str] = None,
                                    chunk_size: int = 8192) -> PostprocessStreamResponseHook:
        """
        Retrieves the object from the object store bucket as PostprocessStreamResponseHook

        :param file_name: object id
        :param context: hopeit EventContext
        :param response: PostprocessHook
        :param content_disposition: Optional[str], overwrites the default = f'attachment; filename="{file_name}"'
        :param content_type: Optional[str], overwrites the default `object` content_type
        :param chunk_size: int =8192, you can overwrites
        :return PostprocessStreamResponseHook
        """
        assert self._conn
        async with self._conn.client(OBJECT_STORAGE_SERVICE, **self._conn_config) as object_store:
            assert self._bucket
            obj = await object_store.get_object(Bucket=self._bucket, Key=file_name)
            stream_response = await response.prepare_stream_response(
                context=context,
                content_disposition=content_disposition or f'attachment; filename="{file_name}"',
                content_type=content_type or obj['ContentType'],
                content_length=obj['ContentLength'])

            async with obj["Body"] as object_store_data:
                chunk = await object_store_data.read(chunk_size)
                while chunk:
                    await stream_response.write(chunk)
                    chunk = await object_store_data.read(chunk_size)
            return stream_response

    async def store_streamed_file(self, file_name: str, file_hook: PreprocessFileHook) -> Optional[FileInfo]:
        """
        Store an object in the object store bucket

        :param file_name: object id
        :param file_hook: PreprocessFileHook
        :return FileInfo
        """
        assert self._conn
        async with self._conn.client(OBJECT_STORAGE_SERVICE, **self._conn_config) as object_store:
            await object_store.upload_fileobj(file_hook, self._bucket, file_name)
        return FileInfo(self._bucket, file_name, file_hook.size)

    async def get(self, key: str, file_obj):
        """
        Download an object from S3 to a file-like object.

        :param key: object id
        :param file_obj: File like object

        The file-like object must be in binary mode.
        This is a managed transfer which will perform a multipart download in
        multiple threads if necessary.
        Usage::
            with open('filename', 'wb') as data:
                object_storage.get('mykey', data)
        """
        assert self._conn
        async with self._conn.client(OBJECT_STORAGE_SERVICE, **self._conn_config) as object_store:
            assert self._bucket
            await object_store.download_fileobj(self._bucket, key, file_obj)

    async def put(self, file_obj, key: str):
        """
        Upload a file-like object to S3.

        :param file_obj: File like object
        :param key: object id
        Usage::

        with open('filename', 'rb') as data:
            object_sotage.put(data, 'mykey')

        """
        assert self._conn
        async with self._conn.client(OBJECT_STORAGE_SERVICE, **self._conn_config) as object_store:
            assert self._bucket
            await object_store.upload_fileobj(file_obj, self._bucket, key)
