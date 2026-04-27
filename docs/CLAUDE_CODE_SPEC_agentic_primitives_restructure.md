# Claude Code Spec — Agentic Primitives Standalone Pages + Math Sections

**Status:** Spec — ready for execution
**Owner:** Claude Code session
**Estimated effort:** ~2 days end-to-end (21 primitive pages × 30-60 min each + 9 thin category overviews + integration + RTD verification)
**Predecessors:**
- `CLAUDE_CODE_SPEC_protocol_variants_batch.md` (Core Primitives — established the locked template that this spec mirrors)
- `CLAUDE_CODE_SPEC_agentic_primitives_completion.md` (**SUPERSEDED by this spec — do not execute**)
**Branch:** `docs/agentic-primitives-restructure` off whichever working branch follows the Core Primitives merge

---

## TL;DR

The Core Primitives batch produced standalone per-primitive pages with a
locked section structure (Hook → "When to use X vs Y" → Signature at a
glance → Common parameters → Protocol-specific parameters → How this
composes → See also). The Swap page is the canonical example — see
screenshot in conversation history.

This spec applies that **same structure** to Agentic Primitives, with one
addition: a **stratified math section** sitting between Common/Protocol-
specific parameters and the Example. Three depth levels, three section
titles, sized to each primitive's actual mathematical contribution:

- **Math** — paper depth (~2-4 paragraphs + `:math:` blocks) for primitives
  with original derivations (`AssessDepegRisk`, `OptimalDepositSplit`,
  `FindBreakEvenPrice`, `DetectFeeAnomaly`)
- **Mathematical contract** — formula + numeraire + V2/V3 dispatch
  (~1 paragraph + key equation) for primitives that compose over upstream
  IL classes (most position/scenario/comparison/portfolio primitives)
- **What this measures** — one paragraph for primitives that are
  structured reads of pool state (`CheckPoolHealth`,
  `CheckTickRangeStatus`, `DetectRugSignals`)

Differentiated titles signal honestly what kind of content the reader is
getting, instead of forcing every primitive into a uniform "Math" header
that would either pad state-readers or shrink original-derivation
primitives.

**Restructure scope:** 21 standalone primitive pages + 9 thin category-
overview pages. Existing notebook examples preserved verbatim where
possible — the substantive content already exists; this batch
restructures the scaffolding around it and adds math sections.

**Out of scope:** Core Primitives re-touches, IA changes beyond what the
restructure mandates, defipy.org Phase 2 work, the DeFi Math sidebar
section (cross-link only, don't rewrite).

---

## What changed vs the superseded spec

The previous Agentic Primitives Completion spec assumed:
- Category pages stay as primary unit, primitive sections inline
- Only 3 dispatcher primitives need protocol-variants treatment
- Other primitives are "already correct" because of sibling pattern

The new direction (per the rendered Swap page setting the bar):
- **Every primitive becomes a standalone page** — strict mirror of Core
- The sibling-vs-dispatcher distinction stays architecturally true but
  no longer affects page structure: each primitive's signature-at-a-
  glance table simply lists the protocols *that primitive* covers
  (one row for sibling primitives, four rows for dispatchers)
- **Every primitive gets a math/contract/measurement section** — not
  just dispatchers
- Category pages shrink to thin overviews + toctree

The previous spec's substantive content (Protocol coverage tables per
category, dispatcher inline blocks) is **subsumed** — same information
gets surfaced on the new per-primitive pages, plus the new math sections.

---

## Locked template (from Core Primitives batch + math addition)

Every primitive page follows this section order:

1. **Page title** = primitive name (e.g., `AnalyzePosition`)
2. **One-paragraph hook** — what the primitive answers, **read-only-not-
   mutating** pinned, link to The Primitive Contract page
3. **"When to use X vs Y" callout** — where there's a sibling/related
   distinction worth resolving up front (e.g., AnalyzePosition vs
   AnalyzeBalancerPosition; SimulatePriceMove vs FindBreakEvenPrice;
   CheckPoolHealth vs DetectRugSignals)
4. **Signature at a glance** — table with one-line `apply()` per
   supported protocol (single row for sibling primitives; multi-row for
   dispatchers). Match the Swap page's table style: bold framing
   sentence ("V2/V3 are binary pools, so X is implicit") above the
   table where the architectural distinction is meaningful
