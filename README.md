# Animated Math & Physics — LangGraph Pipeline

An AI-powered pipeline that generates animated educational math/physics videos using **Manim CE**, **LangGraph**, and **LLM agentic retrieval**.

---

## Pipeline Overview

The pipeline is a **10-node LangGraph** that converts a user question into a rendered MP4:

```
User Question
     │
     ▼
 1. Parse
     │
     ▼
 2. Concept Retrieval  ◄── corpus/textbooks/  (LLM + grep)
     │
     ▼
 3. Planner            ◄── concept context injected
     │
     ▼
 4. Step Descriptions  ◄── step memory + ledger
     │
     ▼
 5. Layout Engine      (deterministic, no LLM)
     │
     ▼
 6. Code Retrieval     ◄── corpus/manim_examples/ + code_patterns.txt  (LLM + grep)
     │
     ▼
 7. Pseudo-code Gen    ◄── per-scene structured outline
     │
     ▼
 8. Manim Code Gen     ◄── ledger + layout + pseudocode + code examples
     │
     ▼
 9. Scene Fix          ◄── api_check → validate → LLM fix loop (max 3 attempts)
     │
     ▼
10. Render & Combine   ◄── parallel Manim render + FFmpeg concat
     │
     ▼
  combined_animation.mp4
```

---

## Stage Details

| # | Node | Description |
|---|------|-------------|
| 1 | **Parse** | Validates non-empty input. |
| 2 | **Concept Retrieval** | LLM generates search keywords → grep `corpus/textbooks/` → LLM summarizes hits into a *concept context* injected into the planner. |
| 3 | **Planner** | Produces a dynamic JSON list of `{id, goal}` steps. Number and content depend on input. Receives concept context for domain accuracy. |
| 4 | **Step Descriptions** | Runs sequentially; each step sees the full plan + all previous step descriptions + the running **ledger** (notation, visual style, object names). |
| 5 | **Layout Engine** | Deterministic greedy placement — assigns each element a zone, position, and animation group. No LLM call. |
| 6 | **Code Retrieval** | LLM generates code-oriented keywords → grep `corpus/manim_examples/` + `prompts/code_patterns.txt` → LLM selects the most relevant Manim snippets. |
| 7 | **Pseudo-code Gen** | For each scene, LLM generates a structured blueprint: *Objects / Animations / Voiceover beats / Layout notes*. Injected into code gen prompt. |
| 8 | **Manim Code Gen** | Generates one `.py` per scene using the description + ledger + layout spec + pseudocode outline + code examples. |
| 9 | **Scene Fix** | Secondary LangGraph per scene: `api_check → validate → LLM fix`. Catches syntax, undefined names, forbidden colors, runtime errors. Up to 3 attempts. |
| 10 | **Render & Combine** | Renders each scene in parallel (max 2 workers — Kokoro TTS is memory-intensive), then concatenates with FFmpeg. |

---

## Project Structure

