# Project genesis

Summary of PedsLetter's final plan, approved by Filipe on 2026-11-15. The full plan lives outside the repository. This document is history, not a source of rules: the rules are in [`AGENTS.md`](../AGENTS.md), the scope in [`ROADMAP.md`](../ROADMAP.md) and the current work in [`PROJECT_STATUS.md`](../PROJECT_STATUS.md).

The plan's appendix, with the rules for associating a physician with the site, was not brought over. It is context for F9-02 and enters the repository in that issue.

## 1. Goal

A site of AI-generated summaries of pediatric literature, published three times a week, for personal use, with clinical calculators afterwards.

| User | Need | Implication |
| --- | --- | --- |
| Main user (physician) | See what relevant came out without digging; calculate fast | Short summary with a link to the source; calculators on the phone |
| Filipe | Run it with no recurring manual work; show the work | Automatic publishing, simple withdrawal and a public repository |

## 2. Decisions built in

| Decision | Effect |
| --- | --- |
| The site names no professional | No byline, no authorship, no professional identification |
| Text uses the generic "médico" | Applies to the site, repository, issues, ADRs and commits |
| Public repository | Free CI; nothing that identifies anyone enters a file, issue, PR or commit |
| No review step | What passes automatic validation is published |
| What is published can be withdrawn later | Withdrawal mechanism in ADR-003 |
| No indexing, and `noindex` is enough | `noindex` everywhere, no sitemap, no Search Console, no login |
| Who uploads the file: Filipe or the Grok Bot | The same path for both: PR with automatic merge |
| Curation sources provided later | Their own ADR (F0-03) |
| Routine runs on the day itself | Monday, Wednesday and Friday mornings, with direct publishing |
| AI curation notice | On every edition, on the home page and in the README |
| Domain after phase 3 | Phase 4, after validating MVP use |
| Preterm charts validated at the start of the issue | F8-03 starts with that validation |
| Associate a physician, review and index | Phase 9 |
| Kept | Zero cost, no e-mail, no sign-up, no ads, no PALS, physician audience |

The public repository changes two things besides cost:

- **Automatic merge needs an author list.** Anyone can open a PR, so the workflow only publishes PRs from Filipe or the bot.
- **The content can be found through GitHub.** `noindex` covers the site, not the repository. The README carries the same AI-generated content notice.

## 3. Scope

**MVP: phases 0 to 3, zero cost**

- Static site on `*.pages.dev`, not indexable.
- Home page with recent editions, edition page, tags and RSS.
- File format for Grok, validated automatically.
- Automatic publishing by PR and withdrawal by a status change.
- Notice that the content is AI-generated and unvalidated.

**After the MVP**

- `pedsletter.com.br` domain (phase 4), still without indexing.
- Drug-free calculators (phases 5 to 8).
- Clinical review, association with a physician, indexing and drug calculators (phase 9).

## 4. Metrics

- **Cadence:** an edition published on at least 10 of the 12 scheduled dates a month.
- **Automation:** at least 80% of editions published without Filipe stepping in.
- **Quality:** zero broken links published; number of editions withdrawn per month.
- **Use:** the main user reads the summaries at least 3 times a week and says whether they help.
- **Cost:** zero until the domain is bought.
- **Technical:** Lighthouse 95 or higher.

SEO becomes a metric only in phase 9.

## 5. Stack and cost

Astro + Markdown on Cloudflare Pages, with public GitHub and CI, cookieless Cloudflare Web Analytics and the scheduled routine on Grok. All free; the `pedsletter.com.br` domain, in phase 4, is the only cost. Alternatives and the full design are in [`architecture/overview.md`](architecture/overview.md).

## 6. How a summary becomes a post

One Markdown file with YAML frontmatter per edition arrives by PR, passes CI validation, reaches `main` by automatic merge and is published by Cloudflare Pages. An edition comes down by `status: retirado`, by deleting the file or by reverting the deploy. Details in [`architecture/overview.md`](architecture/overview.md) and in [ADR-0003](decisions/0003-publishing-format-and-path.md). The Grok routine rules are in `ROADMAP.md`, phase 2.

## 7. Calculator catalog

Effort: S small, M medium, L large.

