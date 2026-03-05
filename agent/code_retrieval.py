"""
Code Retrieval: LLM-guided grep search over Manim code examples.

Searches two sources:
  1. prompts/code_patterns.txt  — always (built-in verified patterns, 20KB)
  2. corpus/manim_examples/     — when the user has placed example files there

Flow:
  plan goals
    → LLM extract keywords
    → grep_files([code_patterns.txt]) + grep_corpus(corpus/manim_examples/)
    → LLM summarize/select most relevant snippets
    → code_examples  (injected into code_gen prompt)

Graceful degradation: returns "" if nothing is found.
"""
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import CORPUS_MANIM_EXAMPLES_DIR, CODE_PATTERNS_FILE, RETRIEVAL_MAX_CHARS
from .llm import get_llm
from .retrieval import grep_files, grep_corpus, llm_extract_keywords, llm_summarize_hits


def retrieve_code_examples(
    plan: List[Dict[str, str]],
    descriptions: Dict[str, Any],
) -> str:
    """
    Retrieve relevant Manim code examples for the planned animation steps.
    Returns a code_examples string (empty if nothing relevant found).
    """
    # Build a compact query string from plan goals
    goals = [s.get("goal", "") for s in plan if s.get("goal")]
    query = "; ".join(goals[:5])
    if not query.strip():
        return ""

    try:
        llm = get_llm(stage="planner", temperature=0.3, max_tokens=256)

        # Step 1: Generate code-oriented keywords.
        # Context tells the LLM it's searching Python code files, so it must produce
        # short terms (1 word preferred) that actually appear in code — variable names,
        # class names, short physics nouns — not long textbook phrases.
        code_context = (
            "You are searching through Manim Python animation code files. "
            "Keywords must be SHORT (1 word, 2 max) so they match variable names, "
            "class names, comments, and short physics nouns inside .py files. "
            "Avoid long phrases like 'thermal equilibrium demonstration' — use 'temperature', "
            "'heat', 'gas', 'VGroup', 'MathTex' etc."
        )
        keywords = llm_extract_keywords(llm, query=query, context=code_context, n=7)
        print(f"   [code_retrieval] Keywords: {keywords}")

        all_hits: List[str] = []
        per_source = RETRIEVAL_MAX_CHARS // 2

        # Source A: code_patterns.txt (always searched — built-in verified patterns)
        if CODE_PATTERNS_FILE.exists():
            hits = grep_files(
                [CODE_PATTERNS_FILE], keywords, window=8, max_chars=per_source
            )
            if hits:
                all_hits.append(hits)

        # Source B: user-provided Manim example files in corpus/manim_examples/
        if CORPUS_MANIM_EXAMPLES_DIR.exists():
            example_files = [
                f for f in CORPUS_MANIM_EXAMPLES_DIR.rglob("*")
                if f.suffix.lower() in {".py", ".txt", ".md"} and f.is_file()
            ]
            if example_files:
                print(f"   [code_retrieval] Searching {len(example_files)} example file(s)...")
                hits = grep_corpus(
                    CORPUS_MANIM_EXAMPLES_DIR, keywords, window=8, max_chars=per_source
                )
                if hits:
                    all_hits.append(hits)

        combined = "\n\n---\n\n".join(all_hits)
        if not combined.strip():
            print("   [code_retrieval] No code examples found.")
            return ""

        # Step 2: LLM selects and summarizes the most relevant snippets
        llm_sum = get_llm(stage="planner", temperature=0.2, max_tokens=1024)
        examples = llm_summarize_hits(llm_sum, query=query, hits=combined, role="code_example")
        print(f"   [code_retrieval] Code examples: {len(examples)} chars")
        return examples

    except Exception as exc:
        print(f"   [code_retrieval] ERROR: {exc}")
        return ""
