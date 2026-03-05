"""
Shared retrieval utilities: grep-based corpus search + LLM-powered keyword extraction
and summarization. Used by concept_retrieval.py and code_retrieval.py.
"""
import re
from pathlib import Path
from typing import List

from langchain_core.messages import HumanMessage, SystemMessage


def grep_files(
    files: List[Path],
    keywords: List[str],
    window: int = 5,
    max_chars: int = 8000,
) -> str:
    """
    Search a list of files for keywords.
    Returns matched chunks (±window lines around each hit), deduplicated, capped at max_chars.
    """
    chunks = []
    seen_ranges = set()

    for filepath in files:
        try:
            lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        for kw in keywords:
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            for i, line in enumerate(lines):
                if pattern.search(line):
                    start = max(0, i - window)
                    end = min(len(lines), i + window + 1)
                    key = (str(filepath), start, end)
                    if key in seen_ranges:
                        continue
                    seen_ranges.add(key)
                    chunk = (
                        f"# [{filepath.name}:{start+1}-{end}]\n"
                        + "\n".join(lines[start:end])
                    )
                    chunks.append(chunk)

    if not chunks:
        return ""

    result = "\n\n---\n\n".join(chunks)
    if len(result) > max_chars:
        result = result[:max_chars] + "\n...[truncated]"
    return result


def grep_corpus(
    directory: Path,
    keywords: List[str],
    window: int = 5,
    max_chars: int = 8000,
    extensions: tuple = (".txt", ".md", ".py"),
) -> str:
    """
    Search all files with given extensions in directory (recursive) for keywords.
    Returns matched chunks, deduplicated, capped at max_chars.
    """
    if not directory.exists():
        return ""
    files = [
        f for f in directory.rglob("*")
        if f.suffix.lower() in extensions and f.is_file()
    ]
    return grep_files(files, keywords, window=window, max_chars=max_chars)


def llm_extract_keywords(llm, query: str, context: str = "", n: int = 5) -> List[str]:
    """
    Ask LLM to generate n short search keywords suitable for grep.
    Returns a list of keyword strings.
    """
    system = (
        f"You are a search assistant. Given a topic, output exactly {n} short search "
        f"keywords (1-3 words each) suitable for grep-based full-text corpus search. "
        f"Output only the keywords, one per line, no numbering, no explanation."
    )
    user = f"Topic: {query}"
    if context:
        user += f"\nContext: {context}"

    try:
        response = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
        raw = response.content if hasattr(response, "content") else str(response)
        if isinstance(raw, list):
            raw = "\n".join(
                b.get("text", "") if isinstance(b, dict) else str(b) for b in raw
            )
        keywords = [line.strip() for line in raw.strip().splitlines() if line.strip()]
        return keywords[:n]
    except Exception as exc:
        print(f"   [retrieval] keyword extraction failed: {exc}")
        # Fallback: naive split
        return query.split()[:n]


def llm_summarize_hits(llm, query: str, hits: str, role: str = "concept") -> str:
    """
    Ask LLM to summarize retrieved corpus hits into a concise, useful block.
    role: "concept" (textbook excerpts) | "code_example" (Manim code patterns).
    """
    if not hits.strip():
        return ""

    if role == "code_example":
        system = (
            "You are a Manim code assistant. From the retrieved snippets below, select and "
            "present the most relevant working code patterns for the given animation task. "
            "Preserve code blocks intact. Omit irrelevant snippets. Be concise."
        )
    else:
        system = (
            "You are an academic assistant. From the retrieved textbook/slides excerpts, "
            "extract and summarize key concepts, definitions, and formulas relevant to the topic. "
            "Be concise (max 300 words). Preserve mathematical notation."
        )

    user = f"Task/Topic: {query}\n\nRetrieved content:\n{hits}"

    try:
        response = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
        raw = response.content if hasattr(response, "content") else str(response)
        if isinstance(raw, list):
            raw = "\n".join(
                b.get("text", "") if isinstance(b, dict) else str(b) for b in raw
            )
        return raw.strip()
    except Exception as exc:
        print(f"   [retrieval] summarization failed: {exc}")
        return hits[:2000]  # fallback: truncated raw hits
