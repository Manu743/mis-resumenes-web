#!/usr/bin/env python3
"""Generate PDFs from Nutrición 2 HTML pages using Edge headless."""

import subprocess
from pathlib import Path

BASE = Path(__file__).parent / "nutricion-2"
OUTPUT_DIR = BASE / "pdfs"
OUTPUT_DIR.mkdir(exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

PAGES = [
    ("evolucion-contexto-alimentario.html", "Tema 1 - Evolucion Humano y Contexto Alimentario"),
    ("determinantes-biologicos-culturales.html", "Tema 2 - Determinantes Biologicos y Culturales del Ciclo Vital"),
    ("analisis-alimentacion-ciclo-vital.html", "Tema 3 - Analisis de la Alimentacion en el Ciclo Vital"),
    ("nutricion-prevencion-enfermedades.html", "Tema 4 - Nutricion y Prevencion de Enfermedades"),
    ("tema1-nutricion-embarazo.html", "Tema 5 - Nutricion Durante la Etapa de Embarazo"),
]

for html_file, title in PAGES:
    html_path = BASE / html_file
    if not html_path.exists():
        print(f"SKIP: {html_file} not found")
        continue

    pdf_path = OUTPUT_DIR / f"{title}.pdf"
    print(f"Generating: {title}...")

    # Use file:// URL for Edge
    file_url = html_path.as_uri()

    result = subprocess.run(
        [
            EDGE,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--print-to-pdf=" + str(pdf_path),
            "--print-to-pdf-no-header",
            file_url,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"  -> {pdf_path.name} ({size_kb:.0f} KB)")
    else:
        print(f"  FAILED: {result.stderr[:200]}")

print(f"\nDone! PDFs at: {OUTPUT_DIR}")
