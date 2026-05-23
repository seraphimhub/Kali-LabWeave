from __future__ import annotations

from pathlib import Path
from typing import Any

from .storage import load_state
from .utils import timestamp_slug


def _line(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def render_markdown(state: dict[str, Any]) -> str:
    checklist_done = len([item for item in state["checklist"] if item["done"]])
    checklist_total = len(state["checklist"])

    lines: list[str] = [
        f"# {state['project_name']} Lab Report",
        "",
        "## Summary",
        "",
        f"- Created: {state['created_at']}",
        f"- Updated: {state['updated_at']}",
        f"- Checklist: {checklist_done}/{checklist_total} done",
        f"- Scopes: {len(state['scopes'])}",
        f"- Notes: {len(state['notes'])}",
        f"- Commands logged: {len(state['commands'])}",
        f"- Evidence files: {len(state['evidence'])}",
        "",
        "## Scope",
        "",
    ]

    if state["scopes"]:
        for item in state["scopes"]:
            owner = f" owner={_line(item.get('owner'))}" if item.get("owner") else ""
            lines.append(f"- `{item['kind']}` {_line(item['value'])}{owner}")
    else:
        lines.append("- No scope recorded.")

    lines.extend(["", "## Notes", ""])
    if state["notes"]:
        for item in state["notes"]:
            tags = f" ({', '.join(item['tags'])})" if item.get("tags") else ""
            lines.append(f"- {item['created_at']}{tags}: {_line(item['text'])}")
    else:
        lines.append("- No notes recorded.")

    lines.extend(["", "## Command Log", ""])
    if state["commands"]:
        for item in state["commands"]:
            lines.append(f"### {item['id']}")
            lines.append("")
            lines.append(f"- Time: {item['created_at']}")
            if item.get("why"):
                lines.append(f"- Why: {_line(item['why'])}")
            if item.get("result"):
                lines.append(f"- Result: {_line(item['result'])}")
            lines.append("")
            lines.append("```bash")
            lines.append(item["command"])
            lines.append("```")
            lines.append("")
    else:
        lines.append("- No commands recorded.")

    lines.extend(["", "## Evidence", ""])
    if state["evidence"]:
        lines.append("| Label | Path | SHA-256 |")
        lines.append("| --- | --- | --- |")
        for item in state["evidence"]:
            lines.append(f"| {_line(item['label'])} | `{item['path']}` | `{item['sha256']}` |")
    else:
        lines.append("- No evidence recorded.")

    lines.extend(["", "## Checklist", ""])
    for item in state["checklist"]:
        marker = "x" if item["done"] else " "
        lines.append(f"- [{marker}] {item['title']} (`{item['id']}`)")

    lines.extend(["", "## Timeline", ""])
    for item in state["events"]:
        lines.append(f"- {item['at']} `{item['kind']}` {_line(item['message'])}")

    return "\n".join(lines).rstrip() + "\n"


def write_report(project_root: Path, output: Path | None = None) -> Path:
    state = load_state(project_root)
    if output is None:
        output = project_root / "reports" / f"lab-report-{timestamp_slug()}.md"
    else:
        output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(state), encoding="utf-8")
    return output
