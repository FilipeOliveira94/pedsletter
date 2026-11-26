# ADR-0001: Curation sources

| ADR-0001 | Detail |
| --- | --- |
| State | `proposed` |
| Opened | 2026-11-15 |
| Decided | — |
| Owner | Filipe (product owner) |
| Index ID | ADR-001 |
| Related issues | F0-03, F2-02, F2-11, F2-12 |
| Replaces | — |
| Replaced by | — |

## Context and problem

Generation by the Claude API (ADR-004) picks the items of each edition: articles, guidelines, alerts and news. Without a closed list of where to read, curation becomes unpredictable and the chance of a weak source or an invented article grows, on a site published without review (ADR-002). The list feeds the collector (F2-11), the domain-restricted search (F2-12) and the prompt (F2-02).

The list does not decide who writes the summary; it decides where the pipeline may read.

## Decision

Initial list proposed on 2026-11-25 and accepted by Filipe to start, with his review later. The state becomes `approved` once he reviews it.

**Tier 1 — journals (collected by feed and PubMed, no open search)**

| Source | Scope |
| --- | --- |
| Pediatrics | Pediatrics |
| JAMA Pediatrics | Pediatrics |
| The Lancet Child & Adolescent Health | Pediatrics |
| Archives of Disease in Childhood | Pediatrics |
| The Journal of Pediatrics | Pediatrics |
| Jornal de Pediatria | Pediatrics, Brazil |
| Revista Paulista de Pediatria | Pediatrics, Brazil |
| NEJM, JAMA, The Lancet, BMJ | General medicine; only items that affect pediatrics |
| Cochrane Database of Systematic Reviews | Systematic reviews; only pediatric items or items that affect pediatrics |

**Tier 2 — organizations and news (search restricted to the domains below)**

| Source | Domain | Scope |
| --- | --- | --- |
| Sociedade Brasileira de Pediatria | `sbp.com.br` | Scientific documents, notes and alerts |
| Ministério da Saúde | `gov.br/saude` | Vaccination schedule, technical notes, alerts |
| ANVISA | `gov.br/anvisa` | Drug and product safety alerts |
| American Academy of Pediatrics | `aap.org`, `publications.aap.org` | Guidelines and position statements |
| World Health Organization | `who.int` | Guidelines and alerts |
| PAHO | `paho.org` | Epidemiological alerts in the Americas |
| CDC | `cdc.gov` | Alerts, vaccine recommendations, MMWR |
| FDA | `fda.gov` | Safety alerts |

**Inclusion criteria**

- A peer-reviewed journal, or an official body or medical society.
- Publishes regularly and has a public page, with a stable link, for each item.
- A general-medicine item gets in only if it directly affects pediatrics, and the summary says how.
- News gets in only if published by a tier 2 source. General press and social media stay out.

**How the list changes:** only by a PR that edits this ADR and the sources configuration file (F2-11), with Filipe's decision.

## Alternatives considered

| Option | Pros | Cons | Why not (if rejected) |
| --- | --- | --- | --- |
| Closed two-tier list with inclusion criteria (chosen) | Predictable curation; validation checks the source; news only from official sources | The list needs upkeep | — |
| Journals only (final plan) | Simpler | Leaves out guidelines, alerts and news, which are in the MVP | Superseded by the 2026-11-25 decision |
| Open search | No upkeep | Weak sources and invented articles become more likely | Rejected in the final plan and in ADR-004 |

## Consequences

- Unblocks F2-02, F2-11 and F2-12.
- The collector and the search read the list from a configuration file, not from loose prompt text.
- A source outside the list makes validation fail (F2-13).

## Evidence

Initial list proposed in the F0-07 plan and accepted by Filipe on 2026-11-25 to start, with a later review. The domains and feed access have not been checked yet; F2-11 checks them.

## Review when

- Filipe reviews the list (the state becomes `approved`).
- A source stops publishing, changes domain or starts requiring access the pipeline does not have.
- F3-02 shows an empty tier or a source that only yields weak items.
