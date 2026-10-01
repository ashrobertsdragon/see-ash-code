# See Ash Code

Personal portfolio and technical blog of **Ashlynn Antrobus** — exploring Python architecture, unit testing philosophies, DevOps tooling, and accessibility in software engineering.

Built with [Astro](https://astro.build/) and [Tailwind CSS v4](https://tailwindcss.com/) with full dark/light mode support, RSS syndication, automated sitemaps, and a markdown publishing toolchain.

---

## Features

- **Portfolio & Blog Hybrid**:
  - **Homepage (`/`)**: Developer hero, focus areas, featured articles, project showcases, and topic explorer.
  - **Blog (`/blog`)**: Chronological archive of technical articles with topic filtering and estimated reading times.
  - **Projects (`/projects` & `/projects/[...slug]`)**: Dedicated case studies for LoreBinders, ProsePal, and Ebook2Text.
  - **About (`/about`)**: Developer background, software architecture principles, indie authorship, and programming with dyslexia.
  - **Tags (`/tags/[tag]`)**: Topic-specific feeds with slugified URLs.
- **Design & Typography**:
  - Tailwind CSS v4 using custom OKLCH design tokens defined in `index.css`.
  - `@tailwindcss/typography` with dual-theme Shiki code blocks (`github-light` / `github-dark`).
  - Interactive copy-to-clipboard buttons on all code snippets.
  - Responsive Table of Contents (TOC) for long technical guides.
- **Markdown Authoring & Publishing Workflow**:
  - Drafts authored in `drafts/` as plain markdown.
  - Companion CLI (`publish.py`) executed with `uv` to manage draft lifecycle and synchronization.
  - Astro Content Collections with Zod schema validation.
- **Syndication & SEO**:
  - Full RSS 2.0 feed at `/rss.xml`.
  - XML Sitemap at `/sitemap-index.xml`.
  - OpenGraph and Twitter Cards metadata for rich social previews.

---

## Getting Started

### Prerequisites

- Node.js `v20+` or `v24+` & `npm`
- Python `3.10+` with [`uv`](https://github.com/astral-sh/uv)

### Installation

```bash
npm install
```

### Development Server

Start the local Astro development server:

```bash
npm run dev
```

### Production Build

Typecheck and generate the static production build:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

---

## Writing & Publishing Workflow

All articles are authored in Markdown. You can create and manage drafts using `publish.py` via `uv`:

```bash
# List all drafts and their published status
uv run publish.py list

# Create a new draft and automatically open it in your editor
uv run publish.py new "My New Article Title"

# Create a draft without opening an editor
uv run publish.py new "My New Article Title" --no-edit

# Publish an existing draft (sets published: true and stamps timestamp)
uv run publish.py publish <slug-or-title>

# Unpublish an article (sets published: false)
uv run publish.py unpublish <slug-or-title>

# Synchronize drafts into src/content/blog/ and normalize image URLs
uv run publish.py sync
```

Only articles marked `published: true` with a publication date in the past are rendered on the public website.

---

## Project Structure

```text
├── drafts/                     # Working markdown drafts and original assets
│   ├── images/                 # Original article images
│   └── *.md                    # Article drafts
├── public/
│   ├── favicon.svg             # Site favicon
│   └── images/                 # Static web-optimized article assets
├── src/
│   ├── components/             # Reusable Astro UI components
│   │   ├── BaseHead.astro      # Metadata, SEO, and stylesheets
│   │   ├── CopyCodeButton.astro# Client-side copy button handler
│   │   ├── Footer.astro        # Site footer with RSS and social links
│   │   ├── Header.astro        # Navigation bar and theme toggle
│   │   ├── PostCard.astro      # Blog article preview card
│   │   ├── ProjectCard.astro   # Portfolio project card
│   │   ├── TableOfContents.astro # Dynamic heading navigation
│   │   ├── ThemeScript.astro   # Zero-FOUC theme detector
│   │   └── ThemeToggle.astro   # Dark/light mode switcher
│   ├── content/
│   │   ├── blog/               # Published blog posts (Content Collection)
│   │   ├── projects/           # Portfolio project case studies
│   │   └── config.ts           # Zod schema definitions
│   ├── layouts/
│   │   └── BaseLayout.astro    # Master HTML page layout
│   ├── pages/                  # File-based routing
│   │   ├── index.astro         # Homepage
│   │   ├── about.astro         # About page
│   │   ├── blog/               # Blog archive and post detail
│   │   ├── projects/           # Project gallery and detail
│   │   ├── tags/               # Dynamic tag feeds
│   │   └── rss.xml.ts          # RSS syndication endpoint
│   ├── styles/
│   │   └── index.css           # Styling import entry
│   ├── consts.ts               # Author and site constants
│   └── utils/                  # Reading time and post query utilities
├── astro.config.mjs            # Astro configuration
├── index.css                   # Tailwind v4 OKLCH design tokens
├── package.json                # Project dependencies and scripts
└── publish.py                  # Python draft manager (uv)
```

---

## License

© 2024–2026 Ashlynn Antrobus. All rights reserved.
