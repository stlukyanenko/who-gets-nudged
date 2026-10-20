"""Find and redact his email address (and any other email addresses) before publishing.

Why: Claude models run through `claude -p`, which puts his account email into their
context (docs/CLAUDE_P_CHECK.md). A model can repeat it in an answer or a log.

The address is never written in this repo. Pass it through an environment variable:
    REDACT_EMAIL="..." python src/redact_email.py            # report only
    REDACT_EMAIL="..." python src/redact_email.py --fix      # replace in place

Scans every text file under runs/, logs/, results/, report/, figures/ and src/data/,
plus README.md. Inspect `.eval` logs are zip archives: every member inside them is
scanned too, and with --fix the archive is rewritten with the redacted members.
Exits with code 1 if anything is found and --fix was not given, so a publish step can
call it as a gate.
"""

import os
import re
import sys
import zipfile
from pathlib import Path

try:  # Inspect writes .eval archives with zstd compression; this package teaches zipfile to read it
    import zipfile_zstd  # noqa: F401
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[1]
SCAN = ["runs", "logs", "results", "report", "figures", "src/data", "README.md"]
TEXT_SUFFIXES = {".json", ".jsonl", ".md", ".txt", ".csv", ".tsv", ".log", ".yaml", ".yml", ".html"}
ANY_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
MASK = "[REDACTED_EMAIL]"


def files():
    for name in SCAN:
        path = ROOT / name
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from (p for p in path.rglob("*")
                        if p.is_file() and (p.suffix in TEXT_SUFFIXES or p.suffix == ".eval"))


def scan_text(label, text, own_re):
    n_own = len(own_re.findall(text))
    others = sorted({m for m in ANY_EMAIL.findall(text) if not own_re.fullmatch(m)})
    if n_own or others:
        print(f"{label}: {n_own} x his email; other addresses: {others or 'none'}")
    return n_own + len(others)


def handle_eval_zip(path, own_re, fix):
    """Scan (and with fix, rewrite) every member of an Inspect .eval archive."""
    hits, members = 0, []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            data = zf.read(info)
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                members.append((info, data))
                continue
            hits += scan_text(f"{path.relative_to(ROOT)}::{info.filename}", text, own_re)
            members.append((info, own_re.sub(MASK, text).encode("utf-8") if fix else data))
    if fix and hits:
        tmp = path.with_suffix(".eval.tmp")
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
            for info, data in members:
                out.writestr(info, data)
        tmp.replace(path)
    return hits


def main():
    own = os.environ.get("REDACT_EMAIL", "").strip()
    if not own:
        sys.exit("set REDACT_EMAIL to his address first")
    own_re = re.compile(re.escape(own), re.I)
    fix = "--fix" in sys.argv
    hits = 0
    for path in files():
        if path.suffix == ".eval":
            hits += handle_eval_zip(path, own_re, fix)
            continue
        text = path.read_text(errors="ignore")
        found = scan_text(str(path.relative_to(ROOT)), text, own_re)
        hits += found
        if fix and found:
            path.write_text(own_re.sub(MASK, text))
    if hits and not fix:
        sys.exit(1)
    print("done" if fix else "clean")


if __name__ == "__main__":
    main()
