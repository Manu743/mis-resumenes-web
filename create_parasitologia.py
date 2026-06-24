#!/usr/bin/env python3
"""Create Parasitología section and update site navigation."""

from pathlib import Path
import re

BASE = Path(r"C:\Users\maren\OneDrive\Documentos\Resumenes\mis-resumenes-web")
PARA = BASE / "parasitologia"
PARA.mkdir(exist_ok=True)

# The nav HTML to add Parasitología
NAV_ITEM = '          <li><a href="../parasitologia/index.html">Parasitología</a></li>\n'
NAV_ITEM_ACTIVE = '          <li><a href="../parasitologia/index.html" class="active">Parasitología</a></li>\n'

# ============================================
# 1. Create section index
# ============================================
(PARA / "index.html").write_text('''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Parasitología — Mis Resúmenes</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <div class="site-title"><a href="../index.html">Mis Resúmenes</a></div>
      <nav class="main-nav">
        <ul>
          <li><a href="../index.html">Inicio</a></li>
          <li><a href="../bioquimica/index.html">Bioquímica</a></li>
          <li><a href="../bromatologia/index.html">Bromatología</a></li>
          <li><a href="../educacion-alimentaria/index.html">Educación Alimentaria</a></li>
          <li><a href="../nutricion-2/index.html">Nutrición 2</a></li>
          <li><a href="index.html" class="active">Parasitología</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <nav class="breadcrumbs">
    <a href="../index.html">Inicio</a><span class="separator">›</span><span class="current">Parasitología</span>
  </nav>

  <main class="main-content">
    <div class="subject-hero">
      <h1>Parasitología</h1>
      <p>Estudio de los parásitos, su relación con los hospedadores, ciclos de vida, patogenia, diagnóstico y tratamiento.</p>
    </div>

    <div class="card-grid">
      <div class="card">
        <div class="card-body">
          <h2 class="card-title"><a href="generalidades.html">Tema 1 — Generalidades de la Parasitología</a></h2>
          <p class="card-text">Definiciones, clasificación de parásitos, terminología (huésped, vector, reservorio), ciclos de vida y mecanismos de transmisión.</p>
        </div>
        <div class="card-footer">
          <a href="generalidades.html">Leer más →</a>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <h2 class="card-title"><a href="amebiasis.html">Tema 2 — Amebiasis (Entamoeba histolytica)</a></h2>
          <p class="card-text">Ciclo de vida, virulencia, patogenia, amebiasis intestinal y extraintestinal, diagnóstico diferencial y tratamiento.</p>
        </div>
        <div class="card-footer">
          <a href="amebiasis.html">Leer más →</a>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <h2 class="card-title"><a href="giardia.html">Tema 3 — Giardia lamblia</a></h2>
          <p class="card-text">Clasificación taxonómica, morfología, patogenia, síntomas, diagnóstico y tratamiento de la giardiasis.</p>
        </div>
        <div class="card-footer">
          <a href="giardia.html">Leer más →</a>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <h2 class="card-title"><a href="amebiasis-general.html">Tema 4 — Amebiasis General</a></h2>
          <p class="card-text">Agente etiológico, anatomía patológica, epidemiología, clínica, diagnóstico, terapia y profilaxis de la amebiasis.</p>
        </div>
        <div class="card-footer">
          <a href="amebiasis-general.html">Leer más →</a>
        </div>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <p>&copy; 2026 Mis Resúmenes Académicos. Todos los derechos reservados.</p>
  </footer>

</body>
</html>
''', encoding="utf-8")

print("OK: index.html")

