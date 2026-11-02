# Design — Dus AI Tool

Design read (afd-design-direction §1):

> Reading this as: **an AI tools blog** for **Indian students, freelancers
> and small business owners**, with a **calm editorial, test-first**
> language, leaning toward **Swiss editorial / magazine**.

One thing a visitor must do or remember: pick the right tool without
wasting money or time, because the test was done in India. The single
surface carrying personality is the featured test / verdict panel and
the article headline — everything else stays quiet.

## Dials (afd-design-direction §2, awesome-frontend-design)

Preset: `static-balanced` — Astro, static, 2 themes (light/dark), custom style.

| Surface | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Home | 7 | 6 | 4 |
| Article | 4 | 3 | 3 |
| Lists / search | 5 | 4 | 5 |

Motion is balanced on home/list (CSS scroll reveal, View Transitions,
one hover microinteraction) and calm on articles (state transitions
only, plus a CSS scroll-driven reading progress bar, no JS).

## Article v6: responsive article + mobile TOC (2026-11-02)

Bug found by screenshots: on mobile the 520px table forced the grid
column wider than the viewport, cutting h1 and paragraphs at the
right edge, and mobile had no TOC at all (sidebar was lg only).
Fix: grid is now grid-cols-1 + min-w-0 on grid, article and sidebar;
prose tables scroll inside the article (display:block, max-width:100%,
overflow-x:auto); h1 breaks long words; breadcrumb current page is
min-w-0 max-w-full truncate. New src/components/ArticleToc.astro:
mobile/tablet only (lg:hidden), in-flow panel after title/meta, never
an overlay; button 52px, aria-expanded/aria-controls, count badge,
chevron rotates, list display:none when closed, closes on link click
and Escape. Desktop sidebar stays, sticky top-20 (was top-32, 72px dead
gap). Verified: 320/360/390/768/1440, scrollWidth == innerWidth at
every width, h1 right edge inside viewport, TOC open/close via CDP
(aria-expanded true, panel visible).

## Tokens — v5: SaaS dark grading (Linear, Exa 2026-11-02, supersedes v4 dark only)

Light stays editorial blue #2c5f8a / paper #fbf8f3. Dark is now Linear
SaaS grading, not warm Material: bg #08090a, surface #0f1011,
surface-2 #141516, border #23252a (1px white 8% hairline, no shadow
on resting cards; floating header 0 4px 24px rgba(0,0,0,0.45)),
text #f7f8f8, secondary #d0d6e0, tertiary #8a8f98, accent
#4ea7fc (Linear info blue, same blue family as light, not a new
hue). Warm stone dark greys replaced by neutral Linear greys in
dark only. Verified by CDP: body rgb(8,9,10), header rgb(15,16,17),
border rgb(35,37,42), body text rgb(208,214,224), accent
rgb(78,167,252). Footer top rule is now a hairline in both themes.

## Tokens — v4: editorial blue + Material dark (Exa cross-verified, 2026-11-02)

Primary changed on user demand (forest green replaced, not kept):
light #2c5f8a (editorial link blue, 6.37:1 on newsprint #fbf8f3, AA),
dark #90caf9 (Material blue 200 tone, desaturated, high contrast on
dark). Paper #fbf8f3, headline black #1a1a1a, body grey #4a4a4a
(everyhexcode newsletter-editorial). Dark: bg warm near-black #1a1714
(Material #121212, warmed), elevated surface #241f1b (header/cards/
footer — surfaces lighter than bg, Material elevation), text warm
near-white #f2eee3 (not pure white, no vibration). Sources: Exa
web_search_exa x4 ($0.007 each) + web_fetch_exa ($0.002): Material
Design dark theme, Android colour, NN/g menu design + sticky headers,
web.dev navigation.

Header v4 (NN/g): utility bar ABOVE primary (RSS, language, theme),
scrolls away; sticky main bar only, 56px, opaque solid (no
backdrop-blur — NN: translucent sticky headers distract), desktop
primary nav always visible (Home, Blog), Search as a blue pill CTA
on the right, hamburger mobile-only, hidden menu display:none so
links are not focusable when closed (web.dev).

## Tokens — v3: serif edition (user decision, 2026-11-02)

