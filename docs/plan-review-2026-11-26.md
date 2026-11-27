# Plan review of 2026-11-26

Four agents reviewed PedsLetter's plan on 2026-11-26: three critics, S (security and risk), P (performance) and M (minimalist), and one that combined their findings into this plan. Nothing paid was run. D1–D13 are Filipe's decisions of 2026-11-26 (section 5): D2–D13 as recommended, D1 decided otherwise. This version applies them.

This is a history document, like [`project-genesis.md`](project-genesis.md). The current scope, acceptance and decisions live in [`ROADMAP.md`](../ROADMAP.md), [`DECISIONS.md`](../DECISIONS.md) and the ADRs, which F0-09 updated from it. How to read the IDs: S1–S14, P1–P13 and M1–M11 are the critics' recommendations, each with its ruling in section 4; U marks a fact the critics could not check; G0–G3 are the gates. The critics' own reports are not in the repository. `file:line` references point to the files as of commit `e654153`; `trial.py` and the spike doc are on the F0-08 branch.

**Update of 2026-11-27 (F0-09).** GitHub's docs list the actors a ruleset can exempt: repository roles, teams, GitHub Apps and Dependabot. Actions' `GITHUB_TOKEN` is not one of them, so D9's job commit could not pass the "PR required" ruleset planned for F0-01. Filipe chose instead: the job opens the PR with the GitHub App token and turns on GitHub's auto-merge, and the required checks gate the merge. Where this document says job commit, `GITHUB_TOKEN` or "F2-10 withdrawn" for publishing, ADR-003 and the roadmap now say App PR with GitHub's auto-merge, and F2-10 merged into F2-05.

**Verification.** Every `file:line` behind a change was opened and holds; M2's count (27 open issues before the first published edition, 14 Hi, 23 plan stops; P6 says 25) re-checks against `ROADMAP.md:76-157`. The claude-api skill's cached docs support P5's server loop, P3's Batches discount, U7 and U8, which stay checks in their issues. Estimates keep their reviewer label.

## 1. Executive summary

The architecture holds: model-free collection, one structured-output call, a static zero-JavaScript site, two spend limits. The order and the gates do not.

1. F0-08 runs on a production-like setup with capped trial credits, and Filipe judges the edition alone (gate G0). The MVP goes live without the main user's check, as ADR-002 planned; the main user's answer stays in F3-03 (D1).
2. The first published edition comes after 11 issues, not 27: adjacent issues merge, and under the phase-gate waiver (D5) Filipe merges the first editions by hand.
3. One pre-push gate fails closed per item: names, a dose screen, tier 1 numbers, no numbers in tier 2 items, DOI registration, provenance. Nothing unchecked is pushed, and one bad item no longer sinks an edition.
4. The repository is hardened, and a job commit of validated editions with `GITHUB_TOKEN` replaces the GitHub App and auto-merge (D9). Changed on 2026-11-27: see the update above.
5. Caching, Batches for development runs and a worst-case pre-check protect the US$30 limit.

## 2. Final plan

**Goal (unchanged):** three editions a week of AI summaries of pediatric literature, guidelines, alerts and news for the main user, on a static non-indexed site; the only cost is the Claude API, up to US$30 a month (`AGENTS.md:5-13`, ADR-004).

**MVP (phases 0–3):** unchanged in substance; tier 2 items carry no numbers until their page text is grounded (S1); RSS conditional and analytics deferred (D10). **After the MVP:** domain (D13), calculators behind gate G3, phase 9 unchanged.

### (a) The F0-08 trial

| ID | Change | Expected Risk/Size | Acceptance delta |
| --- | --- | --- | --- |
| F0-08 | Modify | Hi/Sm (same) | Add: trial-only credits, auto-reload off (U5), key revoked after (S9); caching on; 3–6 items in the four-section body (`overview.md:88-93`); only allow-listed links fetched (S12); wall-clock, effort and Console billing recorded (P4, P5, U8); free replay of 8 weeks of Mon/Wed/Fri PubMed windows, with a per-window projection beside ×13 (P8). A 400 on search plus structured output (U7) makes the allowed rerun split search from writing (S1). Filipe reads the edition and records the verdict (`ROADMAP.md:83`); the main user does not see it (D1). Exit: G0 |

### (b) To the first published edition

