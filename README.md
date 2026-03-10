# Animated Math & Physics

An AI-powered pipeline that converts a natural language topic into a fully rendered **educational animation video** — complete with narration. Built with **Manim CE**, **LangGraph**, and your choice of LLM (DeepSeek, OpenAI, or Anthropic Claude).

> **Input:** `"Explain the Pythagorean theorem"`
> **Output:** A narrated MP4 animation, generated end-to-end.

---

## Pipeline Overview

![Pipeline Structure](structure_graph/structure.png)

The pipeline is a **10-node LangGraph** that takes a user question through planning, scripting, layout, code generation, auto-fixing, and rendering:

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

| # | Node | Description |
|---|------|-------------|
| 1 | **Parse** | Validates non-empty input. |
| 2 | **Concept Retrieval** | LLM generates search keywords → grep `corpus/textbooks/` → LLM summarizes into a concept context for the planner. |
| 3 | **Planner** | Produces a JSON list of `{id, goal}` steps. Number and content depend on the topic. |
| 4 | **Step Descriptions** | Runs sequentially; each step sees the full plan + previous descriptions + a running **ledger** (notation, colors, object names). |
| 5 | **Layout Engine** | Deterministic coordinate placement — assigns each element a zone, position, and animation group. No LLM call. |
| 6 | **Code Retrieval** | LLM generates code-oriented keywords → grep `corpus/manim_examples/` + `prompts/code_patterns.txt` → LLM selects the most relevant Manim snippets. |
| 7 | **Pseudo-code Gen** | LLM generates a structured JSON blueprint per scene: objects, animation beats, voiceover, layout. Injected into code gen. |
| 8 | **Manim Code Gen** | Generates one `.py` per scene using description + ledger + layout + pseudocode + code examples. Includes a self-review pass. |
| 9 | **Scene Fix** | Inner LangGraph: `api_check → validate → LLM fix`. Catches syntax errors, undefined names, forbidden colors, and runtime failures. Up to 3 attempts per scene. |
| 10 | **Render & Combine** | Renders each scene in parallel (max 2 workers), then concatenates with FFmpeg. |

---

## Prerequisites

### Python
- Python 3.10 or newer
- A virtual environment is strongly recommended

### System dependencies

