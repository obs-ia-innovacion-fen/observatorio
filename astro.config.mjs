import { defineConfig } from 'astro/config';

export default defineConfig({
  // URL publica del sitio. Cambiar cuando exista el dominio definitivo.
  site: 'https://observatorio-ce8.pages.dev',
  markdown: { shikiConfig: { theme: 'github-light' } },
});
