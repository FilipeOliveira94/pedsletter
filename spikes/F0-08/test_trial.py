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


class RenderTest(unittest.TestCase):
    def test_notices_verbatim(self):
        resp = json.loads((FIXTURES / "response.json").read_text())
        md = trial.render_markdown(resp, "2026-11-26")
        self.assertIn(AI_NOTICE, md)
        self.assertIn(AUDIENCE_NOTICE, md)
        # AI notice comes before the first item
        self.assertLess(md.index(AI_NOTICE), md.index(resp["artigos"][0]["titulo"]))


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


if __name__ == "__main__":
    unittest.main()
