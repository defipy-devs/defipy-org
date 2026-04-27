# defipy.org — Claude Code Spec

**Goal:** Finish porting [defipy-docs](https://github.com/defipy-devs/defipy-docs) (a Sphinx + ReadTheDocs site) to defipy.org (Astro + Starlight) so we can deploy to Vercel and migrate SEO off RTD.

The skeleton, sidebar, build pipeline, and 9 of ~36 pages are already done. Your job is the remaining bulk content port. **Run this end-to-end locally, on a working branch, with frequent build checks and commits.**

## Repos

- **Source (Sphinx, RST + ipynb):** `/Users/ian_moore/repos/defipy-docs`
  - Site root: `docs/`
  - `index.rst` defines the canonical IA via toctrees
  - All Jupyter notebooks under `docs/` are populated with executed cells
- **Target (Astro + Starlight, MDX):** `/Users/ian_moore/repos/defipy-org`
  - Source: `src/content/docs/`
  - Sidebar: `astro.config.mjs` — already wired to the slug structure below
  - KaTeX is wired (`remark-math` + `rehype-katex`); `katex.min.css` is in `customCss`
  - Wine palette CSS variable: `--sl-color-accent: #673147`
  - Custom output styling: `.nb-output`, `.nb-output-image` in `src/styles/custom.css`
  - Pagefind search auto-builds at build time

## What's already done (skip these)

```
src/content/docs/
├── index.mdx                                    ✅ landing page
├── agentic-overview.mdx                         ✅
├── agentic-primitives.mdx                       ✅ overview + availability table
├── agentic-primitives/
│   ├── position-analysis.mdx                    ✅
│   ├── price-scenarios.mdx                      ✅
│   ├── pool-health.mdx                          ✅
│   ├── risk.mdx                                 ✅
│   ├── optimization.mdx                         ✅
│   ├── comparison.mdx                           ✅
│   ├── execution.mdx                            ✅
│   ├── portfolio.mdx                            ✅
│   └── break-even.mdx                           ✅
└── math/
    └── balancer-math.mdx                        ✅ (POC, may need re-port from RST)
```

These were converted from `defipy-docs/docs/agentic_primitives/notebooks/*.ipynb`. Use them as reference for the expected MDX output style.

## What's remaining

### 1. Notebook → MDX (~25 files)

| Source | Target |
|---|---|
| `docs/math/univ2_math.ipynb` | `src/content/docs/math/univ2-math.mdx` |
| `docs/math/univ3_math.ipynb` | `src/content/docs/math/univ3-math.mdx` |
| `docs/uniswapv2/tutorials/uniswap_v2.ipynb` | `src/content/docs/tutorials/uniswapv2/uniswap-v2.mdx` |
| `docs/uniswapv2/tutorials/imp_loss_v2.ipynb` | `src/content/docs/tutorials/uniswapv2/imp-loss-v2.mdx` |
| `docs/uniswapv2/tutorials/swap_deposit.ipynb` | `src/content/docs/tutorials/uniswapv2/swap-deposit.mdx` |
| `docs/uniswapv2/tutorials/withdraw_swap.ipynb` | `src/content/docs/tutorials/uniswapv2/withdraw-swap.mdx` |
| `docs/uniswapv2/tutorials/indexing_problem.ipynb` | `src/content/docs/tutorials/uniswapv2/indexing-problem.mdx` |
| `docs/uniswapv2/tutorials/machine_precision.ipynb` | `src/content/docs/tutorials/uniswapv2/machine-precision.mdx` |
| `docs/uniswapv2/tutorials/uniswap_simulation.ipynb` | `src/content/docs/tutorials/uniswapv2/uniswap-simulation.mdx` |
| `docs/uniswapv3/tutorials/uniswap_v3.ipynb` | `src/content/docs/tutorials/uniswapv3/uniswap-v3.mdx` |
| `docs/uniswapv3/tutorials/imp_loss_v3.ipynb` | `src/content/docs/tutorials/uniswapv3/imp-loss-v3.mdx` |
| `docs/uniswapv3/tutorials/order_book.ipynb` | `src/content/docs/tutorials/uniswapv3/order-book.mdx` |
| `docs/uniswapv3/tutorials/machine_precision.ipynb` | `src/content/docs/tutorials/uniswapv3/machine-precision.mdx` |
| `docs/balancer/tutorials/abstract_balancer_test.ipynb` | `src/content/docs/tutorials/balancer/abstract-balancer-test.mdx` |
| `docs/balancer/tutorials/primitive_balancer_test.ipynb` | `src/content/docs/tutorials/balancer/primitive-balancer-test.mdx` |
| `docs/stableswap/tutorials/abstract_stableswap_test.ipynb` | `src/content/docs/tutorials/stableswap/abstract-stableswap-test.mdx` |
| `docs/stableswap/tutorials/primitive_stableswap_test.ipynb` | `src/content/docs/tutorials/stableswap/primitive-stableswap-test.mdx` |

**Skip** the legacy flat `docs/notebooks/*.ipynb` and `docs/tutorials/*.ipynb` directories — those are duplicates of the protocol-specific subdirs above (the canonical source is whatever `docs/index.rst` references via toctree).

### 2. RST → MDX (~25 files)

The mapping below follows the slug structure already in `astro.config.mjs`. Use kebab-case slugs.

| Source RST | Target MDX |
|---|---|
| `docs/ecosystem/book.rst` | `src/content/docs/ecosystem/book.mdx` |
| `docs/ecosystem/courses.rst` | `src/content/docs/ecosystem/courses.mdx` |
| `docs/ecosystem/hackathons.rst` | `src/content/docs/ecosystem/hackathons.mdx` |
| `docs/ecosystem/presentations.rst` | `src/content/docs/ecosystem/presentations.mdx` |
| `docs/quick/index.rst` | `src/content/docs/quick.mdx` |
| `docs/quick/whats_new_v2.rst` | `src/content/docs/quick/whats-new-v2.mdx` |
| `docs/installation.rst` | `src/content/docs/installation.mdx` |
| `docs/legal.rst` | `src/content/docs/legal.mdx` |
| `docs/core_primitives/index.rst` | `src/content/docs/core-primitives.mdx` |
| `docs/agentic_primitives/primitive_contract.rst` (if present, else find under `agentic_primitives/` or `_static/`) | `src/content/docs/primitive-contract.mdx` |
| `docs/agentic/index.rst` | (already covered by `agentic-overview.mdx` — diff and merge any extra content) |
| `docs/agentic/tool_schemas.rst` | `src/content/docs/agentic-tool-schemas.mdx` |
| `docs/agentic/binding_to_claude.rst` | `src/content/docs/binding-to-claude.mdx` |
| `docs/agentic/binding_to_other_llms.rst` | `src/content/docs/binding-to-other-llms.mdx` |
| `docs/agentic/mcp_demo.rst` | `src/content/docs/mcp-demo.mdx` |
| `docs/agentic_primitives/agentic_tools_reference.rst` (or similar) | `src/content/docs/agentic-tools-reference.mdx` |
| `docs/agentic_primitives/agentic_twin_reference.rst` | `src/content/docs/agentic-twin-reference.mdx` |
| `docs/agentic_primitives/agentic_result_dataclasses.rst` | `src/content/docs/agentic-result-dataclasses.mdx` |
| `docs/twin_concept.rst` (or under `agentic/`) | `src/content/docs/twin-concept.mdx` |
| `docs/abstract_uniswap.rst` | `src/content/docs/abstract-uniswap.mdx` |
| `docs/primitive_uniswapv2.rst` | `src/content/docs/primitive-uniswapv2.mdx` |
| `docs/primitive_uniswapv3.rst` | `src/content/docs/primitive-uniswapv3.mdx` |
| `docs/primitive_balancer.rst` | `src/content/docs/primitive-balancer.mdx` |
| `docs/primitive_stableswap.rst` | `src/content/docs/primitive-stableswap.mdx` |
| `docs/roadmap.rst` | `src/content/docs/roadmap.mdx` |
| `docs/math/balancer_math.rst` | `src/content/docs/math/balancer-math.mdx` (re-port; the existing file is a stub) |
| `docs/math/stableswap_math.rst` | `src/content/docs/math/stableswap-math.mdx` |

If a file in the table doesn't exist at the listed path, search the source tree (`grep -r "<filename>" docs/`) — the toctrees in `index.rst` and section index files will tell you the real location. Don't invent content; if a target has no source, leave a one-line stub MDX page (`title:` + a "coming soon" line) and note it in your final summary.

### 3. Quality gate (must pass before each commit)

```bash
cd /Users/ian_moore/repos/defipy-org
npm install               # only on first run
npm run build             # Astro must build clean — no errors
```

The build will fail if:
- MDX has unescaped `{` `}` outside a code fence
- A sidebar slug references a missing page
- A markdown link is malformed

Fix every error before committing.

## Conversion strategy

**Use `jupyter nbconvert` + a post-processor, not hand-porting.** A scaffold script lives at `tools/nb_to_mdx.py`. Either use it as-is or extend it. Pseudocode:

```python
# For each notebook:
#   nb = nbformat.read(path)
#   for cell in nb.cells:
#     if markdown:  emit cell.source verbatim
#     if code:      emit ```python ... ``` fence; then for each output:
#       - stream/execute_result: <div class="nb-output">{`...`}</div>
#       - display_data with image/png: <div class="nb-output-image"><img src="data:image/png;base64,..."/></div>
#       - error: <div class="nb-output nb-error">{`...`}</div>
#   Strip the first H1 from the body (it becomes frontmatter `title`)
#   Derive `description` from the first non-heading paragraph after the H1
#   Wrap with frontmatter:
#     ---
#     title: "..."
#     description: "..."
#     ---
```

Then drive it over the whole tree with a shell loop:

```bash
mkdir -p src/content/docs/tutorials/{uniswapv2,uniswapv3,balancer,stableswap}
mkdir -p src/content/docs/math src/content/docs/ecosystem src/content/docs/quick

# Notebooks
python tools/nb_to_mdx.py \
  --input ../defipy-docs/docs/math/univ2_math.ipynb \
  --output src/content/docs/math/univ2-math.mdx
# ... etc per row in the table
```

For RST → MDX, use `pandoc -f rst -t gfm` (GitHub-flavored markdown is a clean subset of MDX) and post-process to:
- Replace `:ref:`label`` with the proper internal link (translate to `/slug/`)
- Replace Sphinx `.. note::` / `.. warning::` admonitions with Starlight `:::note` / `:::caution` directives
- Strip Sphinx-only directives (`.. toctree::`, `.. _label:`)
- Add the YAML frontmatter

A second helper `tools/rst_to_mdx.sh` is a fine place for that.

## MDX gotchas to bake into the converter

These are real bugs you'll hit. Handle them in the script so we don't whack-a-mole:

1. **Curly braces in output text** (e.g. dict/JSON repr): wrap the whole output block in `{`...`}` JSX so MDX treats it as a literal string. Pattern: `<div class="nb-output">{\`...\`}</div>`. Backticks inside the output need to be escaped as `\``.
2. **`<` and `>` in raw text**: same fix — they're inside the JSX-string wrapper, so they don't need HTML-escaping individually.
3. **`>` blockquote-LaTeX style** (used in `univ2_math.ipynb`): Sphinx renders `> $xy = L^2$` as a blockquoted equation. Convert to standalone `$$xy = L^2$$` for KaTeX display math. Inline `$...$` is fine as-is.
4. **`:ref:` cross-references** in RST: rewrite to absolute slug links. Map: `:ref:`agentic_primitive_contract`` → `[The Primitive Contract](/primitive-contract/)`. Build the map by reading `.. _label:` anchors throughout the source tree.
5. **Sphinx `.. list-table::`**: convert to GFM pipe tables. The availability table in `agentic-primitives.mdx` is the reference.
6. **Image references in RST** (`.. image:: foo.png`): copy the image into `src/assets/` and rewrite as standard markdown image syntax.
7. **Description truncation**: the auto-derived description should strip markdown formatting (`**bold**`, `*italic*`, `` `code` ``, `[text](url)`) and cap at ~160 characters.

## Workflow per chunk

1. Read 2–3 source files, build the matching MDX(s) via the converter
2. `npm run build` — fix errors
3. Spot-check rendered HTML: `grep -E '<h[12]|nb-output|katex' dist/<slug>/index.html`
4. Commit: `git add -A && git commit -m "port: <section>"`
5. Move to next chunk

Don't try to convert all 25+ files in one shot. Group them: math, then v2 tutorials, then v3 tutorials, then balancer + stableswap, then RST narrative, then RST API reference.

## When you finish

1. `npm run build` clean
2. `git push` (don't merge to main yet — leave branch open for review)
3. Reply with:
   - List of pages that needed stubs (no source found)
   - Anything in `astro.config.mjs` sidebar that points to a missing page (so we can fix the sidebar or fill the stub)
   - The total page count and approximate build time
4. Suggest the SEO migration next: 301 map from RTD URLs (`defipy.readthedocs.io/en/latest/<path>.html`) to defipy.org slugs

## Out of scope

- The home page splash design — leave `index.mdx` alone unless build breaks
- The legacy flat `docs/notebooks/` and `docs/tutorials/` directories — those duplicate the protocol-specific subdirs
- API autodoc generation — the source uses hand-written RST API pages (no Sphinx autodoc), so just port them as static MDX
- Vercel deployment — that's a follow-up step the user will run
