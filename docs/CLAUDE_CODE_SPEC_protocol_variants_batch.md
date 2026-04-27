# Claude Code Spec — Core Primitives Protocol-Variants Doc Batch

**Status:** Spec — ready for execution
**Owner:** Claude Code session
**Estimated effort:** ~1 day end-to-end (5-6 pages × ~45-90 min each + integration + RTD build verification)
**Predecessor:** ad-hoc session that produced the `Join` template (`join_protocol_variants_draft.md` in /mnt/user-data/outputs)
**Branch:** `docs/protocol-variants-batch` off whichever working branch is current

---

## TL;DR

The `Join` page on RTD currently describes itself as "Join token amounts to
initialize pool with liquidity" — accurate for V2/V3, *misleading* for
Balancer (takes `pool_shares`) and Stableswap (takes `ampl_coeff`). Same
class of gap exists across the other Core Primitives. This batch fixes it
across the 5 dispatcher operations using a shared "Protocol Variants"
template, validated on `Join` in the predecessor session.

**Deliverable:** 5 new RST pages (one per Core Primitive) + an updated
`core_primitives/index.rst` that links to them. Each page splits parameters
into Common (cross-protocol) and Per-Protocol (V2 / V3 / Balancer /
Stableswap), with verified signatures, runnable examples, and the gotcha
callouts that LLMs and direct-link readers need.

**Out of scope (for this batch):** Agentic Primitives (CalculateSlippage,
CheckPoolHealth, etc.), even though some have protocol-scoped behavior —
file follow-ups but don't expand scope mid-flight.

---

## Why this matters now

v1.x audience was humans reading tutorials end-to-end; a V3 user absorbed
tick parameters in context. v2.0 audience includes LLMs reading tool
schemas as ambient context, LLMs reading reference pages when reasoning
about composition, and developers landing directly on a primitive's page
from search. For all three, "the V3 tutorial covers it" is not a fix.

---

## Mode B is mandatory

**Read the source for each primitive's `apply()` signature in the
appropriate sibling repo before drafting the page.** This is the same
discipline that's served the primitive work since session 2026-04-18 —
DEFIPY_V2_AGENTIC_PLAN's success was largely from up-front source reads.

For each primitive, before drafting:

1. Locate the dispatch in the relevant sibling repo (most live in
   `uniswappy/python/prod/process/` since `defipy` re-exports them; some
   may have wrappers in `defipy/python/prod/process/`)
2. Read the `apply()` method signature line-by-line for **all four**
   protocol branches (V2, V3, Balancer, Stableswap) — note required vs
   optional vs ignored parameters per branch
3. Spot-check at least one test from `python/test/primitives/conftest.py`
   or a test using the primitive to confirm the in-the-wild call shape
   matches the source
4. If the primitive doesn't support all four protocols (e.g., `SwapDeposit`
   is V2/V3-only per the availability matrix on `core_primitives/index.rst`),
   note which protocols are skipped and *why* — read the dispatch
   error path so the page can quote the actual error message

A signature surprise during drafting (like the Balancer/Stableswap `Join`
non-token-amount finding) is the **expected** outcome of this read pass —
it's why we read first instead of extrapolating from `Join`.

---

## Verified scope (from current RTD)

The Core Primitives availability matrix at
`https://defipy.readthedocs.io/en/latest/core_primitives/index.html`:

| Operation | V2 | V3 | Balancer | Stableswap |
|---|---|---|---|---|
| `Join()` | ✅ | ✅ | ✅ | ✅ |
| `Swap()` | ✅ | ✅ | ✅ | ✅ |
| `AddLiquidity()` | ✅ | ✅ | ✅ | ✅ |
| `RemoveLiquidity()` | ✅ | ✅ | ✅ | ✅ |
| `SwapDeposit()` | ✅ | ✅ | ❌ | ❌ |
| `WithdrawSwap()` | ✅ | ✅ | ❌ | ❌ |
| `LPQuote()` | ✅ | ✅ | 🔜 | 🔜 |

