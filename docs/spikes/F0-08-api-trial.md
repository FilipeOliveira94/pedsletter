# F0-08 — Cost and quality trial of the Claude API

| F0-08 | Detail |
| --- | --- |
| State | In progress: script, tests and replay done; paid run pending API credits |
| Rating | Risk Hi (raised from Med: the API key and the spend cap), Size Md (raised from Sm on 2026-11-27: about 1,000 hand-written lines) |
| Script | [`spikes/F0-08/trial.py`](../../spikes/F0-08/trial.py). F2-11 to F2-13 start from it and review the part each takes (D6) |
| Model | `claude-sonnet-5-5`, effort `high` (set explicitly), `max_tokens` 32000, prompt caching on |
| Trial cap | US$3 in total, one paid run, one rerun only for the U7 split (Filipe, 2026-11-26; plan review D2) |
| Exit | Gate G0 (`ROADMAP.md`), target 2026-12-11 |

## Setup

- **Account (Filipe):** trial-only credits with auto-reload off, the US$30 monthly limit and a trial key. The run waits for Filipe's explicit go once these are set. After the run, the key file is deleted and Filipe revokes the key in the Console.
- **Tier 1 candidates:** PubMed E-utilities over the ADR-001 journals, entries from the last 7 days with an abstract; letters, comments, editorials, news and errata excluded; general journals (NEJM, JAMA, The Lancet, BMJ, Cochrane) filtered to pediatric terms. At most 8 items per pediatric journal, 5 per general journal, 40 in total, taken one journal at a time so no journal crowds out the others. Authors are not read.
- **Why PubMed and not feeds:** on 2026-11-26 the journal feeds that answered (JAMA Pediatrics, JAMA, Archives of Disease in Childhood, The Journal of Pediatrics, Jornal de Pediatria, Pediatrics) carried titles but no abstracts, and the feeds of The Lancet, NEJM, Cochrane and BMJ answered 403 or 404 to a script. The model needs the abstract to summarize and the number check needs it too. ADR-001 already names PubMed for tier 1.
- **Tier 2:** server-side web search (`web_search_20260209`), restricted to the ADR-001 tier 2 domains, at most 8 searches.
- **One call, or two (U7):** the run first tries search and structured output (`output_config.format`) in one request. If the API rejects that with a 400 (not billed), the one allowed rerun splits it: call A searches and returns plain-text notes, call B gets the notes as data and returns the structured edition with no tools. A credit error never triggers the split.
- **Edition:** the production format in [`overview.md`](../architecture/overview.md) "Edition format": YAML frontmatter and, per item, **Por que importa**, **O que foi feito**, **Resultado** and **Limitações**; 3 to 6 items; both §4 notices in the body. It is written to the git-ignored `spikes/F0-08/out/` and never committed; this report quotes no edition text.
- **Content rules in the prompt:** the roadmap generation rules, with one change Filipe made on 2026-11-27: a dose may appear only as the article states it, attributed to it. D8 as recorded bans any dose; Filipe said that was overlooked, and the D8 record, the roadmap rule and F2-13 are corrected in a separate change.
- **Prices** (pricing page checked on 2026-11-26): Sonnet 5.5 input US$2/MTok, output US$10/MTok, cache write US$2.50/MTok, cache read US$0.10/MTok; web search US$10 per 1,000 searches, with search results billed as input tokens.
- **Spend control:** the SDK's automatic retries are off. Before every request, including each `pause_turn` continuation, the script bounds its worst case and writes it to `out/spend.json` as a reservation; after the request, the reservation is replaced by the tokens actually used. The bound assumes the server-side search loop re-reads the context on every iteration: with 8 searches, the input (characters sent ÷ 3) is counted 9 times, plus 10,000 tokens per search result, all at the cache-write rate, plus the full `max_tokens` and every search. A request whose bound would take the trial past US$3 is refused. A request the API rejects before answering (not billed) releases its reservation; a crash or kill mid-request leaves it on disk, so the cap holds across runs. A continuation resends the request unchanged, as the API documents for `pause_turn`; its bound counts only the searches left, assuming `max_uses` spans the continuations. A connection failure before the response also releases the reservation; a timeout keeps it. To clear a stale reservation by hand, set `out/spend.json` to the last run's recorded total. With about US$0.30 spent on the first turn, a first continuation still fits the cap; a second may be refused, which ends the run without an edition. The key file must live outside the repository.
- **Pre-checks the script runs on the edition (report only; F2-13 is the real gate):** each link is a collected candidate or on a tier 2 domain, and appeared in the run; only allow-listed links are fetched, DOIs at doi.org's handle API; tier 1 numbers appear in the abstract; tier 2 items carry no numbers except dates; a dose screen, with whether the dose is attributed to the article. There is no names screen (F1-06).

## Checks run

