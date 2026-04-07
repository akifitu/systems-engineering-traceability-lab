# Systems Engineering Portfolio Ideas

## 1. Requirements Traceability Lab

Build a repository that turns requirements, interfaces, tests, and risks into structured data with automated consistency checks.

Skills shown:
- requirements engineering
- verification planning
- data discipline
- Python automation

## 2. Satellite Power Budget Simulator

Model eclipse cycles, payload duty cycles, battery margins, and thermal constraints for a small satellite mission.

Skills shown:
- trade studies
- analysis methods
- mission modeling
- visualization

## 3. Interface Control Toolkit

Create a repository that stores interface definitions, validates producers and consumers, and exports interface control documentation.

Skills shown:
- ICD management
- configuration control
- subsystem integration

## 4. Verification Readiness Dashboard

Track each requirement against verification method, evidence, status, owner, and residual open issues.

Skills shown:
- V&V planning
- closure tracking
- audit readiness

## 5. Trade Study Engine

Score architecture alternatives using weighted criteria such as cost, mass, complexity, maintainability, and mission coverage.

Skills shown:
- decision analysis
- architecture selection
- model-based reasoning

## 6. FMEA and Reliability Workbench

Connect failure modes, causes, effects, mitigations, and residual risk into one analyzable dataset.

Skills shown:
- reliability engineering
- hazard analysis
- risk reduction logic

## Recommended Build Order

1. Requirements Traceability Lab
2. Verification Readiness Dashboard
3. Interface Control Toolkit
4. Trade Study Engine
5. FMEA and Reliability Workbench
6. Satellite Power Budget Simulator

The first project is implemented in this repository, and the next four are live as separate public repos:

- `https://github.com/akifitu/verification-readiness-dashboard`
- `https://github.com/akifitu/interface-control-toolkit`
- `https://github.com/akifitu/trade-study-engine`
- `https://github.com/akifitu/fmea-reliability-workbench`

## Where The Step-By-Step Plans Live

The structured source of truth is `data/portfolio_projects.json`.

You can regenerate the full roadmap and todo checklist with:

```bash
make roadmap
```

The generated reviewer-facing output is `reports/portfolio-roadmap.md`.
