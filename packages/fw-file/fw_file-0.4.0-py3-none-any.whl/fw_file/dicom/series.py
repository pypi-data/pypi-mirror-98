"""DICOM Series management."""
import functools
import io
import logging
import pathlib
import shutil
import tempfile
import typing as t
import zipfile
from dataclasses import dataclass

from fw_meta import MetaData
from fw_storage import StorageError
from fw_utils import AnyFile, AnyPath, BinFile
from natsort import natsorted
from pydicom.errors import InvalidDicomError

from .dicom import DICOM, TagType

__all__ = ["DICOMCollection", "DICOMSeries", "build_dicom_tree"]

log = logging.getLogger(__name__)

AnyDICOM = t.Union[AnyFile, DICOM]


class DICOMCollection(list):
    """DICOMCollection represents a list of instances."""

    def __init__(
        self,
        *files: AnyDICOM,
        instance_name_fn: t.Optional[t.Callable] = None,
        **dcm_kw: t.Any,
    ) -> None:
        """Initialize DICOMCollection.

        Args:
            *files (str|Path|file|DICOM): DICOMs to load into the collection.
            instance_name_fn (callable): Function to generate instance filenames
                with when saving to a directory/ZIP. Default: get_instance_name
            **dcm_kw: Keyword arguments to pass to DICOM when reading files.
        """

        @functools.lru_cache(maxsize=16)
        def load_path(localpath: str) -> DICOM:
            """Load a local filepath as a DICOM object (cached)."""
            return DICOM(localpath, **dcm_kw)

        super().__init__()
        self.load_path = load_path
        self.instance_name_fn = instance_name_fn or get_instance_name
        self.dirpath: t.Optional[pathlib.Path] = None  # from_dir()
        self.is_tmp = False  # from_zip()
        self.dcm_kw = dcm_kw
        for file in files:
            self.append(file)

    @classmethod
    def from_dir(
        cls,
        dirpath: AnyPath,
        pattern: str = "*",
        recurse: bool = True,
        **dcm_kw: t.Any,
    ) -> "DICOMCollection":
        """Return DICOMCollection from a directory.

        Args:
            dirpath (str|Path): Directory path to load files from.
            pattern (str, optional): Glob pattern to match files on. Default: "*".
            recurse (bool, optional): Toggle for enabling recursion. Default: True.
            **dcm_kw: Keyword arguments to initialize data-files with.
        """
        files = fileglob(dirpath, pattern=pattern, recurse=recurse)
        coll = cls(*files, **dcm_kw)
        coll.dirpath = pathlib.Path(dirpath)
        return coll

    @classmethod
    def from_zip(
        cls,
        archive: AnyPath,
        pattern: str = "*",
        recurse: bool = True,
        **dcm_kw: t.Any,
    ) -> "DICOMCollection":
        """Return DICOMCollection from a ZIP archive.

        Args:
            archive (str|Path|file): The ZIP archive path or readable to extract
                into a temporary directory and read all files from.
            pattern (str, optional): Glob pattern to match files on. Default: "*".
            recurse (bool, optional): Toggle for enabling recursion. Default: True.
            **dcm_kw: Keyword arguments to initialize data-files with.
        """
        tempdir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, mode="r") as zfile:
            zfile.extractall(tempdir)
        coll = cls.from_dir(tempdir, pattern=pattern, recurse=recurse, **dcm_kw)
        coll.is_tmp = True
        return coll

    def load_any(self, value: AnyDICOM) -> t.Union[str, DICOM]:
        """Load DICOM and return it's filepath (if available) or the instance.

        This method is intended to be used in __setitem__() and insert() to
        store only the filepath (of local files) on the collection instead of
        a reference to the DICOM instance loaded into memory, which also holds
        the file descriptor.

        Storing only the paths allows handling large DICOM series with 10K+
        instances which would otherwise be impossible due to file descriptor
        and memory limitations.

        Consequently, DICOMs need to be loaded on the fly from paths on access
        when using __getitem__() and __iter__().
        """
        if isinstance(value, DICOM):
            return value
        file = BinFile(value)
        if file.localpath:
            self.load_path(file.localpath)
            return file.localpath
        return DICOM(file, **self.dcm_kw)

    def __repr__(self) -> str:
        """Return string representation of the collection."""
        files = [
            str(file) if isinstance(file, DICOM) else f"DICOM({str(file)!r})"
            for file in super().__iter__()
        ]
        return f"[{', '.join(files)}]"

    def __contains__(self, obj: object) -> bool:
        """Return True IFF the given file is in the collection."""
        object_id = id(obj) if isinstance(obj, DICOM) else None
        localpath = obj.file.localpath if isinstance(obj, DICOM) else str(obj)
        for file in super().__iter__():  # using super for speed
            if isinstance(file, DICOM):
                if id(file) == object_id:
                    return True
                if localpath and file.file.localpath == localpath:
                    return True
            elif localpath and file == localpath:
                return True
        return False

    def __iter__(self) -> t.Iterator[DICOM]:
        """Return an iterator of DICOMs in the collection."""
        for file in super().__iter__():
            if isinstance(file, DICOM):
                yield file
            else:
                yield self.load_path(file)

    def __getitem__(self, index: int) -> DICOM:  # type: ignore[override]
        """Get a file from the collection by it's index."""
        if isinstance(index, slice):
            raise NotImplementedError("Array slices are not supported")
        value = super().__getitem__(index)
        if not isinstance(value, DICOM):
            # deferred load of local files - cache by path for speed/convenience
            value = self.load_path(value)
        return value

    def __setitem__(  # type: ignore[override]
        self, index: int, value: AnyDICOM
    ) -> None:
        """Add a file to the collection."""
        if isinstance(index, slice):
            raise NotImplementedError("Array slices are not supported")
        super().__setitem__(index, self.load_any(value))

    def insert(self, index: int, value: AnyDICOM) -> None:
        """Insert file before the given index."""
        super().insert(index, self.load_any(value))

    def append(self, value: AnyDICOM) -> None:
        """Append new file to the end of the collection."""
        self.insert(len(self), value)

    def sort(self, *, key: t.Callable = None, reverse: bool = False) -> None:
        """Sort collection in place, using DICOM.sort_key by default."""
        key = key or get_instance_sort_key
        key_idx = [(key(file), idx) for idx, file in enumerate(self)]
        old_idx = [idx for _, idx in natsorted(key_idx, reverse=reverse)]
        old_list = self.copy()
        for new, old in enumerate(old_idx):
            super().__setitem__(new, old_list[old])

    def bulk_get(self, key: TagType, default: t.Any = None) -> t.List[t.Any]:
        """Get attribute across collection."""
        return [file.get(key, default) for file in self]

    def get(self, key: str) -> t.Any:
        """Get unique attribute across collection."""
        attrs = {file.get(key) for file in self}
        if len(attrs) > 1:
            raise ValueError(f"Multiple values for {key}")
        return attrs.pop()

    def set(self, key: TagType, value: t.Any) -> None:
        """Set attribute across collection."""
        for file in self:
            file[key] = value

    def delete(self, key: TagType) -> None:
        """Delete attribute across collection."""
        for file in self:
            del file[key]

    def save(self) -> None:
        """Save files across collection to their original location."""
        for file in self:
            file.save()

    def to_dir(self, dirpath: AnyPath) -> None:
        """Save all files to the given directory.

        Args:
            dirpath (str|Path): Destination directory. Create if needed.
        """
        if isinstance(dirpath, str):
            dirpath = pathlib.Path(dirpath)
        dirpath = dirpath.resolve()
        for file in self:
            filepath = dirpath / self.instance_name_fn(file)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            file.save(filepath)

    def to_zip(
        self,
        archive: AnyPath,
        comment: t.Optional[t.AnyStr] = None,
        **zip_kw: t.Any,
    ) -> None:
        """Save all files to the given ZIP archive.

        Args:
            archive (str|Path|file): The ZIP archive path or writable to save files to.
            comment (str|bytes, optional): ZIP comments to save with. Default: None.
            **zip_kw: Additional keyword arguments to pass to zipfile.ZipFile.
        """
        zip_kw.setdefault("allowZip64", True)
        with zipfile.ZipFile(archive, mode="w", **zip_kw) as zfile:
            for file in self:
                arcname = self.instance_name_fn(file)
                content = io.BytesIO()
                file.save(content)
                zfile.writestr(arcname, content.getvalue())
            if isinstance(comment, str):
                zfile.comment = comment.encode("utf8")
            elif isinstance(comment, bytes):
                zfile.comment = comment

    def cleanup(self) -> None:
        """Remove the tempdir extracted to via 'from_zip()'."""
        if self.is_tmp and self.dirpath:
            shutil.rmtree(self.dirpath)
            self.is_tmp = False

    def __enter__(self):
        """Return self for 'with' context usage (to remove from_zip temp files)."""
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        """Remove any temp files (of from_zip) when exiting the 'with' context."""
        self.cleanup()

    def __del__(self) -> None:
        """Remove any temp files (of from_zip) when the collection is GC'd."""
        self.cleanup()


