"""
update_codemap.py – Automatische CODE_MAP-Generierung
-----------------------------------------------------
Scant alle Python-Module im Verzeichnis src/colabtool/
und erzeugt eine aktualisierte docs/CODE_MAP.md.

Benötigt keine externen Abhängigkeiten außer 'ast' und 'pathlib'.
"""

import ast
import os
from pathlib import Path
from datetime import datetime

SRC_DIR = Path("src/colabtool")
DOC_PATH = Path("docs/CODE_MAP.md")

HEADER = f"""# 📘 CODE_MAP.md – Automatisch generiert
> Repository: schluchtenscheisser/colabtool  
> Generiert am: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---
"""

def extract_module_info(file_path: Path):
    """Analysiert ein Python-Modul mit AST."""
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)

    functions = []
    classes = []
    imports = []
    variables = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
            else:
                mod = ", ".join([n.name for n in node.names])
            imports.append(mod)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and not t.id.startswith("_"):
                    variables.append(t.id)

    return {
        "functions": sorted(set(functions)),
        "classes": sorted(set(classes)),
        "imports": sorted(set(imports)),
        "variables": sorted(set(variables)),
    }


def scan_repository():
    """Durchläuft alle Module und sammelt deren Metadaten."""
    modules = {}
    for py_file in SRC_DIR.rglob("*.py"):
        rel = py_file.relative_to(SRC_DIR)
        modules[str(rel)] = extract_module_info(py_file)
    return modules


def build_codemap(modules):
    """Erzeugt den Markdown-Inhalt."""
    lines = [HEADER, "## 🧩 Modulübersicht\n"]

    for mod, info in sorted(modules.items()):
        lines.append(f"### 📄 `{mod}`\n")
        if info["classes"]:
            lines.append(f"**Klassen:** {', '.join(info['classes'])}\n")
        lines.append("**Funktionen:** " + (", ".join(info["functions"]) or "–") + "\n")
        lines.append("**Variablen:** " + (", ".join(info["variables"]) or "–") + "\n")
        lines.append("**Imports:** " + (", ".join(info["imports"]) or "–") + "\n")
        lines.append("---\n")

    return "\n".join(lines)


def write_codemap(content: str):
    """Schreibt den Markdown-Output in docs/CODE_MAP.md."""
    DOC_PATH.parent.mkdir(exist_ok=True)
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ CODE_MAP.md aktualisiert unter: {DOC_PATH.resolve()}")


if __name__ == "__main__":
    print("🔍 Scanne Repository...")
    modules = scan_repository()
    content = build_codemap(modules)
    write_codemap(content)
