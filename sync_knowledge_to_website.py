#!/usr/bin/env python3
"""
Sync knowledge/ summaries (lectures, papers, books, podcasts) to website/_knowledge/
for Jekyll. Mirrors the source folder structure and derives front matter from each
file's metadata header instead of relying on a fixed schema, since header fields
vary by content type (Guest/Speaker/Author, Channel/Source, Date/Published, etc).
"""
import argparse
import re
from datetime import datetime
from pathlib import Path

KNOWLEDGE_DIR = Path('knowledge')
WEBSITE_DIR = Path('website') / '_knowledge'

SKIP_FILES = {'README.md', 'knowledge_config.yaml'}

DATE_FORMATS = [
    '%Y-%m-%d', '%B %d, %Y', '%b %d, %Y', '%Y-%m', '%B %Y', '%Y',
]

HEADER_FIELD_RE = re.compile(r'^\*\*([^:*]+):\*\*\s*(.+)$')


def parse_date(raw: str, fallback: str):
    """Try several formats before falling back to a filename-derived date string."""
    if raw:
        raw = raw.strip()
        for fmt in DATE_FORMATS:
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        # Grab first ISO-looking date inside a messier string (e.g. "~85 minutes" duration leaked in)
        match = re.search(r'(\d{4}-\d{2}-\d{2})', raw)
        if match:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
    if fallback:
        for fmt in ('%Y-%m-%d', '%Y-%m', '%Y'):
            try:
                return datetime.strptime(fallback, fmt)
            except ValueError:
                continue
    return None


def parse_knowledge_file(path: Path, content_type: str, series: str):
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')

    title = path.stem
    if lines and lines[0].startswith('# '):
        title = lines[0][2:].strip()
        if title.upper().startswith('META-SUMMARY:'):
            title = title.split(':', 1)[1].strip()

    # Header block = everything before the first standalone '---' line
    header_lines = []
    body_start = len(lines)
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == '---':
            body_start = i + 1
            break
        header_lines.append(line)

    fields = {}
    for line in header_lines:
        m = HEADER_FIELD_RE.match(line.strip())
        if m:
            fields[m.group(1).strip().lower()] = m.group(2).strip()

    body = '\n'.join(lines[body_start:]).strip()

    byline = fields.get('guest') or fields.get('speaker') or fields.get('author')
    outlet = fields.get('channel') or fields.get('podcast') or fields.get('publisher')
    source = fields.get('source', '')
    source_url = fields.get('url') or (source if source.startswith('http') else '')
    if not outlet and source and not source.startswith('http'):
        outlet = source

    date_raw = (fields.get('date processed') or fields.get('date')
                or fields.get('published') or fields.get('processed'))
    filename_date_match = re.match(r'^(\d{4}(?:-\d{2}(?:-\d{2})?)?)', path.stem)
    fallback = filename_date_match.group(1) if filename_date_match else ''
    date_obj = parse_date(date_raw, fallback)
    if date_obj is None:
        mtime = path.stat().st_mtime
        date_obj = datetime.fromtimestamp(mtime)

    tags = re.findall(r'#([\w-]+)', fields.get('tags', ''))
    duration = normalize_duration(fields.get('duration', ''))
    word_count = len(body.split())
    reading_time = max(1, round(word_count / 200))
    is_meta = path.stem.startswith('_meta-summary')

    return {
        'title': title,
        'content_type': content_type,
        'series': series,
        'byline': byline or '',
        'outlet': outlet or '',
        'source_url': source_url,
        'duration': duration,
        'date': date_obj.strftime('%Y-%m-%d'),
        'tags': tags,
        'reading_time': reading_time,
        'is_meta': is_meta,
        'body': body,
    }


def normalize_duration(raw: str) -> str:
    """Normalize wildly inconsistent duration strings (raw seconds, '~85 minutes', etc) to 'N min'."""
    raw = raw.strip()
    if not raw:
        return ''
    if raw.isdigit():
        return f"{round(int(raw) / 60)} min"
    match = re.search(r'(\d+)\s*(?:seconds?|secs?)\b', raw, re.IGNORECASE)
    if match:
        return f"{round(int(match.group(1)) / 60)} min"
    match = re.search(r'(\d+)\s*(?:minutes?|mins?)\b', raw, re.IGNORECASE)
    if match:
        return f"{match.group(1)} min"
    match = re.search(r'(\d+)\s*(?:hours?|hrs?)\b', raw, re.IGNORECASE)
    if match:
        return f"{int(match.group(1)) * 60} min"
    return raw.lstrip('~').strip()


def yaml_escape(value: str) -> str:
    return value.replace('"', "'")


def write_jekyll_file(dest: Path, data: dict):
    tags_yaml = '[' + ', '.join(f'"{yaml_escape(t)}"' for t in data['tags']) + ']'
    front_matter = f"""---
title: "{yaml_escape(data['title'])}"
content_type: {data['content_type']}
series: "{yaml_escape(data['series'])}"
byline: "{yaml_escape(data['byline'])}"
outlet: "{yaml_escape(data['outlet'])}"
source_url: "{data['source_url']}"
duration: "{yaml_escape(data['duration'])}"
date: {data['date']}
tags: {tags_yaml}
reading_time: {data['reading_time']}
is_meta: {'true' if data['is_meta'] else 'false'}
---

{data['body']}
"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(front_matter, encoding='utf-8')


def sync_knowledge(force: bool = False) -> int:
    if not KNOWLEDGE_DIR.exists():
        print(f"Source directory not found: {KNOWLEDGE_DIR}")
        return 0

    synced = 0
    for content_type_dir in sorted(p for p in KNOWLEDGE_DIR.iterdir() if p.is_dir()):
        content_type = content_type_dir.name.rstrip('s')  # lectures -> lecture, podcasts -> podcast, etc.

        for source_file in sorted(content_type_dir.rglob('*.md')):
            if source_file.name in SKIP_FILES:
                continue

            rel = source_file.relative_to(content_type_dir)
            series = rel.parts[0] if len(rel.parts) > 1 else ''

            dest_file = WEBSITE_DIR / content_type_dir.name / rel

            if dest_file.exists() and not force:
                if source_file.stat().st_mtime <= dest_file.stat().st_mtime:
                    continue

            data = parse_knowledge_file(source_file, content_type, series)
            write_jekyll_file(dest_file, data)
            print(f"  ✓ {source_file} -> {dest_file}")
            synced += 1

    return synced


def main():
    parser = argparse.ArgumentParser(description='Sync knowledge/ to website/_knowledge/ for Jekyll')
    parser.add_argument('--force', action='store_true', help='Force overwrite existing files')
    args = parser.parse_args()

    print("=" * 60)
    print("Syncing knowledge base to website")
    print("=" * 60)

    total = sync_knowledge(force=args.force)

    print("\n" + "=" * 60)
    print(f"Done! Total synced: {total}")
    print("=" * 60)


if __name__ == '__main__':
    main()
