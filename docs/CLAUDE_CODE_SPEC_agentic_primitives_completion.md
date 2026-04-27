# Claude Code Spec — Agentic Primitives Doc Completion

**Status:** Spec — ready for execution
**Owner:** Claude Code session
**Estimated effort:** ~half-day end-to-end (Item 1: 30-45 min; Item 2: 90-120 min; integration: 15-30 min)
**Predecessor:** `CLAUDE_CODE_SPEC_protocol_variants_batch.md` (Core Primitives batch — same template, similar discipline; this followup builds on its locked patterns)
**Branch:** `docs/agentic-primitives-completion` off whichever working branch follows the Core Primitives merge

---

## TL;DR

The Agentic Primitives docs are mostly handled correctly — the sibling-
primitive architecture (`AnalyzePosition` / `AnalyzeBalancerPosition` /
`AnalyzeStableswapPosition` rather than one branchy primitive) means
each primitive's reference page is already unambiguous on its own.
**This is by design — PRIMITIVE_AUTHORING_CHECKLIST §11.**

But there are two real gaps:

1. **Empty `Protocol coverage` section on every category page.** The
   heading renders, then jumps straight to `MCP tool exposure` with
   nothing between. 9 category pages, 9 empty sections.
2. **Three dispatcher-shaped Agentic Primitives** that *do* have the
   Core Primitives "single primitive, divergent per-protocol parameters"
   problem in miniature: `AggregatePortfolio`, `CompareProtocols`,
   `CalculateSlippage`. Their per-protocol parameter divergence is
   currently buried in a single sentence of prose rather than surfaced
   as a structured per-protocol breakdown.

This batch fills the first gap and applies the locked Core Primitives
template to the second — inlined into the existing category pages
rather than as new pages, since the Agentic IA is already
category-page-with-primitive-subsections.

**Out of scope:** restructuring the Agentic IA, rewriting the existing
sibling-primitive sections (they're already correct), Core Primitives
re-touches, or the `defipy.org` Phase 2 site.

---

## Verified scope

From the live RTD audit conducted in the predecessor session:

| Category page | Has empty `Protocol coverage`? | Has dispatcher-primitive needing variants? |
|---|---|---|
| Position Analysis | ✅ empty | ❌ (sibling pattern, already correct) |
| Price Scenarios | ✅ empty | ❌ (sibling pattern, already correct) |
| Pool Health | ✅ empty | ❌ (V2/V3 only, scope not divergence) |
| Risk | ✅ empty | ❌ (V3-only + Stableswap-only, scope not divergence) |
| Optimization | ✅ empty | ❌ (single-protocol primitives) |
| Comparison | ✅ empty | ✅ `CompareProtocols` |
| Execution | ✅ empty | ✅ `CalculateSlippage` |
| Portfolio | ✅ empty | ✅ `AggregatePortfolio` |
| Break-Even | ✅ empty | ❌ (sibling extensions deferred to v2.1) |

All 9 category pages are missing Protocol coverage content. 3 of those
9 also have a dispatcher-shaped primitive that needs the Core Primitives
template applied inline.

---

## Item 1 — Fill Protocol coverage sections (~30-45 min total)

### Goal

Every category page's `Protocol coverage` section answers three questions
in a uniform format:
1. What protocols does this category currently cover?
2. What's deferred to v2.1+?
3. Why? (architectural reason, not "not implemented yet")

### Why "what's deferred and why" matters

The Agentic Primitives page is a v2.0 surface that an LLM may read as
ambient context when deciding how to compose a multi-step analysis. If
the page says "covers V2/V3" without naming Balancer/Stableswap as
deferred-with-reason, the LLM has no way to distinguish *"Balancer
isn't supported yet"* from *"Balancer doesn't make architectural sense
here"*. The first is a roadmap detail; the second is a domain fact.
Both shape what the LLM proposes next.

The reasoning material is already written — it lives in PROJECT_CONTEXT
"Bucket A / B / C" analysis, in DEFIPY_V2_AGENTIC_PLAN's deferred-items
list, and in the per-primitive notes in DEFIMIND_TIER1_QUESTIONS. This
item *transcribes* that reasoning into the per-page coverage sections;
it doesn't generate new analysis.

### Format (locked)

Use a 3-row paragraph + table structure. Short paragraph, then table
listing per-protocol status, then a single line on architectural rationale
where appropriate:

```rst
Protocol coverage
^^^^^^^^^^^^^^^^^

<one-paragraph summary of what this category currently covers — about
2-3 sentences naming the protocols supported and why this category
exists>.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Protocol
     - Coverage
     - Notes
   * - Uniswap V2
     - Full
     - <one line>
   * - Uniswap V3
     - Full / Partial / N/A
     - <one line>
   * - Balancer
     - Full / Partial / Deferred (v2.1) / N/A
     - <one line on what's missing and why, or what's intentionally
       N/A and why>
   * - Stableswap
     - Full / Partial / Deferred (v2.1) / N/A
     - <same shape>

<optional one-line architectural rationale paragraph if the coverage
gap reflects a design choice rather than a roadmap item>.
```

The "Coverage" column has 4 valid values:
- **Full** — all primitives in the category support this protocol
- **Partial** — some primitives support it, others don't (use Notes
  to say which)
