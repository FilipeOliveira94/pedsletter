"""Fail when a block-list term or a blocked proper name appears (F1-06).

AGENTS.md §4: no professional's name, registration number, form of address or
review attribution anywhere in the repository, the built site or the PR text.

- The fixed terms live in `src/config/authorship.json`, each written with a
  JSON escape, so no file holds a term in plain text.
- The proper names come only from the environment variable that file names
  (a CI secret, or the shell for the pre-commit hook), one per line; `;` and
  `,` also separate them. A missing or empty variable is a setup error.
- Matching ignores case, accents and runs of whitespace, decodes HTML
  entities and percent-encoding, drops invisible characters, reads each line
  with its tags removed and with slug separators as spaces, and catches a
  phrase split across two lines (quote and list markers ignored). A match needs no letter (no digit, for a term that
  starts or ends with a digit) right before or after it.
- Output names the source, the line and the term's position in its list,
  never the term, the name or the line. A path that itself matches is printed
  as `<redacted path #k>`.

CLI (exit 0 clean, 1 findings, 2 setup error):

    python3 scripts/authorship_check.py --repo --html dist --text-env PR_BODY
    python3 scripts/authorship_check.py --staged      # pre-commit hook

API for the generation job (F2-13), before any push:

    rules = load_rules()                      # raises SetupError
    findings = scan_text(text, "label", rules)
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "src" / "config" / "authorship.json"
NAME_SEPARATOR = re.compile(r"[\n;,]")
TAG = re.compile(r"<[^>]*>")
SPACES = re.compile(r"\s+")
# Slug and path separators read as spaces. Not the dot: two terms end with one.
SEPARATORS = re.compile(r"[-_+/\\]+")
# Hashes blanked, so a term cannot hit by chance inside one: subresource
# integrity values (lockfile) and letter-digit runs of 24 or more with a digit
# (hex digests, hashed names). Slashes never join a run, so a URL path stays.
HASHLIKE = re.compile(
    r"\bsha(?:1|256|384|512)-[A-Za-z0-9+/]+={0,2}"
    r"|(?<![A-Za-z0-9])(?=[A-Za-z0-9]*\d)[A-Za-z0-9]{24,}(?![A-Za-z0-9])"
)
# Edge of a wrapped line: quote, heading and list markers, a hard-break slash.
LEAD = re.compile(r"^[^\w]+")
TRAIL = re.compile(r"[^\w.]+$")
NO_LETTER_BEFORE = r"(?<![^\W\d_])"
NO_LETTER_AFTER = r"(?![^\W\d_])"
NO_DIGIT_BEFORE = r"(?<!\d)"
NO_DIGIT_AFTER = r"(?!\d)"


class SetupError(Exception):
    """The check cannot run: missing config, missing names, missing input."""


@dataclass(frozen=True)
class Finding:
    label: str
    line: int
    kind: str  # "term" or "name"
    index: int  # 1-based position in its list

    def __str__(self) -> str:
        return f"{self.label}:{self.line}: {self.kind} #{self.index}"


@dataclass(frozen=True)
class Rules:
    terms: tuple[re.Pattern[str], ...]
    names: tuple[re.Pattern[str], ...]


def normalize(text: str) -> str:
    """Case-fold, drop accents and invisible characters, collapse whitespace.

    Dropped: every combining mark (accents, joiners, variation selectors),
    format characters (zero-width space, soft hyphen, BOM) and control
    characters other than whitespace.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    bare = "".join(
        c
        for c in decomposed
        if unicodedata.category(c) not in ("Mn", "Me", "Cf")
        and (unicodedata.category(c) != "Cc" or c.isspace())
    )
    return SPACES.sub(" ", bare.casefold())


def _edge(char: str, letter: str, digit: str) -> str:
    if char.isalpha():
        return letter
    if char.isdigit():
        return digit
    return ""


def compile_term(term: str) -> re.Pattern[str]:
    core = normalize(term).strip()
    if not core:
        raise SetupError("a block-list entry is empty after normalization")
    before = _edge(core[0], NO_LETTER_BEFORE, NO_DIGIT_BEFORE)
    after = _edge(core[-1], NO_LETTER_AFTER, NO_DIGIT_AFTER)
    return re.compile(before + re.escape(core) + after)


def load_rules(environ: Mapping[str, str] | None = None, config: Path = CONFIG) -> Rules:
    environ = os.environ if environ is None else environ
    try:
        data = json.loads(config.read_text(encoding="utf-8"))
        terms, variable = data["terms"], data["names_env"]
    except (OSError, ValueError, KeyError) as error:
        raise SetupError(f"cannot read {config.name}: {type(error).__name__}") from None
    raw = environ.get(variable)
    if raw is None:
        raise SetupError(f"{variable} is not set; it must list the names to block")
    names = [name.strip() for name in NAME_SEPARATOR.split(raw) if name.strip()]
    if not names:
        raise SetupError(f"{variable} is empty; it must list the names to block")
    return Rules(
        terms=tuple(compile_term(t) for t in terms),
        names=tuple(compile_term(n) for n in names),
    )


def _views(line: str) -> tuple[str, str, str]:
    """Three normalized readings of a line, entities decoded: as written (so
    attributes count), with tags removed, and that again with percent-encoding
    decoded and slug separators read as spaces."""
    line = HASHLIKE.sub(" ", line)
    untagged = html.unescape(TAG.sub(" ", line))
    slug = SEPARATORS.sub(" ", urllib.parse.unquote(untagged))
    return normalize(html.unescape(line)), normalize(untagged), normalize(slug)


