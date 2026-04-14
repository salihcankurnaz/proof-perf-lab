"""Small metric helpers for reproducible benchmark runs."""

from __future__ import annotations

from statistics import mean
from time import perf_counter_ns
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def time_callable(fn: Callable[[], T], *, repeat: int) -> tuple[T, list[int]]:
    """Run a zero-argument callable multiple times and collect durations in ns."""
    durations: list[int] = []
    last_result: T | None = None
    for _ in range(repeat):
        start = perf_counter_ns()
        last_result = fn()
        durations.append(perf_counter_ns() - start)
    return last_result, durations


def summarize_ns(samples: Iterable[int]) -> dict[str, float]:
    """Summarize durations in milliseconds."""
    sample_list = list(samples)
    if not sample_list:
        return {"runs": 0.0, "mean_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
    to_ms = 1_000_000.0
    return {
        "runs": float(len(sample_list)),
        "mean_ms": mean(sample_list) / to_ms,
        "min_ms": min(sample_list) / to_ms,
        "max_ms": max(sample_list) / to_ms,
    }
