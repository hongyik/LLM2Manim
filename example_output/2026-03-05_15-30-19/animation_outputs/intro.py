from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Create background
        background = Rectangle(
            width=14, height=8,
            fill_color="#0F1B2F",
            fill_opacity=1,
            stroke_width=0
        )
        self.add(background)
        
        # ==================== BEAT 0: TITLE ====================
        title = Text("Linear Transformation", font_size=44, color=WHITE)
        title.move_to(np.array([0.00, 3.27, 0]))
        
        self.play(Write(title))
        self.wait(0.5)
        
        # ==================== BEAT 1: NUMBER FUNCTION ====================
        # Create left plane
        left_plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            },
            axis_config={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 2
            }
        )
        left_plane.move_to(np.array([-3.43, 0.70, 0]))
        
        # Create input point and label
        input_dot = Dot(point=np.array([1, 2, 0]), color=BLUE_C, radius=0.08)
        input_dot.move_to(left_plane.get_center() + np.array([1, 2, 0]))
        
        x_label = MathTex("x", color=BLUE_C, font_size=24)
        x_label.next_to(input_dot, RIGHT, buff=0.1)
        
        # Create arrow to number
        arrow_to_number = Arrow(
            start=input_dot.get_center(),
            end=left_plane.get_center() + np.array([5, 0, 0]),
            color="#00FF00",  # Pure green
            buff=0,
            stroke_width=4
        )
        
        # Create number 5 and function label
        number_five = MathTex("5", color=YELLOW, font_size=36)
        number_five.move_to(left_plane.get_center() + np.array([5, 0, 0]))
        
        func_label = MathTex(r"f(x) = 5", color=WHITE, font_size=28)
        func_label.next_to(number_five, DOWN, buff=0.3)
        
        # Voiceover for beat 1
        with self.voiceover(text="""
            In mathematics, we often study functions that map numbers to numbers. 
            But what about functions that map entire spaces to other spaces?
        """) as tracker:
            self.play(FadeIn(left_plane))
            self.play(Create(input_dot), Write(x_label))
            self.play(GrowArrow(arrow_to_number))
            self.play(FadeIn(number_five), Write(func_label))
        
        self.wait(0.5)
        
        # ==================== BEAT 2: VECTOR TRANSFORMATION ====================
        # Create right plane
        right_plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            },
            axis_config={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 2
            }
        )
        right_plane.move_to(np.array([3.43, 0.70, 0]))
        
        # Create output point and label
        output_dot = Dot(point=np.array([1, 2, 0]), color=BLUE_C, radius=0.08)
        output_dot.move_to(right_plane.get_center() + np.array([1, 2, 0]))
        
        Tx_label = MathTex(r"T(x)", color=BLUE_C, font_size=24)
        Tx_label.next_to(output_dot, RIGHT, buff=0.1)
        
        # Create new arrow (will transform from arrow_to_number)
        arrow_to_vector = Arrow(
            start=input_dot.get_center(),
            end=output_dot.get_center(),
            color="#00FF00",  # Pure green
            buff=0,
            stroke_width=4
        )
        
        # Create specific label
        specific_label = MathTex(r"T: \mathbb{R}^2 \to \mathbb{R}^2", color=WHITE, font_size=32)
        specific_label.to_edge(UP, buff=0.5)
        
        # Voiceover for beat 2
        with self.voiceover(text="""
            A linear transformation is a special kind of function. 
            Instead of mapping numbers, it maps vectors to vectors, 
            and it does so in a way that preserves the structure of the space.
        """) as tracker:
            self.play(FadeOut(number_five), FadeOut(func_label))
            self.play(FadeIn(right_plane))
            self.play(Transform(arrow_to_number, arrow_to_vector))
            self.play(FadeIn(output_dot), Write(Tx_label))
            self.play(Write(specific_label))
        
        self.wait(0.5)
        
        # ==================== BEAT 3: GENERAL DEFINITION ====================
        # Create general label
        general_label = MathTex(r"T: V \to W", color=WHITE, font_size=48)
        general_label.move_to(np.array([0, -1, 0]))
        
        # Create V and W labels
        V_label = MathTex(r"V", color=WHITE, font_size=28)
        V_label.next_to(left_plane, UP, buff=0.1)
        
        W_label = MathTex(r"W", color=WHITE, font_size=28)
        W_label.next_to(right_plane, UP, buff=0.1)
        
        # Voiceover for beat 3
        with self.voiceover(text="""
            Formally, if V and W are vector spaces, a linear transformation T 
            from V to W is a function that takes vectors from V as inputs 
            and outputs vectors in W.
        """) as tracker:
            self.play(FadeIn(general_label))
            self.play(
                Transform(specific_label, VGroup(V_label, W_label)),
                arrow_to_vector.animate.set_stroke(width=6)
            )
        
        self.wait(0.5)
        
        # ==================== BEAT 4: LINEARITY HINT ====================
        # Create continue arrow
        continue_arrow = Arrow(
            start=ORIGIN,
            end=np.array([0, -0.5, 0]),
            color=WHITE,
            buff=0,
            stroke_width=2
        )
        continue_arrow.move_to(np.array([0, -2.5, 0]))
        
        # Voiceover for beat 4
        with self.voiceover(text="""
            The key is in the word 'linear'. In the next step, we'll see 
            the two simple rules that define this linearity.
        """) as tracker:
            # Flash the word "Linear" in the title
            linear_part = title[:6]  # "Linear"
            self.play(
                Flash(linear_part, color=YELLOW, line_length=0.1, flash_radius=1.2),
                FadeIn(continue_arrow)
            )
        
        self.wait(1)
        
        # ==================== CLEANUP ====================
        # Group all objects for cleanup
        container = VGroup(
            title, left_plane, right_plane,
            input_dot, x_label, output_dot, Tx_label,
            arrow_to_vector, V_label, W_label,
            general_label, continue_arrow
        )
        self.play(FadeOut(container))
        self.wait(1)