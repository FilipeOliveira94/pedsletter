"""Walk the built site and fail when a page breaks a §4 or §5 rule (F1-03).

Rules checked on `dist/` (AGENTS.md §4 and §5, ADR-002):

- every `.html` page has `<meta name="robots">` whose content includes
  `noindex`;
- every page carries the audience notice, and every page matched by
  `aiNoticePaths` also carries the AI notice (text after HTML parsing, with
  entities decoded and whitespace collapsed; text inside `<script>` and
  `<style>` does not count);
- no page outside `scriptAllowedPaths` has a `<script>` element;
- no sitemap: no `sitemap*.xml` or `sitemap*.xml.gz` file, no
  `<link rel="sitemap">`;
- `robots.txt` exists and has no `Disallow` and no `Sitemap` line;
- `_headers` has a `/*` rule with `X-Robots-Tag` including `noindex` and a
  `Content-Security-Policy` whose `script-src` is exactly `'none'`;
- at least one page exists, so an empty build never passes.

The notice wording comes from `src/config/avisos.json` (the file `site.ts`
imports) and the path rules from `src/config/site-check.json`.

`noindex` is required whatever `indexavel` says: this check is the guard until
phase 9, and F9-04 changes it together with the switch in `site.ts`.

CLI (exit 0 clean, 1 findings, 2 setup error):

    python3 scripts/site_check.py dist
"""

from __future__ import annotations

import fnmatch
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "src" / "config"
SPACES = re.compile(r"\s+")
SITEMAP_FILE = re.compile(r"sitemap.*\.xml(\.gz)?", re.IGNORECASE)
ROBOTS_FORBIDDEN = re.compile(r"^\s*(disallow|sitemap)\s*:", re.IGNORECASE)


class SetupError(Exception):
    pass


@dataclass(frozen=True)
class Finding:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


@dataclass(frozen=True)
class Rules:
    avisos: dict[str, str]
    ai_notice_paths: list[str] = field(default_factory=list)
    script_allowed_paths: list[str] = field(default_factory=list)


def load_rules(config_dir: Path = CONFIG_DIR) -> Rules:
    try:
        avisos = json.loads((config_dir / "avisos.json").read_text(encoding="utf-8"))
        paths = json.loads((config_dir / "site-check.json").read_text(encoding="utf-8"))
        rules = Rules(
            avisos={"publico": avisos["publico"], "curadoriaIA": avisos["curadoriaIA"]},
            ai_notice_paths=list(paths["aiNoticePaths"]),
            script_allowed_paths=list(paths["scriptAllowedPaths"]),
        )
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SetupError(f"cannot read the site-check config: {exc}") from exc
    if not all(isinstance(v, str) and v.strip() for v in rules.avisos.values()):
        raise SetupError("a notice in avisos.json is empty")
    return rules


def normalize(text: str) -> str:
    return SPACES.sub(" ", text).strip()


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.robots: list[str] = []
        self.scripts = 0
        self.sitemap_link = False
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "script":
            self.scripts += 1
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "meta" and a.get("name", "").strip().lower() == "robots":
            self.robots.append(a.get("content", ""))
        if tag == "link" and "sitemap" in a.get("rel", "").lower().split():
            self.sitemap_link = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag in ("script", "style"):
            self._skip -= 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self.text.append(data)


def matches(rel: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(rel, p) for p in patterns)


def check_page(rel: str, source: str, rules: Rules) -> list[Finding]:
    parser = PageParser()
    parser.feed(source)
    parser.close()
    out: list[Finding] = []
    tokens = {t.strip().lower() for c in parser.robots for t in c.split(",")}
    if "noindex" not in tokens:
        out.append(Finding(rel, 'no <meta name="robots"> with noindex'))
    text = normalize(" ".join(parser.text))
    if normalize(rules.avisos["publico"]) not in text:
        out.append(Finding(rel, "audience notice missing"))
    if matches(rel, rules.ai_notice_paths) and normalize(rules.avisos["curadoriaIA"]) not in text:
        out.append(Finding(rel, "AI notice missing"))
    if parser.scripts and not matches(rel, rules.script_allowed_paths):
        out.append(Finding(rel, f"{parser.scripts} <script> element(s) outside the calculators"))
    if parser.sitemap_link:
        out.append(Finding(rel, 'has <link rel="sitemap">'))
    return out


def check_robots(dist: Path) -> list[Finding]:
    path = dist / "robots.txt"
    if not path.is_file():
        return [Finding("robots.txt", "missing")]
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = ROBOTS_FORBIDDEN.match(line.split("#", 1)[0])
        if m:
            word = "Disallow" if m.group(1).lower() == "disallow" else "Sitemap"
            out.append(Finding("robots.txt", f"line {n}: {word} line (ADR-002: no Disallow, no sitemap)"))
    return out


def parse_headers(text: str) -> dict[str, dict[str, list[str]]]:
    """Cloudflare `_headers`: an unindented URL pattern, then indented `Name: value` lines."""
    rules: dict[str, dict[str, list[str]]] = {}
    current: dict[str, list[str]] | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            current = rules.setdefault(line.strip(), {})
        elif current is not None and ":" in line:
            name, value = line.split(":", 1)
            current.setdefault(name.strip().lower(), []).append(value.strip())
    return rules


def csp_blocks_scripts(policy: str) -> bool:
    for directive in policy.split(";"):
        parts = directive.split()
        if parts and parts[0].lower() == "script-src":
            return [p.lower() for p in parts[1:]] == ["'none'"]
    return False


def check_headers(dist: Path) -> list[Finding]:
    path = dist / "_headers"
    root = parse_headers(path.read_text(encoding="utf-8")).get("/*", {}) if path.is_file() else {}
    out = []
    robots = {t.strip().lower() for v in root.get("x-robots-tag", []) for t in v.split(",")}
    if "noindex" not in robots:
        out.append(Finding("_headers", "no X-Robots-Tag with noindex on /*"))
    if not any(csp_blocks_scripts(v) for v in root.get("content-security-policy", [])):
        out.append(Finding("_headers", "no Content-Security-Policy with script-src 'none' on /*"))
    return out


def check(dist: Path, rules: Rules) -> list[Finding]:
    findings: list[Finding] = []
    pages = 0
    for path in sorted(p for p in dist.rglob("*") if p.is_file()):
        rel = path.relative_to(dist).as_posix()
        if SITEMAP_FILE.fullmatch(path.name):
            findings.append(Finding(rel, "sitemap file in the build"))
        if path.suffix.lower() == ".html":
            pages += 1
            findings.extend(check_page(rel, path.read_text(encoding="utf-8"), rules))
    if not pages:
        findings.append(Finding(".", "no HTML page in the build"))
    findings.extend(check_robots(dist))
    findings.extend(check_headers(dist))
    return findings


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: site_check.py <dist dir>", file=sys.stderr)
        return 2
    dist = Path(args[0])
    try:
        if not dist.is_dir():
            raise SetupError(f"{dist} is not a directory; run make build first")
        rules = load_rules()
    except SetupError as exc:
        print(f"site check: {exc}", file=sys.stderr)
        return 2
    findings = check(dist, rules)
    for f in findings:
        print(f"site check: {f}")
    if findings:
        print(f"site check: {len(findings)} findings")
        return 1
    print("site check: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
