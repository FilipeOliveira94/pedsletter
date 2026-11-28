"""Unit tests for the F1-06 authorship check. No network.

Fixture text is built from `src/config/authorship.json`, so this file holds no
block-list term in plain text. The names are invented placeholders.

Run: make test
"""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import authorship_check as ac  # noqa: E402

CONFIG = json.loads((ROOT / "src/config/authorship.json").read_text(encoding="utf-8"))
TERMS = CONFIG["terms"]
VAR = CONFIG["names_env"]
NAMES = ["Joana Exemplo", "Zé Fictício"]
ENV = {VAR: "\n".join(NAMES)}


def run(argv, environ=ENV):
    """Run the CLI in-process; return (exit code, stdout + stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ac.main(argv, environ)
    return code, out.getvalue() + err.getvalue()


def scan(text):
    return ac.scan_text(text, "x", ac.load_rules(ENV))


def hits(text):
    return [(f.line, f.kind, f.index) for f in scan(text)]


class FixedTerms(unittest.TestCase):
    def test_each_term_hits_with_its_index(self):
        for i, term in enumerate(TERMS, 1):
            with self.subTest(index=i):
                self.assertEqual(hits(f"Texto {term} 12345 aqui."), [(1, "term", i)])

    def test_case_accents_and_spacing_do_not_hide_a_term(self):
        review = TERMS[4]  # two words
        resp = TERMS[5]  # two words with accents
        bare = resp.replace("é", "e").replace("á", "a")
        for text in (
            review.upper(),
            review.replace(" ", "   "),
            review.replace(" ", " "),
            bare,
            bare.upper(),
        ):
            with self.subTest(text=text):
                self.assertTrue(hits(text))

    def test_entities_tags_and_attributes(self):
        review_a, review_b = TERMS[4].split(" ")
        addr = TERMS[2]
        for text in (
            addr.replace(".", "&period;") + " Silva",
            f"{review_a} <em>{review_b}</em> alguém",
            f'<meta name="author" content="{addr} X">',
            TERMS[5].replace("é", "&eacute;"),
        ):
            with self.subTest(text=text):
                self.assertTrue(hits(text))

    def test_phrase_split_across_two_lines(self):
        a, b = TERMS[4].split(" ")
        self.assertEqual(hits(f"um texto {a}\n{b} alguém"), [(1, "term", 5)])

    def test_invisible_characters_do_not_hide_a_term(self):
        a, b = NAMES[0].split(" ")
        for text in (f"{a}\u200b {b}", f"{a[:2]}\u00ad{a[2:]} {b}", f"{a[:2]}&shy;{a[2:]} {b}", f"\ufeff{a} {b}", f"{a}\u034f {b}", f"{a}\ufe0f {b}"):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [(1, "name", 1)])

    def test_slugs_and_percent_encoding(self):
        slug = NAMES[0].replace(" ", "-").lower()
        for text in (f"https://x.org/{slug}/", NAMES[0].replace(" ", "%20"), NAMES[0].replace(" ", "_")):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [(1, "name", 1)])

    def test_wrapped_line_with_quote_or_list_marker(self):
        a, b = NAMES[0].split(" ")
        for text in (f"> {a}\n> {b}", f"- texto {a}\n  {b}", f"{a}\\\n{b}"):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [(1, "name", 1)])

    def test_hash_strings_do_not_cause_false_hits(self):
        blob = "sha512-9" + TERMS[0].lower() + "+" + "a1B2c3D4" * 5 + "=="
        self.assertEqual(hits(f'"integrity": "{blob}"'), [])
        digest = "a1b2c3d4e5f6" + TERMS[1].lower() + "9" + "0a1b2c3d4e5f6"
        self.assertEqual(hits(f"_astro/index.{digest}.css"), [])

    def test_name_in_a_deep_url_path_hits(self):
        a, b = NAMES[0].lower().split(" ")
        self.assertEqual(hits(f"[p](https://example.com/medicos/2026/{a}/{b}/perfil)"), [(1, "name", 1)])

    def test_term_inside_a_longer_word_does_not_hit(self):
        acronym = TERMS[0]
        self.assertEqual(hits(f"x{acronym}y {acronym.lower()}ido"), [])

    def test_term_followed_by_digits_or_punctuation_hits(self):
        acronym = TERMS[0]
        for text in (f"{acronym}12345", f"{acronym}-SP 1", f"({acronym}/SP)"):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [(1, "term", 1)])

    def test_quoting_a_term_is_not_an_exemption(self):
        self.assertTrue(hits(f'the list ("{TERMS[0]}", "{TERMS[2]}")'))

    def test_clean_text_passes(self):
        self.assertEqual(hits("Resumo de um ensaio clínico pediátrico. Confira a fonte."), [])

    def test_config_file_holds_no_term_in_plain_text(self):
        raw = (ROOT / "src/config/authorship.json").read_text(encoding="utf-8")
        self.assertEqual(scan(raw), [])


class Names(unittest.TestCase):
    def test_missing_variable_fails(self):
        code, out = run(["--text-env", "T"], {"T": "ok"})
        self.assertEqual(code, 2)
        self.assertIn(VAR, out)

    def test_empty_or_blank_variable_fails(self):
        for value in ("", "  \n ; , "):
            with self.subTest(value=value):
                code, _ = run(["--text-env", "T"], {VAR: value, "T": "ok"})
                self.assertEqual(code, 2)

    def test_name_hits_across_case_and_accents(self):
        self.assertEqual(hits("Texto de ZE FICTICIO."), [(1, "name", 2)])
        self.assertEqual(hits("joana  exemplo"), [(1, "name", 1)])

    def test_semicolon_and_comma_separate_names(self):
        rules = ac.load_rules({VAR: "Joana Exemplo; Zé Fictício, Outro Nome"})
        self.assertEqual(len(rules.names), 3)

    def test_registration_number_inside_a_longer_number_does_not_hit(self):
        rules = ac.load_rules({VAR: "123456"})
        self.assertEqual(ac.scan_text("nº 1234567", "x", rules), [])
        self.assertEqual(len(ac.scan_text("nº 123456.", "x", rules)), 1)


class Output(unittest.TestCase):
    def test_output_never_carries_the_term_the_name_or_the_line(self):
        env = dict(ENV, T=f"linha secreta {TERMS[0]} e {NAMES[1]}")
        code, out = run(["--text-env", "T"], env)
        self.assertEqual(code, 1)
        self.assertIn("T:1: term #1", out)
        self.assertIn("T:1: name #2", out)
        for secret in (TERMS[0], NAMES[1], "secreta"):
            self.assertNotIn(secret.casefold(), out.casefold())

    def test_github_annotation(self):
        env = dict(ENV, T=TERMS[3], GITHUB_ACTIONS="true")
        _, out = run(["--text-env", "T"], env)
        self.assertIn("::error title=authorship::T:1: term #4", out)

    def test_unset_text_variable_is_empty_text(self):
        code, _ = run(["--text-env", "NOT_SET"])
        self.assertEqual(code, 0)


class Files(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir)
        self.cwd = os.getcwd()
        os.chdir(self.dir)
        self.addCleanup(os.chdir, self.cwd)

    def git(self, *args):
        subprocess.run(["git", *args], check=True, capture_output=True)

    def test_html_dir_is_scanned_and_must_exist(self):
        site = self.dir / "dist"
        site.mkdir()
        (site / "index.html").write_text(f"<p>{NAMES[0]}</p>", encoding="utf-8")
        (site / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")
        code, out = run(["--html", "dist"])
        self.assertEqual(code, 1)
        self.assertIn("dist/index.html:1: name #1", out)
        self.assertIn("1 file skipped", out)
        _, out = run(["--html", "dist"], dict(ENV, GITHUB_ACTIONS="true"))
        self.assertIn("::error file=dist/index.html,line=1,title=authorship::dist/index.html:1: name #1", out)
        code, _ = run(["--html", "missing"])
        self.assertEqual(code, 2)

    def test_non_utf8_text_files_are_scanned(self):
        site = self.dir / "dist"
        site.mkdir()
        (site / "a.txt").write_bytes(NAMES[1].encode("cp1252"))
        (site / "b.txt").write_bytes(NAMES[1].encode("utf-16"))
        code, out = run(["--html", "dist"])
        self.assertEqual(code, 1)
        self.assertIn("dist/a.txt:1: name #2", out)
        self.assertIn("dist/b.txt:1: name #2", out)

    def test_path_with_a_dotted_term_is_redacted(self):
        site = self.dir / "dist"
        site.mkdir()
        (site / f"{TERMS[2]}x.md").write_text(NAMES[0], encoding="utf-8")
        _, out = run(["--html", "dist"])
        self.assertIn("<redacted path #1>:0: term #3", out)
        self.assertIn("<redacted path #1>:1: name #1", out)

    def test_path_that_carries_a_name_is_redacted(self):
        site = self.dir / "dist"
        site.mkdir()
        (site / "joana-exemplo.html").write_text(TERMS[1], encoding="utf-8")
        code, out = run(["--html", "dist"])
        self.assertEqual(code, 1)
        self.assertIn("<redacted path #1>:1: term #2", out)
        self.assertIn("<redacted path #1>:0: name #1", out)
        self.assertNotIn("joana", out.casefold())

    def test_repo_scans_tracked_files_only(self):
        self.git("init", "-q")
        Path("tracked.md").write_text(f"x {TERMS[6]}\n", encoding="utf-8")
        Path("untracked.md").write_text(f"x {TERMS[0]}\n", encoding="utf-8")
        self.git("add", "tracked.md")
        code, out = run(["--repo"])
        self.assertEqual(code, 1)
        self.assertIn("tracked.md:1: term #7", out)
        self.assertNotIn("untracked.md", out)

    def test_staged_reads_the_index_not_the_worktree(self):
        self.git("init", "-q")
        Path("a.md").write_text(f"{NAMES[0]}\n", encoding="utf-8")
        self.git("add", "a.md")
        Path("a.md").write_text("limpo\n", encoding="utf-8")
        code, out = run(["--staged"])
        self.assertEqual(code, 1)
        self.assertIn("a.md:1: name #1", out)

        self.git("add", "a.md")
        Path("a.md").write_text(f"{NAMES[0]}\n", encoding="utf-8")
        code, _ = run(["--staged"])
        self.assertEqual(code, 0)

    def test_hook_runs_the_staged_check(self):
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.invalid")
        self.git("config", "user.name", "t")
        self.git("config", "core.hooksPath", str(ROOT / "scripts/hooks"))
        Path("a.md").write_text(f"{TERMS[2]} X\n", encoding="utf-8")
        self.git("add", "a.md")
        env = {k: v for k, v in os.environ.items() if k != VAR}
        refused = subprocess.run(["git", "commit", "-qm", "x"], env={**env, **ENV}, capture_output=True, text=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("a.md:1: term #3", refused.stdout + refused.stderr)

        no_var = subprocess.run(["git", "commit", "-qm", "x"], env=env, capture_output=True, text=True)
        self.assertNotEqual(no_var.returncode, 0)
        self.assertIn(VAR, no_var.stdout + no_var.stderr)

        Path("a.md").write_text("limpo\n", encoding="utf-8")
        self.git("add", "a.md")
        ok = subprocess.run(["git", "commit", "-qm", "x"], env={**env, **ENV}, capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)


if __name__ == "__main__":
    unittest.main()
