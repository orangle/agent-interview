from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "questions"
MERMAID_MARKER = "<!-- mermaid-diagram:start -->"

TEXT_FENCE = re.compile(r"```text\n(?P<body>.*?)\n```", re.DOTALL)
BOX_CHARS = set("↓↑←→↔⇒⇢├└┌┐┬┴│─")
NON_DIAGRAM_HINTS = (
    "Reason：",
    "Action：",
    "Observation：",
    "Reason:",
    "Action:",
    "Observation:",
    "curl ",
    "kubectl ",
    "docker ",
    "ERROR",
    "Exception",
    "Traceback",
    "SELECT ",
    "CREATE TABLE",
)


def is_ascii_diagram(body: str) -> bool:
    if any(hint in body for hint in NON_DIAGRAM_HINTS):
        return False

    stripped = body.strip()
    if not stripped:
        return False

    lines = [line.rstrip() for line in stripped.splitlines() if line.strip()]
    arrow_count = sum(stripped.count(ch) for ch in BOX_CHARS)
    branch_lines = sum(
        1
        for line in lines
        if any(token in line for token in ("├──", "└──", "│", "┌", "┐"))
    )
    standalone_arrow_lines = sum(
        1
        for line in lines
        if line.strip() and all(ch in BOX_CHARS or ch.isspace() for ch in line)
    )
    linear_chain = stripped.count("→") >= 2 and len(lines) <= 6

    return (
        branch_lines >= 1
        or standalone_arrow_lines >= 1
        or arrow_count >= 4
        or linear_chain
    )


def clean_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    if MERMAID_MARKER not in original:
        return False

    replaced = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal replaced
        body = match.group("body")
        if not is_ascii_diagram(body):
            return match.group(0)
        replaced += 1
        if replaced == 1:
            return "> 对应流程已改为上方 Mermaid 图解。"
        return ""

    updated = TEXT_FENCE.sub(replace, original)
    updated = re.sub(r"\n{4,}", "\n\n\n", updated)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    print(f"cleaned {path.relative_to(ROOT)}: {replaced} diagram block(s)")
    return True


def main() -> None:
    changed = 0
    for path in sorted(QUESTIONS.glob("[0-9][0-9]-*.md")):
        if clean_file(path):
            changed += 1
    print(f"Updated {changed} question files")


if __name__ == "__main__":
    main()