Pages to produce in this batch (in execution order):

1. `Join` — already drafted, port from `/mnt/user-data/outputs/join_protocol_variants_draft.md`, convert to RST, integrate
2. `Swap` — highest traffic among remaining; tests "common-then-divergent" pattern again
3. `AddLiquidity` + `RemoveLiquidity` — paired pass; they mirror each other
4. `SwapDeposit` + `WithdrawSwap` — paired; **V2/V3-only**, validates template handles partial coverage
5. `LPQuote` — modified template (per-mode rather than per-action; read-only with three call modes)

Note `Join` is page 1 in the integration order even though it was drafted
first — the RST conversion still needs to happen, and it needs to be
integrated into the sidebar at the same time as the others.

---

## File layout

Pages live under `doc/source/core_primitives/` (or wherever the existing
`core_primitives/index.rst` source lives — confirm at start). One file per
primitive:

```
doc/source/core_primitives/
├── index.rst                  # existing — UPDATE to link to new pages
├── join.rst                   # NEW
├── swap.rst                   # NEW
├── add_liquidity.rst          # NEW
├── remove_liquidity.rst       # NEW
├── swap_deposit.rst           # NEW
├── withdraw_swap.rst          # NEW
└── lp_quote.rst               # NEW
```

The existing `index.rst` becomes a category overview that lists each
primitive with a one-liner and links to its dedicated page. Keep the
availability matrix on the index page — it's a useful at-a-glance summary
that the per-primitive pages expand.

---

## Template (locked from predecessor session)

The `Join` page in `/mnt/user-data/outputs/join_protocol_variants_draft.md`
is the canonical template. Every page in this batch follows the same
section order:

1. **One-paragraph hook** — what the primitive is, mutating-vs-read pinned,
   cross-link to The Primitive Contract page if relevant
2. **"When to use X vs Y" callout (when applicable)** — resolves the silent
   "did I pick the right primitive?" question (e.g., Join vs AddLiquidity,
   AddLiquidity vs SwapDeposit, RemoveLiquidity vs WithdrawSwap)
3. **Signature at a glance** — table with one-line `apply()` signature per
   protocol; LLM-friendly summary, scannable in a single glance
4. **Common parameters table** — `lp` and any other parameters identical
   across all protocols
5. **Protocol Variants** — one subsection per supported protocol
   (V2 / V3 / Balancer / Stableswap), each with:
   - 1-2 sentence framing of what the operation *means* in this protocol
   - Per-protocol parameter table (only the parameters specific to that
     protocol — common ones live in the Common section above)
   - Runnable code example, **lifted from real READMEs / tests / notebooks**
     where possible (no extrapolation)
   - "Common pitfall" or "Why this is different" callout where there's a
     non-obvious gotcha (e.g., V3 tick alignment, Balancer's vault-funded-
     before-Join, Stableswap's immutable A)
6. **How X interacts with the rest of the pipeline** — small "ecosystem"
   footer giving direct-landing readers context they'd miss without it
7. **See also** — links to related primitives, helper utilities, tutorials,
   and (when read-only is the analogous primitive) The Primitive Contract

For primitives that don't support all four protocols (`SwapDeposit`,
`WithdrawSwap`, `LPQuote`), the omitted protocols get a single line in the
Protocol Variants section explaining *why* that protocol is excluded
(architectural reason, not just "not implemented") with a forward-looking
note for `LPQuote` Balancer/Stableswap support which is 🔜 per the matrix.

### LPQuote modification

LPQuote is read-only with three call modes (token price; LP→token; token→LP).
Its Protocol Variants section organizes by **call mode first, then protocol
inside each mode**, rather than the per-protocol-first structure of the
mutating primitives. The signature-at-a-glance table has 3 rows (one per
mode) × 4 columns (one per protocol). Same Common-vs-per-mode parameter
split otherwise.

