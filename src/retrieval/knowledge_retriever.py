"""Local hybrid-scoring knowledge retrieval for AI Copilot context injection."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

KNOWLEDGE_BASE_DIR = Path("knowledge_base")
MAX_FILES = 3
MAX_CHARS_PER_FILE = 2000

BOOST_KEYWORDS: Dict[str, List[str]] = {
    "source_triplet": ["source_triplet_and_lineage_rules.md"],
    "lineage": ["source_triplet_and_lineage_rules.md"],
    "default row": ["default_row_strategy.md"],
    "unknown member": ["default_row_strategy.md"],
    "scd": ["scd_decision_rules.md"],
    "grain": ["grain_decision_rules.md"],
}


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9_]+", text.lower())


def _collect_markdown_files(base_dir: Path) -> List[Path]:
    return sorted(base_dir.rglob("*.md"))


def _keyword_overlap_score(content: str, query_terms: List[str]) -> int:
    if not query_terms:
        return 0
    content_terms = set(_tokenize(content))
    return sum(1 for term in query_terms if term in content_terms)


def _file_boost_score(query: str, filename: str) -> Tuple[int, List[str]]:
    q = query.lower()
    score = 0
    reasons: List[str] = []

    for trigger, targets in BOOST_KEYWORDS.items():
        if trigger in q and filename in targets:
            score += 8
            reasons.append(f"boost:{trigger}")

    return score, reasons


def _title_match_bonus(filename: str, query_terms: List[str]) -> Tuple[int, List[str]]:
    stem = Path(filename).stem.lower()
    stem_terms = set(_tokenize(stem.replace("-", " ")))
    matched = [term for term in query_terms if term in stem_terms]
    bonus = min(len(set(matched)), 4)
    reasons = [f"title_match:{term}" for term in sorted(set(matched))]
    return bonus, reasons


def _best_matching_chunk(content: str, query_terms: List[str], max_chars: int = MAX_CHARS_PER_FILE) -> str:
    lines = content.splitlines()
    if not lines:
        return ""

    # Windowed scan: pick the chunk with highest keyword density.
    window_size = 24
    best_score = -1
    best_chunk = ""

    for start in range(0, len(lines)):
        end = min(len(lines), start + window_size)
        window = lines[start:end]
        if not window:
            continue
        joined = "\n".join(window)
        tokens = _tokenize(joined)
        if not tokens:
            continue

        hits = sum(1 for term in query_terms if term in tokens)
        density = hits / max(len(tokens), 1)
        score = hits * 1000 + int(density * 100000)

        if score > best_score:
            best_score = score
            best_chunk = joined

    if not best_chunk:
        best_chunk = "\n".join(lines)

    return best_chunk.strip()[:max_chars]


def retrieve_relevant_context(query: str) -> str:
    """
    Search knowledge_base/ for relevant content.
    Return concatenated relevant text chunks.
    """
    query_terms = _tokenize(query)
    candidates: List[Tuple[int, Path, str, str]] = []

    for path in _collect_markdown_files(KNOWLEDGE_BASE_DIR):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue

        overlap = _keyword_overlap_score(content, query_terms)
        boost, boost_reasons = _file_boost_score(query, path.name)
        title_bonus, title_reasons = _title_match_bonus(path.name, query_terms)
        total_score = overlap + boost + title_bonus

        if total_score <= 0:
            continue

        chunk = _best_matching_chunk(content, query_terms)
        if not chunk:
            continue

        reasons = [f"overlap={overlap}", f"boost={boost}", f"title_bonus={title_bonus}"]
        reasons.extend(boost_reasons)
        reasons.extend(title_reasons)
        why_selected = ", ".join(reasons)
        candidates.append((total_score, path, chunk, why_selected))

    candidates.sort(key=lambda x: (-x[0], str(x[1])))
    top = candidates[:MAX_FILES]

    if not top:
        return "No relevant knowledge base context found."

    parts = []
    for score, path, chunk, why_selected in top:
        parts.append(
            f"### Source: {path}\n"
            f"file_name={path.name}\n"
            f"score={score}\n"
            f"why_selected={why_selected}\n"
            f"{chunk}"
        )

    return "\n\n---\n\n".join(parts)
