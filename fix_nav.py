#!/usr/bin/env python3
import re
from pathlib import Path

base = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\mis-resumenes-web")

# Fix Nutrición 2 pages - remove duplicate nav item
pattern = re.compile(r'          <li><a href="\.\./nutricion-2/index\.html">Nutrición 2</a></li>\n')
for f in (base / "nutricion-2").glob("*.html"):
    content = f.read_text(encoding="utf-8")
    new = pattern.sub("", content)
    if new != content:
        f.write_text(new, encoding="utf-8")
        print(f"FIXED: {f.name}")
    else:
        print(f"OK: {f.name} (no duplicate)")

# Also check other sections for duplicate nav
for section in ["bioquimica", "bromatologia", "educacion-alimentaria", "parasitologia"]:
    for f in (base / section).glob("*.html"):
        content = f.read_text(encoding="utf-8")
        # Count occurrences of each nav item
        for item in ["Bioquímica", "Bromatología", "Educación Alimentaria", "Nutrición 2", "Parasitología"]:
            count = content.count(f">{item}<")
            if count > 1:
                print(f"WARN: {f.name} has {count}x {item}")
