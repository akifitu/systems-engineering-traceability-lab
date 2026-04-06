# Step-By-Step Project Plan

This plan is written as a practical roadmap for a systems engineering student portfolio.

For the complete multi-project portfolio roadmap and todo checklist across all ideas, see `reports/portfolio-roadmap.md`.

## Phase 1: Define the flagship problem

1. Pick a realistic system context with multiple subsystems and non-trivial interfaces.
2. Write 3 to 5 stakeholder requirements tied to mission value.
3. Derive 5 to 8 system requirements from those needs.
4. Allocate subsystem requirements to components.

## Phase 2: Structure the engineering data

1. Store requirements in machine-readable files.
2. Define verification cases and connect them to requirements.
3. Define subsystem components and the signals they produce or consume.
4. Create a simple risk register with likelihood, consequence, and mitigation.

## Phase 3: Build the automation

1. Implement loaders for all engineering artifacts.
2. Validate IDs, parent-child traces, and test linkage.
3. Validate interfaces against component inputs and outputs.
4. Generate report artifacts that a reviewer can read without running the code.

## Phase 4: Debug and harden

1. Add regression tests for a clean dataset.
2. Add negative tests for broken interfaces or trace links.
3. Run the CLI and export reports.
4. Fix any schema or validation defects found during execution.

## Phase 5: Publish professionally

1. Add a recruiter-friendly README.
2. Add a license and repository map.
3. Add CI so the repository proves it is maintained.
4. Push to GitHub and keep generated reports committed as evidence.

## Next Extensions

- add configuration baselines
- add requirement status tracking
- add trade study scoring
- add web visualization
- add MBSE-friendly export formats
