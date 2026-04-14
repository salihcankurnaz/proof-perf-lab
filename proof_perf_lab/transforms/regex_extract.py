"""Baseline and optimized regex extraction implementations."""

from __future__ import annotations

import re
from typing import Iterable

PATTERN_TEXT = r"([A-Za-z_][A-Za-z0-9_]*)=(\d+)"
PATTERN = re.compile(PATTERN_TEXT)


def extract_pairs_baseline(lines: Iterable[str]) -> list[tuple[str, int]]:
    """Compile the regex on each iteration."""
    results: list[tuple[str, int]] = []
    for line in lines:
        match = re.compile(PATTERN_TEXT).search(line)
        if match:
            results.append((match.group(1), int(match.group(2))))
    return results


def extract_pairs_optimized(lines: Iterable[str]) -> list[tuple[str, int]]:
    """Reuse a precompiled regex."""
    results: list[tuple[str, int]] = []
    for line in lines:
        match = PATTERN.search(line)
        if match:
            results.append((match.group(1), int(match.group(2))))
    return results
