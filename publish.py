#!/usr/bin/env python3
"""
publish.py — Blog publishing and draft synchronization CLI.
Run with: uv run publish.py [list|publish|unpublish|sync|new]
"""

import sys
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
SIBLING_CONTENT = PROJECT_ROOT.parent / "see-ash-code-content" / "drafts"
ENV_CONTENT = os.environ.get("BLOG_CONTENT_DIR")

if ENV_CONTENT and Path(ENV_CONTENT).exists():
    DRAFTS_DIR = Path(ENV_CONTENT).resolve()
elif SIBLING_CONTENT.exists():
    DRAFTS_DIR = SIBLING_CONTENT
else:
    DRAFTS_DIR = PROJECT_ROOT / "drafts"

CONTENT_DIR = PROJECT_ROOT / "src" / "content" / "blog"
IMAGES_SRC = DRAFTS_DIR / "images"
IMAGES_DEST = PROJECT_ROOT / "public" / "images"

FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(content: str):
    match = FRONTMATTER_REGEX.match(content)
    if not match:
        return {}, content
    raw_yaml, body = match.groups()
    metadata = {}
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            # Parse simple scalars
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1].replace('\\"', '"')
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1].replace("\\'", "'")
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.startswith("[") and val.endswith("]"):
                val = [item.strip().strip("'\"") for item in val[1:-1].split(",") if item.strip()]
            metadata[key] = val
    return metadata, body


def dump_frontmatter(metadata: dict, body: str) -> str:
    lines = ["---"]
    for k, v in metadata.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, list):
            items_str = ", ".join(f'"{item}"' for item in v)
            lines.append(f"{k}: [{items_str}]")
        else:
            v_str = str(v).replace('\\"', '"').replace('"', '\\"')
            lines.append(f'{k}: "{v_str}"')
    lines.append("---")
    lines.append("")
    lines.append(body.lstrip("\r\n"))
    return "\n".join(lines)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text


def sanitize_markdown_body(body: str) -> str:
    # 1. Replace relative ![](images/...) with ![](/images/...)
    body = re.sub(r"!\[(.*?)\]\(images/([^)]+)\)", r"![\1](/images/\2)", body)
    
    # 2. Replace absolute legacy wp-content URLs with /images/...
    body = re.sub(
        r"!\[(.*?)\]\(https?://see-ash\.codes/wp-content/uploads/\d{4}/\d{2}/([^)]+)\)",
        r"![\1](/images/\2)",
        body,
    )
    
    # 3. Clean up multiple empty blank lines
    body = re.sub(r"\n{4,}", "\n\n", body)
    return body


def ensure_tags_and_description(slug: str, meta: dict, body: str):
    # If description is missing, extract first non-empty paragraph
    if "description" not in meta or not meta["description"]:
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#") and not p.strip().startswith("!")]
        if paragraphs:
            summary = paragraphs[0].replace("\n", " ").strip()
            if len(summary) > 160:
                summary = summary[:157] + "..."
            meta["description"] = summary
        else:
            meta["description"] = meta.get("title", "")

    # Assign default tags based on keywords if missing
    if "tags" not in meta or not meta["tags"]:
        title_lower = meta.get("title", "").lower()
        body_lower = body.lower()
        tags = []
        if "python" in title_lower or "python" in body_lower:
            tags.append("Python")
        if "test" in title_lower or "unit test" in body_lower or "pytest" in body_lower:
            tags.append("Testing")
        if "dyslexia" in title_lower or "accessibility" in body_lower:
            tags.append("Accessibility")
            tags.append("Career")
        if "review" in title_lower or "code review" in body_lower:
            tags.append("Best Practices")
        if "import" in title_lower or "future" in title_lower:
            tags.append("Architecture")
        if "codebase" in title_lower or "refactor" in body_lower:
            tags.append("Architecture")
        if not tags:
            tags = ["Software Development"]
        meta["tags"] = sorted(list(set(tags)))