5. **Common parameters** — table of parameters identical across all
   supported protocols. For sibling primitives this is most parameters
6. **Protocol-specific parameters** — per-protocol subsections where
   the dispatcher's input shape diverges. For sibling primitives this
   section is short or omitted entirely; cross-link to the sibling
   pages instead
7. **Math / Mathematical contract / What this measures** — sized per
   stratification (see §"Math section stratification" below). Section
   title varies; placement is fixed (between params and example)
8. **Example** — runnable code with output. **Lift verbatim from the
   existing notebook page** where possible — the examples have real
   MockProvider data and validated output. Where the existing example
   doesn't show the full primitive surface, augment rather than
   replace
9. **How this composes** — small footer naming what the primitive
   depth-chains over (e.g., `DetectRugSignals` over `CheckPoolHealth`),
   breadth-chains over (e.g., `AggregatePortfolio` over `AnalyzePosition`
   siblings), or what other primitives compose over it
10. **See also** — sibling primitives, related primitives, MCP tool
    exposure status, DeFi Math cross-link where relevant

Sections 3, 6, and 9 are **conditional** — include where they apply,
omit where they don't. Sections 1, 2, 4, 5, 7, 8, 10 are **mandatory**
for every page.

---

## Math section stratification

### Paper depth — section title: **Math**

Reserved for primitives whose value proposition is the math itself. Four
primitives in this tier:

#### `AssessDepegRisk`

Closed-form ε ↔ δ derivation over the stableswap invariant. From
PROJECT_CONTEXT session 2026-04-22 notes:

- Parameterize by ε = (x−y)/(x+y)
- Expand the stableswap invariant: u = S/D − 1 = ε²/[(4A+2)(1−ε²)]
- Expand dydx for the off-peg price: δ ≈ 2ε/(α+1+ε) with α = A(1−ε²)²
- Invert via fixed-point on δ → ε (~5 iterations)
- Closed-form values: v_LP = S·(1−δ(1+ε)/2), v_hold = D·(1−δ/2)
- IL = (v_LP − v_hold)/v_hold
- Reachability: |ε|>1 indicates unreachable; flagged via `Optional[float]`
  fields on the result

The page should walk through these five-or-so steps with `:math:`
formatting. PROJECT_CONTEXT cites Cintra & Holloway 2023 and the Curve
whitepaper as the academic precursors — surface this attribution. The
*innovation framing* is also worth surfacing: "the math is academic;
the packaging as a stateless typed primitive with explicit reachability
semantics is what's new." This is consistent with the substrate framing
of the v2 plan.

#### `OptimalDepositSplit`

V2 zap-in quadratic with the dα/d(dx) < 0 result. From PROJECT_CONTEXT
session 2026-04-23 (part 2):

- Closed form: f·α²·dx + r·α·(1+f) − r = 0 with f = 0.997
- Limit: as dx → 0, α → 1/(1+f) ≈ 0.50075
- Implicit differentiation: dα/d(dx) = −α²f / [2αf·dx + r(1+f)] < 0 identically
- Therefore α decreases monotonically with deposit size
- Intuition: a larger swap moves the price more → each unit swapped buys
  *less* of the opposing token → you swap *less*

The page should surface the counterintuitive direction-of-change result
explicitly — PROJECT_CONTEXT records that an earlier test iteration
shipped with the wrong sign assumption and the failing tests forced the
derivation. Naming this in the docs prevents future readers (and LLMs
composing primitives) from making the same mistake.

#### `FindBreakEvenPrice`

Closed-form alpha inversion. The primitive answers "at what price ratio
α does fee income equal IL?" — the V2/V3 case has a closed form
inverting the IL formula. The exact derivation lives in the
implementation; **the spec mandates a source-read of
`FindBreakEvenPrice.py` to lift the actual derivation accurately**
rather than paraphrasing.

Both upside and downside α are reported (the IL formula is symmetric
about α=1, so each level of fees corresponds to two breakeven prices).
The page should surface the both-roots structure, the V2 vs V3
parameterization difference, and the upside-hedged condition (when
fees exceed the IL at α=∞, the position has no upside breakeven —
flagged via `upside_hedged: bool` on the result).

