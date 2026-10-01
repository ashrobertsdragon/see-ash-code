import rss from '@astrojs/rss';
import { getPublishedPosts } from '../utils/posts';
import { SITE_TITLE, SITE_DESCRIPTION, SITE_URL } from '../consts';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getPublishedPosts();

  return rss({
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    site: context.site || SITE_URL,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: new Date(post.data.published_at),
      description: post.data.description,
      link: `/blog/${post.slug}/`,
    })),
    customData: `<language>en-us</language>`,
  });
}
