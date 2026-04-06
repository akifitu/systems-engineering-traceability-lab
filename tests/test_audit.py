"""Regression tests for the Systems Engineering Traceability Lab."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from se_traceability_lab.audit import audit_artifacts
from se_traceability_lab.cli import run
from se_traceability_lab.data import load_artifacts


DATA_DIR = ROOT / "data"


class AuditTests(unittest.TestCase):
    def test_clean_repository_data_passes(self) -> None:
        result = audit_artifacts(load_artifacts(DATA_DIR))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["coverage_percent"], 100.0)

    def test_interface_signal_mismatch_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            sandbox = Path(temp_dir) / "data"
            shutil.copytree(DATA_DIR, sandbox)
            interfaces_path = sandbox / "interfaces.json"
            interfaces = json.loads(interfaces_path.read_text(encoding="utf-8"))
            interfaces[0]["signal"] = "nonexistent_signal"
            interfaces_path.write_text(json.dumps(interfaces, indent=2) + "\n", encoding="utf-8")

            result = audit_artifacts(load_artifacts(sandbox))
            self.assertTrue(
                any("nonexistent_signal" in message for message in result.errors),
                "The audit should fail when an interface references a missing signal.",
            )

    def test_cli_exports_expected_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            export_dir = Path(temp_dir) / "reports"
            exit_code = run(["audit", "--data-dir", str(DATA_DIR), "--export-dir", str(export_dir)])
            self.assertEqual(exit_code, 0)
            self.assertTrue((export_dir / "audit-summary.md").exists())
            self.assertTrue((export_dir / "traceability-matrix.csv").exists())
            self.assertTrue((export_dir / "interface-register.csv").exists())
            self.assertTrue((export_dir / "risk-register.csv").exists())


if __name__ == "__main__":
    unittest.main()

