from __future__ import annotations

import platform
import shutil
import sys
from pathlib import Path
from typing import Any


def _os_release() -> dict[str, str]:
    path = Path("/etc/os-release")
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        values[key] = raw_value.strip().strip('"')
    return values


def collect_diagnostics() -> dict[str, Any]:
    os_release = _os_release()
    tools = ["git", "python3", "pip3", "sha256sum", "script", "tmux"]
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "os_name": os_release.get("PRETTY_NAME", "unknown"),
        "is_kali": os_release.get("ID") == "kali" or "kali" in os_release.get("ID_LIKE", ""),
        "tools": {tool: shutil.which(tool) for tool in tools},
    }


def format_diagnostics(diagnostics: dict[str, Any]) -> str:
    lines = [
        "LabWeave doctor",
        f"Python: {diagnostics['python']}",
        f"Platform: {diagnostics['platform']}",
        f"OS: {diagnostics['os_name']}",
        f"Kali detected: {'yes' if diagnostics['is_kali'] else 'no'}",
        "",
        "Tools:",
    ]
    for tool, path in diagnostics["tools"].items():
        lines.append(f"- {tool}: {path or 'missing'}")

    if not diagnostics["is_kali"]:
        lines.extend(
            [
                "",
                "Note: this can run outside Kali for development, but it is designed for Kali terminal workflows.",
            ]
        )
    return "\n".join(lines)
