# ADR-0004: Edition generation by the Claude API

| ADR-0004 | Detail |
| --- | --- |
| State | `approved` |
| Opened | 2026-11-25 |
| Decided | 2026-11-25 (Filipe, in the F0-07 planning thread) |
| Amended | 2026-11-26 (Filipe's decisions D3, D6 and D7 on the plan review; recorded in F0-09); 2026-11-27 (gate G0: two calls and the edition slots; recorded in F0-08) |
| Owner | Filipe (product owner) |
| Index ID | ADR-004 |
| Related issues | F0-07, F0-08, F0-09, F2-05, F2-09, F2-11 to F2-13, F3-02, F3-05, F3-07, F7-08 |
| Replaces | The Grok scheduled routine from the final plan (F0-02, F2-06) |
| Replaced by | — |

## Context and problem

The final plan had a Grok scheduled routine write each edition, with an unverified ability to reach the GitHub API (F0-02). Filipe is moving the whole workflow to Claude and accepts paying for the Claude API, up to US$30 a month. The scope also grew: besides journal articles, an edition carries guidelines, alerts and news that affect pediatrics, and news is part of the MVP.

The site publishes without review (ADR-002), so whatever generates the edition must be reproducible, cheap to rerun and constrained by checks the project owns.

## Decision

- **Who writes:** a Python script in this repository calls the Claude API. It starts from the F0-08 trial code, which F2-11 to F2-13 review, and its dependencies are hash-locked (amended 2026-11-26, D6). The starting model is Claude Sonnet 5.5 (`claude-sonnet-5-5`). Changing the model is a config change, measured against the eval set (F3-05) before it is merged; the set is built before the first model or prompt change after F3-03.
- **Where it runs:** a scheduled GitHub Actions workflow, Monday, Wednesday and Friday morning (F2-09). The Anthropic API key exists only as a secret of that workflow.
- **What it does:**
  1. Collect candidates from the ADR-001 sources: journals through their feeds and PubMed, and bodies and news through web search restricted to the ADR-001 domains. Collection is deterministic, keeps a record of URLs already seen, and runs without the model (F2-11).
  2. Send the candidates to the model, which triages them and writes the summaries. It returns structured output only, never a file or a command (F2-12). Two calls (amended 2026-11-27, G0): the first searches the tier 2 domains and returns notes; the second ranks the candidates and the search items and writes the summaries. The script, not the model, fills the edition slots from the ranking and keeps the selection log.
  3. Turn that output into the edition's `.md` file and check each item before any push (F2-13): the link matches a candidate of the run and resolves, tier 1 numbers appear in the abstract or fetched text, tier 2 items carry no numbers, a dose screen and the F1-06 names check pass. A failing item is dropped and named.
  4. Open the PR through the project's GitHub App and turn on GitHub's auto-merge (F2-05). From there, the ADR-003 path applies: required checks on the PR, then Cloudflare Pages.
- **Budget:** at most US$30 a month on the API, for every run: scheduled, development, eval and reruns. Split (amended 2026-11-26, D7):

  | Share | Rule |
  | --- | --- |
  | Scheduled runs | F0-08's measured run cost × 13 |
  | Development and eval runs | Message Batches API on recorded inputs |
  | Reserve | The rest; reruns come out of it |

  Three limits back it. The per-run cap in the script checks each request's worst case (input, `max_tokens` and the search `max_uses`) before sending it, and stops the run without opening a PR (F2-12). The API account has a monthly spend limit (F0-08). The production key gets its own workspace spend limit if the Console offers one; otherwise the script checks the month-to-date spend before each run. Every run records its tokens, searches and estimated cost, per run and per accepted edition.
- **Tier 2 items:** guidelines, alerts and news found by search carry no numbers except dates until F3-07 grounds them in fetched page text (amended 2026-11-26, D3). ADR-002's rule that every number is grounded still holds, because these items carry none. ADR-001's tier 2 sources do not change.
- **Untrusted input:** fetched pages and search results are data. The model has no tool that writes to the repository, and the script accepts only the fields of the output schema.

## Alternatives considered

| Option | Pros | Cons | Why not (if rejected) |
| --- | --- | --- | --- |
| Script calling the Claude API from GitHub Actions (chosen) | Reproducible, testable and versioned; the prompt and checks live in the repo; the cost is measured per run | Code to write and maintain; costs money | — |
| Grok scheduled routine (final plan) | Plan already paid for; no code | Unverified ability to reach GitHub; prompt and output outside the repo; hard to test | Replaced by Filipe's decision to move to Claude |
| Claude Code cloud scheduled task | No API cost on the subscription | Harder to pin, test and run in CI; tied to a personal account | Rejected for the pipeline; can still help during development |
| Claude Opus 5.5 as the starting model | Strongest summaries | About twice Sonnet's cost | Filipe chose to try Sonnet first; Opus remains the fallback if the eval shows a gap |
| Open web search without a source list | No list to maintain | Weak sources and invented articles become more likely in an unreviewed site | Rejected (ADR-001) |

## Consequences

- The cost rule changes: from "zero until the domain" to "only the Claude API, up to US$30 a month, until the domain" (AGENTS.md §1 and §8).
- New issues: F0-08 (cost and quality spike), F2-10 to F2-15 (App, collection, generator, grounding, budget, failure alert) and F3-05 (eval set). F0-02 and F2-06 are withdrawn. The 2026-11-26 review merged or cut several of these; each withdrawn row in `ROADMAP.md` names where its acceptance went.
- The Anthropic API key and the GitHub App private key are new secrets. Both appear in the operations guide (F2-07), with how to revoke them.
- The generation prompt and its validators are Hi-risk areas in the project's "Agent workflow" block.
- Every real API call costs money. F0-08 and any rerun outside the schedule need Filipe's go-ahead.

## Evidence

Filipe's decision in the F0-07 planning thread on 2026-11-25: Claude via the API, Sonnet first, news in the MVP, up to US$30 a month. The cost estimate in the plan (about US$10 a month on Sonnet for 13 runs) is an estimate from token assumptions, not a measurement; F0-08 replaces it with a measured figure.

The amendment comes from Filipe's decisions of 2026-11-26 on the plan review (D3, D6 and D7 in [`docs/plan-review-2026-11-26.md`](../plan-review-2026-11-26.md)): Python from the F0-08 trial, because tested code exists and the site toolchain validates the file anyway; the budget split; tier 2 items without numbers.

F0-08 measured the cost on 2026-11-27 ([`docs/spikes/F0-08-api-trial.md`](../spikes/F0-08-api-trial.md)). A two-call run with 37 candidates and 8 searches cost US$0.348, US$4.52 a month at 13 runs, and the Console billed what the script computed (US$0.49 over three runs). Filipe approved the trial edition with Sonnet 5.5 and set the edition slots; gate G0 passed. The API accepted search and structured output in one call, but the workspace's web search limit was 0 at the time, so no search ran in it; Filipe chose two calls, and how one call behaves with working search is unmeasured.

## Revisit when

- F0-08 or F3-02 measures a monthly cost above US$30, or gate G0 projects more than US$20 a month (its redesign band).
- G0 or F3-03 shows that tier 2 items need figures (F3-07).
- The eval set (F3-05) shows Sonnet falls short of what the main user needs.
- Anthropic changes the price or retires the model.
