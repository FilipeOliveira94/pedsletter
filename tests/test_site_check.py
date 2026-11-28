"""Unit tests for the F1-03 page walker (scripts/site_check.py). No network.

Each test builds a small `dist/` in a temporary folder: a valid site passes,
and each broken rule fails with the file named.

Run: make test
"""

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import site_check as sc  # noqa: E402

RULES = sc.load_rules()
PUBLICO = RULES.avisos["publico"]
CURADORIA = RULES.avisos["curadoriaIA"]

HEADERS = """# comment
/*
  X-Robots-Tag: noindex, nofollow
  Content-Security-Policy: script-src 'none'
"""
ROBOTS = "User-agent: *\nAllow: /\n"


def page(body="", head='<meta name="robots" content="noindex, nofollow">', ai=False):
    notice = f"<p>{CURADORIA}</p>" if ai else ""
    return (
        f"<!doctype html><html><head>{head}<title>t</title></head>"
        f"<body>{notice}{body}<footer><p>{PUBLICO}</p></footer></body></html>"
    )


class SiteCheckTest(unittest.TestCase):
    def setUp(self):
        self.dist = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dist)
        self.write("index.html", page(ai=True))
        self.write("sobre/index.html", page("<p>Sobre</p>"))
        self.write("_headers", HEADERS)
        self.write("robots.txt", ROBOTS)

    def write(self, rel, text):
        path = self.dist / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def findings(self, rules=RULES):
        return sc.check(self.dist, rules)

    def assertFails(self, path, fragment):
        found = self.findings()
        self.assertTrue(
            any(f.path == path and fragment in f.message for f in found),
            f"expected a finding on {path} with {fragment!r}, got {found}",
        )

    def test_valid_site_passes(self):
        self.assertEqual(self.findings(), [])

    def test_valid_site_cli_exit_zero(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(sc.main([str(self.dist)]), 0)

    def test_missing_robots_meta(self):
        self.write("sobre/index.html", page(head=""))
        self.assertFails("sobre/index.html", "noindex")

    def test_robots_meta_without_noindex(self):
        self.write("sobre/index.html", page(head='<meta name="robots" content="nofollow">'))
        self.assertFails("sobre/index.html", "noindex")

    def test_robots_meta_name_is_case_insensitive(self):
        self.write("sobre/index.html", page(head='<META NAME="Robots" CONTENT="NOINDEX">'))
        self.assertEqual(self.findings(), [])

    def test_missing_audience_notice(self):
        self.write("sobre/index.html", page().replace(PUBLICO, "outro texto"))
        self.assertFails("sobre/index.html", "audience notice")

    def test_notice_split_across_lines_passes(self):
        self.write("sobre/index.html", page().replace(PUBLICO, PUBLICO.replace(" ", "\n  ", 2)))
        self.assertEqual(self.findings(), [])

    def test_notice_with_entities_passes(self):
        self.write("sobre/index.html", page().replace(PUBLICO, PUBLICO.replace("ú", "&uacute;")))
        self.assertEqual(self.findings(), [])

    def test_notice_inside_style_does_not_count(self):
        self.write("sobre/index.html", page().replace(f"<p>{PUBLICO}</p>", f"<style>{PUBLICO}</style>"))
        self.assertFails("sobre/index.html", "audience notice")

    def test_missing_ai_notice_on_home(self):
        self.write("index.html", page())
        self.assertFails("index.html", "AI notice")

    def test_ai_notice_not_required_elsewhere(self):
        self.assertNotIn("sobre/index.html", [f.path for f in self.findings()])

    def test_ai_notice_path_glob(self):
        rules = sc.Rules(RULES.avisos, ai_notice_paths=["index.html", "edicoes/*"], script_allowed_paths=[])
        self.write("edicoes/2026/x/index.html", page())
        found = sc.check(self.dist, rules)
        self.assertTrue(any(f.path == "edicoes/2026/x/index.html" and "AI notice" in f.message for f in found))

    def test_script_fails(self):
        self.write("sobre/index.html", page('<script type="module">1</script>'))
        self.assertFails("sobre/index.html", "<script>")

    def test_external_script_fails(self):
        self.write("sobre/index.html", page(head='<meta name="robots" content="noindex"><script src="/a.js"></script>'))
        self.assertFails("sobre/index.html", "<script>")

    def test_script_allowed_under_calculator_path(self):
        rules = sc.Rules(RULES.avisos, ai_notice_paths=["index.html"], script_allowed_paths=["calculadoras/*"])
        self.write("calculadoras/imc/index.html", page("<script>1</script>"))
        self.assertEqual(sc.check(self.dist, rules), [])

    def test_sitemap_file_fails(self):
        self.write("sitemap-index.xml", "<xml/>")
        self.assertFails("sitemap-index.xml", "sitemap")

    def test_gzipped_sitemap_fails(self):
        self.write("sub/Sitemap.xml.gz", "x")
        self.assertFails("sub/Sitemap.xml.gz", "sitemap")

    def test_sitemap_link_fails(self):
        self.write("sobre/index.html", page(head='<meta name="robots" content="noindex"><link rel="sitemap" href="/s.xml">'))
        self.assertFails("sobre/index.html", "sitemap")

    def test_missing_robots_txt(self):
        (self.dist / "robots.txt").unlink()
        self.assertFails("robots.txt", "missing")

    def test_robots_disallow_fails(self):
        self.write("robots.txt", "User-agent: *\n  disallow : /privado\n")
        self.assertFails("robots.txt", "Disallow")

    def test_robots_sitemap_line_fails(self):
        self.write("robots.txt", ROBOTS + "Sitemap: https://x/s.xml\n")
        self.assertFails("robots.txt", "Sitemap")

    def test_robots_disallow_in_comment_passes(self):
        self.write("robots.txt", ROBOTS + "# no Disallow: here\n")
        self.assertEqual(self.findings(), [])

    def test_missing_headers_file(self):
        (self.dist / "_headers").unlink()
        self.assertFails("_headers", "X-Robots-Tag")

    def test_headers_without_robots_tag(self):
        self.write("_headers", "/*\n  Content-Security-Policy: script-src 'none'\n")
        self.assertFails("_headers", "X-Robots-Tag")

    def test_headers_robots_tag_on_other_path_only(self):
        self.write("_headers", "/sobre/*\n  X-Robots-Tag: noindex\n/*\n  Content-Security-Policy: script-src 'none'\n")
        self.assertFails("_headers", "X-Robots-Tag")

    def test_headers_without_csp(self):
        self.write("_headers", "/*\n  X-Robots-Tag: noindex\n")
        self.assertFails("_headers", "Content-Security-Policy")

    def test_headers_csp_with_weaker_script_src(self):
        self.write("_headers", "/*\n  X-Robots-Tag: noindex\n  Content-Security-Policy: default-src 'self'; script-src 'self'\n")
        self.assertFails("_headers", "Content-Security-Policy")

    def test_headers_csp_with_more_directives_passes(self):
        self.write("_headers", "/*\n  X-Robots-Tag: noindex\n  content-security-policy: object-src 'none'; script-src 'none'\n")
        self.assertEqual(self.findings(), [])

    def test_headers_detach_on_subpath_fails(self):
        self.write("_headers", HEADERS + "/calculadoras/*\n  ! Content-Security-Policy\n  ! X-Robots-Tag\n")
        found = [f.message for f in self.findings() if f.path == "_headers"]
        self.assertEqual(len(found), 2, found)

    def test_headers_csp_script_src_elem_loosened_fails(self):
        self.write("_headers", "/*\n  X-Robots-Tag: noindex\n  Content-Security-Policy: script-src 'none'; script-src-elem 'self'\n")
        self.assertFails("_headers", "Content-Security-Policy")

    def test_notice_in_hidden_containers_does_not_count(self):
        for wrap in ("<template>{}</template>", "<noscript>{}</noscript>", "<div hidden>{}</div>", "<textarea>{}</textarea>"):
            with self.subTest(wrap=wrap):
                self.write("sobre/index.html", page().replace(f"<p>{PUBLICO}</p>", wrap.format(PUBLICO)))
                self.assertFails("sobre/index.html", "audience notice")

    def test_notice_in_title_does_not_count(self):
        self.write("sobre/index.html", page().replace(f"<p>{PUBLICO}</p>", "").replace("<title>t", f"<title>{PUBLICO}"))
        self.assertFails("sobre/index.html", "audience notice")

    def test_text_after_hidden_container_counts(self):
        self.write("sobre/index.html", page().replace("<footer>", "<div hidden><p>x</p></div><footer>"))
        self.assertEqual(self.findings(), [])

    def test_hidden_void_element_does_not_hide_later_text(self):
        self.write("sobre/index.html", page().replace("<footer>", '<input type="hidden" hidden><footer>'))
        self.assertEqual(self.findings(), [])

    def test_robots_meta_inside_noscript_does_not_count(self):
        self.write("sobre/index.html", page(head='<noscript><meta name="robots" content="noindex"></noscript>'))
        self.assertFails("sobre/index.html", "noindex")

    def test_robots_disallow_after_bom_fails(self):
        (self.dist / "robots.txt").write_text("Disallow: /\n", encoding="utf-8-sig")
        self.assertFails("robots.txt", "Disallow")

    def test_sitemap_txt_fails(self):
        self.write("sitemap.txt", "https://x/\n")
        self.assertFails("sitemap.txt", "sitemap")

    def test_empty_dist_fails(self):
        shutil.rmtree(self.dist)
        self.dist.mkdir()
        self.assertTrue(any("no HTML page" in f.message for f in self.findings()))

    def test_missing_dist_is_setup_error(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(sc.main([str(self.dist / "nope")]), 2)

    def test_cli_exit_one_and_names_file(self):
        self.write("sobre/index.html", page("<script>1</script>"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(sc.main([str(self.dist)]), 1)
        self.assertIn("sobre/index.html", out.getvalue())


class RealConfigTest(unittest.TestCase):
    def test_notices_load_from_shared_json(self):
        self.assertTrue(PUBLICO.startswith("Conteúdo destinado"))
        self.assertTrue(CURADORIA.startswith("Curadoria e resumos"))

    def test_home_needs_ai_notice(self):
        self.assertIn("index.html", RULES.ai_notice_paths)


if __name__ == "__main__":
    unittest.main()
