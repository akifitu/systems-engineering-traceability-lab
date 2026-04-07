# Systems Engineering Portfolio Roadmap

This document is generated from `data/portfolio_projects.json`. It gives a step-by-step build order, project-by-project execution plan, and a concrete todo checklist for each repository idea.

## Portfolio Summary

- Total projects: 6
- Built projects: 4
- Planned projects: 2

## Recommended Build Order

1. Requirements Traceability Lab (`systems-engineering-traceability-lab`, status: built, duration: 1-2 weeks)
2. Verification Readiness Dashboard (`verification-readiness-dashboard`, status: built, duration: 2-3 weeks)
3. Interface Control Toolkit (`interface-control-toolkit`, status: built, duration: 1-2 weeks)
4. Trade Study Engine (`trade-study-engine`, status: built, duration: 2-3 weeks)
5. FMEA and Reliability Workbench (`fmea-reliability-workbench`, status: planned, duration: 2-3 weeks)
6. Satellite Power Budget Simulator (`satellite-power-budget-simulator`, status: planned, duration: 2-3 weeks)

## 1. Requirements Traceability Lab

- Goal: Turn requirements, interfaces, tests, and risks into structured engineering data with automated validation and exportable reports.
- Suggested repository name: `systems-engineering-traceability-lab`
- Current status: `built`
- Estimated duration: 1-2 weeks
- Recommended stack: Python, JSON, CSV, GitHub Actions
- Skills demonstrated: requirements engineering, verification planning, interface management, Python automation

### Step-by-step plan

1. Define the case study
   - Choose a realistic mission with multiple subsystems and visible system interactions.
   - Write stakeholder-level needs and derive engineering requirements.
   - Allocate subsystem responsibilities and define a stable ID scheme.
2. Structure the engineering data
   - Store stakeholder, system, and subsystem requirements in machine-readable files.
   - Add components, interfaces, verification cases, and a risk register.
   - Make parent-child traces explicit so audits can be automated.
3. Build the automation
   - Implement artifact loaders and an audit engine.
   - Validate traceability, verification linkage, interface consistency, and risk data.
   - Export reviewer-facing Markdown and CSV reports.
4. Debug and verify
   - Add regression tests for the clean dataset.
   - Inject negative cases such as broken interfaces and missing links.
   - Fix validation logic until the repository audits cleanly.
5. Publish professionally
   - Write an English README, add licensing, and organize the docs folder.
   - Commit generated reports so reviewers can inspect outputs immediately.
   - Push the repo publicly and keep CI green.

### To-do checklist

- [x] Select a mission scenario with at least five subsystems
- [x] Model stakeholder, system, and subsystem requirements
- [x] Define components, interfaces, verification tests, and risks
- [x] Implement the audit CLI and report exporter
- [x] Add unit tests and negative validation tests
- [x] Generate audit reports into the reports folder
- [x] Set up GitHub Actions CI
- [x] Publish and maintain the public repository

### Expected deliverables

- Structured engineering dataset
- Audit CLI
- Traceability and interface reports
- Automated tests and CI
- Recruiter-friendly README

## 2. Verification Readiness Dashboard

- Goal: Track requirement verification status, evidence, owners, and closure risk in a reviewer-friendly dashboard.
- Suggested repository name: `verification-readiness-dashboard`
- Current status: `built`
- Estimated duration: 2-3 weeks
- Recommended stack: Python, CSV, HTML, GitHub Pages
- Skills demonstrated: verification and validation, status accounting, evidence management, dashboard reporting

### Step-by-step plan

1. Define the verification model
   - Define requirement, verification case, owner, due date, and evidence fields.
   - Decide which status states matter, such as planned, in-work, blocked, and closed.
   - Choose metrics such as closure percentage and open critical items.
2. Build the source datasets
   - Create machine-readable requirement and verification records.
   - Link evidence files or references to each verification case.
   - Capture subsystem ownership and review status.
3. Implement the dashboard
   - Compute readiness metrics by subsystem and verification method.
   - Render a static HTML dashboard or exportable summary tables.
   - Highlight blocked or overdue verification items.
4. Debug and verify
   - Test missing evidence, duplicated cases, and inconsistent statuses.
   - Verify that dashboard totals match the source data.
   - Refine the display so a reviewer can understand status quickly.
