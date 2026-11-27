"""Unit tests for the F0-08 trial script. No network, no API call.

Run: spikes/F0-08/.venv/bin/python -m unittest discover -s spikes/F0-08
"""

import json
import tempfile
import unittest
from pathlib import Path

import trial

HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"

AI_NOTICE = (
    "Curadoria e resumos gerados por IA, sem revisão por profissional de saúde. "
    "Confira sempre a fonte original."
)
AUDIENCE_NOTICE = "Conteúdo destinado a médicos e demais profissionais de saúde."


def usage(inp=0, out=0, cw=0, cr=0, searches=0):
    return {
        "input_tokens": inp,
        "output_tokens": out,
        "cache_creation_input_tokens": cw,
        "cache_read_input_tokens": cr,
        "web_search_requests": searches,
    }


class CostTest(unittest.TestCase):
    def test_tokens_and_searches(self):
        # 100k input x $2/MTok + 10k output x $10/MTok + 8 searches x $10/1000
        self.assertAlmostEqual(trial.cost_usd(usage(100_000, 10_000, searches=8)), 0.38)

    def test_cache_tokens(self):
        # 1M cache writes x $2.50 + 1M cache reads x $0.10
        self.assertAlmostEqual(trial.cost_usd(usage(cw=1_000_000, cr=1_000_000)), 2.60)

    def test_projection_13_runs(self):
        self.assertAlmostEqual(trial.monthly_projection(0.38), 4.94)

    def test_add_usage_sums_continuations(self):
        total = trial.add_usage(usage(10, 20, 1, 2, 3), usage(1, 2, 3, 4, 5))
        self.assertEqual(total, usage(11, 22, 4, 6, 8))


class CapTest(unittest.TestCase):
    def test_cap_blocks_when_spent(self):
        with tempfile.TemporaryDirectory() as d:
            spend = Path(d) / "spend.json"
            spend.write_text(json.dumps({"total_usd": 3.0}))
            with self.assertRaises(trial.BudgetExceeded):
                trial.check_budget(spend, extra=0.0)

    def test_cap_allows_below(self):
        with tempfile.TemporaryDirectory() as d:
            spend = Path(d) / "spend.json"
            spend.write_text(json.dumps({"total_usd": 1.0}))
            trial.check_budget(spend, extra=0.5)

    def test_cap_counts_current_run(self):
        with tempfile.TemporaryDirectory() as d:
            spend = Path(d) / "spend.json"
            spend.write_text(json.dumps({"total_usd": 2.5}))
            with self.assertRaises(trial.BudgetExceeded):
                trial.check_budget(spend, extra=0.6)


class PubMedTest(unittest.TestCase):
    def test_general_journal_gets_pediatric_filter(self):
        q = trial.pubmed_query({"ta": "JAMA", "general": True})
        self.assertIn('"JAMA"[ta]', q)
        self.assertIn("child", q.lower())
        q2 = trial.pubmed_query({"ta": "J Pediatr", "general": False})
        self.assertNotIn("child[", q2.lower())

    def test_parse_keeps_items_with_abstract(self):
        items = trial.parse_pubmed((FIXTURES / "pubmed_sample.xml").read_text())
        self.assertEqual([i["pmid"] for i in items], ["90000001", "90000002"])
        first = items[0]
        self.assertEqual(first["url"], "https://doi.org/10.0000/synthetic.0001")
        self.assertIn("12.5%", first["abstract"])
        self.assertEqual(first["journal"], "J Pediatr")
        self.assertEqual(items[1]["url"], "https://pubmed.ncbi.nlm.nih.gov/90000002/")
        self.assertEqual(first["date"], "2026-11-20")


class ValidateTest(unittest.TestCase):
    def response(self):
        return json.loads((FIXTURES / "response.json").read_text())

    def test_fixture_is_valid(self):
        trial.validate_edition(self.response())

    def test_missing_url_rejected_and_no_file(self):
        resp = self.response()
        resp["artigos"][0]["url"] = ""
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(trial.InvalidEdition):
                trial.write_edition(resp, Path(d), "2026-11-26")
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_non_https_url_rejected(self):
        resp = self.response()
        resp["artigos"][0]["url"] = "javascript:alert(1)"
        with self.assertRaises(trial.InvalidEdition):
            trial.validate_edition(resp)

    def test_unknown_categoria_rejected(self):
        resp = self.response()
        resp["artigos"][0]["categoria"] = "opiniao"
        with self.assertRaises(trial.InvalidEdition):
            trial.validate_edition(resp)