- **Deferred (v2.1)** — architecturally supported, not yet shipped
- **N/A** — protocol architecturally outside the category's scope (e.g.,
  V3-only mechanics like tick ranges don't map to V2)

### Per-page content (transcribed from existing planning docs)

The substance for each of the 9 sections is listed below. Each is a
direct lift from PROJECT_CONTEXT or DEFIPY_V2_AGENTIC_PLAN — the spec
captures it inline so the Claude Code session doesn't have to interpret
which excerpt matters.

#### Position Analysis

Coverage: Full across all 4 protocols via sibling primitives.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `AnalyzePosition`, V2 path |
| Uniswap V3 | Full | `AnalyzePosition`, V3 path with `lwr_tick`/`upr_tick` |
| Balancer | Full | `AnalyzeBalancerPosition`, 2-asset weighted pools; v1 ships with `fee_income = 0.0` (no per-LP fee attribution in upstream) |
| Stableswap | Full | `AnalyzeStableswapPosition`, 2-asset; supports unreachable-alpha and at-peg short-circuit regimes |

Architectural rationale: the sibling-primitive pattern (one primitive
per protocol, separate result dataclasses) is codified as
PRIMITIVE_AUTHORING_CHECKLIST §11. Forcing isinstance dispatch into a
single primitive would conflate result shapes (per-token lists for
stableswap, weight fields for Balancer). Per-protocol siblings keep
each focused on its protocol's natural math.

#### Price Scenarios

Coverage: Full across all 4 protocols via sibling primitives. Mirrors
Position Analysis.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `SimulatePriceMove`, V2 path |
| Uniswap V3 | Full | `SimulatePriceMove`, V3 path with tick-aware IL |
| Balancer | Full | `SimulateBalancerPriceMove`, weight-aware IL formula |
| Stableswap | Full | `SimulateStableswapPriceMove`; unreachable-alpha returns Optional `None` fields with metadata still populated |

#### Pool Health

Coverage: V2/V3 only.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `CheckPoolHealth`, `DetectRugSignals`, `DetectFeeAnomaly` all V2-supported |
| Uniswap V3 | Partial | `CheckPoolHealth` and `DetectRugSignals` work; `DetectFeeAnomaly` is V2-only (blocked on `UniV3Helper.quote` hard-coded fee — see cleanup backlog). `num_swaps` and `fee_accrual_rate_recent` are V2-only on `CheckPoolHealth` because V3 lacks per-swap history |
| Balancer | N/A | Pool-health metrics like LP concentration, swap activity, and rug signals don't map cleanly to weighted-pool semantics where TVL is shares-based and concentration is a different question; v1 keeps the category Uniswap-focused |
| Stableswap | N/A | Same as Balancer; the at-peg / off-peg framing of stableswap risk is captured by `AssessDepegRisk` (see Risk category) instead |