---

## Per-primitive notes

### 1. Join (already drafted)

**Source:** `/mnt/user-data/outputs/join_protocol_variants_draft.md` ✅

**Action:**
- Convert MD → RST (Sphinx-flavored; preserve all gotcha callouts using
  `.. note::` and `.. warning::` directives)
- Code blocks: `.. code-block:: python`
- Cross-references: convert MD links to `:doc:` and `:ref:` as appropriate
- Verify the four code examples still compile mentally against current
  source — no signature drift since the draft was written

**Verified-key facts to preserve:**
- V2: `Join().apply(lp, user_nm, amount0, amount1)`
- V3: `Join().apply(lp, user_nm, amount0, amount1, lwr_tick, upr_tick)` —
  **ticks required, not optional**, must be `tick_spacing`-aligned
- Balancer: `Join().apply(lp, user_nm, pool_shares)` — **no token amounts**;
  vault funded separately via `vault.add_token(token, weight)` after
  `token.deposit(...)`
- Stableswap: `Join().apply(lp, user_nm, ampl_coeff)` — **no token amounts**;
  vault funded separately; A is immutable post-Join in this implementation

### 2. Swap

**Source read:**
- `uniswappy/python/prod/process/swap/Swap.py` (or wherever the dispatch lives)
- Confirm V2/V3 parameter order: `apply(lp, token_in, user_nm, amount_in)`
  (per Medium article example: `Swap().apply(lp, dai, user_nm, 1000)`)
- Confirm Balancer signature: search README excerpt shows
  `swap.apply(lp, dai, usdc, "user", 10)` — **takes both token_in AND token_out**
  because Balancer is multi-asset and the pool may have N>2 tokens; this is
  divergent from V2/V3
- Confirm Stableswap signature: similar to Balancer
  (`swap.apply(lp, dai, usdc, "user", 10)`) — same multi-asset dispatch
- Note: Balancer also has `Swap(Proc.SWAPIN)` constructor mode visible in
  search results — investigate; this may be a dispatcher-vs-proc distinction
  worth surfacing on the page

**Likely "When to use" callouts:**
- Swap vs SwapDeposit — Swap is just the trade; SwapDeposit does swap + deposit
  in one shot to LP into a pool with single-sided input

**Pitfalls likely worth callouts:**
- V2/V3: token order in arguments determines direction (token_in is what
  *you* hand over)
- Balancer/Stableswap: must specify both token_in and token_out because
  the pool may have more than two tokens
- Slippage / price impact is a function of trade size relative to reserves
  (if not already on the page) — link to `CalculateSlippage` for analysis

### 3. AddLiquidity

**Source read:**
- The cross-protocol dispatcher's `apply()` method
- Per current index.rst description: V2/V3 enter one token, the other is
  calculated for 50/50; Balancer/Stableswap enter one token (single-sided
  add)
- **Confirm whether V2/V3 takes one or both token amounts** — the description
  says "enter one token and the other amount is calculated", so the
  signature is likely `apply(lp, token, user_nm, amount, ...)` where `token`
  identifies which side and `amount` is the amount of that side
- For V3, ticks are likely required (same as Join)
- For Balancer, single-token-in semantics — confirm shape