```
Animated-math-and-physics/
│
├── agent/                          # Pipeline modules
│   ├── pipeline_graph.py           # Main 10-node LangGraph
│   ├── planner.py                  # Stage 3: dynamic plan from user input
│   ├── step_agent.py               # Stage 4: step descriptions with memory
│   ├── layout_engine.py            # Stage 5: deterministic layout (no LLM)
│   ├── code_agent.py               # Stage 8: Manim code generation
│   ├── scene_fix_graph.py          # Stage 9: secondary LangGraph fix loop
│   ├── render.py                   # Stage 10: parallel render + FFmpeg
│   │
│   ├── concept_retrieval.py        # Stage 2: textbook grep + LLM summarize
│   ├── code_retrieval.py           # Stage 6: Manim examples grep + LLM summarize
│   ├── pseudocode_agent.py         # Stage 7: per-scene structured outline
│   ├── retrieval.py                # Shared: grep_files, llm_extract_keywords, llm_summarize_hits
│   │
│   ├── api_check.py                # Fast AST pre-check (syntax, undefined names, bad colors)
│   ├── ledger.py                   # Cross-step consistency ledger
│   ├── memory_block.py             # Cross-run error→fix memory
│   ├── llm.py                      # LLM provider routing (DeepSeek / OpenAI / Anthropic)
│   └── __init__.py
│
├── corpus/                         # Retrieval corpora (user-maintained)
│   ├── textbooks/                  # Drop .txt/.md textbook files here
│   └── manim_examples/             # Drop .py Manim example files here
│
├── prompts/                        # All LLM prompt files
│   ├── plan_prompt.txt
│   ├── step_with_memory_prompt.txt
│   ├── system_prompt_code.txt
│   ├── user_prompt_code_template.txt
│   ├── pseudocode_system_prompt.txt
│   ├── code_patterns.txt           # Verified working Manim snippets (20 KB)
│   ├── manim_rules.md              # Manim API rules injected into code gen
│   ├── manim_allowlist.json        # 582 Manim CE symbols (auto-generated)
│   └── error_memory.json           # Cross-run error→fix patterns
│
├── structure_graph/                # Pipeline diagrams
│   ├── pipeline_graph.md           # Mermaid diagram (renders on GitHub)
│   ├── pipeline_graph.mmd          # Raw Mermaid source
│   ├── pipeline_graph.png          # PNG snapshot
│   └── visualize_pipeline.py       # Script to regenerate diagrams
│
├── outputs/                        # Per-run output folders (auto-created)
│   └── YYYY-MM-DD_HH-MM-SS/
│       ├── animation_outputs/      # .py scene files, JSON debug files
│       └── final_animation/        # individual_scenes/, combined_animation.mp4
│
├── config.py                       # All configuration constants
├── llm_config.json                 # Per-stage LLM model routing
├── main.py                         # Entry point
├── requirements.txt
└── .env                            # API keys (not committed)
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. API keys

Create a `.env` file in the project root (or set as system environment variables):

```env
DEEPSEEK_API_KEY=sk-...
GPT4_API_KEY=sk-...          # optional — for OpenAI stages
ANTHROPIC_API_KEY=sk-ant-... # optional — for Claude stages
```

### 3. Add corpus files (optional but recommended)

| Folder | What to put there |
|--------|-------------------|
| `corpus/textbooks/` | `.txt` or `.md` — extracted textbook chapters, lecture notes, Wikipedia articles |
| `corpus/manim_examples/` | `.py` — working Manim scene files to use as code references |

The pipeline works without corpus files — retrieval stages simply return empty strings and are skipped.

---

## Configuration

### LLM routing — `llm_config.json`

Each pipeline stage can use a different provider and model:

```json
{
  "planner":    { "provider": "deepseek", "model": "deepseek-chat" },
  "step":       { "provider": "deepseek", "model": "deepseek-chat" },
  "pseudocode": { "provider": "deepseek", "model": "deepseek-chat" },
  "code":       { "provider": "deepseek", "model": "deepseek-reasoner" },
  "fix":        { "provider": "deepseek", "model": "deepseek-reasoner" }
}
```

Supported providers: `deepseek` · `openai` · `anthropic`

### Environment variable overrides

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `deepseek` | Global fallback provider |
| `PLANNER_PROVIDER` / `PLANNER_MODEL` | from config | Planner + retrieval LLM calls |
| `STEP_PROVIDER` / `STEP_MODEL` | from config | Step descriptions |
| `PSEUDOCODE_PROVIDER` / `PSEUDOCODE_MODEL` | from config | Pseudo-code outlines |
| `CODE_PROVIDER` / `CODE_MODEL` | from config | Manim code generation |
| `FIX_PROVIDER` / `FIX_MODEL` | from config | Scene auto-fix |
| `MAX_SECTIONS` | `7` | Max scenes the planner can produce |
| `MANIM_RENDER_QUALITY` | `l` | `l` / `m` / `h` / `p` / `k` |
| `RETRIEVAL_MAX_CHARS` | `8000` | Token budget per retrieval call |

---

## Usage

### CLI

```bash
python main.py "Explain the Zeroth and First Law of Thermodynamics"
# or prompt interactively:
python main.py
```

### Programmatic

```python
from agent.pipeline_graph import run_pipeline

result = run_pipeline("Explain the material derivative in fluid flow")
if result["status"] == "success":
    print("Video:", result["stages"].get("combined_scene_path"))
else:
    print("Error:", result["error"])
```

### Output structure (per run)

```
outputs/2025-01-15_14-30-00/
├── animation_outputs/
│   ├── animation_descriptions.json   # step descriptions
│   ├── ledger.json                   # consistency ledger
│   ├── pseudocode.json               # per-scene outlines (debug)
│   ├── generated_code.json           # raw LLM code
│   ├── intro.py                      # generated Manim scene
│   ├── derivation.py
│   ├── validation_report.json        # scene fix details
│   └── validation_report.txt
└── final_animation/
    ├── individual_scenes/
    │   ├── intro.mp4
    │   └── derivation.mp4
    └── combined_animation.mp4
```

---

## Key Design Decisions

### Agentic Retrieval (LLM + grep, no vector DB)
- Concept retrieval: LLM generates domain keywords → grep textbook corpus → LLM summarizes → injected into planner
- Code retrieval: LLM generates **code-oriented** short keywords (e.g. `temperature`, `VGroup`, `MathTex`) → grep Manim examples → LLM selects best snippets → injected into code gen
- No embeddings or vector database required

### Consistency Ledger
- Append-only cross-step dictionary: notation, visual style, object names, story-so-far, constraints
- Prevents each scene from reinventing symbols and colors

### Pseudo-code Bridge
- Reduces code-gen hallucinations by providing a concrete per-scene blueprint before writing 400 lines of Manim code
- Format: `Objects → Animations → Voiceover beats → Layout notes`

### Scene Fix Loop (secondary LangGraph)
```
api_check → (violations) → fix → api_check (loop back)
          → (ok)         → validate → (fail) → fix
                                    → (ok)   → END
```
- **`api_check`**: Fast AST scan — undefined names, forbidden colors (`MAGENTA`, `CYAN`, `VIOLET`), syntax errors — before running Manim
- **`validate`**: Runs Manim subprocess (120 s timeout)
- **`fix`**: Sends line-numbered code + error context snippet to LLM. All static violations from `api_check` are appended so the LLM can fix multiple issues per attempt. Uses SEARCH/REPLACE patches; falls back to FULL_REWRITE for syntax errors.
- **Error memory** (`prompts/error_memory.json`): cross-run learning from successful fixes

---

## Regenerate Pipeline Diagram

```bash
python structure_graph/visualize_pipeline.py
```

Outputs updated `structure_graph/pipeline_graph.md`, `.mmd`, `.png`.
