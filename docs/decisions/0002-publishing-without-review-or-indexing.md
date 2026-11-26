# ADR-0002: Publishing without review or indexing

| ADR-0002 | Detail |
| --- | --- |
| State | `approved` |
| Opened | 2026-11-15 |
| Decided | 2026-11-15 (final plan) |
| Owner | Filipe (product owner) |
| Index ID | ADR-002 |
| Related issues | F0-04, F1-03, F1-05, F1-06, F2-07, F2-13, F9-01 to F9-04 |
| Replaces | — |
| Replaced by | — |

## Context and problem

The site publishes AI-generated summaries of pediatric literature three times a week, for personal use. This version has no clinical review step and the site names no professional. Wrong medical information can go live, so the reach has to be limited and it must be clear what the content is.

## Decision

What passes automatic validation is published, with no human review. The site is not indexable: `noindex` on every page, in the meta tag and in the `X-Robots-Tag` header, no sitemap and no Search Console registration. `noindex` is enough; there is no access control or login. The site has no byline, authorship or professional identification, and the text uses only the generic "médico".

## Mitigations

- **AI notice** on every edition, on the home page and in the README: "Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original."
- **Audience notice** on every page: "Conteúdo destinado a médicos e demais profissionais de saúde."
- **Link to the source** on every article; validation checks that the URL responds and the DOI resolves.
- **Grounding check** (F2-13, [ADR-0004](0004-generation-by-claude-api.md)): every number in a summary must appear in the fetched source text, and every link must come from the run's collection or search results.
- **No dose recommendation.** A dose only appears attributed to the article.
- **Simple withdrawal** by `status: retirado`, by deleting the file or by reverting the deploy ([ADR-0003](0003-publishing-format-and-path.md)).
- **Limited reach:** the site is neither indexed nor promoted.
- **Check for absence of authorship** in CI (F1-06).
- **No `Disallow` in `robots.txt`:** a crawler blocked by `robots.txt` never gets to read the `noindex`.

## Alternatives considered

| Option | Pros | Cons | Why not (if rejected) |
| --- | --- | --- | --- |
| Publish without review, without indexing (chosen) | No recurring manual work; zero cost | An error can go live | — |
| Clinical review before publishing | Fewer published errors | Needs an associated physician and recurring work | Deferred to phase 9 |
| Access control or login | Even smaller reach | A function, authentication and a secret to maintain | `noindex` is enough |
| Index with a notice | Visibility | Widens the reach of unreviewed content | Deferred to phase 9 |

## Consequences

- Wrong medical information going live is the accepted risk of this version. The grounding check (F2-13) only proves that a number appears in the source; a number taken from the wrong place or attached to the wrong claim still goes live.
- The repository is public: the summary files can be found through GitHub and search engines, even with the site on `noindex`. The README carries the same notice.
- Withdrawn or deleted text stays in the Git history.
- SEO is not a metric until phase 9. Lighthouse CI ignores the SEO category (F3-04).

## Evidence

Decision recorded in the final plan approved on 2026-11-15 (summary in [`docs/project-genesis.md`](../project-genesis.md)). No implementation yet; F1-03, F1-05, F1-06, F2-07 and F2-13 implement the mitigations.

F0-04 checked this ADR on 2026-11-26: it records the decision, the rationale (context and alternatives), the mitigations and the phase 9 review conditions, and it names no professional (a search for names, "CRM", "Dr." and "Dra." finds nothing). Both notices match the `AGENTS.md` §4 wording byte for byte. The same check added the F2-13 grounding mitigation from ADR-004, which postdates this ADR; the decision did not change.

## Review when

- Filipe decides to start phase 9. The order is: clinical review (F9-01), association with a physician (F9-02), retroactive review or archive (F9-03), and only then indexing (F9-04).
- The number of editions withdrawn per month shows that automatic validation does not hold quality.
- Usage validation (F3-03) ends in "stop".