#### `DetectFeeAnomaly`

Invariant-vs-contract consistency check. From PROJECT_CONTEXT session
2026-04-22:

- The primitive computes the *theoretical* swap output from the
  constant-product invariant at the pool's stated fee, then compares
  against the *actual* output from `lp.get_amount_out`
- Pure-float reference implementation: `out = (y · dx · 0.997) /
  (x + dx · 0.997)` for V2 30bps
- Discrepancy in basis points; signed (positive = pool overdelivers,
  negative = pool underdelivers)
- Direction labels are descriptive (`pool_underdelivers` /
  `pool_overdelivers`), not accusatory (no `pool_skimming`-style verdicts)
- V2-only in v1 because `UniV3Helper.quote` hard-codes 30bps fee — see
  cleanup backlog

The page should surface the philosophical framing PROJECT_CONTEXT names
explicitly: this primitive treats the protocol library as a *metadata
adapter* and uses the invariant directly as the *math source*. That's a
non-obvious architectural choice and it's the reason the primitive is
robust — driving the protocol library's solvers to a counterfactual
state would be more code, less reliable, and harder to verify.

### Contract depth — section title: **Mathematical contract**

For primitives that compose over upstream IL classes
(`UniswapImpLoss` / `BalancerImpLoss` / `StableswapImpLoss`) or
otherwise wrap a known formula. The math isn't original to the
primitive but the *contract* is — numeraire convention, V2-vs-V3
dispatch, edge cases, what's deferred to upstream vs handled here.

About one paragraph plus the key formula in `:math:` form. Coverage:

- `AnalyzePosition` — V2/V3 IL formula `2√α/(1+α) − 1`; numeraire is
  token0; uses `UniswapImpLoss.calc_iloss`; paper-value via
  `x_tkn_init`/`y_tkn_init` not settlement-value (RebaseIndexToken
  V3 100%-ownership crash, per PROJECT_CONTEXT)
- `AnalyzeBalancerPosition` — Balancer weighted-pool IL
  `α^w_base + (1-w_base)·α^(w_base-1) − 1`; opp-token numeraire;
  fee-free spot computed inline (not via `lp.get_price` which bakes
  in SWAP_FEE); v1 has `fee_income = 0.0` (upstream limit)
- `AnalyzeStableswapPosition` — stableswap IL via the invariant; peg
  numeraire (1:1 across tokens); at-peg short-circuit (`abs(dydx-1.0)
  < 1e-12`); unreachable-alpha returns `Optional[float]` with
  metadata still populated
- `SimulatePriceMove` (V2/V3) — projects α' = α·(1+pct), evaluates IL
  formula at α', returns scenario in same numeraire as the underlying
  IL class
- `SimulateBalancerPriceMove` — same shape, weighted-pool IL formula,
  weight-aware
- `SimulateStableswapPriceMove` — same shape; current-alpha derivation
  via `lp.math_pool.dydx(0, 1, use_fee=False)`; new shock compounds:
  `new_alpha = current_alpha · (1+pct)`
- `FindBreakEvenTime` — given fee accrual rate, blocks/days until
  cumulative fees match IL at current α; relies on V2's `fee0_arr`/
  `fee1_arr` history (V3 has accumulator only — surface this)
- `EvaluateRebalance` — depth-chain over multiple per-position
  primitives + breadth-chain over candidate ranges; rebalance cost =
  swap fees + slippage + gas; benefit = projected IL reduction at
  scenario shocks
- `EvaluateTickRanges` — V3-only; per-candidate range-width, capital
  efficiency, in-range probability heuristic
- `CompareFeeTiers` — V3-only breadth-chain over CheckPoolHealth +
  CheckTickRangeStatus; observed_fee_yield = cumulative_fees / TVL
  (cumulative, not annualized — pool age unknown)
- `CompareProtocols` — IL at price shock + slippage at trade size
  across two protocols; V3 IL is `None` when shock > range; Balancer/
  Stableswap slippage is `None` (CalculateSlippage Uniswap-only in v1)
- `AggregatePortfolio` — breadth-chain over per-protocol analyzers;
  numeraire = first-token symbol; mixed-numeraire raises ValueError;
  Stableswap unreachable-alpha contributes 0 to totals + appends to
  shared_exposure_warnings
