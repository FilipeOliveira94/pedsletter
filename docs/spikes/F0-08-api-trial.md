# F0-08 — Cost and quality trial of the Claude API

| F0-08 | Detail |
| --- | --- |
| State | In progress: script ready, paid run pending API credits |
| Rating | Risk Hi (raised from Med: the API key and the spend cap), Size Sm |
| Script | [`spikes/F0-08/trial.py`](../../spikes/F0-08/trial.py) (throwaway; does not become F2-12) |
| Model | `claude-sonnet-5-5`, default effort, `max_tokens` 32000 |
| Trial cap | US$3 in total, one paid run, at most 2 reruns after a technical failure (Filipe, 2026-11-26) |

## Setup

- **Tier 1 candidates:** PubMed E-utilities over the ADR-001 journals, entries from the last 7 days with an abstract; letters, comments, editorials, news and errata excluded; general journals (NEJM, JAMA, The Lancet, BMJ, Cochrane) filtered to pediatric terms. At most 8 items per pediatric journal, 5 per general journal, 40 in total. Authors are not read.
- **Why PubMed and not feeds:** on 2026-11-26 the journal feeds that answered (JAMA Pediatrics, JAMA, Archives of Disease in Childhood, The Journal of Pediatrics, Jornal de Pediatria, Pediatrics) carried titles but no abstracts, and the feeds of The Lancet, NEJM, Cochrane and BMJ answered 403 or 404 to a script. The model needs the abstract to summarize and the number check needs it too. ADR-001 already names PubMed for tier 1.
- **Tier 2:** server-side web search (`web_search_20260209`), restricted to the ADR-001 tier 2 domains, at most 8 searches.
- **Output:** structured JSON (`output_config.format`) with the edition fields; the script validates it, renders Markdown with both §4 notices and writes it to the git-ignored `spikes/F0-08/out/`. The edition is never committed.
- **Prices** (pricing page checked on 2026-11-26): Sonnet 5.5 input US$2/MTok, output US$10/MTok, cache write US$2.50/MTok, cache read US$0.10/MTok; web search US$10 per 1,000 searches, with search results billed as input tokens. Projection: run cost × 13 runs a month.
- **Pre-checks the script runs on the edition:** each link is a collected candidate or on a tier 2 domain, appeared in the run, and its HTTP status; each number in a tier 1 summary appears in the abstract.

## Checks run

- `spikes/F0-08/.venv/bin/python -m unittest discover -s spikes/F0-08`: 15 tests pass (cost, cap, PubMed parsing, schema rejection with no file written, both notices verbatim, number and link pre-checks).
- `trial.py --dry-run`: renders the synthetic fixture with both notices.
- Real PubMed collection on 2026-11-26 (no API call): 24 candidates from 9 of the 12 journals (none from The Lancet Child & Adolescent Health, Archives of Disease in Childhood, Revista Paulista de Pediatria or NEJM in the window); the request is about 67,600 characters.
- First paid attempt on 2026-11-26: refused by the API before any processing, "credit balance is too low". Nothing billed; trial spend US$0.00.

## Measured figures

Pending the paid run.

| Measure | Value |
| --- | --- |
| Input tokens | — |
| Output tokens | — |
| Web searches | — |
| Run cost | — |
| Monthly projection (13 runs) | — |

## Quality verdict

Pending. Filipe reads the edition against this checklist:

- Every link resolves and is from an ADR-001 source.
- Every number in a summary appears in the source.
- Any dose in a summary is stated in the article and attributed to it; no dose of our own.
- Summaries are in the model's own words, in pt-BR, and say why each item matters to pediatrics.
- General-medicine items say how they affect pediatrics.
- Triage: would he have picked these items?
- Verdict: continue with Sonnet, adjust the prompt, or try Opus.

## Limitations

- One run is one data point; F3-02 measures two weeks.
- The 7-day window is wider than a production run (2 or 3 days between editions), so the candidate count and the input tokens overstate a production run.
- The journal feeds are not exercised; F2-11 decides feeds versus PubMed.
- Numbers in tier 2 items cannot be checked locally: the search results' page text is not returned to the script.
- The API account's US$30 monthly limit is not set yet; the Console does not allow it before credits are added.