**Likely "When to use" callouts:**
- Join vs AddLiquidity — first mint vs subsequent mint (exact text from Join
  page; reuse so they're consistent across both pages)
- AddLiquidity vs SwapDeposit — AddLiquidity needs 50/50 already (V2/V3) or
  single token (Bal/Ssw); SwapDeposit handles the swap-to-balance internally

### 4. RemoveLiquidity

**Source read:**
- Same dispatcher pattern
- Per current index.rst: V2/V3 calculate the other side; Balancer/Stableswap
  enter one token
- **Confirm whether the input is "amount of LP tokens to burn" or "amount of
  one of the underlying tokens to receive"** — the index page wording is
  ambiguous on this; only source read settles it
- For V3, ticks are likely required (must specify which range to withdraw from)

**Likely "When to use" callouts:**
- RemoveLiquidity vs WithdrawSwap — RemoveLiquidity gives you both tokens
  in pool ratio; WithdrawSwap converts back to a single specified token

### 5. SwapDeposit (V2/V3-only)

**Source read:**
- `SwapDeposit.apply()` and `SwapDeposit._calc_univ2_deposit_portion()`
  (the latter is private but is the math heart that `OptimalDepositSplit`
  composes against — note this in the "See also" pointing at
  `OptimalDepositSplit` as the non-mutating projection)
- Confirm V3 signature includes ticks
- Confirm Balancer/Stableswap dispatch raises a clean error or simply isn't
  routed; quote the actual error / behavior on the page in the per-protocol
  "Why this protocol isn't supported" sections

**Likely "When to use" callouts:**
- SwapDeposit vs (Swap + AddLiquidity) — convenience for single-tx zap-in;
  closed-form optimal swap fraction handled internally
- SwapDeposit vs OptimalDepositSplit — execution vs non-mutating projection;
  pair them when you want to preview before executing

**Why no Balancer/Stableswap section:**
- Balancer/Stableswap already accept single-sided adds via `AddLiquidity`
  with one token specified; the swap-then-deposit pattern that
  `SwapDeposit` solves for V2/V3 (where `AddLiquidity` requires balanced
  amounts) doesn't apply because the underlying pool math handles the
  imbalanced case directly
- State this architectural reason on the page; don't just say "not
  implemented"

### 6. WithdrawSwap (V2/V3-only)

**Source read:**
- `WithdrawSwap.apply()` and any helper methods
- V3: confirm tick requirement (per the search-result notebook excerpt:
  `WithdrawSwap().apply(lp, dai, user_nm, 1000, lwr_tick, upr_tick)`)

**Why no Balancer/Stableswap section:**
- Symmetric to SwapDeposit's exclusion: Balancer/Stableswap support
  single-token withdrawals via `RemoveLiquidity` directly because the pool
  math doesn't require balanced removal

### 7. LPQuote

**Modified template** — see "LPQuote modification" note above. The Protocol
Variants section organizes by call mode first, protocol second.

**Source read:**
- `LPQuote(...)` constructor — the boolean argument controls fee/no-fee or
  similar dispatch (see PROJECT_CONTEXT.md "Paper value vs settlement value"
  for context — `LPQuote(False)` returns settlement value via internal
  RebaseIndexToken swap, scale-dependent and crashes with ZeroDivisionError
  on V3 at 100% pool ownership)
- `LPQuote.get_amount(lp, token, amount_in, lwr, upr)` — the V3-friendly
  alternative to `lp.get_amount_out` per Key Internal Conventions
- `LPQuote.get_reserve(lp, token, lwr, upr)` — the V3-friendly alternative
  to `lp.get_reserve` per Key Internal Conventions
- The three "modes" mentioned in the current index.rst description:
  (a) token price; (b) LP token amount → token amount;
  (c) token amount → LP token amount

**Critical content for the page** (lift from PROJECT_CONTEXT.md "Key
Internal Conventions"):
- "LPQuote is the nucleus of the package" framing — every meaningful
  cross-protocol operation routes through it
- The polymorphism gotcha: `lp.get_amount_out` and `lp.get_reserve` are
  V2-specific and fail on V3 with AttributeError; `LPQuote` dispatches
  correctly. **This is the page to surface this loud and clear** — it's
  the primary reason a v2 reader needs to choose `LPQuote` over direct
  `lp.*` calls
- Paper-value vs settlement-value distinction
- The `[chain]` extra forward-looking note that LPQuote will work the
  same way against `LiveProvider`-built twins once v2.1 ships

**Why Balancer/Stableswap is 🔜 not ❌:**
- Per the matrix on the index page, the architectural support is intended
  but not yet wired through. State that v2.1 is the expected landing for
  full LPQuote cross-protocol support and that the API shape will not
  break (add-only)

---

## RST conversion notes

The team uses Sphinx with what appears to be the Read the Docs theme
(per the live RTD output). Specific conversion guidance for the MD draft:

| Markdown | RST equivalent |
|---|---|
| `# Heading` | `=========` underline (with title) |
| `## Heading` | `---------` underline |
| `### Heading` | `^^^^^^^^^` underline |
| `> **Note.** Text` | `.. note::\n\n   Text` |
| `> **Warning.** Text` | `.. warning::` |
| ` ```python ` | `.. code-block:: python` |
| `**bold**` | `**bold**` (same) |
| `` `code` `` | `` `code` `` (same — but inline) |
| `[text](url)` | external: `` `text <url>`_ `` |
| `[text](#anchor)` | internal: `:ref:`anchor`` or `:doc:`/path`` |
| Tables | RST grid tables or list-tables (preferred for editing — `.. list-table::`) |

Tables in this batch are non-trivial (parameter tables, signature-at-a-glance,
availability matrix). **Use `.. list-table::` directive** — easier to edit
than grid tables and renders identically in the RTD theme.

Cross-references between the new pages and existing ones:
- Use `:doc:` for whole-page links: `:doc:`/primitive_contract``
- Use `:ref:` for anchored links if explicit labels exist
- For primitive-page-to-primitive-page links within `core_primitives/`,
  use relative paths: `:doc:`add_liquidity``

---

## Index page update

`doc/source/core_primitives/index.rst` currently has:
- Intro paragraph (keep)
- Availability matrix (keep — still useful as the at-a-glance entry point)
- One-line operation descriptions (REPLACE with one-liner + link to the
  new dedicated page)
- "Relationship to other sections" (keep)

New shape for the operation descriptions section:

```rst
**Operation pages**

.. toctree::
   :maxdepth: 1

   join
   swap
   add_liquidity
   remove_liquidity
   swap_deposit
   withdraw_swap
   lp_quote

* :doc:`join` — initialize a pool with starting liquidity (V2/V3 takes
  token amounts; Balancer takes pool shares; Stableswap takes amplification
  coefficient).
* :doc:`swap` — exchange one token for another at the pool's current price.
* :doc:`add_liquidity` — contribute to an already-initialized pool.
* :doc:`remove_liquidity` — withdraw from a pool, receiving both tokens
  in pool ratio.
* :doc:`swap_deposit` — single-sided deposit (V2/V3 only); zap one token
  into a balanced LP position.
* :doc:`withdraw_swap` — single-sided withdrawal (V2/V3 only); exit a
  position into a single specified token.
* :doc:`lp_quote` — read-only price and conversion queries; the
  recommended cross-protocol entry point for state reads.
```

Update the **first sentence** of each one-liner so it captures the
protocol-divergent shape — not just the V2/V3 framing currently in the
descriptions. The `Join` example above models the right tone.

---

## Top-of-batch verification

Before drafting any pages:

```bash
cd ~/repos/defipy
git checkout -b docs/protocol-variants-batch
pytest python/test/primitives/ -v 2>&1 | tail -5
```

Expected: 504 passed (or current branch's equivalent — DEFIPY_V2_SHIPPED.md
records 629 passing across the full v2 suite). If tests fail, stop and
investigate before writing docs against an unstable working tree.

```bash
ls doc/source/core_primitives/
cat doc/source/core_primitives/index.rst
```

Confirm the path layout matches what this spec assumes; adjust paths in
the spec if the source layout differs (this is a documentation file
location, not a code-change concern).

```bash
cd doc && make html 2>&1 | tail -20
```

Build the existing docs to confirm Sphinx is wired correctly; baseline
the warning count so additions can be evaluated against it.

---

## Per-page execution rhythm

For each of the 5 remaining pages (after Join is ported):

1. **Read the source** — ~10 minutes. Open the relevant
   `process/<primitive>/...` files in uniswappy / balancerpy / stableswappy.
   Note the actual signatures for each protocol branch.
2. **Spot-check a test** — ~5 minutes. Confirm the in-the-wild call shape
   matches what you read. Find a test under `python/test/primitives/` that
   uses the primitive against the relevant fixture.
3. **Draft the RST page** — ~30-60 minutes depending on complexity.
   Follow the locked template section order. Lift code examples from
   READMEs / tests / notebooks where possible.
4. **Local Sphinx build** — ~2 minutes. Run `make html` from `doc/`,
   resolve any RST warnings/errors (broken refs, malformed directives).
5. **Read the rendered page** — ~5 minutes. Open the local HTML in a
   browser. Look for: do the tables render correctly; do the callouts
   look right; does the page read cleanly when seen in the rendered RTD
   theme rather than as RST source.
6. **Commit** — small commits per page, not one giant batch commit. Commit
   message pattern:

```
docs(core_primitives): protocol-variants page for <Primitive>

Adds doc/source/core_primitives/<primitive>.rst with
Common-vs-Per-Protocol parameter splits, protocol-specific examples,
and gotcha callouts. Verified against
<sibling_repo>/python/prod/process/<file>.py at <short-sha-or-version>.

Part of the protocol-variants batch — see
doc/execution/CLAUDE_CODE_SPEC_protocol_variants_batch.md.
```

Sequence as before: Join → Swap → AddLiquidity → RemoveLiquidity →
SwapDeposit → WithdrawSwap → LPQuote → index update.

The index update is the **last** commit in the batch — that way the
sidebar links don't 404 against unmerged pages if anyone happens to
build mid-sequence.

---

## Risk list

**1. RST table cross-references resolve at build time, not draft time.**
Easy to commit a page with `:doc:`add_liquidity`` referencing a sibling
page that doesn't exist yet in the same commit. Mitigation: build after
each commit; add the `add_liquidity` page before any page references it.
The execution sequence above already accounts for this.

**2. Sphinx may flag "document isn't included in any toctree" for new
pages until the index update lands.** This is expected during the batch
and resolves at the final commit. Don't suppress the warning globally —
it's the correct signal.

**3. Source signature surprises.** Expected. The Balancer/Stableswap
finding for `Join` is the canonical case. If you find another, **note it
in the page directly** — that's the whole point of the batch. The page
is more valuable for naming the surprise than for being a clean
restatement of what users already think they know.

**4. Test fixtures for non-V2/V3 protocols may have non-obvious setup.**
Per PROJECT_CONTEXT.md the conftest exposes `balancer_setup`,
`stableswap_setup`, `weighted_balancer_setup`, `amplified_stableswap_setup`
factory fixtures. If you need to construct a pool inline for an example,
mirror the conftest pattern rather than inventing a new shape.

**5. The Sphinx theme used by RTD may not be Furo as suggested in the
v2 plan — the live site appears to use the standard `sphinx_rtd_theme`.**
Don't change the theme as part of this batch; the spec is doc-content-only.
The protocol-variants pages should render acceptably in either theme.

**6. RTD build environment vs. local build environment.** Local `make
html` may succeed while RTD's build fails (different Python versions,
sibling-package availability, etc.). Push the branch before merging; let
RTD's PR-preview build run; eyeball the rendered output on the preview
URL before merging.

---

## Out of scope (file but don't expand)

If during execution you spot:

- Agentic Primitive pages with similar protocol-variant gaps (e.g.,
  `CalculateSlippage` documenting V2/V3 only without naming the protocol
  scope; `CheckPoolHealth` not surfacing the V2-only `num_swaps`)
- Tutorial pages whose protocol-variant treatment lags the new reference
  pages (the `Join` tutorial shows V3 with ticks but doesn't frame it as
  "the V3 variant")
- Cross-references in `agentic_primitives/` that point at the old
  `core_primitives/index.rst` description and need to point at the new
  per-primitive pages

**File these to** `doc/execution/V2_FOLLOWUPS.md` (or wherever the
followups list lives — confirm path at start; PROJECT_CONTEXT.md
references it). Don't address inline. Phase 2 / v2.1 catches them.

---

## Definition of done

- [ ] Branch `docs/protocol-variants-batch` exists and contains 7 commits
      (one per page + one for the index update)
- [ ] `make html` builds cleanly with no new RST errors (warnings count
      acceptable if the only new warnings are pre-existing-style issues
      not introduced by this batch)
- [ ] All 7 new pages render correctly in the local browser preview:
      tables format, callouts render, code blocks have syntax highlighting,
      cross-references resolve
- [ ] Index page `core_primitives/index.rst` has the toctree referencing
      all 7 new pages
- [ ] Each per-page commit names the source file(s) read for verification
      in the commit message
- [ ] Branch pushed; RTD PR-preview build green; preview URL eyeballed for
      visual regressions vs main
- [ ] Followups (if any) filed to V2_FOLLOWUPS.md with brief context — not
      addressed inline
- [ ] PR opened against main with a description that:
  - Names the predecessor session (the `Join` template draft)
  - Names the architectural reasoning (LLM/direct-link audience needs
    protocol parameters at the reference page, not buried in tutorials)
  - Names the Balancer/Stableswap finding for `Join` and any other
    surprises uncovered during execution as the substantive content of
    the batch (these are the bugs being fixed, not just polish)
  - Lists each new page with a one-line description
  - Confirms scope held: 7 pages + index update; no Agentic Primitive
    work; no tutorial rewrites

---

## Appendix A — Reference materials

In execution order, the documents to consult:

1. **`/mnt/user-data/outputs/join_protocol_variants_draft.md`** — locked
   template; canonical example of the Join page in MD form
2. **`PROJECT_CONTEXT.md`** in the repo root or `doc/` — Key Internal
   Conventions section captures the V2-vs-V3 polymorphism gotchas,
   numeraire conventions, V3 tick alignment notes, paper-vs-settlement
   value distinction
3. **`DEFIPY_V2_AGENTIC_PLAN.md`** — frame for why v2.0 reference pages
   matter more than v1.x ones (LLM audience, MCP tool schemas, direct-
   link traffic)
4. **`DEFIPY_V2_SHIPPED.md`** — the curated 10-primitive v2.0 MCP tool
   set lives in `defipy/python/prod/tools/registry.py`; useful when
   writing the "this primitive is part of the v2.0 MCP tool set" cross-
   reference notes (which curated primitives are exposed as MCP tools is
   a small but useful signal for readers wondering which primitives an
   LLM would auto-pick)
5. **Live RTD pages** under `https://defipy.readthedocs.io/en/latest/`
   for the existing `core_primitives/index` and `abstract_uniswap` pages
   — read both to understand the current voice and the existing breakage

---

## Appendix B — Why the spec is this prescriptive

The predecessor session validated that the template works for `Join` by
producing a draft that was already useful as documentation, with clear
gotcha-callouts that don't appear anywhere else in the docs. The risk in
batching out is template drift — page 5 looks substantively different
from page 1, and the consistency that makes the batch useful is lost.

This spec locks the template in §"Template" and the per-primitive
intelligence in §"Per-primitive notes", so each page is a fill-in
rather than a redesign. Source-read first, draft against the locked
template, integrate, move on.

The "What this should feel like" rhythm: page 5 should take less time
than page 2, not more, because the only thing changing per page is the
substance of what the source code actually says.

— end spec —