class DICOMSeries(DICOMCollection):
    """DICOMSeries represents a list of instances from the same series."""

    def __init__(
        self,
        *files: AnyDICOM,
        instance_name_fn: t.Optional[t.Callable] = None,
        series_name_fn: t.Optional[t.Callable] = None,
        validate_meta_fn: t.Optional[t.Callable] = None,
        **dcm_kw: t.Any,
    ) -> None:
        """Initialize DICOMSeries.

        Args:
            *files (str|Path|file|DICOM): DICOMs to load into the series.
            instance_name_fn (callable): Function to generate instance filenames
                with when saving to a directory/ZIP. Default: get_instance_name
            series_name_fn (callable): Function to generate the series filename
                with when getting meta or saving to a ZIP. Default: get_series_name
            validate_meta_fn (callable): Function to build and validate series
                meta with instance by instance. Default: validate_series_meta
            **dcm_kw: Keyword arguments to use when reading files.
        """
        super().__init__(*files, instance_name_fn=instance_name_fn, **dcm_kw)
        self.series_name_fn = series_name_fn or get_series_name
        self.validate_meta_fn = validate_meta_fn or validate_series_meta
        self.meta_cache = None

    def get_meta(self, cache: bool = True) -> MetaData:
        """Return the Flywheel metadata of the DICOM series."""
        if cache and self.meta_cache is not None:
            return self.meta_cache
        if not self:
            raise ValueError("No DICOMs to extract series meta from")
        meta = MetaData()
        for file in self:
            meta = self.validate_meta_fn(meta, file.get_meta(cache=cache))
        self.meta_cache = meta
        return meta

    def to_upload(
        self, dirpath: t.Optional[AnyPath] = None
    ) -> t.Tuple[pathlib.Path, MetaData]:
        """Return (filepath, metadata) tuple for the series for FW upload.

        Prepare (pack/save) the series as a single file in the given directory
        (defaults to the current working dir), and extract metadata for upload.

        If there are multiple DICOM files in the series, create a ZIP archive.
        Zipping keeps classic DICOM series together that consist of as many
        files as image slices, simplifying transfers and storage.

        If the series only contains one file, the single file is not zipped.
        Enhanced DICOMs allow encoding all instances in a single file, thus
        zipping is not necessary for keeping cohesion.
        """
        meta = self.get_meta()
        series_name = self.series_name_fn(self[0])
        if not dirpath:
            dirpath = pathlib.Path.cwd()
        elif isinstance(dirpath, str):
            dirpath = pathlib.Path(dirpath)
        if len(self) > 1:  # classic or otherwise multifile - pack
            meta["file.zip_member_count"] = len(self)
            filepath = dirpath / f"{series_name}.dicom.zip"
            self.to_zip(filepath)
        else:  # enhanced or otherwise standalone dcm - send as is
            filepath = dirpath / f"{series_name}.dcm"
            self[0].save(filepath)
        meta["file.name"] = filepath.name
        return filepath.resolve(), meta


