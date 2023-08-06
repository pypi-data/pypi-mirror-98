import asyncio
from functools import partial
from tempfile import SpooledTemporaryFile
from pathlib import Path
from typing import Union

import aiofiles
import aiofiles.os
from aiofiles.threadpool import wrap as aio_wrap

from .base import AbstractStorage, SimpleDirEntry
from .eager_scandir import ResolvedDirEntry, recursive_list_files


class FilesystemStorage(AbstractStorage):
    spool_size = 1024 * 1024

    async def get(
        self, path: Union[Path, str], text: bool = True, **kwargs
    ) -> Union[str, bytes]:
        mode = 'r' if text else 'rb'
        async with aiofiles.open(self.prefix.joinpath(path), mode=mode) as f:
            return await f.read()

    async def put(
        self,
        path: Union[Path, str],
        data: Union[str, bytes],
        **kwargs,
    ) -> None:
        await self.makedirs(Path(self.prefix.joinpath(path)).parent)
        mode = 'w' if isinstance(data, str) else 'wb'
        async with aiofiles.open(self.prefix.joinpath(path), mode=mode) as f:
            await f.write(data)

    async def load(self, path, readonly=False, **kwargs):
        file = await aiofiles.open(self.prefix.joinpath(path), mode='rb')
        if readonly:
            return file

        try:
            tmp_file = aio_wrap(
                SpooledTemporaryFile(max_size=self.spool_size),
                loop=asyncio.get_event_loop(),
            )

            try:
                data = await file.read(self.spool_size)
                while data:
                    await tmp_file.write(data)
                    data = await file.read(self.spool_size)
                await tmp_file.seek(0)
            except Exception:
                await tmp_file.close()
                raise
        finally:
            file.close()
        return tmp_file

    async def store(self, path, stream, **kwargs):
        # TODO: seamlessly create parent dirs
        await self.makedirs(Path(self.prefix.joinpath(path)).parent)
        # TODO: resolve relative paths and sanity check
        async with aiofiles.open(self.prefix.joinpath(path), mode='wb') as f:
            data = await stream.read(self.spool_size)
            while data:
                await f.write(data)
                data = await stream.read(self.spool_size)

    async def list(self, path, **kwargs):
        dir_entries = await recursive_list_files(
            [
                ResolvedDirEntry(
                    name=path.rsplit('/', 1)[-1],
                    path=self.prefix.joinpath(path),
                    is_dir=True,
                )
            ],
            entry_constructor=partial(
                SimpleDirEntry.from_dir_entry, prefix=self.prefix
            ),
        )
        return dir_entries

    async def makedirs(self, path, missing=[]):
        try:
            await aiofiles.os.stat(path)
            if not missing:
                return
        except FileNotFoundError:
            return await self.makedirs(
                path.parent,
                [path.name] + missing,
            )
        for dir in missing:
            path = path.joinpath(dir)
            await aiofiles.os.mkdir(path)
