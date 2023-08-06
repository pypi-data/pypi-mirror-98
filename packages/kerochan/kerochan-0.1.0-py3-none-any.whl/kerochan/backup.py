import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import DEVNULL, PIPE, Popen
from typing import Iterator, Optional, Text

from parse import parse

from .errors import KeroError
from .structs import Progress


class KeroBackup(ABC):
    """
    Backup interface. It can basically backup a local folder into wherever
    you want. The backup is supposed to be incremental so that existing files
    don't need to be uploaded again.
    """

    SCHEME = None

    def __init__(self, target: Text, dir_format: Text = "sd_{:>05d}"):
        self.target = target
        self.dir_format = dir_format

    @staticmethod
    def from_string_id(
        string_id: Text, dir_format: Text = "sd_{:>05d}"
    ) -> "KeroBackup":
        """
        Uses the known database of backup schemes to create the instance from
        the string that comes most likely from CLI.

        Notes
        -----
        That is kinda messy because the idea is that you can potentially
        add backup classes from outside the code of this repo so it would
        mean that a register is held rather in the ImportManager just like for
        sources but I was drinking home-made vodka when I wrote this and got
        a bit carried away, so... sorry.

        Parameters
        ----------
        string_id
            String ID to create the instance for
        dir_format
            Format of directories used to determine the highest directory ID
            found on the backup medium.
        """

        try:
            scheme, target = string_id.split("://", 1)

            return {RClone.SCHEME: RClone}[scheme](target, dir_format)
        except (ValueError, KeyError):
            raise KeroError(f'Unknown backup string_id "{string_id}"')

    def string_id(self) -> Text:
        """
        Converts back to string ID
        """

        return f"{self.SCHEME}://{self.target}"

    @abstractmethod
    def highest_number(self) -> Optional[int]:
        """
        Scans the backup medium to figure out what is the highest directory ID
        there. This is done to allow numbering subsequent SD cards with
        sequential numbers.
        """

        raise NotImplementedError

    @abstractmethod
    def backup(self, root: Path):
        """
        Copies the provided directory to the backup location.

        Parameters
        ----------
        root
            Path to the directory that has to be backed up
        """

        raise NotImplementedError


class RClone(KeroBackup):
    """
    Backup using RClone.
    """

    SCHEME = "rclone"

    def highest_number(self) -> Optional[int]:
        """
        Fortunately rclone has a json output for its ls command so it's very
        easy to parse. The only problem is that it's not an iterator but I
        guess that it'll be fine for some time.

        Directory names are parsed using the dir_format specification and the
        highest found number (if any) will be reported.
        """

        candidates = []
        proc = Popen(
            [
                "rclone",
                "lsjson",
                f"{self.target}",
            ],
            stdin=DEVNULL,
            stdout=PIPE,
            stderr=PIPE,
        )

        out, err = proc.communicate()

        if proc.returncode:
            raise KeroError(f"Cannot list backup dirs: {err[:1000]}")

        dirs = json.loads(out)

        for entry in dirs:
            if entry["IsDir"]:
                path = entry["Path"]

                if p := parse(self.dir_format, path):
                    candidates.append(p[0])

        if candidates:
            return max(candidates)

    def backup(self, root: Path) -> Iterator[Progress]:
        """
        Do the backup using rclone. Most tf the logic here is just to parse
        the output of rclone and report progress correctly.
        """

        exp = re.compile(
            rb"((?P<done_num>\d+(\.\d+)?)(?P<done_unit>[PTGMk]?)) / "
            rb"((?P<total_num>\d+(\.\d+)?) (?P<total_unit>[PTGMk]?)Bytes)"
        )
        proc = Popen(
            [
                "rclone",
                "copy",
                "-P",
                "--stats-one-line",
                f"{root}",
                f"{self.target}",
            ],
            stderr=PIPE,
            stdout=PIPE,
            stdin=DEVNULL,
        )
        last_obj = None

        multiplier = {
            b"": 1024 ** 0,
            b"k": 1024 ** 1,
            b"M": 1024 ** 2,
            b"G": 1024 ** 3,
            b"T": 1024 ** 4,
            b"P": 1024 ** 5,
        }

        try:
            buf = b""

            # noinspection PyUnresolvedReferences
            while chunk := proc.stdout.read1():
                buf += chunk

                for m in exp.finditer(buf):
                    done = round(
                        float(m.group("done_num")) * multiplier[m.group("done_unit")]
                    )
                    total = round(
                        float(m.group("total_num")) * multiplier[m.group("total_unit")]
                    )

                    progress = Progress(
                        unit="byte",
                        total=total,
                        done=done,
                    )

                    yield progress
                    last_obj = progress

                    buf = buf[m.regs[0][1] :]

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
