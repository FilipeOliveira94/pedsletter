# F0-08 — Cost and quality trial of the Claude API

| F0-08 | Detail |
| --- | --- |
| State | Done: gate G0 passed on 2026-11-27, approved with Sonnet 5.5 |
| Rating | Risk Hi (raised from Med: the API key and the spend cap), Size Md (raised from Sm on 2026-11-27: about 1,000 hand-written lines) |
| Script | [`spikes/F0-08/trial.py`](../../spikes/F0-08/trial.py). F2-11 to F2-13 start from it and review the part each takes (D6) |
| Model | `claude-sonnet-5-5`, effort `high` (set explicitly), `max_tokens` 32000, prompt caching on |
| Trial cap | US$3 in total, one paid run, one rerun only for the U7 split (Filipe, 2026-11-26; plan review D2). Filipe authorized two more runs on 2026-11-27, after the first made no search; spent US$0.494 |
| Exit | Gate G0 (`ROADMAP.md`), target 2026-12-11 |

## Setup

- **Account (Filipe):** trial-only credits with auto-reload off, the US$30 monthly limit and a trial key. The run waits for Filipe's explicit go once these are set. After the run, the key file is deleted and Filipe revokes the key in the Console.
- **Tier 1 candidates:** PubMed E-utilities over the ADR-001 journals, entries with an abstract; letters, comments, editorials, news and errata excluded; general journals (NEJM, JAMA, The Lancet, BMJ, Cochrane) filtered to pediatric terms. Run 1: the last 7 days, at most 8 items per pediatric journal and 5 per general journal, 40 in total. Run 3: the newest 3 items per pediatric journal and 2 per general journal from the last 30 days, plus 1 per journal from 31 to 90 days ago, 45 in total. Items are taken one journal at a time so no journal crowds out the others. Authors are not read.
- **Why PubMed and not feeds:** on 2026-11-26 the journal feeds that answered (JAMA Pediatrics, JAMA, Archives of Disease in Childhood, The Journal of Pediatrics, Jornal de Pediatria, Pediatrics) carried titles but no abstracts, and the feeds of The Lancet, NEJM, Cochrane and BMJ answered 403 or 404 to a script. The model needs the abstract to summarize and the number check needs it too. ADR-001 already names PubMed for tier 1.
- **Tier 2:** server-side web search (`web_search_20260209`), restricted to the ADR-001 tier 2 domains, at most 8 searches.
- **Two calls (since run 3):** call A always searches and returns plain-text notes; call B ranks the candidates and the notes and returns structured output with no tools; the script fills the edition slots from the ranking (see Checks run). If call A bills no search, the run stops before call B.
- **One call, or two (U7), run 1 only:** the run first tries search and structured output (`output_config.format`) in one request. If the API rejects that with a 400 (not billed), the one allowed rerun splits it: call A searches and returns plain-text notes, call B gets the notes as data and returns the structured edition with no tools. A credit error never triggers the split.
- **Edition:** the production format in [`overview.md`](../architecture/overview.md) "Edition format": YAML frontmatter and, per item, **Por que importa**, **O que foi feito**, **Resultado** and **Limitações**; 3 to 6 items; both §4 notices in the body. It is written to the git-ignored `spikes/F0-08/out/` and never committed; this report quotes no edition text.
- **Content rules in the prompt:** the roadmap generation rules, with one change Filipe made on 2026-11-27: a dose may appear only as the article states it, attributed to it. D8 as recorded bans any dose; Filipe said that was overlooked, and the D8 record, the roadmap rule and F2-13 were corrected in F0-11.
- **Prices** (pricing page checked on 2026-11-26): Sonnet 5.5 input US$2/MTok, output US$10/MTok, cache write US$2.50/MTok, cache read US$0.10/MTok; web search US$10 per 1,000 searches, with search results billed as input tokens.
- **Spend control:** the SDK's automatic retries are off. Before every request, including each `pause_turn` continuation, the script bounds its worst case and writes it to `out/spend.json` as a reservation; after the request, the reservation is replaced by the tokens actually used. The bound assumes the server-side search loop re-reads the context on every iteration: with 8 searches, the input (characters sent ÷ 3) is counted 9 times, plus 10,000 tokens per search result, all at the cache-write rate, plus the full `max_tokens` and every search. A request whose bound would take the trial past US$3 is refused. A request the API rejects before answering (not billed) releases its reservation; a crash or kill mid-request leaves it on disk, so the cap holds across runs. A continuation resends the request unchanged, as the API documents for `pause_turn`; its bound counts only the searches left, assuming `max_uses` spans the continuations. A connection failure before the response also releases the reservation; a timeout keeps it. To clear a stale reservation by hand, set `out/spend.json` to the last run's recorded total. With about US$0.30 spent on the first turn, a first continuation still fits the cap; a second may be refused, which ends the run without an edition. The key file must live outside the repository.
- **Pre-checks the script runs on the edition (report only; F2-13 is the real gate):** each link is a collected candidate or on a tier 2 domain, and appeared in the run; only allow-listed links are fetched, DOIs at doi.org's handle API; tier 1 numbers appear in the abstract; tier 2 items carry no numbers except dates; a dose screen, with whether the dose is attributed to the article. There is no names screen (F1-06).

