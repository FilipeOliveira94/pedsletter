# F3-08 — Free-tier model survey

| F3-08 | Detail |
| --- | --- |
| State | Delivered on 2026-11-28; the console figures are still to check (end of this file) |
| Rating | Risk Lo, Size Sm: a check of the docs, with no code and no API call |
| Waiver | W2 (`DECISIONS.md`): runs before phase 3, by Filipe's decision of 2026-11-28 |
| Sources | The providers' own pages, read on 2026-11-28. `ai.google.dev` redirects to the same paths on `aistudio.google.com`. Third-party tables were left out |
| Next | F3-09 (conditional), which waits for F2-13 and the eval set (F3-05) |

## Yardstick: one production run

A candidate is measured against run 3 of F0-08 ([`F0-08-api-trial.md`](F0-08-api-trial.md)), the shape of a production run:

| Call | Input tokens | Output tokens | Needs | Cost on Sonnet 5.5 |
| --- | --- | --- | --- | --- |
| Search (call A) | About 96,000, mostly cache reads | About 4,000 | Web search restricted to the ADR-001 tier 2 domains | US$0.198 |
| Write (call B) | About 37,000 | About 7,500 | Structured output by JSON schema, no tools | US$0.150 |

13 runs a month cost about US$4.52. ADR-001 requires the tier 2 search to stay inside the listed domains.

## Google AI Studio (Gemini API)

| Check | Finding |
| --- | --- |
| Free models (exact IDs) | `gemini-3.8-flash` and `gemini-3.5-flash-lite` are Stable and "Free of charge" for input and output in the pricing tables. `gemini-3.6-flash` is listed as free too, but its limits were not checked. `gemini-2.5-flash` is deprecated and routes to `gemini-3.5-flash-lite` from 2026-12-01. `gemini-2.0-flash`, `gemini-2.0-flash-lite` and `gemini-3.1-flash-lite-preview` are shut down |
| Card or billing | The Free tier offers "Free input & output tokens". A paid tier starts only when you "set up billing" on a Cloud project, so the Free tier implies no card. No page says so outright |
| Rate limits | Not published for Flash or Flash-Lite. The page says the limits "can be viewed in Google AI Studio". They apply "per project, not per API key", and the daily limits reset at midnight Pacific time |
| Context and output | Both models: input 1,048,576 tokens, output 65,536 |
| Structured output | Both models list structured outputs: `response_format` with `application/json` and a `schema` |
| Web search (grounding) | "Not available" on the Free tier for `gemini-3.8-flash`, `gemini-3.6-flash` and `gemini-3.5-flash-lite`. The pages read offer no domain allow list |
| Data use | On the Unpaid Services, Google uses content "to provide, improve, and develop Google products and services and machine learning technologies", and "human reviewers may read, annotate, and process your API input and output". The terms also say "do not submit sensitive, confidential, or personal information" |
| Use terms | For "professional or business purposes", not consumer use. You "may not use the Services in clinical practice, to provide medical advice". No ban on automated or scheduled use was found. Brazil is an available region. The EEA, Switzerland and the UK get Paid Services only (terms effective 2026-03-23) |

## Groq