V3 fee anomaly support unblocks once the upstream `UniV3Helper.quote`
fix lands (tracked in the cleanup backlog).

#### Risk

Coverage: split by protocol — different risks matter for different AMM
families.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | N/A | V2's symmetric reserves don't have V3's range-status risk or Stableswap's depeg risk; V2-specific risks (MEV, slippage) live in Execution |
| Uniswap V3 | Full | `CheckTickRangeStatus` answers "is my range still active?" |
| Balancer | Deferred (v2.1) | Weight-imbalance and out-of-band swap-fee risks are tracked but not yet primitive-formalized |
| Stableswap | Full | `AssessDepegRisk` quantifies exposure to a stablecoin depeg using the closed-form ε ↔ δ derivation over the invariant; 2-asset only in v1 (N>2 is non-trivial new math) |

Architectural rationale: Risk is the most protocol-divergent category
in v2.0. What "risk" *means* differs structurally per AMM family — V3's
risk is range-status, Stableswap's is depeg, Balancer's is weight
exposure — so the category fans out into protocol-specific primitives
rather than parallel siblings.

#### Optimization

Coverage: per-protocol single-primitive coverage.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `OptimalDepositSplit` (zap-in fraction), `EvaluateRebalance` (rebalance cost vs benefit) |
| Uniswap V3 | Full | `EvaluateTickRanges` (tick range candidate evaluation + split) |
| Balancer | Deferred (v2.1) | Optimal-weight selection and zap-in optimization deferred until weighted-pool primitives stabilize |
| Stableswap | Deferred (v2.1) | Stableswap zap-in is non-trivial (non-symmetric reserves at peg) and unblocked by future invariant-math primitives |

#### Comparison

Coverage: Full cross-protocol on `CompareProtocols`; V3-only on
`CompareFeeTiers`.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full (`CompareProtocols`); N/A (`CompareFeeTiers` — V2 has a single 30bps fee) | |
| Uniswap V3 | Full (both primitives) | `CompareFeeTiers` is V3-only by definition |
| Balancer | Partial | Accepted as candidate in `CompareProtocols`; `slippage_at_amount` returns `None` because `CalculateSlippage` is Uniswap-only (see Execution coverage); IL still computed |
| Stableswap | Partial | Same shape as Balancer — accepted in `CompareProtocols`, slippage degrades to `None` |

Slippage gap closes when `CalculateSlippage` extensions land for
Balancer/Stableswap (Bucket A / v2.1).

#### Execution

Coverage: V2/V3 only in v2.0.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `CalculateSlippage`, `DetectMEV` |
| Uniswap V3 | Full | Both primitives |
| Balancer | Deferred (v2.1) | Sibling primitives (`CalculateBalancerSlippage`) or protocol-dispatching `CalculateSlippage` planned; Bucket A in DEFIPY_V2_AGENTIC_PLAN. Math is available in upstream `BalancerExchange.get_amount_out`; the gap is primitive packaging, not derivation |
| Stableswap | Deferred (v2.1) | Same as Balancer; math available in `StableswapExchange.get_amount_out` (with the upstream `get_y` iteration-cap fix on the cleanup backlog as a related item) |

Closing this gap also unblocks full `CompareProtocols.slippage_at_amount`
plumbing.

#### Portfolio

Coverage: Cross-protocol via composition-layer dispatch.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `entry_x_amt` / `entry_y_amt`; full PnL contribution to portfolio totals |
| Uniswap V3 | Full | Same input shape as V2 plus optional `lwr_tick`/`upr_tick` for tick-aware analysis |
| Balancer | Full | `entry_x_amt` / `entry_y_amt` (mapped to base/opp internally); `fee_income = 0.0` (upstream limit) |
| Stableswap | Partial (⚠ in matrix) | Uses `entry_amounts` (list, not pair); unreachable-alpha positions contribute `0.0` to totals and append to `shared_exposure_warnings`; `fee_income = 0.0` (upstream limit) |