## Checks run

- `spikes/F0-08/.venv/bin/python -m unittest discover -s spikes/F0-08`: 66 tests pass. They cover cost and cap, the worst-case bound, the on-disk reservation (released after an unbilled 400, kept after a crash mid-request, blocking a request over the cap before it is sent), the continuation resent unchanged, redirects not followed, journal round-robin, PubMed parsing, schema rejection with no file written, the edition format and both notices, the dose screen and attribution, tier 2 numbers, allow-listed fetches, the U7 split on a fake 400 (with the projection taken from the write call), no split on a credit error or on a 400 after a billed turn, no write call after empty search notes, `pause_turn` continuation with summed usage, the replay windows, and the projection (input priced uncached, so a run that read the cache cannot give a negative fixed part).
- `trial.py --dry-run`: renders the synthetic fixture in the production format.
- Real PubMed collection on 2026-11-26 (no API call): 24 candidates from 9 of the 12 journals.
- Paid attempts on 2026-11-26 and 2026-11-27: refused by the API before any processing, "credit balance is too low" (the credits first bought sat in the Claude app plan, not the API organization). Nothing billed; trial spend US$0.00.
- Paid run on 2026-11-27 (`out/20261127T190256Z`): one combined call, `end_turn`, 6 items. Trial spend US$0.111.
- `trial.py --project out/20261127T190256Z`: a per-window projection from run 1 (US$2.32 a month), superseded by run 3, whose windows are 30 and 90 days.
- The first run made no search. Filipe then set the flow and the edition slots (2026-11-27): call A always searches, call B ranks articles and search items, and the script fills at most 6 places: up to 2 articles from the last 30 days and 1 from the last 90, 1 guideline from the last 60 days, 2 alerts from the last 30 days, 2 news items from the last 7 days. A category with no item yet takes precedence over a second item of another; places still free go to the next items in rank order. Collection now takes, per journal, the newest records of the last 30 days and of 31 to 90 days ago.
- Second paid run on 2026-11-27 (`out/20261127T220021Z`): 37 candidates collected; call A stopped after 94 s because every web search came back `too_many_requests`, so nothing was billed for search and the script stopped before call B. Run cost US$0.035; trial spend US$0.147. The first run's 73,251 cache-read tokens fit the same pattern: the server-side loop re-reads the context after each failed search.
- Third paid run on 2026-11-27 (`out/20261127T221301Z`), after Filipe raised the workspace's web search limit from 0 to 2 a second: both calls ended with `end_turn`, 6 items. Run cost US$0.348; trial spend US$0.494.

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

Entrez dates of past windows can still shift as PubMed indexes late records. The trial run itself uses a 7-day window (24 candidates), wider than any production window, so its cost was an upper bound for one edition under that design. The slot windows of 2026-11-27 replaced the Mon/Wed/Fri windows, so the replay now only shows how many new articles a production window brings.

## Measured figures

Run 1 (`out/20261127T190256Z`): combined call, 7-day window, 18 candidates. Run 3 (`out/20261127T221301Z`): two calls with the edition slots, 37 candidates from the 30- and 90-day windows. Run 2 stopped on the search limit (see Checks run).

