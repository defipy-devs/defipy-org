# defipy-org

The source for [**defipy.org**](https://defipy.org), the documentation and project site for [DeFiPy](https://github.com/defipy-devs/defipy) — the Python SDK for agentic DeFi.

This repo is the **site**, not the library. For the SDK itself, see [defipy-devs/defipy](https://github.com/defipy-devs/defipy). For the original Sphinx-based docs (still live at [defipy.readthedocs.io](https://defipy.readthedocs.io/en/latest/) during the migration), see [defipy-devs/defipy-docs](https://github.com/defipy-devs/defipy-docs).

Built with [Astro](https://astro.build) and [Starlight](https://starlight.astro.build). Deployed to Vercel.

---

## Quick start

```bash
git clone https://github.com/defipy-devs/defipy-org
cd defipy-org
npm install
npm run dev
```

Dev server runs at `http://localhost:4321` (or the next free port). Most edits hot-reload; changes to `astro.config.mjs` need a full restart (`Ctrl+C`, then `npm run dev` again).

## Commands

| Command           | What it does                                       |
| :---------------- | :------------------------------------------------- |
| `npm install`     | Install dependencies                               |
| `npm run dev`     | Local dev server with hot-reload                   |
| `npm run build`   | Production build to `./dist/`                      |
| `npm run preview` | Serve the production build locally for inspection  |

Always run `npm run build` before pushing — the production build is stricter than dev mode and catches MDX issues that Vite tolerates.

## Repo layout

```
defipy-org/
├── astro.config.mjs       Sidebar, integrations, Starlight config
├── public/                Static assets (favicons, /img/)
├── src/
│   ├── assets/            Logo, hero images (imported by components)
│   ├── content/docs/      All page content (MDX)
│   │   ├── index.mdx      Home page
│   │   ├── api/           Class-reference pages
│   │   ├── tutorials/     Notebook-derived walkthroughs
│   │   ├── math/          Hand-derived AMM math
│   │   ├── ecosystem/     Book, courses, hackathons, presentations
│   │   └── ...            Concepts, getting-started, etc.
│   └── styles/custom.css  Wine palette, header band, notebook-output styling
├── tools/
│   ├── nb_to_mdx.py       Jupyter notebook → MDX converter
│   ├── rst_to_mdx.py      Sphinx RST → MDX converter (uses pandoc)
│   └── port_all.sh        Batch driver for both
└── CLAUDE_CODE_SPEC.md    Spec used during the initial bulk port from RTD
```

## Authoring

Pages are MDX under `src/content/docs/`. Frontmatter sets the page title and meta description; the body is normal Markdown plus optional Starlight components (`<Card>`, `<CardGrid>`, `<Tabs>`, etc.).

### Sidebar

Sidebar structure lives in `astro.config.mjs`. Adding a page generally means:

1.  Create the MDX file under the right subdirectory of `src/content/docs/`.
2.  Add an entry to the matching sidebar group in `astro.config.mjs`. (Some groups use `autogenerate` and pick up new files automatically — check the existing config before adding manual entries.)
3.  Restart the dev server.

### Math

KaTeX is wired via `remark-math` + `rehype-katex`. Inline math: `$x = 1$`. Display math: `$$ ... $$`. The blockquote-LaTeX style from Sphinx (`> $...$`) is **not** supported — use `$$...$$` instead.

### Code outputs in notebook pages

When a notebook cell's output contains characters MDX would otherwise interpret (curly braces in dict reprs, angle brackets, etc.), wrap the output in the JSX template-literal pattern:

```mdx
<div class="nb-output">{`Exchange ETH-DAI (LP)
Reserves: ETH = 1000.0, DAI = 100000.0`}</div>
```

`tools/nb_to_mdx.py` produces this shape automatically. If you're hand-writing notebook output, follow the same pattern.

## Conversion tooling

The site was bulk-ported from the Sphinx source. The two converter scripts under `tools/` exist for re-runs and incremental ports:

- **`tools/nb_to_mdx.py`** — `.ipynb` → `.mdx`. Uses `nbformat`. Handles markdown cells, code fences, stream/execute_result outputs (text, images, tracebacks), frontmatter derivation from the first H1 + paragraph.
- **`tools/rst_to_mdx.py`** — `.rst` → `.mdx`. Shells out to `pandoc -f rst -t gfm`, then post-processes: `:ref:` cross-refs via `REF_TO_SLUG`, Sphinx admonitions → Starlight directives, toctree stripping.
- **`tools/port_all.sh`** — batch driver running both converters over the file map from the original port.

Re-running individual files:

```bash
# Notebook
python tools/nb_to_mdx.py \
  --input  ../defipy-docs/docs/math/univ2_math.ipynb \
  --output src/content/docs/math/univ2-math.mdx

# RST (requires pandoc on PATH)
python tools/rst_to_mdx.py \
  --input  ../defipy-docs/docs/installation.rst \
  --output src/content/docs/installation.mdx
```

`CLAUDE_CODE_SPEC.md` documents the original bulk port — the file mapping, the MDX gotchas, and the workflow used. Useful context if you're picking up where that work left off.

## Theming

Wine palette comes from `src/styles/custom.css`. Two variables drive the palette in light vs. dark mode:

- `--sl-color-accent` — link color, sidebar highlight
- `--sl-color-bg-nav` — header band background

The header band is sized via `--sl-nav-height` so the logo (`src/assets/defipy_logo.png`, configured as `replacesTitle: true` in `astro.config.mjs`) sits cleanly with even padding above and below.

## Deploy

Production is deployed to Vercel from `main`. The `vercel.json` file (when added) handles the 301 redirects from RTD URLs:

- `defipy.readthedocs.io/en/latest/<path>.html` → `defipy.org/<slug>/`

The `_` to `-` slug transformation matters here — RTD's `binding_to_claude.html` becomes defipy.org's `binding-to-claude/`.

## Migration status

The site is content-complete relative to the RTD source. ReadTheDocs remains live indefinitely as a redirect target so accumulated SEO equity isn't lost. See the home page's "Looking for the older docs?" line and the upper-right header link for visitor-facing wayfinding during the transition.

Per-class API pages for the 21 agentic primitives and the four protocols are in progress — the current Primitive API → Agentic and Protocol API sections ship as overview pages plus a "details coming" note. The plan is to autogenerate those from numpydoc-style docstrings in the live SDK rather than hand-writing them.

## License

The site content is published under the same Apache 2.0 license as DeFiPy. See [defipy/LICENSE](https://github.com/defipy-devs/defipy/blob/main/LICENSE) for the full terms.

Built with [Astro](https://astro.build) + [Starlight](https://starlight.astro.build). [![Built with Starlight](https://astro.badg.es/v2/built-with-starlight/tiny.svg)](https://starlight.astro.build)
