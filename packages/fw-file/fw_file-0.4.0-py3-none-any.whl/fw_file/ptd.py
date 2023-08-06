"""Reading and writing Siemens RAW PET - aka. PTD - data (.ptd files)."""
import io
import struct
import typing as t

from fw_utils import AnyFile, BinFile

from .dicom.dicom import DICOM, TagType
from .file import File

MAGIC_STR = b"LARGE_PET_LM_RAWDATA"
MAGIC_LEN = len(MAGIC_STR)
INT_SIZE = struct.calcsize("i")


class PTD(File):  # pylint: disable=too-many-ancestors
    """PTD data-file class.

    Siemens RAW PET files are usually named with the extension ".ptd".
    PTD is a proprietary file format which has an embedded DICOM dataset:
        <PTD PREAMBLE> <DICOM DATASET> <DICOM SIZE> <MAGIC BYTES>
    This parser peels the wrapping bytes and exposes the embedded DICOM.
    """

    def __init__(self, file: t.Union[AnyFile, BinFile], **kwargs: t.Any) -> None:
        """Initialize a PTD file by extracting the embedded DICOM.

        Args:
            file (str|Path|file): The file to read from as a string (filepath),
                Path or file-like object. Files opened from str and Path objects
                are automatically closed after reading. The caller is
                responsible for closing file-like objects.
            kwargs: Extra keyword args to pass to `fw_file.dicom.dicom.DICOM`.
        """
        super().__init__(file)
        # verify PTD magic bytes at the end of the file
        self.file.seek(-MAGIC_LEN, 2)
        magic_str = self.file.read(MAGIC_LEN)
        if magic_str != MAGIC_STR:
            msg = "Invalid PTD magic bytes: {!r} (expected {!r})"
            raise ValueError(msg.format(magic_str, MAGIC_STR))

        # calculate the PTD preamble size
        self.file.seek(-INT_SIZE - MAGIC_LEN, 2)
        dcm_size = struct.unpack("i", self.file.read(INT_SIZE))[0]
        dcm_offset = dcm_size + INT_SIZE + MAGIC_LEN
        ptd_size = self.file.seek(0, 2) - dcm_offset

        # store the proprietary PTD preamble data as bytes
        self.file.seek(0)
        object.__setattr__(self, "preamble", self.file.read(ptd_size))

        # store the DICOM parsed
        dcm_buffer = io.BytesIO(self.file.read(dcm_size))
        object.__setattr__(self, "dcm", DICOM(dcm_buffer, **kwargs))

    def __getitem__(self, key: TagType) -> t.Any:
        """Get dataelement value by tag/keyword."""
        return self.dcm[key]

    def __setitem__(self, key: TagType, value: t.Any) -> None:
        """Set dataelement value by tag/keyword."""
        self.dcm[key] = value

    def __delitem__(self, key: TagType) -> None:
        """Delete a dataelement by tag/keyword."""
        del self.dcm[key]

    def __iter__(self):
        """Return dataelement iterator."""
        return iter(self.dcm)

    def __len__(self) -> int:
        """Return the number of elements in the dataset."""
        return len(self.dcm)

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata extracted from the PTD."""
        meta = self.dcm.default_meta
        meta["file.type"] = "ptd"  # TODO cross-check with core's filetypes
        meta["file.name"] = meta["file.name"].replace(".dcm", ".ptd")
        return meta

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save PTD file."""
        with self.open_dst(file) as wfile:
            wfile.write(self.preamble)
            self.dcm.save(wfile)
            wfile.seek(0, 2)
            dcm_size = wfile.tell() - len(self.preamble)
            wfile.write(struct.pack("i", dcm_size))
            wfile.write(MAGIC_STR)
