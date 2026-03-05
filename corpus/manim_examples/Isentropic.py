from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np
import random

class Isentropic(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Configure voiceover service with detailed voice instructions.
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        # Run each section
        self.section2()
        self.clear()
        self.section3()
        self.clear()

    def create_piston_cylinder(self):
        # Create cylinder
        cylinder = VGroup(
            Line(start=[-1, -2, 0], end=[-1, 1, 0], color=WHITE),
            Line(start=[1, -2, 0], end=[1, 1, 0], color=WHITE),
            Line(start=[-1, -2, 0], end=[1, -2, 0], color=WHITE)
        )
        
        # Create piston (movable top) - just the line, no rectangle
        piston = Line(start=[-1.2, 1, 0], end=[1.2, 1, 0], color=WHITE)
        
        # Create initial weights
        weights = VGroup(
            Rectangle(height=0.1, width=1.5, color=GRAY, fill_opacity=0.8)
        ).next_to(piston, UP, buff=0)
        
        return VGroup(cylinder, piston, weights)

    def create_particles(self, cylinder, num_particles=20):
        particles = VGroup()
        particle_velocities = []
        
        # Get cylinder dimensions from the VGroup
        left_wall = cylinder[0]  # First line in cylinder VGroup
        right_wall = cylinder[1] # Second line in cylinder VGroup
        bottom = cylinder[2]     # Third line in cylinder VGroup
        
        # Calculate bounds from cylinder lines
        x_min = left_wall.get_start()[0] + 0.2  # Add buffer from walls
        x_max = right_wall.get_start()[0] - 0.2
        y_min = bottom.get_start()[1] + 0.2
        y_max = left_wall.get_end()[1] - 0.2  # Leave space below piston
        
        for _ in range(num_particles):
            particle = Dot(radius=0.05)
            particle.set_fill(BLUE, opacity=0.8)
            
            # Random position within cylinder bounds
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            particle.move_to([x, y, 0])
            particles.add(particle)
            
            # Initialize with random velocity (higher speed)
            speed = 0.2  # Slightly reduced speed for better visualization
            theta = np.random.uniform(0, 2 * np.pi)
            vx = speed * np.cos(theta)
            vy = speed * np.sin(theta)
            particle_velocities.append(np.array([vx, vy]))
        
        return particles, particle_velocities

    def update_particles(self, cylinder, particles, velocities, dt):
        # Get cylinder bounds
        left_wall = cylinder[0]
        right_wall = cylinder[1]
        bottom = cylinder[2]
        
        x_min = left_wall.get_start()[0] + 0.2
        x_max = right_wall.get_start()[0] - 0.2
        y_min = bottom.get_start()[1] + 0.2
        y_max = left_wall.get_end()[1] - 0.2
        
        for i, particle in enumerate(particles):
            pos = particle.get_center()
            vel = velocities[i]
            
            # Update position
            new_x = pos[0] + vel[0] * dt
            new_y = pos[1] + vel[1] * dt
            
            # Boundary collisions with elastic response
            if new_x < x_min or new_x > x_max:
                velocities[i][0] *= -1  # Reflect velocity
                new_x = np.clip(new_x, x_min, x_max)  # Ensure within bounds
            
            if new_y < y_min or new_y > y_max:
                velocities[i][1] *= -1  # Reflect velocity
                new_y = np.clip(new_y, y_min, y_max)  # Ensure within bounds
            
            particle.move_to([new_x, new_y, 0])

    def create_nozzle(self):
        # Create nozzle shape using CubicBezier curves
        nozzle = VGroup()
        
        # Define control points for better nozzle shape
        inlet_height = 1.0
        throat_height = 0.5
        exit_height = 1.2
        
        # Inlet section (converging)
        inlet_top = CubicBezier(
            start_anchor=np.array([-2, inlet_height, 0]),
            start_handle=np.array([-1.5, inlet_height, 0]),
            end_handle=np.array([-0.5, throat_height + 0.1, 0]),
            end_anchor=np.array([0, throat_height, 0])
        )
        inlet_bottom = CubicBezier(
            start_anchor=np.array([-2, -inlet_height, 0]),
            start_handle=np.array([-1.5, -inlet_height, 0]),
            end_handle=np.array([-0.5, -throat_height - 0.1, 0]),
            end_anchor=np.array([0, -throat_height, 0])
        )
        
        # Exit section (diverging)
        exit_top = CubicBezier(
            start_anchor=np.array([0, throat_height, 0]),
            start_handle=np.array([0.5, throat_height + 0.1, 0]),
            end_handle=np.array([1.5, exit_height - 0.1, 0]),
            end_anchor=np.array([2, exit_height, 0])
        )
        exit_bottom = CubicBezier(
            start_anchor=np.array([0, -throat_height, 0]),
            start_handle=np.array([0.5, -throat_height - 0.1, 0]),
            end_handle=np.array([1.5, -exit_height + 0.1, 0]),
            end_anchor=np.array([2, -exit_height, 0])
        )
        
        nozzle.add(inlet_top, inlet_bottom, exit_top, exit_bottom)
        nozzle.set_color(WHITE)
        return nozzle

    def create_flow_arrows(self):
        # Create arrows to represent flow through nozzle
        arrows = VGroup()
        
        # Adjust x positions for smoother transition
        x_positions = np.concatenate([
            np.linspace(-1.8, -0.4, 5),  # Inlet section (add one more)
            np.linspace(-0.3, 0.3, 5),   # Throat section
            np.linspace(0.4, 1.8, 5)     # Exit section (add one more)
        ])
        
        for x in x_positions:
            # Calculate local nozzle height at this x position
            y_bound = self.get_nozzle_height(x)
            
            # Calculate number of arrows based on local height
            num_arrows = max(2, int(y_bound * 3))  # More arrows in wider sections
            y_positions = np.linspace(-y_bound * 0.7, y_bound * 0.7, num_arrows)
            
            # Calculate arrow properties based on position
            if abs(x) <= 0.3:  # Throat region
                length = 0.35  # Slightly shorter than current 0.4
                color = BLUE_B  # Brighter color
            else:
                # Smoother length transition
                area_ratio = y_bound / self.get_nozzle_height(0)
                length = 0.35 / np.sqrt(area_ratio)  # Use sqrt for smoother transition
                # Color gradient based on position
                t = abs(x) / 2.0  # Normalize position
                color = interpolate_color(BLUE_B, BLUE, t)
            
            for y in y_positions:
                # Smoother angle transition
                if x < -0.3:  # Converging section
                    angle = np.arctan2(-y * 0.2, 1.0)  # Reduce angle factor from 0.3 to 0.2
                elif x > 0.3:  # Diverging section
                    angle = np.arctan2(y * 0.2, 1.0)   # Reduce angle factor from 0.3 to 0.2
                else:  # Throat section
                    angle = 0  # Horizontal flow
                
                # Create arrow with calculated direction
                start = np.array([x, y, 0])
                end = start + length * np.array([np.cos(angle), np.sin(angle), 0])
                
                arrow = Arrow(
                    start=start,
                    end=end,
                    color=color,
                    buff=0.05,
                    max_tip_length_to_length_ratio=0.2,
                    stroke_width=2
                )
                arrows.add(arrow)
            
            # Add centerline arrow for each x position
            if x < 1.6:  # Stop before the last position to avoid arrow extending beyond nozzle
                start = np.array([x, 0, 0])
                end = start + length * np.array([1, 0, 0])  # Horizontal flow at centerline
                centerline_arrow = Arrow(
                    start=start,
                    end=end,
                    color=color,
                    buff=0.05,
                    max_tip_length_to_length_ratio=0.2,
                    stroke_width=2
                )
                arrows.add(centerline_arrow)
        
        return arrows

    def update_flow_arrows(self, arrows, dt):
        # Animate arrows by cycling their opacity
        for arrow in arrows:
            # Create pulsing effect
            t = self.time % 1.0  # Use scene time for smooth animation
            opacity = 0.5 + 0.5 * np.sin(2 * PI * t)  # Oscillate between 0.5 and 1.0
            arrow.set_opacity(opacity)

    def get_nozzle_height(self, x):
        # Helper function to get nozzle height at any x position
        if x < -2 or x > 2:
            return 1.0
        elif -2 <= x <= 0:  # Converging section
            t = (x + 2) / 2  # Normalize to [0,1]
            return 1.0 * (1 - t) + 0.5 * t  # Linear interpolation
        else:  # Diverging section
            t = x / 2  # Normalize to [0,1]
            return 0.5 * (1 - t) + 1.2 * t  # Linear interpolation

    def section2(self):
        # Introduction to Isentropic Relations
        with self.voiceover(text="""
            We've already learned about entropy in thermodynamics, and we know how ideal gases behave.
            Today, we'll combine these concepts to study a special type of flow: isentropic flow.
            When entropy stays constant and gases behave ideally, we get elegant relationships between pressure, temperature, and density.
            These powerful relations help us analyze high-speed flows in nozzles, diffusers, and jet engines.
            """) as tracker:
            # Create recap equation with animation
            recap_eq = MathTex("\\Delta S = 0", "\\quad \\text{(Constant Entropy)}").to_edge(UP)
            
            # Create assumption boxes with icons
            # First create content for each box
            ideal_gas_content = VGroup(
                Text("Ideal Gas", font_size=24),
                MathTex("pV = nRT")
            ).arrange(DOWN, buff=0.2)
            
            entropy_content = VGroup(
                Text("Constant Entropy", font_size=24),
                MathTex("ds = 0")
            ).arrange(DOWN, buff=0.2)
            
            # Create rectangles that surround the content
            ideal_gas_box = Rectangle(
                width=ideal_gas_content.width + 0.5,
                height=ideal_gas_content.height + 0.5,
                color=BLUE
            )
            
            entropy_box = Rectangle(
                width=entropy_content.width + 0.5,
                height=entropy_content.height + 0.5,
                color=RED
            )
            
            # Group content with their boxes
            ideal_gas_group = VGroup(ideal_gas_box, ideal_gas_content)
            entropy_group = VGroup(entropy_box, entropy_content)
            
            # Position boxes relative to their content
            ideal_gas_box.move_to(ideal_gas_content)
            entropy_box.move_to(entropy_content)
            
            # Arrange the two assumption groups
            assumptions = VGroup(ideal_gas_group, entropy_group).arrange(RIGHT, buff=1).next_to(recap_eq, DOWN, buff=0.8)
            
            # Create arrow pointing to results
            arrow = Arrow(
                start=assumptions.get_bottom(),
                end=assumptions.get_bottom() + DOWN,
                color=YELLOW
            )
            
            # Create result box with flow variables
            result_box = VGroup(
                Text("Flow Relations:", font_size=28, color=YELLOW),
                MathTex("p = f(T)", "\\quad", "\\rho = f(T)", "\\quad", "p = f(\\rho)")
            ).arrange(DOWN, buff=0.3).next_to(arrow, DOWN)
            
            # Create nozzle visualization
            nozzle = self.create_nozzle().scale(0.4).to_edge(DOWN, buff=0.5)
            flow_arrows = self.create_flow_arrows().scale(0.4)
            flow_arrows.shift(nozzle.get_center() - flow_arrows.get_center())
            
            # Animation sequence synchronized with voiceover
            self.play(Write(recap_eq))  # First line of voiceover
            self.wait(0.5)
            
            self.play(  # Second line
                LaggedStartMap(Create, assumptions),
                run_time=2
            )
            
            self.play(  # Third line
                GrowArrow(arrow),
                FadeIn(result_box)
            )
            
            self.play(  # Fourth line
                Create(nozzle),
                Create(flow_arrows)
            )
            

        # Scene 1: What is an Isentropic Process?
        with self.voiceover(text="We define an isentropic process as one where the entropy remains constant. From thermodynamics, we know that this requires two things: the process must be adiabatic, so no heat is transferred, and reversible, meaning no friction or dissipation.") as tracker:
            # Create main equation
            # Now fade out everything
            self.play(
                FadeOut(recap_eq),
                FadeOut(assumptions),
                FadeOut(arrow),
                FadeOut(result_box),
                FadeOut(nozzle),
                FadeOut(flow_arrows)
            )
            isentropic_eq = MathTex(
                "dS = 0", "\\text{ (Isentropic)}"
            ).to_edge(UP)
            
            # Create recall equation
            recall_eq = MathTex(
                "\\text{Recall: }",
                "dS = \\frac{\\delta Q_{rev}}{T}",
                "\\implies",
                "\\delta Q_{rev} = 0"
            ).next_to(isentropic_eq, DOWN, buff=0.5)
            
            # Create interpretation labels
            interpretations = VGroup(
                MathTex("dS:", "\\text{ Differential change in entropy}"),
                MathTex("\\delta Q_{rev}:", "\\text{ Reversible heat transfer}"),
                MathTex("T:", "\\text{ Temperature}")
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.7)
            interpretations.next_to(recall_eq, DOWN, buff=0.2)
            
            # Create Venn diagram circles
            adiabatic = Circle(radius=1.5, color=BLUE)
            reversible = Circle(radius=1.5, color=RED)
            
            # Position circles for intersection
            adiabatic.shift(LEFT * 0.8)
            reversible.shift(RIGHT * 0.8)
            
            # Create labels for circles
            adiabatic_label = Text("Adiabatic", color=BLUE, font_size=30)
            reversible_label = Text("Reversible", color=RED, font_size=30)
            isentropic_label = Text("Isentropic", color=YELLOW, font_size=30)
            
            # Position labels
            adiabatic_label.next_to(adiabatic, DOWN)
            reversible_label.next_to(reversible, DOWN)
            adiabatic_label.shift(LEFT*0.2)
            reversible_label.shift(RIGHT*0.2)
            isentropic_label.move_to((adiabatic.get_center() + reversible.get_center()) / 2)            
            # Create intersection fill
            intersection = Intersection(adiabatic, reversible)
            intersection.set_fill(YELLOW, opacity=0.3)
            
            # Group Venn diagram elements
            venn_group = VGroup(
                adiabatic, reversible, intersection,
                adiabatic_label, reversible_label, isentropic_label
            )
            venn_group.scale(0.8)  # Make it slightly smaller
            venn_group.to_edge(DOWN, buff=1)
            
            # Show equations first
            self.play(Write(isentropic_eq))
            self.play(Write(recall_eq))
            
            # Show interpretations
            self.play(
                LaggedStartMap(FadeIn, interpretations, lag_ratio=0.3)
            )
            
            # Create and show Venn diagram
            self.play(
                Create(adiabatic),
                Create(reversible),
                Write(adiabatic_label),
                Write(reversible_label)
            )
            
            self.play(
                FadeIn(intersection),
                Write(isentropic_label)
            )
            
            # Add heat transfer arrows that will disappear
            heat_arrows = VGroup(*[
                Arrow(
                    start=adiabatic.point_at_angle(angle),
                    end=adiabatic.point_at_angle(angle) + RIGHT * 0.5,
                    color=ORANGE
                )
                for angle in np.linspace(0, 2*PI, 8)
            ])
            
        self.play(Create(heat_arrows))
        self.play(FadeOut(heat_arrows))  # Show heat transfer disappearing
            
            # Clean up for next scene
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        with self.voiceover(text="We now step into the idealized world of compressible flows, where gases behave as ideal and processes are isentropic. These assumptions give us clean and powerful relations between pressure, temperature, and density.") as tracker:
            # Create title card
            title_card = Text("Ideal Gas + Isentropic → Flow Relations", font_size=30, color=YELLOW)
            self.play(Write(title_card))
            self.wait(1)
            self.play(FadeOut(title_card))

        # Scene 2: Deriving the First Isentropic Relation
        # Initial setup - create all equations but don't display yet
        derivation = VGroup()

        with self.voiceover(text="We're about to derive the isentropic relation. Let's be careful and precise. We'll begin from the First Law of Thermodynamics, and apply it to an adiabatic and reversible process.") as tracker:
            first_law = MathTex("\\Delta U = Q - W").to_edge(UP)
            labels = VGroup(
                MathTex("U:", "\\text{ Internal energy}"),
                MathTex("Q:", "\\text{ Heat transfer}"),
                MathTex("W:", "\\text{ Work done by system}")
            ).arrange(DOWN, aligned_edge=LEFT).scale(0.6).next_to(first_law, DOWN)
            
            # Create P-V diagram
            axes = Axes(
                x_range=[0, 4, 1],
                y_range=[0, 4, 1],
                x_length=3,
                y_length=3,
                axis_config={"include_tip": True}
            ).scale(0.6).to_edge(RIGHT)
            
            # Add labels to axes
            x_label = MathTex("V").next_to(axes.x_axis.get_end(), RIGHT)
            y_label = MathTex("p").next_to(axes.y_axis.get_end(), UP)
            
            # Create hyperbolic curve for p-V relation
            curve = axes.plot(lambda x: 3/x, x_range=[0.75, 4], color=YELLOW)
            curve_label = Text("p∝1/V", font_size=20).next_to(curve, RIGHT)
            
            # Group P-V elements
            pv_group = VGroup(axes, x_label, y_label, curve, curve_label)
            pv_group.next_to(first_law, DOWN, buff=0.5)
            # Animation sequence
            self.play(Write(first_law))
            self.play(LaggedStartMap(FadeIn, labels))
            self.play(
                Create(axes),
                Write(x_label),
                Write(y_label)
            )
            self.play(
                Create(curve),
                Write(curve_label)
            )
            self.wait(1)
            self.play(
                FadeOut(first_law),
                FadeOut(labels),
                FadeOut(pv_group)
            )
        
        # Step 1: First Law for adiabatic process
        step1 = MathTex(
            "dQ = 0", "\\implies", "dU = -p\\,dV"
        ).scale(0.9)
        
        # Step 2: Ideal gas internal energy
        step2 = MathTex(
            "\\text{For ideal gas: }",
            "dU = c_v\\,dT",
            "\\implies",
            "c_v\\,dT = -p\\,dV"
        ).scale(0.9)
        
        # Step 3: Ideal gas law substitution
        step3 = MathTex(
            "\\text{Using ideal gas law: }",
            "pV = nRT",
            "\\implies",
            "p = \\frac{RT}{V}"
        ).scale(0.9)
        
        # Step 4: Substitution and rearrangement
        step4 = MathTex(
            "c_v\\,dT &= -\\frac{RT}{V}\\,dV \\\\",
            "\\frac{dT}{T} &= -\\frac{R}{c_v}\\cdot\\frac{dV}{V} \\\\",
            "\\frac{dT}{T} &= -(\\gamma-1)\\frac{dV}{V}"
        ).scale(0.9)
        
        # Final result
        final_result = MathTex(
            "pV^\\gamma = \\text{constant}",
            "\\quad \\text{or} \\quad",
            "\\frac{p}{\\rho^\\gamma} = \\text{constant}"
        ).scale(0.9)
        
        # Definition of gamma
        gamma_def = MathTex(
            "\\text{where }\\gamma = \\frac{c_p}{c_v}\\text{ (ratio of specific heats)}"
        ).scale(0.8)
        
        # Arrange equations vertically
        derivation.add(step1, step2, step3, step4)
        derivation.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        derivation.to_edge(UP, buff=0.5)
        
        # Position final result and gamma definition
        final_result.next_to(step4, RIGHT, buff=0.3)        
        # Create highlighting rectangles
        highlights = [
            SurroundingRectangle(eq, color=YELLOW, buff=0.1)
            for eq in [step1, step2, step3, step4, final_result]
        ]

        # Step 1: Introduce the Process
        with self.voiceover(text="We begin with a reversible adiabatic process, where no heat is exchanged. That gives us our key constraint.") as tracker:
            self.play(Write(step1))
            self.play(Create(highlights[0]))
            self.wait(0.5)
            self.play(FadeOut(highlights[0]))

        # Step 2: Apply First Law and Internal Energy
        with self.voiceover(text="For an ideal gas, we can express this in terms of internal energy and temperature.") as tracker:
            self.play(Write(step2))
            self.play(Create(highlights[1]))
            self.wait(0.5)
            self.play(FadeOut(highlights[1]))

        # Step 3: Ideal Gas Law
        with self.voiceover(text="To connect pressure and temperature, we'll use the ideal gas law.") as tracker:
            self.play(Write(step3))
            self.play(Create(highlights[2]))
            self.wait(0.5)
            self.play(FadeOut(highlights[2]))

        # Step 4: Derivation
        with self.voiceover(text="After substituting and rearranging, we get a relationship between temperature and volume changes.") as tracker:
            self.play(Write(step4))
            self.play(Create(highlights[3]))
            self.wait(0.5)
            self.play(FadeOut(highlights[3]))

        # Final Result
        with self.voiceover(text="This leads us to our first isentropic relation, a fundamental equation for compressible flows.") as tracker:
            self.play(
                Write(final_result),
                Create(highlights[4])
            )
            self.play( FadeOut(derivation))
            final_result.move_to(ORIGIN).shift(UP)
            gamma_def.next_to(final_result, DOWN, buff=0.3)
            self.play(
                FadeOut(highlights[4]),
                Write(gamma_def)
            )

        # Gamma Visualization
        with self.voiceover(text="Here, gamma represents the ratio of specific heats, a key property that determines how the gas stores energy.") as tracker:
            # Create visual aid for gamma
            gamma_circle = Circle(radius=0.5, color=BLUE)
            gamma_circle.next_to(gamma_def, DOWN, buff=0.5)
            gamma_label = MathTex("\\gamma").move_to(gamma_circle.get_center())
            
            cp_arrow = Arrow(gamma_circle.get_top(), gamma_circle.get_top() + UP, color=RED)
            cv_arrow = Arrow(gamma_circle.get_right(), gamma_circle.get_right() + RIGHT, color=GREEN)
            
            cp_label = MathTex("c_p").next_to(cp_arrow, UP)
            cv_label = MathTex("c_v").next_to(cv_arrow, RIGHT)
            
            gamma_group = VGroup(gamma_circle, gamma_label, cp_arrow, cv_arrow, cp_label, cv_label)
            
            self.play(Create(gamma_group))
            
            # Clean up for next scene
            self.wait(1)
            self.play(*[FadeOut(mob) for mob in self.mobjects])
    
        # Scene 3: Temperature-Pressure & Temperature-Density Relations
        # Create starting equations
        starting_point = MathTex(
            "p = \\rho RT", "\\quad \\text{and} \\quad",
            "\\frac{p}{\\rho^\\gamma} = \\text{const}"
        ).scale(0.9).to_edge(UP, buff=1)
        
        # Before starting the pairwise derivations
        with self.voiceover(text="In compressible flow, we often work with three key variables: pressure, temperature, and density. With two independent equations—like the ideal gas law and the isentropic relation—we can derive a relationship between any pair, and eliminate the third.") as tracker:
            triple_eqs = VGroup(
                MathTex("p = \\rho R T"),
                MathTex("\\frac{p}{\\rho^\\gamma} = \\text{const}")
            ).arrange(DOWN, buff=0.4).to_edge(LEFT)
            
            variables = VGroup(
                Text("Three variables:", font_size=24),
                MathTex("p,", "T,", "\\rho")
            ).arrange(RIGHT, buff=0.3).to_edge(RIGHT)
            
            self.play(Write(triple_eqs), Write(variables))
            self.wait(1)
            self.play(FadeOut(triple_eqs), FadeOut(variables))

        # First derivation (T-p relation)
        deriv1_title = Text("Temperature-Pressure Relation", color=BLUE).to_edge(LEFT, buff=0.3).scale(0.5).shift(UP*0.8)
        
        deriv1_steps = VGroup(
            MathTex("T_2 = \\frac{p_2}{\\rho_2 R}"),
            MathTex("T_1 = \\frac{p_1}{\\rho_1 R}"),
            MathTex("\\frac{T_2}{T_1} = \\frac{p_2}{p_1}\\cdot\\frac{\\rho_1}{\\rho_2}"),
            MathTex("\\text{Using } \\frac{\\rho_2}{\\rho_1} = \\left(\\frac{p_2}{p_1}\\right)^{1/\\gamma}"),
            MathTex("\\frac{T_2}{T_1} = \\left(\\frac{p_2}{p_1}\\right)^{\\frac{\\gamma-1}{\\gamma}}")
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(deriv1_title, DOWN, buff=0.5)
        
        # Second derivation (T-ρ relation)
        deriv2_title = Text("Temperature-Density Relation", color=RED).to_edge(RIGHT, buff=0.3).scale(0.5).shift(UP*0.8)
        
        deriv2_steps = VGroup(
            MathTex("\\text{From } p = \\rho RT:"),
            MathTex("\\frac{p_2}{p_1} = \\frac{\\rho_2 T_2}{\\rho_1 T_1}"),
            MathTex("\\text{Using } \\frac{p_2}{p_1} = \\left(\\frac{\\rho_2}{\\rho_1}\\right)^\\gamma"),
            MathTex("\\left(\\frac{\\rho_2}{\\rho_1}\\right)^\\gamma = \\frac{\\rho_2 T_2}{\\rho_1 T_1}"),
            MathTex("\\frac{T_2}{T_1} = \\left(\\frac{\\rho_2}{\\rho_1}\\right)^{\\gamma-1}")
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(deriv2_title, DOWN, buff=0.5)

        # Introduction
        with self.voiceover(text="Now that we have our isentropic relation, we can derive how temperature changes with pressure and density. We'll start with two fundamental equations: the ideal gas law and our isentropic relation.") as tracker:
            self.play(Write(starting_point))
            self.wait(0.5)

        # Temperature-Pressure Derivation
        with self.voiceover(text="Let's first find how temperature relates to pressure. We'll use the ideal gas law at two different states.") as tracker:
            self.play(Write(deriv1_title))
            self.play(Write(deriv1_steps[0]), Write(deriv1_steps[1]))
            box1 = SurroundingRectangle(VGroup(deriv1_steps[0], deriv1_steps[1]), color=YELLOW)
            self.play(Create(box1))

        with self.voiceover(text="Taking the ratio eliminates the gas constant R and gives us temperature in terms of pressure and density ratios.") as tracker:
            self.play(Write(deriv1_steps[2]))
            self.play(FadeOut(box1))
            box2 = SurroundingRectangle(deriv1_steps[2], color=YELLOW)
            self.play(Create(box2))

        with self.voiceover(text="From our isentropic relation, we know how density ratio relates to pressure ratio. We can substitute this to eliminate density.") as tracker:
            self.play(Write(deriv1_steps[3]))
            self.play(FadeOut(box2))
            box3 = SurroundingRectangle(deriv1_steps[3], color=YELLOW)
            self.play(Create(box3))

        with self.voiceover(text="After substituting and simplifying, we get our first key relation between temperature and pressure.") as tracker:
            self.play(Write(deriv1_steps[4]))
            self.play(FadeOut(box3))
            box4 = SurroundingRectangle(deriv1_steps[4], color=YELLOW)
            self.play(Create(box4))

        # Temperature-Density Derivation
        with self.voiceover(text="For the temperature-density relation, we'll again start with the ideal gas law, but this time focus on the density changes.") as tracker:
            self.play(Write(deriv2_title))
            self.play(Write(deriv2_steps[0]), Write(deriv2_steps[1]))
            box5 = SurroundingRectangle(VGroup(deriv2_steps[0], deriv2_steps[1]), color=YELLOW)
            self.play(Create(box5))

        with self.voiceover(text="We can use our isentropic relation again, this time keeping the density ratio and eliminating pressure.") as tracker:
            self.play(Write(deriv2_steps[2]))
            self.play(FadeOut(box5))
            box6 = SurroundingRectangle(deriv2_steps[2], color=YELLOW)
            self.play(Create(box6))

        with self.voiceover(text="After substituting and rearranging, we arrive at our second key relation between temperature and density.") as tracker:
            self.play(Write(deriv2_steps[3]), Write(deriv2_steps[4]))
            self.play(FadeOut(box6))
            box7 = SurroundingRectangle(deriv2_steps[4], color=YELLOW)
            self.play(Create(box7))

        # Final Relations and Application
        with self.voiceover(text="These two relations are powerful tools for analyzing compressible flows. They tell us exactly how temperature changes as pressure and density vary through a nozzle or any isentropic process.") as tracker:
            final_relations = VGroup(
                MathTex("\\frac{T_2}{T_1} = \\left(\\frac{p_2}{p_1}\\right)^{\\frac{\\gamma-1}{\\gamma}}"),
                MathTex("\\frac{T_2}{T_1} = \\left(\\frac{\\rho_2}{\\rho_1}\\right)^{\\gamma-1}")
            ).arrange(DOWN, buff=0.5)
            
            # First clear previous content
            self.play(*[FadeOut(mob) for mob in [deriv1_title, deriv1_steps, deriv2_title, deriv2_steps, box4, box7]])
            
            # Then show final relations
            final_relations.move_to(ORIGIN)
            self.play(Write(final_relations))
            
            # Create flow visualization
            nozzle = self.create_nozzle().scale(0.5).to_edge(DOWN)
            
            # Add labels at different positions
            positions = [(LEFT * 2, "1"), (ORIGIN, "t"), (RIGHT * 2, "2")]
            labels = VGroup()
            arrows = VGroup()
            
            for pos, label in positions:
                point = nozzle.get_center() + pos
                labels.add(MathTex(label).move_to(point + UP * 0.5))
                arrows.add(Arrow(point + UP * 0.2, point - UP * 0.2, color=BLUE))
            
            self.play(
                Create(nozzle),
                *[Write(label) for label in labels],
                *[GrowArrow(arrow) for arrow in arrows]
            )
            
            # Clean up for next scene
            self.wait(1)
            self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Scene 4: Why Isentropic Relations Matter in High-Speed Flow
        with self.voiceover(text="In many high-speed flow scenarios, like nozzles or expanding jets, heat exchange with the surroundings is minimal and friction is small. This makes the isentropic assumption remarkably accurate.") as tracker:
            # Create nozzle with flow visualization
            nozzle = self.create_nozzle().scale(0.8)
            
            # Create flow arrows
            flow_arrows = self.create_flow_arrows()
            flow_arrows.shift(nozzle.get_center() - flow_arrows.get_center())
            
            # Create labels for conditions
            conditions = VGroup(
                Text("• Minimal Heat Exchange", color=YELLOW, font_size=30),
                Text("• Low Friction", color=GREEN, font_size=30),
                Text("• No Shock Waves", color=BLUE, font_size=30)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            conditions.to_edge(RIGHT, buff=1)
            
            # Show nozzle and flow
            self.play(Create(nozzle))
            self.play(Create(flow_arrows))
            
            # Show conditions
            self.play(Write(conditions))
            
            # Clean up for next scene
            self.wait(1)
            self.play(*[FadeOut(mob) for mob in self.mobjects])

        with self.voiceover(text="Now that we've developed the mathematical tools for ideal compressible flows,") as tracker:
            self.wait(1)

    def section3(self):
        # Scene 1: From Isentropic Relations to Flow Analysis
        with self.voiceover(text="Now that we understand how pressure and temperature change in ideal flows, let's look at the bigger picture. These changes don't happen randomly - they're governed by some fundamental laws that apply to all fluid flows, whether they're isentropic or not.") as tracker:
            # Create boxes for isentropic and conservation laws
            isentropic_box = Rectangle(width=3, height=1.5, color=YELLOW)
            isentropic_title = Text("Isentropic Relations", font_size=24).move_to(isentropic_box)
            isentropic_group = VGroup(isentropic_box, isentropic_title).to_edge(UP)
            
            # Create conservation law boxes
            conservation_boxes = VGroup()
            titles = ["Mass", "Momentum", "Energy"]
            colors = [BLUE, RED, GREEN]
            
            for title, color in zip(titles, colors):
                box = Rectangle(width=2, height=1, color=color)
                text = Text(title, font_size=20).move_to(box)
                group = VGroup(box, text)
                conservation_boxes.add(group)
            
            conservation_boxes.arrange(RIGHT, buff=0.5).to_edge(DOWN)
            
            # Create connecting arrows
            arrows = VGroup()
            for box in conservation_boxes:
                arrow = Arrow(
                    isentropic_group.get_bottom(),
                    box.get_top(),
                    color=YELLOW
                )
                arrows.add(arrow)
            
            # Create control volume visualization
            cv_rect = Rectangle(width=3, height=2, color=WHITE)
            cv_label = Text("Control Volume", font_size=20).next_to(cv_rect, UP)
            
            # Create flow arrows
            in_arrow = Arrow(LEFT*2, LEFT*1, color=BLUE)
            out_arrow = Arrow(RIGHT*1, RIGHT*2, color=BLUE)
            
            # Position control volume group
            cv_group = VGroup(cv_rect, cv_label, in_arrow, out_arrow)
            cv_group.move_to(ORIGIN)
            
            # Animation sequence
            self.play(
                Create(isentropic_group)
            )
            
            self.play(
                LaggedStartMap(Create, conservation_boxes),
                LaggedStartMap(GrowArrow, arrows)
            )
            
            self.play(
                FadeOut(arrows),
                FadeOut(isentropic_group),
                Create(cv_group)
            )
        self.wait(1)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Scene 2: Conservation of Mass (Continuity Equation)
        with self.voiceover(text="Let's start with mass conservation. If more mass enters than leaves, something must be building up inside. But in steady flow, what goes in must come out. We can write this as a simple equation:") as tracker:
            # Create main continuity equation
            continuity_eq = MathTex(
                "\\rho_1 u_1 A_1 = \\rho_2 u_2 A_2",
                "\\quad \\text{or} \\quad",
                "\\frac{d}{dx}(\\rho u A) = 0"
            ).to_edge(UP)
            
            # Create variable explanations
            explanations = VGroup(
                MathTex("\\rho:", "\\text{ Density - how packed the fluid is}"),
                MathTex("u:", "\\text{ Flow velocity - how fast it's moving}"),
                MathTex("A:", "\\text{ Cross-sectional area - the space it has to flow through}"),
                MathTex("\\rho u A:", "\\text{ Mass flow rate - our key player}")
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8)
            explanations.next_to(continuity_eq, DOWN, buff=0.5)
            
            # Create nozzle visualization
            nozzle = self.create_nozzle().scale(0.7)
            nozzle.to_edge(DOWN, buff=1)
            
            # Add station labels
            station1 = VGroup(
                MathTex("\\rho_1, u_1, A_1"),
                Arrow(LEFT*0.5, ORIGIN, color=BLUE)
            ).arrange(DOWN).next_to(nozzle.get_left(), LEFT)
            
            station2 = VGroup(
                MathTex("\\rho_2, u_2, A_2"),
                Arrow(ORIGIN, RIGHT*0.5, color=BLUE)
            ).arrange(DOWN).next_to(nozzle.get_right(), RIGHT)
            
            # Create mass flow rate bar
            mass_flow_label = Text("Constant mass flow rate", font_size=20).next_to(nozzle, UP)

            # Animation sequence
            self.play(Write(continuity_eq))
            self.play(Write(explanations))
            self.play(Create(nozzle))
            self.play(
                Write(station1),
                Write(station2)
            )
            self.play(
                Write(mass_flow_label)
            )
            
            # Clean up for next scene
            self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Scene 3: Conservation of Momentum
        with self.voiceover(text="Next up is momentum conservation. Think of it like this: when you squeeze a garden hose, the water speeds up. That's because the pressure difference creates a force, and force changes momentum. Newton's laws still rule, even in fluids!") as tracker:
            # Create momentum equation
            momentum_eq = MathTex(
                "F = \\dot{m}\\cdot\\Delta u = (p_1A_1 - p_2A_2)"
            ).to_edge(UP)
            
            # Create control volume with forces
            cv_rect = Rectangle(width=3, height=2, color=WHITE)
            
            # Add pressure forces
            p1_arrow = Arrow(LEFT*2, LEFT*1, color=RED, max_tip_length_to_length_ratio=0.2)
            p2_arrow = Arrow(RIGHT*1, RIGHT*2, color=RED, max_tip_length_to_length_ratio=0.2)
            p1_label = MathTex("p_1A_1").next_to(p1_arrow, LEFT)
            p2_label = MathTex("p_2A_2").next_to(p2_arrow, RIGHT)
            
            # Add momentum arrows
            m1_arrow = Arrow(LEFT*2, LEFT*1, color=BLUE, max_tip_length_to_length_ratio=0.15)
            m2_arrow = Arrow(RIGHT*1, RIGHT*2, color=BLUE, max_tip_length_to_length_ratio=0.25)
            m1_label = MathTex("\\dot{m}u_1").next_to(m1_arrow, UP)
            m2_label = MathTex("\\dot{m}u_2").next_to(m2_arrow, UP)
            
            # Group all elements
            cv_group = VGroup(
                cv_rect, p1_arrow, p2_arrow, p1_label, p2_label,
                m1_arrow, m2_arrow, m1_label, m2_label
            )
            cv_group.move_to(ORIGIN)
            
            # Animation sequence
            self.play(Write(momentum_eq))
            self.play(Create(cv_rect))
            self.play(
                GrowArrow(p1_arrow), Write(p1_label),
                GrowArrow(p2_arrow), Write(p2_label)
            )
            self.play(
                GrowArrow(m1_arrow), Write(m1_label),
                GrowArrow(m2_arrow), Write(m2_label)
            )
            
            # Clean up for next scene
            self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Scene 4: Conservation of Energy
        with self.voiceover(text="Finally, let's talk about energy. In a fluid, energy can take different forms - it could be the energy of motion, or the internal energy of the hot fluid itself. When there's no heat exchange with the surroundings, the total energy stays constant - it just shifts between these different forms.") as tracker:
            # Create energy equation
            energy_eq = MathTex(
                "h + \\frac{u^2}{2} = \\text{constant}",
                "\\quad \\text{or} \\quad",
                "c_pT + \\frac{u^2}{2} = \\text{constant}"
            ).to_edge(UP)
            
            # Create explanations
            energy_terms = VGroup(
                MathTex("h = c_pT:", "\\text{ Enthalpy}"),
                MathTex("\\frac{u^2}{2}:", "\\text{ Kinetic energy}"),
                Text("No heat added (adiabatic)", font_size=24)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(energy_eq, DOWN, buff=1.5)  # Increased buffer to move down
            
            # Create fluid parcel visualization
            parcel = Square(side_length=0.5, color=BLUE, fill_opacity=0.3)
            velocity_arrow = Arrow(ORIGIN, RIGHT*1, color=RED)
            parcel_group = VGroup(parcel, velocity_arrow)
            parcel_group.move_to(LEFT*3)
            
            # Create stagnation point visualization
            stagnation = Dot(color=YELLOW)
            stagnation_label = MathTex("T_0 = \\text{Total (stagnation) temperature}").next_to(stagnation, RIGHT)
            stagnation_group = VGroup(stagnation, stagnation_label).move_to(RIGHT*2)
            
            # Position stagnation group below energy terms
            stagnation_group.next_to(energy_terms, DOWN, buff=1)
            
            # Animation sequence
            self.play(Write(energy_eq))
            self.play(Write(energy_terms))
            self.play(Create(parcel_group))
            self.play(
                parcel_group.animate.move_to(stagnation.get_center()),
                FadeIn(stagnation),
                Write(stagnation_label)
            )
            
            # Clean up for next scene
            self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Scene 5: Summary of Governing Equations
        with self.voiceover(text="These three laws - mass, momentum, and energy conservation - work together to tell us exactly how a flow will behave. Think of them as the rules of the game that all flows must follow, whether we're designing a jet engine or understanding wind patterns.") as tracker:
            # Create table
            table = VGroup()
            
            # Headers
            headers = VGroup(
                Text("Law", font_size=24),
                Text("Equation", font_size=24),
                Text("Assumptions", font_size=24)
            ).arrange(RIGHT, buff=1).to_edge(UP)
            
            # Rows
            rows = VGroup(
                VGroup(
                    Text("Mass", font_size=20, color=BLUE),
                    MathTex("\\frac{d}{dx}(\\rho u A) = 0"),
                    Text("Steady, 1D", font_size=20)
                ).arrange(RIGHT,buff=1),
                VGroup(
                    Text("Momentum", font_size=20, color=RED),
                    MathTex("\\rho u\\frac{du}{dx} = -\\frac{dp}{dx}"),
                    Text("Neglect friction", font_size=20)
                ).arrange(RIGHT,buff=1),
                VGroup(
                    Text("Energy", font_size=20, color=GREEN),
                    MathTex("h + \\frac{u^2}{2} = \\text{constant}"),
                    Text("Adiabatic", font_size=20)
                ).arrange(RIGHT,buff=1)
            )
            
            # Arrange each row
            for row in rows:
                row.arrange(RIGHT, buff=1, aligned_edge=LEFT)
            
            # Arrange all rows vertically
            rows.arrange(DOWN, buff=0.5)
            
            # Add horizontal lines
            lines = VGroup()
            for i in range(len(rows) + 1):
                line = Line(
                    LEFT * 4, RIGHT * 4,
                    stroke_width=1 if i > 0 else 2
                )
                if i == 0:
                    line.next_to(headers, DOWN)
                else:
                    line.next_to(rows[i-1], DOWN, buff=0.25)
                lines.add(line)
            
            # Group everything
            table = VGroup(headers, rows, lines)
            table.move_to(ORIGIN)
            
            # Animation sequence
            self.play(Write(headers))
            self.play(Create(lines[0]))
            
            for i, row in enumerate(rows):
                self.play(
                    Write(row),
                    Create(lines[i+1])
                )
            
            # Final pause
            self.wait(2)

if __name__ == "__main__":
    from manim import *
    config.disable_caching = False
    config.quality = "high_quality"
    scene = Isentropic()
    scene.render()