| Measure | Run 1, combined call | Run 3, two calls |
| --- | --- | --- |
| Input tokens | 98,132: 10 uncached, 24,871 cache write, 73,251 cache read | Search call 96,112: 14 uncached, 28,347 cache write, 67,751 cache read. Write call 37,206 uncached |
| Output tokens | 4,187 | 4,025 search, 7,520 write |
| Web searches | 0 (every search refused, see below) | 8 billed, 75 results |
| Effort | high | high |
| Wall-clock time | 45.5 s | 94.5 s |
| Items | 6 articles | 3 articles, 1 guideline, 2 news; no alert found |
| Run cost (computed) | US$0.111 | US$0.348 |
| Console billing (U8) | US$0.11, matching the computed cost | US$0.49 for the three runs, matching the computed US$0.494 |
| Monthly projection, run × 13 | US$1.45 | US$4.52 |
| G0 cost band | ≤ US$10: proceed | ≤ US$10: proceed |

- **Search was refused in runs 1 and 2.** The `pedsletter` workspace had its web search limit at 0 uses a second; every search came back `too_many_requests` and was not billed. In run 1 the model then wrote the edition from the journal articles alone; the 73,251 cache-read tokens fit the server-side loop re-reading the context after each refused search. Filipe set the limit to 2 a second before run 3.
- **Where run 3's money went.** The search call cost US$0.198: 8 searches at US$0.01, 4,025 output tokens, and the search loop re-read the context from the cache on each step, so most of its input was billed at the read rate. The write call cost US$0.150: 37,206 input tokens at the full rate (it carries no cache mark) and 7,520 output tokens for a ranked list of 10 items. Run 3 is the shape of a production run, so US$4.52 a month is the working figure. The earlier per-window projection from run 1 no longer applies: a run's candidates now come from 30- and 90-day windows, not from the days since the last edition.
- **Search worst case.** The script's bound for the search call was US$1.15, against US$0.198 spent; the bound assumes no cache, and run 3 shows the loop does read it.
- **Pre-check findings for F2-13.** Every link came from the run and was on the allow-list. All resolved except the AAP News page, which answered 403 to the script although its URL came from the search results, so F2-13 needs a rule for allow-listed sites that refuse scripts. The number check gave false positives in both runs. Run 1's abstracts wrote thousands with spaces (3 643 376) and run 3's decimals with a middle dot (1·4); the script splits both into separate numbers, so the edition's 3.643.376 and 1,4 were not found, and a stray single digit would pass. F2-13 must read spaces, middle dots, commas and dots as separators before comparing. The dose screen flagged the word "dose" with no number, and missed the attributions "segundo o relato" (run 1) and "segundo o documento" (run 3); neither mention carried a number. No tier 2 item carried a number other than a date.
- **Slot behaviour.** Ranked 10 items: 6 articles, 2 guidelines, 2 news. The third-ranked article, 5 days old, took the 90-day article slot, as the overlapping slots allow; the 51-day-old article ranked sixth did not get a place. The guideline was 60 days old, the edge of its window.

## Quality verdict (G0)

Filipe read the run 3 edition on 2026-11-27: "the articles are great, pediatric filter is spot on". After run 1 he noted the edition held only journal articles, which led to the two-call flow and the slots. Verdict: approved with Sonnet 5.5; gate G0 passes.

- Cost band: US$4.52 a month, under US$10: proceed.
- Tier 2 (D3): run 3 placed one guideline and two news items; Filipe approved the edition with them, so tier 2 stays in the MVP without numbers.
- Minimum items (D4): with 30- and 90-day windows a run had 37 candidates, so the minimum of 3 stands.
- Follow-up: Filipe wants to review later which items were placed and dropped, as in `selection.json` (F7-08).

## Limitations

- One run is one data point; F3-02 measures two weeks.
- The journal feeds are not exercised; F2-11 decides feeds versus PubMed.
- Numbers in tier 2 items cannot be checked against the page: the search results' text is not returned to the script, so the rule is "no numbers but dates".
- The monthly figure is one run × 13. Cost varies with the candidate count and the number of searches; F3-02 measures two weeks of runs. (`trial.py --project` still splits a run's cost per candidate for the old per-window design; it no longer applies.)