class RenderTest(unittest.TestCase):
    def setUp(self):
        self.resp = json.loads((FIXTURES / "response.json").read_text())
        self.resp.pop("_comment")
        self.md = trial.render_markdown(self.resp, "2026-11-26")

    def test_notices_verbatim_before_items(self):
        self.assertIn(AI_NOTICE, self.md)
        self.assertIn(AUDIENCE_NOTICE, self.md)
        self.assertLess(self.md.index(AI_NOTICE), self.md.index("## " + self.resp["artigos"][0]["titulo"]))

    def test_frontmatter_fields(self):
        self.assertTrue(self.md.startswith("---\n"))
        front = self.md.split("---\n")[1]
        for key in ("titulo:", "data: 2026-11-26", "resumo:", "tags:", "status: publicado", "artigos:"):
            self.assertIn(key, front)
        for key in ("titulo:", "fonte:", "url:", "publicadoEm: 2026-11-20", "tipo:", "categoria: artigo", "acesso:"):
            self.assertIn(key, front)
        # string values are JSON-quoted, which is valid YAML
        line = next(l for l in front.splitlines() if l.startswith("titulo:"))
        self.assertEqual(json.loads(line.split(":", 1)[1]), self.resp["titulo"])

    def test_four_sections_per_item(self):
        for heading in ("**Por que importa:**", "**O que foi feito:**", "**Resultado:**", "**Limitações:**"):
            self.assertEqual(self.md.count(heading), len(self.resp["artigos"]))

    def test_item_count_note(self):
        self.assertEqual(trial.item_count_note(self.resp), "2 items: below the 3-item minimum")
        self.resp["artigos"] *= 2
        self.assertEqual(trial.item_count_note(self.resp), "4 items")


class PreCheckTest(unittest.TestCase):
    def test_numbers_found_and_missing(self):
        source = "Mortality fell from 12.5% to 8% in 1,204 infants."
        self.assertEqual(trial.missing_numbers("Caiu de 12,5% para 8%.", source), [])
        self.assertEqual(trial.missing_numbers("Caiu para 7%.", source), ["7"])
        self.assertEqual(trial.missing_numbers("Em 1.204 lactentes.", source), [])

    def test_link_allowed(self):
        domains = ["gov.br/saude", "cdc.gov"]
        known = {"https://doi.org/10.1/x"}
        self.assertTrue(trial.link_allowed("https://doi.org/10.1/x", known, domains))
        self.assertTrue(trial.link_allowed("https://www.cdc.gov/a", set(), domains))
        self.assertTrue(trial.link_allowed("https://www.gov.br/saude/pt-br/x", set(), domains))
        self.assertFalse(trial.link_allowed("https://www.gov.br/fazenda/x", set(), domains))
        self.assertFalse(trial.link_allowed("https://evilcdc.gov.example.com/", set(), domains))
        self.assertFalse(trial.link_allowed("https://doi.org/10.1/other", known, domains))


class DoseScreenTest(unittest.TestCase):
    def test_flags_doses(self):
        self.assertTrue(trial.dose_hits("Usou 5 mg/kg/dia por 7 dias."))
        self.assertTrue(trial.dose_hits("Uma dose de 10 mL."))
        self.assertTrue(trial.dose_hits("Recebeu 250 mcg."))

    def test_ignores_non_doses(self):
        self.assertEqual(trial.dose_hits("Caiu de 12,5% para 8% em 2026-11-20."), [])

    def test_attribution(self):
        self.assertTrue(trial.dose_attributed("Segundo o artigo, 5 mg/kg/dia."))
        self.assertFalse(trial.dose_attributed("Use 5 mg/kg/dia."))


class Tier2NumbersTest(unittest.TestCase):
    def test_number_flagged(self):
        self.assertEqual(trial.tier2_numbers("A incidência caiu 30% no período."), ["30"])

    def test_dates_allowed(self):
        self.assertEqual(trial.tier2_numbers("Publicado em 2026-11-24, válido desde 24/11/2026."), [])
        self.assertEqual(trial.tier2_numbers("Emitido em 24 de novembro de 2026."), [])


