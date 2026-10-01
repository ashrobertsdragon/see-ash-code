export function getReadingTime(content: string): string {
  // Strip code blocks and markdown symbols for rough word count
  const cleanText = content
    .replace(/```[\s\S]*?```/g, '')
    .replace(/<[^>]*>/g, '')
    .replace(/[#*_~`>-]/g, ' ')
    .trim();
  const words = cleanText.split(/\s+/).filter(Boolean).length;
  const minutes = Math.max(1, Math.ceil(words / 220));
  return `${minutes} min read`;
}