English everywhere: Instrument Serif (only weight 400 + italic, so
hierarchy comes from size, spacing and colour, never font-bold —
faux bold is disabled in UI via `font-synthesis-weight: none`, and
only semantic <strong> in article content may synthesise).
Hindi everywhere: Noto Serif Devanagari (400 + 700).
Root size 17px mobile / 18px desktop, so serif small text lands at
~15-16px, not 14px. Warm paper #fdfcf8, warm stone greys, one forest
accent #1f4d3a (sage #a8c5b3 in dark). Fraunces/Inter removed.

Header v3: mobile hamburger (real button, aria-expanded, morphs to
X, transform only), desktop one-row nav with animated underline,
current page underlined, scroll shadow via IntersectionObserver
(no scroll listener), every target >= 44px, language button shows
EN on mobile so Hindi header fits 360px.
Footer v3: 4-column grid (brand + promise, Explore, computed Topics,
Follow + Back to top), 1 col mobile, 2 col tablet, thick top rule.

Motion v3: hero entrance once (staggered 60/140/220ms, transform +
opacity only), scroll reveal on lists, View Transitions, reading
progress, theme icon rotates, brand mark tilts on hover. All
respect `prefers-reduced-motion` (reveal/hero forced visible).

## Tokens (afd-theme-systems, tailwind-design-system) — v2, superseded by v3 above

- One grey family: zinc, in both themes. No warm/cool grey mixing.
- One brand accent: teal. Light: `#0f766e` (text and fills, white text
  on fills, ~5.5:1 on white). Dark: `#5eead4` for text, `#134e4a` for
  soft fills. Dark is designed, not inverted: surfaces are raised
  (`zinc-900` on `zinc-950`), borders carry more weight.
- Status colours are separate from the brand accent and always paired
  with a label: emerald = pros/verdict, rose = cons, amber = warning.
- One radius system: `rounded-2xl` for panels, `rounded-full` for
  pills and primary buttons. One shadow, used only on raised panels
  (featured test, ToolCard) — list rows have no shadow, just hairlines.
- Typography: two families maximum. Display = Fraunces Variable
  (editorial serif, headlines only). Body/UI = Inter Variable (deliberate
  pairing, high legibility for Hinglish Roman). Hindi headings fall back
  to Noto Serif Devanagari; Hindi body to Noto Sans Devanagari, never
  letter-spaced, line-height 1.8.
- Body measure: 60–70ch for reading. Article grid is
  `minmax(0,65ch) + 240px` (contents on desktop, hidden on mobile).
  Headings use `text-wrap: balance`, paragraphs `pretty`.

## Layout families (no family twice on one page)

- Home: asymmetric hero (headline + CTAs, 1.6fr) + featured-test panel
  (1fr), then tag chips with build-time counts, then a hairline list
  (not equal cards) for the remaining posts.
- Blog list: headline + count (computed, never typed) + tag chips +
  hairline list.
- Article: breadcrumb + 65ch prose + sticky contents (desktop) +
  related guides (same tags first, then category, newest first).
- Search: input (48px) + popular searches (build-time tags) + results
  with count + an explicit empty state. Hindi search filters Pagefind
  results to `/hi/` URLs; English filters them out.
- 404: real suggested pages (latest posts, computed) + a home button.

## What was wrong before, and what changed

| Before (generic SaaS card kit) | After |
|---|---|
| Identical rounded cards, same shadow everywhere | One raised featured panel; rest is a hairline list |
| Empty hero: title + tagline, no job, no CTA | Hero fits the viewport: label, headline (max 2 lines), one sentence, two CTAs, featured test as the real visual |
| Inter everywhere, no display face | Fraunces display + Inter body, deliberate pairing |
| No accent identity, slate everywhere, blue links | One teal accent, one zinc family, links in accent |
| Header targets ~28px, nav wrapped awkwardly on mobile | Sticky header, brand row + nav row, every target ≥44px, current page marked with `aria-current` |
| Hindi search was a dead page | Hindi search works, filtered to Hindi results |
| No tag filter, no contents, no related posts, no progress | Tag pages, contents, related posts, CSS reading progress |
| No OG image (favicon used) | Branded `public/og.png` (1200×630), `summary_large_image` |
| No motion at all, static template feel | Balanced CSS reveal + View Transitions, article calm, `prefers-reduced-motion` respected |

## Anti-patterns avoided (frontend-design, frontend-ui-ux, afd)