DICOMTree = t.Dict[str, t.Dict[str, t.Dict[str, AnyPath]]]


@dataclass
class DICOMError:  # pylint: disable=too-few-public-methods
    """DICOM error class capturing any issues from build_dicom_tree."""

    __slots__ = ("file", "message")

    file: str
    message: str


def build_dicom_tree(
    files: t.Iterable[AnyPath],
    open_fn: t.Optional[t.Callable] = None,
    validate_meta_fn: t.Optional[t.Callable] = None,
    natural_sort: bool = True,
    **dcm_kw: t.Any,
) -> t.Tuple[DICOMTree, t.List[DICOMError]]:
    """Build DICOM hierarchy from DICOM files.

    Args:
        files (iterable[str|Path]): Files to place in the DICOM tree.
        open_fn (callable, optional): Function to open the files with.
            Default: BinFile (expecting files on the local filesystem).
        validate_meta_fn (callable, optional): Function to build and validate
            series meta with instance by instance. Default: validate_series_meta
        natural_sort (bool, optional): Toggle to disable natural sorting on the
            UIDs in the returned DICOM tree. Default: True.
        **dcm_kw: Keyword arguments to use when reading files.
    """
    # pylint: disable=too-many-locals
    open_file = open_fn or BinFile
    validate_meta = validate_meta_fn or validate_series_meta
    dcm_kw.setdefault("force", True)
    dcm_kw.setdefault("stop_when", "PixelData")
    tree: DICOMTree = {}
    series_to_study: t.Dict[str, str] = {}
    series_meta: t.Dict[str, t.Any] = {}
    instance_to_series: t.Dict[str, str] = {}
    errors: t.List[DICOMError] = []

    def process_dcm(file: AnyPath):
        with open_file(file) as file_obj:
            dcm = DICOM(file_obj, **dcm_kw)
            meta = dcm.get_meta()
            sort_key = dcm.sort_key
        study, series, instance = sort_key
        if not study:
            raise ValueError("Missing study key")
        if not series:
            raise ValueError("Missing series key")
        if not instance:
            raise ValueError("Missing instance key")
        series_to_study.setdefault(series, study)
        if study != series_to_study[series]:
            c_study = series_to_study[series]
            c_file = tree[c_study][series][instance]
            raise ValueError(
                f"Series {study}/{series} is already associated with "
                f"study {c_study} in file {c_file}"
            )
        if instance not in instance_to_series:
            instance_to_series[instance] = series
        else:
            c_series = instance_to_series[instance]
            c_study = series_to_study[c_series]
            c_file = tree[c_study][c_series][instance]
            raise ValueError(
                f"Instance {study}/{series}/{instance} conflicts with "
                f"instance {c_study}/{c_series}/{instance} in file {c_file}"
            )
        series_meta.setdefault(series, {})
        series_meta[series] = validate_meta(series_meta[series], meta)
        tree.setdefault(study, {})
        tree[study].setdefault(series, {})
        tree[study][series][instance] = file

    for file in files:
        try:
            process_dcm(file)
        except (
            FileNotFoundError,
            InvalidDicomError,
            PermissionError,
            StorageError,
            ValueError,
        ) as exc:
            errors.append(DICOMError(str(file), str(exc)))

    if natural_sort:
        sorted_tree: DICOMTree = {}
        for study in natsorted(tree, key=str.lower):
            sorted_tree[study] = {}
            for series in natsorted(tree[study], key=str.lower):
                sorted_tree[study][series] = {}
                for inst in natsorted(tree[study][series], key=str.lower):
                    sorted_tree[study][series][inst] = tree[study][series][inst]
        tree = sorted_tree

    return tree, errors


