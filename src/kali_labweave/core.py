from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .models import event
from .storage import LabweaveError, load_state, save_state
from .utils import relative_to, sha256_file, short_id, slugify, timestamp_slug, utc_now

VALID_SCOPE_KINDS = {"ip", "domain", "url", "note"}


def add_scope(project_root: Path, value: str, kind: str = "note", owner: str | None = None) -> dict[str, Any]:
    if kind not in VALID_SCOPE_KINDS:
        raise LabweaveError(f"invalid scope kind '{kind}'")

    state = load_state(project_root)
    item = {
        "id": short_id("scope"),
        "kind": kind,
        "value": value,
        "owner": owner,
        "created_at": utc_now(),
    }
    state["scopes"].append(item)
    state["events"].append(event("scope.added", f"Scope added: {value}", {"id": item["id"], "kind": kind}))
    save_state(project_root, state)
    return item


def add_note(project_root: Path, text: str, tags: list[str] | None = None) -> dict[str, Any]:
    state = load_state(project_root)
    item = {
        "id": short_id("note"),
        "text": text,
        "tags": tags or [],
        "created_at": utc_now(),
    }
    state["notes"].append(item)
    state["events"].append(event("note.added", "Note added.", {"id": item["id"], "tags": item["tags"]}))
    save_state(project_root, state)
    return item


def add_command(
    project_root: Path,
    command: str,
    why: str | None = None,
    result: str | None = None,
) -> dict[str, Any]:
    state = load_state(project_root)
    item = {
        "id": short_id("cmd"),
        "command": command,
        "why": why,
        "result": result,
        "created_at": utc_now(),
    }
    state["commands"].append(item)
    state["events"].append(event("command.logged", f"Command logged: {command}", {"id": item["id"]}))
    save_state(project_root, state)
    return item


def add_evidence(project_root: Path, source: Path, label: str | None = None) -> dict[str, Any]:
    source = source.expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise LabweaveError(f"evidence file not found: {source}")

    state = load_state(project_root)
    safe_label = slugify(label or source.stem, "evidence")
    suffix = source.suffix
    destination_name = f"{timestamp_slug()}-{safe_label}{suffix}"
    destination = project_root / "evidence" / destination_name
    destination.parent.mkdir(parents=True, exist_ok=True)

    if source == destination.resolve():
        raise LabweaveError("source evidence is already the destination file")

    shutil.copy2(source, destination)
    digest = sha256_file(destination)
    item = {
        "id": short_id("evd"),
        "label": label or source.name,
        "source": str(source),
        "path": relative_to(destination, project_root),
        "sha256": digest,
        "created_at": utc_now(),
    }
    state["evidence"].append(item)
    state["events"].append(
        event(
            "evidence.added",
            f"Evidence added: {item['label']}",
            {"id": item["id"], "path": item["path"], "sha256": digest},
        )
    )
    save_state(project_root, state)
    return item


def checklist_rows(project_root: Path) -> list[dict[str, Any]]:
    return load_state(project_root)["checklist"]


def mark_checklist(project_root: Path, item_id: str, done: bool = True) -> dict[str, Any]:
    state = load_state(project_root)
    for item in state["checklist"]:
        if item["id"] == item_id:
            item["done"] = done
            item["done_at"] = utc_now() if done else None
            state["events"].append(
                event(
                    "checklist.updated",
                    f"Checklist {'done' if done else 'reset'}: {item['title']}",
                    {"id": item_id, "done": done},
                )
            )
            save_state(project_root, state)
            return item
    raise LabweaveError(f"unknown checklist item: {item_id}")


def status(project_root: Path) -> dict[str, Any]:
    state = load_state(project_root)
    total = len(state["checklist"])
    done = len([item for item in state["checklist"] if item["done"]])
    return {
        "project_name": state["project_name"],
        "created_at": state["created_at"],
        "updated_at": state["updated_at"],
        "scope_count": len(state["scopes"]),
        "note_count": len(state["notes"]),
        "command_count": len(state["commands"]),
        "evidence_count": len(state["evidence"]),
        "checklist_done": done,
        "checklist_total": total,
        "event_count": len(state["events"]),
    }


def timeline(project_root: Path, limit: int | None = None) -> list[dict[str, Any]]:
    events = load_state(project_root)["events"]
    if limit is None:
        return events
    return events[-limit:]