| ID | Change | Expected Risk/Size | Acceptance delta |
| --- | --- | --- | --- |
| F0-01 | Modify; runs while F0-08 waits for credits | Lo→Med/Sm | Add: Pages linked; free-plan limits checked (`PROJECT_STATUS.md:86`); `main` ruleset (PR required, no force push or deletion), with the generation job as its only bypass (D9; whether a ruleset can exempt that job is unverified, and the answer shapes F2-05); read-only default token; push protection (U11); U1 recorded (S5) |
| F0-09 | Add | Lo/Md | Docs only: records this plan's approved parts in `ROADMAP.md`, the ADR index and status; fixes F0-08's status mismatch (`ROADMAP.md:83` vs `PROJECT_STATUS.md:49`, M9). D2–D13 decided on 2026-11-26, so it can start now; G0's outcome is added when known |
| F1-01 (+F1-02) | Merge | Med→Hi/Sm | Adds F1-02; no fork previews (U4); previews keep `noindex` (S13); Actions pinned by SHA with Dependabot, step-level secrets, `persist-credentials: false` (S10) |
| F1-06 | Modify; moved to right after F1-01 | Hi/Sm | A missing or empty names secret fails; output gives file, line and term index only (S4); callable by the job before any push; a local pre-commit hook takes names from an environment variable, never a file (§4, S3) |
| F1-03 | Modify | Hi/Sm | The walker also asserts the §4 notices and no `<script>` outside calculators (P12); CSP `script-src 'none'` in `_headers` (S7) |
| F1-04 (+F1-05, F1-07) | Merge | Lo→Hi/Md | Keeps every F1-05 and F1-07 line; raw HTML in `.md` escaped, shown by a fixture (U3, S7); one manual Lighthouse run (M6) |
| F2-01 | Modify | Med/Sm | Add: `url` is `https://` on an ADR-001 host (S7) |
| F2-11 (+F2-04) | Merge | Med→Hi/Md | From the spike collector (M3, D6); used URLs read from `src/content/posts/`; a withdrawn edition's URL fails; path-scoped tier 2 domains pinned to a host such as `www.gov.br`, so the gate does not rely on U6 (S1); replayed windows as fixtures (P8) |
| F2-12 (+F2-14, F2-02 prompt) | Merge | Hi/Md (Lg if D6 picks TypeScript; estimate) | From the spike (M3). Caching, `cache_read_input_tokens` > 0 logged (P5); model, effort, `max_tokens` in `src/config/` (P11); YAML serializer (S7); hash-locked dependencies (S10); dispatch only until F2-09. No request whose worst case (input + `max_tokens` + `max_uses`) breaks the per-run cap; cap × 13 plus reruns under the monthly limit; production key in its own workspace and limit if offered (U5), else a month-to-date guard (S9, P3, D7). Logs and PR text carry counts and IDs, never raw output; artifacts keep inputs and validated editions (S4, M8) |
| F2-13 (+F2-03, F2-02 check) | Merge | Hi/Md | Runs in the job before any push (S3). Per item: URL and title bound to one candidate or search result (S1); tier 1 numbers in the abstract; tier 2 items carry no numbers but dates (S1); dose screen on every field (S2, D8); F1-06 names; DOI registered at doi.org, PMID via E-utilities, allow-listed tier 2 page with one retry (S12, P2, M7). Failing items drop, named; under 3 items, no edition (P1). Fixtures with an off-list URL, a dose, a name, raw HTML and an unsupported number are each blocked, no API call (S8). F2-02's check: three recorded windows, sent as one Message Batch, pass every check (P3) |

With D5, the first edition publishes after F2-13: Filipe dispatches the run, uploads the validated file (`ADR-0003:25`) and merges after CI; withdrawal meanwhile is deletion or a Pages rollback (`ADR-0003:36-37`). That makes 11 issues instead of 27; without D5, 14 to 16.

### (c) To MVP close