- `CalculateSlippage` — V2/V3 only; spot price from raw reserves
  (no fee), execution price from `get_amount_out` (with fee),
  slippage_pct = 1 − execution/spot
- `DetectMEV` — theoretical-vs-actual output comparison for a single
  swap; difference attributed to MEV when above noise threshold; V2/V3

For each, the source-read mandate applies — confirm the formula and
edge cases against the implementation file before drafting.

### Measurement depth — section title: **What this measures**

For primitives that are structured reads, not derivations. Three
primitives:

- `CheckPoolHealth` — TVL in token0, reserves, total_liquidity,
  collected fees, num_swaps (V2-only), fee_accrual_rate_recent
  (V2-only), num_lps, top_lp_share_pct (excluding `"0"` MINIMUM_LIQUIDITY
  sentinel), has_activity. **What this measures**: a snapshot of
  pool-level health metrics — reserves and liquidity from pool state,
  fee totals from the running accumulator (V2: per-swap history; V3:
  globalX128 accumulator), LP concentration computed across
  `liquidity_providers` excluding the MINIMUM_LIQUIDITY burn sentinel
- `CheckTickRangeStatus` — V3-only. pct_to_lower / pct_to_upper
  (positive when in-range, negative when crossed); in_range bool;
  range_width_pct. **What this measures**: where the pool's current
  tick sits relative to the position's range bounds, in percentage
  terms. No math beyond unit conversion from ticks to percent
- `DetectRugSignals` — three signals: tvl_suspiciously_low,
  single_sided_concentration (strict `>` threshold so passing 1.0
  disables), inactive_with_liquidity (V2-only — depends on
  `fee_accrual_rate_recent`). **What this measures**: depth-chain over
  `CheckPoolHealth` — applies threshold comparators to the health
  snapshot to surface a count-based risk bucket
  (low/medium/high/critical based on signal count). The primitive
  surfaces signals; the verdict belongs to the caller

The "What this measures" framing is honest: these primitives don't
derive anything, they read state and apply thresholds. Calling that
"Math" would oversell what the code does and mislead readers about
where the calculator framing lives.

---

## Per-primitive page assignment

21 primitive pages, one per file. Categorized for execution order
(starting with paper-depth primitives because they have the most
content to draft and benefit from doing them while the math is fresh):

### Tier 1 — Paper depth (4 pages, ~60 min each)

1. `AssessDepegRisk` (Risk category)
2. `OptimalDepositSplit` (Optimization category)
3. `FindBreakEvenPrice` (Break-Even category)
4. `DetectFeeAnomaly` (Pool Health category)

### Tier 2 — Contract depth, sibling primitives (6 pages, ~45 min each)

5. `AnalyzePosition` (Position Analysis)
6. `AnalyzeBalancerPosition` (Position Analysis)
7. `AnalyzeStableswapPosition` (Position Analysis)
8. `SimulatePriceMove` (Price Scenarios)
9. `SimulateBalancerPriceMove` (Price Scenarios)
10. `SimulateStableswapPriceMove` (Price Scenarios)

### Tier 3 — Contract depth, dispatcher and remaining (8 pages, ~45 min each)

11. `AggregatePortfolio` (Portfolio)
12. `CompareProtocols` (Comparison)
13. `CompareFeeTiers` (Comparison)
14. `CalculateSlippage` (Execution)
15. `DetectMEV` (Execution)
16. `EvaluateRebalance` (Optimization)
17. `EvaluateTickRanges` (Optimization)
18. `FindBreakEvenTime` (Break-Even)

### Tier 4 — Measurement depth (3 pages, ~30 min each)

19. `CheckPoolHealth` (Pool Health)
20. `CheckTickRangeStatus` (Risk)
21. `DetectRugSignals` (Pool Health)

### Category overview pages (9 pages, ~15 min each)

22. Position Analysis overview
23. Price Scenarios overview
24. Pool Health overview
25. Risk overview
26. Optimization overview
27. Comparison overview
28. Execution overview
29. Portfolio overview
30. Break-Even overview

