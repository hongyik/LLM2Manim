"""
Short-term working memory ledger for one pipeline run.

Tracks notation, visual style, scene objects, story progress, and constraints
across all steps so that descriptions and code stay mutually consistent.

Append-only: existing entries are never overwritten, only added to.
"""
import json
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Ledger:
    notation: Dict[str, str] = field(default_factory=dict)      # symbol -> definition
    visual_style: Dict[str, str] = field(default_factory=dict)  # key -> value
    objects: Dict[str, str] = field(default_factory=dict)       # name -> description
    story_so_far: List[str] = field(default_factory=list)       # key conclusions so far
    constraints: List[str] = field(default_factory=list)        # invariants for future steps

    def apply_updates(self, updates: dict) -> None:
        """Merge LLM-generated updates into the ledger (append-only; never overwrites)."""
        for k, v in updates.get("notation", {}).items():
            if k not in self.notation:
                self.notation[k] = v
        for k, v in updates.get("visual_style", {}).items():
            if k not in self.visual_style:
                self.visual_style[k] = v
        for k, v in updates.get("objects", {}).items():
            if k not in self.objects:
                self.objects[k] = v
        for bullet in updates.get("story_so_far", []):
            if bullet and bullet not in self.story_so_far:
                self.story_so_far.append(bullet)
        for constraint in updates.get("constraints", []):
            if constraint and constraint not in self.constraints:
                self.constraints.append(constraint)

    def to_text(self) -> str:
        """Human-readable representation for LLM prompts."""
        if not any([self.notation, self.visual_style, self.objects,
                    self.story_so_far, self.constraints]):
            return "(Ledger is empty — this is the first step.)"
        lines = []
        if self.notation:
            lines.append("NOTATION (symbol -> definition):")
            for k, v in self.notation.items():
                lines.append(f"  {k}: {v}")
        if self.visual_style:
            lines.append("VISUAL STYLE:")
            for k, v in self.visual_style.items():
                lines.append(f"  {k}: {v}")
        if self.objects:
            lines.append("SCENE OBJECTS:")
            for k, v in self.objects.items():
                lines.append(f"  {k}: {v}")
        if self.story_so_far:
            lines.append("STORY SO FAR (key conclusions):")
            for b in self.story_so_far:
                lines.append(f"  - {b}")
        if self.constraints:
            lines.append("CONSTRAINTS (do not violate):")
            for c in self.constraints:
                lines.append(f"  ! {c}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "notation": dict(self.notation),
            "visual_style": dict(self.visual_style),
            "objects": dict(self.objects),
            "story_so_far": list(self.story_so_far),
            "constraints": list(self.constraints),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Ledger":
        return cls(
            notation=d.get("notation", {}),
            visual_style=d.get("visual_style", {}),
            objects=d.get("objects", {}),
            story_so_far=d.get("story_so_far", []),
            constraints=d.get("constraints", []),
        )
