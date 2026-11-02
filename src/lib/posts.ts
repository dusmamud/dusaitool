import { getCollection, type CollectionEntry } from 'astro:content';
import type { Locale } from '../i18n/index';
import { slugFromId, readingMinutes } from '../i18n/index';

export type BlogEntry = CollectionEntry<'blog'>;

export function entrySlug(entry: BlogEntry): string {
  return slugFromId(entry.id);
}

export function entryUrl(entry: BlogEntry): string {
  const slug = entrySlug(entry);
  return entry.data.locale === 'hi' ? `/hi/blog/${slug}/` : `/blog/${slug}/`;
}

export async function publishedPosts(locale: Locale): Promise<BlogEntry[]> {
  const all = await getCollection('blog', ({ data }) => !data.draft && data.locale === locale);
  return all.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export async function findPost(locale: Locale, slug: string): Promise<BlogEntry | undefined> {
  const posts = await publishedPosts(locale);
  return posts.find((post) => entrySlug(post) === slug);
}

export async function hasTranslation(slug: string, locale: Locale): Promise<boolean> {
  return (await findPost(locale, slug)) !== undefined;
}

export async function postMinutes(entry: BlogEntry): Promise<number> {
  // Body is available on the entry in Astro 7 content collections.
  const body = typeof entry.body === 'string' ? entry.body : '';
  return readingMinutes(body);
}

export function isoDate(date: Date): string {
  return date.toISOString().slice(0, 10);
}

/** All tags in this locale with their post counts, computed at build
    time, never typed by hand (afd-design-direction §6). */
export async function tagCounts(locale: Locale): Promise<{ tag: string; count: number }[]> {
  const posts = await publishedPosts(locale);
  const map = new Map<string, number>();
  for (const post of posts) {
    for (const tag of post.data.tags ?? []) map.set(tag, (map.get(tag) ?? 0) + 1);
  }
  return [...map.entries()]
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
}

export function tagUrl(locale: Locale, tag: string): string {
  const slug = tag.toLowerCase().replace(/[^a-z0-9ऀ-ॿ]+/g, '-').replace(/^-|-$/g, '');
  return locale === 'hi' ? `/hi/blog/tag/${slug}/` : `/blog/tag/${slug}/`;
}

/** Related posts: same tag first, then same category, newest first. */
export async function relatedPosts(entry: BlogEntry, limit = 3): Promise<BlogEntry[]> {
  const posts = (await publishedPosts(entry.data.locale)).filter((p) => p.id !== entry.id);
  const score = (p: BlogEntry) => {
    const sharedTags = (p.data.tags ?? []).filter((tag) => (entry.data.tags ?? []).includes(tag)).length;
    const sameCategory = p.data.category === entry.data.category ? 1 : 0;
    return sharedTags * 2 + sameCategory;
  };
  return posts.sort((a, b) => score(b) - score(a) || b.data.pubDate.valueOf() - a.data.pubDate.valueOf()).slice(0, limit);
}
