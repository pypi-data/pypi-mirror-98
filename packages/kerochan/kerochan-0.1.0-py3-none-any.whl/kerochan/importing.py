from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence, Text, Type

from parse import parse

from .backup import KeroBackup
from .errors import KeroError
from .sources import KeroSource, LocalSource
from .structs import Operation


class ImportManager:
    """
    Manages the import process as well as the source/backup instance creation.
    That's a bit the masterclass.
    """

    def __init__(
        self,
        target: Path,
        sources: Optional[Dict[Text, Type["KeroSource"]]] = None,
        prevent_default_sources: bool = False,
        dir_format: Text = "sd_{:>05d}",
        backups: Optional[Sequence[KeroBackup]] = None,
    ):
        """
        Constructor

        Parameters
        ----------
        target
            Local target to save files on disk
        sources
            Source classes that can provide sources
        prevent_default_sources
            Prevent default source classes to be inserted automatically
        dir_format
            Format of the directories that will be created inside the target
        backups
            Backup instances (yeah doesn't make sense to have classes of
            sources and backup instances directly but I was drunk okay I'll
            fix it)
        """

        self.sources: Dict[Text, Type["KeroSource"]] = (
            {
                "local": LocalSource,
            }
            if not prevent_default_sources
            else {}
        )
        self.active_sources: List["KeroSource"] = []
        self.target = target
        self.dir_format = dir_format
        self.backups: Sequence[KeroBackup] = backups or []

        if sources:
            self.sources.update(sources)

    def auto_discover(self) -> Iterator["KeroSource"]:
        """
        Let each source class auto-discover the potential instances that there
        is. This allows by example to scan for all drives and detect which ones
        look like they are a camera SD card.
        """

        for source in self.sources.values():
            yield from source.auto_discover()

    def source_from_string_id(self, string_id: Text) -> "KeroSource":
        """
        Makes the source instance from the string_id according to the local
        DB of source classes.

        Parameters
        ----------
        string_id
            String ID to turn into an instance
        """

        try:
            scheme, _ = string_id.split("://", 1)

            return self.sources[scheme].from_string_id(string_id)
        except (ValueError, KeyError):
            raise KeroError(f'Unknown source "{string_id}"')

    def backup_from_string_id(self, string_id: Text) -> "KeroBackup":
        """
        Creates the backup instance from the string ID

        Parameters
        ----------
        string_id
            String ID to create an instance from
        """

        return KeroBackup.from_string_id(string_id, self.dir_format)

    def activate_source(self, source: "KeroSource"):
        """
        Adds a source to the list of active sources for this import

        Parameters
        ----------
        source
            Source instance to activate
        """

        self.active_sources.append(source)

    def parse_dir(self, name: Text) -> Optional[int]:
        """
        Parses a directory name to check if it could be a storage directory
        that matches the dir_format. If so, the encoded ID will be returned
        and otherwise None will be returned.

        Parameters
        ----------
        name
            Directory name
        """

        if p := parse(self.dir_format, name):
            return p[0]

    def source_dir(self, source: "KeroSource") -> Path:
        """
        For a given source, computes the path where to save it on the local
        drive. This won't work if the source doesn't have an assigned ID yet.

        Parameters
        ----------
        source
            Source for which you want the target storage path
        """

        return self.target / self.dir_format.format(source.get_number())

    def highest_number(self) -> int:
        """
        Guesses the highest source ID from:

        - Backups
        - Sources
        - Local storage

        This allows to attribute new incremental IDs to new SD cards.
        """

        candidates = []

        for source in self.active_sources:
            if (num := source.get_number()) and num is not None:
                candidates.append(num)

        for child in self.target.iterdir():
            try:
                if child.is_dir():
                    if (num := self.parse_dir(child.name)) and num is not None:
                        candidates.append(num)
            except PermissionError:
                pass

        for backup in self.backups:
            if (num := backup.highest_number()) and num is not None:
                candidates.append(num)

        if candidates:
            return max(candidates)

        return 0

    def ensure_ids(self):
        """
        Ensures that all sources have a designated ID. If they do not have it,
        an incremental ID will be given according to the highest number found.
        """

        next_id = self.highest_number() + 1

        for source in self.active_sources:
            num = source.get_number()

            if num is None:
                source.set_number(next_id)
                next_id += 1

    def do_import(self) -> Iterator[Operation]:
        """
        Copy all the sources locally and then back them up to all backups.
        You have to call ensure_ids() before calling this.
        """

        for source in self.active_sources:
            dest = self.source_dir(source)

            try:
                dest.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                raise KeroError(f'Permission missing to create target dir "{dest}"')
            except FileExistsError:
                raise KeroError(f'Target dir "{dest}" is actually a file')

            yield Operation(
                id="local_save",
                label=f'Saving files locally from "{source.string_id()}"',
                progress=source.copy_to(dest),
            )

        for backup in self.backups:
            yield Operation(
                id="backup",
                label=f'Backing-up to "{backup.string_id()}"',
                progress=backup.backup(self.target),
            )
