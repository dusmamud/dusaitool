import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// One collection for both locales. The locale lives in frontmatter AND
// in the folder (en-IN/ or hi/) so a post can never be published in the
// wrong language by accident — pages filter on both.
const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string().min(10).max(120),
    description: z.string().min(30).max(180),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    locale: z.enum(['en-IN', 'hi']),
    tags: z.array(z.string()).default([]),
    category: z.string().default('ai-tools'),
    draft: z.boolean().default(false),
    // Short, human verdict shown on cards. Keep it honest, not clickbait.
    verdict: z.string().max(160).optional(),
    heroAlt: z.string().default(''),
    // Per-article OG image path (e.g. '/og/<slug>-en.png'). When absent,
    // SEO falls back to the site-wide /og.png.
    ogImage: z.string().optional(),
  }),
});

export const collections = { blog };