5. Publish professionally
   - Add screenshots and a sample readiness review pack.
   - Document how to add new requirements and evidence.
   - Push the repo and optionally deploy GitHub Pages.

### To-do checklist

- [x] Design the verification status data model
- [x] Create requirement-to-evidence sample data
- [x] Implement subsystem and method readiness metrics
- [x] Render a static dashboard or HTML report
- [x] Add tests for missing or inconsistent evidence
- [ ] Prepare screenshots for the README
- [x] Document update workflow for new verification cases
- [x] Publish and push the repository

### Expected deliverables

- Verification tracking dataset
- Readiness metrics engine
- Static dashboard export
- Evidence review examples
- Public repository or GitHub Pages deployment

## 3. Interface Control Toolkit

- Goal: Model subsystem interfaces, validate producer-consumer compatibility, and export interface control documentation.
- Suggested repository name: `interface-control-toolkit`
- Current status: `built`
- Estimated duration: 1-2 weeks
- Recommended stack: Python, JSON, Markdown, CSV
- Skills demonstrated: interface management, integration engineering, configuration control, automation

### Step-by-step plan

1. Define the integration context
   - Pick a system with at least four interacting subsystems.
   - List critical interfaces, protocols, data items, and timing constraints.
   - Set naming rules for signals, interface IDs, and ownership.
2. Build the interface schema
   - Store components and their provided and required signals in machine-readable files.
   - Model each interface with source, target, protocol, payload, units, and update rate.
   - Capture versioning or compatibility metadata.
3. Implement the toolkit
   - Validate that every source produces the declared signal.
   - Validate that every target consumes the declared signal.
   - Export an interface register and an ICD-style summary document.
4. Debug and verify
   - Create broken sample interfaces to prove the validator catches errors.
   - Test naming mismatches, missing units, and duplicate identifiers.
   - Fix schema gaps that make reviews harder.
5. Publish professionally
   - Add diagrams or tables that explain the integration context.
   - Document how a reviewer adds a new interface.
   - Publish example exports and push the repo.

### To-do checklist

- [x] Choose the reference system and subsystem set
- [x] Define an interface schema with timing and units
- [x] Implement producer-consumer validation
- [x] Generate interface register and ICD exports
- [x] Add negative tests for mismatched interfaces
- [x] Write onboarding documentation for new interfaces
- [x] Create a sample dataset and diagrams
- [x] Publish and push the repository

### Expected deliverables

- Interface schema and sample dataset
- Compatibility validator
- ICD-style export
- Negative test suite
- Integration-focused README

## 4. Trade Study Engine

- Goal: Compare architecture options against weighted decision criteria and make trade study logic reproducible.
- Suggested repository name: `trade-study-engine`
- Current status: `built`
- Estimated duration: 2-3 weeks
- Recommended stack: Python, CSV, Markdown, Plots
- Skills demonstrated: trade studies, decision analysis, architecture evaluation, sensitivity analysis

### Step-by-step plan

1. Define the decision problem
   - Choose an architecture decision such as propulsion, communications, or sensing options.
   - Define the candidate concepts and evaluation criteria.
   - Assign rationale and initial weights for each criterion.
2. Build the scoring data
   - Create machine-readable alternatives, scores, assumptions, and references.
   - Separate raw technical data from weighted decision logic.
   - Capture uncertainty bounds or confidence notes.
3. Implement the engine
   - Calculate weighted scores and rank alternatives.
   - Generate tables and charts that explain why the preferred option wins.
   - Support quick what-if analysis by changing weights.
4. Debug and verify
   - Test that weights sum correctly and rankings update as expected.
   - Validate edge cases such as tied scores or missing inputs.
   - Check that published conclusions match the underlying math.
5. Publish professionally
   - Write a decision narrative around the trade study.
   - Include sensitivity results and assumptions in the README.
   - Push the repo with example scenarios and outputs.

### To-do checklist

- [x] Choose a concrete architecture decision to analyze
- [x] Define alternatives and weighted criteria
- [x] Store scoring inputs in structured files
- [x] Implement weighted ranking and what-if analysis
- [x] Generate comparison tables and charts
- [x] Test score normalization and ranking changes
- [x] Write a technical decision narrative
- [x] Publish and push the repository