def sync_drafts():
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DEST.mkdir(parents=True, exist_ok=True)

    if IMAGES_SRC.exists():
        for img in IMAGES_SRC.glob("*.*"):
            dest = IMAGES_DEST / img.name
            if not dest.exists() or img.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(img, dest)
    
    draft_files = list(DRAFTS_DIR.glob("*.md"))
    print(f"Syncing {len(draft_files)} drafts from {DRAFTS_DIR}...")
    
    for df in draft_files:
        content = df.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        slug = df.stem
        
        # Format body
        cleaned_body = sanitize_markdown_body(body)
        
        # Ensure title
        if "title" not in meta:
            meta["title"] = slug.replace("-", " ").title()
            
        # Ensure published
        if "published" not in meta:
            meta["published"] = False
            
        # Ensure published_at
        if "published_at" not in meta:
            meta["published_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            
        ensure_tags_and_description(slug, meta, cleaned_body)
        
        # Update draft itself with normalized tags/descriptions
        updated_draft_content = dump_frontmatter(meta, cleaned_body)
        df.write_text(updated_draft_content, encoding="utf-8")
        
        # Write to content directory
        target_file = CONTENT_DIR / f"{slug}.md"
        target_file.write_text(updated_draft_content, encoding="utf-8")
        
        status = "PUBLISHED" if meta.get("published") else "DRAFT"
        print(f"  [✓] ({status}) {meta['title']} -> {target_file.name}")

    print("\nSync completed successfully.")


def list_drafts():
    draft_files = sorted(list(DRAFTS_DIR.glob("*.md")))
    print(f"{'Status':<12} {'Date':<22} {'Slug / Title'}")
    print("-" * 75)
    for df in draft_files:
        meta, _ = parse_frontmatter(df.read_text(encoding="utf-8"))
        is_pub = meta.get("published", False)
        status = "Published" if is_pub else "Draft"
        date_str = str(meta.get("published_at", "—"))[:19]
        title = meta.get("title", df.stem)
        print(f"{status:<12} {date_str:<22} {df.stem}")
        print(f"    Title: {title}")
        tags = meta.get("tags", [])
        if tags:
            print(f"    Tags: {', '.join(tags)}")
        print()


def set_publish_status(slug_query: str, status: bool):
    matches = list(DRAFTS_DIR.glob(f"*{slug_query}*.md"))
    if not matches:
        print(f"Error: No draft found matching '{slug_query}' in {DRAFTS_DIR}")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Multiple matches found for '{slug_query}':")
        for m in matches:
            print(f"  - {m.name}")
        print("Please specify a more precise query.")
        sys.exit(1)
        
    draft_file = matches[0]
    meta, body = parse_frontmatter(draft_file.read_text(encoding="utf-8"))
    meta["published"] = status
    if status and ("published_at" not in meta or not meta["published_at"]):
        meta["published_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
    cleaned_body = sanitize_markdown_body(body)
    ensure_tags_and_description(draft_file.stem, meta, cleaned_body)
    
    updated_content = dump_frontmatter(meta, cleaned_body)
    draft_file.write_text(updated_content, encoding="utf-8")
    
    # Also sync to content/blog
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    target_file = CONTENT_DIR / draft_file.name
    target_file.write_text(updated_content, encoding="utf-8")
    
    action = "Published" if status else "Unpublished"
    print(f"{action} successfully: '{meta.get('title')}' ({draft_file.name})")


def open_in_editor(target: Path):
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL")
    if not editor:
        for candidate in ["code", "cursor", "nano", "vim"]:
            if shutil.which(candidate):
                editor = candidate
                break

    if not editor:
        print(f"Draft ready. Open with your editor: {target}")
        return

    print(f"Opening with {editor}...")
    try:
        subprocess.run([editor, str(target)])
    except Exception as e:
        print(f"Could not open {editor}: {e}")
        print(f"Draft path: {target}")


def create_new_draft(title: str, auto_open: bool = True):
    slug = slugify(title)
    target = DRAFTS_DIR / f"{slug}.md"
    if target.exists():
        print(f"Error: Draft already exists at {target}")
        sys.exit(1)
        
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {
        "title": title,
        "published": False,
        "published_at": now,
        "description": "Short summary of this article...",
        "tags": ["Python", "Software Development"],
    }
    body = f"\n\nWrite your markdown content for '{title}' here...\n"
    content = dump_frontmatter(meta, body)
    target.write_text(content, encoding="utf-8")
    print(f"Created new draft: {target}")

    if auto_open:
        open_in_editor(target)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("Usage: uv run publish.py <command> [args...]")
        print("\nCommands:")
        print("  list              List all drafts and their published status")
        print("  sync              Sync and normalize drafts into src/content/blog/")
        print("  publish <query>   Publish draft matching query (set published: true)")
        print("  unpublish <query> Unpublish draft matching query (set published: false)")
        print("  new <title>       Create a new draft and open it in your editor")
        print("                    (Use --no-edit to create without launching an editor)")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "list":
        list_drafts()
    elif cmd == "sync":
        sync_drafts()
    elif cmd == "publish":
        if len(sys.argv) < 3:
            print("Error: Specify post slug or title query to publish")
            sys.exit(1)
        set_publish_status(sys.argv[2], True)
    elif cmd == "unpublish":
        if len(sys.argv) < 3:
            print("Error: Specify post slug or title query to unpublish")
            sys.exit(1)
        set_publish_status(sys.argv[2], False)
    elif cmd == "new":
        if len(sys.argv) < 3:
            print("Error: Specify a title for the new draft")
            sys.exit(1)
        args = sys.argv[2:]
        auto_open = True
        if "--no-edit" in args:
            auto_open = False
            args.remove("--no-edit")
        title = " ".join(args)
        create_new_draft(title, auto_open=auto_open)
    else:
        print(f"Unknown command: '{cmd}'. Run 'uv run publish.py --help' for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