| Check | Finding |
| --- | --- |
| Models (exact IDs) | Production: `openai/gpt-oss-120b`, `openai/gpt-oss-20b` (context 131,072, completion up to 65,536). Preview: `qwen/qwen3.8-27b` (131,072 and 16,384). Enterprise only: `meta-models/muse-spark-open`. Shut down: `meta-llama/llama-4-scout-17b-16e-instruct` and `qwen/qwen3-32b` (2026-07-17), `meta-llama/llama-4-maverick-17b-128e-instruct` (2026-03-09), `llama-3.3-70b-versatile` and `llama-3.1-8b-instant` (2026-08-16), `qwen/qwen3.6-27b` (2026-09-14), `groq/compound` and `groq/compound-mini` (2026-09-21). The models page still lists the two Llama 3 models, but the deprecations page shuts them down. No Llama 4 model is left |
| Card or billing | A payment method is needed only to move up to the Developer plan, so the Free plan implies no card |
| Rate limits | Requests per minute / requests per day / tokens per minute / tokens per day: `openai/gpt-oss-120b`, `openai/gpt-oss-20b` and `qwen/qwen3.8-27b` 30 / 1K / 8K / 200K. The page has Free and Developer tabs and the text read does not name its tab; these figures sit below the Developer figures on the models page (1K RPM, 250K TPM for gpt-oss-120b), so they read as Free. Limits apply "at the organization level" and per model; going over returns HTTP 429 with `retry-after`. Cached tokens do not count |
| Structured output | Strict JSON schema on `openai/gpt-oss-120b`, `openai/gpt-oss-20b` and `qwen/qwen3.8-27b`. "Streaming and tool use are not currently supported with Structured Outputs" |
| Web search | `browser_search` (powered by Exa) on the gpt-oss models only. Domain restriction is not documented, "Browser search is not compatible with structured outputs", and the pages do not say whether it is on the Free plan |
| Data use | "By default, Groq does not retain customer data for inference requests"; abuse logs are kept up to 30 days, and Zero Data Retention is open to every customer. The Services Agreement (2026-06-22) bars Groq from using Inputs or Outputs for training unless told to |
| Use terms | The services "should not be used for medical, legal, financial, or other professional advice". The usage policy bars automated decisions in healthcare "without human supervision". Section 6.3 bars use "in a manner intended to avoid incurring Fees". No ban on automated or production use on the Free plan was found |
| API shape | OpenAI-compatible at `https://api.groq.com/openai/v1`, "mostly compatible" (`n` must be 1; `logprobs` and `logit_bias` return 400) |

## Verdict per call

| Call | Gemini (free) | Groq (free) |
| --- | --- | --- |
| Search (call A) | Out. Free grounding is not available on the current Flash models, and no domain allow list was found (ADR-001) | Out. No domain restriction, no structured output alongside it, and 8K tokens a minute is far below about 96,000 input tokens |
| Write (call B) | **Candidate:** `gemini-3.8-flash`, with `gemini-3.5-flash-lite` as the next one down. The context, output and schema fit. The rate limits are still to check in the console | Out as shaped. 8K tokens a minute is below the 37,000-token call, so it cannot go in one request. Only a different shape fits: one small call per candidate (37 candidates at under 8K tokens each stays under 30 a minute and 200K a day). At about 1,000 tokens each, 37 calls fit 30 a minute, 8K tokens a minute and 200K a day, in about five minutes. That is a design change for F3-09 to weigh, not a drop-in swap |
| Fallback for call B | Candidate, on the same conditions | Only with the per-candidate shape |

## What this means for cost

- **A free write call saves at most US$0.150 a run,** about US$1.95 a month at 13 runs. The search call stays on Claude and costs US$0.198 a run (about US$2.57 a month).
- **Reaching zero means replacing the search call,** not only the model. A deterministic tier 2 collection (feeds or pages fetched from the ADR-001 hosts, which F3-07 already weighs) would leave only the write call, which Gemini could then take.
- **Google's free tier trains on the prompt and output, and humans may read them.** The inputs are public abstracts and the outputs are published anyway, so nothing sensitive is in them. The system prompt and the schema would be seen too.
- **Both providers' terms bar medical advice.** The site publishes literature summaries for professionals, with the AI notice and no dose recommendation (§4), not advice to patients. Whether that is enough under Google's "clinical practice, to provide medical advice" clause is Filipe's call before F3-09 (open question in `PROJECT_STATUS.md`).

## Still to check in the consoles

These need a signed-in account, so they wait for Filipe and are checked at the start of F3-09:

- **AI Studio rate-limit view:** the requests a minute, tokens a minute and requests a day for `gemini-3.8-flash` and `gemini-3.5-flash-lite` on a Free project. A tokens-a-minute figure below 37,000 rules the model out for call B as shaped.
- **Groq limits page:** confirm that the 30 / 1K / 8K / 200K figures are the Free plan, and whether `browser_search` is on it.

## Pages read

- Google: `/gemini-api/docs/rate-limits`, `/pricing`, `/models`, `/models/gemini-3.8-flash`, `/models/gemini-3.5-flash-lite`, `/structured-output`, `/google-search`, `/available-regions`, and the Gemini API Additional Terms.
- Groq: `console.groq.com/docs/rate-limits`, `/models`, `/deprecations`, `/structured-outputs`, `/tool-use/built-in-tools`, `/tool-use/built-in-tools/browser-search`, `/billing-faqs`, `/your-data`, `/openai`, `/legal/ai-policy`, `/legal/services-agreement`, and `groq.com/terms-of-use`.
