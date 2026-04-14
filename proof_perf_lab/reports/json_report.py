"""JSON report helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json_report(path: Path, payload: dict[str, Any]) -> None:
    """Persist a report payload to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