Each category overview contains: short paragraph, the existing
availability matrix (kept), one-liner per primitive in that category
with a `:doc:` link to the primitive page, and the existing
`Protocol coverage` and `MCP tool exposure` sections (filled with
content from the superseded spec's per-page tables — that content is
still valid, just relocated).

---

## File layout

```
doc/source/agentic_primitives/
├── index.rst                                 # MOVED — becomes top-level overview
├── position_analysis/
│   ├── index.rst                             # category overview
│   ├── analyze_position.rst                  # NEW
│   ├── analyze_balancer_position.rst         # NEW
│   └── analyze_stableswap_position.rst       # NEW
├── price_scenarios/
│   ├── index.rst
│   ├── simulate_price_move.rst
│   ├── simulate_balancer_price_move.rst
│   └── simulate_stableswap_price_move.rst
├── pool_health/
│   ├── index.rst
│   ├── check_pool_health.rst
│   ├── detect_rug_signals.rst
│   └── detect_fee_anomaly.rst
├── risk/
│   ├── index.rst
│   ├── check_tick_range_status.rst
│   └── assess_depeg_risk.rst
├── optimization/
│   ├── index.rst
│   ├── optimal_deposit_split.rst
│   ├── evaluate_rebalance.rst
│   └── evaluate_tick_ranges.rst
├── comparison/
│   ├── index.rst
│   ├── compare_fee_tiers.rst
│   └── compare_protocols.rst
├── execution/
│   ├── index.rst
│   ├── calculate_slippage.rst
│   └── detect_mev.rst
├── portfolio/
│   ├── index.rst
│   └── aggregate_portfolio.rst
└── break_even/
    ├── index.rst
    ├── find_break_even_price.rst
    └── find_break_even_time.rst
```

The existing notebook-based pages at `doc/source/agentic_primitives/
notebooks/` are **demoted** but not deleted — they continue to exist
for the notebook-renderable examples, and the new `.rst` pages
reference them via `:doc:` cross-references for the runnable example.
Alternatively, lift the example code into the `.rst` pages directly
and retire the `notebooks/` subtree; spec defaults to the first
option (preserve notebooks, reference from RST) because the existing
notebook examples have already-validated output cells.

The Claude Code session should confirm at start which approach is
correct based on whether the existing notebooks still serve a
purpose beyond the API docs (e.g., are they linked from the textbook
or course?). If yes — preserve and reference. If no — lift inline
and retire the subtree.

---

## Mode B mandate (locked from Core Primitives batch)

For each primitive page, before drafting:

1. **Read the implementation file.** Locate at `defipy/python/prod/
   primitives/<category>/<PrimitiveName>.py`. Read the `apply()`
   signature line-by-line. Confirm parameter types, defaults, the
   exact dispatch logic if multi-protocol.
2. **Read the result dataclass.** At `defipy/python/prod/utils/data/
   <ResultClassName>.py`. Confirm field names, Optional vs required,
   and any field semantics that aren't obvious from the name.
3. **Read the existing test file.** At `python/test/primitives/
   <category>/test_<primitive_name>.py` (or similar). Confirm in-
   the-wild call shapes match the spec's per-protocol tables.
4. **For Tier 1 (paper-depth) primitives, also read the docstring
   in detail.** PROJECT_CONTEXT notes that primitives like
   AssessDepegRisk carry the closed-form derivation in the
   implementation docstring or comments. Quote the actual derivation
   rather than paraphrasing.
5. **For composition primitives (DetectRugSignals over CheckPoolHealth,
   AggregatePortfolio over Analyze* siblings), read both files** — the
   composition primitive should match the dependency primitive's
   contract honestly.

A signature surprise during drafting is the **expected** outcome of
this read pass — it's the same discipline that produced the
Balancer/Stableswap finding in the Core Primitives `Join` page.
Lower-effort surprises this batch will likely produce: parameter
defaults that PROJECT_CONTEXT didn't capture, Optional vs required
fields on result dataclasses that affect example construction,
edge cases handled in the implementation that the original notebook
example didn't exercise.

---

## Example handling

The existing notebook pages have substantial validated content —
real MockProvider data, real numbers, runnable cells. Preservation is
the rule:

- **Lift the example verbatim** from the existing notebook page when
  it exercises the primitive's full surface
