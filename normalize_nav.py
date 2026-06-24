#!/usr/bin/env python3
"""Normalize navigation across all HTML pages."""
import re
from pathlib import Path

BASE = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\mis-resumenes-web")

# The correct nav for each section
NAV_ITEMS = [
    ('{prefix}index.html', 'Inicio'),
    ('{prefix}bioquimica/index.html', 'Bioquímica'),
    ('{prefix}bromatologia/index.html', 'Bromatología'),
    ('{prefix}educacion-alimentaria/index.html', 'Educación Alimentaria'),
    ('{prefix}nutricion-2/index.html', 'Nutrición 2'),
    ('{prefix}parasitologia/index.html', 'Parasitología'),
]

def get_prefix(fpath):
    """Get the relative prefix based on depth."""
    rel = fpath.relative_to(BASE)
    parts = len(rel.parts) - 1  # subtract filename
    return '../' * parts if parts > 0 else ''

def fix_nav(fpath):
    content = fpath.read_text(encoding='utf-8')
    prefix = get_prefix(fpath)
    
    # Find the nav block
    nav_match = re.search(r'(<nav class="main-nav">\s*<ul>)(.*?)(</ul>\s*</nav>)', content, re.DOTALL)
    if not nav_match:
        return False
    
    old_nav = nav_match.group(0)
    
    # Determine which item is "active" based on the file's section
    rel = fpath.relative_to(BASE)
    section = rel.parts[0] if len(rel.parts) > 1 else ''
    
    # Build new nav
    items = []
    for url_template, label in NAV_ITEMS:
        url = url_template.format(prefix=prefix)
        # Check if this is the active section
        is_active = False
        if section and section in url:
            is_active = True
        if not section and 'index.html' in url and url.endswith('index.html'):
            # Main index - Inicio is active
            if label == 'Inicio':
                is_active = True
        
        if is_active:
            items.append(f'          <li><a href="{url}" class="active">{label}</a></li>')
        else:
            items.append(f'          <li><a href="{url}">{label}</a></li>')
    
    new_nav = f'''<nav class="main-nav">
        <ul>
{chr(10).join(items)}
        </ul>
      </nav>'''
    
    new_content = content[:nav_match.start()] + new_nav + content[nav_match.end():]
    
    if new_content != content:
        fpath.write_text(new_content, encoding='utf-8')
        return True
    return False

# Process all HTML files
count = 0
for fpath in sorted(BASE.rglob("*.html")):
    if "parasitologia" in str(fpath).lower() and "img" in str(fpath).lower():
        continue
    if fix_nav(fpath):
        count += 1
        print(f"FIXED: {fpath.relative_to(BASE)}")
    else:
        print(f"OK: {fpath.relative_to(BASE)}")

print(f"\nFixed {count} files")
