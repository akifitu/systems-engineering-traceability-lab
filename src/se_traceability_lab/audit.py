"""Validation and reporting logic for the Systems Engineering Traceability Lab."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence, Tuple
import re


VALID_METHODS = {"analysis", "inspection", "demonstration", "test"}
AMBIGUOUS_TERMS = ("fast", "easy", "robust", "simple", "quick", "efficient")

REQ_PATTERNS = {
    "stakeholder": re.compile(r"^STK-\d{3}$"),
    "system": re.compile(r"^SYS-\d{3}$"),
    "subsystem": re.compile(r"^SUB-[A-Z]+-\d{3}$"),
}


@dataclass
class AuditResult:
    errors: List[str]
    warnings: List[str]
    summary: Dict[str, Any]
    traceability_rows: List[Dict[str, str]]
    interface_rows: List[Dict[str, str]]
    risk_rows: List[Dict[str, str]]


def audit_artifacts(artifacts: Dict[str, List[Dict[str, Any]]]) -> AuditResult:
    """Audit a repository's engineering artifacts and build exportable report rows."""
    errors: List[str] = []
    warnings: List[str] = []

    stakeholder_requirements = artifacts["stakeholder_requirements"]
    system_requirements = artifacts["system_requirements"]
    subsystem_requirements = artifacts["subsystem_requirements"]
    components = artifacts["components"]
    interfaces = artifacts["interfaces"]
    verification_tests = artifacts["verification_tests"]
    risks = artifacts["risks"]

    _check_duplicate_ids(stakeholder_requirements, "stakeholder_requirements", errors)
    _check_duplicate_ids(system_requirements, "system_requirements", errors)
    _check_duplicate_ids(subsystem_requirements, "subsystem_requirements", errors)
    _check_duplicate_ids(components, "components", errors)
    _check_duplicate_ids(interfaces, "interfaces", errors)
    _check_duplicate_ids(verification_tests, "verification_tests", errors)
    _check_duplicate_ids(risks, "risks", errors)

    all_requirements = _build_requirement_index(
        stakeholder_requirements, system_requirements, subsystem_requirements
    )
    tests_by_id = {test["id"]: test for test in verification_tests}
    components_by_id = {component["id"]: component for component in components}

    _validate_requirements(stakeholder_requirements, "stakeholder", all_requirements, tests_by_id, errors, warnings)
    _validate_requirements(system_requirements, "system", all_requirements, tests_by_id, errors, warnings)
    _validate_requirements(subsystem_requirements, "subsystem", all_requirements, tests_by_id, errors, warnings)
    _validate_tests(verification_tests, all_requirements, errors, warnings)
    _validate_components(components, errors)
    _validate_interfaces(interfaces, components_by_id, errors)
    risk_rows = _validate_risks(risks, all_requirements, errors)

    traceability_rows = _build_traceability_rows(stakeholder_requirements, system_requirements, subsystem_requirements)
    interface_rows = _build_interface_rows(interfaces)
    summary = _build_summary(
        stakeholder_requirements=stakeholder_requirements,
        system_requirements=system_requirements,
        subsystem_requirements=subsystem_requirements,
        components=components,
        interfaces=interfaces,
        risks=risk_rows,
        errors=errors,
        warnings=warnings,
    )

    return AuditResult(
        errors=errors,
        warnings=warnings,
        summary=summary,
        traceability_rows=traceability_rows,
        interface_rows=interface_rows,
        risk_rows=risk_rows,
    )


def _check_duplicate_ids(records: Sequence[Dict[str, Any]], label: str, errors: List[str]) -> None:
    seen = set()
    duplicates = []
    for record in records:
        record_id = record.get("id")
        if record_id in seen:
            duplicates.append(record_id)
        seen.add(record_id)
    for duplicate in duplicates:
        errors.append(f"{label}: duplicate id '{duplicate}' detected.")


def _build_requirement_index(
    stakeholder_requirements: Sequence[Dict[str, Any]],
    system_requirements: Sequence[Dict[str, Any]],
    subsystem_requirements: Sequence[Dict[str, Any]],
) -> Dict[str, Tuple[str, Dict[str, Any]]]:
    requirement_index: Dict[str, Tuple[str, Dict[str, Any]]] = {}
    for level, records in (
        ("stakeholder", stakeholder_requirements),
        ("system", system_requirements),
        ("subsystem", subsystem_requirements),
    ):
        for record in records:
            requirement_index[record["id"]] = (level, record)
    return requirement_index


