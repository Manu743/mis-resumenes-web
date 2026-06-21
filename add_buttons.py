#!/usr/bin/env python3
"""Add Export PDF button to all resume HTML pages."""

import re
from pathlib import Path

BASE = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\mis-resumenes-web")

BUTTON = """
    <button class="btn-export" onclick="window.print()">
      <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
      Exportar a PDF
    </button>"""

# All content pages (excluding index pages)
PAGES = [
    # Bioquímica
    "bioquimica/agua.html",
    "bioquimica/ph.html",
    "bioquimica/lipidos.html",
    "bioquimica/carbohidratos.html",
    "bioquimica/cadena-respiratoria.html",
    # Bromatología
    "bromatologia/los-alimentos.html",
    "bromatologia/alteracion-alimentos.html",
    "bromatologia/principios-conservacion.html",
    "bromatologia/fundamentos-conservacion.html",
    "bromatologia/metodos-control.html",
    "bromatologia/control-calidad.html",
    # Educación Alimentaria
    "educacion-alimentaria/analisis-historico.html",
    "educacion-alimentaria/bases-conceptuales.html",
    "educacion-alimentaria/cultura-alimentaria.html",
    "educacion-alimentaria/elementos-culturales.html",
    "educacion-alimentaria/formacion-nutricionista.html",
    "educacion-alimentaria/grupos-poblacion.html",
    "educacion-alimentaria/influencia-cambios.html",
    "educacion-alimentaria/instrumentos-diagnostico.html",
    "educacion-alimentaria/variables-indicadores.html",
    "educacion-alimentaria/diagnostico-ean.html",
]

# Pattern: find the closing </div> of topic-header (after topic-meta)
pattern = re.compile(r'(<p class="topic-meta">.*?</p>\s*</div>)')

count = 0
for rel_path in PAGES:
    fpath = BASE / rel_path
    if not fpath.exists():
        print(f"SKIP: {rel_path}")
        continue

    content = fpath.read_text(encoding="utf-8")

    # Check if button already exists
    if "btn-export" in content:
        print(f"SKIP (already has button): {rel_path}")
        continue

    # Insert button after topic-header closing div
    new_content = pattern.sub(r'\1' + BUTTON, content, count=1)

    if new_content == content:
        print(f"WARN: pattern not matched in {rel_path}")
        continue

    fpath.write_text(new_content, encoding="utf-8")
    count += 1
    print(f"OK: {rel_path}")

print(f"\nDone! Added button to {count} pages.")
