#!/usr/bin/env python3
"""
Simple preview server for the macro briefs website.
Renders Jekyll-style markdown to HTML without requiring Ruby.
"""
import http.server
import socketserver
import re
import os
from pathlib import Path
from urllib.parse import unquote

PORT = 4000
WEBSITE_DIR = Path(__file__).parent / 'website'

# Brand colors
COLORS = {
    'dark': '#040505',
    'blue': '#5597cb',
    'light_blue': '#aac3e3',
}

def load_css():
    css_file = WEBSITE_DIR / 'assets' / 'css' / 'style.css'
    if css_file.exists():
        return css_file.read_text()
    return ""

def parse_front_matter(content):
    """Parse YAML front matter from markdown using simple regex."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = {}
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    front_matter[key] = value
            body = parts[2].strip()
            return front_matter, body
    return {}, content

def markdown_to_html(md):
    """Simple markdown to HTML conversion."""
    html = md

    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Lists
    lines = html.split('\n')
    result = []
    in_list = False
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if line.strip() and not line.strip().startswith('<'):
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)
    if in_list:
        result.append('</ul>')

    return '\n'.join(result)

def render_header():
    return f'''
    <header class="site-header">
      <div class="container">
        <div class="header-content">
          <a href="/" class="logo">
            <div class="logo-mark">M</div>
            <div class="logo-text">
              <span class="logo-subtitle">The Daily</span>
              <span class="logo-title">Macro & Market Brief</span>
            </div>
          </a>
          <nav class="nav-links">
            <a href="/daily/">Daily</a>
            <a href="/weekly/">Weekly</a>
            <a href="/monthly/">Monthly</a>
          </nav>
        </div>
      </div>
    </header>
    <div class="accent-line"></div>
    '''

def render_footer():
    return f'''
    <footer class="site-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="footer-logo">M</div>
            <div>
              <div class="footer-text">The Daily Macro & Market Brief</div>
              <div class="footer-tagline">Cut through the noise. Get the macro story in 5 minutes.</div>
            </div>
          </div>
        </div>
      </div>
    </footer>
    '''

def render_page(title, content, css):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | The Daily Macro & Market Brief</title>
  <style>{css}</style>
</head>
<body>
  <div class="site-wrapper">
    {render_header()}
    <main class="main-content">
      {content}
    </main>
    {render_footer()}
  </div>
</body>
</html>'''

def render_brief(front_matter, body, css):
    title = front_matter.get('title', 'Brief')
    brief_type = front_matter.get('brief_type', 'daily')
    lead = front_matter.get('lead', '')
    day_name = front_matter.get('day_name', '')
    reading_time = front_matter.get('reading_time', 5)

    type_labels = {'daily': 'Daily Brief', 'weekly': 'Weekly Brief', 'monthly': 'Monthly Brief'}
    lead_subtitles = {
        'daily': 'What moved markets today, by order of importance.',
        'weekly': "The week's key themes and developments.",
        'monthly': 'What really mattered this month.'
    }

    header_html = f'''
    <header class="brief-header">
      <div class="container">
        <div class="brief-header-content">
          <div class="brief-meta">
            <div class="brief-type-label">{type_labels.get(brief_type, 'Brief')}</div>
            <h1 class="brief-date">{title}</h1>
          </div>
          <div class="brief-info">
            {f'<span>{day_name}</span>' if day_name else ''}
            <span>{reading_time} min read</span>
          </div>
        </div>
      </div>
    </header>
    <div class="accent-line"></div>
    '''

    content_html = f'''
    <div class="container">
      <article class="brief-content">
        <div class="brief-lead">
          <p>{lead}</p>
          <div class="brief-lead-subtitle">{lead_subtitles.get(brief_type, '')}</div>
        </div>
        <div class="brief-body">
          {markdown_to_html(body)}
        </div>
      </article>
    </div>
    '''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | The Daily Macro & Market Brief</title>
  <style>{css}</style>
</head>
<body>
  <div class="site-wrapper">
    {render_header().replace('class="brief-header"', '')}
    {header_html}
    <main class="main-content">
      {content_html}
    </main>
    {render_footer()}
  </div>
</body>
</html>'''

def render_index(brief_type, briefs, css):
    titles = {'daily': 'Daily Briefs', 'weekly': 'Weekly Briefs', 'monthly': 'Monthly Reviews'}
    descriptions = {
        'daily': "Each day's key market developments and macro insights, in 5 minutes.",
        'weekly': "The week's key themes and how stories evolved across sessions.",
        'monthly': 'What really mattered each month, cutting through the noise with hindsight.'
    }

    cards_html = ''
    for brief in sorted(briefs, key=lambda x: x.get('date', ''), reverse=True):
        title = brief.get('title', '')
        lead = brief.get('lead', '')[:150] + '...' if len(brief.get('lead', '')) > 150 else brief.get('lead', '')
        url = brief.get('url', '')
        reading_time = brief.get('reading_time', 5)

        cards_html += f'''
        <div class="brief-card">
          <a href="{url}">
            <div class="brief-card-date">{title}</div>
            <p class="brief-card-excerpt">{lead}</p>
            <div class="brief-card-meta">{reading_time} min read</div>
          </a>
        </div>
        '''

    content = f'''
    <div class="container">
      <section class="section-nav">
        <div class="section-tabs">
          <a href="/daily/" class="section-tab {'active' if brief_type == 'daily' else ''}">Daily</a>
          <a href="/weekly/" class="section-tab {'active' if brief_type == 'weekly' else ''}">Weekly</a>
          <a href="/monthly/" class="section-tab {'active' if brief_type == 'monthly' else ''}">Monthly</a>
        </div>
      </section>
      <header class="archive-header">
        <h1 class="archive-title">{titles.get(brief_type, 'Briefs')}</h1>
        <p class="archive-description">{descriptions.get(brief_type, '')}</p>
      </header>
      {cards_html}
    </div>
    '''

    return render_page(titles.get(brief_type, 'Briefs'), content, css)

def render_home(all_briefs, css):
    sections = ''
    for brief_type, briefs in all_briefs.items():
        titles = {'daily': 'Latest Daily Briefs', 'weekly': 'Latest Weekly Briefs', 'monthly': 'Monthly Reviews'}
        limit = 3 if brief_type == 'daily' else (2 if brief_type == 'weekly' else 1)

        cards = ''
        for brief in sorted(briefs, key=lambda x: x.get('date', ''), reverse=True)[:limit]:
            title = brief.get('title', '')
            lead = brief.get('lead', '')[:150] + '...' if len(brief.get('lead', '')) > 150 else brief.get('lead', '')
            url = brief.get('url', '')
            reading_time = brief.get('reading_time', 5)

            cards += f'''
            <div class="brief-card">
              <a href="{url}">
                <div class="brief-card-date">{title}</div>
                <p class="brief-card-excerpt">{lead}</p>
                <div class="brief-card-meta">{reading_time} min read</div>
              </a>
            </div>
            '''

        sections += f'''
        <section class="latest-section">
          <div class="latest-header">
            <h2 class="latest-title">{titles.get(brief_type, '')}</h2>
            <a href="/{brief_type}/" class="view-all">View All &rarr;</a>
          </div>
          {cards}
        </section>
        '''

    hero = f'''
    <section class="hero">
      <div class="container">
        <div class="hero-subtitle">The Daily</div>
        <h1 class="hero-title">Macro & Market Brief</h1>
        <p class="hero-tagline">Cut through the noise. Get the macro story in 5 minutes.</p>
      </div>
    </section>
    '''

    content = f'{hero}<div class="container">{sections}</div>'
    return render_page('Home', content, css)

def load_briefs(brief_type):
    """Load all briefs of a given type."""
    briefs = []
    brief_dir = WEBSITE_DIR / f'_{brief_type}'

    if brief_dir.exists():
        for md_file in brief_dir.glob('*.md'):
            content = md_file.read_text()
            front_matter, _ = parse_front_matter(content)
            front_matter['url'] = f'/{brief_type}/{md_file.stem}/'
            briefs.append(front_matter)

    return briefs

class BriefHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.css = load_css()
        super().__init__(*args, directory=str(WEBSITE_DIR), **kwargs)

    def do_GET(self):
        path = unquote(self.path)

        # Home page
        if path == '/' or path == '/index.html':
            all_briefs = {
                'daily': load_briefs('daily'),
                'weekly': load_briefs('weekly'),
                'monthly': load_briefs('monthly'),
            }
            html = render_home(all_briefs, self.css)
            self.send_html(html)
            return

        # Brief type index pages
        for brief_type in ['daily', 'weekly', 'monthly']:
            if path == f'/{brief_type}/' or path == f'/{brief_type}':
                briefs = load_briefs(brief_type)
                html = render_index(brief_type, briefs, self.css)
                self.send_html(html)
                return

            # Individual brief pages
            match = re.match(f'^/{brief_type}/([^/]+)/?$', path)
            if match:
                slug = match.group(1)
                md_file = WEBSITE_DIR / f'_{brief_type}' / f'{slug}.md'
                if md_file.exists():
                    content = md_file.read_text()
                    front_matter, body = parse_front_matter(content)
                    html = render_brief(front_matter, body, self.css)
                    self.send_html(html)
                    return

        # Static files (CSS, images)
        super().do_GET()

    def send_html(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

def main():
    os.chdir(WEBSITE_DIR)

    with socketserver.TCPServer(("", PORT), BriefHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"  Preview server running at http://localhost:{PORT}")
        print(f"{'='*60}")
        print(f"\n  Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    main()
