"""Correctness checks for the structured log parsing transform."""

from __future__ import annotations

from proof_perf_lab.transforms.log_parse import (
    parse_logs_baseline,
    parse_logs_optimized,
)


def check_log_parse_equivalence(lines: list[str]) -> bool:
    """Return True when the two parsing strategies agree exactly."""
    return parse_logs_baseline(lines) == parse_logs_optimized(lines)
