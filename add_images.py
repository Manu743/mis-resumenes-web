#!/usr/bin/env python3
"""Copy referenced images to parasitologia/img/ and add them to HTML files."""

import shutil
from pathlib import Path

BASE = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\mis-resumenes-web")
PARA = BASE / "parasitologia"
SRC = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\Parasitologia")
IMG = PARA / "img"
IMG.mkdir(exist_ok=True)

# Image mapping: (source_folder, page_number, output_name)
IMAGES = [
    # Tema 1 — Generalidades
    ("Tema 1", 15, "tema1-p15-mecanismos-transmision.png"),
    ("Tema 1", 17, "tema1-p17-factores-riesgo.png"),
    # Tema 2 — Amebiasis (ciclo de vida)
    ("Tema 2", 5, "tema2-p05-ciclo-vida.png"),
    ("Tema 2", 6, "tema2-p06-ciclo-vida.png"),
    ("Tema 2", 7, "tema2-p07-ciclo-vida.png"),
    ("Tema 2", 8, "tema2-p08-ciclo-vida.png"),
    ("Tema 2", 9, "tema2-p09-ciclo-vida.png"),
    ("Tema 2", 10, "tema2-p10-ciclo-vida.png"),
    ("Tema 2", 11, "tema2-p11-ciclo-vida.png"),
    # Tema 2 — Amebiasis (otros)
    ("Tema 2", 21, "tema2-p21-factores-riesgo.png"),
    ("Tema 2", 26, "tema2-p26-diagnostico-diferencial.png"),
    # Tema 4 — Amebiasis General
    ("Tema 4", 30, "tema4-p30-norma-bolivia.png"),
]

# Build page-to-file mapping
def get_file(src_folder, page_num):
    src_dir = SRC / src_folder
    files = sorted(src_dir.glob("*.png"), key=lambda f: f.name)
    if page_num <= len(files):
        return files[page_num - 1]
    return None

# Copy images
for src_folder, page_num, out_name in IMAGES:
    src_file = get_file(src_folder, page_num)
    if src_file:
        dst = IMG / out_name
        shutil.copy2(src_file, dst)
        print(f"COPY: {src_file.name} -> img/{out_name}")
    else:
        print(f"MISS: {src_folder} page {page_num}")

# Update HTML files — replace comments with img tags
HTML_UPDATES = {
    "generalidades.html": [
        (
            '<!-- Revisar imagen página 15: gráfico explicativo de mecanismos de transmisión -->',
            '<div class="content-section">\n      <h3>Referencia visual — Mecanismos de transmisión</h3>\n      <img src="img/tema1-p15-mecanismos-transmision.png" alt="Mecanismos de transmisión de parásitos" style="max-width:100%; border-radius:8px; border:1px solid #ddd;">\n    </div>'
        ),
        (
            '<!-- Revisar imagen página 17: gráfico explicativo de factores de riesgo -->',
            '<div class="content-section">\n      <h3>Referencia visual — Factores de riesgo</h3>\n      <img src="img/tema1-p17-factores-riesgo.png" alt="Factores de riesgo de parasitosis" style="max-width:100%; border-radius:8px; border:1px solid #ddd;">\n    </div>'
        ),
    ],
    "amebiasis.html": [
        (
            '<!-- Revisar imágenes páginas 5 a 11: diagrama del ciclo de vida de E. histolytica, texto parcialmente ilegible por OCR -->',
            '<div class="content-section">\n      <h3>Diagrama — Ciclo de vida de <em>E. histolytica</em></h3>\n      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1rem; margin-top:1rem;">\n        <img src="img/tema2-p05-ciclo-vida.png" alt="Ciclo de vida - parte 1" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n        <img src="img/tema2-p06-ciclo-vida.png" alt="Ciclo de vida - parte 2" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n        <img src="img/tema2-p07-ciclo-vida.png" alt="Ciclo de vida - parte 3" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n        <img src="img/tema2-p08-ciclo-vida.png" alt="Ciclo de vida - parte 4" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n        <img src="img/tema2-p09-ciclo-vida.png" alt="Ciclo de vida - parte 5" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n        <img src="img/tema2-p10-ciclo-vida.png" alt="Ciclo de vida - parte 6" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n        <img src="img/tema2-p11-ciclo-vida.png" alt="Ciclo de vida - parte 7" style="width:100%; border-radius:8px; border:1px solid #ddd;">\n      </div>\n    </div>'
        ),
        (
            'SIRROFAGIA <!-- Revisar imagen página 21: verificar si se refiere a cirrhosis/alcoholismo/síndrome de mala absorción -->',
            'SIRROFAGIA\n      <div style="margin-top:0.5rem;"><img src="img/tema2-p21-factores-riesgo.png" alt="Factores de riesgo - detalle" style="max-width:100%; border-radius:8px; border:1px solid #ddd;"></div>'
        ),
        (
            '<!-- Revisar imagen página 26: lista completa de virus del diagnóstico diferencial, texto ilegible por OCR -->',
            '<div style="margin-top:0.5rem;"><img src="img/tema2-p26-diagnostico-diferencial.png" alt="Diagnóstico diferencial - virus" style="max-width:100%; border-radius:8px; border:1px solid #ddd;"></div>'
        ),
    ],
    "amebiasis-general.html": [
        (
            '<!-- Revisar imagen página 30: norma boliviana sobre tratamiento de amebiasis, texto ilegible en la captura -->',
            '<div class="content-section">\n      <h3>Referencia visual — Norma en Bolivia</h3>\n      <img src="img/tema4-p30-norma-bolivia.png" alt="Norma Bolivia - tratamiento amebiasis" style="max-width:100%; border-radius:8px; border:1px solid #ddd;">\n    </div>'
        ),
    ],
}

for html_file, replacements in HTML_UPDATES.items():
    fpath = PARA / html_file
    content = fpath.read_text(encoding="utf-8")
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"UPDATE: {html_file} — replaced comment with image")
        else:
            print(f"WARN: {html_file} — comment not found: {old[:50]}...")
    fpath.write_text(content, encoding="utf-8")

print("\nDone!")
