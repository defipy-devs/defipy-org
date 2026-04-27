#!/usr/bin/env bash
# Generate one-line stub MDX pages for every slug referenced by the sidebar.
# Stubs are overwritten as real ports land; their purpose is to keep the build
# green between chunks.

set -euo pipefail

DST="src/content/docs"
mkdir -p "$DST/ecosystem" "$DST/quick" "$DST/math" \
	"$DST/agentic-primitives" \
	"$DST/tutorials/uniswapv2" "$DST/tutorials/uniswapv3" \
	"$DST/tutorials/balancer" "$DST/tutorials/stableswap"

write_stub() {
	local path="$1"
	local title="$2"
	# Skip if a real port already exists (size > 200 bytes is a useful heuristic).
	if [ -f "$path" ] && [ "$(wc -c <"$path")" -gt 200 ]; then
		return
	fi
	cat >"$path" <<EOF
---
title: "$title"
description: "Coming soon."
---

This page is being ported. See the [GitHub source](https://github.com/defipy-devs/defipy-docs) in the meantime.
EOF
}

# Landing
write_stub "$DST/index.mdx" "DeFiPy"

# Ecosystem
write_stub "$DST/ecosystem/book.mdx"          "DeFiPy Book"
write_stub "$DST/ecosystem/courses.mdx"       "Courses"
write_stub "$DST/ecosystem/hackathons.mdx"    "Hackathons"
write_stub "$DST/ecosystem/presentations.mdx" "Presentations"

# Getting Started
write_stub "$DST/quick.mdx"                   "Quick Start"
write_stub "$DST/quick/whats-new-v2.mdx"      "What's New (v2)"
write_stub "$DST/installation.mdx"            "Installation"
write_stub "$DST/legal.mdx"                   "Legal"

# Core / Agentic top-level
write_stub "$DST/core-primitives.mdx"             "Core Primitives"
write_stub "$DST/agentic-primitives.mdx"          "Agentic Primitives"
write_stub "$DST/primitive-contract.mdx"          "The Primitive Contract"
write_stub "$DST/agentic-tools-reference.mdx"     "Agentic Tools Reference"
write_stub "$DST/agentic-twin-reference.mdx"      "Agentic Twin Reference"
write_stub "$DST/agentic-result-dataclasses.mdx"  "Agentic Result Dataclasses"
write_stub "$DST/agentic-overview.mdx"            "Agentic Overview"
write_stub "$DST/twin-concept.mdx"                "Twin Concept"
write_stub "$DST/agentic-tool-schemas.mdx"        "Tool Schemas"
write_stub "$DST/binding-to-claude.mdx"           "Binding to Claude"
write_stub "$DST/binding-to-other-llms.mdx"       "Binding to Other LLMs"
write_stub "$DST/mcp-demo.mdx"                    "MCP Demo"

# Math
write_stub "$DST/math/univ2-math.mdx"      "Uniswap V2 Math"
write_stub "$DST/math/univ3-math.mdx"      "Uniswap V3 Math"
write_stub "$DST/math/balancer-math.mdx"   "Balancer Math"
write_stub "$DST/math/stableswap-math.mdx" "Stableswap Math"

# Agentic primitive pages
write_stub "$DST/agentic-primitives/break-even.mdx"        "Break Even"
write_stub "$DST/agentic-primitives/comparison.mdx"        "Comparison"
write_stub "$DST/agentic-primitives/execution.mdx"         "Execution"
write_stub "$DST/agentic-primitives/optimization.mdx"      "Optimization"
write_stub "$DST/agentic-primitives/pool-health.mdx"       "Pool Health"
write_stub "$DST/agentic-primitives/portfolio.mdx"         "Portfolio"
write_stub "$DST/agentic-primitives/position-analysis.mdx" "Position Analysis"
write_stub "$DST/agentic-primitives/price-scenarios.mdx"   "Price Scenarios"
write_stub "$DST/agentic-primitives/risk.mdx"              "Risk"

# Uniswap V2 tutorials
write_stub "$DST/tutorials/uniswapv2/uniswap-v2.mdx"          "Uniswap V2"
write_stub "$DST/tutorials/uniswapv2/imp-loss-v2.mdx"         "Impermanent Loss V2"
write_stub "$DST/tutorials/uniswapv2/swap-deposit.mdx"        "Swap and Deposit"
write_stub "$DST/tutorials/uniswapv2/withdraw-swap.mdx"       "Withdraw and Swap"
write_stub "$DST/tutorials/uniswapv2/indexing-problem.mdx"    "Indexing Problem"
write_stub "$DST/tutorials/uniswapv2/machine-precision.mdx"   "Machine Precision (V2)"
write_stub "$DST/tutorials/uniswapv2/uniswap-simulation.mdx"  "Uniswap Simulation"

# Uniswap V3 tutorials
write_stub "$DST/tutorials/uniswapv3/uniswap-v3.mdx"        "Uniswap V3"
write_stub "$DST/tutorials/uniswapv3/imp-loss-v3.mdx"       "Impermanent Loss V3"
write_stub "$DST/tutorials/uniswapv3/order-book.mdx"        "Order Book"
write_stub "$DST/tutorials/uniswapv3/machine-precision.mdx" "Machine Precision (V3)"

# Balancer tutorials
write_stub "$DST/tutorials/balancer/abstract-balancer-test.mdx"  "Abstract Balancer Test"
write_stub "$DST/tutorials/balancer/primitive-balancer-test.mdx" "Primitive Balancer Test"

# Stableswap tutorials
write_stub "$DST/tutorials/stableswap/abstract-stableswap-test.mdx"  "Abstract Stableswap Test"
write_stub "$DST/tutorials/stableswap/primitive-stableswap-test.mdx" "Primitive Stableswap Test"

# Primitive / Protocol classes
write_stub "$DST/abstract-uniswap.mdx"     "Abstract Uniswap"
write_stub "$DST/primitive-uniswapv2.mdx"  "Primitive Uniswap V2"
write_stub "$DST/primitive-uniswapv3.mdx"  "Primitive Uniswap V3"
write_stub "$DST/primitive-balancer.mdx"   "Primitive Balancer"
write_stub "$DST/primitive-stableswap.mdx" "Primitive Stableswap"

# Roadmap
write_stub "$DST/roadmap.mdx" "Roadmap"

echo "Stubs generated."
