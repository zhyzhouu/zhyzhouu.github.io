#!/usr/bin/env python3
"""Build the static homepage using one JSON file per paper (Python 3 only)."""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def esc(value):
    return html.escape(str(value), quote=True)

def render_author(name, coauthors):
    label = '<strong>'+esc(name)+'</strong>' if name == 'Zhenyu Zhou' else esc(name)
    url = coauthors.get(name.strip().casefold(), '')
    if url:
        return f'<a href="{esc(url)}" target="_blank" rel="noreferrer">{label}</a>'
    return label

def render(p, placeholders, coauthors):
    pid = p['id']
    url = esc(p['arxiv'])
    placeholder = placeholders.get(p.get('placeholder'), {})
    cls = placeholder.get('cssClass', '')
    image = placeholder.get('content', '<span class="thumb-label">Figure coming soon</span>')
    if p.get('image'):
        if not (ROOT / p['image']).is_file():
            raise ValueError(f'{pid}: image not found')
        cls = ''
        image = f'<img src="{esc(p["image"])}" alt="{esc(p.get("imageAlt") or p["title"])}" loading="lazy">'
    meta = '<span class="venue">' + esc(p['venue']) + '</span>'
    if p.get('distinction'):
        meta += '<span class="distinction">' + esc(p['distinction']) + '</span>'
    authors = ', '.join(render_author(a, coauthors) for a in p['authors'])
    tldr = '<p class="paper-tldr"><strong>TL;DR</strong> '+esc(p['tldr'])+'</p>' if p.get('tldr', '').strip() else ''
    buttons, panels = [], []
    for kind, label, field in [('abs', 'Abs', 'abstract'), ('bib', 'Bib', 'bibtex')]:
        value = p.get(field, '')
        disabled = '' if value else ' disabled'
        buttons.append(f'<button class="paper-action panel-toggle" type="button" aria-expanded="false" aria-controls="{kind}-{pid}"{disabled}>{label}</button>')
        body = '<pre><code>'+esc(value)+'</code></pre>' if kind == 'bib' else '<p>'+esc(value)+'</p>'
        panelcls = 'paper-panel bib-panel' if kind == 'bib' else 'paper-panel'
        panels.append(f'<div class="{panelcls}" id="{kind}-{pid}" hidden>{body}</div>')
    for label, field in [('arXiv', 'arxiv'), ('Code', 'code')]:
        if p.get(field):
            buttons.append(f'<a class="paper-action" href="{esc(p[field])}" target="_blank" rel="noreferrer">{label}</a>')
        else:
            buttons.append(f'<button class="paper-action" type="button" disabled title="Link coming soon">{label}</button>')
    return f'''        <article class="paper">
          <button class="paper-thumb {cls}" type="button" aria-label="Enlarge figure: {esc(p['title'])}" aria-haspopup="dialog"{'' if p.get('image') else ' disabled'}>{image}</button>
          <div class="paper-body">
            <div class="paper-meta">{meta}</div>
            <h3><a href="{url}" target="_blank" rel="noreferrer">{esc(p['title'])}</a></h3>
            <p class="authors">{authors}</p>
            {tldr}
            <div class="paper-links">{''.join(buttons)}</div>
          </div>
          {''.join(panels)}
        </article>'''

def main():
    order = json.loads((ROOT/'publications/order.json').read_text())
    if len(order) != len(set(order)):
        raise ValueError('Duplicate ID in order.json')
    placeholders = json.loads((ROOT/'templates/thumbnails.json').read_text())
    author_data = json.loads((ROOT/'coauthors.json').read_text())
    coauthors = {}
    for name, url in author_data.items():
        if not isinstance(url, str) or (url and not url.startswith(('https://', 'http://'))):
            raise ValueError(f'{name}: author URL must be an HTTP(S) URL or empty')
        key = name.strip().casefold()
        if key in coauthors:
            raise ValueError(f'Duplicate author name: {name}')
        coauthors[key] = url.strip()
    cards = []
    for pid in order:
        if not isinstance(pid, str) or not pid.replace('-', '').isalnum():
            raise ValueError('IDs must contain letters, digits or hyphens')
        p = json.loads((ROOT/'publications'/f'{pid}.json').read_text())
        if p['id'] != pid:
            raise ValueError(f'{pid}: filename and id must match')
        for field in ('title', 'authors', 'venue', 'arxiv'):
            if not p.get(field):
                raise ValueError(f'{pid}: missing {field}')
        cards.append(render(p, placeholders, coauthors))
    template = (ROOT/'templates/index.html').read_text()
    if template.count('{{PUBLICATIONS}}') != 1:
        raise ValueError('Template needs exactly one PUBLICATIONS placeholder')
    output = template.replace('{{PUBLICATIONS}}', '\n\n'.join(cards))
    output = '\n'.join(line.rstrip() for line in output.splitlines()) + '\n'
    if '--check' in sys.argv:
        if (ROOT/'index.html').read_text() != output:
            raise SystemExit('index.html is outdated; run python3 build.py')
        print(f'Checked {len(cards)} papers; generated page is up to date.')
    else:
        (ROOT/'index.html').write_text(output)
        print(f'Generated index.html with {len(cards)} papers.')

if __name__ == '__main__':
    main()
