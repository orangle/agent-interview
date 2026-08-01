"""Normalize source URLs before MkDocs renders Markdown.

Many question files were imported with this shape:

- Source description
  - https://example.com/doc

For the learning site, render it as one compact, clickable item:

- Source description [查看原文](https://example.com/doc)
"""

from __future__ import annotations

import re


_NESTED_URL_ITEM = re.compile(
    r"(?m)^(?P<indent>[ \t]*)-\s+(?P<label>[^\n]+?)\s*\n"
    r"(?P=indent)[ \t]{2,}-\s+(?P<url>https?://[^\s<>]+)\s*$"
)

_STANDALONE_URL_ITEM = re.compile(
    r"(?m)^(?P<indent>[ \t]*)-\s+(?P<url>https?://[^\s<>]+)\s*$"
)


def _clean_url(url: str) -> str:
    return url.rstrip(".,;，。；")


def on_page_markdown(markdown: str, **_: object) -> str:
    """Merge nested source URLs and make standalone URL bullets clickable."""

    def merge_nested(match: re.Match[str]) -> str:
        indent = match.group("indent")
        label = match.group("label").rstrip()
        url = _clean_url(match.group("url"))
        return f"{indent}- {label} [查看原文]({url})"

    def link_standalone(match: re.Match[str]) -> str:
        indent = match.group("indent")
        url = _clean_url(match.group("url"))
        return f"{indent}- [查看原文]({url})"

    markdown = _NESTED_URL_ITEM.sub(merge_nested, markdown)
    return _STANDALONE_URL_ITEM.sub(link_standalone, markdown)
