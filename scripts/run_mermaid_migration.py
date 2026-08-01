from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from add_mermaid_diagrams import DIAGRAMS

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "questions"
START = "<!-- mermaid-diagram:start -->"
END = "<!-- mermaid-diagram:end -->"


def render_block(diagram: str) -> str:
    body = dedent(diagram).strip()
    body = body.replace("-.抑制.->", "-.->|抑制|")
    return f"{START}\n\n## 可视化图解\n\n```mermaid\n{body}\n```\n\n{END}"


def upsert(content: str, block: str) -> str:
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    anchors = ["\n## 核心结论", "\n## 先建立直觉", "\n## 一、", "\n## 完整链路"]
    positions = [content.find(anchor) for anchor in anchors if content.find(anchor) >= 0]
    if positions:
        pos = min(positions)
        return content[:pos].rstrip() + "\n\n" + block + "\n\n" + content[pos:].lstrip()

    lines = content.splitlines()
    insert_at = 1
    while insert_at < len(lines) and not lines[insert_at].startswith("## "):
        insert_at += 1
    lines[insert_at:insert_at] = ["", block, ""]
    return "\n".join(lines).rstrip() + "\n"


def migrate_questions() -> list[str]:
    changed: list[str] = []
    for filename, diagram in DIAGRAMS.items():
        path = QUESTIONS / filename
        if not path.exists():
            raise FileNotFoundError(path)
        original = path.read_text(encoding="utf-8")
        updated = upsert(original, render_block(diagram))
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    return changed


def ensure_mkdocs_config() -> bool:
    path = ROOT / "mkdocs.yml"
    text = path.read_text(encoding="utf-8")
    if "custom_fences:" in text and "name: mermaid" in text:
        return False

    old = "  - pymdownx.superfences\n"
    new = (
        "  - pymdownx.superfences:\n"
        "      custom_fences:\n"
        "        - name: mermaid\n"
        "          class: mermaid\n"
        "          format: !!python/name:pymdownx.superfences.fence_code_format\n"
    )
    if old not in text:
        raise RuntimeError("pymdownx.superfences entry not found in mkdocs.yml")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def ensure_css() -> bool:
    path = QUESTIONS / "stylesheets" / "extra.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* Mermaid diagrams */"
    if marker in text:
        return False
    addition = """

/* Mermaid diagrams */
.md-typeset .mermaid {
  margin: 1.4rem 0;
  text-align: center;
  overflow-x: auto;
}

.md-typeset .mermaid svg {
  display: inline-block;
  max-width: 100%;
  height: auto;
}

@media screen and (max-width: 600px) {
  .md-typeset .mermaid {
    margin-left: -0.35rem;
    margin-right: -0.35rem;
  }
}
"""
    path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")
    return True


def validate_source() -> None:
    expected = set(DIAGRAMS)
    actual = {path.name for path in QUESTIONS.glob("[0-9][0-9]-*.md")}
    missing = sorted(expected - actual)
    if missing:
        raise RuntimeError(f"Diagram targets missing: {missing}")

    for filename, diagram in DIAGRAMS.items():
        body = dedent(diagram).strip()
        if not body.startswith(("flowchart ", "graph ", "sequenceDiagram", "stateDiagram-v2")):
            raise RuntimeError(f"Unsupported Mermaid type in {filename}")
        if "```" in body:
            raise RuntimeError(f"Unexpected fence inside diagram: {filename}")


def main() -> None:
    validate_source()
    changed = migrate_questions()
    if ensure_mkdocs_config():
        changed.append("mkdocs.yml")
    if ensure_css():
        changed.append("questions/stylesheets/extra.css")

    print(f"Updated {len(changed)} files")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