class FetchTest(unittest.TestCase):
    def setUp(self):
        self.calls = []

        def fake(url):
            self.calls.append(url)
            return "200"

        self.fake = fake
        self.domains = ["cdc.gov", "gov.br/saude"]
        self.cands = {"https://doi.org/10.1/abc", "https://pubmed.ncbi.nlm.nih.gov/123/"}

    def test_off_list_never_fetched(self):
        status = trial.check_link("https://example.com/x", self.cands, self.domains, self.fake)
        self.assertEqual(status, "off-list, not fetched")
        self.assertEqual(self.calls, [])

    def test_doi_checked_at_handle_api(self):
        trial.check_link("https://doi.org/10.1/abc", self.cands, self.domains, self.fake)
        self.assertEqual(self.calls, ["https://doi.org/api/handles/10.1/abc"])

    def test_pubmed_fetched_directly(self):
        trial.check_link("https://pubmed.ncbi.nlm.nih.gov/123/", self.cands, self.domains, self.fake)
        self.assertEqual(self.calls, ["https://pubmed.ncbi.nlm.nih.gov/123/"])

    def test_tier2_one_retry(self):
        def failing(url):
            self.calls.append(url)
            return "503"

        status = trial.check_link("https://www.cdc.gov/a", self.cands, self.domains, failing)
        self.assertEqual(status, "503")
        self.assertEqual(len(self.calls), 2)


class WorstCaseTest(unittest.TestCase):
    def test_bound_counts_search_iterations(self):
        # 8 searches: input read 9 times (270k) + results 10k x (1+...+8) = 360k, at the $2.50 cache-write rate;
        # 32k output x $10/MTok; 8 searches x $0.01
        self.assertAlmostEqual(trial.worst_case_usd(30_000, 32_000, 8), 630_000 * 2.5e-6 + 0.32 + 0.08)

    def test_bound_without_tools(self):
        self.assertAlmostEqual(trial.worst_case_usd(30_000, 32_000, 0), 30_000 * 2.5e-6 + 0.32)

    def test_bound_over_cap_blocks_before_request(self):
        with tempfile.TemporaryDirectory() as d:
            spend = Path(d) / "spend.json"
            spend.write_text(json.dumps({"total_usd": 2.5}))
            with self.assertRaises(trial.BudgetExceeded):
                trial.check_budget(spend, extra=trial.worst_case_usd(30_000, 32_000, 8))


class SplitModeTest(unittest.TestCase):
    def setUp(self):
        self.sources = json.loads((HERE / "sources.json").read_text())
        self.cands = trial.parse_pubmed((FIXTURES / "pubmed_sample.xml").read_text())

    def test_combined_request(self):
        r = trial.build_request(self.cands, self.sources, "2026-11-26")
        self.assertEqual(r["tools"][0]["type"], "web_search_20260209")
        self.assertIn("format", r["output_config"])
        self.assertEqual(r["output_config"]["effort"], "high")
        self.assertEqual(r["cache_control"], {"type": "ephemeral"})

    def test_search_call_has_no_format(self):
        a = trial.build_search_request(self.sources, "2026-11-26")
        self.assertEqual(a["tools"][0]["allowed_domains"], self.sources["tier2_domains"])
        self.assertNotIn("format", a.get("output_config", {}))

    def test_write_call_has_no_tools(self):
        b = trial.build_write_request(self.cands, "notes from the search call", "2026-11-26")
        self.assertNotIn("tools", b)
        self.assertIn("format", b["output_config"])
        self.assertIn("notes from the search call", b["messages"][0]["content"])


