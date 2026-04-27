#!/usr/bin/env python3
"""
Convert a Jupyter notebook to MDX for Astro/Starlight.

Usage:
    python tools/nb_to_mdx.py --input path/to/file.ipynb --output path/to/file.mdx

Notes for whoever extends this:
  - Markdown cells pass through verbatim (markdown is a subset of MDX).
  - Code cells become ```python fenced blocks; outputs follow as styled
    <div class="nb-output">{`...`}</div> blocks. The `{`...`}` wrapper
    makes MDX treat the whole text as a JSX string literal, which sidesteps
    the curly-brace and angle-bracket problems entirely.
  - The first H1 in the first markdown cell becomes the frontmatter `title`
    (and is then stripped from the body so the page doesn't render it twice).
    The first paragraph after that H1 becomes the `description` (~160 chars).
  - Backticks inside outputs are escaped to \\` so they don't close the JSX
    template-literal wrapper.

Tested on Python 3.11+. Requires `nbformat` (`pip install nbformat`).
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import nbformat
except ImportError:
    print("ERROR: install nbformat first: pip install nbformat", file=sys.stderr)
    sys.exit(1)


# -- helpers --------------------------------------------------------------

def cell_source(cell: dict[str, Any]) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return src


def output_text(output: dict[str, Any]) -> str:
    """Pull text from a single output cell (handles list-of-strings format)."""
    text = output.get("text", "")
    if isinstance(text, list):
        text = "".join(text)
    if text:
        return text

    data = output.get("data", {})
    if "text/plain" in data:
        plain = data["text/plain"]
        if isinstance(plain, list):
            plain = "".join(plain)
        return plain
    return ""


def output_image_png(output: dict[str, Any]) -> str | None:
    """Return base64 PNG payload from display_data / execute_result, if present."""
    data = output.get("data", {})
    png = data.get("image/png")
    if png:
        if isinstance(png, list):
            png = "".join(png)
        return png.strip()
    return None


def escape_for_jsx_template_literal(text: str) -> str:
    """Escape characters that would break a JSX `template-literal` wrapper.

    Inside `{`...`}`, the only characters that close the literal are backticks
    and `${`. We escape backticks. Curly braces and angle brackets are safe.
    """
    return text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


# -- title / description derivation --------------------------------------

_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_md_formatting(text: str) -> str:
    out = _LINK.sub(r"\1", text)
    out = _BOLD.sub(r"\1", out)
    out = _ITALIC.sub(r"\1", out)
    out = _CODE.sub(r"\1", out)
    return out


def derive_title_and_description(nb: dict[str, Any], fallback: str) -> tuple[str, str | None]:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell_source(cell).strip()
        if not src:
            continue
        lines = src.split("\n")
        title = None
        for line in lines:
            m = re.match(r"^#\s+(.+)$", line.strip())
            if m:
                title = m.group(1).strip()
                break
        if not title:
            break
        # First non-blank, non-heading, non-bullet line after the title is desc.
        desc_lines: list[str] = []
        in_desc = False
        for line in lines:
            if not in_desc and re.match(r"^#\s+", line):
                in_desc = True
                continue
            if in_desc:
                s = line.strip()
                if s and not s.startswith("#") and not s.startswith(("*", "-", "1.")):
                    desc_lines.append(s)
                elif desc_lines:
                    break
        if desc_lines:
            desc = strip_md_formatting(" ".join(desc_lines))
            if len(desc) > 160:
                desc = desc[:157].rsplit(" ", 1)[0] + "…"
            return title, desc
        return title, None
    return fallback, None


def strip_first_h1(nb: dict[str, Any]) -> dict[str, Any]:
    cells = nb.get("cells", [])
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell_source(cell)
        new_lines: list[str] = []
        h1_seen = False
        for line in src.split("\n"):
            if not h1_seen and re.match(r"^#\s+", line):
                h1_seen = True
                continue
            new_lines.append(line)
        if h1_seen:
            cells[i] = {**cell, "source": "\n".join(new_lines).lstrip("\n")}
        return {**nb, "cells": cells}
    return nb


# -- link rewrites for cross-references ----------------------------------

_LINK_REWRITES = [
    # [text](category_xxx.ipynb) -> /agentic-primitives/category-xxx/
    (re.compile(r"\]\(category_([a-z_]+)\.ipynb\)"),
     lambda m: "](/agentic-primitives/" + m.group(1).replace("_", "-") + "/)"),
    # [text](some_page.html) -> /some-page/
    (re.compile(r"\]\(([a-z][a-z0-9_]*)\.html\)"),
     lambda m: "](/" + m.group(1).replace("_", "-") + "/)"),
    # Sibling notebook ref: [text](some_page.ipynb) -> /some-page/
    (re.compile(r"\]\(([a-z][a-z0-9_]*)\.ipynb\)"),
     lambda m: "](/" + m.group(1).replace("_", "-") + "/)"),
]


def rewrite_links(text: str) -> str:
    out = text
    for pat, repl in _LINK_REWRITES:
        out = pat.sub(repl, out)
    return out


# -- LaTeX blockquote normalization --------------------------------------
#
# The univ2_math notebook (and similar) uses Sphinx's mathjax blockquote
# convention: lines beginning with `> $...$` for display math. Astro+KaTeX
# wants `$$...$$` for display math. Convert.

_BLOCKQUOTE_DISPLAY_MATH = re.compile(r"^>\s*\$([^$\n]+)\$\s*$", re.MULTILINE)


def normalize_blockquote_math(text: str) -> str:
    return _BLOCKQUOTE_DISPLAY_MATH.sub(r"$$\1$$", text)


# Notebook markdown sometimes uses raw LaTeX environments
# (`\begin{equation} ... \end{equation}`, also `align`, `aligned`, `gather`).
# MDX parses the leading backslash as JSX, so wrap in $$ ... $$ for KaTeX.
_LATEX_ENV = re.compile(
    r"\\begin\{(equation\*?|align\*?|aligned|gather\*?|gathered|cases|matrix|pmatrix|bmatrix)\}"
    r"(.*?)"
    r"\\end\{\1\}",
    re.DOTALL,
)


def normalize_latex_envs(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        env = m.group(1)
        body = m.group(2).strip()
        # `equation*` / `equation` / `align` etc. — keep the env *inside* the
        # display block so KaTeX rendering matches the original.
        return f"$$\n\\begin{{{env}}}\n{body}\n\\end{{{env}}}\n$$"
    return _LATEX_ENV.sub(repl, text)


# -- cell rendering ------------------------------------------------------

def render_cell(cell: dict[str, Any]) -> str:
    ctype = cell.get("cell_type")
    if ctype == "markdown":
        src = cell_source(cell)
        src = rewrite_links(src)
        src = normalize_blockquote_math(src)
        src = normalize_latex_envs(src)
        return src.rstrip() + "\n"

    if ctype == "code":
        src = cell_source(cell).rstrip()
        if not src:
            return ""
        parts = ["```python", src, "```"]
        rendered: list[str] = []
        for o in cell.get("outputs", []):
            otype = o.get("output_type")
            if otype in ("stream", "execute_result", "display_data"):
                png = output_image_png(o)
                if png:
                    rendered.append(
                        '<div class="nb-output-image">\n'
                        f'  <img alt="output" src="data:image/png;base64,{png}" />\n'
                        '</div>'
                    )
                    continue
                txt = output_text(o)
                if txt.strip():
                    safe = escape_for_jsx_template_literal(txt.rstrip())
                    rendered.append('<div class="nb-output">{`' + safe + '`}</div>')
            elif otype == "error":
                tb = o.get("traceback", [])
                tb_text = "\n".join(tb) if isinstance(tb, list) else str(tb)
                # Strip ANSI escapes
                tb_text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", tb_text)
                safe = escape_for_jsx_template_literal(tb_text.rstrip())
                rendered.append('<div class="nb-output nb-error">{`' + safe + '`}</div>')
        body = "\n".join(parts)
        if rendered:
            body += "\n\n" + "\n\n".join(rendered)
        return body + "\n"

    return ""  # raw cells etc — skip


# -- main ----------------------------------------------------------------

def convert(nb: dict[str, Any], fallback_title: str) -> str:
    title, description = derive_title_and_description(nb, fallback_title)
    nb = strip_first_h1(nb)

    fm = ["---", f"title: {json.dumps(title, ensure_ascii=False)}"]
    if description:
        fm.append(f"description: {json.dumps(description, ensure_ascii=False)}")
    fm.append("---")
    fm_text = "\n".join(fm) + "\n\n"

    body_parts = []
    for cell in nb.get("cells", []):
        rendered = render_cell(cell)
        if rendered.strip():
            body_parts.append(rendered)
    return fm_text + "\n".join(body_parts)


def main() -> int:
    p = argparse.ArgumentParser(description="Convert .ipynb to MDX for Astro/Starlight")
    p.add_argument("--input", required=True, help="Path to input .ipynb")
    p.add_argument("--output", required=True, help="Path to output .mdx")
    p.add_argument("--title", default=None, help="Fallback title if no H1 in notebook")
    args = p.parse_args()

    in_path = Path(args.input)
    nb = nbformat.read(in_path, as_version=4)
    fallback = args.title or in_path.stem.replace("_", " ").replace("-", " ").title()
    mdx = convert(nb, fallback)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(mdx, encoding="utf-8")
    print(f"Wrote {out_path} ({len(mdx)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
