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
    """Analysiert ein Python-Modul mit AST und extrahiert Funktionen, Klassen, Imports und Aufrufbeziehungen."""
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)

    functions, classes, imports, variables = [], [], [], []
    calls = defaultdict(set)
    current_function = None
    parent_stack = []

    # Liste bekannter Builtins, die im Call Graph ausgefiltert werden
    BUILTIN_FUNCS = {
        "len", "print", "range", "type", "str", "int", "float", "list",
        "dict", "set", "max", "min", "sum", "any", "all", "zip", "map",
        "filter", "sorted", "enumerate", "open", "isinstance", "hasattr",
        "getattr", "setattr", "abs", "round", "next", "iter"
    }

    class CallVisitor(ast.NodeVisitor):
        """AST-Visitor, der Funktionsaufrufe innerhalb anderer Funktionen erkennt."""
        def visit_FunctionDef(self, node):
            nonlocal current_function
            prev = current_function
            current_function = node.name
            parent_stack.append(node.name)
            self.generic_visit(node)
            parent_stack.pop()
            current_function = prev

        def visit_Call(self, node):
            if current_function:
                func_name = None
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name and func_name not in BUILTIN_FUNCS:
                    calls[current_function].add(func_name)
            self.generic_visit(node)

    # Call-Graph scannen
    CallVisitor().visit(tree)

    # Funktions- und Moduldefinitionen auslesen
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        elif isinstance(node, ast.Import):
            imports.extend([n.name for n in node.names])
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
    """Durchläuft alle Python-Dateien und sammelt Metadaten."""
    modules = {}
    for py_file in SRC_DIR.rglob("*.py"):
        rel = py_file.relative_to(SRC_DIR)
        modules[str(rel)] = extract_module_info(py_file)
    return modules


def build_codemap(modules):
    """Erstellt die Markdown-Dokumentation mit Funktions- und Aufrufinformationen."""
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
    """Schreibt die generierte Dokumentation in docs/CODE_MAP.md."""
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
