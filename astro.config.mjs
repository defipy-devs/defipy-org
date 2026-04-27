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
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/defipy-devs/defipy' },
			],
			customCss: [
				'./src/styles/custom.css',
				'katex/dist/katex.min.css',
			],
			sidebar: [
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
				{
					label: 'Core Primitives',
					items: [
						{ label: 'Overview', slug: 'core-primitives' },
					],
				},
				{
					label: 'Agentic Primitives',
					items: [
						{ label: 'Overview', slug: 'agentic-primitives' },
						{ label: 'The Primitive Contract', slug: 'primitive-contract' },
						{ label: 'Tools Reference', slug: 'agentic-tools-reference' },
						{ label: 'Twin Reference', slug: 'agentic-twin-reference' },
						{ label: 'Result Dataclasses', slug: 'agentic-result-dataclasses' },
						{ label: 'Primitive Pages', autogenerate: { directory: 'agentic-primitives' } },
					],
				},
				{
					label: 'Agentic DeFi',
					items: [
						{ label: 'Agentic Overview', slug: 'agentic-overview' },
						{ label: 'Twin Concept', slug: 'twin-concept' },
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
				{
					label: 'Tutorials',
					items: [
						{ label: 'Uniswap V2', autogenerate: { directory: 'tutorials/uniswapv2' } },
						{ label: 'Uniswap V3', autogenerate: { directory: 'tutorials/uniswapv3' } },
						{ label: 'Balancer', autogenerate: { directory: 'tutorials/balancer' } },
						{ label: 'Stableswap', autogenerate: { directory: 'tutorials/stableswap' } },
					],
				},
				{
					label: 'Primitive Classes',
					items: [
						{ label: 'Abstract Uniswap', slug: 'abstract-uniswap' },
					],
				},
				{
					label: 'Protocol Classes',
					items: [
						{ label: 'Primitive Uniswap V2', slug: 'primitive-uniswapv2' },
						{ label: 'Primitive Uniswap V3', slug: 'primitive-uniswapv3' },
						{ label: 'Primitive Balancer', slug: 'primitive-balancer' },
						{ label: 'Primitive Stableswap', slug: 'primitive-stableswap' },
					],
				},
				{
					label: 'Roadmap & Changelog',
					items: [
						{ label: 'Roadmap', slug: 'roadmap' },
					],
				},
			],
		}),
	],
});