class ReplayTest(unittest.TestCase):
    def test_windows(self):
        from datetime import date

        w = trial.replay_windows(date(2026, 11, 27), weeks=8)
        self.assertEqual(len(w), 24)
        for ed, start, end in w:
            self.assertIn(ed.weekday(), (0, 2, 4))
            self.assertEqual((end - start).days + 1, 3 if ed.weekday() == 0 else 2)
            self.assertLess(ed, date(2026, 11, 27))

    def test_projection(self):
        # base US$0.10 + US$0.01 per candidate; windows of 10 and 20 candidates
        p = trial.per_window_projection(base_usd=0.10, per_candidate_usd=0.01, counts=[10, 20])
        self.assertAlmostEqual(p["mean_window_usd"], 0.25)
        self.assertAlmostEqual(p["monthly_usd"], 0.25 * 13)

    def test_uncached_cost_prices_cache_reads_as_writes(self):
        u = {"input_tokens": 10, "output_tokens": 1000, "cache_creation_input_tokens": 90,
             "cache_read_input_tokens": 900_000, "web_search_requests": 1}
        expected = 900_100 * 2.50 / 1e6 + 1000 * 10 / 1e6 + 0.01
        self.assertAlmostEqual(trial.uncached_cost_usd(u), expected)

    def test_project_from_run_base_not_negative_with_cache_reads(self):
        # a run whose input was mostly read from cache must not yield a negative fixed part
        cands = [{"pmid": str(i), "journal": "J", "title": "t", "date": "2026-11-20",
                  "url": "https://doi.org/10.0/x", "abstract": "a" * 2000} for i in range(10)]
        from trial import _candidates_block
        chars = len(_candidates_block(cands)) + 5000
        # like the real run: input mostly read from cache, so the billed cost is below the
        # candidates' input at the full rate (the old projection then gave a negative base)
        usage = {"input_tokens": 10, "output_tokens": 1000, "cache_creation_input_tokens": 2000,
                 "cache_read_input_tokens": 98_000, "web_search_requests": 0}
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "candidates.json").write_text(json.dumps({"log": [], "candidates": cands}))
            (d / "metrics.json").write_text(json.dumps({
                "usage": usage, "request_chars": chars, "first_turn_input_tokens": 100_010,
                "run_cost_usd": trial.cost_usd(usage), "monthly_projection_usd": 0}))
            (d / "replay.json").write_text(json.dumps({"windows": [{"candidates": 10}, {"candidates": 2}]}))
            p = trial.project_from_run(d, d / "replay.json")
        self.assertGreater(p["base_usd"], 0)
        self.assertGreater(p["uncached_run_usd"], p["run_cost_usd"])


def _bad_request(message):
    import anthropic
    import httpx2

    resp = httpx2.Response(400, request=httpx2.Request("POST", "https://api.anthropic.com/v1/messages"))
    return anthropic.BadRequestError(message, response=resp, body=None)


class _Msg:
    def __init__(self, text, stop="end_turn"):
        from types import SimpleNamespace as NS

        self.content = [NS(type="text", text=text)]
        self.stop_reason = stop
        self.stop_details = None
        self.model = "claude-sonnet-5-5"
        self.usage = NS(input_tokens=1000, output_tokens=100, cache_creation_input_tokens=0,
                        cache_read_input_tokens=0, server_tool_use=NS(web_search_requests=1, web_fetch_requests=0))


class _FakeClient:
    """Raises `first_error` on the first request, then answers in order."""

    def __init__(self, first_error, answers):
        self.first_error, self.answers, self.requests = first_error, list(answers), []
        self.messages = self
        self.error_on = None  # request number (1-based) that gets a 400
        self.crash = False

    def stream(self, **req):
        self.requests.append(req)
        client = self
        n = len(self.requests)

        class _S:
            def __enter__(self):
                if client.first_error is not None:
                    err, client.first_error = client.first_error, None
                    raise err
                if client.error_on == n:
                    raise _bad_request("rejected continuation")
                return self

            def __exit__(self, *a):
                return False

            def get_final_message(self):
                if client.crash:
                    raise ConnectionError("dropped mid-stream")
                return client.answers.pop(0)

        return _S()


class RunModelTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_spend = trial.SPEND_FILE
        trial.SPEND_FILE = Path(self.tmp.name) / "spend.json"
        sources = json.loads((HERE / "sources.json").read_text())
        cands = trial.parse_pubmed((FIXTURES / "pubmed_sample.xml").read_text())
        self.request = trial.build_request(cands, sources, "2026-11-26")
        self.split = (trial.build_search_request(sources, "2026-11-26"),
                      lambda notes: trial.build_write_request(cands, notes, "2026-11-26"))

    def tearDown(self):
        trial.SPEND_FILE = self.old_spend
        self.tmp.cleanup()

    def ledger(self):
        return trial.SpendLedger(trial.SPEND_FILE)

    def test_400_triggers_split_rerun(self):
        fake = _FakeClient(_bad_request("output_config.format is not supported with web_search"),
                           [_Msg("search notes"), _Msg('{"titulo": "x"}')])
        ledger = self.ledger()
        _, text, meta = trial.run_model(self.request, "k", ledger, self.split, client=fake)
        self.assertEqual(meta["u7"]["combined_call"], "rejected")
        self.assertEqual(text, '{"titulo": "x"}')
        self.assertEqual(len(fake.requests), 3)  # rejected combined, search, write
        self.assertNotIn("tools", fake.requests[2])
        self.assertIn("search notes", fake.requests[2]["messages"][0]["content"])
        self.assertEqual(ledger.usage["web_search_requests"], 2)
        # the projection uses the write call, which carries the candidates
        self.assertEqual(meta["request_chars"], trial.request_chars(fake.requests[2]))

    def test_credit_error_does_not_split_and_releases_reservation(self):
        trial.SPEND_FILE.write_text(json.dumps({"total_usd": 0.25}))
        fake = _FakeClient(_bad_request("Your credit balance is too low"), [])
        with self.assertRaises(Exception):
            trial.run_model(self.request, "k", self.ledger(), self.split, client=fake)
        self.assertEqual(len(fake.requests), 1)
        self.assertAlmostEqual(trial.spent_so_far(trial.SPEND_FILE), 0.25)  # unbilled: nothing kept

    def test_continuation_resends_request_unchanged(self):
        fake = _FakeClient(None, [_Msg("", stop="pause_turn"), _Msg('{"ok": 1}')])
        trial.run_model(self.request, "k", self.ledger(), self.split, client=fake)
        # the continuation is resent unchanged (documented pause_turn pattern)
        self.assertEqual(fake.requests[1]["tools"], fake.requests[0]["tools"])
        self.assertEqual(fake.requests[1]["messages"][0], self.request["messages"][0])
        self.assertEqual(fake.requests[1]["messages"][1]["role"], "assistant")

    def test_empty_search_notes_stop_before_write_call(self):
        fake = _FakeClient(_bad_request("format not supported"), [_Msg("", stop="max_tokens")])
        with self.assertRaises(trial.SplitAborted):
            trial.run_model(self.request, "k", self.ledger(), self.split, client=fake)
        self.assertEqual(len(fake.requests), 2)  # no write call

    def test_400_after_a_billed_turn_does_not_split(self):
        fake = _FakeClient(None, [_Msg("", stop="pause_turn")])
        fake.error_on = 2  # the continuation is rejected
        with self.assertRaises(Exception):
            trial.run_model(self.request, "k", self.ledger(), self.split, client=fake)
        self.assertEqual(len(fake.requests), 2)

    def test_pause_turn_continues_and_sums(self):
        fake = _FakeClient(None, [_Msg("", stop="pause_turn"), _Msg('{"ok": 1}')])
        ledger = self.ledger()
        _, text, meta = trial.run_model(self.request, "k", ledger, self.split, client=fake)
        self.assertEqual(text, '{"ok": 1}')
        self.assertEqual(ledger.usage["input_tokens"], 2000)
        self.assertEqual([t["web_search_requests"] for t in ledger.turns], [1, 1])
        self.assertEqual(meta["u7"]["combined_call"], "ok")

    def test_spend_on_disk_after_each_turn(self):
        fake = _FakeClient(None, [_Msg('{"ok": 1}')])
        ledger = self.ledger()
        trial.run_model(self.request, "k", ledger, self.split, client=fake)
        self.assertAlmostEqual(trial.spent_so_far(trial.SPEND_FILE), ledger.run_cost())

    def test_crash_mid_request_keeps_reservation(self):
        fake = _FakeClient(None, [])
        fake.crash = True
        with self.assertRaises(ConnectionError):
            trial.run_model(self.request, "k", self.ledger(), self.split, client=fake)
        self.assertGreater(trial.spent_so_far(trial.SPEND_FILE), 0.5)  # the worst case stays reserved

    def test_reservation_over_cap_blocks_before_request(self):
        trial.SPEND_FILE.write_text(json.dumps({"total_usd": 2.0}))
        fake = _FakeClient(None, [_Msg('{"ok": 1}')])
        with self.assertRaises(trial.BudgetExceeded):
            trial.run_model(self.request, "k", self.ledger(), self.split, client=fake)
        self.assertEqual(fake.requests, [])