# ============================================
# Helper: wrap markdown-like content into HTML
# ============================================
def md_to_html(md_text, title, subtitle):
    """Simple md to html for our specific content."""
    lines = md_text.split("\n")
    html_parts = []
    in_table = False
    in_list = False
    in_ol = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            if in_list:
                html_parts.append("      </ul>")
                in_list = False
            if in_ol:
                html_parts.append("      </ol>")
                in_ol = False
            if in_table:
                html_parts.append("        </tbody>\n      </table>")
                in_table = False
            html_parts.append("")
            continue
        
        # HTML comments - pass through
        if stripped.startswith("<!--"):
            html_parts.append(f"    {stripped}")
            continue
        
        # Horizontal rule
        if stripped == "---":
            continue
        
        # Headers
        if stripped.startswith("# ") and not stripped.startswith("## "):
            continue  # skip top-level, we use our own
        if stripped.startswith("## "):
            if in_list:
                html_parts.append("      </ul>")
                in_list = False
            if in_table:
                html_parts.append("        </tbody>\n      </table>")
                in_table = False
            heading = stripped[3:].strip()
            html_parts.append(f"      <h2>{heading}</h2>")
            continue
        if stripped.startswith("### "):
            if in_list:
                html_parts.append("      </ul>")
                in_list = False
            heading = stripped[4:].strip()
            html_parts.append(f"      <h3>{heading}</h3>")
            continue
        if stripped.startswith("#### "):
            if in_list:
                html_parts.append("      </ul>")
                in_list = False
            heading = stripped[5:].strip()
            html_parts.append(f"      <h4>{heading}</h4>")
            continue
        
        # Table
        if stripped.startswith("|") and "---" in stripped:
            continue  # skip table separator
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                html_parts.append("      <table>")
                html_parts.append("        <thead>")
                html_parts.append("          <tr>")
                for c in cells:
                    html_parts.append(f"            <th>{c}</th>")
                html_parts.append("          </tr>")
                html_parts.append("        </thead>")
                html_parts.append("        <tbody>")
                in_table = True
            else:
                html_parts.append("          <tr>")
                for c in cells:
                    html_parts.append(f"            <td>{c}</td>")
                html_parts.append("          </tr>")
            continue
        
        # Unordered list
        if stripped.startswith("- "):
            if not in_list:
                if in_ol:
                    html_parts.append("      </ol>")
                    in_ol = False
                html_parts.append("      <ul>")
                in_list = True
            content = stripped[2:].strip()
            # Handle bold
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'_(.+?)_', r'<em>\1</em>', content)
            html_parts.append(f"        <li>{content}</li>")
            continue
        
        # Ordered list
        if re.match(r'^\d+\.\s', stripped):
            if not in_ol:
                if in_list:
                    html_parts.append("      </ul>")
                    in_list = False
                html_parts.append("      <ol>")
                in_ol = True
            content = re.sub(r'^\d+\.\s', '', stripped)
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'_(.+?)_', r'<em>\1</em>', content)
            html_parts.append(f"        <li>{content}</li>")
            continue
        
        # Close lists if we reach here
        if in_list:
            html_parts.append("      </ul>")
            in_list = False
        if in_ol:
            html_parts.append("      </ol>")
            in_ol = False
        if in_table:
            html_parts.append("        </tbody>\n      </table>")
            in_table = False
        
        # Regular paragraph
        content = stripped
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'_(.+?)_', r'<em>\1</em>', content)
        # Handle blockquotes
        if content.startswith("> "):
            content = content[2:]
            html_parts.append(f"      <blockquote><p>{content}</p></blockquote>")
        else:
            html_parts.append(f"      <p>{content}</p>")
    
    # Close any open tags
    if in_list:
        html_parts.append("      </ul>")
    if in_ol:
        html_parts.append("      </ol>")
    if in_table:
        html_parts.append("        </tbody>\n      </table>")
    
    body = "\n".join(html_parts)
    
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Parasitología</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <div class="site-title"><a href="../index.html">Mis Resúmenes</a></div>
      <nav class="main-nav">
        <ul>
          <li><a href="../index.html">Inicio</a></li>
          <li><a href="../bioquimica/index.html">Bioquímica</a></li>
          <li><a href="../bromatologia/index.html">Bromatología</a></li>
          <li><a href="../educacion-alimentaria/index.html">Educación Alimentaria</a></li>
          <li><a href="../nutricion-2/index.html">Nutrición 2</a></li>
          <li><a href="index.html" class="active">Parasitología</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <nav class="breadcrumbs">
    <a href="../index.html">Inicio</a><span class="separator">›</span>
    <a href="index.html">Parasitología</a><span class="separator">›</span>
    <span class="current">{title}</span>
  </nav>

  <main class="main-content">
    <div class="topic-header">
      <h1>{title}</h1>
      <p class="topic-meta">{subtitle}</p>
    </div>

    <button class="btn-export" onclick="window.print()">
      <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
      Exportar a PDF
    </button>

{body}

  </main>

  <footer class="site-footer">
    <p>&copy; 2026 Mis Resúmenes Académicos. Todos los derechos reservados.</p>
  </footer>

