import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  site: 'https://evotianusx.github.io',
  integrations: [starlight({
    title: 'Evotianus Page',
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
    }, {
      label: 'Projects',
      autogenerate: {
        directory: 'projects'
      }
    }]
  }), tailwind()]
});