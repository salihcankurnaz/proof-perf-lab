from proof_perf_lab.oracles.parallel_scan_oracle import check_parallel_scan_equivalence
from proof_perf_lab.transforms.parallel_scan import (
    scan_records_parallel,
    scan_records_sequential,
)


def test_parallel_scan_matches_sequential_output() -> None:
    records = [
        "record:1:payload:5:user_1:action_1",
        "record:2:payload:8:user_2:action_2",
        "record:3:payload:13:user_3:action_3",
    ]
    assert scan_records_sequential(records) == scan_records_parallel(
        records,
        max_workers=2,
    )


def test_parallel_scan_oracle_passes_on_generated_inputs() -> None:
    records = [
        f"record:{i}:payload:{i % 17}:user_{i % 11}:action_{i % 5}"
        for i in range(32)
    ]
    assert check_parallel_scan_equivalence(records, max_workers=2)
