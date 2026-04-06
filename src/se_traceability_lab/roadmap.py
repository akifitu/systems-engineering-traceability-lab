"""Portfolio roadmap loading and export helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


Project = Dict[str, Any]


def load_portfolio_projects(projects_file: Path | str) -> List[Project]:
    """Load the structured portfolio roadmap from JSON."""
    return json.loads(Path(projects_file).read_text(encoding="utf-8"))


def filter_projects(projects: Sequence[Project], slug: str | None = None) -> List[Project]:
    """Return all projects or a single project filtered by slug."""
    if slug is None:
        return sorted(list(projects), key=lambda project: project["build_order"])
    return [project for project in projects if project["slug"] == slug]


def export_portfolio_roadmap(projects: Sequence[Project], export_path: Path | str) -> None:
    """Write a Markdown roadmap document."""
    path = Path(export_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_portfolio_roadmap(projects), encoding="utf-8")


def render_portfolio_roadmap(projects: Sequence[Project]) -> str:
    """Render the roadmap and todo board as Markdown."""
    total_projects = len(projects)
    built_projects = sum(1 for project in projects if project["status"] == "built")
    planned_projects = total_projects - built_projects

    sections = [
        "# Systems Engineering Portfolio Roadmap",
        "",
        "This document is generated from `data/portfolio_projects.json`. It gives a step-by-step build order, project-by-project execution plan, and a concrete todo checklist for each repository idea.",
        "",
        "## Portfolio Summary",
        "",
        f"- Total projects: {total_projects}",
        f"- Built projects: {built_projects}",
        f"- Planned projects: {planned_projects}",
        "",
        "## Recommended Build Order",
        "",
    ]

    for project in projects:
        sections.append(
            f"{project['build_order']}. {project['title']} "
            f"(`{project['repo_name']}`, status: {project['status']}, duration: {project['duration_weeks']} weeks)"
        )

    for index, project in enumerate(projects, start=1):
        sections.extend(
            [
                "",
                f"## {index}. {project['title']}",
                "",
                f"- Goal: {project['goal']}",
                f"- Suggested repository name: `{project['repo_name']}`",
                f"- Current status: `{project['status']}`",
                f"- Estimated duration: {project['duration_weeks']} weeks",
                f"- Recommended stack: {', '.join(project['recommended_stack'])}",
                f"- Skills demonstrated: {', '.join(project['skills'])}",
                "",
                "### Step-by-step plan",
                "",
            ]
        )
        for phase_index, phase in enumerate(project["phases"], start=1):
            sections.append(f"{phase_index}. {phase['name']}")
            for step in phase["steps"]:
                sections.append(f"   - {step}")

        sections.extend(["", "### To-do checklist", ""])
        for todo in project["todos"]:
            checkbox = "x" if todo["status"] == "done" else " "
            sections.append(f"- [{checkbox}] {todo['task']}")

        sections.extend(["", "### Expected deliverables", ""])
        for deliverable in project["deliverables"]:
            sections.append(f"- {deliverable}")

    sections.append("")
    return "\n".join(sections)


def build_portfolio_summary(projects: Sequence[Project]) -> Dict[str, Any]:
    """Build a compact summary dictionary for CLI output."""
    ordered = sorted(projects, key=lambda project: project["build_order"])
    return {
      "project_count": len(ordered),
      "built_count": sum(1 for project in ordered if project["status"] == "built"),
      "planned_count": sum(1 for project in ordered if project["status"] != "built"),
      "next_project": next((project["slug"] for project in ordered if project["status"] != "built"), "none"),
    }