| ID | Change | Expected Risk/Size | Acceptance delta |
| --- | --- | --- | --- |
| F0-05 | Modify | Lo/Sm | ADR-003 records the job-commit path (D9) and its ruleset exemption, with S6's controls as the fallback; `proposed` until F2-09 |
| F2-05 (+F2-10) | Merge; job commit (D9) | Hi/Sm | The generation job commits only what F2-13 passed, with a job-scoped `GITHUB_TOKEN`; Pages builds on that push (M4, unverified); the F0-01 ruleset exempts only this job, and named required checks still guard every PR, tested against a skipped job (U2, S5); F2-10 withdrawn. If the ruleset cannot exempt the job, the App path with S6's controls goes back to Filipe |
| F2-07 (+F2-08) | Merge | Hi/Sm | Guide order: pause the schedule, roll back, fix the repository; one key-revocation drill (S13) |
| F2-09 (+F3-01) | Merge | Hi/Sm | Schedule plus dispatch only, `concurrency` 1, `timeout-minutes` (S9); a second cron 2–3 h later exits if the day's edition exists (P10); one forced failure shows whether GitHub's notice reaches Filipe (M7) |
| F2-15 | Cut | — | Restored if that notice does not arrive (M7) |
| F1-08 | Modify; conditional (D10) | Lo→Hi/Sm | Only for a feed reader: title, link and AI notice per item; last 20 editions; `X-Robots-Tag` on the feed (S11, S13, P12) |
| F1-09 | Defer (D10) | — | Drop recommended |
| F3-02 | Modify | Med/Sm | Adds errors found per edition (Filipe's read; no main-user ratings before F3-03, D1) and dropped items with reasons (M10, P1) |
| F3-03 (+F3-06) | Merge | Lo/Sm | The main user's answer, as planned (`ROADMAP.md:192`); one record of usage, sources and model; gate G2 |
| F3-05 | Defer | — | Built before the first model or prompt change after F3-03; Batches; model × effort by cost per accepted edition (M8, P11); `ADR-0004:22` still binds |
| F3-04 | Defer to phase 5 | — | After F5-02 (M6) |

MVP close: 17 issues (19 with F1-08 and F1-09) against 32 open today. Under D9's job commit, phase 2's outside-author line (`ROADMAP.md:131`) goes.

### Later phases

- **Phase 4:** F4-01 Med→Hi: registrant not a health professional; published registrant data checked (S11, U9).
- **Phase 5:** new F5-07 "Calculator demand check" (Lo/Sm) first (G3, M11); F5-01 measures the island runtime against 30 kB gzip (P13); F5-02 rejects ambiguous separators ("3.450") and echoes value and unit; F5-06 adds verbatim worked-example cases; `connect-src 'none'` on calculator pages (S14); the engine is extracted at the second calculator (M11).
- **Phase 6:** F6-02 waits on D13; F6-03 loads both sexes' data before input (P13). **Phases 7–8:** parked until G3. **Phase 9:** unchanged.
- **Conditional F3-07** "Tier 2 numbers grounded in fetched text" (Hi/Md, estimate), if G0 or G2 shows tier 2 items need figures; P9's feeds are weighed there.

### Metrics and gates

| Metric | Target (proposed, D12) | Measured by |
| --- | --- | --- |
| Use (deciding) | The main user reads the summaries at least 3 times a week and says whether they help (`ROADMAP.md:52`); asked in F3-03, with no per-edition ratings before it (D1) | F3-03 |
| Errors | Zero misleading errors past the checks; withdrawals per month (`ROADMAP.md:51`) | F3-02 log |
| Cadence | At most 2 missed dates a month: `ROADMAP.md:49` restated, since Mon/Wed/Fri give 12–14 dates by calendar, 13 on average (`trial.py:40`) | Commits on `main` |
| Automation | At least 80% without Filipe (`ROADMAP.md:50`), from F2-09 | Merge author |
| Cost | Under US$30 a month in total; per run and per accepted edition (P11) | Job summary, Console |
| Technical | Walker green on every page; Lighthouse 95 from phase 5 | CI |

| Gate | Versus M | When (proposed) | Evidence | Decision |
| --- | --- | --- | --- | --- |
| G0 | Adapted: Filipe's read, not the main user's (D1); cost bands added | After F0-08; 2026-12-11 (M) | Filipe's verdict (`ROADMAP.md:83`), run cost, U7, replay counts | Stop or re-plan if Filipe judges the edition not worth publishing; fix the prompt if under 2 items are worth reading; re-plan tier 2 (D3) if its items add nothing. Bands (P, D2): up to US$10 a month proceed; US$10–20 tune F2-12; above US$20 redesign |
| G1 | Adapted: re-plan, not drop the site | First published edition; 2027-02-05 (M) | Stretch (b) done | If missed, Filipe re-plans (tier 1 only, manual publishing) or stops |
| G2 | Adapted: the main user's answer in F3-03 (D1); phase 9 left to Filipe | F3-03, after two weeks of operation (F3-02) | F3-02 log (errors, drops, cost) and the main user's answer (`ROADMAP.md:192`) | Continue, adjust or stop, recorded in F3-03. From the first published edition: pause after one misleading error past the checks; after a second, Filipe chooses stop or phase 9 review |
| G3 | Adapted: Filipe decides | Before phase 5 (F5-07) | A calculator the main user would use weekly that their current tool lacks | Otherwise Filipe decides whether phases 5–8 stay |

## 3. Debate log

| Topic | Security | Performance | Minimalist | Ruling | Why |
| --- | --- | --- | --- | --- | --- |
| Tier 2 first | Fetch text or no numbers; drop accepted (S1) | Feeds first (P9) | Tier 1 only until G0 (M5) | Tier 2 kept with no numbers and host pins; tier 1 first; rest in D3 | Scope is Filipe's; the rule closes S1 cheaply |
| Publishing path | Harden App and auto-merge (S5, S6) | Filipe merges meanwhile (P6) | Job commit with `GITHUB_TOKEN` (M4) | Job commit (D9) with the ruleset bypass checked in F0-01; interim merge (D5); both approved | Removes the App key and the privileged PR workflow |
| Failure granularity | Fail closed before push (S3) | Drop bad items, keep 3 (P1) | Smaller editions fine | Per-item drop in the pre-push gate; CI keeps the edition backstop | Nothing unchecked ships; editions survive one bad link |
| F0-08 scope | Trial credits, key revoked (S9) | Production setup, caching, replay (P4, P5, P8) | Reader rates it; second run (M1) | All free or one-line changes; Filipe rates it, not the main user (D1); second run only if a band flips | Only paid measurement before phase 2; the main user joins after the MVP goes live |
| Cost work timing | Worst-case bound (S9) | Caching, Batches, budget table (P3, P5) | Nothing until US$20 a month | Caching, Batches, bound now; other levers on measured spend | A tuning month is about US$40, estimate (P3), against a hard US$30 |
| Issue count | Distinct §4 checks; higher ratings (S11) | Issue-level dependencies (P6) | 12 merged steps (M2) | Merge adjacent issues; F1-03, F1-06, F2-13 stay separate | Fewer plan stops, undiluted §4 reviews |
| Spike reuse | Hash-locked dependencies (S10) | Language open (P's question 8) | Promote, keep Python (M3) | Reuse with review; language in D6 | About 740 tested lines exist (`21ed2e9`) |
| Link checks | Handle API, allow-listed fetch (S12) | DOI API, one retry (P2) | DOI registration in F2-13 (M7) | Merge F2-03 into F2-13; tier 2 retried once, then dropped | Publishers refused the script (spike doc :14) |
| Failure alert | No leaks (S4) | Alert after last attempt (P10) | Cut F2-15 (M7) | Cut; F2-09 forces one failure | Platform notice (unverified) gets tested |
| Eval set | — | Batches, model × effort (P3, P11) | Defer (M8) | Defer to the first model or prompt change | One reader reads every edition |
| Zero JS, analytics | CSP (S7) | Walker; F1-09 needs an exception (P12) | Cut F1-09; Lighthouse later (M6) | Walker and CSP now; F3-04 to phase 5; F1-09 in D10 | A test and a header enforce §5 |
| Future phases | Calculator guards (S14) | Runtime measured (P13) | Demand check; domain later (M11) | Guards now; runtime at phase 5; G3; domain in D13 | Building waits for demand |

## 4. Recommendation ledger

| ID | Decision | Lands in | Reason |
| --- | --- | --- | --- |
| S1 | adapt | F2-11, F2-12, F2-13 | No numbers in tier 2 items closes the gap in scope |
| S2 | adopt | F2-13, D8 | Deterministic dose screen; a hit drops the item |
| S3 | adopt | F2-13, F1-06; `AGENTS.md:89` in D12 | Checks before any push; hook reads names from the environment |
| S4 | adopt | F1-06, F2-12 | Logs carry indexes, not terms; a missing secret fails |
| S5 | adopt | F0-01, F2-05 | Ruleset now; named required checks once checks exist |
| S6 | adopt | F2-05 | Known auto-merge traps become acceptance lines |
| S7 | adopt | F1-03, F1-04, F2-01, F2-12 | Serializer, host allow-list, escaped HTML, CSP: all cheap |
| S8 | adopt | F2-13 | Tests the gate, not the model, with no API spend |
| S9 | adopt | F0-08, F2-12, F2-09 | Trial credits capped now; worst-case bound; one run at a time |
| S10 | adopt | F1-01, F2-12 | Applies `AGENTS.md:107` pinning to Actions and the generator |
| S11 | adopt | F2-11, F2-13, F1-08, F4-01 ratings | The project's own Hi list names them |
| S12 | adopt | F2-13, F0-08 | DOI registration avoids publisher blocks; allow-listed fetches only |
| S13 | adopt | F1-01, F1-08, F2-07 | Rollback order, revocation drill, no fork previews |
| S14 | adapt | F5-02, F5-06; F6-02 in D13 | Guards now; a dose ceiling needs Filipe |
| P1 | adopt | F2-13 | Per-item drop protects cadence; nothing unchecked publishes |
| P2 | adopt | F2-13 | Same fix as S12 and M7 |
| P3 | adapt | F2-12, F2-13; split in D7 | Batches for development; a budget split amends ADR-004 |
| P4 | adapt | F0-08 | Production-like trial; bands left to Filipe |
| P5 | adopt | F0-08, F2-12 | Small change, recurring saving; server tools reuse the cache |
| P6 | adopt | D5 (approved) | Waiver and interim merge approved by Filipe |
| P7 | reject | D1 (Filipe) | Same as M1 |
| P8 | adopt | F0-08, F2-11 | Free replay sizes windows and cadence |
| P9 | defer | F3-07, D3 | Amends approved ADRs; trigger: search share of cost, G0 |
| P10 | adopt | F2-09 | A cheap retry protects cadence |
| P11 | adapt | F2-12, F3-05 | Config now; comparison once an eval exists |
| P12 | adapt | F1-03, F1-08, D10 | Walker enforces zero JS; Lighthouse waits for phase 5 |
| P13 | defer | F5-01, F6-03 | Measured at phase 5 start, if G3 passes |
| M1 | reject | D1 (Filipe) | The MVP goes live without the main user's check; their answer stays in F3-03 |
| M2 | adapt | Stretches (b) and (c) | Merge adjacent issues; §4 checks keep their own issues |
| M3 | adapt | F2-11, F2-12, D6 | Reuse with review; a rewrite buys nothing measured |
| M4 | adopt | D9 (approved), F0-05, F2-05 | Approved; F0-09 edits `AGENTS.md` §5 and §13 and ADR-003 |
| M5 | adapt | F2-13, D3 | The no-number rule keeps scope; tier 1 built first |
| M6 | adapt | F1-04, phase 5, D10 | No decision depends on visit counts yet |
| M7 | adopt | F2-13, F2-09; F2-15 cut | DOI registration; platform notice tested once |
| M8 | adopt | F3-05, F2-12 | The reader is the eval until a model change |
| M9 | adapt | F0-09, D12 | Mismatch fixed now; trimming edits `AGENTS.md` §12 |
| M10 | adapt | Metrics, F3-02, F3-03, D12 | Thresholds become proposals; 12 versus 13 dates reconciled |
| M11 | adapt | F5-07, G3, D13 | Demand check first; domain timing is scope |

## 5. Filipe's decisions (2026-11-26)

D2–D13 approved as recommended; D1 decided otherwise. Ordered by the first work each blocks.

1. **D1. Trial reader (F0-08).** *Decided:* Filipe judges the trial edition alone, as `ROADMAP.md:83` already says. The MVP goes live without the main user's check (ADR-002). The first users are Filipe and the main user; the main user's answer comes in F3-03 (`ROADMAP.md:192`), and the clinical review stays in phase 9, before the public release.
2. **D2. Trial setup (F0-08).** Trial-only credits, auto-reload off, key revoked after; the stretch (a) changes; P's cost bands; a second paid run on a 2–3 day window. *Approved:* all but the second run, which waits for a per-window projection in another band (US$3 cap, spike doc :9).
3. **D3. Tier 2 (G0, F2-11).** Keep with no numbers; defer past G0 (reverses the 2026-11-25 scope); text grounding (F3-07); feeds first (amends ADR-001, ADR-004). *Approved:* keep, tier 1 first; defer if U7 forces a split call or Filipe's G0 read finds the tier 2 items add nothing.
4. **D4. Cadence (G0, F3-01).** Three editions a week of at least 3 items (`ROADMAP.md:162`), fewer editions, or a lower minimum. *Approved:* decide at G0 from the replay counts.
5. **D5. Phase-gate waiver (after F1-01).** Issue-level dependencies under a `DECISIONS.md` waiver (`ROADMAP.md:15`), with you merging dispatched editions until the job commit exists (F2-05, D9); or keep the gate. *Approved:* waiver; same checks, 11 issues instead of 14–16.
6. **D6. Pipeline language (F2-11).** Python from the spike, hash-locked, or TypeScript sharing the Astro schema; either edits `ROADMAP.md:64`. *Approved:* Python; tested code exists, and the site toolchain validates the file anyway.
7. **D7. Budget split (F2-12).** Amend ADR-004 to split the US$30 (scheduled, development and eval, reserve); production key in its own workspace. *Approved:* scheduled = F0-08's run cost × 13; development and eval via Batches; the rest reserve.
8. **D8. Dose-screen hit (F2-13).** Drop the item, or park the edition for you. *Approved:* drop; count drops in F3-02.
9. **D9. Publishing path (F0-05, F2-05).** Hardened App PR with auto-merge, or a job commit with `GITHUB_TOKEN` (edits `AGENTS.md:53`, `:97`, `:102`, `:183` and ADR-003). *Approved:* job commit: no private key, a smaller issue, no privileged workflow on pull requests. *Changed on 2026-11-27 (F0-09):* a ruleset cannot exempt `GITHUB_TOKEN`, so Filipe chose the App PR with GitHub's auto-merge. It keeps the App's private key and still needs no privileged workflow on pull requests.
10. **D10. RSS and analytics.** F1-08 only for a feed reader; F1-09 dropped, or kept with a §5 exception for a beacon script (unverified). *Approved:* Filipe settles F1-08 before it starts (how the main user reads is a habit question, not a content check); drop F1-09.
11. **D11. Repository visibility.** Public (free CI, "show the work", `docs/project-genesis.md:14`) or a private editions repository; does §4 cover your posts about the project? *Approved:* public; yes.
12. **D12. Rules, docs, metrics (F0-09).** Correct `AGENTS.md:89` once U1 is checked; trim status docs (`AGENTS.md:166-170`); narrow "Hi risk here" (`AGENTS.md:61`) or not; approve section 2's metrics and dates. *Approved:* yes, yes, keep the list, approve.
13. **D13. Later phases.** Domain in phase 9 or after F3-03; G3 before phase 5; F6-02 with S14's guards or in phase 9. *Approved:* domain in phase 9 unless the main user wants a stable address; G3 yes; F6-02 in phase 9 (a ceiling needs drug data).

## 6. Risks the final plan accepts

| Risk | Why accepted | Evidence that reopens it |
| --- | --- | --- |
| No main-user signal before F3-03: until then, errors past the checks surface only through Filipe's read | Filipe's D1; ADR-002 publishes without review | An error report from any reader; a withdrawal |
| A grounded number attached to the wrong claim goes live (`ADR-0002:45`) | Approved ADR-002 | A misleading error past the checks (G2); rising withdrawals (`ADR-0002:59`) |
| Tier 2 items lose their figures | Cheapest S1 control in scope | Filipe's read or the main user's F3-03 answer flags missing figures: open F3-07 |
| The dose screen drops relevant items | §4 fails closed | The main user asks for dropped items; drop counts in F3-02 |
| A dead publisher page behind a registered DOI | Publishers block scripts (spike doc :14) | The main user reports a dead link |
| Pushed content is visible on GitHub (`ADR-0002:46`; PR refs, U1) | Public repository by decision | Any §4 hit in a branch, PR, log or artifact: D11 |
| No dedicated failure alert | GitHub's notice, checked in F2-09 | A failed run unnoticed on a scheduled date |
| Spike shortcuts reach production (`trial.py:234`) | Review in each issue | A reviewer finding still open after two rounds |
| One paid data point before phase 2 (spike doc :53) | US$3 trial cap | F3-02 spend outside F0-08's band |
| Bigger Hi PRs after merges | Fewer plan stops | A §4 regression found after a merge |

## 7. Next three actions

1. The agent plans the stretch (a) changes to F0-08 (Hi/Sm: plan, `po-reviewer`, Filipe's approval), then applies them on `feat/F0-08-api-trial`, extends and runs the unit tests and the dry run, and runs the free window replay.
2. Filipe buys trial-only credits with auto-reload off, sets the US$30 monthly limit, creates a trial key and authorizes the run; the agent runs it once; Filipe reads the edition and records the G0 verdict; the key is revoked; F0-08 records the figures and U7.
3. While the run waits for credits, at no API cost: F0-01 (Pages link, free-plan limits, ruleset with the job's bypass checked, read-only token, push protection, U1) and F0-09, which records D2–D13 in `ROADMAP.md`, the ADRs and `AGENTS.md`.
