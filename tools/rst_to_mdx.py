#!/usr/bin/env python3
"""
Convert a Sphinx RST file to MDX for Astro/Starlight.

Pipeline:
  1. pandoc -f rst -t gfm to get GitHub-flavored markdown
  2. Post-process: rewrite :ref: cross-refs, convert .. note:: directives to
     Starlight admonitions, strip toctrees, derive title from first H1.

Usage:
    python tools/rst_to_mdx.py --input docs/installation.rst --output src/content/docs/installation.mdx

Requires `pandoc` on PATH and Python 3.11+.
"""

from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# Cross-reference label → slug map. Extend as you discover labels.
# These come from `.. _label:` anchors in the source RST.
REF_TO_SLUG = {
    "agentic_primitive_contract": "/primitive-contract/",
    "agentic_categories": "/agentic-primitives/",
    "core_primitives_index": "/core-primitives/",
    "primitive_uniswapv2": "/primitive-uniswapv2/",
    "primitive_uniswapv3": "/primitive-uniswapv3/",
    "primitive_balancer": "/primitive-balancer/",
    "primitive_stableswap": "/primitive-stableswap/",
    "abstract_uniswap": "/abstract-uniswap/",
    "agentic_overview": "/agentic-overview/",
    "twin_concept": "/twin-concept/",
    "tool_schemas": "/agentic-tool-schemas/",
    "binding_to_claude": "/binding-to-claude/",
    "binding_to_other_llms": "/binding-to-other-llms/",
    "mcp_demo": "/mcp-demo/",
    "agentic_tools_reference": "/agentic-tools-reference/",
    "agentic_twin_reference": "/agentic-twin-reference/",
    "agentic_result_dataclasses": "/agentic-result-dataclasses/",
    "installation": "/installation/",
    "quick_start": "/quick/",
    "whats_new_v2": "/quick/whats-new-v2/",
    "roadmap": "/roadmap/",
}


def pandoc_to_gfm(rst_text: str) -> str:
    """Run pandoc to produce GitHub-flavored markdown."""
    proc = subprocess.run(
        ["pandoc", "-f", "rst", "-t", "gfm", "--wrap=preserve"],
        input=rst_text, capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        print(f"pandoc failed: {proc.stderr}", file=sys.stderr)
        sys.exit(1)
    return proc.stdout


# Pandoc emits Sphinx admonitions as fenced divs: `::: note\n...\n:::`.
# Starlight uses `:::note ... :::` with no space. Map: note -> note,
# warning -> caution, important -> tip.
_ADMONITION_DIV = re.compile(
    r"^:::\s*\{?\.?(\w+)\}?\s*\n(.*?)^:::\s*$",
    re.MULTILINE | re.DOTALL,
)
_STARLIGHT_KIND = {
    "note": "note",
    "warning": "caution",
    "important": "tip",
    "danger": "danger",
    "tip": "tip",
}


def fix_admonitions(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        kind = _STARLIGHT_KIND.get(m.group(1).lower(), "note")
        body = m.group(2).rstrip()
        return f":::{kind}\n{body}\n:::"
    return _ADMONITION_DIV.sub(repl, text)


# Pandoc keeps Sphinx :ref: as inline code: `:ref:\`label\``.
_REF_PATTERN = re.compile(r":ref:`([^`]+)`")


def rewrite_refs(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        label = m.group(1)
        slug = REF_TO_SLUG.get(label)
        if slug:
            # Best-effort link-text from the slug.
            return f"[{label}]({slug})"
        # Unknown ref — leave a visible TODO so the converter doesn't silently swallow it.
        return f"<!-- TODO: ref `{label}` not in REF_TO_SLUG -->`{label}`"
    return _REF_PATTERN.sub(repl, text)


# Strip ::: toctree containers, .. _label: anchors, .. _module-level metadata.
_TOCTREE = re.compile(r"^:::\s*toctree\b.*?^:::\s*$", re.MULTILINE | re.DOTALL)
_LABEL_ANCHOR = re.compile(r"^\.\.\s+_[\w-]+:\s*$", re.MULTILINE)


def strip_sphinx_only(text: str) -> str:
    text = _TOCTREE.sub("", text)
    text = _LABEL_ANCHOR.sub("", text)
    return text


# Pandoc renders RST hash-banners (`####\n title \n####`) as `# title`.
# Already correct, no fix needed.

def extract_title_and_strip(text: str) -> tuple[str | None, str]:
    """Pull the first H1, return (title, body_with_h1_stripped)."""
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if not m:
        return None, text
    title = m.group(1).strip()
    body = text[: m.start()] + text[m.end():]
    body = body.lstrip("\n")
    return title, body


def derive_description(body: str) -> str | None:
    """First paragraph of the body, stripped of markdown formatting, ≤ 160 chars."""
    for para in body.split("\n\n"):
        para = para.strip()
        if not para or para.startswith("#") or para.startswith(":::"):
            continue
        # Strip light formatting
        para = re.sub(r"\*\*([^*]+)\*\*", r"\1", para)
        para = re.sub(r"\*([^*]+)\*", r"\1", para)
        para = re.sub(r"`([^`]+)`", r"\1", para)
        para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
        para = re.sub(r"\s+", " ", para)
        if len(para) > 160:
            para = para[:157].rsplit(" ", 1)[0] + "…"
        return para
    return None


def convert(rst_text: str, fallback_title: str) -> str:
    md = pandoc_to_gfm(rst_text)
    md = strip_sphinx_only(md)
    md = rewrite_refs(md)
    md = fix_admonitions(md)
    title, body = extract_title_and_strip(md)
    title = title or fallback_title
    description = derive_description(body)

    fm = ["---", f"title: {json.dumps(title, ensure_ascii=False)}"]
    if description:
        fm.append(f"description: {json.dumps(description, ensure_ascii=False)}")
    fm.append("---")
    return "\n".join(fm) + "\n\n" + body.strip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Convert RST to MDX for Astro/Starlight")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--title", default=None)
    args = p.parse_args()

    in_path = Path(args.input)
    rst = in_path.read_text(encoding="utf-8")
    fallback = args.title or in_path.stem.replace("_", " ").replace("-", " ").title()
    mdx = convert(rst, fallback)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(mdx, encoding="utf-8")
    print(f"Wrote {out_path} ({len(mdx)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
