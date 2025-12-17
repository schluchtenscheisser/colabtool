"""
update_codemap.py – Automatische CODE_MAP-Generierung mit Call-Dependency-Analyse
--------------------------------------------------------------------------------
Scant alle Python-Module im Verzeichnis src/colabtool/
und erzeugt eine aktualisierte docs/CODE_MAP.md.
Erkennt:
- welche Funktionen andere Funktionen aufrufen (Call Graph)
- unterscheidet interne und externe Aufrufe
- erstellt am Ende eine Abhängigkeits-Statistik
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

    # Builtins, die im Call Graph ausgefiltert werden
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
            self.generic_visit(node)
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
    stats = {}  # Statistik: Modul -> (interne, externe)

    for mod, info in sorted(modules.items()):
        lines.append(f"### 📄 `{mod}`\n")
        if info["classes"]:
            lines.append(f"**Klassen:** {', '.join(info['classes'])}\n")
        lines.append("**Funktionen:** " + (", ".join(info["functions"]) or "–") + "\n")
        lines.append("**Variablen:** " + (", ".join(info["variables"]) or "–") + "\n")
        lines.append("**Imports:** " + (", ".join(info["imports"]) or "–") + "\n")
        lines.append("---\n")

    # Ergänze Call Graph (nach Modulen gruppiert, intern/extern getrennt)
    lines.append("\n## 🔗 Funktionsabhängigkeiten (Call Graph)\n")

    has_any_calls = False
    for mod, info in sorted(modules.items()):
        if any(info["calls"].values()):
            has_any_calls = True
            lines.append(f"\n### 📄 {mod}\n")
            lines.append("| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |\n")
            lines.append("|----------------------|------------------|------------------|\n")

            func_set = set(info["functions"])  # Alle Funktionen des Moduls
            internal_total, external_total = 0, 0

            for func, called in sorted(info["calls"].items()):
                if called:
                    internal = sorted([c for c in called if c in func_set])
                    external = sorted([c for c in called if c not in func_set])
                    internal_total += len(internal)
                    external_total += len(external)
                    lines.append(
                        f"| `{func}` | "
                        f"{', '.join(internal) if internal else '–'} | "
                        f"{', '.join(external) if external else '–'} |\n"
                    )

            stats[mod] = (internal_total, external_total)

    if not has_any_calls:
        lines.append("\n| – | – | – |\n")

    # Statistikabschnitt am Ende
    if stats:
        lines.append("\n---\n\n## 📊 Abhängigkeits-Statistik\n")
        lines.append("| Modul | Interne Aufrufe | Externe Aufrufe | Gesamt |\n")
        lines.append("|--------|------------------|------------------|---------|\n")
        for mod, (i, e) in sorted(stats.items(), key=lambda x: (x[1][1] + x[1][0]), reverse=True):
            lines.append(f"| {mod} | {i} | {e} | {i + e} |\n")
        lines.append(
            "\n🧠 *Hinweis:* Viele **externe Aufrufe** deuten auf hohe Kopplung hin → "
            "Kandidaten für Refactoring oder Modularisierung.\n"
        )

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
    print("✅ Fertig! CODE_MAP.md enthält jetzt interne/externe Funktionsabhängigkeiten + Statistik.")
