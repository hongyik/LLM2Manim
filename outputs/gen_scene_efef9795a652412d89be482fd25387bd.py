from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class GenScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

        # 1️⃣ Definition: Boolean operations
        tree_root = Text("Root: Binary variable")
        true_node = Text("True").set_color(GREEN).next_to(tree_root, LEFT, buff=1)
        false_node = Text("False").set_color(RED).next_to(tree_root, RIGHT, buff=1)
        tree = VGroup(tree_root, true_node, false_node)
        tree.shift(UP)

        with self.voiceover(text="Boolean operations are fundamental in logic and computer science, dealing with binary variables that can either be True or False.") as tracker:
            self.play(Write(tree))
        self.wait(1)
        self.play(FadeOut(tree))

        # 2️⃣ Boolean operations formulas
        and_formula = MathTex("A \\land B").scale(1.5)
        or_formula = MathTex("A \\lor B").scale(1.5)
        not_formula = MathTex("\\neg A").scale(1.5)
        formulas = VGroup(and_formula, or_formula, not_formula).arrange(DOWN, buff=1)
        
        with self.voiceover(text="The primary Boolean operations are AND, OR, and NOT, represented as follows...") as tracker:
            self.play(FadeIn(and_formula))
            self.play(FadeIn(or_formula))
            self.play(FadeIn(not_formula))
        self.wait(1)
        self.play(FadeOut(formulas))

        # 3️⃣ Derivation of truth tables
        and_table_data = [
            ["A", "B", "A ∧ B"],
            ["True", "True", "True"],
            ["True", "False", "False"],
            ["False", "True", "False"],
            ["False", "False", "False"]
        ]
        and_table = Table(
            and_table_data,
            include_outer_lines=True,
            line_config={'stroke_width': 1}
        ).scale(0.75).shift(UP)

        with self.voiceover(text="For the AND operation, the truth table shows that the result is only True when both A and B are True...") as tracker:
            self.play(Create(and_table))
        self.wait(2)
        self.play(FadeOut(and_table))

        or_table_data = [
            ["A", "B", "A ∨ B"],
            ["True", "True", "True"],
            ["True", "False", "True"],
            ["False", "True", "True"],
            ["False", "False", "False"]
        ]
        or_table = Table(
            or_table_data,
            include_outer_lines=True,
            line_config={'stroke_width': 1}
        ).scale(0.75).shift(UP)

        with self.voiceover(text="In contrast, the OR operation results in True if at least one of A or B is True...") as tracker:
            self.play(Create(or_table))
        self.wait(2)
        self.play(FadeOut(or_table))

        not_table_data = [
            ["A", "¬ A"],
            ["True", "False"],
            ["False", "True"]
        ]
        not_table = Table(
            not_table_data,
            include_outer_lines=True,
            line_config={'stroke_width': 1}
        ).scale(0.75).shift(UP)
        
        with self.voiceover(text="The NOT operation simply inverts the value of A...") as tracker:
            self.play(Create(not_table))
        self.wait(2)
        self.play(FadeOut(not_table))

        # 4️⃣ Example: Light Control using Boolean operations
        switch_a = Rectangle(height=1, width=0.5, color=BLUE).shift(LEFT * 2)
        switch_a_label = Text("Switch A").scale(0.5).next_to(switch_a, DOWN)
        switch_b = Rectangle(height=1, width=0.5, color=BLUE).shift(RIGHT * 2)
        switch_b_label = Text("Switch B").scale(0.5).next_to(switch_b, DOWN)
        light_bulb = Circle(color=YELLOW).next_to(switch_a, UP, buff=2).set_fill(YELLOW, opacity=0.3)
        light_off_text = Text("OFF", color=RED).move_to(light_bulb)
        light_on_text = Text("ON", color=GREEN).move_to(light_bulb)
        
        self.play(FadeIn(switch_a, switch_a_label, switch_b, switch_b_label, light_bulb, light_off_text))
        
        with self.voiceover(text="Let's consider a light controlled by two switches. The light will only turn ON when both switches are ON.") as tracker:
            pass

        self.play(switch_a.animate.set_color(GREEN))
        self.wait(1)
        with self.voiceover(text="As we turn on both switches, the light turns ON, demonstrating the AND operation.") as tracker:
            self.play(switch_b.animate.set_color(GREEN))
            self.play(FadeOut(light_off_text))
            self.play(FadeIn(light_on_text))
        self.wait(2)

        # 5️⃣ Conclusion
        summary_text = Text("In summary, Boolean operations are essential in digital logic and computing. They dictate the behavior of systems based on binary states.", font_size=32)

        with self.voiceover(text="In summary, Boolean operations are essential in digital logic and computing. They dictate the behavior of systems based on binary states.") as tracker:
            self.play(FadeIn(summary_text))
        self.wait(2)

if __name__ == "__main__":
    scene = GenScene()
    scene.render()