# After Action Review

Continuous improvement log. Each session ends with a brief review: what went well, what didn't, what to change. This is the POOGI (Process Of Ongoing Improvement) record for this project.

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
