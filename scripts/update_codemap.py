"""
update_codemap.py – Automatische CODE_MAP-Generierung mit Call-Dependency-Analyse
--------------------------------------------------------------------------------
Scant alle Python-Module im Verzeichnis src/colabtool/
und erzeugt eine aktualisierte docs/CODE_MAP.md.
Neu: erkennt, welche Funktionen andere Funktionen aufrufen (Call Graph).
"""

import ast
from pathlib import Path
from datetime import datetime
from collections import defaultdict

SRC_DIR = Path("src/colabtool")
DOC_PATH = Path("docs/CODE_MAP.md")

HEADER = f"""# 📘 CODE_MAP.md – Automatisch generiert
> Repository: schluchtenscheisser/colabtool  
> Letzte Aktualisierung: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---
"""

def extract_module_info(file_path: Path):
    """Analysiert ein Python-Modul mit AST."""
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)

    functions, classes, imports, variables = [], [], [], []
    calls = defaultdict(set)

    current_function = None
    parent_stack = []

    class CallVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            nonlocal current_function
            prev = current_function
            current_function = node.name
            parent_stack.append(node.name)
            self.generic_visit(node)
            parent_stack.pop()
            current_function = prev

        def visit_Call(self, node):
            if current_function and isinstance(node.func, ast.Name):
                calls[current_function].add(node.func.id)
            elif current_function and isinstance(node.func, ast.Attribute):
                calls[current_function].add(node.func.attr)
            self.generic_visit(node)

    CallVisitor().visit(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = node.module or ", ".join(n.name for n in node.names)
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
        "calls": {k: sorted(v) for k, v in calls.items()},
    }


def scan_repository():
    modules = {}
    for py_file in SRC_DIR.rglob("*.py"):
        rel = py_file.relative_to(SRC_DIR)
        modules[str(rel)] = extract_module_info(py_file)
    return modules


def build_codemap(modules):
    lines = [HEADER, "## 🧩 Modulübersicht\n"]

    for mod, info in sorted(modules.items()):
        lines.append(f"### 📄 `{mod}`\n")
        if info["classes"]:
            lines.append(f"**Klassen:** {', '.join(info['classes'])}\n")
        lines.append("**Funktionen:** " + (", ".join(info["functions"]) or "–") + "\n")
        lines.append("**Variablen:** " + (", ".join(info["variables"]) or "–") + "\n")
        lines.append("**Imports:** " + (", ".join(info["imports"]) or "–") + "\n")
        lines.append("---\n")

    # Ergänze Call Graph
    lines.append("\n## 🔗 Funktionsabhängigkeiten (Call Graph)\n")
    lines.append("| Aufrufende Funktion | Ruft auf |\n|----------------------|-----------|\n")

    all_calls = []
    for mod, info in modules.items():
        for func, called in info["calls"].items():
            if called:
                all_calls.append((f"{mod}:{func}", ", ".join(called)))

    if not all_calls:
        lines.append("| – | – |\n")
    else:
        for caller, targets in sorted(all_calls):
            lines.append(f"| `{caller}` | {targets} |\n")

    return "\n".join(lines)


def write_codemap(content: str):
    DOC_PATH.parent.mkdir(exist_ok=True)
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ CODE_MAP.md aktualisiert unter: {DOC_PATH.resolve()}")


if __name__ == "__main__":
    print("🔍 Scanne Repository für Funktionen & Aufrufbeziehungen ...")
    modules = scan_repository()
    content = build_codemap(modules)
    write_codemap(content)
    print("✅ Fertig! CODE_MAP.md enthält jetzt Funktionsabhängigkeiten.")
