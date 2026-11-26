# Agent work prompts

Three prompts drive an issue: plan, implement and close. The rules live in [`AGENTS.md`](../AGENTS.md). Replace the placeholders and run the plan prompt first. An issue rated above Sm + Lo has its plan approved before any file change; an Sm + Lo issue goes straight to the PR (AGENTS.md §3, "Size and risk").

---

## 1. Plan (no file edits)

```text
Follow AGENTS.md.

I want to work on issue: <ISSUE-ID> — <title>.
Rating: <Sm|Md|Lg> / <Lo|Med|Hi> (the expected half of the roadmap's Risk and Size columns; estimate it in the plan if missing).

First inspect the code, the docs, the roadmap, the acceptance and the current project status. Do not edit files yet.

Return:
1. Current state and relevant files.
2. Dependencies and prerequisites.
3. A small, ordered implementation plan.
4. Acceptance criteria and how each will be checked.
5. Risks, assumptions and compatibility points.
6. Exact commands to run.
7. Files to create or change.
8. The feature branch name (AGENTS.md §13) and which items of §12 "Issue closing checklist" and §4 "Content rules" the issue touches.
9. The Size and Risk, and whether planning raises either.

Keep the scope to this issue. Do not implement future phases or change the architecture silently. Above Sm + Lo: run po-reviewer on the plan, show its verdict with the plan and wait for my approval before editing. Sm + Lo: go on to implementation. If the issue turns out bigger or riskier, raise the rating and say why.
```

## 2. Implement (straight away for Sm + Lo; after the plan is approved otherwise)

```text
Follow AGENTS.md.

Implement only the plan we just agreed on.
- Work on the issue's feature branch, never on main.
- Keep the diff focused. Explain any deviation before making it.
- Add or update the tests for the changed behavior.
- Do not implement tasks from future phases.
- Do not add dependencies or services outside the approved plan.
- Do not run destructive commands or sign up for anything paid without my explicit approval.
- Run the checks and report the actual output.
- Update the docs and PROJECT_STATUS.md only for what was actually verified.
- Do not commit; the close step does.

At the end, report changed files, checks run, results, acceptance met and not met, limitations and the recommended next task.
```

## 3. Close

```text
Follow AGENTS.md.

Review the current diff against the agreed plan and the acceptance. Do not add features.
- Look for out-of-scope changes, secrets, generated files, weak tests, configuration drift and undocumented behavior.
- Check the diff, the commit message and the PR text against §4 "Content rules": no professional's name, no dose recommendation.
- Run the validation commands and report the actual output.
- Point out acceptance criteria that are not met or not verified.
- Run the review gates in AGENTS.md §3 "Agent workflow": code-reviewer on every code or config change; above Sm + Lo, then po-reviewer in acceptance mode. Fix blocking findings and put each final verdict in the PR.
- Apply §12 "Issue closing checklist".
- Make a Conventional Commit on the feature branch, push it, open the PR and read the CI. Never push to main and never merge; the merge is Filipe's (AGENTS.md §13).

Return a short completion report, the commit SHA, the suggested PR text (with the issue ID, the rating and the acceptance checked) and the next useful task.
```
