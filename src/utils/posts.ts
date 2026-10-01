import { getCollection, type CollectionEntry } from 'astro:content';

export function slugifyTag(tag: string): string {
  return tag
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '');
}

export async function getPublishedPosts(): Promise<CollectionEntry<'blog'>[]> {
  const posts = await getCollection('blog', ({ data }) => {
    // In production or default build, only include published posts
    return data.published === true && new Date(data.published_at) <= new Date();
  });

  return posts.sort(
    (a, b) => new Date(b.data.published_at).getTime() - new Date(a.data.published_at).getTime()
  );
}

export async function getAllTags(): Promise<{ tag: string; slug: string; count: number }[]> {
  const posts = await getPublishedPosts();
  const tagCounts: Record<string, number> = {};

  for (const post of posts) {
    for (const tag of post.data.tags || []) {
      tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    }
  }

  return Object.entries(tagCounts)
    .map(([tag, count]) => ({ tag, slug: slugifyTag(tag), count }))
    .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
}
