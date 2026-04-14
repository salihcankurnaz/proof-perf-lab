# proof-perf-lab

A research platform for optimization experiments where every speedup is paired with an explicit correctness check.

## Goal

This project treats optimization as a two-part claim:

1. the optimized version is faster
2. the optimized version preserves behavior

The first version of the lab is intentionally small. It includes one benchmarkable transformation family and one explicit correctness oracle.

## Initial experiments

The lab currently includes two small experiment families:

- regex extraction
  - `baseline`: compiles the regex pattern on every call
  - `optimized`: reuses a precompiled regex

- structured log parsing
  - `baseline`: uses a regex parser
  - `optimized`: uses delimiter-aware string splitting

- deterministic parallel scan
  - `baseline`: computes a pure scoring function sequentially
  - `optimized`: computes the same scoring function in a process pool and preserves output order

These are simple but realistic examples of the type of work often done in performance engineering. Each one is paired with an explicit behavior check.

## Project layout

```text
proof-perf-lab/
  README.md
  pyproject.toml
  proof_perf_lab/
    core/
    bench/
    transforms/
    oracles/
    reports/
  experiments/
  tests/
```

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
python -m proof_perf_lab.bench.run_regex_benchmark
python -m proof_perf_lab.bench.run_log_parser_benchmark
python -m proof_perf_lab.bench.run_parallel_scan_benchmark
```

## Method

Each experiment should follow the same shape:

1. define a baseline implementation
2. define an optimized implementation
3. define a correctness oracle
4. run reproducible benchmarks
5. emit a machine-readable report

## Next milestones

1. Add property-based testing for transformation pairs.
2. Add report generation across multiple runs.
3. Add more transform families such as parsers, traversal logic, and deterministic parallelization.
