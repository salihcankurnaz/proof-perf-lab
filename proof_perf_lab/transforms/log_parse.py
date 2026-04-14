"""Baseline and optimized structured log parsers."""

from __future__ import annotations

import re
from typing import Iterable

LOG_PATTERN = re.compile(
    r"ts=(?P<ts>\d+)\|level=(?P<level>[A-Z]+)\|user=(?P<user>[A-Za-z0-9_]+)\|action=(?P<action>[a-z_]+)"
)


def parse_logs_baseline(lines: Iterable[str]) -> list[dict[str, str | int]]:
    """Parse logs with regex matching."""
    rows: list[dict[str, str | int]] = []
    for line in lines:
        match = LOG_PATTERN.fullmatch(line)
        if not match:
            continue
        rows.append(
            {
                "ts": int(match.group("ts")),
                "level": match.group("level"),
                "user": match.group("user"),
                "action": match.group("action"),
            }
        )
    return rows


def parse_logs_optimized(lines: Iterable[str]) -> list[dict[str, str | int]]:
    """Parse logs with fixed-delimiter splitting."""
    rows: list[dict[str, str | int]] = []
    for line in lines:
        parts = line.split("|")
        if len(parts) != 4:
            continue
        values: dict[str, str] = {}
        valid = True
        for part in parts:
            if "=" not in part:
                valid = False
                break
            key, value = part.split("=", 1)
            values[key] = value
        if not valid:
            continue
        required = {"ts", "level", "user", "action"}
        if set(values) != required:
            continue
        if not values["ts"].isdigit():
            continue
        rows.append(
            {
                "ts": int(values["ts"]),
                "level": values["level"],
                "user": values["user"],
                "action": values["action"],
            }
        )
    return rows
