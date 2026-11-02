import rss from '@astrojs/rss';
import { publishedPosts, entryUrl } from '../lib/posts.js';
export async function GET(context) {
  const posts = await publishedPosts('en-IN');
  return rss({
    title: 'Dus AI Tool — English (India)',
    description: 'AI tools, tested in India.',
    site: context.site,
    items: posts.map((post) => ({ title: post.data.title, description: post.data.description, pubDate: post.data.pubDate, link: entryUrl(post) })),
  });
}
