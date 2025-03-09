from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Configure voiceover
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))

        # Scene 1: Introduction
        with self.voiceover(
            text="Welcome to today's lesson on Reynolds Transport Theorem, "
            "a fundamental tool in fluid mechanics that relates changes within "
            "a control volume to the behavior of fluid particles."
        ):
            title = Text("Reynolds Transport Theorem (RTT)", font_size=48)
            self.play(FadeIn(title))
        
        # Transition to definition
        with self.voiceover(
            text="Let's start by clearly defining Reynolds Transport Theorem."
        ):
            self.play(title.animate.shift(UP * 2))
            definition = Text(
                "Reynolds Transport Theorem links the rate of change\n"
                "of a fluid property within a moving fluid particle\n"
                "to the rate of change within a fixed region of space\n"
                "called a control volume.",
                font_size=32,
                line_spacing=1.2
            )
            self.play(FadeIn(definition))

        # Scene 2: Formula Derivation
        with self.voiceover(
            text="Here, B-sys is any extensive property of the fluid system, "
            "beta is that property per unit mass, rho is density, "
            "and V is fluid velocity."
        ):
            # Clear previous content
            self.play(FadeOut(title), FadeOut(definition))
            
            # Display the main RTT equation
            rtt_equation = MathTex(
                r"\frac{DB_{sys}}{Dt} = \frac{\partial}{\partial t}"
                r"\int_{CV}\beta \rho dV + \int_{CS}\beta \rho \mathbf{V}"
                r"\cdot d\mathbf{A}",
                font_size=42
            )
            self.play(Write(rtt_equation))

        # Create groups for equation components
        cv_term = MathTex(
            r"\frac{\partial}{\partial t}\int_{CV}\beta \rho dV",
            font_size=42,
            color=BLUE
        )
        cs_term = MathTex(
            r"\int_{CS}\beta \rho \mathbf{V}\cdot d\mathbf{A}",
            font_size=42,
            color=RED
        )

        # Highlight components
        with self.voiceover(
            text="The first integral represents accumulation within the control volume."
        ):
            self.play(
                rtt_equation.animate.shift(UP * 1.5),
                FadeIn(cv_term.next_to(rtt_equation, DOWN * 2))
            )

        with self.voiceover(
            text="The second integral represents flux across the control surface."
        ):
            self.play(FadeIn(cs_term.next_to(cv_term, DOWN)))

        # Scene Transition: Simplified version
        with self.voiceover(
            text="By simplifying, we see a clearer view: the total change equals "
            "accumulation within the volume plus net outflow through the boundary."
        ):
            # Clear previous equations
            self.play(FadeOut(cv_term), FadeOut(cs_term))
            
            simplified_eq = MathTex(
                r"\frac{DB_{sys}}{Dt} = \frac{\partial B_{CV}}{\partial t} + "
                r"\int_{CS}\beta \rho \mathbf{V}\cdot d\mathbf{A}",
                font_size=42
            )
            self.play(
                Transform(rtt_equation, simplified_eq)
            )

        # Scene: Practical Example with Pipe
        with self.voiceover(
            text="Consider fluid flowing through a pipe. We'll use the Reynolds "
            "Transport Theorem to analyze mass conservation."
        ):
            self.play(FadeOut(rtt_equation))
            
            # Create pipe visualization
            pipe = Rectangle(height=1.5, width=4, color=WHITE)
            cv_label = Text("Control Volume", font_size=24).next_to(pipe, UP)
            
            # Create flow arrows
            arrow_in = Arrow(
                start=LEFT * 3, 
                end=LEFT * 2, 
                color=BLUE,
                buff=0
            ).next_to(pipe, LEFT)
            arrow_out = Arrow(
                start=RIGHT * 2,
                end=RIGHT * 3,
                color=RED,
                buff=0
            ).next_to(pipe, RIGHT)
            
            pipe_group = VGroup(pipe, cv_label, arrow_in, arrow_out)
            self.play(Create(pipe_group))

        # Mass Conservation Equation
        with self.voiceover(
            text="Mass is neither created nor destroyed, so its material derivative "
            "must be zero. Hence, we arrive at a simplified form."
        ):
            mass_eq = MathTex(
                r"\frac{Dm}{Dt} = \frac{\partial}{\partial t}\int_{CV}\rho dV + "
                r"\int_{CS}\rho \mathbf{V}\cdot d\mathbf{A}",
                font_size=42
            ).to_edge(UP)
            self.play(Write(mass_eq))

        # Continuity Equation
        with self.voiceover(
            text="This is the continuity equation, stating that the mass accumulation "
            "plus the net mass flux must balance out."
        ):
            continuity_eq = MathTex(
                r"0 = \frac{\partial}{\partial t}\int_{CV}\rho dV + "
                r"\int_{CS}\rho \mathbf{V}\cdot d\mathbf{A}",
                font_size=42
            ).next_to(mass_eq, DOWN)
            self.play(Write(continuity_eq))

        # Animated Particles
        with self.voiceover(
            text="As fluid moves through our pipe, fluid particles entering and leaving "
            "illustrate the flux term. If inflow and outflow are equal, mass remains "
            "constant within the control volume."
        ):
            # Create animated particles
            particles = VGroup(*[
                Dot(color=BLUE_C) for _ in range(5)
            ])
            
            # Position particles along the pipe
            particle_positions = [
                pipe.get_left() + LEFT * 0.5 + UP * (i * 0.2 - 0.4)
                for i in range(5)
            ]
            for dot, pos in zip(particles, particle_positions):
                dot.move_to(pos)

            self.play(FadeIn(particles))
            
            # Animate particles moving through pipe
            self.play(
                *[
                    dot.animate.shift(RIGHT * 5)
                    for dot in particles
                ],
                run_time=3,
                rate_func=linear
            )

        # Final Example with Annotations
        with self.voiceover(
            text="Here, fluid enters the control volume at velocity V-in and leaves "
            "at V-out. The net mass flow determines whether the mass within the pipe "
            "increases, decreases, or remains constant."
        ):
            # Clear previous content except pipe
            self.play(
                FadeOut(mass_eq),
                FadeOut(continuity_eq),
                FadeOut(particles)
            )
            
            # Add velocity and density labels
            v_in = MathTex(r"V_{in}", font_size=32).next_to(arrow_in, UP)
            v_out = MathTex(r"V_{out}", font_size=32).next_to(arrow_out, UP)
            rho_in = MathTex(r"\rho_{in}", font_size=32).next_to(arrow_in, DOWN)
            rho_out = MathTex(r"\rho_{out}", font_size=32).next_to(arrow_out, DOWN)
            
            labels = VGroup(v_in, v_out, rho_in, rho_out)
            self.play(Write(labels))

        # Final simplified continuity equation
        with self.voiceover(
            text="If density is constant and the flow is steady, the accumulation "
            "term vanishes, simplifying the continuity equation further."
        ):
            final_eq = MathTex(
                r"\int_{CS}\rho \mathbf{V}\cdot d\mathbf{A} = 0",
                font_size=42
            ).to_edge(UP)
            self.play(Write(final_eq))

        # Conclusion
        with self.voiceover(
            text="To summarize, Reynolds Transport Theorem is a powerful method "
            "for linking system-wide changes to localized control volume analyses, "
            "essential for solving many fluid mechanics problems."
        ):
            # Display original RTT equation one last time
            conclusion_eq = MathTex(
                r"\frac{DB_{sys}}{Dt} = \frac{\partial}{\partial t}"
                r"\int_{CV}\beta \rho dV + \int_{CS}\beta \rho \mathbf{V}"
                r"\cdot d\mathbf{A}",
                font_size=42
            ).next_to(final_eq, DOWN)
            self.play(
                Write(conclusion_eq),
                FadeOut(pipe_group),
                FadeOut(labels)
            )
            
        # Final fade out
        self.play(
            FadeOut(final_eq),
            FadeOut(conclusion_eq)
        )