def decode(raw: bytes) -> str | None:
    """Text of a file: UTF-16 with a BOM, UTF-8, else Windows-1252 (so a
    stray byte never hides a file). None for binary (a NUL byte)."""
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", "replace")
    if b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", "replace")


def _count(views: Iterable[str], rules: Rules) -> Counter[tuple[str, int]]:
    """Per (kind, index), the most matches any single view of the text has."""
    best: Counter[tuple[str, int]] = Counter()
    for view in views:
        for kind, patterns in (("term", rules.terms), ("name", rules.names)):
            for i, pattern in enumerate(patterns, 1):
                n = len(pattern.findall(view))
                if n > best[(kind, i)]:
                    best[(kind, i)] = n
    return best


def scan_text(text: str, label: str, rules: Rules) -> list[Finding]:
    lines = text.splitlines()
    views = [_views(line) for line in lines]
    counts = [_count(v, rules) for v in views]
    found: set[tuple[int, str, int]] = set()
    for n, count in enumerate(counts):
        found.update((n + 1, kind, i) for (kind, i), c in count.items() if c)
        if n + 1 < len(lines):
            # A phrase split across two lines: more matches in the joined pair
            # than in the two lines apart. Reported on the first line.
            joined = _count(
                (TRAIL.sub("", a) + " " + LEAD.sub("", b) for a, b in zip(views[n], views[n + 1])),
                rules,
            )
            for (kind, i), c in joined.items():
                if c > count[(kind, i)] + counts[n + 1][(kind, i)]:
                    found.add((n + 1, kind, i))
    return [Finding(label, line, kind, i) for line, kind, i in sorted(found)]


def _git(*args: str) -> bytes:
    return subprocess.run(["git", *args], capture_output=True, check=True).stdout


def _paths(output: bytes) -> list[str]:
    return [p.decode("utf-8", "surrogateescape") for p in output.split(b"\0") if p]


def _sources(args: argparse.Namespace, environ: Mapping[str, str]) -> Iterable[tuple[str, bytes | None, bool]]:
    """Yield (label, content, is_path); content None means a path to read."""
    if args.repo:
        for path in _paths(_git("ls-files", "-z")):
            yield path, None, True
    if args.staged:
        for path in _paths(_git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR")):
            yield path, _git("cat-file", "blob", f":{path}"), True
    for directory in args.html:
        root = Path(directory)
        if not root.is_dir():
            raise SetupError(f"{directory} is not a directory; run make build first")
        for file in sorted(p for p in root.rglob("*") if p.is_file()):
            yield file.as_posix(), None, True
    for variable in args.text_env:
        yield variable, environ.get(variable, "").encode("utf-8"), False


def _property(value: str) -> str:
    """Escape a GitHub workflow-command property value."""
    for char, code in (("%", "%25"), ("\r", "%0D"), ("\n", "%0A"), (":", "%3A"), (",", "%2C")):
        value = value.replace(char, code)
    return value


def _annotation(finding: Finding, files: set[str]) -> str:
    """A GitHub error annotation, placed on the file and line when there is one."""
    where = ""
    if finding.label in files and finding.line > 0:
        where = f"file={_property(finding.label)},line={finding.line},"
    return f"::error {where}title=authorship::{finding}"


def main(argv: list[str] | None = None, environ: Mapping[str, str] | None = None) -> int:
    environ = os.environ if environ is None else environ
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", action="store_true", help="every file git tracks")
    parser.add_argument("--staged", action="store_true", help="the staged version of each added or changed file")
    parser.add_argument("--html", action="append", default=[], metavar="DIR", help="every file under DIR (must exist)")
    parser.add_argument("--text-env", action="append", default=[], metavar="VAR", help="the text in an environment variable")
    args = parser.parse_args(argv)

    findings: list[Finding] = []
    scanned = skipped = 0
    redacted: dict[str, str] = {}
    files: set[str] = set()
    try:
        rules = load_rules(environ)
        for label, content, is_path in _sources(args, environ):
            if is_path:
                path_hits = scan_text(label, label, rules)
                if path_hits:
                    redacted.setdefault(label, f"<redacted path #{len(redacted) + 1}>")
                    findings += [Finding(redacted[label], 0, f.kind, f.index) for f in path_hits]
            raw = Path(label).read_bytes() if content is None else content
            text = decode(raw)
            if text is None:
                skipped += 1
                continue
            scanned += 1
            if is_path and label not in redacted:
                files.add(label)
            findings += scan_text(text, redacted.get(label, label), rules)
    except SetupError as error:
        print(f"authorship check: setup error: {error}", file=sys.stderr)
        return 2
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"authorship check: setup error: {type(error).__name__}", file=sys.stderr)
        return 2

    in_actions = environ.get("GITHUB_ACTIONS") == "true"
    for finding in findings:
        print(_annotation(finding, files) if in_actions else str(finding))
    summary = f"{scanned} sources scanned, {skipped} file{'s' if skipped != 1 else ''} skipped (binary)"
    if findings:
        print(f"authorship check: {len(findings)} findings; {summary}. Terms: src/config/authorship.json; names: the secret.")
        return 1
    print(f"authorship check: passed; {summary}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
