"""Benchmark the deterministic parallel scan transform pair."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from proof_perf_lab.core.metrics import summarize_ns, time_callable
from proof_perf_lab.oracles.parallel_scan_oracle import check_parallel_scan_equivalence
from proof_perf_lab.reports.json_report import write_json_report
from proof_perf_lab.transforms.parallel_scan import (
    scan_records_parallel,
    scan_records_sequential,
)

REPEAT = 8
RECORD_COUNT = 8_000
MAX_WORKERS = 4


def build_dataset(record_count: int = RECORD_COUNT) -> list[str]:
    """Create a deterministic dataset for scan benchmarks."""
    return [
        f"record:{index}:payload:{index % 97}:user_{index % 257}:action_{index % 13}"
        for index in range(record_count)
    ]


def run() -> dict[str, object]:
    """Run the benchmark and write a JSON report."""
    records = build_dataset()
    if not check_parallel_scan_equivalence(records, max_workers=MAX_WORKERS):
        raise RuntimeError("Sequential and parallel scans diverged.")

    _, baseline_samples = time_callable(
        lambda: scan_records_sequential(records),
        repeat=REPEAT,
    )
    result, optimized_samples = time_callable(
        lambda: scan_records_parallel(records, max_workers=MAX_WORKERS),
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
        "experiment": "deterministic_parallel_scan",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "repeat": REPEAT,
        "record_count": RECORD_COUNT,
        "max_workers": MAX_WORKERS,
        "correctness_check_passed": True,
        "records_emitted": len(result),
        "baseline": baseline_summary,
        "optimized": optimized_summary,
        "speedup": speedup,
    }

    report_path = Path("experiments") / "reports" / "parallel_scan_report.json"
    write_json_report(report_path, payload)
    return payload


if __name__ == "__main__":
    report = run()
    print("Benchmark complete:")
    print(f"  experiment: {report['experiment']}")
    print(f"  mean baseline ms: {report['baseline']['mean_ms']:.4f}")
    print(f"  mean optimized ms: {report['optimized']['mean_ms']:.4f}")
    print(f"  speedup: {report['speedup']:.2f}x")
