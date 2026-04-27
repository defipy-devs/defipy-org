// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
	site: 'https://defipy.org',
	markdown: {
		remarkPlugins: [remarkMath],
		rehypePlugins: [rehypeKatex],
	},
	integrations: [
		starlight({
			title: 'DeFiPy',
			logo: {
				src: './src/assets/defipy_logo.png',
				replacesTitle: true,
			},
			// Header right-corner icons. Starlight renders these in order, so
			// GitHub stays leftmost and the legacy-docs link sits next to it.
			// `label` is the accessibility text + hover tooltip — visitors who
			// hover see "Legacy Docs (ReadTheDocs)" so the destination is clear.
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/defipy-devs/defipy' },
				{ icon: 'external', label: 'Legacy Docs (ReadTheDocs)', href: 'https://defipy.readthedocs.io/en/latest/' },
			],
			customCss: [
				'./src/styles/custom.css',
				'katex/dist/katex.min.css',
			],
			// Sidebar default-state policy:
			//   Always-open groups: Ecosystem, Getting Started, Concepts, DeFi Math.
			//     These are the "user-guide" surface — landing visitors should see
			//     the full IA at a glance.
			//   Default-collapsed groups: Tutorials, Primitive API, Protocol API,
			//     Roadmap. These are deeper / longer trees that would dominate the
			//     sidebar if always expanded.
			//   Starlight rule: omitting `collapsed` ⇒ open. `collapsed: true` ⇒
			//     starts closed but auto-expands when the user is inside that section.
			sidebar: [
				// Top-level Home — mirrors the RTD sidebar's first entry.
				{ label: 'Home', link: '/' },

				{
					label: 'DeFiPy Ecosystem',
					items: [
						{ label: 'Book', slug: 'ecosystem/book' },
						{ label: 'Courses', slug: 'ecosystem/courses' },
						{ label: 'Hackathons', slug: 'ecosystem/hackathons' },
						{ label: 'Presentations', slug: 'ecosystem/presentations' },
					],
				},

				{
					label: 'Getting Started',
					items: [
						{ label: 'Quick Start', slug: 'quick' },
						{ label: "What's New (v2)", slug: 'quick/whats-new-v2' },
						{ label: 'Installation', slug: 'installation' },
						{ label: 'Legal', slug: 'legal' },
					],
				},

				// Concepts — narrative / explanatory pages. Pairs with the
				// API sections below in the scikit-learn pattern: User Guide
				// (concepts) + API (reference).
				{
					label: 'Concepts',
					items: [
						{ label: 'Core Primitives', slug: 'core-primitives' },
						{ label: 'Agentic Primitives', slug: 'agentic-primitives' },
						{ label: 'The Primitive Contract', slug: 'primitive-contract' },
						{ label: 'Twin Concept', slug: 'twin-concept' },
						{ label: 'Agentic Overview', slug: 'agentic-overview' },
						{ label: 'Tool Schemas', slug: 'agentic-tool-schemas' },
						{ label: 'Binding to Claude', slug: 'binding-to-claude' },
						{ label: 'Binding to Other LLMs', slug: 'binding-to-other-llms' },
						{ label: 'MCP Demo', slug: 'mcp-demo' },
					],
				},

				{
					label: 'DeFi Math',
					items: [
						{ label: 'Uniswap V2 Math', slug: 'math/univ2-math' },
						{ label: 'Uniswap V3 Math', slug: 'math/univ3-math' },
						{ label: 'Balancer Math', slug: 'math/balancer-math' },
						{ label: 'Stableswap Math', slug: 'math/stableswap-math' },
					],
				},

				// Tutorials — collapsed by default. Long protocol-tree under each
				// would dominate the sidebar if always open.
				{
					label: 'Tutorials',
					collapsed: true,
					items: [
						{ label: 'Uniswap V2', autogenerate: { directory: 'tutorials/uniswapv2' } },
						{ label: 'Uniswap V3', autogenerate: { directory: 'tutorials/uniswapv3' } },
						{ label: 'Balancer', autogenerate: { directory: 'tutorials/balancer' } },
						{ label: 'Stableswap', autogenerate: { directory: 'tutorials/stableswap' } },
					],
				},

				// Primitive API — collapsed by default. Full class-tree on the
				// reference side; visitors who want it will click in.
				{
					label: 'Primitive API',
					collapsed: true,
					items: [
						{
							label: 'Core',
							items: [
								{ label: 'Overview', slug: 'api/primitive/core' },
								{ label: 'Join', slug: 'api/primitive/core/join' },
								{ label: 'Swap', slug: 'api/primitive/core/swap' },
								{ label: 'AddLiquidity', slug: 'api/primitive/core/add-liquidity' },
								{ label: 'RemoveLiquidity', slug: 'api/primitive/core/remove-liquidity' },
								{ label: 'SwapDeposit', slug: 'api/primitive/core/swap-deposit' },
								{ label: 'WithdrawSwap', slug: 'api/primitive/core/withdraw-swap' },
								{ label: 'LPQuote', slug: 'api/primitive/core/lp-quote' },
							],
						},
						{
							label: 'Agentic',
							items: [
								{ label: 'Overview', slug: 'api/primitive/agentic' },
								{ label: 'Tools Reference', slug: 'agentic-tools-reference' },
								{ label: 'Twin Reference', slug: 'agentic-twin-reference' },
								{ label: 'Result Dataclasses', slug: 'agentic-result-dataclasses' },
								{ label: 'Categories', autogenerate: { directory: 'agentic-primitives' } },
							],
						},
					],
				},

				// Protocol API — collapsed by default.
				{
					label: 'Protocol API',
					collapsed: true,
					items: [
						{ label: 'Uniswap V2', slug: 'api/protocol/uniswap-v2' },
						{ label: 'Uniswap V3', slug: 'api/protocol/uniswap-v3' },
						{ label: 'Balancer', slug: 'api/protocol/balancer' },
						{ label: 'Stableswap', slug: 'api/protocol/stableswap' },
					],
				},

				{
					label: 'Roadmap & Changelog',
					collapsed: true,
					items: [
						{ label: 'Roadmap', slug: 'roadmap' },
					],
				},
			],
		}),
	],
});
