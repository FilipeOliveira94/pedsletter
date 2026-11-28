"""Walk the built site and fail when a page breaks a §4 or §5 rule (F1-03).

Rules checked on `dist/` (AGENTS.md §4 and §5, ADR-002):

- every `.html` page has `<meta name="robots">` whose content includes
  `noindex`;
- every page carries the audience notice, and every page matched by
  `aiNoticePaths` also carries the AI notice (text after HTML parsing, with
  entities decoded and whitespace collapsed; text inside `<script>`,
  `<style>`, `<template>`, `<noscript>`, `<title>`, `<textarea>` or an element
  with `hidden` does not count);
- no page outside `scriptAllowedPaths` has a `<script>` element;
- no sitemap: no `sitemap*.xml`, `sitemap*.xml.gz` or `sitemap*.txt` file, no
  `<link rel="sitemap">`;
- `robots.txt` exists and has no `Disallow` and no `Sitemap` line;
- `_headers` has a `/*` rule with `X-Robots-Tag` including `noindex` and a
  `Content-Security-Policy` whose `script-src` is exactly `'none'` (and whose
  `script-src-elem` and `script-src-attr`, when present, are too); no rule
  detaches either header with `!`;
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
SITEMAP_FILE = re.compile(r"sitemap.*\.(xml|xml\.gz|txt)", re.IGNORECASE)
# Text inside these never reaches the reader, so a notice there does not count.
HIDDEN_TEXT = {"script", "style", "template", "noscript", "title", "textarea"}
# A robots meta inside these is not applied by the browser or the crawler.
INERT = {"template", "noscript"}
# Void elements never get an end tag, so they never open a hiding scope.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
CSP_SCRIPT_DIRECTIVES = {"script-src", "script-src-elem", "script-src-attr"}
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
        # Open elements that hide text or make a meta inert, innermost last.
        self._stack: list[tuple[str, bool, bool]] = []

    def _hidden(self) -> bool:
        return any(h for _, h, _ in self._stack)

    def _inert(self) -> bool:
        return any(i for _, _, i in self._stack)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "script":
            self.scripts += 1
        if tag == "meta" and a.get("name", "").strip().lower() == "robots" and not self._inert():
            self.robots.append(a.get("content", ""))
        if tag == "link" and "sitemap" in a.get("rel", "").lower().split():
            self.sitemap_link = True
        hidden = tag in HIDDEN_TEXT or "hidden" in a
        if (hidden or tag in INERT) and tag not in VOID:
            self._stack.append((tag, hidden, tag in INERT))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if not self._hidden():
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
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        m = ROBOTS_FORBIDDEN.match(line.split("#", 1)[0])
        if m:
            word = "Disallow" if m.group(1).lower() == "disallow" else "Sitemap"
            out.append(Finding("robots.txt", f"line {n}: {word} line (ADR-002: no Disallow, no sitemap)"))
    return out


def parse_headers(text: str) -> tuple[dict[str, dict[str, list[str]]], list[tuple[str, str]]]:
    """Cloudflare `_headers`: an unindented URL pattern, then indented `Name: value` lines.

    Returns the rules and the `! Name` detach lines as (pattern, lowercased name).
    """
    rules: dict[str, dict[str, list[str]]] = {}
    detached: list[tuple[str, str]] = []
    pattern = ""
    current: dict[str, list[str]] | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            pattern = line.strip()
            current = rules.setdefault(pattern, {})
        elif line.strip().startswith("!"):
            detached.append((pattern, line.strip()[1:].strip().lower()))
        elif current is not None and ":" in line:
            name, value = line.split(":", 1)
            current.setdefault(name.strip().lower(), []).append(value.strip())
    return rules, detached


def csp_blocks_scripts(policy: str) -> bool:
    """`script-src 'none'`, and no `script-src-elem` or `-attr` that loosens it."""
    sources = {}
    for directive in policy.split(";"):
        parts = directive.split()
        if parts and parts[0].lower() in CSP_SCRIPT_DIRECTIVES:
            sources.setdefault(parts[0].lower(), [p.lower() for p in parts[1:]])
    return sources.get("script-src") == ["'none'"] and all(v == ["'none'"] for v in sources.values())


def check_headers(dist: Path) -> list[Finding]:
    path = dist / "_headers"
    rules, detached = parse_headers(path.read_text(encoding="utf-8-sig")) if path.is_file() else ({}, [])
    root = rules.get("/*", {})
    out = [
        Finding("_headers", f"rule {pattern} detaches {name} with !")
        for pattern, name in detached
        if name in ("x-robots-tag", "content-security-policy")
    ]
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