</body>
</html>
'''

# ============================================
# 2. Create Tema 1 — Generalidades
# ============================================
md1 = (BASE.parent / "Parasitologia" / "Tema_1_Parasitologia.md").read_text(encoding="utf-8")
# Remove the top heading
md1 = re.sub(r'^# .+\n+', '', md1, count=1)
html1 = md_to_html(md1, "Tema 1 — Generalidades de la Parasitología", "Parasitología — Conceptos fundamentales")
(PARA / "generalidades.html").write_text(html1, encoding="utf-8")
print("OK: generalidades.html")

# ============================================
# 3. Create Tema 2 — Amebiasis
# ============================================
md2 = (BASE.parent / "Parasitologia" / "Tema_2_Parasitologia.md").read_text(encoding="utf-8")
md2 = re.sub(r'^# .+\n+', '', md2, count=1)
html2 = md_to_html(md2, "Tema 2 — Amebiasis (Entamoeba histolytica)", "Parasitología — Entamoeba histolytica")
(PARA / "amebiasis.html").write_text(html2, encoding="utf-8")
print("OK: amebiasis.html")

# ============================================
# 4. Create Tema 3 — Giardia
# ============================================
md3 = (BASE.parent / "Parasitologia" / "Tema_3_Parasitologia.md").read_text(encoding="utf-8")
md3 = re.sub(r'^# .+\n+', '', md3, count=1)
# Remove the blockquote intro
md3 = re.sub(r'^> Transcripción.*\n> Fuente.*\n+', '', md3, count=1)
html3 = md_to_html(md3, "Tema 3 — Giardia lamblia", "Parasitología — Protozoario flagelado")
(PARA / "giardia.html").write_text(html3, encoding="utf-8")
print("OK: giardia.html")

# ============================================
# 5. Create Tema 4 — Amebiasis General
# ============================================
md4 = (BASE.parent / "Parasitologia" / "Tema_4_Parasitologia_General.md").read_text(encoding="utf-8")
md4 = re.sub(r'^# .+\n+', '', md4, count=1)
html4 = md_to_html(md4, "Tema 4 — Amebiasis General", "Parasitología — Dra. Melani Garron")
(PARA / "amebiasis-general.html").write_text(html4, encoding="utf-8")
print("OK: amebiasis-general.html")

# ============================================
# 6. Update navigation in ALL existing pages
# ============================================
nav_pattern = re.compile(r'(<li><a href="\.\./nutricion-2/index\.html">Nutrición 2</a></li>\n)')

# Find all HTML files
all_html = list(BASE.rglob("*.html"))
updated = 0
for fpath in all_html:
    if "parasitologia" in str(fpath).lower():
        continue
    content = fpath.read_text(encoding="utf-8")
    if "Parasitología" in content:
        continue  # already updated
    
    # Check if it has the nav
    if nav_pattern.search(content):
        # Determine which nav item to use (active or not)
        if "parasitologia" in str(fpath).lower():
            new_nav = NAV_ITEM_ACTIVE
        else:
            new_nav = NAV_ITEM
        new_content = nav_pattern.sub(r'\1' + new_nav, content)
        fpath.write_text(new_content, encoding="utf-8")
        updated += 1

print(f"OK: Updated navigation in {updated} files")

# ============================================
# 7. Add Parasitología card to main index
# ============================================
idx = (BASE / "index.html").read_text(encoding="utf-8")
if "Parasitología" not in idx:
    card = '''
      <!-- Parasitología -->
      <div class="card">
        <div class="card-body">
          <span class="card-subject">Materia</span>
          <h2 class="card-title"><a href="parasitologia/index.html">Parasitología</a></h2>
          <p class="card-text">
            Estudio de los parásitos, sus ciclos de vida, patogenia,
            diagnóstico y tratamiento.
          </p>
        </div>
        <div class="card-footer">
          <a href="parasitologia/index.html">Ver temas →</a>
        </div>
      </div>'''
    # Insert before the closing card-grid div
    idx = idx.replace("    </div>\n\n  </main>", card + "\n    </div>\n\n  </main>")
    (BASE / "index.html").write_text(idx, encoding="utf-8")
    print("OK: Added Parasitología card to main index")
else:
    print("SKIP: Parasitología already in main index")

print("\nDone!")
