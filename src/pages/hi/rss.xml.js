import rss from '@astrojs/rss';
import { publishedPosts, entryUrl } from '../../lib/posts.js';
export async function GET(context) {
  const posts = await publishedPosts('hi');
  return rss({
    title: 'Dus AI Tool — Hindi',
    description: 'भारत में टेस्ट किए गए AI टूल।',
    site: context.site,
    items: posts.map((post) => ({ title: post.data.title, description: post.data.description, pubDate: post.data.pubDate, link: entryUrl(post) })),
  });
}
