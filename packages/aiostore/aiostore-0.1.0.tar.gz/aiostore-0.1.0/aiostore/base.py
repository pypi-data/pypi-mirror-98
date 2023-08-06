from pathlib import Path
from typing import Union


class AbstractStorage:
    def __init__(
        self,
        prefix: Union[Path, str] = Path(''),
        **kwargs,
    ):
        if isinstance(prefix, str):
            prefix = Path(prefix)
        self.prefix = prefix

    def __repr__(self):
        class_name = type(self).__name__
        return f'<{class_name} prefix={self.prefix!r}>'

    async def get(self, path, **kwargs):
        raise NotImplementedError()

    async def put(self, path, string, **kwargs):
        raise NotImplementedError()

    async def load(self, path, readonly=False, **kwargs):
        raise NotImplementedError()

    async def store(self, path, stream, **kwargs):
        raise NotImplementedError()

    async def list(self, path, **kwargs):
        raise NotImplementedError()


class SimpleDirEntry:
    """Dumbed-down version of os.DirEntry"""
    __slots__ = ['name', 'path', 'is_dir', 'is_file', 'size']

    def __init__(self, name, path, is_dir=False, is_file=True, size=None):
        self.name = name
        self.path = path
        self.is_dir = is_dir
        self.is_file = is_file
        self.size = size

    def __repr__(self):
        class_name = type(self).__name__
        type_ = (self.is_file and 'f') or (self.is_dir and 'd') or '?'
        return f'<{class_name} {type_} {self.name!r} {self.size}>'

    @classmethod
    def from_dir_entry(cls, dir_entry, prefix='/'):
        return cls(
            name=dir_entry.name,
            # TODO: use pathlib paths all over?
            path=str(Path(dir_entry.path).relative_to(prefix)),
            is_dir=dir_entry.is_dir(),
            is_file=dir_entry.is_file(),
            size=dir_entry.stat().st_size,
        )
