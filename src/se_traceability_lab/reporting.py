"""Export audit results to Markdown and CSV files."""

from __future__ import annotations

from csv import DictWriter
from pathlib import Path
from typing import Iterable, Mapping

from .audit import AuditResult


def export_reports(result: AuditResult, export_dir: Path | str) -> None:
    """Write audit summary, traceability, interface, and risk reports."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    _write_text(export_path / "audit-summary.md", _build_summary_markdown(result))
    _write_csv(export_path / "traceability-matrix.csv", result.traceability_rows)
    _write_csv(export_path / "interface-register.csv", result.interface_rows)
    _write_csv(export_path / "risk-register.csv", result.risk_rows)


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[Mapping[str, str]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def _build_summary_markdown(result: AuditResult) -> str:
    summary = result.summary
    error_block = "\n".join(f"- {message}" for message in result.errors) or "- None"
    warning_block = "\n".join(f"- {message}" for message in result.warnings) or "- None"

    return (
        "# Audit Summary\n\n"
        "## Coverage\n\n"
        f"- Stakeholder requirements: {summary['stakeholder_requirement_count']}\n"
        f"- System requirements: {summary['system_requirement_count']}\n"
        f"- Subsystem requirements: {summary['subsystem_requirement_count']}\n"
        f"- Engineering requirement coverage: {summary['covered_requirement_count']}/{summary['engineering_requirement_count']} "
        f"({summary['coverage_percent']}%)\n\n"
        "## Inventory\n\n"
        f"- Components: {summary['component_count']}\n"
        f"- Interfaces: {summary['interface_count']}\n"
        f"- Risks: {summary['risk_count']}\n"
        f"- High or critical risks: {summary['high_risk_count']}\n\n"
        "## Validation Status\n\n"
        f"- Errors: {summary['error_count']}\n"
        f"- Warnings: {summary['warning_count']}\n\n"
        "## Errors\n\n"
        f"{error_block}\n\n"
        "## Warnings\n\n"
        f"{warning_block}\n"
    )

