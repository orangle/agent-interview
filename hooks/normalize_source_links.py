"""Normalize source links before MkDocs renders Markdown.

The imported question bank contains several source-link shapes, for example::

    - Source description
      - https://example.com/doc

    - Source description

    - https://example.com/doc

    https://example.com/doc

Within source/reference sections this hook compacts those shapes into one clickable
line. Bare URLs elsewhere are handled by ``pymdownx.magiclink``.
"""

from __future__ import annotations

import re
from typing import Iterable


_HEADING = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*$")
_LIST_ITEM = re.compile(r"^(?P<indent>[ \t]*)[-*+]\s+(?P<body>.+?)\s*$")
_URL_ONLY = re.compile(r"^<?(?P<url>https?://[^\s<>]+)>?\s*$")
_MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(https?://[^)]+\)")
_SOURCE_TITLES = {
    "来源",
    "参考",
    "参考资料",
    "技术依据",
    "资料来源",
    "延伸阅读",
}
_TRAILING_PUNCTUATION = ".,;:!?，。；：！？"


def _clean_url(url: str) -> str:
    return url.rstrip(_TRAILING_PUNCTUATION)


def _is_source_heading(title: str) -> bool:
    normalized = title.strip().strip("#").strip()
    return any(normalized == item or normalized.startswith(f"{item}（") for item in _SOURCE_TITLES)


def _is_url_only(text: str) -> str | None:
    match = _URL_ONLY.match(text.strip())
    if not match:
        return None
    return _clean_url(match.group("url"))


def _already_has_link(text: str) -> bool:
    return bool(_MARKDOWN_LINK.search(text) or re.search(r"https?://", text))


def _next_nonempty(lines: list[str], start: int) -> tuple[int, str] | None:
    index = start
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines):
        return None
    return index, lines[index]


def _normalize_source_section(lines: list[str]) -> list[str]:
    output: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        item = _LIST_ITEM.match(line)

        if item and not _already_has_link(item.group("body")):
            following = _next_nonempty(lines, index + 1)
            if following is not None:
                next_index, next_line = following
                next_item = _LIST_ITEM.match(next_line)

                if next_item:
                    url = _is_url_only(next_item.group("body"))
                    if url:
                        current_indent = len(item.group("indent").expandtabs(4))
                        next_indent = len(next_item.group("indent").expandtabs(4))

                        # Accept both imported forms:
                        #   - description\n    - URL
                        #   - description\n- URL
                        # but do not merge an URL belonging to an outer list item.
                        if next_indent >= current_indent:
                            output.append(
                                f"{item.group('indent')}- {item.group('body').rstrip()} "
                                f"[查看原文]({url})"
                            )
                            index = next_index + 1
                            continue

        if item:
            url = _is_url_only(item.group("body"))
            if url:
                output.append(f"{item.group('indent')}- [查看原文]({url})")
                index += 1
                continue

        url = _is_url_only(line)
        if url:
            output.append(f"[查看原文]({url})")
            index += 1
            continue

        output.append(line)
        index += 1

    return output


def _process_markdown(lines: Iterable[str]) -> list[str]:
    source_section = False
    source_level = 0
    in_fence = False
    fence_marker = ""
    buffer: list[str] = []
    output: list[str] = []

    def flush_buffer() -> None:
        nonlocal buffer
        if not buffer:
            return
        output.extend(_normalize_source_section(buffer) if source_section else buffer)
        buffer = []

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                flush_buffer()
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            output.append(line)
            continue

        if in_fence:
            output.append(line)
            continue

        heading = _HEADING.match(line)
        if heading:
            flush_buffer()
            level = len(heading.group("level"))
            title = heading.group("title")

            if _is_source_heading(title):
                source_section = True
                source_level = level
            elif source_section and level <= source_level:
                source_section = False
                source_level = 0

            output.append(line)
            continue

        buffer.append(line)

    flush_buffer()
    return output


def on_page_markdown(markdown: str, **_: object) -> str:
    """Normalize source links for every rendered Markdown page."""

    return "\n".join(_process_markdown(markdown.splitlines()))
