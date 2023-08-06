import asyncio
import os
from functools import partial
from operator import attrgetter


class ResolvedDirEntry:
    __slots__ = [
        'name', 'path', 'inode', 'is_dir', 'is_file', 'is_symlink', 'stat'
    ]

    def __init__(
        self, name, path, inode=None, is_dir=None, is_file=None,
        is_symlink=None, stat=None,
    ):
        self.name = name
        self.path = path
        self.inode = inode
        self.is_dir = is_dir
        self.is_file = is_file
        self.is_symlink = is_symlink
        self.stat = stat

    def __repr__(self):
        class_name = type(self).__name__
        type_ = (self.is_file and 'f') or (self.is_dir and 'd') or '?'
        return f'<{class_name} {type_} {self.name!r}>'

    @classmethod
    def from_dir_entry(cls, dir_entry):
        return cls(
            name=dir_entry.name,
            path=dir_entry.path,
            inode=dir_entry.inode(),
            is_dir=dir_entry.is_dir(),
            is_file=dir_entry.is_file(),
            is_symlink=dir_entry.is_symlink(),
            stat=dir_entry.stat(),
        )


def resolve_scandir(
    path=None,
    best_effort=True,
    entry_constructor=ResolvedDirEntry.from_dir_entry,
):
    def _resolve(e):
        try:
            return entry_constructor(e)
        except OSError:
            if not best_effort:
                raise
    return tuple(
        resolved
        for resolved in (
            _resolve(dir_entry)
            for dir_entry in os.scandir(path)
        )
        if resolved
    )


async def eager_scandir(
    path=None,
    executor=None,
    entry_constructor=ResolvedDirEntry.from_dir_entry,
):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        executor,
        partial(resolve_scandir, path=path, entry_constructor=entry_constructor),
    )


def filter_visible(resolved_entries):
    return filter(
        lambda rde: not rde.name.startswith('.'),
        resolved_entries
    )


def filter_directories(resolved_entries, hidden=False):
    filtered = filter(attrgetter('is_dir'), resolved_entries)
    if not hidden:
        filtered = filter_visible(filtered)
    return filtered


def split_dirs(entries):
    dirs = []
    files = []
    for entry in filter_visible(entries):
        if entry.is_file:
            files.append(entry)
        elif entry.is_dir:
            dirs.append(entry)
    return dirs, files


async def traverse_tree(entries, parent=None):
    dirs, files = split_dirs(entries)
    next_level = await asyncio.gather(
        *[
            traverse_tree(subdirs)
            for subdirs in await asyncio.gather(
                *(eager_scandir(d.path) for d in dirs)
            )
        ]
    )
    level = {
        file.name: file
        for file in files
    }
    level.update({
        dir.name: subdir
        for dir, subdir in zip(dirs, next_level)
    })
    return level


async def recursive_list_files(
    entries,
    entry_constructor=ResolvedDirEntry.from_dir_entry,
):
    dirs, files = split_dirs(entries)
    next_level = await asyncio.gather(
        *[
            recursive_list_files(subdirs, entry_constructor=entry_constructor)
            for subdirs in await asyncio.gather(
                *(
                    eager_scandir(d.path, entry_constructor=entry_constructor)
                    for d in dirs
                )
            )
        ]
    )
    for subdir, subfiles in zip(dirs, next_level):
        files.extend(subfiles)
    return files