def fileglob(
    dirpath: AnyPath,
    pattern: str = "*",
    recurse: bool = False,
) -> t.List[pathlib.Path]:
    """Return the list of files under a given directory.

    Args:
        dirpath (str|Path): The directory path to glob in.
        pattern (str, optional): The glob pattern to match files on. Default: "*".
        recurse (bool, optional): Toggle for enabling recursion. Default: False.

    Returns:
        list[Path]: The file paths that matched the glob within the directory.
    """
    if isinstance(dirpath, str):
        dirpath = pathlib.Path(dirpath)
    glob_fn = getattr(dirpath, "rglob" if recurse else "glob")
    return list(sorted(f for f in glob_fn(pattern) if f.is_file()))


def get_instance_sort_key(dcm: DICOM) -> str:
    """Return default DICOM instance sort key."""
    return "/".join(dcm.sort_key)


def get_instance_name(dcm: DICOM) -> str:
    """Return default instance filename for a DICOM."""
    meta = dcm.get_meta()
    if meta.get("file.name"):
        return meta["file.name"]
    if dcm.filepath:
        return pathlib.Path(dcm.filepath).name
    raise ValueError("Cannot determine DICOM instance filename")


def get_series_name(dcm: DICOM) -> str:
    """Return default series filename based on a single DICOM from the series."""
    meta = dcm.get_meta()
    return meta.get("acquisition.label") or meta.get("acquisition.uid")


def validate_series_meta(
    series_meta: t.Dict[str, t.Any], dcm_meta: t.Dict[str, t.Any]
) -> MetaData:
    """Build and validate DICOM series metadata instance by instance.

    Given a (potentially empty) series meta dict and a DICOM's meta dict
     * apply every key from the DICOM to the series if it's not set yet
     * raise on any key that is present in both but has a different value
    """
    meta = series_meta or MetaData()
    for key, value in dcm_meta.items():
        if key == "file.name":
            continue  # ignore different instance file names
        if not meta.get(key):
            meta[key] = value
        elif meta[key] != value:
            raise ValueError(f"Metadata conflict on {key}: {value} != {meta[key]}")
    return meta
