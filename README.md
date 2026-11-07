# Dus AI Tool — dusaitool

AI tools, tested in India, in English (India) and Hindi.
Static Astro blog. No backend, no database. Free hosting on Cloudflare Pages
via GitHub Actions.

Live (before a custom domain): https://dusaitool.pages.dev

## Verified versions (checked 2026-11-02)

Checked with Exa MCP for Astro i18n / accessibility best practice, and with
`npm view` for exact versions:

- Astro 7.4.5
- Tailwind CSS 4.3.3 + `@tailwindcss/vite` 4.3.3 + `@tailwindcss/typography` 0.5.20
- `@astrojs/mdx` 8.1.2, `@astrojs/sitemap` 3.7.4, `@astrojs/rss` 4.0.19
- Pagefind 1.6.0 (search, built at deploy time, no server)
- Wrangler 4.156.1, Sharp 0.35.5, TypeScript 7.0.2, Node 24

Do not add a Cloudflare adapter. This is a static site: `output: 'static'`
and the adapter is only for SSR. Adding it is the most common mistake here.

## Quickstart

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # astro build + pagefind --site dist
npm run preview
```

## Locales

- Default: English (India) — `en-IN`, no URL prefix: `/`, `/blog/...`
- Hindi — `hi`, Devanagari, under `/hi/`, `/hi/blog/...`
- Default is English on purpose. A Hindi reader switches with the language
  button in the header; the switcher links to the same post when a
  translation exists, otherwise to the Hindi home page.

Add a post:

1. English: `src/content/blog/en-IN/my-slug.md`
2. Hindi: `src/content/blog/hi/my-slug.md` (same slug, translated content)
3. Frontmatter must include `locale` matching the folder, or the build
   schema check will fail — that is intentional.

## MD or MDX? The rule

- `.md` — 90% of posts. Pure text, headings, tables, images. Never breaks.
- `.mdx` — only when a post needs a component: `ToolCard`, `ProsCons`,
  `Callout`. Import the component at the top of the file.

Example MDX components live in `src/components/`.

## Theme

- Light / dark, class-based Tailwind dark variant.
- First paint: an inline script in `<head>` reads `localStorage`
  (`dusaitool-theme`) or `prefers-color-scheme`. No flash of wrong theme.
- Both palettes are checked for 4.5:1 text contrast (WCAG AA).
- Toggle button has an accessible label; it is a real `<button>`, not a div.

## Accessibility checklist (applied, not aspirational)

- Skip-to-content link, first focusable element, visible on focus.
- Semantic landmarks: `<header>`, `<nav>`, `<main id="main-content">`, `<footer>`.
- One `<h1>` per page, heading order preserved in posts.
- `:focus-visible` is never removed; focus is never hidden by a sticky header.
- `lang` is set per page (`en-IN` / `hi`); Devanagari gets line-height 1.8
  and no letter-spacing.
- Images need `alt`; decorative images are `aria-hidden`.
- Search input has a real `<label>`; results live in `aria-live="polite"`.
- `prefers-reduced-motion` disables smooth scroll and transitions.
- Layout works at 400% zoom: no fixed widths, tables scroll horizontally,
  grids collapse to one column on mobile.

## Project tree

```
dusaitool/
  .github/workflows/deploy.yml   # Node 24 -> npm ci -> build -> Pages
  astro.config.mjs                # site, static, i18n, mdx, sitemap, Tailwind
  src/
    content.config.ts             # typed blog schema (zod)
    content/blog/en-IN/           # English posts (.md / .mdx)
    content/blog/hi/              # Hindi posts
    i18n/index.ts                 # locales, UI strings, slug + reading-time helpers
    lib/posts.ts                  # published posts, URLs, translation lookup
    components/                   # SEO, Header, Footer, PostCard, ToolCard, ProsCons, Callout
    layouts/BaseLayout.astro      # html lang, theme script, skip link, landmarks
    pages/                        # en-IN routes at root, rss.xml.js (JS, not .ts — see note below)
    pages/hi/                     # Hindi routes under /hi/
    styles/global.css             # Tailwind v4, dark variant, focus, lang(hi)
  public/                         # favicon.svg, robots.txt (copied as-is)
```

## Deploy

1. Create a GitHub repo named `dusaitool` and push this code.
2. In Cloudflare Pages, create a project named `dusaitool` first
   (a direct-upload deploy cannot create it interactively).
3. Add repo secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`.
4. Push to `main`. The workflow builds and deploys `dist/`.
5. Later, add a custom domain in Pages and change only `site` in
   `astro.config.mjs` — no code rewrite.

## Build notes (senior-level fixes found by actually building)

- RSS endpoints are `.js`, not `.ts`: Astro 7 + the pinned TypeScript
  failed to transform `rss.xml.ts` endpoints at build time, JS works.
- Blog slugs are lower-cased by Astro (`en-IN` becomes `en-in` in the
  entry id), so `slugFromId` strips the locale case-insensitively.
  Without that fix, English posts wrongly built under `/blog/en-in/`.
- Pagefind is loaded with `/* @vite-ignore */` on the search page, or
  Vite tries to resolve `/pagefind/pagefind.js` before it is generated.

## What is deliberately NOT in this stack

WordPress (needs PHP + database), Next.js (server features, heavier JS),
React for the whole blog, a CMS, a database, Bootstrap/jQuery, Disqus.
Each of those breaks the free, static, no-backend constraint.
Tip: use `.md` for 90% of posts and reach for `.mdx` only when a post needs a component such as `ToolCard`, `ProsCons` or `Callout`.
Note: a post's frontmatter `locale` must match its folder (`en-IN` or `hi`), or the build schema check will fail — that failure is intentional.
The Hindi language switcher links to the same post when a translation exists, and falls back to the Hindi home page when it does not.
Search is built at deploy time with Pagefind, so it works with no server — the build step is `astro build + pagefind --site dist`.
