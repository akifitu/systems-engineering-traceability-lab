"""Regression tests for the portfolio roadmap command."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from se_traceability_lab.cli import run
from se_traceability_lab.roadmap import filter_projects, load_portfolio_projects, render_portfolio_roadmap


PROJECTS_FILE = ROOT / "data" / "portfolio_projects.json"


class RoadmapTests(unittest.TestCase):
    def test_portfolio_projects_load_and_sort(self) -> None:
        projects = filter_projects(load_portfolio_projects(PROJECTS_FILE))
        self.assertEqual(len(projects), 16)
        self.assertEqual(projects[0]["slug"], "traceability-lab")
        self.assertEqual(projects[1]["slug"], "verification-readiness-dashboard")
        self.assertEqual(projects[-1]["slug"], "autonomous-disaster-response-enterprise-platform")

    def test_rendered_roadmap_contains_todos(self) -> None:
        content = render_portfolio_roadmap(filter_projects(load_portfolio_projects(PROJECTS_FILE)))
        self.assertIn("## 1. Requirements Traceability Lab", content)
        self.assertIn("- [x] Implement the audit CLI and report exporter", content)
        self.assertIn("- [x] Choose a reference satellite mission and orbit", content)
        self.assertIn("Autonomous Disaster Response Enterprise Platform", content)

    def test_cli_exports_single_project_roadmap(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path(temp_dir) / "trade-study-roadmap.md"
            exit_code = run(
                [
                    "roadmap",
                    "--projects-file",
                    str(PROJECTS_FILE),
                    "--project",
                    "trade-study-engine",
                    "--export-path",
                    str(export_path),
                ]
            )
            self.assertEqual(exit_code, 0)
            self.assertTrue(export_path.exists())
            content = export_path.read_text(encoding="utf-8")
            self.assertIn("Trade Study Engine", content)
            self.assertNotIn("Satellite Power Budget Simulator", content)


if __name__ == "__main__":
    unittest.main()