| Tool | Purpose | Install |
|------|---------|---------|
| **FFmpeg** | Video concatenation | [ffmpeg.org](https://ffmpeg.org/download.html) · `winget install ffmpeg` |
| **LaTeX** (MiKTeX or TeX Live) | MathTex rendering in Manim | [miktex.org](https://miktex.org/download) |
| **sox** | Audio processing for Manim voiceover | [sourceforge.net/projects/sox](https://sourceforge.net/projects/sox/) |

Make sure all three are on your system `PATH`.

### Kokoro TTS model files

This project uses [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) for local text-to-speech. Download and place these two files in the **project root**:

| File | Source |
|------|--------|
| `kokoro-v1.0.onnx` | [HuggingFace — hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) |
| `voices-v1.0.bin` | Same repository |

> The model files are ~300 MB total and are not included in this repository.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/animated-math-and-physics.git
cd animated-math-and-physics
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

```env
# .env
DEEPSEEK_API_KEY=sk-...          # required if using DeepSeek (default)
GPT4_API_KEY=sk-...              # required if using OpenAI stages
ANTHROPIC_API_KEY=sk-ant-...     # required if using Anthropic stages
```

You only need the key(s) for the provider(s) you configure in `llm_config.json`.

### 5. (Optional) Add corpus files

| Folder | What to put there |
|--------|-------------------|
| `corpus/textbooks/` | `.txt` or `.md` files — textbook chapters, lecture notes, Wikipedia excerpts |
| `corpus/manim_examples/` | `.py` files — working Manim scene files to use as code references |

The pipeline works without any corpus files. Retrieval stages simply return empty strings and are skipped gracefully.

### 6. Download Kokoro model files

Place `kokoro-v1.0.onnx` and `voices-v1.0.bin` in the project root directory (see [Prerequisites](#prerequisites)).

---

## Usage

### Command line

```bash
python main.py "Explain the Pythagorean theorem"
```

Or run interactively (you will be prompted for input):

```bash
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

### Output structure

Each run creates a timestamped folder:

```
outputs/2025-01-15_14-30-00/
├── animation_outputs/
│   ├── animation_descriptions.json   # step narrations
│   ├── ledger.json                   # consistency state
│   ├── pseudocode.json               # per-scene blueprints
│   ├── generated_code.json           # raw LLM code output
│   ├── intro.py                      # generated Manim scene files
│   ├── derivation.py
│   ├── validation_report.json        # scene fix attempt details
│   └── validation_report.txt         # human-readable fix log
└── final_animation/
    ├── individual_scenes/
    │   ├── intro.mp4
    │   └── derivation.mp4
    └── combined_animation.mp4        ← final output
```

---

## Configuration

### LLM routing — `llm_config.json`

Each pipeline stage can use a different provider and model. Copy the example and customize:

```bash
cp llm_config.example.json llm_config.json
```

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
| `LLM_PROVIDER` | `deepseek` | Global fallback provider if not set in `llm_config.json` |
| `MAX_SECTIONS` | `7` | Maximum number of scenes the planner can produce |
| `MANIM_RENDER_QUALITY` | `l` | `l` (480p) · `m` (720p) · `h` (1080p) · `p` · `k` (4K) |
| `RETRIEVAL_MAX_CHARS` | `8000` | Character budget per retrieval call |
| `CODE_AGENT_DEBUG` | `0` | Set to `1` to save per-step LLM prompts and raw responses |

---

## Project Structure

```
animated-math-and-physics/
│
├── agent/                          # Pipeline modules
│   ├── pipeline_graph.py           # Main 10-node LangGraph
│   ├── planner.py                  # Stage 3: dynamic plan from user input
│   ├── step_agent.py               # Stage 4: step descriptions with ledger
│   ├── layout_engine.py            # Stage 5: deterministic layout (no LLM)
│   ├── code_agent.py               # Stage 8: Manim code generation + self-review
│   ├── scene_fix_graph.py          # Stage 9: inner LangGraph fix loop
│   ├── render.py                   # Stage 10: parallel render + FFmpeg
│   │
│   ├── concept_retrieval.py        # Stage 2: textbook grep + LLM summarize
│   ├── code_retrieval.py           # Stage 6: Manim examples grep + LLM summarize
│   ├── pseudocode_agent.py         # Stage 7: per-scene JSON blueprint
│   ├── retrieval.py                # Shared: grep_files, llm_extract_keywords
│   │
│   ├── api_check.py                # Fast AST pre-check (syntax, undefined names, bad colors)
│   ├── ledger.py                   # Cross-step consistency ledger
│   ├── memory_block.py             # Cross-run error → fix memory
│   ├── llm.py                      # LLM provider routing (DeepSeek / OpenAI / Anthropic)
│   └── __init__.py
│
├── corpus/                         # Retrieval corpora (user-maintained, not committed)
│   ├── textbooks/                  # Drop .txt/.md textbook files here
│   └── manim_examples/             # Drop .py Manim example files here
│
├── prompts/                        # LLM prompt files
│   ├── plan_prompt.txt
│   ├── step_with_memory_prompt.txt
│   ├── system_prompt_code.txt
│   ├── user_prompt_code_template.txt
│   ├── pseudocode_system_prompt.txt
│   ├── code_patterns.txt           # Verified working Manim snippets
│   ├── manim_rules.md              # Manim API rules injected into code gen
│   ├── manim_allowlist.json        # 582 valid Manim CE symbols (auto-generated)
│   └── error_memory.json           # Cross-run learned error → fix patterns
│
├── structure_graph/                # Pipeline diagrams
│   ├── structure.png               # Visual pipeline overview
│   ├── pipeline_graph.md           # Mermaid diagram (renders on GitHub)
│   └── visualize_pipeline.py       # Script to regenerate diagrams
│
├── outputs/                        # Per-run output folders (auto-created, not committed)
│
├── config.py                       # All configuration constants
├── llm_config.json                 # Per-stage LLM model routing (not committed)
├── llm_config.example.json         # Template — copy and customize
├── main.py                         # Entry point
├── requirements.txt
├── .env                            # API keys (never committed)
└── .env.example                    # Template — copy and fill in keys
```

---

## Key Design Decisions

### LLM + grep retrieval (no vector DB)
Retrieval uses keyword extraction + grep over plain text files. No embeddings or vector database are required. The LLM generates short, targeted search keywords, grep finds matching chunks, and another LLM call summarizes the hits. This keeps the system self-contained and easy to extend.

### Consistency Ledger
A shared, append-only dictionary passed through all Step Description calls. It tracks notation symbols, visual style, object names, story so far, and constraints — preventing each scene from re-defining variables or switching color schemes mid-animation.

### Pseudo-code Bridge
Rather than asking the LLM to write 400 lines of Manim code from a paragraph description, the pipeline first produces a structured JSON blueprint (objects, animation beats, voiceover, layout). The code generator uses this blueprint as a grounded specification, significantly reducing hallucinations.

### Scene Fix Inner Loop
```
api_check (AST) → ok → validate (manim subprocess) → ok → END
                ↓                                  ↓
                 ←←←←←←←← LLM fix (patch / rewrite) ←←
```
- **`api_check`**: Pure-Python AST scan — catches undefined names, forbidden colors (`MAGENTA`, `CYAN`, `VIOLET`), and syntax errors before running Manim. Fast and cheap.
- **`validate`**: Runs the actual Manim subprocess with a 120 s timeout.
- **`fix`**: LLM receives line-numbered code + error message + static violations from `api_check`. Uses SEARCH/REPLACE patches where possible; falls back to FULL_REWRITE for syntax errors.
- **Error memory** (`prompts/error_memory.json`): successful fixes are recorded and injected as hints in future runs.

---

## Troubleshooting

**`ModuleNotFoundError: manim`** — Make sure your virtual environment is activated and `pip install -r requirements.txt` completed successfully.

**`FileNotFoundError: kokoro-v1.0.onnx`** — The Kokoro model files must be placed in the project root. See [Prerequisites](#prerequisites).

**`ffmpeg not found`** — Install FFmpeg and make sure it is on your system PATH.

**LaTeX errors in generated scenes** — Manim requires a LaTeX distribution (MiKTeX on Windows, TeX Live on Linux/macOS) for `MathTex` objects. Install it and re-run.

**Scenes fail even after 3 fix attempts** — Check `outputs/.../animation_outputs/validation_report.txt` for the full error history. You can also set `CODE_AGENT_DEBUG=1` to inspect the raw LLM prompts and responses.

---

## License

This project is released under the [MIT License](LICENSE).

The Kokoro TTS model (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) is distributed separately under its own license — see the [Kokoro repository](https://huggingface.co/hexgrad/Kokoro-82M) for details.

