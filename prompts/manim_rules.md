# Manim CE API Rules (v0.17+)
## This project uses: manim, manim_voiceover, kokoro_mv

---

## Required imports (always use these exact lines)
```python
from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np
```

---

## Scene skeleton (never deviate from this structure)
```python
class GenScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        # ... animations ...
```
- Class MUST be named `GenScene`
- MUST subclass `VoiceoverScene` (not `Scene`, not `ThreeDScene` unless truly needed)
- MUST call `set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))` first

---

## Valid color constants
Only these are guaranteed to exist in manim:
`RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, PINK, TEAL, GOLD, MAROON,
WHITE, GRAY, GREY, BLACK, DARK_BLUE, DARK_BROWN, DARK_GRAY, DARK_GREY,
LIGHT_GRAY, LIGHT_GREY, LIGHT_PINK, LIGHT_BROWN, RED_A, RED_B, RED_C,
RED_D, RED_E, GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E,
BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E`

**FORBIDDEN** (do not use — they do not exist):
`MAGENTA, CYAN, VIOLET, INDIGO, LIME, AMBER, NAVY`

Use hex strings for other colors: `"#FF00FF"` instead of MAGENTA, `"#00FFFF"` instead of CYAN.

---

## Animation functions — valid signatures
```python
# ✅ Correct
FadeIn(mob)
FadeIn(mob, shift=UP)          # shift must be a numpy/manim direction vector
FadeOut(mob)
FadeOut(mob, shift=DOWN)
Create(mob)
Write(mob)                     # for Text and MathTex
Transform(mob_a, mob_b)
ReplacementTransform(mob_a, mob_b)
GrowArrow(arrow)
GrowFromCenter(mob)
MoveAlongPath(mob, path)

# ❌ Wrong
FadeIn(mob, UP)                # positional arg for direction is not supported
Rotate(mob, radians=PI/4)      # use angle= not radians=
self.camera_frame              # use self.camera.frame
```

---

## Rotate / Indicate animations
```python
# ✅ Correct
self.play(Rotate(mob, angle=PI/4))
self.play(Rotate(mob, angle=PI/2, about_point=ORIGIN))
self.play(Indicate(mob))
self.play(Flash(mob))
self.play(Circumscribe(mob))

# ❌ Wrong
self.play(Rotate(mob, radians=PI/4))   # radians= is not a valid kwarg
```

---

## Geometry objects — safe patterns
```python
# Line and DashedLine: start and end MUST be different points
line = Line(start=LEFT*2, end=RIGHT*2)         # ✅
dline = DashedLine(start=LEFT*2, end=RIGHT*2)  # ✅
# NEVER: DashedLine(start=ORIGIN, end=ORIGIN)  ← zero-length → crash

# Arrow
arrow = Arrow(start=ORIGIN, end=RIGHT*2, buff=0)

# Axes — always set explicit ranges
axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    axis_config={"color": WHITE},
)

# NumberPlane — limit range to avoid memory issues
plane = NumberPlane(x_range=[-5, 5], y_range=[-3, 3])

# VGroup — only accepts Mobject instances, never strings
group = VGroup(circle, square, text)   # ✅
group = VGroup("hello", circle)        # ❌ strings are not Mobjects
```

---

## MathTex / Tex — LaTeX rules
```python
# Always use raw strings to avoid Python escape issues
eq = MathTex(r"\frac{d\Phi}{dt} = \frac{\partial\Phi}{\partial t} + \vec{u} \cdot \nabla\Phi")

# ✅ valid LaTeX in MathTex
MathTex(r"\omega", r"\alpha", r"\vec{v}")
MathTex(r"x(t) = A\cos(\omega t + \phi)")
MathTex(r"\frac{\partial f}{\partial x}")

# ❌ common mistakes
MathTex("\\frac{...}")    # use r"..." raw strings instead
Tex("$$x = y$$")          # $$ in Tex causes "Missing $ inserted" error; use $x = y$ or no $
MathTex("$x = y$")        # MathTex adds $ automatically; don't add them yourself
```

---

## Positioning
```python
mob.to_edge(UP)
mob.to_edge(DOWN)
mob.to_edge(LEFT)
mob.to_edge(RIGHT)
mob.move_to(ORIGIN)
mob.next_to(other_mob, UP, buff=0.3)
mob.shift(RIGHT * 2)
mob.scale(0.8)
```

---

## ValueTracker pattern (for dynamic values)
```python
tracker = ValueTracker(0)
dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), np.sin(tracker.get_value()))))
self.add(dot)
self.play(tracker.animate.set_value(2 * PI), run_time=3)
```

---

## Camera (MovingCameraScene)
```python
# ✅ Correct (manim >= 0.17)
self.camera.frame.animate.scale(0.5)
self.camera.frame.animate.move_to(some_point)

# ❌ Wrong
self.camera_frame   # renamed in v0.17
```

---

## Voiceover pattern
```python
with self.voiceover(text="Spoken text here.") as tracker:
    self.play(Create(mob), run_time=tracker.duration)
self.wait(0.5)
```

---

## Common mistakes to avoid
1. Do NOT invent function names — if unsure, use simpler built-ins
2. Do NOT use color constants not listed above
3. Do NOT call `Line(ORIGIN, ORIGIN)` or `DashedLine(p, p)` (zero length)
4. Do NOT add `$$` or `$` in `MathTex()`
5. Do NOT use `radians=` in animation kwargs — use `angle=`
6. Do NOT use `self.camera_frame` — use `self.camera.frame`
7. Do NOT pass strings into `VGroup()`
8. DO always end scenes with `self.play(FadeOut(container))` and `self.wait(1)`