class SlotTest(unittest.TestCase):
    """Edition slots (Filipe, 2026-11-27)."""

    def setUp(self):
        from datetime import date, timedelta

        self.today = date(2026, 11, 27)
        self.cands = []
        self._day = lambda age: (self.today - timedelta(days=age)).isoformat()

    def art(self, n, age=5):
        pmid = f"{len(self.cands) + 1}"
        self.cands.append({"pmid": pmid, "date": self._day(age)})
        return {"categoria": "artigo", "candidato": pmid, "titulo": f"a{n}", "publicadoEm": ""}

    def t2(self, cat, n, age=2):
        return {"categoria": cat, "candidato": "", "titulo": f"{cat}{n}", "publicadoEm": self._day(age)}

    def pick(self, ranked):
        items, log = trial.select_items(ranked, self.cands, self.today)
        return [i["titulo"] for i in items], log

    def test_filipe_example_articles_yield_to_empty_categories(self):
        # 5 articles ranked first, then 1 news and 1 alert: articles drop to 4
        ranked = [self.art(i) for i in range(5)] + [self.t2("noticia", 1), self.t2("alerta", 1)]
        got, _ = self.pick(ranked)
        self.assertEqual(got, ["a0", "a1", "a2", "a3", "alerta1", "noticia1"])

    def test_articles_fill_free_places_when_nothing_else(self):
        got, _ = self.pick([self.art(i) for i in range(6)])
        self.assertEqual(len(got), 6)

    def test_only_one_article_older_than_30_days_in_its_slot(self):
        ranked = [self.art(0, age=40), self.art(1, age=50), self.t2("alerta", 1)]
        got, log = self.pick(ranked)
        # the second old article only gets a free place, after the in-cap alert
        self.assertEqual(log[0]["placed"], "artigo slot, 90 days")
        self.assertEqual(log[1]["placed"], "free place")
        self.assertEqual(log[2]["placed"], "alerta slot, 30 days")

    def test_caps_sum_past_six_keeps_rank_order(self):
        ranked = ([self.art(0), self.art(1), self.art(2, age=60), self.t2("diretriz", 1, age=30)]
                  + [self.t2("alerta", i) for i in range(2)] + [self.t2("noticia", i) for i in range(2)])
        got, log = self.pick(ranked)
        # every category's best item first, then the other in-cap items in rank order
        self.assertEqual(got, ["a0", "a1", "a2", "diretriz1", "alerta0", "noticia0"])
        self.assertTrue(log[5]["placed"].startswith("not placed"))
        self.assertTrue(log[7]["placed"].startswith("not placed"))

    def test_empty_category_beats_a_second_item(self):
        # news ranked last still beats the second alert
        ranked = [self.art(0), self.art(1), self.art(2), self.t2("diretriz", 1, age=10),
                  self.t2("alerta", 0), self.t2("alerta", 1), self.t2("noticia", 0)]
        got, _ = self.pick(ranked)
        self.assertIn("noticia0", got)
        self.assertNotIn("alerta1", got)

    def test_duplicate_url_dropped(self):
        n = self.t2("noticia", 1) | {"url": "https://cdc.gov/x"}
        got, log = self.pick([n, dict(n)])
        self.assertEqual(len(got), 1)
        self.assertEqual(log[1]["dropped"], "duplicate")

    def test_article_date_rendered_from_pubmed(self):
        a = self.art(0, age=3) | {"publicadoEm": "2020-01-01"}
        self.pick([a])
        self.assertEqual(a["publicadoEm"], self._day(3))

    def test_windows_drop_out_of_range_items(self):
        ranked = [self.t2("noticia", 1, age=8), self.t2("diretriz", 1, age=61), self.t2("alerta", 1, age=31),
                  self.art(0, age=91), self.t2("noticia", 2, age=7)]
        got, log = self.pick(ranked)
        self.assertEqual(got, ["noticia2"])
        self.assertEqual([("dropped" in r) for r in log], [True, True, True, True, False])

    def test_unknown_candidate_and_missing_date_dropped(self):
        ranked = [{"categoria": "artigo", "candidato": "999", "titulo": "x", "publicadoEm": ""},
                  self.t2("alerta", 1) | {"publicadoEm": ""}]
        got, log = self.pick(ranked)
        self.assertEqual(got, [])
        self.assertEqual(log[0]["dropped"], "not a collected candidate")
        self.assertEqual(log[1]["dropped"], "no publication date")

    def test_article_age_comes_from_pubmed_not_the_model(self):
        a = self.art(0, age=200) | {"publicadoEm": self._day(1)}
        got, log = self.pick([a])
        self.assertEqual(got, [])
        self.assertIn("outside the 90-day window", log[0]["dropped"])

    def test_edition_order_articles_first(self):
        ranked = [self.t2("noticia", 1), self.art(0), self.t2("diretriz", 1, age=10)]
        got, _ = self.pick(ranked)
        self.assertEqual(got, ["a0", "diretriz1", "noticia1"])