- **Augment the example** when it doesn't (e.g., the existing
  `CompareFeeTiers` example shows only one candidate per the
  MockProvider single-V3-recipe limitation — add a second hand-built
  candidate to show the ranking actually working)
- **Replace the example** only if it's broken or misleading (this is
  rare — the existing notebooks have been audited)

The example section on each new RST page should sit *after* the math
section (per the locked template) and use Sphinx `.. code-block::
python` directive with `:linenos:` if multi-step. Output blocks
follow the existing convention — fenced code blocks with a `# OUTPUT:`
comment marker, matching the README and existing notebook style.

If the existing notebooks are kept (per §"File layout" question), the
example section can be a short `:doc:` cross-reference instead — but
the page should still embed at minimum the construction call and one
result print so a direct-link reader gets the gist without clicking
out.

---

## Top-of-batch verification

```bash
cd ~/repos/defipy
git checkout -b docs/agentic-primitives-restructure
pytest python/test/ -v 2>&1 | tail -5
```

Expected: 629 passed (per DEFIPY_V2_SHIPPED.md). Investigate before
proceeding if different.

```bash
ls doc/source/agentic_primitives/
ls doc/source/agentic_primitives/notebooks/
```

Confirm current layout matches what this spec assumes; adjust file
paths if needed.

```bash
cd doc && make html 2>&1 | tail -10
```

Baseline build before the batch.

**Sphinx mathjax check.** The spec uses `:math:` directives heavily.
Confirm mathjax is enabled:

```bash
grep -A 2 "mathjax\|extensions" doc/source/conf.py
```

Look for `'sphinx.ext.mathjax'` in the extensions list. If missing,
add it before drafting any Tier 1 page (the math-heavy ones break
without mathjax). If present, proceed.

---

## Per-page execution rhythm

For each primitive page:

1. **Source read** (~10-15 min for Tier 1 paper-depth; ~5-10 min for
   others) — implementation file, result dataclass, test file, plus
   docstring for Tier 1
2. **Lift the existing example** (~5 min) — copy from current notebook
   page; note any augmentation needed
3. **Draft the RST page** (~25-50 min depending on tier) — follow
   the locked template; fill the math/contract/measurement section
   per its tier
4. **Local Sphinx build** (~2 min) — `make html`, resolve any RST
   warnings (broken refs, malformed directives, mathjax issues)
5. **Read the rendered page** (~5 min) — open local HTML in browser;
   verify tables format, callouts render, code blocks have syntax
   highlighting, math equations render via mathjax, cross-references
   resolve
6. **Commit** — small commits per primitive page. Pattern:

```
docs(agentic_primitives): standalone page for <Primitive>

Replaces inline section on the <Category> notebook page with a
standalone RST page following the locked Core Primitives template
(Hook → When-to-use → Signature → Common params → Protocol-specific →
<Math|Mathematical contract|What this measures> → Example → Composes →
See also).

<For Tier 1: brief math summary, e.g., "Math section walks the
ε ↔ δ closed-form derivation over the stableswap invariant.">

Verified against defipy/python/prod/primitives/<path>/<Primitive>.py
and python/test/primitives/<test>.py.

Part of the Agentic Primitives restructure batch — see
doc/execution/CLAUDE_CODE_SPEC_agentic_primitives_restructure.md.
```

Sequence: Tier 1 → Tier 2 → Tier 3 → Tier 4 → Category overviews →
top-level `agentic_primitives/index.rst` update.

The category overview commits land **after** all primitives in that
category are committed. The top-level index update lands **last** so
the toctree doesn't 404 mid-sequence.

---

## Index page updates

### Top-level `agentic_primitives/index.rst`

Currently a single overview page with a giant per-primitive availability
matrix. Becomes a thinner overview that:

- Keeps the introductory paragraph and "all primitives follow the
  same contract" framing
- Keeps the giant availability matrix (it's a useful at-a-glance entry
  point even if every cell links to the per-primitive page)
- Replaces the per-primitive descriptions block with a `toctree`
  pointing at the 9 category overviews

```rst
.. toctree::
   :maxdepth: 2

   position_analysis/index
   price_scenarios/index
   pool_health/index
   risk/index
   optimization/index
   comparison/index
   execution/index
   portfolio/index
   break_even/index
```

