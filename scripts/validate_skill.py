"""Validate the portable skill package without network access or generators."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    core = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    assert core.startswith('---\n'), 'Missing skill frontmatter'
    assert re.search(r'^name: image-gen-soul$', core, re.M), 'Unexpected skill name'
    for phrase in ['No emoji icons', 'No eyebrows', '14px', '4.5:1', '3:1', 'cursor: pointer', 'No sliders', '200%', '320']:
        assert phrase in core, f'Missing interface rule: {phrase}'
    for phrase in ['Ask before generating UI mockups', 'generated logo', 'font imports', 'screenshot hash', 'marketing and product', 'Attach the inspected brand-kit screenshot']:
        assert phrase in core, f'Missing brand-first requirement: {phrase}'
    references = {path.rstrip('.') for path in re.findall(r'(?:guides|scripts|templates)/[\w.-]+', core)}
    references.update(['templates/site-brief.md', 'requirements.txt', 'README.md', 'CHANGELOG.md'])
    for relative in references:
        assert (ROOT / relative).is_file(), f'Missing referenced file: {relative}'
    json.loads((ROOT / 'templates/job.json').read_text(encoding='utf-8'))
    for path in [ROOT/'SKILL.md', ROOT/'README.md', *(ROOT/'guides').glob('*.md')]:
        text = path.read_text(encoding='utf-8')
        assert 'C:\\Users\\' not in text and '/Users/' not in text, f'Local path in {path.name}'
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in target and not target.startswith('#'):
                assert not target.startswith('/'), f'Host-local link in {path.name}: {target}'
                assert (path.parent / target.split('#')[0]).is_file(), f'Broken link in {path.name}: {target}'
    print(f'PASS: core rules, {len(references)} package references, Markdown links and job template.')

if __name__ == '__main__':
    main()