def _validate_requirements(
    requirements: Sequence[Dict[str, Any]],
    level: str,
    all_requirements: Dict[str, Tuple[str, Dict[str, Any]]],
    tests_by_id: Dict[str, Dict[str, Any]],
    errors: List[str],
    warnings: List[str],
) -> None:
    pattern = REQ_PATTERNS[level]
    for requirement in requirements:
        requirement_id = requirement["id"]
        text = requirement.get("text", "")
        text_lower = text.lower()

        if not pattern.match(requirement_id):
            errors.append(f"{requirement_id}: invalid {level} requirement id format.")
        if "shall" not in text_lower:
            errors.append(f"{requirement_id}: requirement text must contain 'shall'.")
        for term in AMBIGUOUS_TERMS:
            if term in text_lower:
                warnings.append(f"{requirement_id}: requirement text contains ambiguous term '{term}'.")

        if level == "stakeholder":
            continue

        parent_ids = requirement.get("parents", [])
        if not parent_ids:
            errors.append(f"{requirement_id}: engineering requirement is missing parent requirements.")
        for parent_id in parent_ids:
            if parent_id not in all_requirements:
                errors.append(f"{requirement_id}: parent requirement '{parent_id}' does not exist.")

        verification_methods = set(requirement.get("verification_methods", []))
        if not verification_methods:
            errors.append(f"{requirement_id}: at least one verification method is required.")
        invalid_methods = verification_methods - VALID_METHODS
        if invalid_methods:
            errors.append(
                f"{requirement_id}: invalid verification methods declared: {', '.join(sorted(invalid_methods))}."
            )

        linked_tests = requirement.get("tests", [])
        if not linked_tests:
            errors.append(f"{requirement_id}: at least one verification test link is required.")

        matched_methods = False
        for test_id in linked_tests:
            if test_id not in tests_by_id:
                errors.append(f"{requirement_id}: linked test '{test_id}' does not exist.")
                continue
            test = tests_by_id[test_id]
            if requirement_id not in test.get("requirement_ids", []):
                errors.append(f"{requirement_id}: linked test '{test_id}' does not trace back to the requirement.")
            if test.get("method") in verification_methods:
                matched_methods = True

        if linked_tests and not matched_methods:
            errors.append(f"{requirement_id}: no linked tests use one of the declared verification methods.")


def _validate_tests(
    verification_tests: Sequence[Dict[str, Any]],
    all_requirements: Dict[str, Tuple[str, Dict[str, Any]]],
    errors: List[str],
    warnings: List[str],
) -> None:
    for test in verification_tests:
        test_id = test["id"]
        method = test.get("method")
        if method not in VALID_METHODS:
            errors.append(f"{test_id}: invalid verification method '{method}'.")

        requirement_ids = test.get("requirement_ids", [])
        if not requirement_ids:
            warnings.append(f"{test_id}: verification case is not linked to any requirements.")

        for requirement_id in requirement_ids:
            if requirement_id not in all_requirements:
                errors.append(f"{test_id}: linked requirement '{requirement_id}' does not exist.")


def _validate_components(components: Sequence[Dict[str, Any]], errors: List[str]) -> None:
    for component in components:
        if not component.get("inputs"):
            errors.append(f"{component['id']}: component must declare at least one input signal.")
        if not component.get("outputs"):
            errors.append(f"{component['id']}: component must declare at least one output signal.")


def _validate_interfaces(
    interfaces: Sequence[Dict[str, Any]],
    components_by_id: Dict[str, Dict[str, Any]],
    errors: List[str],
) -> None:
    for interface in interfaces:
        interface_id = interface["id"]
        source_id = interface.get("source")
        target_id = interface.get("target")
        signal = interface.get("signal")

        source = components_by_id.get(source_id)
        target = components_by_id.get(target_id)

        if source is None:
            errors.append(f"{interface_id}: source component '{source_id}' does not exist.")
            continue
        if target is None:
            errors.append(f"{interface_id}: target component '{target_id}' does not exist.")
            continue

        if signal not in source.get("outputs", []):
            errors.append(f"{interface_id}: signal '{signal}' is not produced by source component '{source_id}'.")
        if signal not in target.get("inputs", []):
            errors.append(f"{interface_id}: signal '{signal}' is not consumed by target component '{target_id}'.")


