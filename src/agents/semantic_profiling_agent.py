"""Semantic profiling agent wrapper.

This module provides a callable wrapper around the semantic profiling
skill/prompt contract. It supports mock execution and optional real LLM
execution (when API key and client are available).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Tuple


PROMPT_TEMPLATE_PATH = Path(".ai/prompts/semantic-profiling-prompt-template.md")
OUTPUT_PATH = Path("test_outputs/semantic_profiling/ACTUAL_SEMANTIC_OUTPUT.md")
RAW_OUTPUT_PATH = Path("test_outputs/semantic_profiling/ACTUAL_LLM_RAW_OUTPUT.md")
GEMINI_RAW_OUTPUT_PATH = Path("test_outputs/semantic_profiling/ACTUAL_GEMINI_RAW_OUTPUT.md")


def _load_profile_artifacts(profile_json_path: Path) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Any]:
    """Load required profiling artifacts.

    Supports two shapes:
    1) A single combined JSON containing keys:
       - table_profile
       - relationship_candidates
       - domain_pattern_findings
       - optional sample_rows
    2) A directory containing:
       - table_profile.json
       - relationship_candidates.json
       - domain_pattern_findings.json
       - optional sample_rows.json
    """
    if profile_json_path.is_file():
        combined = json.loads(profile_json_path.read_text(encoding="utf-8"))
        if all(k in combined for k in ("table_profile", "relationship_candidates", "domain_pattern_findings")):
            return (
                combined["table_profile"],
                combined["relationship_candidates"],
                combined["domain_pattern_findings"],
                combined.get("sample_rows", []),
            )
        raise ValueError(
            "profile_json_path is a file but missing required keys: "
            "table_profile, relationship_candidates, domain_pattern_findings"
        )

    if profile_json_path.is_dir():
        table_profile = json.loads((profile_json_path / "table_profile.json").read_text(encoding="utf-8"))
        relationship_candidates = json.loads(
            (profile_json_path / "relationship_candidates.json").read_text(encoding="utf-8")
        )
        domain_pattern_findings = json.loads(
            (profile_json_path / "domain_pattern_findings.json").read_text(encoding="utf-8")
        )
        sample_rows_path = profile_json_path / "sample_rows.json"
        sample_rows = json.loads(sample_rows_path.read_text(encoding="utf-8")) if sample_rows_path.exists() else []
        return table_profile, relationship_candidates, domain_pattern_findings, sample_rows

    raise FileNotFoundError(f"Profile artifact path not found: {profile_json_path}")


def _build_prompt(table_profile: Dict[str, Any], relationships: Any, domain_findings: Dict[str, Any], sample_rows: Any) -> str:
    """Inject profile artifacts into the prompt template placeholders."""
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    prompt = (
        template.replace("{{TABLE_PROFILE_JSON}}", json.dumps(table_profile, indent=2, ensure_ascii=False))
        .replace("{{RELATIONSHIP_CANDIDATES_JSON}}", json.dumps(relationships, indent=2, ensure_ascii=False))
        .replace("{{DOMAIN_PATTERN_FINDINGS_JSON}}", json.dumps(domain_findings, indent=2, ensure_ascii=False))
        .replace("{{SAMPLE_ROWS_OPTIONAL}}", json.dumps(sample_rows, indent=2, ensure_ascii=False))
    )
    return prompt


def _call_llm(prompt: str) -> str:
    """Execute a real OpenAI LLM call and return raw text output."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY environment variable")

    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover - env dependent
        raise RuntimeError("openai package is not installed") from exc

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict data warehouse modeling reasoning engine."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""


def _call_gemini(prompt: str) -> str:
    """Execute a real Gemini call and return raw text output."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable")

    try:
        from google import genai
    except Exception as exc:  # pragma: no cover - env dependent
        raise RuntimeError("google-genai package is not installed") from exc

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "You are a strict data warehouse modeling reasoning engine.",
            prompt,
        ],
    )
    return response.text or ""


def _extract_json_block(raw_text: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM/Gemini output with robust fallbacks."""
    text = (raw_text or "").strip().lstrip("﻿​‌‍")

    # 1) Preferred: fenced ```json block
    match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", text, flags=re.IGNORECASE)
    if match:
        return json.loads(match.group(1).strip())

    # 2) Fallback: generic fenced ``` block that contains JSON
    generic_match = re.search(r"```\s*(\{[\s\S]*?\})\s*```", text)
    if generic_match:
        return json.loads(generic_match.group(1).strip())

    # 3) Fallback: first top-level JSON object in text
    start = text.find("{")
    if start != -1:
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
            else:
                if ch == '"':
                    in_string = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = text[start : i + 1].strip()
                        return json.loads(candidate)

    raise ValueError("No parseable JSON object found in LLM output")


