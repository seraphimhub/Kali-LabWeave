from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kali_labweave.core import add_command, add_evidence, add_note, add_scope, mark_checklist, status
from kali_labweave.report import render_markdown, write_report
from kali_labweave.storage import init_project, load_state


class LabweaveCoreTests(unittest.TestCase):
    def test_project_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            init_project(root, "demo")

            add_scope(root, "authorized local lab", "note", "tester")
            add_note(root, "first note", ["start"])
            add_command(root, "ip addr", "record local interfaces", "ok")
            mark_checklist(root, "scope-authorized", True)

            info = status(root)
            self.assertEqual(info["scope_count"], 1)
            self.assertEqual(info["note_count"], 1)
            self.assertEqual(info["command_count"], 1)
            self.assertEqual(info["checklist_done"], 1)

    def test_evidence_is_copied_and_hashed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            source = Path(tmp) / "source.txt"
            source.write_text("hello\n", encoding="utf-8")

            init_project(root, "demo")
            item = add_evidence(root, source, "sample")

            self.assertTrue((root / item["path"]).exists())
            self.assertEqual(
                item["sha256"],
                "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03",
            )

    def test_report_contains_logged_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            init_project(root, "demo")
            add_note(root, "report note", ["report"])

            state = load_state(root)
            markdown = render_markdown(state)
            self.assertIn("# demo Lab Report", markdown)
            self.assertIn("report note", markdown)

            output = write_report(root)
            self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