### Category overview pages (9 files)

Each `<category>/index.rst` contains:

```rst
<Category Name>
===============

<Short paragraph framing what this category answers and why it exists.
Lift from the existing notebook page intro, tighten if needed.>

.. toctree::
   :maxdepth: 1

   <primitive_1>
   <primitive_2>
   ...

Primitives in this category
---------------------------

* :doc:`<Primitive 1>` — <one-line description from the existing
  primitive descriptions section>.
* :doc:`<Primitive 2>` — <one line>.
* ...

Protocol coverage
-----------------

<Lift table from superseded spec's per-page coverage section. The
content is already written; just slot it in here under the new
location.>

MCP tool exposure
-----------------

<Lift from existing notebook page's MCP tool exposure section.>
```

The Protocol coverage tables from the superseded spec map directly
onto these category pages — that's the merge of the prior spec's
Item 1 into this restructure. The substance is the same; the
location moves from the bottom of a category-as-notebook page to a
section on a category-as-overview page.

---

## Risk list

**1. Mathjax rendering inconsistency between local and RTD builds.**
Mathjax can render fine locally but fail on RTD if conf.py doesn't
explicitly enable the extension. The verification step above catches
this — but if the page-level math sections start failing on the RTD
preview, the fix is in conf.py, not in the pages. Don't try to
work around mathjax issues at the per-page level.

**2. Notebook-vs-RST format mixing.** If the spec retains the
existing notebooks and the new RST pages reference them, Sphinx must
resolve `:doc:` references across both formats. Confirm at first
build that nbsphinx is wired and the cross-format references resolve.
If not, lift examples into RST and retire notebooks.

**3. PROJECT_CONTEXT may have drifted from current implementation.**
The closed-form derivation for AssessDepegRisk in PROJECT_CONTEXT
session 2026-04-22 notes was accurate at write time. The
implementation may have evolved (refactor, extension, bug fix). Mode
B mandates source-read; if the source has diverged from
PROJECT_CONTEXT, **trust the source** and update PROJECT_CONTEXT in
a separate followup commit.

**4. The IL formula `2√α/(1+α) − 1` is one of several equivalent
forms.** Different protocols / implementations / academic sources
prefer different parameterizations. Use the form that matches the
implementation (read the source); reference the academic precursors
in the See also section but don't introduce a parameterization the
code doesn't actually use. Inconsistency between the page's math
section and the actual implementation code is the bug to avoid.

