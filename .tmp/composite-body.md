## Issues
- #11 — pyproject.toml: requires-python >=3.10 vs ruff/mypy target py311
- #9 — generator.py: positional bool params are a boolean trap
- #17 — BANNER hardcoded in cli.py module body
- #14 — pyproject.toml: missing PyPI classifiers and project URLs

## Scope

Configuration consistency and API design for publication readiness. These issues block PyPI publication and establish sustainable development practices:

1. **pyproject.toml consistency** (#11, #14): Align Python version constraints, add publication metadata
2. **API clarity** (#9): Replace positional bool params with meaningful names
3. **Module state isolation** (#17): Extract BANNER constant to avoid module-level execution side effects

Shared files: `pyproject.toml`, `src/openloci/cli.py`, `src/openloci/generator.py`

## Acceptance Criteria

- pyproject.toml requires-python matches ruff/mypy target-version (3.11)
- pyproject.toml includes all PyPI classifiers (License, Python versions, Topics)
- pyproject.toml includes project.urls (Homepage, Repository, Bug Tracker, Changelog)
- generator.py positional bool params (no_input, overwrite) replaced with keyword-only args
- BANNER and other module-level state moved to function/constant definition
- Tests pass. ruff/mypy clean. No new warnings.

## Implementation Notes

Order: #11 (pyproject) → #14 (pyproject) → #9 (generator) → #17 (cli). 
Config consistency first, then API fixes.
