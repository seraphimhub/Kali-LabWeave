from __future__ import annotations

import json
from importlib import resources
from typing import Any

from .utils import utc_now


def default_checklist() -> list[dict[str, Any]]:
    checklist_path = resources.files("kali_labweave").joinpath("data/checklists.json")
    with checklist_path.open("r", encoding="utf-8") as file_obj:
        items = json.load(file_obj)

    now = utc_now()
    return [
        {
            "id": item["id"],
            "title": item["title"],
            "done": False,
            "created_at": now,
            "done_at": None,
        }
        for item in items
    ]


def new_state(project_name: str) -> dict[str, Any]:
    now = utc_now()
    return {
        "version": 1,
        "project_name": project_name,
        "created_at": now,
        "updated_at": now,
        "scopes": [],
        "notes": [],
        "commands": [],
        "evidence": [],
        "checklist": default_checklist(),
        "events": [
            {
                "at": now,
                "kind": "project.created",
                "message": f"Project {project_name} created.",
                "detail": {},
            }
        ],
    }


def event(kind: str, message: str, detail: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "at": utc_now(),
        "kind": kind,
        "message": message,
        "detail": detail or {},
    }
