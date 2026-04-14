from proof_perf_lab.oracles.log_parse_oracle import check_log_parse_equivalence
from proof_perf_lab.transforms.log_parse import (
    parse_logs_baseline,
    parse_logs_optimized,
)


def test_log_parsers_match_on_valid_and_invalid_inputs() -> None:
    lines = [
        "ts=1700000000|level=INFO|user=user_1|action=login",
        "ts=1700000001|level=WARN|user=user_2|action=upload",
        "bad line",
        "ts=nope|level=INFO|user=user_3|action=sync",
        "ts=1700000002|level=ERROR|user=user_4|action=purchase",
    ]
    assert parse_logs_baseline(lines) == parse_logs_optimized(lines)


def test_log_parse_oracle_passes_on_generated_inputs() -> None:
    lines = [
        f"ts={1700000000 + i}|level=DEBUG|user=user_{i}|action=logout"
        for i in range(20)
    ]
    assert check_log_parse_equivalence(lines)
