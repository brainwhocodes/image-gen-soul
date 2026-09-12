"""Validate a copied skill's routing, portability and record templates offline."""
from pathlib import Path
from urllib.parse import unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def markdown_links(path):
    """Return local file destinations; ignore remote URLs and same-page anchors."""
    content = path.read_text(encoding='utf-8')
    assert not re.search(r'(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/', content), f'Host path: {path}'
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if re.match(r'[a-z][a-z0-9+.-]*:', target, re.I) or target.startswith('#'):
            continue
        relative = unquote(target.split('#')[0].split('?')[0])
        assert not relative.startswith(('/', '\\')), f'Absolute link: {target}'
        destination = (path.parent / relative).resolve()
        assert destination.is_relative_to(ROOT), f'Link leaves package: {target}'
        assert destination.is_file(), f'Broken link in {path.relative_to(ROOT)}: {target}'
        yield destination


def check_skill(path, name):
    content = path.read_text(encoding='utf-8')
    assert content.startswith('---\n'), f'Missing frontmatter: {path}'
    metadata, body = content[4:].split('\n---\n', 1)
    assert re.search(rf'^name: {re.escape(name)}$', metadata, re.M), f'Wrong name: {path}'
    assert re.search(r'^description:\s*>-?\n\s+\S', metadata, re.M), f'Missing description: {path}'
    assert re.search(r'^  version: "\d+\.\d+\.\d+"$', metadata, re.M), f'Missing version: {path}'
    return body


def main():
    core = ROOT / 'SKILL.md'
    body = check_skill(core, 'image-gen-soul')
    check_skill(ROOT / 'skills/redesign/SKILL.md', 'redesign')
    assert len(body.split()) <= 1600, 'Main skill should stay a concise task router'
    documents = [core, ROOT / 'README.md', *sorted((ROOT / 'guides').glob('*.md')),
                 ROOT / 'skills/redesign/SKILL.md', *sorted((ROOT / 'templates').glob('*.md'))]
    links = {path: set(markdown_links(path)) for path in documents}
    guides = set((ROOT / 'guides').glob('*.md'))
    assert guides <= links[core], 'Every focused guide must have a route from SKILL.md'
    assert ROOT / 'skills/redesign/SKILL.md' in links[core], 'REDESIGN is not routed'
    assert core in links[ROOT / 'skills/redesign/SKILL.md'], 'REDESIGN must link to its parent'
    assert all(links[guide] for guide in guides), 'A guide has no usable next-step links'
    job = json.loads((ROOT / 'templates/job.json').read_text(encoding='utf-8'))
    assert {'references', 'brief', 'generation', 'color_correction', 'production', 'qa'} <= job.keys()
    inventory = json.loads((ROOT / 'templates/page-inventory.json').read_text(encoding='utf-8'))
    assert {'navigation', 'pages', 'variations', 'brand_kit', 'image_assets'} <= inventory.keys()
    assert {'screenshot', 'sha256', 'captured_at', 'reviewed_at'} <= inventory['brand_kit'].keys()
    for relative in ['requirements.txt', 'CHANGELOG.md', 'THIRD_PARTY_NOTICES.md',
                     'scripts/color_pipeline.py', 'scripts/palette_extract.py',
                     'scripts/writing/lint.mjs', 'scripts/writing/cliche-lint.mjs']:
        assert (ROOT / relative).is_file(), f'Missing helper: {relative}'
    print(f'PASS: {len(body.split())}-word router, {len(guides)} routed guides, '
          f'{len(documents)} portable Markdown documents and job templates.')


if __name__ == '__main__':
    main()
