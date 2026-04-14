"""Benchmark the structured log parsing transform pair."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from proof_perf_lab.core.metrics import summarize_ns, time_callable
from proof_perf_lab.oracles.log_parse_oracle import check_log_parse_equivalence
from proof_perf_lab.reports.json_report import write_json_report
from proof_perf_lab.transforms.log_parse import (
    parse_logs_baseline,
    parse_logs_optimized,
)

REPEAT = 25
LINE_COUNT = 25_000
LEVELS = ("INFO", "WARN", "ERROR", "DEBUG")
ACTIONS = ("login", "logout", "purchase", "sync", "upload")


def build_dataset(line_count: int = LINE_COUNT) -> list[str]:
    """Create a deterministic log dataset."""
    lines: list[str] = []
    for index in range(line_count):
        level = LEVELS[index % len(LEVELS)]
        action = ACTIONS[index % len(ACTIONS)]
        user = f"user_{index % 257}"
        lines.append(
            f"ts={1_700_000_000 + index}|level={level}|user={user}|action={action}"
        )
    return lines


def run() -> dict[str, object]:
    """Run the benchmark and write a JSON report."""
    lines = build_dataset()
    if not check_log_parse_equivalence(lines):
        raise RuntimeError("Baseline and optimized log parsers diverged.")

    _, baseline_samples = time_callable(
        lambda: parse_logs_baseline(lines),
        repeat=REPEAT,
    )
    result, optimized_samples = time_callable(
        lambda: parse_logs_optimized(lines),
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
        "experiment": "structured_log_parse_split_vs_regex",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "repeat": REPEAT,
        "line_count": LINE_COUNT,
        "correctness_check_passed": True,
        "records_emitted": len(result),
        "baseline": baseline_summary,
        "optimized": optimized_summary,
        "speedup": speedup,
    }

    report_path = Path("experiments") / "reports" / "log_parse_report.json"
    write_json_report(report_path, payload)
    return payload


if __name__ == "__main__":
    report = run()
    print("Benchmark complete:")
    print(f"  experiment: {report['experiment']}")
    print(f"  mean baseline ms: {report['baseline']['mean_ms']:.4f}")
    print(f"  mean optimized ms: {report['optimized']['mean_ms']:.4f}")
    print(f"  speedup: {report['speedup']:.2f}x")
