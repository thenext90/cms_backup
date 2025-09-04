// @ts-check
// Last updated: 2025-09-04 10:20 - FINAL DEPLOYMENT: Navbar reorganization complete
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.cmsconsultores.cl',
  integrations: [tailwind(), sitemap()],
  output: 'static',
  build: {
    format: 'directory'
  },
  vite: {
    build: {
      rollupOptions: {
        output: {
          assetFileNames: 'assets/[name].[hash][extname]'
        }
      }
    }
  }
});