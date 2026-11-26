# ADR-0004: Edition generation by the Claude API

| Field | Value |
| --- | --- |
| State | `aprovado` |
| Opened | 2026-11-25 |
| Decided | 2026-11-25 (Filipe, in the F0-07 planning thread) |
| Owner | Filipe (product owner) |
| Index ID | ADR-004 |
| Related issues | F0-07, F0-08, F2-02, F2-10 to F2-15, F3-01, F3-02 |
| Replaces | The Grok scheduled routine from the final plan (F0-02, F2-06) |
| Replaced by | — |

## Context and problem

The final plan had a Grok scheduled routine write each edition, with an unverified ability to reach the GitHub API (F0-02). Filipe is moving the whole workflow to Claude and accepts paying for the Claude API, up to US$30 a month. The scope also grew: besides journal articles, an edition carries guidelines, alerts and news that affect pediatrics, and news is part of the MVP.

The site publishes without review (ADR-002), so whatever generates the edition must be reproducible, cheap to rerun and constrained by checks the project owns.

## Decision

- **Who writes:** a script in this repository calls the Claude API. The starting model is Claude Sonnet 5.5 (`claude-sonnet-5-5`). Changing the model is a config change, measured against the eval set (F3-05) before it is merged.
- **Where it runs:** a scheduled GitHub Actions workflow, Monday, Wednesday and Friday morning (F3-01). The Anthropic API key exists only as a secret of that workflow.
- **What it does:**
  1. Collect candidates from the ADR-001 sources: journals through their feeds and PubMed, and bodies and news through web search restricted to the ADR-001 domains. Collection is deterministic, keeps a record of URLs already seen, and runs without the model (F2-11).
  2. Send the candidates to the model, which triages them and writes the summaries. It returns structured output only, never a file or a command (F2-12).
  3. Turn that output into the edition's `.md` file, check that every number and link is grounded in the fetched source (F2-13) and open the PR through the project's GitHub App (F2-10).
  4. From there, the ADR-003 path applies unchanged: PR validation, automatic merge, Cloudflare Pages.
- **Budget:** at most US$30 a month on the API. Two limits back it: a per-run cap in the script, which stops the run without opening a PR (F2-14), and the monthly spend limit on the API account (F0-08). Every run records its tokens, searches and estimated cost.
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
- New issues: F0-08 (cost and quality spike), F2-10 to F2-15 (App, collection, generator, grounding, budget, failure alert) and F3-05 (eval set). F0-02 and F2-06 are withdrawn.
- The Anthropic API key and the GitHub App private key are new secrets. Both appear in the operations guide (F2-08), with how to revoke them.
- The generation prompt and its validators are Hi-risk areas in the project's "Agent workflow" block.
- Every real API call costs money. F0-08 and any rerun outside the schedule need Filipe's go-ahead.

## Evidence

Filipe's decision in the F0-07 planning thread on 2026-11-25: Claude via the API, Sonnet first, news in the MVP, up to US$30 a month. The cost estimate in the plan (about US$10 a month on Sonnet for 13 runs) is an estimate from token assumptions, not a measurement; F0-08 replaces it with a measured figure.

## Revisit when

- F0-08 or F3-02 measures a monthly cost above US$30.
- The eval set (F3-05) shows Sonnet falls short of what the main user needs.
- Anthropic changes the price or retires the model.