### Expected deliverables

- Trade study dataset
- Weighted scoring engine
- Sensitivity analysis outputs
- Decision summary report
- Public architecture-selection repository

## 5. FMEA and Reliability Workbench

- Goal: Connect failure modes, causes, effects, controls, and residual risk into a structured engineering analysis workspace.
- Suggested repository name: `fmea-reliability-workbench`
- Current status: `planned`
- Estimated duration: 2-3 weeks
- Recommended stack: Python, JSON, CSV, Markdown
- Skills demonstrated: reliability engineering, hazard analysis, risk reduction, mitigation tracking

### Step-by-step plan

1. Define the reliability scope
   - Pick a subsystem or mission concept with meaningful failure modes.
   - Define severity, occurrence, and detection scales.
   - Choose how mitigations and controls will be recorded.
2. Build the analysis dataset
   - Create structured records for functions, failure modes, causes, and effects.
   - Link mitigations, controls, and residual risks to each failure mode.
   - Add subsystem ownership and review status.
3. Implement the workbench
   - Calculate risk priority values and highlight the highest-risk items.
   - Generate sortable tables or Markdown reports for review boards.
   - Trace mitigations back to affected functions or requirements.
4. Debug and verify
   - Test invalid scale values, duplicate failure modes, and missing mitigations.
   - Verify that risk priority calculations match the documented method.
   - Review whether mitigations actually reduce the residual score.
5. Publish professionally
   - Document the scoring model and review assumptions clearly.
   - Include a sample FMEA review report in the repository.
   - Push the repo with generated outputs and test coverage.

### To-do checklist

- [ ] Select the system or subsystem to analyze
- [ ] Define severity, occurrence, and detection scales
- [ ] Model failure modes, causes, effects, and controls
- [ ] Implement risk-priority calculations and reports
- [ ] Trace mitigations to functions or requirements
- [ ] Add tests for invalid scores and missing controls
- [ ] Write a review-ready README and sample report
- [ ] Publish and push the repository

### Expected deliverables

- Structured FMEA dataset
- Risk-priority analysis engine
- Mitigation traceability report
- Failure-review sample output
- Public reliability engineering repository

## 6. Satellite Power Budget Simulator

- Goal: Simulate solar generation, eclipse losses, battery usage, and subsystem loads across orbital mission phases.
- Suggested repository name: `satellite-power-budget-simulator`
- Current status: `planned`
- Estimated duration: 2-3 weeks
- Recommended stack: Python, CSV, Matplotlib, Jupyter
- Skills demonstrated: mission analysis, energy budgeting, scenario modeling, engineering visualization

### Step-by-step plan

1. Define the mission assumptions
   - Select a cubesat or microsat mission concept and target orbit.
   - List subsystem load cases for sunlight, eclipse, safe mode, and payload mode.
   - Document battery, solar array, and depth-of-discharge assumptions.
2. Build the data model
   - Create machine-readable scenario inputs for orbital periods and subsystem duty cycles.
   - Define reusable configuration files for power generation and consumption.
   - Capture nominal and worst-case scenarios.
3. Implement the simulator
   - Calculate orbital energy balance across mission segments.
   - Simulate state-of-charge evolution over multiple orbits.
   - Export plots and CSV tables for each mission scenario.
4. Debug and verify
   - Cross-check sample scenarios against hand calculations.
   - Test edge cases such as prolonged eclipse or payload overuse.
   - Refine model assumptions when margins look unrealistic.
5. Publish professionally
   - Write a clear assumptions section and scenario guide.
   - Include comparison charts and an example mission run.
   - Push the repo with generated figures and validation notes.

### To-do checklist

- [ ] Choose a reference satellite mission and orbit
- [ ] Create sunlight and eclipse load-case assumptions
- [ ] Model solar array and battery parameters
- [ ] Implement orbit-by-orbit energy balance simulation
- [ ] Add plots for state of charge and power margins
- [ ] Validate the model against hand calculations
- [ ] Write a technical README and scenario guide
- [ ] Publish example results and push the repo

### Expected deliverables

- Configurable mission power model
- Scenario input files
- Power margin plots
- Validation notebook or report
- Public case-study repository
