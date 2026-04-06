"""Command line interface for the Systems Engineering Traceability Lab."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .audit import audit_artifacts
from .data import load_artifacts
from .roadmap import (
    build_portfolio_summary,
    export_portfolio_roadmap,
    filter_projects,
    load_portfolio_projects,
)
from .reporting import export_reports


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        prog="se-trace-lab",
        description="Audit requirements traceability, interfaces, verification, and risk artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Validate engineering artifacts and optionally export reports.")
    audit_parser.add_argument("--data-dir", default="data", help="Directory containing JSON artifact files.")
    audit_parser.add_argument("--export-dir", help="Directory where reports should be written.")

    roadmap_parser = subparsers.add_parser(
        "roadmap",
        help="Render the multi-project portfolio roadmap and todo checklist.",
    )
    roadmap_parser.add_argument(
        "--projects-file",
        default="data/portfolio_projects.json",
        help="JSON file containing the portfolio roadmap source data.",
    )
    roadmap_parser.add_argument(
        "--project",
        help="Optional project slug to render only one roadmap entry.",
    )
    roadmap_parser.add_argument(
        "--export-path",
        help="Optional Markdown file path where the roadmap should be written.",
    )
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        artifacts = load_artifacts(Path(args.data_dir))
        result = audit_artifacts(artifacts)
        _print_summary(result)
        if args.export_dir:
            export_reports(result, Path(args.export_dir))
            print(f"Reports exported to: {args.export_dir}")
        return 1 if result.errors else 0

    if args.command == "roadmap":
        projects = filter_projects(load_portfolio_projects(Path(args.projects_file)), args.project)
        if not projects:
            print(f"No portfolio project found for slug: {args.project}")
            return 1
        _print_roadmap_summary(projects)
        if args.export_path:
            export_portfolio_roadmap(projects, Path(args.export_path))
            print(f"Roadmap exported to: {args.export_path}")
        return 0

    parser.error("Unknown command.")
    return 2


def _print_summary(result) -> None:
    summary = result.summary
    print("Audit summary")
    print(f"  Stakeholder requirements: {summary['stakeholder_requirement_count']}")
    print(f"  System requirements: {summary['system_requirement_count']}")
    print(f"  Subsystem requirements: {summary['subsystem_requirement_count']}")
    print(
        "  Engineering coverage: "
        f"{summary['covered_requirement_count']}/{summary['engineering_requirement_count']} "
        f"({summary['coverage_percent']}%)"
    )
    print(f"  Components: {summary['component_count']}")
    print(f"  Interfaces: {summary['interface_count']}")
    print(f"  Risks: {summary['risk_count']} ({summary['high_risk_count']} high/critical)")
    print(f"  Errors: {summary['error_count']}")
    print(f"  Warnings: {summary['warning_count']}")
    if result.errors:
        print("Validation errors:")
        for message in result.errors:
            print(f"  - {message}")
    if result.warnings:
        print("Validation warnings:")
        for message in result.warnings:
            print(f"  - {message}")


def _print_roadmap_summary(projects) -> None:
    summary = build_portfolio_summary(projects)
    print("Roadmap summary")
    print(f"  Projects: {summary['project_count']}")
    print(f"  Built: {summary['built_count']}")
    print(f"  Planned: {summary['planned_count']}")
    print(f"  Next suggested project: {summary['next_project']}")


if __name__ == "__main__":
    raise SystemExit(run())

