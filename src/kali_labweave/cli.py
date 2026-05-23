from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __app_name__, __version__
from .core import (
    VALID_SCOPE_KINDS,
    add_command,
    add_evidence,
    add_note,
    add_scope,
    checklist_rows,
    mark_checklist,
    status,
    timeline,
)
from .doctor import collect_diagnostics, format_diagnostics
from .report import write_report
from .storage import LabweaveError, init_project, resolve_project
from .utils import format_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="labweave",
        description="Kali terminal lab session journal.",
    )
    parser.add_argument("--project", type=Path, help="Path to an existing LabWeave project.")
    parser.add_argument("--version", action="version", version=f"{__app_name__} {__version__}")

    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init", help="Create a new lab workspace.")
    init_parser.add_argument("name", help="Project name or folder name.")
    init_parser.add_argument("--root", type=Path, help="Destination folder. Defaults to ./NAME.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite state if project already exists.")
    init_parser.set_defaults(func=handle_init)

    doctor_parser = subcommands.add_parser("doctor", help="Check Kali/Codespaces terminal readiness.")
    doctor_parser.set_defaults(func=handle_doctor)

    status_parser = subcommands.add_parser("status", help="Show project status.")
    status_parser.set_defaults(func=handle_status)

    scope_parser = subcommands.add_parser("scope", help="Manage authorized scope records.")
    scope_subcommands = scope_parser.add_subparsers(dest="scope_command", required=True)
    scope_add = scope_subcommands.add_parser("add", help="Add a scope record.")
    scope_add.add_argument("value", help="Scope value or boundary note.")
    scope_add.add_argument("--kind", choices=sorted(VALID_SCOPE_KINDS), default="note")
    scope_add.add_argument("--owner", help="Owner or authorizer.")
    scope_add.set_defaults(func=handle_scope_add)

    note_parser = subcommands.add_parser("note", help="Manage notes.")
    note_subcommands = note_parser.add_subparsers(dest="note_command", required=True)
    note_add = note_subcommands.add_parser("add", help="Add a note.")
    note_add.add_argument("text", help="Note text.")
    note_add.add_argument("--tag", action="append", default=[], help="Tag. Can be used multiple times.")
    note_add.set_defaults(func=handle_note_add)

    command_parser = subcommands.add_parser("cmd", help="Log commands without executing them.")
    command_subcommands = command_parser.add_subparsers(dest="cmd_command", required=True)
    command_add = command_subcommands.add_parser("add", help="Add a command log entry.")
    command_add.add_argument("command_text", help="Command to record.")
    command_add.add_argument("--why", help="Reason for running the command.")
    command_add.add_argument("--result", help="Short result summary.")
    command_add.set_defaults(func=handle_command_add)

    evidence_parser = subcommands.add_parser("evidence", help="Manage evidence files.")
    evidence_subcommands = evidence_parser.add_subparsers(dest="evidence_command", required=True)
    evidence_add = evidence_subcommands.add_parser("add", help="Copy evidence and record SHA-256.")
    evidence_add.add_argument("file", type=Path, help="Evidence file to copy into the project.")
    evidence_add.add_argument("--label", help="Human-readable label.")
    evidence_add.set_defaults(func=handle_evidence_add)

    checklist_parser = subcommands.add_parser("checklist", help="Manage the lab checklist.")
    checklist_subcommands = checklist_parser.add_subparsers(dest="checklist_command", required=True)
    checklist_list = checklist_subcommands.add_parser("list", help="List checklist items.")
    checklist_list.set_defaults(func=handle_checklist_list)
    checklist_done = checklist_subcommands.add_parser("done", help="Mark checklist item as done.")
    checklist_done.add_argument("item_id")
    checklist_done.set_defaults(func=handle_checklist_done)
    checklist_reset = checklist_subcommands.add_parser("reset", help="Reset checklist item.")
    checklist_reset.add_argument("item_id")
    checklist_reset.set_defaults(func=handle_checklist_reset)

    report_parser = subcommands.add_parser("report", help="Write a Markdown report.")
    report_parser.add_argument("--output", type=Path, help="Report destination path.")
    report_parser.set_defaults(func=handle_report)

    timeline_parser = subcommands.add_parser("timeline", help="Show project timeline.")
    timeline_parser.add_argument("--limit", type=int, help="Show only the newest N events.")
    timeline_parser.set_defaults(func=handle_timeline)

    return parser


def _project(args: argparse.Namespace) -> Path:
    return resolve_project(args.project)


def handle_init(args: argparse.Namespace) -> int:
    root = args.root or (Path.cwd() / args.name)
    init_project(root, args.name, force=args.force)
    print(f"created LabWeave project: {root.expanduser().resolve()}")
    print("next: cd", root)
    return 0


def handle_doctor(args: argparse.Namespace) -> int:
    print(format_diagnostics(collect_diagnostics()))
    return 0


def handle_status(args: argparse.Namespace) -> int:
    root = _project(args)
    info = status(root)
    print(f"Project: {info['project_name']}")
    print(f"Root: {root}")
    print(f"Created: {info['created_at']}")
    print(f"Updated: {info['updated_at']}")
    print(f"Scopes: {info['scope_count']}")
    print(f"Notes: {info['note_count']}")
    print(f"Commands: {info['command_count']}")
    print(f"Evidence: {info['evidence_count']}")
    print(f"Checklist: {info['checklist_done']}/{info['checklist_total']} done")
    print(f"Timeline events: {info['event_count']}")
    return 0


def handle_scope_add(args: argparse.Namespace) -> int:
    item = add_scope(_project(args), args.value, args.kind, args.owner)
    print(f"scope added: {item['id']}")
    return 0


def handle_note_add(args: argparse.Namespace) -> int:
    item = add_note(_project(args), args.text, args.tag)
    print(f"note added: {item['id']}")
    return 0


def handle_command_add(args: argparse.Namespace) -> int:
    item = add_command(_project(args), args.command_text, args.why, args.result)
    print(f"command logged: {item['id']}")
    return 0


def handle_evidence_add(args: argparse.Namespace) -> int:
    item = add_evidence(_project(args), args.file, args.label)
    print(f"evidence added: {item['id']}")
    print(f"path: {item['path']}")
    print(f"sha256: {item['sha256']}")
    return 0


def handle_checklist_list(args: argparse.Namespace) -> int:
    rows = []
    for item in checklist_rows(_project(args)):
        rows.append([item["id"], "yes" if item["done"] else "no", item["title"]])
    print(format_table(["ID", "Done", "Title"], rows))
    return 0


def handle_checklist_done(args: argparse.Namespace) -> int:
    item = mark_checklist(_project(args), args.item_id, True)
    print(f"checklist done: {item['id']}")
    return 0


def handle_checklist_reset(args: argparse.Namespace) -> int:
    item = mark_checklist(_project(args), args.item_id, False)
    print(f"checklist reset: {item['id']}")
    return 0


def handle_report(args: argparse.Namespace) -> int:
    output = write_report(_project(args), args.output)
    print(f"report written: {output}")
    return 0


def handle_timeline(args: argparse.Namespace) -> int:
    rows = []
    for item in timeline(_project(args), args.limit):
        rows.append([item["at"], item["kind"], item["message"]])
    print(format_table(["Time", "Kind", "Message"], rows))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except LabweaveError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
