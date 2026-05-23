from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import new_state
from .utils import utc_now

STATE_DIR = ".labweave"
STATE_FILE = "state.json"


class LabweaveError(RuntimeError):
    """Raised for user-facing CLI errors."""


def state_path(project_root: Path) -> Path:
    return project_root / STATE_DIR / STATE_FILE


def init_project(project_root: Path, project_name: str, force: bool = False) -> dict[str, Any]:
    project_root = project_root.expanduser().resolve()
    current_state = state_path(project_root)

    if current_state.exists() and not force:
        raise LabweaveError(f"project already exists at {project_root}")

    (project_root / STATE_DIR).mkdir(parents=True, exist_ok=True)
    (project_root / "evidence").mkdir(parents=True, exist_ok=True)
    (project_root / "notes").mkdir(parents=True, exist_ok=True)
    (project_root / "reports").mkdir(parents=True, exist_ok=True)

    notes_readme = project_root / "notes" / "README.md"
    if not notes_readme.exists():
        notes_readme.write_text(
            "# Notes\n\nCatatan manual untuk sesi lab ini.\n",
            encoding="utf-8",
        )

    state = new_state(project_name)
    save_state(project_root, state)
    return state


def find_project(start: Path | None = None) -> Path:
    cursor = (start or Path.cwd()).expanduser().resolve()
    if cursor.is_file():
        cursor = cursor.parent

    for candidate in [cursor, *cursor.parents]:
        if state_path(candidate).exists():
            return candidate

    raise LabweaveError("no LabWeave project found; run 'labweave init NAME' first")


def resolve_project(explicit: Path | None = None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        if not state_path(root).exists():
            raise LabweaveError(f"no LabWeave project found at {root}")
        return root
    return find_project()


def load_state(project_root: Path) -> dict[str, Any]:
    try:
        with state_path(project_root).open("r", encoding="utf-8") as file_obj:
            return json.load(file_obj)
    except FileNotFoundError as exc:
        raise LabweaveError(f"missing state file at {state_path(project_root)}") from exc
    except json.JSONDecodeError as exc:
        raise LabweaveError(f"state file is not valid JSON: {exc}") from exc


def save_state(project_root: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    destination = state_path(project_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file_obj:
        json.dump(state, file_obj, indent=2, sort_keys=True)
        file_obj.write("\n")
