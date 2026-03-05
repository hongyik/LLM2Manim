"""
Concept Retrieval: LLM-guided grep search over the textbooks/slides corpus.

Flow:
  user_input
    → LLM extract keywords
    → grep_corpus(corpus/textbooks/)
    → LLM summarize hits
    → concept_context  (injected into planner prompt)

Graceful degradation: returns "" if corpus directory is missing or empty.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import CORPUS_TEXTBOOKS_DIR, RETRIEVAL_MAX_CHARS
from .llm import get_llm
from .retrieval import grep_corpus, llm_extract_keywords, llm_summarize_hits


def retrieve_concepts(user_input: str) -> str:
    """
    Retrieve and summarize relevant textbook/slides content for the given topic.
    Returns a concept_context string (empty string if corpus is missing/empty).
    """
    if not CORPUS_TEXTBOOKS_DIR.exists():
        return ""

    text_files = [
        f for f in CORPUS_TEXTBOOKS_DIR.rglob("*")
        if f.suffix.lower() in {".txt", ".md"} and f.is_file()
    ]
    if not text_files:
        print("   [concept_retrieval] No textbook files found — skipping.")
        return ""

    print(f"   [concept_retrieval] Searching {len(text_files)} textbook file(s)...")

    try:
        llm = get_llm(stage="planner", temperature=0.3, max_tokens=256)

        # Step 1: LLM generates focused search keywords
        keywords = llm_extract_keywords(llm, query=user_input, n=5)
        print(f"   [concept_retrieval] Keywords: {keywords}")

        # Step 2: grep corpus
        hits = grep_corpus(
            CORPUS_TEXTBOOKS_DIR, keywords, window=5, max_chars=RETRIEVAL_MAX_CHARS
        )
        if not hits:
            print("   [concept_retrieval] No hits found in textbook corpus.")
            return ""

        # Step 3: LLM summarizes into a concise concept block
        context = llm_summarize_hits(llm, query=user_input, hits=hits, role="concept")
        print(f"   [concept_retrieval] Concept context: {len(context)} chars")
        return context

    except Exception as exc:
        print(f"   [concept_retrieval] ERROR: {exc}")
        return ""
