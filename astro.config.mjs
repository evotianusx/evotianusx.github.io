import { defineConfig, passthroughImageService } from "astro/config";
import starlight from "@astrojs/starlight";
import starlightThemeRapide from "starlight-theme-rapide";
import svelte from "@astrojs/svelte";
import mdx from '@astrojs/mdx';
// https://astro.build/config
export default defineConfig({
  site: "https://evotianusx.github.io",
  image: {
    service: passthroughImageService(),
  },
  integrations: [

    svelte({ extensions: ['.svelte'] }),
    starlight({
      title: "Evotianus Page",
      plugins: [starlightThemeRapide()],
      head: [
        {
          tag: "script",
          attrs: {
            src: "https://scripts.withcabin.com/hello.js",
            defer: true,
            async: true,
          },
        },
      ],
      logo: { src: "./src/assets/logo.svg" },
      customCss: [
        // Path to your Tailwind base styles:
        "./src/tailwind.css",
      ],
      social: [
        {
          label: 'GitHub',
          icon: 'github',
          href: 'https://github.com/evotianusx',
        },
        {
          label: 'LinkedIn',
          icon: 'linkedin',
          href: 'https://www.linkedin.com/in/evotianusb',
        },
      ],
      sidebar: [
        {
          label: "Home",
          link: "/",
        },
        {
          label: "Resume",
          link: "/resume",
        },
        {
          label: "Projects",
          autogenerate: {
            directory: "projects",
          },
        },
        {
          label: "Tools",
          autogenerate: {
            directory: "tools",
          },
        },
      ],
    }),
    mdx(),
  ],
  vite: {
    ssr: {
      noExternal: ['svelte', '@astrojs/svelte'], // Or any other problematic dependencies
    },


  },
});

