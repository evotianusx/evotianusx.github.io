import { defineConfig, passthroughImageService } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from "@astrojs/tailwind";
import starlightThemeRapide from 'starlight-theme-rapide'
import svelte from '@astrojs/svelte';
// https://astro.build/config
export default defineConfig({
  site: 'https://evotianusx.github.io',
  image: {
    service: passthroughImageService(),
  },
  integrations: [
    svelte(),
    starlight({
    title: 'Evotianus Page',
    plugins: [starlightThemeRapide()],
    head: [{
      tag: 'script',
      attrs: {
        src: 'https://scripts.withcabin.com/hello.js',
        defer: true,
        async: true
      }
    }]
    ,
    logo:
      { src: './src/assets/logo.svg' },
    customCss: [
      // Path to your Tailwind base styles:
      './src/tailwind.css',
    ],
    social: {
      github: 'https://github.com/evotianusx',
      linkedin: 'https://www.linkedin.com/in/evotianusb'
    },
    sidebar: [{
      label: 'Home',
      link: '/'
    }, {
      label: 'Resume',
      link: '/resume'
    },
    {
      label: 'Projects',
      autogenerate: {
        directory: 'projects'
      }
    },{
      label:"Tools",
      autogenerate:{
        directory:'tools'
      }
    }]
  }), tailwind({
    // Disable the default base styles:
    applyBaseStyles: false,
  })]
});