Architectural rationale: `AggregatePortfolio` is the canonical
*breadth-chain* (PROJECT_CONTEXT — one primitive applied N times,
results aggregated). Cross-protocol dispatch lives in this aggregator,
not in the per-protocol leaf analyzers, per heuristic #13
("Composition-layer dispatch scales; primitive-layer dispatch does
not"). All positions in a single call must share a common first-token
numeraire.

#### Break-Even

Coverage: V2/V3 only in v2.0.

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `FindBreakEvenPrice`, `FindBreakEvenTime` |
| Uniswap V3 | Full | Both primitives, full-range and concentrated-range |
| Balancer | Deferred (v2.1) | New derivation needed: weighted-pool IL `α^w + (1-w)·α^(w-1) - 1` doesn't have a general closed-form inverse; Newton iteration converges cleanly but the symmetric upside/downside alpha framing needs work |
| Stableswap | Deferred (v2.1) | New derivation needed over the invariant; mirrors `AssessDepegRisk`'s ε ↔ δ fixed-point but inverted to solve for the δ where fees compensate IL |

Bucket B in DEFIPY_V2_AGENTIC_PLAN. Half-day each, deferred until
demand surfaces.

### Item 1 execution rhythm

For each of the 9 category pages:

1. **Locate the source.** Pages live under
   `doc/source/agentic_primitives/notebooks/<category>.ipynb` (Jupyter
   notebooks rendered into Sphinx via nbsphinx — confirm at start;
   the page-source links in the live RTD point to `.ipynb.txt`
   suggesting notebooks). The empty `Protocol coverage` heading
   already exists; this is content insertion, not heading creation.
2. **Insert the content.** A markdown cell (since these are notebooks)
   inside the existing `Protocol coverage` section. Use the locked
   format above. Use the per-page content from §"Per-page content".
3. **Re-render to confirm.** `make html` from `doc/`. The list-table
   directives render in Sphinx-flavored RST; in a notebook markdown
   cell, raw HTML tables or RST list-tables should both work — confirm
   which renders correctly in the existing build by checking how the
   `Setup` and `MCP tool exposure` sections are written and matching
   that flavor.

If the existing pages use plain markdown rather than RST directives in
their cells, drop the `.. list-table::` directive and use a markdown
table — substance over format. The locked-format constraint is the
3-column structure (Protocol / Coverage / Notes) and the 4-value
Coverage vocabulary, not the specific table syntax.

### Item 1 commit pattern

One commit per category page, in the sidebar order they appear:

```
docs(agentic_primitives): fill Protocol coverage on <Category>

Replaces empty `Protocol coverage` section with structured per-protocol
status table covering current support, v2.1 deferrals, and architectural
N/A cases.

Source: PROJECT_CONTEXT.md "Bucket A/B/C" analysis and
DEFIPY_V2_AGENTIC_PLAN deferred-items list.

Part of the Agentic Primitives doc completion batch — see
doc/execution/CLAUDE_CODE_SPEC_agentic_primitives_completion.md.
```

9 commits total for Item 1. Small commits per page so the batch can be
paused or partially rolled back.

---

## Item 2 — Apply Protocol Variants template to dispatcher primitives (~90-120 min)

### Goal

Three primitives behave like Core Primitives dispatchers — single
primitive, single signature, divergent per-protocol input semantics.
Apply the Core Primitives Protocol Variants template, **inlined into
the existing category page** (not a new page).

### Architectural rationale

These three primitives are dispatchers, not siblings, by deliberate
design. Per heuristic #13 ("composition-layer dispatch scales;
primitive-layer dispatch does not"), `AggregatePortfolio` and
`CompareProtocols` correctly live as single primitives that route by
protocol — fanning them into siblings would require N×4 primitive
maintenance. `CalculateSlippage` is a leaf primitive whose protocol
divergence is *deferred*, not architectural — sibling versions
(`CalculateBalancerSlippage`, `CalculateStableswapSlippage`) are
planned as Bucket A v2.1 work; until then it ships V2/V3 only.

So:
- `AggregatePortfolio` and `CompareProtocols` get **structured per-
  protocol input documentation** because their signatures genuinely
  span four protocols
- `CalculateSlippage` gets a **scope-and-deferral note** rather than a
  full per-protocol breakdown, because its v2.0 scope is V2/V3 and the
  Balancer/Stableswap story is "deferred sibling primitives"

### Template application (modified for inline use)

The Core Primitives template is for full standalone pages. For inline
application, drop the page-level hooks and keep the per-section
structure. Add the following block **after the existing `Signature.`
block** and **before the existing `Setup` / first code example** for
each of the three primitives:

```rst
**Protocol-specific input shapes**

The single signature above dispatches across protocols. Each protocol
expects a different input shape for the per-position fields:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Protocol
     - Required fields
     - Notes
   * - Uniswap V2
     - <fields>
     - <one line>
   * - Uniswap V3
     - <fields>
     - <one line>
   * - Balancer
     - <fields>
     - <one line>
   * - Stableswap
     - <fields>
     - <one line on `entry_amounts` shape, unreachable-alpha behavior, etc.>
```

This block is the inline equivalent of the Core Primitives "Signature
at a glance" + "Common parameters" + "Protocol Variants" sections,
collapsed into a single table because the per-protocol divergence is
narrower than for `Join` (no full ecosystem-pipeline wrapping needed
since the parent category page already provides that context).

### Per-primitive content

#### `AggregatePortfolio` (Portfolio category page)

The `PortfolioPosition` dataclass has these fields per protocol —
already partially documented in the existing page's prose, but
collected here as the structured table:

| Protocol | Required fields on `PortfolioPosition` | Notes |
|---|---|---|
| Uniswap V2 | `lp`, `lp_init_amt`, `entry_x_amt`, `entry_y_amt` | Standard pair shape |
| Uniswap V3 | `lp`, `lp_init_amt`, `entry_x_amt`, `entry_y_amt`, `lwr_tick`, `upr_tick` | Tick range required for concentrated liquidity |
| Balancer | `lp`, `lp_init_amt`, `entry_x_amt`, `entry_y_amt` | Same pair shape as V2/V3; mapped to base/opp internally |
| Stableswap | `lp`, `lp_init_amt`, `entry_amounts` | **Different shape** — `entry_amounts` is a list `[x0, x1]` in pool insertion order, not paired x/y fields. Set `entry_x_amt`/`entry_y_amt` to `None` (or omit if Optional in the dataclass). Unreachable-alpha positions contribute `0.0` to totals and append a note to `shared_exposure_warnings` |

Common to all: `holding_period_days` (optional, enables real-APR fields
on per-position summaries), `name` (optional, used as ranking label).

The numeraire-enforcement behavior and the V→ValueError raised on
mismatched first-tokens already appear in the existing example —
keep the existing example, don't replace it.

#### `CompareProtocols` (Comparison category page)

The `apply()` signature takes two `lp` objects and a single `amount` —
input shape doesn't structurally diverge per protocol the way
`AggregatePortfolio` does. What diverges is *which output fields are
populated*:

| Protocol | IL at shock | Slippage at amount | Notes |
|---|---|---|---|
| Uniswap V2 | ✅ Always populated | ✅ Always populated | |
| Uniswap V3 | ⚠ `None` when `price_shock > v3_range_pct` | ✅ Always populated | Out-of-range regime: position has exited the active tick range, so IL framing doesn't apply |
| Balancer | ✅ Always populated | ❌ Always `None` (v2.0) | `CalculateSlippage` is V2/V3-only; Balancer slippage closes once Bucket A lands |
| Stableswap | ⚠ `None` on `DepegUnreachableError` | ❌ Always `None` (v2.0) | High A + large shock can produce unreachable target state; slippage same as Balancer |

The `notes` field on the result already surfaces the slippage gap when
it occurs (per the existing example output); this table makes the
contract visible *before* the example.

#### `CalculateSlippage` (Execution category page)

This is the lighter case — same template structure but the per-protocol
table collapses to a scope statement plus a v2.1 forward-look:

| Protocol | Coverage | Notes |
|---|---|---|
| Uniswap V2 | Full | `slippage_pct`, `slippage_cost`, `price_impact_pct`, `max_size_at_1pct` |
| Uniswap V3 | Partial | All fields except `max_size_at_1pct` populated; max-size analysis is V2-only because V3's tick-walking infrastructure isn't implemented yet (tracked alongside `AssessLiquidityDepth`) |
| Balancer | Deferred (v2.1) | Bucket A. Sibling primitive (`CalculateBalancerSlippage`) or protocol-dispatching extension planned. Calling `CalculateSlippage` against a Balancer pool raises `ValueError` |
| Stableswap | Deferred (v2.1) | Same as Balancer; sibling primitive planned |

Add a one-line forward-look paragraph after the table:

> Once the Balancer/Stableswap extensions land (v2.1, Bucket A in
> DEFIPY_V2_AGENTIC_PLAN), `CompareProtocols.slippage_at_amount`
> closes its current `None` gap automatically — no API break expected.

### Item 2 execution rhythm

For each of the 3 primitives:

1. **Read the source.** Per the predecessor batch's Mode B mandate.
   Confirm the dataclass fields and Optional/required signatures.
   Files (likely paths — confirm at start):
   - `defipy/python/prod/utils/data/PortfolioPosition.py`
   - `defipy/python/prod/primitives/portfolio/AggregatePortfolio.py`
   - `defipy/python/prod/primitives/comparison/CompareProtocols.py`
   - `defipy/python/prod/primitives/execution/CalculateSlippage.py`
2. **Spot-check a test.** Find one test per primitive in
   `python/test/primitives/` confirming the per-protocol input shape
   matches what the spec asserts above.
3. **Insert the inline block.** After `Signature.`, before `Setup` /
   first example.
4. **Build and review.** `make html`, browser-eyeball the new block in
   the existing page flow.

### Item 2 commit pattern

One commit per primitive:

```
docs(agentic_primitives): protocol-specific input shapes for <Primitive>

Adds a structured per-protocol input table after the Signature block
on the <Category> page. Surfaces the dispatcher-shaped primitive's
divergent per-protocol input fields / output behavior, previously
documented only as a single sentence of prose buried in the section.

Verified against <source-file>:<approximate-line> at <branch>.

Part of the Agentic Primitives doc completion batch — see
doc/execution/CLAUDE_CODE_SPEC_agentic_primitives_completion.md.
```

3 commits total for Item 2.

---

## Top-of-batch verification

```bash
cd ~/repos/defipy
git checkout -b docs/agentic-primitives-completion
pytest python/test/ -v 2>&1 | tail -5
```

Expected: 629 passed (per DEFIPY_V2_SHIPPED.md). If different, the spec
still applies — the doc work doesn't depend on test count — but
investigate before assuming the working tree is clean.

```bash
ls doc/source/agentic_primitives/notebooks/
```

Confirm 9 notebook files exist matching the 9 category pages. If the
file extensions are `.rst` rather than `.ipynb`, the markdown-vs-RST
question for Item 1 resolves to RST; if `.ipynb`, the cells are markdown
and tables should be markdown-flavored.

```bash
cd doc && make html 2>&1 | tail -10
```

Baseline build before the batch.

---

## Risk list

**1. Notebook vs RST format ambiguity.** The page sources listed by
RTD are `.ipynb.txt`, suggesting Jupyter notebooks rendered via
nbsphinx. Markdown cells use markdown syntax; RST cells use RST
directives. Confirm at start by reading one existing page's source.
If notebooks, use markdown tables; if RST source files, use
`.. list-table::`.

**2. Empty `Protocol coverage` heading may be a literal empty section
or an artifact.** If the heading is rendered from an existing markdown
cell that's literally just `## Protocol coverage` with nothing after,
add content to that cell. If it's auto-generated from a notebook
metadata structure, you may need to add a new cell instead. The cell
inspection during step 1 of Item 1 resolves this.

**3. The MCP tool exposure section provides good per-page content
patterning.** Read the existing `MCP tool exposure` section on each
page before writing the `Protocol coverage` content — they're the
neighbor section, and matching their tone (short, direct, naming the
architectural reason rather than just the surface fact) will keep
voice consistent across the page.

**4. Source-read may surface dataclass-field mismatches.** The
`PortfolioPosition` field list in this spec is reconstructed from
PROJECT_CONTEXT excerpts and the live RTD example. If the actual
dataclass differs (e.g., `entry_amounts` is also Optional on V2/V3
positions, or `holding_period_days` lives on `PortfolioPosition` and
not just per-position-summary), correct the table inline. The spec
captures the structure; the source captures the truth.

**5. Heuristic #6 reminder ("name fields for information, not
verdicts").** The `CompareProtocols` table above uses ✅ / ⚠ / ❌ for
output-population status. This is descriptive (always populated /
sometimes populated / never populated), not evaluative ("good / bad").
If the inline rendering of these glyphs looks alarming or judgmental
in the rendered theme, swap to "Always" / "Sometimes" / "Never" or
"Always" / "Conditional" / "Deferred" without changing the
information content.

**6. Item 2's tables are *more* prescriptive than the Core Primitives
batch's are, because they're inlined into existing pages with existing
voice.** The Core batch had the luxury of writing each page from
scratch with a locked template. This batch has to slot into existing
pages without breaking voice — read the existing primitive section
(intro paragraph, Signature, Setup) before inserting the new block,
to make sure the inserted prose connects rather than reads as a
parachuted-in addition.

---

## Out of scope (file but don't expand)

If during execution you spot:

- Tutorial pages with similar protocol-coverage gaps
- Result Dataclasses page (`agentic_result_dataclasses.html`) lacking
  per-protocol shape notes for the dispatcher dataclasses
  (`PortfolioPosition`, `ProtocolCandidate`, `FeeTierCandidate`)
- The `defipy.tools` reference page lacking per-tool MCP-exposure
  notes that reflect the Item 1 protocol-coverage tables

**File these to** `doc/execution/V2_FOLLOWUPS.md`. Don't address inline.

---

## Definition of done

- [ ] Branch `docs/agentic-primitives-completion` exists and contains
      12 commits (9 for Item 1 category pages + 3 for Item 2 dispatcher
      primitives)
- [ ] `make html` builds cleanly with no new warnings introduced by
      this batch
- [ ] All 9 category pages have populated `Protocol coverage` sections
      following the locked format (3 columns: Protocol / Coverage /
      Notes) with the 4-value Coverage vocabulary
- [ ] All 3 dispatcher primitives (`AggregatePortfolio`,
      `CompareProtocols`, `CalculateSlippage`) have an inline
      `Protocol-specific input shapes` block after their `Signature`
      section
- [ ] Each per-page commit names the source file(s) and/or planning-doc
      excerpt(s) the content was lifted from in the commit message
- [ ] Branch pushed; RTD PR-preview build green; preview URL eyeballed
      for visual regressions vs main
- [ ] Followups (if any) filed to V2_FOLLOWUPS.md
- [ ] PR opened against main with a description that:
  - Names the predecessor (Core Primitives batch) and the architectural
    distinction (sibling pattern doesn't have the Join problem; only
    dispatcher primitives need the Core template applied)
  - Names the audit finding (9 empty `Protocol coverage` sections, 3
    dispatcher primitives needing the inline-template treatment)
  - Confirms scope held: no new pages, no IA changes, no rewrites of
    existing sibling-primitive sections, no Core re-touches

---

## Appendix — Why this spec is shorter than the Core Primitives one

The Core batch wrote 7 pages from scratch using a single template; the
template needed full specification because page 5 had to look like page 1.

This batch slots into 9 existing pages and 3 existing primitive
sections. The template is already locked (Core Primitives batch
defined it; this batch is a smaller application). The substantive
content for Item 1 is already written — it lives in PROJECT_CONTEXT
and DEFIPY_V2_AGENTIC_PLAN — and this spec just routes the right
excerpts to the right pages. The novel work is Item 2's three inline
blocks, and even those reuse most of the per-protocol vocabulary
established in Item 1.

The half-day estimate reflects the actual delta: 9 transcription tasks
+ 3 source-read-then-table tasks. Not 12 from-scratch authorings.

— end spec —
