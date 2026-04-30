"""Local keyword-based knowledge retrieval for AI Copilot context injection."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

KNOWLEDGE_BASE_DIR = Path("knowledge_base")
MAX_FILES = 3
MAX_CHARS_PER_FILE = 2000


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9_]+", text.lower())


def _score_content(content: str, query_terms: List[str]) -> int:
    if not query_terms:
        return 0
    content_terms = set(_tokenize(content))
    return sum(1 for term in query_terms if term in content_terms)


def _collect_markdown_files(base_dir: Path) -> List[Path]:
    return sorted(base_dir.rglob("*.md"))


def _extract_chunk(content: str, query_terms: List[str], max_chars: int = MAX_CHARS_PER_FILE) -> str:
    lines = content.splitlines()
    if not lines:
        return ""

    # Prefer lines that contain any query term and capture local window.
    lowered = [line.lower() for line in lines]
    for i, line in enumerate(lowered):
        if any(term in line for term in query_terms):
            start = max(0, i - 8)
            end = min(len(lines), i + 20)
            chunk = "\n".join(lines[start:end]).strip()
            return chunk[:max_chars]

    return "\n".join(lines)[:max_chars].strip()


def retrieve_relevant_context(query: str) -> str:
    """
    Search knowledge_base/ for relevant content.
    Return concatenated relevant text chunks.
    """
    query_terms = _tokenize(query)
    candidates: List[Tuple[int, Path, str]] = []

    for path in _collect_markdown_files(KNOWLEDGE_BASE_DIR):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue

        score = _score_content(content, query_terms)
        if score <= 0:
            continue

        chunk = _extract_chunk(content, query_terms)
        if chunk:
            candidates.append((score, path, chunk))

    candidates.sort(key=lambda x: (-x[0], str(x[1])))
    top = candidates[:MAX_FILES]

    if not top:
        return "No relevant knowledge base context found."

    parts = []
    for score, path, chunk in top:
        parts.append(f"### Source: {path}\n(score={score})\n{chunk}")

    return "\n\n---\n\n".join(parts)
