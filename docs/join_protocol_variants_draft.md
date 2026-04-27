# Join

Initialize a pool with starting liquidity. `Join` is a **mutating** dispatch
primitive — it routes to the protocol-specific mint operation underneath the
unified interface.

> **When to use `Join` vs `AddLiquidity`** — use `Join` to seed an empty pool
> (first mint, sets the initial reserves and price). Use `AddLiquidity` to
> contribute to a pool that already has liquidity. Calling `Join` on a
> non-empty pool is undefined behavior; calling `AddLiquidity` on an empty
> pool will fail because there is no price to match.

## Signature at a glance

The `apply()` signature varies by protocol because the *meaning* of pool
initialization varies by protocol. The first three parameters are common
across all four; the trailing parameters are protocol-specific.

| Protocol | Required signature |
|---|---|
| Uniswap V2 | `Join().apply(lp, user_nm, amount0, amount1)` |
| Uniswap V3 | `Join().apply(lp, user_nm, amount0, amount1, lwr_tick, upr_tick)` |
| Balancer | `Join().apply(lp, user_nm, pool_shares)` |
| Stableswap | `Join().apply(lp, user_nm, ampl_coeff)` |

**Common parameters** (all protocols)

| Parameter | Type | Description |
|---|---|---|
| `lp` | `Exchange` | Pool object returned by `factory.deploy(...)`. Must be empty (no prior `Join`). |
| `user_nm` | `str` | Account name receiving the LP credit for this initialization. |

The remaining parameters depend on what initialization *means* for the
protocol — see the per-protocol sections below.

## Protocol Variants

### Uniswap V2

Two-sided deposit at the pool's natural price. The two amounts you pass
**define** the initial price ratio; subsequent traders observe `price = y/x`
based on what you seeded.

| Parameter | Type | Notes |
|---|---|---|
| `amount0` | `float` | Amount of `tkn0` (the first token from `UniswapExchangeData`). |
| `amount1` | `float` | Amount of `tkn1`. The ratio `amount1/amount0` becomes the initial price. |

```python
from uniswappy import (
    ERC20, UniswapExchangeData, UniswapFactory, Join,
)

eth = ERC20("ETH", "0x09")
tkn = ERC20("TKN", "0x111")
exch_data = UniswapExchangeData(
    tkn0=eth, tkn1=tkn, symbol="LP", address="0x011",
)
factory = UniswapFactory("ETH pool factory", "0x2")
lp = factory.deploy(exch_data)

Join().apply(lp, "user", 1000, 100000)
# Initial price: 100 TKN per ETH
```

### Uniswap V3

Two-sided deposit into a **specific tick range**. Concentrated liquidity has
no meaning without a range, so V3 requires `lwr_tick` and `upr_tick` in
addition to the two amounts. For a position equivalent to V2's full-range
behavior, use `UniV3Utils.getMinTick(tick_spacing)` and
`getMaxTick(tick_spacing)`.

| Parameter | Type | Notes |
|---|---|---|
| `amount0` | `float` | Amount of `tkn0`. |
| `amount1` | `float` | Amount of `tkn1`. Sets the initial price; subsequent in-range trades use this as the spot reference. |
| `lwr_tick` | `int` | Lower tick of the range. Must be a multiple of `tick_spacing`. |
| `upr_tick` | `int` | Upper tick of the range. Must be `> lwr_tick` and a multiple of `tick_spacing`. |

```python
from uniswappy import (
    ERC20, UniswapExchangeData, UniswapFactory, Join, UniV3Utils,
)

eth = ERC20("ETH", "0x09")
tkn = ERC20("TKN", "0x111")
tick_spacing = 60
fee = 3000

exch_data = UniswapExchangeData(
    tkn0=eth, tkn1=tkn, symbol="LP", address="0x011",
    version="V3", tick_spacing=tick_spacing, fee=fee,
)
factory = UniswapFactory("ETH pool factory", "0x2")
lp = factory.deploy(exch_data)

lwr_tick = UniV3Utils.getMinTick(tick_spacing)
upr_tick = UniV3Utils.getMaxTick(tick_spacing)

Join().apply(lp, "user", 1000, 100000, lwr_tick, upr_tick)
# Full-range V3 position; behaves analogously to V2 within the range
```

