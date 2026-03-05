"""
Layout Engine: deterministic placement system for Manim scenes.

Pipeline position: step_descriptions → [layout_engine] → code_gen

Flow:
  description text  →  extract_manifest()  →  ContentManifest
  ContentManifest   →  compute_layout()    →  LayoutSpec
  LayoutSpec        →  to_prompt_text()    →  injected into code_gen user prompt

The LLM then follows the LayoutSpec coordinates instead of guessing placement,
which eliminates element overlap and produces consistent visual balance.

Algorithm (greedy, deterministic — no solver needed):
  Step A: classify template (T1–T5) from element roles
  Step B: assign each element to a zone (title/left/right/top/bottom/content)
  Step C: vertical-stack elements within each zone (priority order, scale if overflow)
  Step D: emit PlacedElement list with Manim-ready (cx, cy) + font_size + anim_group
"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ── Canvas (Manim Community defaults, 16:9) ───────────────────────────────────
# Frame x ∈ [-7.111, 7.111],  y ∈ [-4.0, 4.0]
FRAME_W = 14.222
FRAME_H = 8.0
MARGIN_X = 0.6    # horizontal safe-zone margin
MARGIN_Y = 0.45   # vertical safe-zone margin
SAFE_X_MIN = -(FRAME_W / 2 - MARGIN_X)   # -6.511
SAFE_X_MAX =  (FRAME_W / 2 - MARGIN_X)   #  6.511
SAFE_Y_MIN = -(FRAME_H / 2 - MARGIN_Y)   # -3.555
SAFE_Y_MAX =  (FRAME_H / 2 - MARGIN_Y)   #  3.555


# ── Zone definitions (Manim coords) ──────────────────────────────────────────
def _z(xl: float, xr: float, yb: float, yt: float) -> dict:
    """Build a zone dict from left/right/bottom/top Manim coords."""
    return {
        "cx": (xl + xr) / 2, "cy": (yb + yt) / 2,
        "w": xr - xl,        "h": yt - yb,
        "x_min": xl, "x_max": xr, "y_min": yb, "y_max": yt,
    }

ZONES: Dict[str, dict] = {
    # Title strip: top 18% of safe area
    "title":   _z(SAFE_X_MIN, SAFE_X_MAX, 2.5,        SAFE_Y_MAX),
    # Full content area: below title
    "content": _z(SAFE_X_MIN, SAFE_X_MAX, SAFE_Y_MIN, 2.3),
    # T2 split: left 47% / right 47% (gap in middle)
    "left":    _z(SAFE_X_MIN, -0.35,      SAFE_Y_MIN, 2.3),
    "right":   _z(0.35,       SAFE_X_MAX, SAFE_Y_MIN, 2.3),
    # T3 split: top 40% / bottom 42% of content
    "top":     _z(SAFE_X_MIN, SAFE_X_MAX, 0.2,        2.3),
    "bottom":  _z(SAFE_X_MIN, SAFE_X_MAX, SAFE_Y_MIN, 0.0),
    # Footer strip
    "footer":  _z(SAFE_X_MIN, SAFE_X_MAX, SAFE_Y_MIN, SAFE_Y_MIN + 0.9),
}


# ── Role metadata ─────────────────────────────────────────────────────────────
ROLE_PRIORITY: Dict[str, int] = {
    "title": 100, "key_takeaway": 90, "figure": 80,
    "equation": 75, "bullets": 70, "code": 60,
    "annotation": 50, "callout": 50, "decoration": 10,
}

ROLE_FONT_SIZE: Dict[str, int] = {
    "title": 44, "key_takeaway": 34,
    "equation": 40, "bullets": 30,
    "annotation": 26, "callout": 24, "code": 28,
}

ROLE_ANIM: Dict[str, str] = {
    "title": "Write",        "key_takeaway": "FadeIn",
    "equation": "Write",     "bullets": "FadeIn",
    "figure": "Create",      "annotation": "FadeIn",
    "callout": "FadeIn",     "code": "Write",
}

# Content budget — prevent information overload per scene
BUDGET = {
    "max_bullets": 5,
    "max_equations": 2,
    "max_callouts": 3,
    "min_font_scale": 0.65,   # never scale below 65%
}


# ── Data classes ──────────────────────────────────────────────────────────────
@dataclass
class ContentElement:
    """A single logical content element in a scene."""
    id: str           # unique id (role name used as id when only one of each)
    role: str         # title / equation / figure / bullets / key_takeaway / callout / annotation
    label: str = ""   # short description hint for the LLM
    count: int = 1    # for bullets: number of items; for equations: number


@dataclass
class ContentManifest:
    """Structured description of what a scene contains."""
    scene_id: str
    elements: List[ContentElement] = field(default_factory=list)

    def roles(self) -> List[str]:
        return [e.role for e in self.elements]

    def has(self, role: str) -> bool:
        return role in self.roles()

    def get(self, role: str) -> Optional[ContentElement]:
        return next((e for e in self.elements if e.role == role), None)


@dataclass
class PlacedElement:
    """A content element with all layout decisions resolved."""
    id: str
    role: str
    label: str
    zone: str
    cx: float         # Manim x-center
    cy: float         # Manim y-center
    font_size: int
    scale: float      # scale relative to default (1.0 = no scaling)
    z_index: int
    anim_in: str      # Manim animation class
    anim_group: int   # elements in the same group animate in the same voiceover beat


@dataclass
class LayoutSpec:
    """Complete layout decision for one scene."""
    scene_id: str
    template: str
    elements: List[PlacedElement] = field(default_factory=list)

    def to_prompt_text(self) -> str:
        """Render as human-readable text for injection into the code_gen prompt."""
        lines = [
            f"--- LAYOUT SPEC  scene={self.scene_id}  template={self.template} ---",
            "Follow these placement instructions exactly when creating Manim objects.",
            "After creating each object call: obj.move_to(np.array([x, y, 0]))",
            "",
            f"  {'ID':<20} {'ZONE':<8} {'CX':>6} {'CY':>6} {'FS':>4} {'SC':>5} {'Z':>3} {'ANIM_IN':<10} GRP",
            f"  {'-'*20} {'-'*8} {'-'*6} {'-'*6} {'-'*4} {'-'*5} {'-'*3} {'-'*10} ---",
        ]
        for el in self.elements:
            lines.append(
                f"  {el.id:<20} {el.zone:<8} {el.cx:>6.2f} {el.cy:>6.2f}"
                f" {el.font_size:>4} {el.scale:>5.2f} {el.z_index:>3}"
                f" {el.anim_in:<10} {el.anim_group}"
            )
        lines += [
            "",
            "KEY RULES:",
            "  - anim_group=0 → first voiceover beat (title intro)",
            "  - anim_group=1 → second voiceover beat (primary content)",
            "  - anim_group=2 → third beat (secondary content / figure)",
            "  - anim_group=3+ → later beats (annotations, callouts, highlights)",
            "  - Elements in the same anim_group go INSIDE the same 'with self.voiceover' block.",
            "  - Objects with higher z_index render on top of lower z_index objects.",
            "  - Stay within safe area: x ∈ [-6.5, 6.5],  y ∈ [-3.5, 3.5].",
            "  - Create each element BEFORE its 'with self.voiceover' block, animate INSIDE it.",
        ]
        return "\n".join(lines)


# ── Template selection ────────────────────────────────────────────────────────
def _select_template(manifest: ContentManifest) -> str:
    """
    T1 single_column:         no figure — text/equation stacked vertically
    T2 left_text_right_fig:   figure + text (most common)
    T3 top_eq_bottom_fig:     equation on top, figure below
    T4 two_column_compare:    explicit compare element
    T5 full_figure_overlays:  figure dominant, annotations overlay
    """
    has_fig = manifest.has("figure")
    has_eq  = manifest.has("equation")
    has_txt = manifest.has("bullets") or manifest.has("key_takeaway")

    if manifest.has("compare"):
        return "T4"
    if has_fig and has_eq and not has_txt:
        return "T3"   # equation on top, figure below
    if has_fig and has_txt:
        return "T2"   # text left, figure right
    if has_fig and has_eq:
        return "T3"
    if has_fig and len(manifest.elements) >= 4:
        return "T5"   # figure dominates with overlays
    return "T1"       # text only


# ── Zone assignment ───────────────────────────────────────────────────────────
def _assign_zones(manifest: ContentManifest, template: str) -> Dict[str, str]:
    """Assign each element to a named zone based on the selected template."""
    assignments: Dict[str, str] = {}

    for el in manifest.elements:
        if el.role == "title":
            assignments[el.id] = "title"
            continue
        if el.role == "footer":
            assignments[el.id] = "footer"
            continue

        if template == "T1":
            assignments[el.id] = "content"

        elif template == "T2":
            # figure → right; everything else → left
            assignments[el.id] = "right" if el.role == "figure" else "left"

        elif template == "T3":
            # equation / text → top; figure → bottom
            if el.role == "figure":
                assignments[el.id] = "bottom"
            else:
                assignments[el.id] = "top"

        elif template == "T4":
            # split: figure/key_takeaway/callout → right; rest → left
            right_roles = {"figure", "key_takeaway", "callout"}
            assignments[el.id] = "right" if el.role in right_roles else "left"

        else:  # T5
            assignments[el.id] = "content"   # all overlaid

    return assignments


# ── Vertical stacker ──────────────────────────────────────────────────────────
def _natural_height(el: ContentElement, font_size: int) -> float:
    """Estimate element height in Manim units (rough but consistent)."""
    lh = font_size / 100.0 * 1.15   # one line height in Manim units
    if el.role == "title":           return lh * 1.1
    if el.role == "equation":        return lh * 2.4
    if el.role == "bullets":         return lh * 1.5 * min(el.count, BUDGET["max_bullets"])
    if el.role == "figure":          return 3.2
    if el.role in ("key_takeaway", "annotation", "callout"):
        return lh * 1.6
    return lh * 1.5


def _stack(elements: List[ContentElement], zone: dict,
           gap: float = 0.3) -> List[Tuple[ContentElement, float, float, float]]:
    """
    Stack elements top→bottom inside zone (highest priority first).
    Returns [(element, cx, cy, scale)] with scale applied uniformly if overflow.
    """
    if not elements:
        return []

    # Highest priority → top of zone
    sorted_els = sorted(elements, key=lambda e: -ROLE_PRIORITY.get(e.role, 50))
    natural = [(e, _natural_height(e, ROLE_FONT_SIZE.get(e.role, 30)))
               for e in sorted_els]

    total_h = sum(h for _, h in natural) + gap * max(0, len(natural) - 1)
    scale = 1.0
    if total_h > zone["h"]:
        scale = max(BUDGET["min_font_scale"], zone["h"] / total_h)

    results = []
    y = zone["y_max"]
    for el, h in natural:
        eff_h = h * scale
        cy = y - eff_h / 2
        results.append((el, zone["cx"], round(cy, 3), round(scale, 3)))
        y -= eff_h + gap * scale

    return results


# ── Animation group assignment ────────────────────────────────────────────────
# Zones → voice beat order: title first, then primary content, then secondary
_ZONE_BEAT: Dict[str, int] = {
    "title": 0,
    "left": 1, "top": 1, "content": 1,    # primary content zones
    "right": 2, "bottom": 2,               # secondary content zones
    "footer": 3,
}


# ── Main entry point ──────────────────────────────────────────────────────────
def compute_layout(manifest: ContentManifest) -> LayoutSpec:
    """Run the greedy layout algorithm. Returns a fully resolved LayoutSpec."""
    template = _select_template(manifest)
    zone_assignments = _assign_zones(manifest, template)

    # Group elements by zone
    zone_groups: Dict[str, List[ContentElement]] = {}
    for el in manifest.elements:
        z = zone_assignments.get(el.id, "content")
        zone_groups.setdefault(z, []).append(el)

    placed: List[PlacedElement] = []
    zone_order = ["title", "left", "top", "content", "right", "bottom", "footer"]

    for zone_name in zone_order:
        els = zone_groups.get(zone_name, [])
        if not els:
            continue
        zone = ZONES.get(zone_name, ZONES["content"])
        anim_group = _ZONE_BEAT.get(zone_name, 1)
        stacked = _stack(els, zone)

        for el, cx, cy, scale in stacked:
            fs = max(18, int(ROLE_FONT_SIZE.get(el.role, 30) * scale))
            placed.append(PlacedElement(
                id=el.id, role=el.role, label=el.label,
                zone=zone_name, cx=round(cx, 3), cy=cy,
                font_size=fs, scale=scale,
                z_index=ROLE_PRIORITY.get(el.role, 50),
                anim_in=ROLE_ANIM.get(el.role, "FadeIn"),
                anim_group=anim_group,
            ))

    return LayoutSpec(scene_id=manifest.scene_id, template=template, elements=placed)


# ── Keyword-based manifest extraction (no LLM call) ──────────────────────────
_KEYWORDS: Dict[str, List[str]] = {
    "equation":     [r"equat", r"formula", r"derivat", r"integral",
                     r"\blaw\b", r"theorem", r"proof", r"\bsum\b"],
    "figure":       [r"diagram", r"figure", r"graph", r"plot", r"visual",
                     r"animat", r"illustrat", r"axes", r"coordinat",
                     r"spring", r"wave", r"circle", r"particle",
                     r"pendulum", r"vector", r"arrow", r"simulat"],
    "bullets":      [r"bullet", r"list", r"\bpoints?\b", r"\bsteps?\b",
                     r"propert", r"overview", r"introduc", r"comparison"],
    "key_takeaway": [r"takeaway", r"conclusion", r"key result",
                     r"highlight", r"important.*result"],
    "callout":      [r"callout", r"label", r"annotati", r"highlight.*term"],
}


def extract_manifest(scene_id: str, description: str) -> ContentManifest:
    """
    Keyword-based extraction of ContentManifest from a scene description.
    Always includes a title element. No LLM call — runs in microseconds.
    """
    desc = description.lower()
    elements: List[ContentElement] = [
        ContentElement(id="title", role="title", label=scene_id.title())
    ]

    for role, patterns in _KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, desc):
                if not any(e.id == role for e in elements):
                    count = 1
                    if role == "bullets":
                        m = re.search(r"(\d+)\s*(bullet|point|step|item|propert)", desc)
                        count = int(m.group(1)) if m else 4
                    elif role == "equation":
                        count = min(BUDGET["max_equations"],
                                    len(re.findall(r"equat|formula|derivat", desc)) or 1)
                    elements.append(ContentElement(
                        id=role, role=role, label=role, count=count
                    ))
                break   # found this role, move to next

    return ContentManifest(scene_id=scene_id, elements=elements)


def build_layout_specs(step_results: dict) -> Dict[str, str]:
    """
    Main entry: given {step_id: {"description": "..."}} from step_agent,
    returns {step_id: layout_spec_prompt_text} ready for injection into code_gen.
    """
    specs: Dict[str, str] = {}
    for scene_id, data in step_results.items():
        desc = data.get("description", "")
        manifest = extract_manifest(scene_id, desc)
        spec = compute_layout(manifest)
        specs[scene_id] = spec.to_prompt_text()
    return specs
