#!/usr/bin/env bash
# Batch-port docs from defipy-docs (Sphinx) to defipy-org (Astro/Starlight).
# Run from the defipy-org repo root.
#
# This script is meant to be edited as you go. Comment out rows you've already
# done, uncomment more as you work through chunks. After each chunk, run:
#     npm run build
# and fix any errors before moving on.

set -euo pipefail

SRC="${SRC:-../defipy-docs/docs}"
DST="src/content/docs"

mkdir -p "$DST/tutorials/uniswapv2"
mkdir -p "$DST/tutorials/uniswapv3"
mkdir -p "$DST/tutorials/balancer"
mkdir -p "$DST/tutorials/stableswap"
mkdir -p "$DST/math"
mkdir -p "$DST/ecosystem"
mkdir -p "$DST/quick"

# ---- Notebooks → MDX --------------------------------------------------

nb() {
    # nb <source-relative-path> <dest-relative-path>
    python tools/nb_to_mdx.py --input "$SRC/$1" --output "$DST/$2"
}

# Math
nb math/univ2_math.ipynb                         math/univ2-math.mdx
nb math/univ3_math.ipynb                         math/univ3-math.mdx

# Uniswap V2 tutorials
nb uniswapv2/tutorials/uniswap_v2.ipynb          tutorials/uniswapv2/uniswap-v2.mdx
nb uniswapv2/tutorials/imp_loss_v2.ipynb         tutorials/uniswapv2/imp-loss-v2.mdx
nb uniswapv2/tutorials/swap_deposit.ipynb        tutorials/uniswapv2/swap-deposit.mdx
nb uniswapv2/tutorials/withdraw_swap.ipynb       tutorials/uniswapv2/withdraw-swap.mdx
nb uniswapv2/tutorials/indexing_problem.ipynb    tutorials/uniswapv2/indexing-problem.mdx
nb uniswapv2/tutorials/machine_precision.ipynb   tutorials/uniswapv2/machine-precision.mdx
nb uniswapv2/tutorials/uniswap_simulation.ipynb  tutorials/uniswapv2/uniswap-simulation.mdx

# Uniswap V3 tutorials
nb uniswapv3/tutorials/uniswap_v3.ipynb          tutorials/uniswapv3/uniswap-v3.mdx
nb uniswapv3/tutorials/imp_loss_v3.ipynb         tutorials/uniswapv3/imp-loss-v3.mdx
nb uniswapv3/tutorials/order_book.ipynb          tutorials/uniswapv3/order-book.mdx
nb uniswapv3/tutorials/machine_precision.ipynb   tutorials/uniswapv3/machine-precision.mdx

# Balancer tutorials
nb balancer/tutorials/abstract_balancer_test.ipynb    tutorials/balancer/abstract-balancer-test.mdx
nb balancer/tutorials/primitive_balancer_test.ipynb   tutorials/balancer/primitive-balancer-test.mdx

# Stableswap tutorials
nb stableswap/tutorials/abstract_stableswap_test.ipynb    tutorials/stableswap/abstract-stableswap-test.mdx
nb stableswap/tutorials/primitive_stableswap_test.ipynb   tutorials/stableswap/primitive-stableswap-test.mdx

# ---- RST → MDX --------------------------------------------------------

rst() {
    python tools/rst_to_mdx.py --input "$SRC/$1" --output "$DST/$2"
}

# Ecosystem
rst ecosystem/book.rst                ecosystem/book.mdx
rst ecosystem/courses.rst             ecosystem/courses.mdx
rst ecosystem/hackathons.rst          ecosystem/hackathons.mdx
rst ecosystem/presentations.rst       ecosystem/presentations.mdx

# Getting Started
rst quick/index.rst                   quick.mdx
rst quick/whats_new_v2.rst            quick/whats-new-v2.mdx
rst installation.rst                  installation.mdx
rst legal.rst                         legal.mdx

# Core / Agentic narrative
rst core_primitives/index.rst         core-primitives.mdx
rst agentic/tool_schemas.rst          agentic-tool-schemas.mdx
rst agentic/binding_to_claude.rst     binding-to-claude.mdx
rst agentic/binding_to_other_llms.rst binding-to-other-llms.mdx
rst agentic/mcp_demo.rst              mcp-demo.mdx

# Math (RST sources)
rst math/balancer_math.rst            math/balancer-math.mdx
rst math/stableswap_math.rst          math/stableswap-math.mdx

# API reference (hand-written RST)
rst abstract_uniswap.rst              abstract-uniswap.mdx
rst primitive_uniswapv2.rst           primitive-uniswapv2.mdx
rst primitive_uniswapv3.rst           primitive-uniswapv3.mdx
rst primitive_balancer.rst            primitive-balancer.mdx
rst primitive_stableswap.rst          primitive-stableswap.mdx

# Roadmap
rst roadmap.rst                       roadmap.mdx

echo
echo "Done. Run: npm run build"