> **Common pitfall.** `lwr_tick` and `upr_tick` are **required** for V3, not
> optional. Omitting them does not silently produce a full-range position;
> it raises an error. The values must also be tick-aligned to the pool's
> `tick_spacing` (60 for the 30-bps fee tier, 10 for 5-bps, 200 for 100-bps).

### Balancer

Pool shares-based initialization. Token amounts are **already loaded into the
vault** before `Join` is called — `Join` issues the initial pool-share supply
against those vault balances. The single positional argument is the number of
pool shares to mint, not a token amount.

| Parameter | Type | Notes |
|---|---|---|
| `pool_shares` | `float` | Initial pool-share supply minted to `user_nm`. The vault balances divided by `pool_shares` define the per-share token claim. |

```python
from defipy import (
    ERC20, BalancerVault, BalancerExchangeData, BalancerFactory, Join,
)

dai = ERC20("DAI", "0x111")
usdc = ERC20("USDC", "0x999")
dai.deposit(None, 10000)
usdc.deposit(None, 20000)

vault = BalancerVault()
vault.add_token(dai, 10)   # denormalized weight
vault.add_token(usdc, 40)  # denormalized weight

exch_data = BalancerExchangeData(vault=vault, symbol="BSP", address="0x3")
factory = BalancerFactory("pool factory", "0x2")
lp = factory.deploy(exch_data)

Join().apply(lp, "user", 100)
# 100 pool shares minted to "user"; per-share claim is the vault contents / 100
```

> **Why no token amounts here?** Balancer separates *vault funding* (loading
> tokens via `vault.add_token(token, weight)` after `token.deposit(...)`) from
> *pool initialization* (minting initial shares against the funded vault).
> `Join` performs only the second step. If your vault is empty when you call
> `Join`, you'll get a degenerate pool.

### Stableswap

Amplification-based initialization. Like Balancer, token amounts are loaded
into the vault beforehand. The single positional argument is the **amplification
coefficient** `A` — the parameter that controls how flat the invariant curve
is around the peg.

| Parameter | Type | Notes |
|---|---|---|
| `ampl_coeff` | `int` | Stableswap amplification coefficient. Higher `A` = flatter invariant near peg = lower slippage on small trades but sharper depeg risk past the basin. Typical values: 10 (cautious), 100 (Curve 3pool-class), 2000 (high-amplification stable basket). |

```python
from defipy import (
    ERC20, StableswapVault, StableswapExchangeData,
    StableswapFactory, Join,
)

dai = ERC20("DAI", "0x111", 18)
usdc = ERC20("USDC", "0x222", 6)
dai.deposit(None, 10000)
usdc.deposit(None, 20000)

vault = StableswapVault()
vault.add_token(dai)
vault.add_token(usdc)

exch_data = StableswapExchangeData(vault=vault, symbol="LP", address="0x011")
factory = StableswapFactory("Stableswap factory", "0x2")
lp = factory.deploy(exch_data)

AMPL_COEFF = 2000
Join().apply(lp, "user", AMPL_COEFF)
# Pool initialized at A=2000; LP supply derived from vault balances + invariant
```

> **`A` is fixed at initialization in this implementation.** The on-chain
> Curve contract supports `ramp_A` for governance-controlled amplification
> changes; the DeFiPy stableswap exchange treats `A` as immutable post-`Join`.
> If you need to model an `A` ramp, deploy a fresh pool at the new `A`.

## How `Join` interacts with the rest of the pipeline

After `Join`, the typical pipeline is:

1. **`Join`** — initialize the pool (this primitive).
2. **`Swap`** — exercise the pool with trades to accrue fees / move price.
3. **Analytics** (Agentic Primitives) — `AnalyzePosition`,
   `SimulatePriceMove`, `CheckPoolHealth`, etc. read the pool's state.
4. **`AddLiquidity` / `RemoveLiquidity`** — additional LPs join or exit.
5. **`SwapDeposit` / `WithdrawSwap`** *(V2/V3 only)* — single-sided
   deposit/withdrawal flows.

For full pipeline tutorials by protocol, see the **Tutorials** section in
the sidebar.

## See also

- [`AddLiquidity`](#) — for joining an already-initialized pool
- [`Swap`](#) — for trading against the pool
- [`UniV3Utils`](#) — tick-spacing helpers for V3 ranges
- [Uniswap V3 tutorial](#) — full V3 pipeline including `Join` with a
  custom tick range
- [The Primitive Contract](#) — read-only analytics over the pool `Join`
  produces
