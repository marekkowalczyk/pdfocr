# After Action Review

Continuous improvement log. Each session ends with a brief review: what went well, what didn't, what to change. This is the POOGI (Process Of Ongoing Improvement) record for this project.

## 2026-07-24 — Fast path (`-f`/`--fast`), v1.3.0

**What went well:**
- The `-f` text-layer path dropped in with minimal surface area: it reused the existing `resolve_input`/output-naming/`OcrError` plumbing and only needed a new `extract_text_layer()` plus two branches in `main()` (skip the API-key check, swap the extraction fn).
- Pushed back on the user's original "auto-detect good text vs. garbage" framing before writing any code — the honest answer was that a reliable quality gate is the hard part and a silent quality regression is worse than the status quo. The user reframed it as an explicit, opt-in, user-owns-the-judgment flag, which is a much cleaner design.
- Named the output plain `input.txt` rather than `input-ocr.txt`: the `-ocr` marker would be a lie (no OCR happens) and plain `.txt` matches native `pdftotext` output — least surprise for the muscle memory the flag is meant to serve.
- Kept poppler an *optional* runtime dep (not in `requirements.txt`), with a clear "install poppler" error when the binary is missing, so the pure-Python default install is unchanged.
- Forced `-enc UTF-8` on the `pdftotext` call for deterministic output encoding, and made `--fast --images` a hard usage error rather than a silent no-op.

**What didn't go well:**
- No automated tests for the new path (a deliberate, user-approved call). Verified manually via a hand-crafted text-layer PDF; my first throwaway test PDF had a sloppy content stream that produced garbled reading order and briefly looked like a tool bug before I recognized it as the fixture's fault.

**What we'll do differently:**
- When smoke-testing an extraction feature, build the minimal fixture correctly the first time (or use a known-good PDF) so fixture artifacts don't masquerade as regressions.
- Revisit test coverage for `-f` if it ever gains a quality heuristic or an automatic fallback to OCR — at that point the behavior stops being a pure pass-through and the judgment is no longer entirely the user's.

## 2026-07-21 — Unix citizenship, project-local venv, tests

**What went well:**
- Sysexits-style exit codes, 128+signum signal exits, and stdin/batch input landed cleanly with no regressions to the existing OCR flow — verified against a real API call before and after.
- Spotting `urltomd`'s project-local `.venv` + self-re-exec shebang pattern and porting it over fixed a real portability problem (the previous shebang hardcoded this machine's username).
- Writing the test suite surfaced a genuine bug in the test's own isolation logic: `load_dotenv()`'s bare call searches upward from the *script's file location*, not cwd or `$HOME` — env-var/HOME tricks didn't stop it from finding the real `~/.env`. Had to move the real file aside for the duration of that one test.
- Comparing `CLAUDE.md` against `urltomd`'s leaner version caught real duplication (usage/install/architecture repeated near-verbatim from README) before it caused another staleness incident like the shebang one below.
- Before making the repo public, scanning full git history for committed secrets (`.env`, API keys, tokens) first caught the gap cheaply — the LICENSE/README mismatch was found the same way, before anyone browsing the newly-public repo would.
- Tagged and published a proper GitHub release (v1.2.0) with real release notes, and verified it through the authenticated `gh api` rather than trusting an unauthenticated `WebFetch` 404 (which was just the repo being private at the time, not a broken release).

**What didn't go well:**
- `.claude/settings.local.json` was tracked in git (unlike the other two project repos), so a session's worth of one-off permission approvals showed up as unwanted diff noise and had to be untracked after the fact.
- `README.md` had claimed MIT since early in the project's history with no actual `LICENSE` file backing it — a latent gap that only mattered once the repo went public.

**What we'll do differently:**
- When comparing conventions across sibling repos (venv layout, CLAUDE.md structure, `.gitignore` contents), check whether *this* repo already diverges from the others as a first step — the divergence itself is often the thing worth fixing, not just the immediate ask.
- Before flipping a repo's visibility to public, run the secret-scan + license-file check proactively rather than waiting to be asked — both are cheap, and the cost of skipping them only shows up after the repo is already exposed.

## 2026-06-24 — Implemented all backlog milestones

**What went well:**
- All four milestones implemented in one session without needing to revisit scope
- Moving API key check into `main()` was the right fix for `--version` working without a key set

**What didn't go well:**
- Changing the shebang from `python3.11` to `python3` broke the installed command — `python3` on this system is 3.13 and doesn't have `requests`. Had to revert immediately after the user reported the error.

**What we'll do differently:**
- Before changing the shebang, verify that `python3 -c "import requests"` succeeds first
- The shebang stays `python3.11` on this machine — deps are installed there, not under the system `python3`

## 2026-05-16 — Backlog restructured into milestones; added README

**What went well:**
- Quick alignment on Unix philosophy issues — user flagged verbosity, we agreed on the fix shape and logged it
- Efficient "log it, don't code it" approach — kept the session short and focused on planning over premature implementation

**What didn't go well:**
- Ran close checklist once, then user added more work — had to re-run. Minor friction.

**What we'll do differently:**
- When user says "one more thing" after close, handle it and then re-run close as a single pass rather than partial re-checks
