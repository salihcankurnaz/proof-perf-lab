"""Correctness checks for the regex extraction transform."""

from __future__ import annotations

from proof_perf_lab.transforms.regex_extract import (
    extract_pairs_baseline,
    extract_pairs_optimized,
)


def check_regex_extract_equivalence(lines: list[str]) -> bool:
    """Return True when baseline and optimized variants agree exactly."""
    return extract_pairs_baseline(lines) == extract_pairs_optimized(lines)
