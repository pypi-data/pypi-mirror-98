from typing import Iterator, NamedTuple, Text


class Progress(NamedTuple):
    done: float
    total: float
    unit: Text


class Operation(NamedTuple):
    id: Text
    label: Text
    progress: Iterator[Progress]
