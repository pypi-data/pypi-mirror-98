from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple, Optional, Sequence, Text

import inquirer
from inquirer.errors import ValidationError
from inquirer.themes import GreenPassion
from tqdm import tqdm

from kerochan.errors import KeroError
from kerochan.importing import ImportManager


class Args(NamedTuple):
    """
    Type-annotated structure to hold the CLI arguments
    """

    target: Optional[Text] = None
    backup: Sequence[Text] = []


def parse_args(argv: Optional[Sequence[Text]] = None) -> Args:
    """
    Parses arguments from CLI or from specified argv.

    Parameters
    ----------
    argv
        Overrides CLI arguments with those
    """

    parser = ArgumentParser(
        description=(
            "Incrementally copies photos from a SD card and back them up to "
            "the cloud)"
        )
    )

    parser.add_argument("-t", "--target", help="Target backup dir")
    parser.add_argument("-b", "--backup", help="Backup location", nargs="*")

    return Args(**parser.parse_args(argv).__dict__)


def make_questions(args: Args, importer: ImportManager):
    """
    Generates the questions for the inquirer library. Some CLI arguments can
    allow to skip some questions.

    Parameters
    ----------
    args
        Parsed CLI arguments
    importer
        Current instance of the importer
    """

    sources = [(s.string_id(), s.get_number()) for s in importer.auto_discover()]

    def validate_sources(answers, current):
        """
        Makes sure that there is at least one selected source
        """

        if not current:
            raise ValidationError("", reason="You must choose at last one source")

        return True

    def validate_other_source(answers, current):
        """
        If "Other" is within selected sources, it will be mandatory to provide
        a valid one, validated by the fact that the importer can make an
        instance of it.
        """

        try:
            importer.source_from_string_id(current)
        except KeroError as e:
            raise ValidationError("", reason=f"{e}")

        return True

    def validate_backup(answers, current):
        """
        Validates that a backup string can be instantiated into a real
        backup.
        """

        if not current:
            return True

        try:
            importer.backup_from_string_id(current)
        except KeroError as e:
            raise ValidationError("", reason=f"{e}")

        return True

    return [
        *(
            [
                inquirer.Path(
                    "target",
                    message="Where do you want to save your files?",
                    exists=True,
                    path_type=inquirer.Path.DIRECTORY,
                )
            ]
            if args.target is None
            else []
        ),
        inquirer.Checkbox(
            "sources",
            message="What sources do you want to import?",
            choices=[
                *[
                    (f'{name} (#{number if number is not None else "tbd"})', name)
                    for name, number in sources
                ],
                ("Other", "other"),
            ],
            default=[name for name, _ in sources],
            validate=validate_sources,
        ),
        inquirer.Text(
            "other_source",
            message="What other source do you want to use?",
            ignore=lambda answers: "other" not in answers["sources"],
            validate=validate_other_source,
        ),
        *(
            [
                inquirer.Text(
                    "backup",
                    message="Where do you want to backup (leave empty to skip)?",
                    validate=validate_backup,
                )
            ]
            if not args.backup
            else []
        ),
    ]


def main(argv: Optional[Sequence[Text]] = None):
    """
    Lots of piping done there:

    - Parsing CLI
    - Prompting remaining details via inquirer
    - Orchestrating the import and displaying progress

    Parameters
    ----------
    argv
        Optional override of CLI arguments in case by example you want to call
        this from another Python program
    """

    args = parse_args(argv)
    importer = ImportManager(Path("."))

    if args.backup:
        importer.backups = [importer.backup_from_string_id(x) for x in args.backup]

    answers = inquirer.prompt(make_questions(args, importer), theme=GreenPassion())

    if answers is None:
        return

    if args.target is None:
        importer.target = Path(answers["target"])
    else:
        importer.target = Path(args.target)

    if not args.backup:
        importer.backups = [importer.backup_from_string_id(answers["backup"])]

    for source in (
        importer.source_from_string_id(x)
        for x in [
            *(x for x in answers["sources"] if x != "other"),
            *([answers["other_source"]] if "other" in answers["sources"] else []),
        ]
    ):
        importer.activate_source(source)

    importer.ensure_ids()

    for op in importer.do_import():
        print("")
        print("")
        print(f"---> {op.label}")
        print("")

        bar = tqdm(colour="blue")

        try:
            for p in op.progress:
                bar.total = p.total
                bar.unit = p.unit

                if bar.unit == "byte":
                    bar.unit_scale = True
                    bar.unit_divisor = 1024

                bar.update(p.done - bar.n)
        finally:
            bar.close()


def __main__():
    """
    Target for Poetry script
    """

    try:
        main()
    except KeyboardInterrupt:
        print("Okay, bye")
    except SystemExit:
        pass


if __name__ == "__main__":
    __main__()
