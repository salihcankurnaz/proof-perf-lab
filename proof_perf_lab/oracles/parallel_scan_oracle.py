"""Correctness checks for deterministic parallel scans."""

from __future__ import annotations

from proof_perf_lab.transforms.parallel_scan import (
    scan_records_parallel,
    scan_records_sequential,
)


def check_parallel_scan_equivalence(
    records: list[str],
    *,
    max_workers: int = 4,
) -> bool:
    """Return True when sequential and parallel scans agree exactly."""
    return scan_records_sequential(records) == scan_records_parallel(
        records,
        max_workers=max_workers,
    )
