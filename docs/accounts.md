# Accounts, repository settings and free-plan limits

What F0-01 checked on 2026-11-28: the accounts the project runs on, the repository settings, and the free-plan limits from the providers' current pages. No paid plan was bought. The Claude API account and its spend limit are in [`docs/spikes/F0-08-api-trial.md`](spikes/F0-08-api-trial.md) and ADR-004.

## Accounts

| Account | State on 2026-11-28 | How it was checked |
| --- | --- | --- |
| GitHub repository [FilipeOliveira94/pedsletter](https://github.com/FilipeOliveira94/pedsletter) | Public, GitHub Free | `gh api repos/FilipeOliveira94/pedsletter` → `visibility: public` |
| Cloudflare Pages project `pedsletter` (`pedsletter.pages.dev`) | Free plan, linked to this repository by the Cloudflare Git integration; automatic production and preview deployments paused until F1-01, as Filipe confirmed (the agent cannot read that dashboard setting) | The `Cloudflare Pages` check run (app `cloudflare-workers-and-pages`) on `main` at `09061f2`, conclusion `failure` ("Build failed"); `https://pedsletter.pages.dev/` answers 522, so nothing is served |

The project was created with no build command and the output directory `dist`, which does not exist yet. The build Cloudflare runs when a project is created, on `09061f2`, failed, and as of 2026-11-28 nothing is served. F1-01 sets the build and turns deployments back on, with previews per branch, none for forks, and `noindex` (F1-03).

## Repository settings

Read with `gh api` on 2026-11-28. None was changed by F0-01.

| Setting | Value | Acceptance |
| --- | --- | --- |
| Ruleset `protect-main` (id 27377947) | `active`, target `~DEFAULT_BRANCH`, no bypass actors | Ruleset on `main`, nothing needs a bypass |
| Rule `pull_request` | `required_approving_review_count: 0`; merge, squash and rebase allowed | PR required with no required approval |
| Rule `non_fast_forward` | Present | No force push |
| Rule `deletion` | Present | No deletion |
| Required checks | `build` and `docs-lint`, source GitHub Actions (integration 15368), added by F1-01 on 2026-11-28 | F2-05 adds the content checks |
| Actions `default_workflow_permissions` | `read`; `can_approve_pull_request_reviews: false` | Default `GITHUB_TOKEN` is read-only |
| `secret_scanning`, `secret_scanning_push_protection` | `enabled` | Push protection on |
| `delete_branch_on_merge` | `true` | Workflow rule (merged branches deleted by GitHub) |
| `allow_auto_merge` | `false` | F2-05 turns it on |

Open item for F2-05: the `pull_request` rule also reports `require_extra_approval_for_unattributed_changes: true`. F2-05 checks that a PR opened by the GitHub App still merges with no approval and no bypass.

Commands:

```sh
gh api repos/FilipeOliveira94/pedsletter -q '{visibility, delete_branch_on_merge, allow_auto_merge, security_and_analysis}'
gh api repos/FilipeOliveira94/pedsletter/rulesets/27377947 -q '{conditions, rules, bypass_actors}'
gh api repos/FilipeOliveira94/pedsletter/actions/permissions/workflow
gh api repos/FilipeOliveira94/pedsletter/commits/main/check-runs -q '.check_runs[] | [.name, .app.slug, .conclusion]'
```

## Free-plan limits

From the providers' pages, read on 2026-11-28. Expected use: 13 generation runs a month (ADR-004), one production build per merge and one preview build per branch push once F1-01 turns them on.

| Provider and limit | Free plan | Expected use | Source |
| --- | --- | --- | --- |
| Cloudflare Pages builds | 500 a month, 1 at a time per account, 20-minute timeout | Tens a month (edition PRs and code PRs, with previews) | [Pages limits](https://developers.cloudflare.com/pages/platform/limits/) |
| Cloudflare Pages files | 20,000 per site, 25 MiB per file | About 160 editions a year, a few pages each | Same |
| Cloudflare Pages `_headers` | 100 rules, 2,000 characters per line | A few rules (F1-03 CSP and `X-Robots-Tag`) | Same |
| Cloudflare Pages `_redirects` | 2,000 static and 100 dynamic | None planned | Same |
| Cloudflare Pages deployments | Kept 30 days; the 100 most recent and the current production one always kept | Rollback (F2-07) uses recent deployments | Same |
| Cloudflare Pages custom domains | 100 per project | One, in phase 9 | Same |
| Cloudflare Pages bandwidth | Not stated on the limits page | Personal use | Same |
| GitHub Actions | Standard GitHub-hosted runners free in public repositories, no minute limit stated; larger runners are billed | CI per PR and 13 generation runs a month on standard runners | [About billing for GitHub Actions](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions) |
| GitHub rulesets | Up to 75 per repository | One | [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets); the active ruleset above shows it works on this free public repository |
| GitHub push protection | Push protection for users is on by default for public repositories; repository push protection needs Secret Protection | On for this repository | [About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection); the repository setting above |

Fork PRs get no Cloudflare preview, and no setting turns one on (read 2026-11-28 for F1-01). The [GitHub integration page](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/): "Note that preview URLs will not be created for pull requests created from forks of your repository." The [known issues page](https://developers.cloudflare.com/pages/platform/known-issues/): "Commits/PRs from forked repositories will not create a preview." Not exercised: there is no second GitHub account to open a fork PR, and Filipe accepted the docs as evidence. The [preview deployments page](https://developers.cloudflare.com/pages/configuration/preview-deployments/) adds that "every preview deployment generated by Cloudflare Pages includes the X-Robots-Tag: noindex HTTP response header"; `public/_headers` also sends it on production.

Branch build controls (Settings > Build > Branch control): "Enable automatic production branch deployments" off pauses production; preview branches set to "None" pause previews ([Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/), [branch build controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)).

## Cloudflare Pages build (F1-01)

Set by Filipe in the dashboard (Settings > Build); the agent has no access to it.

| Setting | Value |
| --- | --- |
| Framework preset | None (Astro also works) |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Environment variable | `NODE_VERSION` = `22.23.4` (same as `.nvmrc`), production and preview |
| Production branch | `main`, automatic deployments on |
| Preview branches | All non-production branches |

Each branch push builds a preview at `<branch>.pedsletter.pages.dev`, with `/` turned into `-`. The Cloudflare preview is not a GitHub required check: it builds outside GitHub Actions.
