"""Benchmark the regex extraction transform pair."""

from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path

from proof_perf_lab.core.metrics import summarize_ns, time_callable
from proof_perf_lab.oracles.regex_oracle import check_regex_extract_equivalence
from proof_perf_lab.reports.json_report import write_json_report
from proof_perf_lab.transforms.regex_extract import (
    extract_pairs_baseline,
    extract_pairs_optimized,
)

REPEAT = 25
LINE_COUNT = 20_000


def build_dataset(line_count: int = LINE_COUNT) -> list[str]:
    """Create a deterministic benchmark dataset."""
    return [
        f"item_{index % 97}={index} payload text and trailing noise"
        for index in range(line_count)
    ]


def run() -> dict[str, object]:
    """Run the benchmark and write a JSON report."""
    lines = build_dataset()
    if not check_regex_extract_equivalence(lines):
        raise RuntimeError("Baseline and optimized implementations diverged.")

    _, baseline_samples = time_callable(
        lambda: extract_pairs_baseline(lines),
        repeat=REPEAT,
    )
    result, optimized_samples = time_callable(
        lambda: extract_pairs_optimized(lines),
        repeat=REPEAT,
    )

    baseline_summary = summarize_ns(baseline_samples)
    optimized_summary = summarize_ns(optimized_samples)
    speedup = (
        baseline_summary["mean_ms"] / optimized_summary["mean_ms"]
        if optimized_summary["mean_ms"]
        else 0.0
    )

    payload: dict[str, object] = {
        "experiment": "regex_extract_compile_reuse",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "repeat": REPEAT,
        "line_count": LINE_COUNT,
        "correctness_check_passed": True,
        "records_emitted": len(result),
        "baseline": baseline_summary,
        "optimized": optimized_summary,
        "speedup": speedup,
    }

    report_path = Path("experiments") / "reports" / "regex_extract_report.json"
    write_json_report(report_path, payload)
    return payload


if __name__ == "__main__":
    report = run()
    print("Benchmark complete:")
    print(f"  experiment: {report['experiment']}")
    print(f"  mean baseline ms: {report['baseline']['mean_ms']:.4f}")
    print(f"  mean optimized ms: {report['optimized']['mean_ms']:.4f}")
    print(f"  speedup: {report['speedup']:.2f}x")
