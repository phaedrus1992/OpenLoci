## Issues
- #1 — Failing test: no skin ships a 'The Palace' directory
- #2 — mypy --strict fails on the package
- #8 — cli.py 'new': bare except Exception swallows traceback
- #10 — cli.py: re-raise without 'from e' loses exception chain (B904)

## Scope
Foundation sprint fixing test failures, type errors, and error-handling defects in CLI command implementations. All issues block PyPI publish readiness and expose users to poor debugging experience.

**Shared files:**
- `tests/test_skins.py` — test structure / assertions
- `src/openloci/cli.py` — error-handling patterns in `new` + `rooms` commands
- `src/openloci/skins.py` — type annotations

**Data flow:**
- #1 fixtures populate skin list → assertions check template structure
- #2 skins.py returns dict that mypy rejects → fixing type coercion unblocks strict mode
- #8/#10 cli commands catch and re-raise exceptions → standardizing the pattern across all handlers

## Acceptance Criteria
- [ ] All 23 pytest tests pass (including `test_has_palace` on all skins)
- [ ] `mypy --strict src/openloci` returns no errors
- [ ] All exception handlers in cli.py use `raise typer.Exit(code=1) from e` pattern
- [ ] Bare `except Exception` removed; specific exceptions caught instead
- [ ] PR includes closing refs for all 4 sub-issues

## Implementation Notes

**Order:**
1. Fix #2 first (mypy errors) — unblocks linting on other changes
2. Fix #1 (test) — either populate The Palace/ templates or drop test + update README
3. Fix #8/#10 together (cli.py exception handling) — standardize pattern across module

**Template structure note (#1):**
Decision: populate all skins with basic `The Palace/` directory skeleton (9 prefixed rooms). This aligns with README + philosophy. Alternative: drop test + README claim (simpler but cuts a headline feature).

**Exception chain notes (#8/#10):**
- Check `cli.py:125` (FileNotFoundError in `new`)
- Check `cli.py:143` (FileNotFoundError in `new`)
- Check `cli.py:148` (Exception in `new`)
- Check `cli.py:232` (FileNotFoundError in `rooms`)

Replace all with exception-specific handlers + `from e` chain.