- No purple-blue gradient hero, no gradient headline text, no neon glow.
- No all-caps eyebrow labels, no `01 /` sequence markers on
  non-sequential content, no fake metrics or testimonials (counts are
  computed from the content collection at build time).
- No icon-only buttons without a label: theme toggle has a visible
  label and `aria-pressed`; language switch is a labelled link.
- No `outline: none`, no hover-only affordances, no content hidden
  until JavaScript runs (search and theme work without JS for reading;
  search degrades to a clear message when the index is missing).
- No new third-party origin, no new font family without a reason:
  Fraunces is self-hosted via Fontsource, `font-display: swap`.

## Not checked

- Real iOS Safari, real screen reader, slow-network throttling.
- Contrast is checked by token choice (teal-700 on white, teal-300 on
  zinc-950, zinc-600 on white), not by an automated build gate yet.

## v7 — Article layout, side gap fix (2026-11-02)
Research: Exa (2 searches, $0.014) + Firecrawl (1 search, 2 credits). Cross-verified:
reading measure 60–75 characters/line, ~640–720px at 18px — full-width body text on a
wide monitor is tiring to read, so the article column must stay narrow; the bug was
not the narrow column, it was the grid not filling its container (old grid
65ch + 240px = ~825px inside a 1152px container left ~325px of asymmetric empty
space on the right, and the sidebar held only a short TOC, so below it the right
side was empty). Two-column ratio ~2/3 content + 1/3 sidebar, sidebar 280–320px
from 1024px, and a post-page sidebar earns its space only with TOC + related
posts + tags (UI Potion, Blaskan, Aceternity). Lots of whitespace should be
balanced/centered, not left-aligned.
Fix (both `blog/[...slug].astro` and `hi/blog/[...slug].astro`):
grid `mx-auto max-w-[1044px] lg:grid-cols-[minmax(0,680px)_300px] lg:gap-16` —
article 680px max, sidebar 300px, gap 64px, grid centered so page margins are
symmetric; sidebar is now a full right rail (TOC + Related guides mini list +
current-post Topics chips + tested-promise note), `lg:sticky lg:top-20
lg:self-start` so it sticks below the 56px header without hiding under it
(self-start matters: a stretched grid item pins to the grid bottom and its
heading slides under the header near the article end).
Verified: 1440 grid 191→1235 (1044px, centered), article 672px, sidebar 300px,
scrolled sidebar top 90px; 1024 grid fills 955px, sidebar 300px; 390 mobile
unchanged, sidebar hidden, no overflow anywhere. Build 19 pages.

## v8 — Orbit Spark icon (2026-11-03)
Icon decision: first letter-based set (A–E) was rejected by Dus, with the rule
"no letter at all, professional unique shape". Second letter-free set (1–5)
was shown, Dus chose 3 — Orbit Spark (gradient spark + orbit ring, no text).
Applied everywhere the old "D" badge was: `public/favicon.svg` (now the Orbit
Spark SVG), Header brand mark and Footer brand mark (both now
`<img src="/favicon.svg">`, no D circle left in either component), and
`public/og.png` regenerated from `shot-tmp/og.html` with the spark mark.
Verified: home light + dark, header logo `/favicon.svg` present, no overflow,
build 19 pages.

## v9 — Smooth TOC + full-screen mobile menu (2026-11-03)
Research: Exa (2 searches, $0.014) — W3C/APG + web.dev + NN/g pattern for
full-screen menus, and the CSS grid 0fr -> 1fr accordion technique.
Why it felt bad before: mobile TOC panel toggled display:none (instant
jump, no animation), hamburger middle bar faded instantly (only
transform was transitioned, not opacity), and the mobile menu was a
small dropdown under the header, not a full screen.
Fix:
- Mobile TOC (ArticleToc.astro): panel is now a grid with
  grid-template-rows 0fr -> 1fr (400ms, ease-out token, no guessed
  max-height, no layout jump), chevron rotates 180deg with the same
  token, closed panel is visibility:hidden so its links are NOT
  keyboard-focusable while closed, and it becomes visible instantly
  on open. Reduced-motion: transition delays are forced to 0ms.
- Desktop TOC (both slug pages): IntersectionObserver (rootMargin
  -96px / -70%) highlights the current h2 in the sidebar (blue text
  + blue left border, border is the second cue, not colour alone).