- `spikes/F0-08/.venv/bin/python -m unittest discover -s spikes/F0-08`: 48 tests pass. They cover cost and cap, the worst-case bound, the on-disk reservation (released after an unbilled 400, kept after a crash mid-request, blocking a request over the cap before it is sent), the continuation resent unchanged, redirects not followed, journal round-robin, PubMed parsing, schema rejection with no file written, the edition format and both notices, the dose screen and attribution, tier 2 numbers, allow-listed fetches, the U7 split on a fake 400 (with the projection taken from the write call), no split on a credit error or on a 400 after a billed turn, no write call after empty search notes, `pause_turn` continuation with summed usage, the replay windows and the projection.
- `trial.py --dry-run`: renders the synthetic fixture in the production format.
- Real PubMed collection on 2026-11-26 (no API call): 24 candidates from 9 of the 12 journals.
- First paid attempt on 2026-11-26: refused by the API before any processing, "credit balance is too low". Nothing billed; trial spend US$0.00.

## Replay of 8 weeks of windows (P8, free)

`trial.py --replay` on 2026-11-27 counted the PubMed candidates each Mon/Wed/Fri edition would have had, from the previous edition date to the day before, with the run's query and caps. No API call.

| Measure | Value |
| --- | --- |
| Windows | 24 |
| Candidates per window | min 2, median 10, max 21 |
| Windows with fewer than 3 candidates | 2 |

| Edition | Window | Candidates |
| --- | --- | --- |
| 2026-10-02 | 2026-09-30 to 2026-10-01 | 10 |
| 2026-10-05 | 2026-10-02 to 2026-10-04 | 7 |
| 2026-10-07 | 2026-10-05 to 2026-10-06 | 15 |
| 2026-10-09 | 2026-10-07 to 2026-10-08 | 11 |
| 2026-10-12 | 2026-10-09 to 2026-10-11 | 2 |
| 2026-10-14 | 2026-10-12 to 2026-10-13 | 13 |
| 2026-10-16 | 2026-10-14 to 2026-10-15 | 6 |
| 2026-10-19 | 2026-10-16 to 2026-10-18 | 3 |
| 2026-10-21 | 2026-10-19 to 2026-10-20 | 12 |
| 2026-10-23 | 2026-10-21 to 2026-10-22 | 8 |
| 2026-10-26 | 2026-10-23 to 2026-10-25 | 16 |
| 2026-10-28 | 2026-10-26 to 2026-10-27 | 11 |
| 2026-10-30 | 2026-10-28 to 2026-10-29 | 3 |
| 2026-11-02 | 2026-10-30 to 2026-11-01 | 5 |
| 2026-11-04 | 2026-11-02 to 2026-11-03 | 11 |
| 2026-11-06 | 2026-11-04 to 2026-11-05 | 17 |
| 2026-11-09 | 2026-11-06 to 2026-11-08 | 5 |
| 2026-11-11 | 2026-11-09 to 2026-11-10 | 9 |
| 2026-11-13 | 2026-11-11 to 2026-11-12 | 12 |
| 2026-11-16 | 2026-11-13 to 2026-11-15 | 2 |
| 2026-11-18 | 2026-11-16 to 2026-11-17 | 21 |
| 2026-11-20 | 2026-11-18 to 2026-11-19 | 21 |
| 2026-11-23 | 2026-11-20 to 2026-11-22 | 5 |
| 2026-11-25 | 2026-11-23 to 2026-11-24 | 6 |

Entrez dates of past windows can still shift as PubMed indexes late records. The trial run itself uses a 7-day window (24 candidates), wider than any production window, so its cost is an upper bound for one edition; the per-window projection below corrects for that.

## Measured figures

Pending the paid run. `trial.py --project out/<run>` fills the per-window projection.

| Measure | Value |
| --- | --- |
| Input tokens (incl. cache writes and reads) | — |
| Output tokens | — |
| Web searches | — |
| Effort | high |
| Wall-clock time | — |
| One call or split (U7) | — |
| Run cost (computed) | — |
| Console billing for the run (U8) | — |
| Monthly projection, flat (run × 13) | — |
| Monthly projection, per window (replay) | — |
| G0 cost band | — |

## Quality verdict (G0)

Pending. Filipe reads the edition against this checklist and records the verdict:

- Every link resolves and is from an ADR-001 source.
- Every number in a summary appears in the source; tier 2 items carry no numbers except dates.
- Any dose is stated in the article and attributed to it; no dose of our own.
- Summaries are in the model's own words, in pt-BR, with the four sections.
- General-medicine items say how they affect pediatrics.
- Triage: would he have picked these items? How many are worth reading (G0: fewer than 2 means fix the prompt)?
- Do the tier 2 items add anything (D3)?
- Verdict: continue with Sonnet, adjust the prompt, try Opus, or stop.

## Limitations

- One run is one data point; F3-02 measures two weeks.
- The journal feeds are not exercised; F2-11 decides feeds versus PubMed.
- Numbers in tier 2 items cannot be checked against the page: the search results' text is not returned to the script, so the rule is "no numbers but dates".
- The per-window projection splits the run's cost into a fixed part and a per-candidate part by the candidates' share of the first request's characters; output length does not scale exactly with the candidate count.