class CollectTest(unittest.TestCase):
    def test_two_windows_tagged(self):
        from datetime import date
        from unittest import mock

        calls = []

        def fake_esearch(term, days, retmax, mindate=None, maxdate=None):
            calls.append((days, retmax, mindate, maxdate))
            return {"idlist": ["90000001"] if mindate is None else ["90000002", "90000001"]}

        xml = (FIXTURES / "pubmed_sample.xml").read_text()
        sources = {"tier1": [{"name": "J", "ta": "J Pediatr", "general": False}]}
        with mock.patch.object(trial, "esearch", fake_esearch), \
                mock.patch.object(trial, "efetch", lambda ids: xml), mock.patch.object(trial.time, "sleep"):
            cands, log = trial.collect(sources, date(2026, 11, 27))
        self.assertEqual(calls[0], (30, 3, None, None))
        self.assertEqual(calls[1][2:], (date(2026, 8, 29), date(2026, 10, 27)))
        self.assertEqual({c["pmid"]: c["janela"] for c in cands}, {"90000001": "30d", "90000002": "90d"})
        self.assertEqual(log[0]["found_90d"], 1)  # a record in both windows counts as recent


class TwoCallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.spend = Path(self.tmp.name) / "spend.json"
        sources = json.loads((HERE / "sources.json").read_text())
        self.cands = trial.parse_pubmed((FIXTURES / "pubmed_sample.xml").read_text())
        self.search = trial.build_search_request(sources, "2026-11-27")

    def tearDown(self):
        self.tmp.cleanup()

    def test_search_then_write(self):
        fake = _FakeClient(None, [_Msg("notes"), _Msg('{"titulo": "x"}')])
        _, text, meta = trial.run_two_calls(
            self.search, lambda n: trial.build_write_request(self.cands, n, "2026-11-27"), "k",
            trial.SpendLedger(self.spend), client=fake)
        self.assertEqual(text, '{"titulo": "x"}')
        self.assertEqual(meta["u7"], {"flow": "two calls"})
        self.assertIn("tools", fake.requests[0])
        self.assertNotIn("format", fake.requests[0].get("output_config", {}))
        self.assertNotIn("tools", fake.requests[1])
        self.assertIn("<search_notes>\nnotes", fake.requests[1]["messages"][0]["content"])

    def test_no_search_aborts_before_write_and_notes_saved(self):
        from types import SimpleNamespace as NS

        msg = _Msg("nothing found")
        msg.usage.server_tool_use = NS(web_search_requests=0)
        fake = _FakeClient(None, [msg])
        saved = []
        with self.assertRaises(trial.SplitAborted):
            trial.run_two_calls(self.search, lambda n: trial.build_write_request(self.cands, n, "2026-11-27"),
                                "k", trial.SpendLedger(self.spend), client=fake, save_notes=saved.append)
        self.assertEqual(len(fake.requests), 1)  # no write call
        self.assertEqual(saved, ["nothing found"])

    def test_search_errors_listed(self):
        from types import SimpleNamespace as NS

        content = [NS(type="server_tool_use"),
                   NS(type="web_search_tool_result", content=NS(type="web_search_tool_result_error",
                                                               error_code="too_many_requests")),
                   NS(type="web_search_tool_result", content=[NS(url="https://cdc.gov/x", title="t")])]
        self.assertEqual(trial.search_errors(content), ["too_many_requests"])

    def test_search_prompt_demands_searches_and_windows(self):
        p = self.search["system"]
        self.assertIn("at least one search for guidelines, one for safety alerts and one for news", p)
        for w in ("last 60 days", "last 30 days", "last 7 days"):
            self.assertIn(w, p)


class MiscTest(unittest.TestCase):
    def test_round_robin(self):
        groups = [[{"j": "a", "i": i} for i in range(5)], [{"j": "b", "i": 0}], [{"j": "c", "i": 0}]]
        out = trial.round_robin(groups, 4)
        self.assertEqual([x["j"] for x in out], ["a", "b", "c", "a"])

    def test_redirects_not_followed(self):
        h = trial._NoRedirect()
        self.assertIsNone(h.redirect_request(None, None, 302, "Found", {}, "http://169.254.169.254/"))

    def test_key_file_inside_repo_refused(self):
        with self.assertRaises(SystemExit):
            trial.read_key(str(HERE / "sources.json"))


if __name__ == "__main__":
    unittest.main()