def _mock_llm_call(_: str, table_profile: Dict[str, Any], relationships: Any, domain_findings: Dict[str, Any]) -> Dict[str, Any]:
    """Mock LLM call placeholder.

    Replace this function with a real LLM/API call in a future integration.
    """
    table_name = table_profile.get("table_name", "unknown_table")
    business_process_guess = "transaction/event capture" if "txn" in table_name.lower() else "unclear"

    return {
        "business_process_guess": business_process_guess,
        "entity_type_guess": "fact-like transactional" if table_profile.get("row_count", 0) > 0 else "unclear",
        "grain_candidates": [
            "one row per transaction_id",
            "one row per transaction_id + product_id + customer_id + transaction_dt",
        ],
        "recommended_grain": "one row per transaction_id + product_id + customer_id + transaction_dt",
        "dimension_candidates": ["customer", "product", "store", "date"],
        "fact_candidates": [table_name],
        "measure_candidates": ["quantity", "unit_price", "total_sales"],
        "candidate_natural_keys": ["transaction_id + product_id + customer_id + transaction_dt"],
        "data_quality_risks": [
            "review null ratios for key columns",
            "review parse-success gaps for numeric/date fields",
        ],
        "cross_source_conflicts": [
            "review domain_pattern_findings.cross_source_entity_conflicts for survivorship/SCD implications"
        ]
        if domain_findings.get("cross_source_entity_conflicts")
        else [],
        "modeling_notes": [
            "grain_notes: mock output; replace with model-generated scored grain evidence.",
            "key_notes: mock output; evaluate uniqueness/null sensitivity/stability before acceptance.",
            "dimension_notes: mock output inferred from relationship-style columns.",
            f"relationship_notes: {len(relationships)} candidate relationship(s) provided.",
            "quality_notes: confirm parse/null/duplication risks from profile metrics.",
            "scd_notes: if cross-source conflicts exist, mark attributes as SCD candidates for human review.",
            "unresolved_questions: requires human decision before model finalization.",
        ],
        "confidence_level": "medium",
        "requires_human_decision": True,
    }


def _write_output_markdown(output_json: Dict[str, Any]) -> None:
    """Write output using the existing manual-run markdown structure."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    markdown = (
        "# ACTUAL_SEMANTIC_OUTPUT\n\n"
        "## Section 1: JSON Output\n\n"
        "```json\n"
        f"{json.dumps(output_json, indent=2, ensure_ascii=False)}\n"
        "```\n\n"
        "## Section 2: Reasoning Sections\n\n"
        "### grain reasoning\n"
        "- See `modeling_notes` entries prefixed with `grain_notes`.\n\n"
        "### key reasoning\n"
        "- See `modeling_notes` entries prefixed with `key_notes`.\n\n"
        "### dimension vs fact reasoning\n"
        "- See `modeling_notes` entries prefixed with `dimension_notes`.\n\n"
        "### relationship reasoning\n"
        "- See `modeling_notes` entries prefixed with `relationship_notes`.\n\n"
        "### data quality impact\n"
        "- See `modeling_notes` entries prefixed with `quality_notes` and `scd_notes`.\n"
    )
    OUTPUT_PATH.write_text(markdown, encoding="utf-8")


def run_semantic_profiling(profile_json_path: str, mode: str = "mock") -> Dict[str, Any]:
    """Run semantic profiling wrapper and return parsed JSON output.

    Args:
        profile_json_path: Path to combined profile JSON file or a directory
            containing the required JSON artifacts.
        mode: "mock" (default), "llm", or "gemini".

    Returns:
        Parsed semantic profiling JSON object, or structured error object.
    """
    path = Path(profile_json_path)
    table_profile, relationships, domain_findings, sample_rows = _load_profile_artifacts(path)
    prompt = _build_prompt(table_profile, relationships, domain_findings, sample_rows)

    if mode == "mock":
        output_json = _mock_llm_call(prompt, table_profile, relationships, domain_findings)
        _write_output_markdown(output_json)
        return output_json

    if mode == "llm":
        RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            raw_output = _call_llm(prompt)
            RAW_OUTPUT_PATH.write_text(raw_output, encoding="utf-8")
            parsed_json = _extract_json_block(raw_output)
            _write_output_markdown(parsed_json)
            return parsed_json
        except Exception as exc:
            if not RAW_OUTPUT_PATH.exists():
                RAW_OUTPUT_PATH.write_text(
                    f"LLM execution failed before raw response could be captured.\nError: {exc}",
                    encoding="utf-8",
                )
            return {
                "error": str(exc),
                "raw_output_path": str(RAW_OUTPUT_PATH),
                "requires_human_decision": True,
            }

    if mode == "gemini":
        GEMINI_RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            raw_output = _call_gemini(prompt)
            GEMINI_RAW_OUTPUT_PATH.write_text(raw_output, encoding="utf-8")
            parsed_json = _extract_json_block(raw_output)
            _write_output_markdown(parsed_json)
            return parsed_json
        except Exception as exc:
            if not GEMINI_RAW_OUTPUT_PATH.exists():
                GEMINI_RAW_OUTPUT_PATH.write_text(
                    f"Gemini execution failed before raw response could be captured.\nError: {exc}",
                    encoding="utf-8",
                )
            return {
                "error": str(exc),
                "raw_output_path": str(GEMINI_RAW_OUTPUT_PATH),
                "requires_human_decision": True,
            }

    return {
        "error": f"Unsupported mode: {mode}. Use 'mock', 'llm', or 'gemini'.",
        "raw_output_path": str(RAW_OUTPUT_PATH),
        "requires_human_decision": True,
    }