def _validate_risks(
    risks: Sequence[Dict[str, Any]],
    all_requirements: Dict[str, Tuple[str, Dict[str, Any]]],
    errors: List[str],
) -> List[Dict[str, str]]:
    risk_rows: List[Dict[str, str]] = []
    for risk in risks:
        risk_id = risk["id"]
        likelihood = risk.get("likelihood")
        consequence = risk.get("consequence")
        if not isinstance(likelihood, int) or likelihood < 1 or likelihood > 5:
            errors.append(f"{risk_id}: likelihood must be an integer between 1 and 5.")
        if not isinstance(consequence, int) or consequence < 1 or consequence > 5:
            errors.append(f"{risk_id}: consequence must be an integer between 1 and 5.")

        for requirement_id in risk.get("related_requirements", []):
            if requirement_id not in all_requirements:
                errors.append(f"{risk_id}: related requirement '{requirement_id}' does not exist.")

        score = int(likelihood) * int(consequence)
        if score >= 15:
            level = "critical"
        elif score >= 9:
            level = "high"
        elif score >= 5:
            level = "medium"
        else:
            level = "low"

        risk_rows.append(
            {
                "id": risk_id,
                "description": risk["description"],
                "likelihood": str(likelihood),
                "consequence": str(consequence),
                "score": str(score),
                "level": level,
                "mitigation": risk["mitigation"],
                "related_requirements": "; ".join(risk.get("related_requirements", [])),
            }
        )
    return risk_rows


def _build_traceability_rows(
    stakeholder_requirements: Sequence[Dict[str, Any]],
    system_requirements: Sequence[Dict[str, Any]],
    subsystem_requirements: Sequence[Dict[str, Any]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for level, records in (
        ("stakeholder", stakeholder_requirements),
        ("system", system_requirements),
        ("subsystem", subsystem_requirements),
    ):
        for requirement in records:
            rows.append(
                {
                    "id": requirement["id"],
                    "level": level,
                    "title": requirement["title"],
                    "parents": "; ".join(requirement.get("parents", [])),
                    "verification_methods": "; ".join(requirement.get("verification_methods", [])),
                    "tests": "; ".join(requirement.get("tests", [])),
                    "allocations": "; ".join(requirement.get("component_allocations", [])),
                }
            )
    return rows


def _build_interface_rows(interfaces: Sequence[Dict[str, Any]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for interface in interfaces:
        rows.append(
            {
                "id": interface["id"],
                "name": interface["name"],
                "source": interface["source"],
                "target": interface["target"],
                "signal": interface["signal"],
                "protocol": interface["protocol"],
                "payload": interface["payload"],
            }
        )
    return rows


def _build_summary(
    *,
    stakeholder_requirements: Sequence[Dict[str, Any]],
    system_requirements: Sequence[Dict[str, Any]],
    subsystem_requirements: Sequence[Dict[str, Any]],
    components: Sequence[Dict[str, Any]],
    interfaces: Sequence[Dict[str, Any]],
    risks: Sequence[Dict[str, str]],
    errors: Sequence[str],
    warnings: Sequence[str],
) -> Dict[str, Any]:
    engineering_requirements = list(system_requirements) + list(subsystem_requirements)
    covered_requirements = sum(1 for requirement in engineering_requirements if requirement.get("tests"))
    coverage_percent = round((covered_requirements / len(engineering_requirements)) * 100, 1) if engineering_requirements else 0.0
    high_risk_count = sum(1 for risk in risks if risk["level"] in {"high", "critical"})

    return {
        "stakeholder_requirement_count": len(stakeholder_requirements),
        "system_requirement_count": len(system_requirements),
        "subsystem_requirement_count": len(subsystem_requirements),
        "engineering_requirement_count": len(engineering_requirements),
        "covered_requirement_count": covered_requirements,
        "coverage_percent": coverage_percent,
        "component_count": len(components),
        "interface_count": len(interfaces),
        "risk_count": len(risks),
        "high_risk_count": high_risk_count,
        "error_count": len(errors),
        "warning_count": len(warnings),
    }

