from render import render_animation

test_code = '''```python
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait()
```'''

render_animation(test_code) 