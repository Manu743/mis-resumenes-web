import re
from pathlib import Path
base = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\mis-resumenes-web")
for f in sorted(base.rglob("*.html")):
    if "img" in str(f):
        continue
    content = f.read_text(encoding="utf-8")
    nav_match = re.search(r'<nav class="main-nav">(.*?)</nav>', content, re.DOTALL)
    if nav_match:
        items = re.findall(r"<li><a[^>]*>([^<]+)</a></li>", nav_match.group(1))
        if len(items) != len(set(items)):
            dupes = [x for x in set(items) if items.count(x) > 1]
            print(f"DUPE: {f.relative_to(base)}: {dupes}")
print("Done")
