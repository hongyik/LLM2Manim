# LangChain Agent Version – Animated Math & Physics

This folder implements the same animation pipeline as the parent project using **LangChain** in an **agent-like** way, with:

1. **Dynamic animation plan** – Stage 2 is not fixed; the number and content of steps depend on the user input (e.g. simple topic → fewer steps, complex topic → more steps).
2. **Step memory** – When generating each step’s description, the agent sees the **full plan** and the **descriptions of all previous steps**, so the narrative stays consistent and each step builds on the others.

## Pipeline

The pipeline is a **LangGraph**: each stage is a node. To visualize it and save a diagram:

```bash
cd langchain_agent
python visualize_pipeline.py   # or use your venv Python
```

This writes `pipeline_graph.md` (Mermaid, renders on GitHub), `pipeline_graph.mmd`, and optionally `pipeline_graph.png`. See [pipeline_graph.md](pipeline_graph.md) for the diagram.

| Stage | What it does |
|-------|----------------|
| 1 | Parse user input (topic/concept). |
| 2 | **Planner agent**: From the topic, produce a structured plan (list of steps with `id` and `goal`). Plan is **dynamic** (depends on input). |
| 3 | **Step agent**: For each step, generate an animation description with **memory** of the plan and all previous step descriptions. |
| 4 | **Code agent**: Generate Manim code for each step (reuses parent project’s code prompts). |
| 5 | **LangGraph auto-fix**: For each scene, validate (run Manim); if it fails, LLM fixes the code and we re-validate in a loop (up to 2 attempts per scene). |
| 6 | **Render & combine**: Render each step’s Manim scene **in parallel**, then concatenate all videos (in plan order) into one final MP4 using FFmpeg. |

## Setup

From the repo root (or from this folder):

```bash
cd langchain_agent
pip install -r requirements.txt
```

Set API keys (same as parent project), e.g. in a `.env` in the repo root:

- `DEEPSEEK_API_KEY` (or use `LLM_PROVIDER=openai` and `GPT4_API_KEY`)

### Per-stage API/model selection

Each stage can use a **different** provider and model. Set these in your environment (or `.env`):

| Variable | Default | Description |
|----------|--------|-------------|
| `LLM_PROVIDER` | `deepseek` | Fallback when a stage does not set its own. |
| `PLANNER_PROVIDER` | same as `LLM_PROVIDER` | Provider: `deepseek`, `openai`, or `anthropic`. |
| `PLANNER_MODEL` | per-provider default | Model for the planner. |
| `STEP_PROVIDER` | same as `LLM_PROVIDER` | Provider for the step-description stage. |
| `STEP_MODEL` | per-provider default | Model for step descriptions. |
| `CODE_PROVIDER` | same as `LLM_PROVIDER` | Provider for the code-generation stage. |
| `CODE_MODEL` | per-provider default | Model for Manim code generation. |

For **anthropic** (Claude): set `ANTHROPIC_API_KEY` and optionally `ANTHROPIC_MODEL`; install with `pip install langchain-anthropic`.

Example: DeepSeek for planning, GPT-4 for code:

```bash
PLANNER_PROVIDER=deepseek
CODE_PROVIDER=openai
CODE_MODEL=gpt-4o
DEEPSEEK_API_KEY=sk-...
GPT4_API_KEY=sk-...
```

Example: add Claude for the step stage:

```bash
PLANNER_PROVIDER=deepseek
STEP_PROVIDER=anthropic
CODE_PROVIDER=openai
DEEPSEEK_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GPT4_API_KEY=sk-...
# pip install langchain-anthropic
```

## Example usage

### 1. Command line

From the `langchain_agent` directory (or repo root with `python langchain_agent/main.py`):

```bash
cd langchain_agent

# Topic as argument
python main.py "Explain the material derivative in fluid flow"

# Or prompt for topic
python main.py
# Then type e.g.: Geometric interpretation of the derivative at x=2
```

### 2. Programmatic (Python)

Run the full pipeline from your own script; the pipeline is a LangGraph, so you can also inspect or reuse the graph.

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path("path/to/Animated-math-and-physics/langchain_agent").resolve()))

from agent.pipeline_graph import run_pipeline, build_pipeline_graph

# One-shot: run entire pipeline
result = run_pipeline("Explain the chain rule with a simple example")
if result["status"] == "success":
    plan = result["stages"]["plan"]["steps"]
    video_path = result["stages"].get("combined_scene_path")
    print("Steps:", [s["id"] for s in plan])
    print("Video:", video_path)
else:
    print("Error:", result["error"])

# Or use the graph directly (e.g. for streaming or custom state)
graph = build_pipeline_graph()
app = graph.compile()
final_state = app.invoke({"user_input": "Derivative of x^2", "stages": {}})
print(final_state.get("plan"), final_state.get("stages", {}).keys())
```

### 3. Load env from `.env`

If you use a `.env` file in the project root:

```python
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from agent.pipeline_graph import run_pipeline
result = run_pipeline("Your math topic here")
```

## Run (CLI)

From the `langchain_agent` directory:

```bash
python main.py "Explain the material derivative in fluid flow"
# or
python main.py
# then enter topic when prompted
```

Outputs (per run, under a **timestamped folder**):

- `outputs/<YYYY-MM-DD_HH-MM-SS>/` – one folder per run (current date and time when the run started).
  - `animation_outputs/` – `animation_descriptions.json`, `<step_id>.py`, `generated_code.json`.
  - `final_animation/` – `individual_scenes/<step_id>.mp4`, `combined_animation.mp4`.

### Rendering (Stage 5)

- **Manim** and **FFmpeg** must be installed for video output.
- Optional env: `MANIM_RENDER_QUALITY` (default `l`; use `m` or `h` for higher quality), `MANIM_CLI` (default `python -m manim`).

## Design

- **Planner** (`agent/planner.py`): One LLM call that returns a JSON list of `{id, goal}`. No fixed template; the model decides how many steps and what each step is.
- **Step agent** (`agent/step_agent.py`): Runs **sequentially**. For step *i*, the prompt includes the full plan and the text of steps 1…*i*−1 so each step “remembers” the others.
- **Code agent** (`agent/code_agent.py`): Uses the parent project’s `system_prompt_code.txt` and `user_prompt_code_template.txt` to generate Manim code from each step description.
- **Scene auto-fix** (`agent/scene_fix_graph.py`): **LangGraph** workflow: `validate` (run Manim) → on failure → `fix` (LLM rewrites code from error + code) → `validate` again, until success or max attempts. Uses the same stage config as code gen (e.g. `CODE_PROVIDER`).
- **Render** (`agent/render.py`): Renders each step’s `.py` in **parallel** (multiprocessing), then merges the resulting MP4s with FFmpeg in plan order into `final_animation/combined_animation.mp4`.
