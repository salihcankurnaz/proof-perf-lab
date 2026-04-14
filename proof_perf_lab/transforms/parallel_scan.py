"""Sequential and deterministic parallel scan implementations."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from typing import Iterable


def score_record(record: str) -> int:
    """Compute a deterministic score for a record."""
    total = 0
    for index, char in enumerate(record):
        total += (index + 1) * ord(char)
    return total


def scan_records_sequential(records: Iterable[str]) -> list[int]:
    """Score records in input order on a single process."""
    return [score_record(record) for record in records]


def scan_records_parallel(records: list[str], *, max_workers: int = 4) -> list[int]:
    """Score records in parallel while preserving input order."""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(score_record, records))
