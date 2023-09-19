/** @type {import('tailwindcss').Config} */
const starlightPlugin = require('@astrojs/starlight-tailwind');
module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {},
	},
	plugins: [starlightPlugin()],
}