| # | Calculator | Value | Effort | Reference source | Phase |
| --- | --- | --- | --- | --- | --- |
| 1 | Maintenance fluids | High | S | Holliday and Segar, Pediatrics 1957; note on isotonic fluid, AAP, Feld et al., Pediatrics 2018 | 5 |
| 2 | Body surface area and BMI | Medium | S | Mosteller, NEJM 1987 | 6 |
| 3 | Generic weight-based dose | High | S | Arithmetic; parameters entered by the user | 6 |
| 4 | WHO chart 0–5 years | High | L | WHO Child Growth Standards 2006, official LMS tables | 6 |
| 5 | WHO chart 5–19 years | High | M | WHO Reference 2007 (de Onis et al., Bull WHO 2007) | 7 |
| 6 | Preterm corrected age | Medium | S | SBP, Seguimento ambulatorial do prematuro de risco | 7 |
| 7 | Newborn weight loss (%) | Medium | S | Arithmetic; SBP and AAP thresholds | 7 |
| 8 | Mid-parental target height | Medium | S | Tanner et al., Arch Dis Child 1970 | 7 |
| 9 | Estimated GFR (Schwartz) | Medium | S | Schwartz et al., JASN 2009 | 7 |
| 10 | Oral rehydration, plans A, B and C | Medium | M | Ministério da Saúde, Manejo do paciente com diarreia | 8 |
| 11 | Preterm growth charts | Medium | L | Intergrowth-21st (Villar et al., Lancet 2014), to be validated | 8 |
| 12 | Blood pressure percentile | Medium | L | AAP 2017 (Flynn et al., Pediatrics) | 8 |
| 13 | Bilirubin and phototherapy | Medium | L | AAP 2022 (Kemper et al., Pediatrics) | 8 |
| 14 | CDC 2000 chart | Low in Brazil | M | CDC Growth Charts 2000, LMS files | 8 |
| 15 | Antipyretics | High | M | SBP as the default; ANVISA package insert, Harriet Lane and BNFc for comparison | 9 |
| 16 | Common antibiotics by weight | High | M | SBP as the default; ANVISA package insert and Harriet Lane for comparison | 9 |

The references above are article authors and organizations cited as the source of the formulas; they are not people connected to the site.

**Source rule for doses** (from phase 9): SBP is the default; a conflict between sources stays visible, in a block that shows each source and what differs; if SBP takes no position, the ANVISA package insert applies, and the page says so.

## 8. Content safety

- **Notice on every edition, on the home page and in the README:** "Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. Confira sempre a fonte original."
- **Audience notice:** "Conteúdo destinado a médicos e demais profissionais de saúde."
- **Invented article or wrong link:** validation checks that each URL responds and each DOI resolves.
- **Wrong number in a summary:** nothing automatic catches it. The notice, the link to the source and withdrawal are the mitigation.
- **Limited reach:** the site is neither indexed nor promoted.
- **Copyright:** summary in our own words and a link to the source.

The rules for calculators, privacy, accessibility and performance are in [`architecture/overview.md`](architecture/overview.md).

## 9. Risks

- **Wrong medical information goes live.** It is the accepted risk of this version. Mitigation: AI notice, link to the source, non-indexed site and simple withdrawal.
- **The public repository can be found.** The summaries show up on GitHub and in search engines, even with the site on `noindex`. Mitigation: AI notice in the README; the risk is accepted in exchange for visibility.
- **Third-party PRs.** Mitigation: author list and fork block in F2-05.
- **Git history does not forget.** A withdrawn edition or a name written by mistake stays in the history. Mitigation: F1-06 blocks it before merge; rewriting history is the last resort.
- **A professional's name slips in.** Mitigation: F1-06 and the generic "médico" rule.
- **The bot publishes something off-format.** Mitigation: format and link validation, and merge restricted to the posts folder.
- **Leaked bot token.** Mitigation: access to this repository only, with an expiry; revocation described in the operations guide.
- **The Grok routine does not deliver what the plan assumes.** Mitigation: F0-02 tests it first; manual upload covers it.
- **Calculator without clinical validation.** Mitigation: cases from a published source, a visible badge and no drug tables before phase 9.
- **Copyright.** Mitigation: summary in our own words and a link to the source.
- **ANVISA regulation.** Before F9-05, check RDC 657/2022 and RDC 96/2008.

## 10. Plan caveats

- Three points are recommendations by the plan's author, accepted on approval: drug calculators only in phase 9, summaries without dose recommendations, and publishing by PR with automatic merge.
- What the Grok scheduled routine can do was not verified. F0-02 tests it.
- The free-plan limits were cited from memory. F0-01 checks them.

## 11. Open questions

1. **Curation sources:** the list enters ADR-001 when Filipe provides it; it blocks F2-02.
2. **Doses in the summaries:** the routine writes no dose recommendation until there is review. The rule holds until Filipe says otherwise.
