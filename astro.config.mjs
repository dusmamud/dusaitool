// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Static site only: no adapter, no SSR. Cloudflare Pages serves `dist/`.
// The i18n block documents the two locales; routing itself is file-based
// (see src/pages/ and src/pages/hi/) so a missing translation never
// breaks the build — it falls back to the English (India) page via
// the language switcher, never via a silent redirect.
export default defineConfig({
  site: 'https://dusaitool.pages.dev',
  output: 'static',
  trailingSlash: 'ignore',
  i18n: {
    locales: ['en-IN', 'hi'],
    defaultLocale: 'en-IN',
    routing: {
      prefixDefaultLocale: false,
      fallback: { hi: 'en-IN' },
    },
  },
  integrations: [mdx(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: true,
    },
  },
});
