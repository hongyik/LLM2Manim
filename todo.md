# Project TODO

## ✅ Done

### 1. Manim Code Alignment
Ensure all generated Manim code follows strict API conventions and is consistent
across scenes.

**Resolved by:**
- `api_check.py` — AST pre-check catches undefined names, forbidden colors, syntax errors before any subprocess call
- `_sanitize_scene_code()` in `code_agent.py` and `scene_fix_graph.py` — auto-fixes `camera_frame → camera.frame`, `radians= → angle=`, wrong Kokoro import
- `prompts/manim_rules.md` — injected into code_gen system prompt as authoritative rule reference
- `prompts/manim_allowlist.json` — 582 valid Manim CE symbols used by `api_check.py`
- Self-reflection loop in `code_agent.py` — reviewer LLM checks generated code against `manim_rules.md` before writing to disk

---

### 2. Output Structure and Forced Kokoro Settings
Lock the output scene structure (`GenScene`, `VoiceoverScene`) and Kokoro TTS
configuration so LLMs cannot deviate from it.

**Resolved by:**
- `system_prompt_code.txt` — enforces `class GenScene(ThreeDScene, VoiceoverScene)` and `KokoroService(voice="af_sarah", lang="en-us")` as non-negotiable
- `_sanitize_scene_code()` — regex replaces any variant `KokoroService(...)` call back to the correct one
- `scene_fix_graph.py` invariant check — after every fix, verifies `GenScene` class name and `set_speech_service` call are still present

---

### 3. Layout Settings — via Skill or System Prompt?
Decide how to specify per-scene layout (where objects sit on screen).

**Resolved by:** `agent/layout_engine.py` — deterministic layout spec generator, runs as a dedicated pipeline node (node 5 of 10). Output injected into code_gen user prompt as `{layout_spec}`. No LLM needed for layout rules — handled deterministically.

---

### 4. Few-Shot Fine-Tuning or Rule-Based Learning?
Evaluate whether to fine-tune a model on Manim examples or stick with rule-based guidance.

**Resolved by:** Rule-based learning (concluded not to fine-tune at this stage). Reasons:
- Errors are constraint violations, not knowledge gaps — fine-tuning does not fix them
- Insufficient data (need 500+ quality pairs for meaningful improvement)
- Current RAG + rules + error memory + self-reflection closes ~80% of the gap fine-tuning would give
- Re-evaluate when the pipeline has accumulated 500+ successful `(description → working code)` pairs

---

## 🔲 Future Work

### 5. Add More API Provider Options
Currently supports: DeepSeek, OpenAI (GPT-4), Anthropic (Claude).

**Remaining work:**
- Add Google Gemini (via `langchain-google-genai`)
- Add Mistral / Groq / local Ollama endpoints
- Add per-stage fallback chain (e.g. if DeepSeek rate-limits → fall back to OpenAI automatically)
- Validate API keys at startup with a clear error message per provider

---

### 6. Packaging for Local Deployment by Others
Make the project deployable by others (similar to how tools like Open WebUI or
LocalAI allow self-hosting), with a web interface and packaged core.

**Remaining work:**
- Docker / docker-compose setup (Python env, FFmpeg, Manim, Kokoro models bundled)
- Simple web UI (FastAPI backend + minimal frontend) for submitting topics and watching pipeline progress
- Encapsulate core pipeline as an importable Python package (`pip install amp-pipeline`)
- Config wizard for first-time setup (API keys, voice selection, render quality)
- One-click installer / setup script for Windows and Linux
