"""Load structured engineering artifacts from JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ArtifactStore = Dict[str, List[Dict[str, Any]]]


ARTIFACT_FILES = {
    "stakeholder_requirements": "stakeholder_requirements.json",
    "system_requirements": "system_requirements.json",
    "subsystem_requirements": "subsystem_requirements.json",
    "components": "components.json",
    "interfaces": "interfaces.json",
    "verification_tests": "verification_tests.json",
    "risks": "risks.json",
}


def load_artifacts(data_dir: Path | str) -> ArtifactStore:
    """Load the repository engineering artifacts from a directory."""
    base_path = Path(data_dir)
    artifacts: ArtifactStore = {}
    for key, filename in ARTIFACT_FILES.items():
        path = base_path / filename
        artifacts[key] = json.loads(path.read_text(encoding="utf-8"))
    return artifacts

