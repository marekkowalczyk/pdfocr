# After Action Review

Continuous improvement log. Each session ends with a brief review: what went well, what didn't, what to change. This is the POOGI (Process Of Ongoing Improvement) record for this project.

## 2026-07-21 — Unix citizenship, project-local venv, tests

**What went well:**
- Sysexits-style exit codes, 128+signum signal exits, and stdin/batch input landed cleanly with no regressions to the existing OCR flow — verified against a real API call before and after.
- Spotting `urltomd`'s project-local `.venv` + self-re-exec shebang pattern and porting it over fixed a real portability problem (the previous shebang hardcoded this machine's username).
- Writing the test suite surfaced a genuine bug in the test's own isolation logic: `load_dotenv()`'s bare call searches upward from the *script's file location*, not cwd or `$HOME` — env-var/HOME tricks didn't stop it from finding the real `~/.env`. Had to move the real file aside for the duration of that one test.
- Comparing `CLAUDE.md` against `urltomd`'s leaner version caught real duplication (usage/install/architecture repeated near-verbatim from README) before it caused another staleness incident like the shebang one below.

**What didn't go well:**
- `.claude/settings.local.json` was tracked in git (unlike the other two project repos), so a session's worth of one-off permission approvals showed up as unwanted diff noise and had to be untracked after the fact.

**What we'll do differently:**
- When comparing conventions across sibling repos (venv layout, CLAUDE.md structure, `.gitignore` contents), check whether *this* repo already diverges from the others as a first step — the divergence itself is often the thing worth fixing, not just the immediate ask.

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
