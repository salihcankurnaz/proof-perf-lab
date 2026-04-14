from proof_perf_lab.oracles.regex_oracle import check_regex_extract_equivalence
from proof_perf_lab.transforms.regex_extract import (
    extract_pairs_baseline,
    extract_pairs_optimized,
)


def test_regex_extract_variants_match_on_mixed_inputs() -> None:
    lines = [
        "alpha=1 trailing data",
        "no assignment here",
        "beta_2=200 more text",
        "gamma=003",
        "bad key -= 4",
    ]
    assert extract_pairs_baseline(lines) == extract_pairs_optimized(lines)


def test_regex_extract_oracle_passes_on_generated_inputs() -> None:
    lines = [f"item_{i}= {i}" for i in range(10)]
    normalized_lines = [line.replace("= ", "=") for line in lines]
    assert check_regex_extract_equivalence(normalized_lines)