- Hamburger menu (Header.astro): dropdown replaced by a full-screen
  modal dialog (fixed inset-0, z-50, role="dialog", aria-modal):
  top bar with logo + close X, large 28px / 64px links (Home, Blog,
  Search) staggered in 60/120/180ms, language + RSS + tagline at the
  bottom. Open: fade + 12px rise, transform/opacity only. Focus is
  trapped inside (Tab cycles), Escape closes, body scroll locks
  (previous overflow saved and restored), focus returns to the
  hamburger button on close, hamburger bars morph to X with
  transform + opacity transitions.
- Bug found in testing: the modal first rendered sideways because
  flex-col was missing (flex row by default) — fixed, then re-tested.
Verified: mobile TOC closed visibility:hidden height 1px, open height
194px chevron rotated, no overflow at 390px; menu open display:flex
opacity 1 body overflow hidden focus on close button, Escape closes
(display:none, overflow restored, focus back on hamburger); desktop
TOC "What was tested" active after scrolling to it. Build 100 pages.

## v10 — Skill 1: frontend-design (Anthropic), AI tells removed (2026-11-03)
Audit against frontend-design §"commonest tells of a generated page"
and §"AI-generated design clusters":
- Middle-dot meta strings everywhere (trait 5: 'A · B · C') — removed
  from article meta, PostRow, featured panel, tag pages, 404 and
  footer. Meta is now prose with commas, or separated by layout gap
  (PostRow) / a separate Back-to-blog link (tag pages), never a dot.
- Decorative status dot in the home pill — removed. Pill now reads
  "Tested this week: N tools tested" (N is build-time computed,
  now 19, not a typed number).
- Scattered fade-and-slide-up on every post row (.reveal, view
  timeline) — removed. Only the home hero keeps one orchestrated
  entrance; the list is static editorial content.
- Featured panel drop shadow in light — removed. Resting panels
  are hairline only, matching the v5 "no drop shadow on resting
  cards" rule that the panel itself was violating.
Checked and kept (not tells here): no all-caps labels, no single-word
accent in headlines, no numbered eyebrows, no gradient washes,
no purple-blue glow, no '→' on links, no monospace data labels.
Numbered list in "How to choose" kept: it is a real sequence.
Verified: home + article body text contains no '·', build 124 pages.

## v11 — Skill 2: web-design-guidelines (Vercel), fresh rules checked (2026-11-03)
Fetched https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
and audited the site against it, file:line style. Passes already in
place (not re-fixed): focus-visible 3px outline, skip link,
scroll-margin on heading anchors, semantic buttons/links, search
label + aria-live="polite" results, theme-color + color-scheme,
text-wrap balance/pretty, tabular-nums, no transition:all, no
outline-none, viewport without user-scalable=no, placeholders
ending with '…', autocomplete="off" on the search field.
Fixes in this commit:
- <img> without width/height (CLS rule): header favicon 36x36 (2
  places: main header + modal top bar), footer favicon 40x40.
- Search input without a meaningful name: added name="q" (en + hi).
- Touch rules missing: a/button get touch-action: manipulation and
  an intentional brand-tint tap highlight; the full-screen menu
  gets overscroll-behavior: contain. Page overscroll is NOT
  suppressed, so pull-to-refresh still works on phones.
Verified: build passes, search page renders unchanged (these fixes
are invisible by design, except for the tap feedback on mobile).

## v12 — Skill 3: ui-ux-pro-max, Priority 2 Touch (2026-11-03)
Ran the skill's design-system search for "editorial blog reading long
articles" (Swiss Modernism 2.0, editorial, grid — matches the current
direction, so no palette/font change: the tool's pink accent and
Libre Bodoni suggestion is generic output and does NOT override the
user's Instrument Serif + editorial blue decision).
Audit against its Priority 1-2 rules: contrast already passes
(4.5:1+ on small text in both themes), no emoji icons, focus visible,
reduced motion respected, no horizontal scroll. Touch violations
fixed in this commit (min 44x44px, 8px+ spacing):
- Header utility links (RSS, language) and theme button: 36px -> 44px.
- PostRow tag chips: 32px -> 44px (link and plain versions, same
  height so the row does not shift between the two).
- Desktop TOC links and sidebar topic chips (both slug pages):
  36px -> 44px.
- Footer nav lists: gap 4px -> 8px between the already-44px links.
Verified: build passes, no layout break (sidebar is scrollable, so
taller TOC links still fit).