**5. The "How this composes" section can become repetitive across
sibling primitives.** AnalyzePosition / AnalyzeBalancerPosition /
AnalyzeStableswapPosition all compose into AggregatePortfolio. Don't
copy-paste the same paragraph three times — vary the framing per
primitive (e.g., "A V2/V3 entry point for portfolio analysis" vs
"The Balancer entry point that lets `AggregatePortfolio` route
mixed-protocol portfolios" vs "The Stableswap entry point with
unreachable-alpha handling that propagates to portfolio totals").

**6. The Tier-stratification is editorial, not algorithmic.** A
primitive can have nontrivial math under the hood (e.g.,
AnalyzePosition uses `UniswapImpLoss` which has a real derivation)
but still belong in Tier 2 because the *primitive's contribution* is
contractual, not derivational. Don't promote primitives to Tier 1
because their dependencies have math; promote them only when the
primitive itself contributed a derivation. PROJECT_CONTEXT's
"invariant-math vs state-threading" framing (heuristic #9) helps:
invariant-math primitives belong in Tier 1; state-threading
primitives are usually Tier 2 unless the threading itself is novel.

**7. Existing notebook examples may not exercise the full result
dataclass surface.** The Mode B source-read of the result dataclass
will surface fields the example doesn't print. Either augment the
example to show those fields, or note them as available in the
result without showing them — the page should give the reader a
complete view of what the primitive returns, not just what the
example happens to print.

---

## Out of scope (file but don't expand)

If during execution you spot:

- Tutorial pages with similar surface-pattern gaps (the V3 tutorial
  showing Join with ticks but not framing it as "the V3 variant of a
  dispatcher")
- The DeFi Math sidebar section lacking pages for Balancer or
  Stableswap derivations that the new Math sections cross-reference
- The `defipy.tools` reference page lacking per-tool MCP exposure
  notes that mirror the new per-primitive pages
- The Result Dataclasses page lacking field-level semantics for fields
  like `Optional[float]` that are surfaced loudly on the new primitive
  pages
- Composition examples (the explicit "DetectRugSignals over
  CheckPoolHealth" pattern) that would benefit from a dedicated
  "Composing primitives" page

**File these to** `doc/execution/V2_FOLLOWUPS.md`. Don't address inline.

The biggest temptation in this batch is to start fixing the DeFi Math
section while writing the math sections — resist. The DeFi Math
section is its own surface with its own audience; this batch
cross-links to it where useful but doesn't restructure it.

---

## Definition of done

- [ ] Branch `docs/agentic-primitives-restructure` exists and contains
      ~30+ commits (21 primitive pages + 9 category overviews + index
      update + any conftest/setup commits)
- [ ] All 21 primitive pages exist as standalone `.rst` files in their
      category subdirectories
- [ ] All 9 category overviews exist as `index.rst` in their
      subdirectories with the toctree wired
- [ ] Top-level `agentic_primitives/index.rst` updated with the
      category-overview toctree
- [ ] `make html` builds cleanly (no new warnings introduced by this
      batch beyond the pre-existing baseline)
- [ ] All math sections render correctly: equations format via
      mathjax, no missing references, no malformed `:math:` directives
- [ ] Spot-check three pages in the rendered preview to verify
      structural consistency: pick one Tier 1 (e.g., `AssessDepegRisk`),
      one Tier 2 sibling (e.g., `AnalyzeBalancerPosition`), one Tier 4
      measurement (e.g., `CheckPoolHealth`). Confirm all three follow
      the same section order with appropriately-sized math sections
- [ ] Each per-page commit names the implementation source file and
      result dataclass file in the commit message body
- [ ] Branch pushed; RTD PR-preview build green; preview URL eyeballed
      for visual regressions vs main
- [ ] Followups (if any) filed to `V2_FOLLOWUPS.md`
- [ ] PR opened against main with a description that:
  - Names the predecessor (Core Primitives batch) and explicitly notes
    the superseded prior Agentic Completion spec
  - Names the architectural decision (strict mirror of Core template
    onto every primitive, with stratified math sections)
  - Lists the three math-depth tiers with example primitives in each
  - Names the Tier 1 primitives where the docs surface original
    derivations (these are the four pages that most strongly earn the
    "DeFiPy ships the math" framing for v2)
  - Confirms scope held: 21 primitive pages + 9 category overviews +
    index; no Core re-touches; no DeFi Math section restructure;
    no IA changes beyond what the per-primitive split mandates

---

## Appendix — Why the math sections matter for v2.0

The v2.0 substrate framing rests on a claim DEFIPY_V2_AGENTIC_PLAN
makes explicitly: "DeFiPy ships the math" — most DeFi tools wrap APIs;
DeFiPy's value is the hand-derived primitive math, exposed as
composable typed primitives. That framing is currently *asserted* in
the v2.0 README and home page but not *demonstrated* on the API doc
surface where the primitives actually live. A reader who lands on
`AssessDepegRisk` from a search result currently sees signature, prose
description, and example — none of which surface the closed-form
ε ↔ δ derivation that's the actual reason to use this primitive over
"a generic Curve IL calculator."

The Math section on the four Tier 1 primitive pages is where that
framing earns its keep. The Mathematical contract section on Tier 2
primitives is where the V2-vs-V3 dispatch, numeraire, and edge-case
discipline becomes visible. The What this measures section on Tier 4
primitives keeps the framing honest by *not* overclaiming math content
where there isn't any.

The stratification is therefore not just editorial convenience — it's
the mechanism by which the substrate framing becomes verifiable on the
primary documentation surface. An LLM reading these pages as ambient
context can distinguish "primitive that contributed a derivation" from
"primitive that wraps an upstream formula" from "primitive that reads
state and applies thresholds" — and that distinction matters when the
LLM reasons about whether to compose primitives or call them in
isolation.

That's the deeper "why" behind this batch. The Core Primitives mirror
makes the API surface uniform; the math sections make the calculator
framing real.

— end spec —
