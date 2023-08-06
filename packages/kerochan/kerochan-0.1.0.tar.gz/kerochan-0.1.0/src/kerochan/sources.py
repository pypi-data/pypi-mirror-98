import re
from abc import ABC, abstractmethod
from os.path import sep
from pathlib import Path
from subprocess import DEVNULL, PIPE, Popen
from typing import Iterator, Optional, Text

from psutil import disk_partitions

from .errors import KeroError
from .structs import Progress


class KeroSource(ABC):
    """
    Interface for Kero sources. They allow to retrieve files from SD cards but
    also to keep track of which source has which ID. And finally, sources can
    be auto-discovered to some extent.
    """

    @classmethod
    @abstractmethod
    def auto_discover(cls) -> Iterator["KeroSource"]:
        """
        Scans the system or whatever you'd like to figure what are the
        potential sources for this class.
        """

        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_string_id(cls, string_id: Text) -> "KeroSource":
        """
        Creates an instance from the string ID.

        Parameters
        ----------
        string_id
            String ID you want to instantiate
        """

        raise NotImplementedError

    @abstractmethod
    def string_id(self) -> Text:
        """
        Generates the string ID for this instance.
        """

        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}({self.string_id()!r})"

    @abstractmethod
    def get_number(self) -> Optional[int]:
        """
        Reads the ID number of that source. If not written yet, None is
        returned.
        """

        raise NotImplementedError

    @abstractmethod
    def set_number(self, number: int) -> None:
        """
        Sets the ID number for that source.

        Parameters
        ----------
        number
            Number to set
        """

        raise NotImplementedError

    @abstractmethod
    def copy_to(self, path: Path) -> Iterator[Progress]:
        """
        Copies the files from that source to the given local directory.

        Parameters
        ----------
        path
            Local path where to copy the files. It must already exist.
        """

        raise NotImplementedError


class LocalSource(KeroSource):
    SD_ID_FILE = "sd_card_id.txt"
    PREFIX = "local://"

    def __init__(self, root: Path):
        self.root = root

    @classmethod
    def from_string_id(cls, string_id: Text) -> "KeroSource":
        if not string_id.startswith(cls.PREFIX):
            raise KeroError(f'Path "{string_id}" not prefixed with "{cls.PREFIX}"')

        return LocalSource(Path(string_id[len(cls.PREFIX) :]))

    def string_id(self) -> Text:
        return f"{self.PREFIX}{self.root}"

    @classmethod
    def auto_discover(cls) -> Iterator["KeroSource"]:
        for part in disk_partitions():
            path = Path(part.mountpoint)

            try:
                is_camera = (
                    (path / cls.SD_ID_FILE).is_file()
                    or (path / "DCIM").is_dir()
                    or (path / "AVF_INFO").is_dir()
                )

                if is_camera:
                    yield cls(root=path)
            except PermissionError:
                pass

    @property
    def id_file(self) -> Path:
        return self.root / self.SD_ID_FILE

    def get_number(self) -> Optional[int]:
        if self.id_file.exists():
            try:
                with open(self.id_file, encoding="utf-8") as f:
                    return int(f.read().strip())
            except ValueError:
                return None

    def set_number(self, number: int) -> None:
        with open(self.id_file, "w", encoding="utf-8") as f:
            f.write(f"{number}")

    def copy_to(self, path: Path) -> Iterator[Progress]:
        exp = re.compile(
            rb" \(xfr#(?P<transfer>\d+), to-chk=(?P<to_check>\d+)/(?P<total>\d+)\)"
        )
        proc = Popen(
            [
                "rsync",
                "--block-size=131072",
                "-aP",
                f"{self.root.resolve()}{sep}",
                f"{path.resolve()}{sep}",
            ],
            stderr=PIPE,
            stdout=PIPE,
            stdin=DEVNULL,
        )
        last_obj = None

        try:
            while chunk := proc.stdout.readline():
                for m in exp.finditer(chunk):
                    total = float(m.group("total"))
                    to_check = float(m.group("to_check"))

                    progress = Progress(
                        unit="file", total=total, done=(total - to_check - 1)
                    )

                    if progress != last_obj:
                        yield progress
                        last_obj = progress

            proc.wait()

            if proc.returncode:
                raise KeroError(
                    f'Could not copy: {proc.stderr.read(1000).decode("utf-8")}'
                )

            if last_obj:
                yield last_obj._replace(done=last_obj.total)
        finally:
            # noinspection PyBroadException
            try:
                proc.kill()
            except Exception:
                pass
