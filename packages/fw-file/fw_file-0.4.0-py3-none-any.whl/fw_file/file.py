"""Common data-file interface."""
import functools
import typing as t
from abc import abstractmethod
from collections.abc import MutableMapping
from contextlib import contextmanager

from fw_meta import MetaData, MetaExtractor
from fw_utils import AnyFile, BinFile, TempFile

from .common import AttrMixin

CHUNKSIZE = 8 << 20  # 8MB


# TODO: remove type ignore when solved: https://github.com/python/mypy/issues/8539
@functools.total_ordering  # type: ignore
class File(AttrMixin, MutableMapping):  # pylint: disable=too-many-ancestors
    """Data-file base class defining the common interface for parsed files."""

    def __init__(
        self,
        file: t.Union[AnyFile, BinFile],
        extractor: t.Optional[MetaExtractor] = None,
        **_: t.Any,
    ) -> None:
        """Read the data-file - subclasses are expected to add parsing."""
        file = file if isinstance(file, BinFile) else BinFile(file)
        if not file.read(1):
            raise ValueError("Zero-byte file")
        file.seek(0)
        # NOTE using object.__setattr__ to side-step AttrMixin
        object.__setattr__(self, "file", file)
        object.__setattr__(self, "extractor", extractor or MetaExtractor())
        object.__setattr__(self, "meta_cache", None)

    @property
    def filepath(self) -> t.Optional[str]:
        """Return file path which can be a real local path or a remote one."""
        return str(self.file.metapath) if self.file.metapath else None

    @property
    @abstractmethod
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata extracted from the file."""

    def get_meta(self, cache: bool = True) -> MetaData:
        """Return the customized Flywheel metadata extracted from the file."""
        if cache and self.meta_cache is not None:
            return self.meta_cache
        meta = self.extractor.extract(self)
        object.__setattr__(self, "meta_cache", meta)
        return self.meta_cache

    @property
    def sort_key(self) -> t.Any:
        """Return sort key used for comparing/ordering instances."""
        return self.filepath  # pragma: no cover

    @contextmanager
    def open_dst(self, file: t.Optional[AnyFile]) -> t.Iterator[TempFile]:
        """Open destination file for writing using 'with'.

        Under the hood it yields a temporary file and the temp content
        will be written to the given destination file or to the
        original one when exiting from the context.
        """
        dst_file = file if file is not None else self.file.localpath
        if not dst_file:
            raise ValueError("Unspecified destination file")
        with TempFile() as tmp:
            yield tmp
            tmp.seek(0)
            self.file.close()
            with BinFile(dst_file, write=True) as dst:
                while data := tmp.read(CHUNKSIZE):
                    dst.write(data)
            object.__setattr__(self, "file", BinFile(dst_file))

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save (potentially modified) data file."""
        raise NotImplementedError  # pragma: no cover

    def close(self):
        """Close underlying file object."""
        self.file.close()

    def __eq__(self, other: object) -> bool:
        """Return that file equals other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key == other.sort_key

    def __lt__(self, other: object) -> bool:
        """Return that file is before other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key < other.sort_key

    def __enter__(self):
        """Return self for 'with' context usage (auto close underlying file)."""
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        """Close underlying file object when exiting the 'with' context."""
        self.close()

    def __repr__(self):
        """Return string representation of the data-file."""
        return f"{type(self).__name__}({self.filepath!r})"
