import asyncio
from functools import partial
from tempfile import SpooledTemporaryFile

import aiobotocore
import aiofiles
from aiohttp.payload import register_payload, BytesIOPayload
from aiofiles.threadpool import wrap as aio_wrap, AsyncFileIO

from . import settings
from .base import AbstractStorage

register_payload(BytesIOPayload, SpooledTemporaryFile)


@aio_wrap.register(SpooledTemporaryFile)
def _(file, *, loop=None, executor=None):
    return AsyncFileIO(file, loop, executor)


class MinioStorage(AbstractStorage):
    spool_size = 1024 * 1024

    def __init__(self, bucket, **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self._session = aiobotocore.get_session()

    @property
    def _create_client(self):
        return partial(
            self._session.create_client,
            's3',
            endpoint_url=settings.MINIO_URL,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
        )

    async def load(self, path, readonly=False):
        print('creating client')
        async with self._create_client() as client:
            print('calling minio')
            response = await client.get_object(
                Bucket=self.bucket,
                Key=self.make_path(path),
            )
            print('making tmp_file')
            tmp_file = aio_wrap(
                SpooledTemporaryFile(max_size=self.spool_size),
                loop=asyncio.get_event_loop(),
            )
            async with response['Body'] as stream:
                data = await stream.read(self.spool_size)
                while data:
                    await tmp_file.write(data)
                    data = await stream.read(self.spool_size)
        print('seeking')
        await tmp_file.seek(0)
        print('done load()')
        return tmp_file

    async def store(self, path, stream):
        # TODO: refactor
        async with self._session.create_client(
            's3',
            endpoint_url=settings.MINIO_URL,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
        ) as client:
            response = await client.put_object(
                Bucket=self.bucket,
                Key=self.make_path(path),
                Body=stream._file,
            )
            return response

    async def list(self, path):
        prefix = self.make_path(path)
        async with self._create_client() as client:
            paginator = client.get_paginator('list_objects')
            async for result in paginator.paginate(
                Bucket=self.bucket,
                Prefix=prefix,
            ):
                for c in result.get('Contents', []):
                    print(c)

    def make_path(self, path):
        return self.prefix + '/' + path

    # TODO: create_bucket() ? convenience


async def test_fetch(storage, d):
    print('fetching')
    f = await storage.load('Riksbanken_Valutafix2019.csv')
    print('reading')
    d['data'] = await f.read()
    print('closing')
    await f.close()
    print('done')


async def test_store(storage):
    async with aiofiles.open('Riksbanken_Valutafix2019_v2.csv', 'rb') as file:
        await storage.store('Riksbanken_Valutafix2019_v2.csv', file)
