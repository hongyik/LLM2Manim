from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np
import random

class CarnotProcessScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Configure voiceover service with detailed voice instructions.
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        # Run each section
        self.section1() #introduction and recap
        self.clear()
        self.section2() #definition of reversible and irreversible processes and examples
        self.clear()
        self.section3() 
        self.clear()
        self.section4() 
        self.clear()
        self.section5()  # Heat quantities relationship
        self.clear()
        self.section6()  # Entropy section
        self.clear()
        self.section7()  # Second Law of Thermodynamics
    def section1(self):
        # Create text objects for each part of the transition
        with self.voiceover(text="Last time, we explored the First Law of Thermodynamics — how energy is conserved in a system, neither created nor destroyed, only transferred as heat and work.") as tracker:
            # Create a more dynamic title with gradient color
            first_law = Text("First Law of Thermodynamics", font_size=40)
            first_law.set_color_by_gradient(BLUE, GREEN)
            
            # Create energy flow diagram
            energy_concepts = VGroup(
                Text("Energy Conservation", font_size=30, color=BLUE),
                Text("Heat Transfer", font_size=30, color=RED),
                Text("Work", font_size=30, color=GREEN),
                Text("Internal Energy Changes", font_size=30, color=YELLOW)
            ).arrange(DOWN, buff=0.5)
            
            # Add arrows between concepts to show flow
            arrows = VGroup(*[
                Arrow(
                    start=energy_concepts[i].get_right(),
                    end=energy_concepts[i+1].get_right(),
                    color=GRAY,
                    max_tip_length_to_length_ratio=0.15
                ) for i in range(len(energy_concepts)-1)
            ])
            
            # Create a circular arrow to represent conservation
            circle_arrow = Circle(radius=0.3, color=BLUE).next_to(energy_concepts, LEFT)
            circle_arrow.add_tip(tip_length=0.2)
            
            self.play(Write(first_law), run_time=1)
            self.play(first_law.animate.to_edge(UP))
            self.play(
                Write(energy_concepts),
                Create(arrows),
                Create(circle_arrow),
                run_time=tracker.duration-3
            )
            
        with self.voiceover(text="But you might wonder: if energy is always conserved, why can't our engines convert 100% of heat into mechanical work? This leads us to a deeper question about the quality of energy.") as tracker:
            # Create energy transfer visualization
            system_a = Circle(radius=0.8, color=RED).shift(LEFT*3)
            system_b = Circle(radius=0.8, color=BLUE).shift(RIGHT*3)
            energy_dot = Dot(color=YELLOW).move_to(system_a)
            
            transfer_arrow = Arrow(system_a.get_right(), system_b.get_left(), color=YELLOW)
            
            new_question = Text("If energy is conserved...", font_size=35, color=BLUE_B).to_edge(UP)
            efficiency_question = Text("Why not 100% efficiency?", font_size=30, color=RED_B).next_to(new_question, DOWN)
            
            self.play(
                FadeOut(first_law),
                FadeOut(energy_concepts),
                FadeOut(arrows),
                FadeOut(circle_arrow),
                run_time=tracker.duration/3
            )
            
            self.play(
                Create(system_a),
                Create(system_b),
                FadeIn(energy_dot),
                Write(new_question),
                Write(efficiency_question),
                run_time=tracker.duration/3
            )
            
            # Animate energy transfer
            self.play(
                Create(transfer_arrow),
                energy_dot.animate.move_to(system_b),
                run_time=tracker.duration/3
            )

        with self.voiceover(text="Although energy is never lost, it can become 'unavailable' or 'degrade' into forms we can't recover. This brings us to the crucial concept of reversibility.") as tracker:
            # Create degradation visualization
            degraded_dot = energy_dot.copy().set_opacity(0.5)
            degradation_text = Text("Energy Degradation", font_size=30, color=YELLOW_A).next_to(system_b, DOWN)
            
            reverse_arrow = Arrow(system_b.get_left(), system_a.get_right(), color=YELLOW_A, stroke_opacity=0.5)
            question_mark = Text("?", font_size=60, color=YELLOW).next_to(reverse_arrow, UP)
            
            reversibility_text = Text("Reversibility?", font_size=30, color=GREEN).next_to(degradation_text, DOWN)
            
            self.play(
                Transform(energy_dot, degraded_dot),
                Write(degradation_text),
                run_time=tracker.duration/2
            )
            
            self.play(
                Create(reverse_arrow),
                Write(question_mark),
                Write(reversibility_text),
                run_time=tracker.duration/2
            )

        with self.voiceover(text="Today, we'll explore this fundamental distinction between reversible and irreversible processes, and discover the Carnot cycle — the most ideal reversible process that sets the theoretical limit for all heat engines.") as tracker:
            # Create dynamic final presentation
            final_text = VGroup(
                Text("Reversible vs Irreversible", font_size=40, color=BLUE),
                Text("Processes", font_size=40, color=BLUE),
                Text("The Carnot Cycle", font_size=45, color=YELLOW),
                Text("(The Ideal Process)", font_size=35, color=YELLOW_A)
            ).arrange(DOWN, buff=0.5)
            
            self.play(
                FadeOut(system_a),
                FadeOut(system_b),
                FadeOut(energy_dot),
                FadeOut(transfer_arrow),
                FadeOut(reverse_arrow),
                FadeOut(question_mark),
                FadeOut(new_question),
                FadeOut(efficiency_question),
                FadeOut(degradation_text),
                FadeOut(reversibility_text),
                run_time=tracker.duration/3
            )
            
            self.play(
                Write(final_text),
                run_time=tracker.duration*2/3
            )
            
            self.wait(1)
            self.play(FadeOut(final_text))
     # Setup: Create piston-cylinder system
    def create_piston_system(self):
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

    def create_dynamic_particles(self, num_particles=20):
        particles = VGroup()
        particle_velocities = []
        
        for _ in range(num_particles):
            particle = Dot(radius=0.05)
            particle.set_fill(BLUE, opacity=0.8)
            # Random initial position within the cylinder, below piston
            x = np.random.uniform(-0.8, 0.8)
            y = np.random.uniform(-1.8, 0.8)  # Leave space for compression
            particle.move_to([x, y, 0])
            particles.add(particle)
            
            # Initialize with random velocity (higher speed)
            speed = 0.3  # Increased from 0.15
            theta = np.random.uniform(0, 2 * np.pi)
            vx = speed * np.cos(theta)
            vy = speed * np.sin(theta)
            particle_velocities.append(np.array([vx, vy]))
        
        return particles, particle_velocities

    def update_particles(self, particles, velocities, dt, bottom=-2, top=1):
        for i, particle in enumerate(particles):
            pos = particle.get_center()
            vel = velocities[i]
            
            # Update position
            new_x = pos[0] + vel[0] * dt
            new_y = pos[1] + vel[1] * dt
            
            # Boundary collisions with more elastic response
            if new_x < -0.8 or new_x > 0.8:
                velocities[i][0] *= -1.1  # Slightly increase speed on collision
                new_x = pos[0]
            
            if new_y < bottom or new_y > top:
                velocities[i][1] *= -1.1  # Slightly increase speed on collision
                new_y = pos[1]
                
                # Ensure particles stay below piston
                if new_y > top:
                    new_y = top - 0.05
            
            particle.move_to([new_x, new_y, 0])
    def section2(self):
        with self.voiceover(text="Let's understand what makes a process reversible in thermodynamics.") as tracker:
            # Title
            title = Text("Reversible Process", font_size=40, color=BLUE)
            title.to_edge(UP)
            
            self.play(Write(title), run_time=tracker.duration)

        with self.voiceover(text="Let's visualize this with a piston-cylinder system. Notice how the gas particles move randomly but maintain an overall equilibrium state.") as tracker:
            # Create initial system
            piston_system = self.create_piston_system()
            particles, velocities = self.create_dynamic_particles()
            
            # Create temperature visualization rectangle (initially invisible)
            # Use exact cylinder dimensions
            temp_rect = Rectangle(
                width=2,  # Exact width between cylinder walls
                height=3,  # Initial height from bottom to piston
                fill_opacity=0,
                fill_color=BLUE,
                stroke_opacity=0
            )
            # Position at center of cylinder
            temp_rect.move_to([0, -0.5, 0])
            
            # Add labels
            labels = VGroup(
                Text("T", font_size=25).next_to(piston_system, RIGHT),
                Text("P", font_size=25).next_to(piston_system, LEFT),
                Text("V", font_size=25).next_to(piston_system, RIGHT, buff=1)
            )
            
            # Show equilibrium state label
            eq_state = Text("Equilibrium State", font_size=25, color=YELLOW)
            eq_state.next_to(piston_system, UP, buff=1)
            
            self.play(
                Create(piston_system),
                FadeIn(temp_rect),
                run_time=tracker.duration/3
            )
            self.play(
                LaggedStart(*[FadeIn(p) for p in particles]),
                Write(labels),
                Write(eq_state),
                run_time=tracker.duration/3
            )

            # Animate particles for a short while
            for _ in range(30):  # 30 frames of particle motion
                self.update_particles(particles, velocities, 0.1)
                self.wait(0.1)

        with self.voiceover(text="In a reversible process, we change the system so slowly — like adding a tiny weight — that the system has time to adjust and remain in equilibrium at all times.") as tracker:
            # Transition from particles to filled rectangle
            self.play(
                FadeOut(particles),
                temp_rect.animate.set_fill(opacity=1.0),  # Make rectangle fully opaque
                run_time=1
            )
            
            # Create small weights to add
            small_weights = VGroup(*[
                Rectangle(height=0.05, width=1.5, color=GRAY, fill_opacity=0.8)
                for _ in range(5)
            ])

            # Add weights and compress slowly
            current_top = 1
            for i in range(5):
                new_weight = small_weights[i].copy()
                new_weight.next_to(piston_system[2], UP, buff=0)
                
                # Update equilibrium state label
                new_eq_state = Text(f"Equilibrium State {i+2}", font_size=25, color=YELLOW)
                new_eq_state.move_to(eq_state.get_center())
                
                # Calculate new position
                new_top = current_top - 0.15
                
                # Gradually change color to represent temperature increase
                temp_color = interpolate_color(BLUE, RED, (i + 1) / 5)
                
                # Calculate new rectangle height
                new_height = temp_rect.height - 0.15
                
                # Create a new rectangle with updated height but same width
                new_rect = Rectangle(
                    width=2,  # Keep exact cylinder width
                    height=new_height,
                    fill_opacity=1.0,
                    fill_color=temp_color,
                    stroke_opacity=0
                ).move_to([0, piston_system[0].get_bottom()[1] + new_height/2, 0])
                
                self.play(
                    FadeIn(new_weight),
                    piston_system[1].animate.shift(DOWN * 0.15),  # Move piston down
                    piston_system[2].animate.shift(DOWN * 0.15),  # Move existing weights down
                    Transform(temp_rect, new_rect),  # Transform to new rectangle
                    Transform(eq_state, new_eq_state),
                    run_time=tracker.duration/5
                )
                
                # Add weight to system and update current top position
                piston_system[2].add(new_weight)
                current_top = new_top

        with self.voiceover(text="Each state in this process is an equilibrium state, with the internal pressure of the gas practically equal to the external pressure from the weights.") as tracker:
            # Add pressure indicators
            p_internal = Arrow([-1.5, 0, 0], [-1, 0, 0], color=RED, max_tip_length_to_length_ratio=0.15)
            p_external = Arrow([-1, 0, 0], [-1.5, 0, 0], color=BLUE, max_tip_length_to_length_ratio=0.15)
            
            pressure_text = VGroup(
                Text("Internal Pressure ≈ External Pressure", font_size=23, color=GREEN),
                Text("(Infinitesimal difference)", font_size=18, color=YELLOW)
            ).arrange(DOWN, buff=0.3)
            pressure_text.next_to(piston_system, DOWN, buff=0.8)
            
            self.play(
                Create(p_internal),
                Create(p_external),
                Write(pressure_text),
                run_time=tracker.duration
            )

        with self.voiceover(text="Let's review why this compression process is reversible. Notice how each state is an equilibrium state, with infinitesimal changes between them. The system moves so slowly through these states that at any moment, we could reverse the process by removing weights, and the system would return through exactly the same states. This is the essence of a reversible process - the ability to retrace our path through a continuous sequence of equilibrium states.") as tracker:
            # Clear everything except title by fading out all mobjects
            self.play(
                *[FadeOut(mob) for mob in self.mobjects if not isinstance(mob, Text) or mob != title],
                run_time=tracker.duration/4
            )

            # Create small cylinders showing different states
            states = VGroup()
            arrows = VGroup()
            state_labels = VGroup()
            
            # Scale factor for mini states
            scale_factor = 0.4
            
            # Create 6 states (initial + 5 compressed states)
            for i in range(6):
                # Create mini cylinder (same proportions as original)
                mini_cylinder = VGroup(
                    Line(start=[-1, -2, 0], end=[-1, 1, 0], color=WHITE),
                    Line(start=[1, -2, 0], end=[1, 1, 0], color=WHITE),
                    Line(start=[-1, -2, 0], end=[1, -2, 0], color=WHITE)
                )
                
                # Create mini piston
                mini_piston = Line(start=[-1.2, 1 - i * 0.15, 0], end=[1.2, 1 - i * 0.15, 0], color=WHITE)
                
                # Create mini weights
                mini_weights = VGroup()
                for w in range(i + 1):  # Add weights progressively
                    weight = Rectangle(
                        height=0.1,
                        width=1.5,
                        color=GRAY,
                        fill_opacity=0.8
                    ).move_to([0, 1 - i * 0.15 + 0.05 + w * 0.1, 0])  # Stack weights
                    mini_weights.add(weight)
                
                # Create filled rectangle for temperature
                current_height = 3 - i * 0.15  # Height decreases with each state
                temp_color = interpolate_color(BLUE, RED, i/5)
                temp_rect = Rectangle(
                    width=2,
                    height=current_height,
                    fill_opacity=1.0,
                    fill_color=temp_color,
                    stroke_opacity=0
                ).move_to([0, -2 + current_height/2, 0])  # Align with bottom
                
                # Group all elements
                state = VGroup(temp_rect, mini_cylinder, mini_piston, mini_weights)
                state.scale(scale_factor)  # Scale down the entire state
                
                # Position state
                state.shift(RIGHT * (i * 2.5 - 6) + UP * 1)  # Spread horizontally
                states.add(state)
                
                # Add state label
                label = Text(f"State {i+1}", font_size=20)
                label.next_to(state, DOWN, buff=0.2)
                state_labels.add(label)
                
                # Add arrow between states (except for the last state)
                if i < 5:
                    # Forward arrow (yellow)
                    forward_arrow = Arrow(
                        state.get_right() + RIGHT * 0.2,
                        state.get_right() + RIGHT * 1.3,
                        color=YELLOW,
                        max_tip_length_to_length_ratio=0.15,
                        buff=0.1
                    )
                    # Backward arrow (slightly offset and lighter color)
                    backward_arrow = Arrow(
                        state.get_right() + RIGHT * 1.3,
                        state.get_right() + RIGHT * 0.2,
                        color=YELLOW_A,
                        max_tip_length_to_length_ratio=0.15,
                        buff=0.1
                    ).shift(UP * 0.1)
                    arrows.add(VGroup(forward_arrow, backward_arrow))

            # Add explanation text
            explanation = VGroup(
                Text("Reversible Process:", font_size=25, color=BLUE),
                Text("• Continuous sequence of equilibrium states", font_size=20),
                Text("• Infinitesimal changes between states", font_size=20),
                Text("• Process can be reversed at any point", font_size=20)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)

            # Animate everything
            self.play(
                Write(explanation[0]),
                run_time=tracker.duration/4
            )
            
            self.play(
                LaggedStart(*[Create(state) for state in states]),
                LaggedStart(*[Write(label) for label in state_labels]),
                run_time=tracker.duration/4
            )
            
            self.play(
                LaggedStart(*[Create(arrow) for arrow in arrows]),
                Write(explanation[1:]),
                run_time=tracker.duration/4
            )

        # Pause briefly before showing irreversible processes
        self.wait(1)

        with self.voiceover(text="In contrast, most real-world processes are irreversible. Although energy is conserved, these processes cannot be perfectly reversed.") as tracker:
            # Clear previous animations
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=tracker.duration)

            # Create title for irreversible processes
            title = Text("Irreversible Processes", font_size=40, color=RED)
            title.to_edge(UP)
            
            # Create three example titles
            friction_title = Text("Friction", font_size=30, color=BLUE)
            turbulence_title = Text("Turbulent Flow", font_size=30, color=BLUE)
            heat_title = Text("Heat Conduction", font_size=30, color=BLUE)
            
            titles = VGroup(friction_title, turbulence_title, heat_title)
            titles.arrange(RIGHT, buff=2)
            titles.next_to(title, DOWN)

            # Add note about energy representation
            energy_note = Text(
                "(Red dots represent energy, not actual particles)",
                font_size=20,
                color=YELLOW_A
            ).next_to(title, DOWN, buff=0.2)

            self.play(
                Write(title),
                Write(titles),
                Write(energy_note),
                run_time=tracker.duration
            )

            # Move titles below the note
            titles.next_to(energy_note, DOWN)

            # Setup all three demonstrations but don't animate yet
            # 1. Friction setup
            block = Square(side_length=0.8, color=BLUE, fill_opacity=0.8)
            ground = Line(LEFT * 1.5, RIGHT * 1.5, color=WHITE)
            friction_group = VGroup(block, ground)
            friction_group.next_to(friction_title, DOWN, buff=1)
            block.move_to(friction_group.get_left() + RIGHT * 0.5 + UP * 0.5)
            
            friction_arrows = VGroup(*[
                Arrow(
                    start=block.get_bottom() + RIGHT * 0.1 * i - RIGHT * 0.2,
                    end=block.get_bottom() + RIGHT * 0.1 * i - RIGHT * 0.2 + LEFT * 0.1,
                    color=RED,
                    max_tip_length_to_length_ratio=0.2,
                    buff=0
                ) for i in range(5)
            ])
            
            heat_particles_friction = VGroup(*[
                Dot(radius=0.03, color=RED_A) 
                for _ in range(8)
            ])
            for dot in heat_particles_friction:
                dot.move_to(block.get_bottom())

            # 2. Turbulent flow setup
            flow_path = Line(LEFT * 1.5, RIGHT * 1.5, color=BLUE)
            streamlines = VGroup(*[
                Line(LEFT * 1.5, RIGHT * 1.5, color=BLUE_A, stroke_opacity=0.6)
                .shift(UP * (i * 0.15))
                for i in range(4)
            ])
            
            flow_group = VGroup(flow_path, streamlines)
            flow_group.next_to(turbulence_title, DOWN, buff=1)
            
            eddies = VGroup(*[
                Circle(radius=0.2, color=RED_A, stroke_opacity=0.8)
                .shift(RIGHT * (i - 1) * 0.8)
                for i in range(3)
            ])
            eddies.move_to(flow_group)
            
            eddy_arrows = VGroup(*[
                CurvedArrow(
                    eddy.point_at_angle(0),
                    eddy.point_at_angle(PI/2),
                    color=RED_A,
                    angle=PI/2
                )
                for eddy in eddies
            ])

            # 3. Heat conduction setup
            hot_object = Square(side_length=0.8, color=RED, fill_opacity=0.8)
            cold_object = Square(side_length=0.8, color=BLUE, fill_opacity=0.8)
            heat_group = VGroup(hot_object, cold_object)
            heat_group.arrange(RIGHT, buff=0.5)
            heat_group.next_to(heat_title, DOWN, buff=1)
            
            heat_particles = VGroup(*[
                Dot(radius=0.03, color=RED_A)
                for _ in range(12)
            ])
            for dot in heat_particles:
                dot.move_to(
                    hot_object.get_center() +
                    RIGHT * np.random.uniform(-0.3, 0.3) +
                    UP * np.random.uniform(-0.3, 0.3)
                )

            # Add specific energy labels for each demonstration
            friction_energy = Text("(Kinetic → Thermal)", font_size=18, color=RED_A)
            friction_energy.next_to(friction_group, DOWN, buff=0.2)

            flow_energy = Text("(Ordered → Chaotic)", font_size=18, color=RED_A)
            flow_energy.next_to(flow_group, DOWN, buff=0.2)

            heat_energy = Text("(Temperature gradient → Uniform)", font_size=18, color=RED_A)
            heat_energy.next_to(heat_group, DOWN, buff=0.2)

            # Show initial state of all three with energy labels
            self.play(
                Create(friction_group),
                Create(flow_group),
                Create(heat_group),
                Write(friction_energy),
                Write(flow_energy),
                Write(heat_energy),
                run_time=1
            )

        with self.voiceover(text="In friction, when a block slides and stops, kinetic energy converts to thermal energy. This heat energy can never spontaneously convert back to the block's original motion.") as tracker:
            # Animate friction example
            self.play(
                block.animate.shift(RIGHT * 1),
                rate_func=lambda t: 1 - (1-t)**2,
                run_time=tracker.duration/2
            )
            
            self.play(
                Create(friction_arrows),
                *[
                    dot.animate.shift(
                        UP * np.random.uniform(0.3, 0.8) +
                        RIGHT * np.random.uniform(-0.5, 0.5)
                    ).set_opacity(0.3)
                    for dot in heat_particles_friction
                ],
                run_time=tracker.duration/2
            )

        with self.voiceover(text="In turbulent flow, ordered fluid motion breaks into chaotic eddies, dissipating energy that cannot be recovered to restore the original flow pattern.") as tracker:
            # Animate turbulent flow
            self.play(
                *[
                    line.animate.become(
                        CubicBezier(
                            line.get_start(),
                            line.get_start() + RIGHT * 1 + UP * np.random.uniform(-0.1, 0.1),
                            line.get_end() + LEFT * 1 + UP * np.random.uniform(-0.1, 0.1),
                            line.get_end()
                        )
                    )
                    for line in streamlines
                ],
                Create(eddies),
                Create(eddy_arrows),
                run_time=tracker.duration
            )

        with self.voiceover(text="And in heat conduction, heat flows spontaneously from hot to cold until temperatures equalize. This process never reverses on its own - heat won't spontaneously flow back to create the original temperature difference.") as tracker:
            # Animate heat conduction
            self.play(
                *[
                    dot.animate.move_to(
                        cold_object.get_center() +
                        RIGHT * np.random.uniform(-0.3, 0.3) +
                        UP * np.random.uniform(-0.3, 0.3)
                    )
                    for dot in heat_particles
                ],
                hot_object.animate.set_color(PURPLE),
                cold_object.animate.set_color(PURPLE),
                run_time=tracker.duration
            )

        with self.voiceover(text="These irreversible processes are fundamental to understanding why real heat engines can never achieve 100% efficiency.") as tracker:
            # Add final explanation text
            explanation = Text(
                "Energy is conserved but cannot be fully recovered",
                font_size=25,
                color=YELLOW
            ).next_to(VGroup(friction_group, heat_group), DOWN, buff=0.8)
            
            self.play(
                Write(explanation),
                run_time=tracker.duration
            )

        # Pause briefly before moving to next section
        self.wait(1)
    def section3(self):
        with self.voiceover(text="Now that we've understood the difference between reversible and irreversible processes, a natural question arises: What is the maximum efficiency a heat engine can achieve, if it operates entirely through reversible processes?") as tracker:
            # Clear previous scene
            self.clear()
            
            # Create title
            title = Text("The Quest for Maximum Efficiency", font_size=40, color=BLUE)
            title.to_edge(UP)

            # Create efficiency question
            question = MathTex(
                r"\eta_{max} = \, ?",
                font_size=45,
                color=YELLOW
            )
            
            # Create real engine visualization
            engine_box = Rectangle(height=2, width=3, color=WHITE)
            hot_reservoir = Rectangle(height=0.8, width=4, color=RED, fill_opacity=0.3)
            cold_reservoir = Rectangle(height=0.8, width=4, color=BLUE, fill_opacity=0.3)
            
            # Position reservoirs and engine
            hot_reservoir.next_to(engine_box, UP, buff=0.5)
            cold_reservoir.next_to(engine_box, DOWN, buff=0.5)

            # Create labels
            hot_label = MathTex("T_H", color=RED).next_to(hot_reservoir, RIGHT)
            cold_label = MathTex("T_C", color=BLUE).next_to(cold_reservoir, RIGHT)
            engine_label = Text("Heat Engine", font_size=25).move_to(engine_box)
            
            # Create energy flow arrows
            q_in = Arrow(
                hot_reservoir.get_bottom(),
                engine_box.get_top(),
                color=RED,
                max_tip_length_to_length_ratio=0.15
            )
            q_out = Arrow(
                engine_box.get_bottom(),
                cold_reservoir.get_top(),
                color=BLUE,
                max_tip_length_to_length_ratio=0.15
            )
            work = Arrow(
                engine_box.get_right(),
                engine_box.get_right() + RIGHT * 1.5,
                color=GREEN,
                max_tip_length_to_length_ratio=0.15
            )
            
            # Create energy labels
            q_in_label = MathTex("Q_{in}", color=RED).next_to(q_in, LEFT)
            q_out_label = MathTex("Q_{out}", color=BLUE).next_to(q_out, LEFT)
            work_label = MathTex("W", color=GREEN).next_to(work, UP)
            
            # Group all elements
            engine_system = VGroup(
                engine_box, hot_reservoir, cold_reservoir,
                hot_label, cold_label, engine_label,
                q_in, q_out, work,
                q_in_label, q_out_label, work_label
            )
            
            # Animate
            self.play(
                Write(title),
                run_time=tracker.duration/3
            )

            self.play(
                Write(question),
                run_time=tracker.duration/3
            )
            
            self.play(
                question.animate.to_edge(LEFT),
                Create(engine_system),
                run_time=tracker.duration/3
            )

        with self.voiceover(text="To answer that, we turn to an idealized thermodynamic cycle proposed by the French engineer Sadi Carnot — the Carnot cycle.") as tracker:
            # Clear previous content
            self.clear()
            
            # Create Carnot's information
            carnot_name = Text("Sadi Carnot", font_size=30, color=GOLD_B)
            carnot_years = Text("(1796-1832)", font_size=25, color=GRAY)
            carnot_title = VGroup(
                Text("French Engineer", font_size=25, color=BLUE),
                Text("Father of Thermodynamics", font_size=22, color=BLUE_B)
            ).arrange(DOWN, buff=0.1)
            
            contribution = VGroup(
                Text("Key Insight:", font_size=25, color=YELLOW),
                Text("Heat engines are limited", font_size=20),
                Text("by the temperatures of", font_size=20),
                Text("their heat reservoirs", font_size=20)
            ).arrange(DOWN, buff=0.1)
            
            # Group and position information
            carnot_info = VGroup(
                carnot_name,
                carnot_years,
                carnot_title,
                Line(LEFT, RIGHT, color=GOLD_B).scale(2),
                contribution
            ).arrange(DOWN, buff=0.2)
            
            carnot_info.to_edge(LEFT, buff=1)
            
            # Animate
            self.play(
                Write(carnot_info),
                run_time=tracker.duration
            )

        with self.voiceover(text="It is composed entirely of reversible processes and sets the theoretical upper bound on efficiency for any heat engine. Let's dive into how it works.") as tracker:
            # Create Carnot cycle key points
            key_points = VGroup(
                Text("• Composed of reversible processes", font_size=25),
                Text("• Sets theoretical maximum efficiency", font_size=25),
                Text("• Ideal benchmark for all heat engines", font_size=25)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            
            key_points.next_to(carnot_info, DOWN, buff=0.5)
            
            self.play(
                Write(key_points),
                run_time=tracker.duration
            )

            # Prepare for transition to next section
            self.play(
                *[FadeOut(mob) for mob in self.mobjects],
                run_time=1
            )
    def section4(self):
        # Define temperature colors
        HIGH_TEMP_COLOR = RED
        LOW_TEMP_COLOR = BLUE
        
        # Step 1: Setup coordinate axes
        with self.voiceover(text="Let's examine how the Carnot cycle works. It consists of four ideal, reversible processes forming a closed loop on a P-V diagram.") as tracker:
            # Create axes
            axes = Axes(
                x_range=[0, 5, 1],  # Adjusted range to fit doubled x values
                y_range=[0, 1.2, 0.2],   # y range stays the same
                x_length=5,
                y_length=5,
                axis_config={"include_tip": True},
            ).to_edge(LEFT, buff=1)

            # Add labels
            x_label = MathTex("V").next_to(axes.x_axis.get_end(), RIGHT)
            y_label = MathTex("p").next_to(axes.y_axis.get_end(), UP)
            
            labels = VGroup(x_label, y_label)
            
            # Animate creation
            self.play(
                Create(axes),
                run_time=tracker.duration/2
            )
            self.play(
                Write(labels),
                run_time=tracker.duration/2
            )

        # Step 2: Point A - Initial State
        with self.voiceover(text="The first step of the cycle is the reversible isothermal expansion. Let's start at point A.") as tracker:
            # Create point A (Point 1)
            point_a = Dot(axes.c2p(2.0, 1.0), color=YELLOW)  # Point 1: V=2.0 (doubled), P=1.0
            label_a = MathTex("A").next_to(point_a, UP+RIGHT)
            
            self.play(
                Create(point_a),
                Write(label_a),
            )

        # Create detailed piston system with heat source
        with self.voiceover(text="Let's label the temperature of the gas T_H. The cylinder head is in close contact with an energy source, which we represent as a heat reservoir at temperature T_H.") as tracker:
            # Create initial system using section 2's functions
            piston_system = self.create_piston_system()
            # Move piston to lower position
            piston_system[1].shift(DOWN * 1.5)  # Move piston down from its default position
            piston_system[2].shift(DOWN * 1.5)  # Move weights down with piston
            piston_system.shift(RIGHT*3)  # Move to right side
            
            particles, velocities = self.create_dynamic_particles()
            # Update particles to be below the new piston position
            for particle in particles:
                if particle.get_y() > -0.5:  # If particle is too high
                    particle.shift(DOWN * 2)  # Move it down
            particles.shift(RIGHT*3)  # Move particles with system
            
            # Create temperature visualization rectangle (initially invisible)
            temp_rect = Rectangle(
                width=2,  # Exact width between cylinder walls
                height=1.5,  # Initial height (lower than before)
                fill_opacity=0,
                fill_color=HIGH_TEMP_COLOR,
                stroke_opacity=0
            )
            # Position at center of cylinder, lower than before
            temp_rect.move_to([3, -1.25, 0])  # Shifted right by 3 units and down
            
            
            # Add labels
            temp_label_h = MathTex("T_H", color=HIGH_TEMP_COLOR).next_to(piston_system, UP)
            source_temp_label = MathTex("T_H", color=HIGH_TEMP_COLOR).next_to(piston_system, DOWN, buff=0.5)
            
            # Add cylinder head label and arrow
            cylinder_head_label = Text("Cylinder Head", font_size=20)
            cylinder_head_label.next_to(piston_system, RIGHT, buff=1)
            head_arrow = Arrow(
                cylinder_head_label.get_left(),
                piston_system[0].get_bottom(),
                color=WHITE,
                max_tip_length_to_length_ratio=0.15
            )
            
            self.play(
                Create(piston_system),
                FadeIn(temp_rect),
                LaggedStart(*[FadeIn(p) for p in particles]),
                Write(temp_label_h),
                Write(source_temp_label),
                Create(head_arrow),
                Write(cylinder_head_label),
                run_time=tracker.duration
            )

            # Animate particles for a short while with proper boundaries
            piston_height = piston_system[1].get_y()  # Get current piston height
            for _ in range(30):  # 30 frames of particle motion
                self.update_particles(particles, velocities, 0.1, bottom=-2, top=piston_height)
                self.wait(0.1)

        # Demonstrate isothermal expansion
        with self.voiceover(text="Now the gas inside is allowed to expand. When the gas expands, it does work on the surroundings, moving the piston upward. As the gas expands, its temperature would naturally decrease, but heat is continuously transferred from our energy source back into the gas, keeping the temperature constant at T_H.") as tracker:
            # Create heat transfer arrows
            def create_heat_arrows():
                arrows = VGroup()
                for i in range(4):
                    arrow = Arrow(
                        piston_system.get_bottom() + RIGHT*(i-1.5)*0.4,
                        temp_rect.get_bottom() + RIGHT*(i-1.5)*0.4,
                        color=HIGH_TEMP_COLOR,
                        max_tip_length_to_length_ratio=0.15
                    )
                    arrows.add(arrow)
                return arrows
            
            heat_arrows = create_heat_arrows()
            q_h_label = MathTex("Q_H", color=HIGH_TEMP_COLOR).next_to(heat_arrows, LEFT)
            
            # First show heat arrows
            self.play(
                FadeOut(head_arrow),
                FadeOut(cylinder_head_label),
                Create(heat_arrows),
                Write(q_h_label),
                run_time=tracker.duration/4
            )
            
            # Transition from particles to filled rectangle
            self.play(
                FadeOut(particles),
                temp_rect.animate.set_fill(opacity=0.3),
                run_time=tracker.duration/4
            )
            
            # Calculate new height for expansion
            initial_height = 1.5  # Starting from lower height
            expanded_height = 3.0  # Expand to original height
            
            # Create new rectangle with updated height but same width
            new_rect = Rectangle(
                width=2,  # Keep exact cylinder width
                height=expanded_height,
                fill_opacity=0.3,
                fill_color=HIGH_TEMP_COLOR,  # Color stays constant (isothermal)
                stroke_opacity=0
            ).move_to([3, -1.25 + (expanded_height - initial_height)/2, 0])  # Move up from initial position
            
            # Animate expansion
            self.play(
                piston_system[1].animate.shift(UP*1.5),  # Move piston up
                piston_system[2].animate.shift(UP*1.5),  # Move weights up with piston
                Transform(temp_rect, new_rect),  # Transform to new rectangle
                rate_func=smooth,

                run_time=tracker.duration/4
            )
            
            # Add explanation text
            explanation = VGroup(
                Text("• Reversible heat transfer", font_size=25),
                Text("• Temperature remains at T_H", font_size=25, color=HIGH_TEMP_COLOR),
                Text("• Gas does work as it expands", font_size=25)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            explanation.next_to(piston_system, DOWN, buff=1)
            
            self.play(
                Write(explanation),
                run_time=tracker.duration/4
            )

        with self.voiceover(text="Because the temperature difference between our energy source and the gas never changes more than an infinitesimal amount, this is a reversible heat transfer process. The total amount of heat transferred during this step is Q_H.") as tracker:
            # Create a small copy of the system next to point A
            small_piston = piston_system.copy().scale(0.4)
            small_piston.next_to(point_a, RIGHT, buff=0.1)
            small_temp_h = temp_label_h.copy().scale(0.4).next_to(small_piston, UP, buff=0.1)
            
            # Create small version of the temperature rectangle
            small_rect = temp_rect.copy().scale(0.4)
            small_rect.move_to(small_piston.get_center())  # Center with the small piston system
            
            # Create the small system with animation
            self.play(
                Create(small_piston),
                Create(small_rect),
                Write(small_temp_h),
                run_time=tracker.duration/2
            )
            
            # Fade out additional elements
            self.play(
                FadeOut(source_temp_label),
                FadeOut(heat_arrows),
                FadeOut(q_h_label),
                FadeOut(cylinder_head_label),
                FadeOut(explanation),
                run_time=tracker.duration/2
            )

        # Point B - Reversible Adiabatic Expansion
        with self.voiceover(text="The second step is called the Reversible Adiabatic Expansion. At this step, we remove the energy source and replace it with insulation. The system then becomes adiabatic. Adiabatic just means there is no heat transfer to or from the system to the surroundings. The gas still expands and drops in temperature. We will label the new temperature TL. In this hypothetical cycle, there is no friction between the piston and cylinder, so the process is reversible.") as tracker:
            # Create insulation visual (gray rectangle around cylinder)
            insulation = Rectangle(
                height=piston_system.height + 0.5,
                width=piston_system.width + 0.5,
                stroke_color=GRAY,
                fill_color=GRAY,
                fill_opacity=0.3
            ).move_to(piston_system)
            
            # Show insulation being added
            self.play(
                Create(insulation),
                run_time=tracker.duration/4
            )
            
            # Animate temperature change in main system
            self.play(
                temp_rect.animate.set_fill(color=LOW_TEMP_COLOR),
                run_time=tracker.duration/4
            )
            
            # Create point B and isothermal path from A to B
            point_b = Dot(axes.c2p(3.5, 0.45), color=YELLOW)
            label_b = MathTex("B").next_to(point_b, UP+RIGHT)
            
            # Create isothermal path A to B
            path_ab = CurvedArrow(
                start_point=point_a.get_center(),
                end_point=point_b.get_center(),
                angle=TAU/8,  # Slight curve
                color=YELLOW,
                tip_length=0.2
            )

            self.play(
                Create(point_b),
                Write(label_b),
                Create(path_ab),
                run_time=tracker.duration/4
            )

            # Create small copy at point B
            small_system_b = VGroup(
                piston_system.copy(),
                temp_rect.copy()
            ).scale(0.4)
            small_system_b.next_to(point_b, UP, buff=0.1)
            
            # Add temperature label T_L
            temp_label_b = MathTex("T_L", color=LOW_TEMP_COLOR).scale(0.4)
            temp_label_b.next_to(small_system_b, UP, buff=0.1)
            
            # Show small system
            self.play(
                Create(small_system_b),
                Write(temp_label_b),
                run_time=tracker.duration/4
            )

        # Point C - Reversible Isothermal Compression
        with self.voiceover(text="The third step is called the Reversible Isothermal Compression. Now the insulation is removed and the cylinder is now in contact with an energy sink at temperature TL. In simple terms, the sink we place is at the same temperature as the gas. Now an external force pushes on the piston downward. This causes the gas to compress, and the temperature begins to rise, but as soon as it's rising, the heat is transferred to the energy sink. So the temperature of the gas remains constant at TL. Because the temperature difference between our energy sink and the gas never changes more than an infinitesimal amount, this is a reversible heat transfer process.") as tracker:
            # Remove insulation
            self.play(
                FadeOut(insulation),
                run_time=tracker.duration/5
            )

            # Create point C and adiabatic path from B to C
            point_c = Dot(axes.c2p(4.0, 0.25), color=YELLOW)
            label_c = MathTex("C").next_to(point_c, DOWN+RIGHT)
            
            # Create adiabatic path B to C
            path_bc = CurvedArrow(
                start_point=point_b.get_center(),
                end_point=point_c.get_center(),
                angle=TAU/8,
                color=YELLOW,
                tip_length=0.2
            )

            # Calculate exact height change for compression
            height_change = 0.5  # The amount we want to compress
            current_height = temp_rect.height
            new_height = current_height - height_change
            
            # Create new temperature rectangle for main view
            new_main_temp_rect = Rectangle(
                width=temp_rect.width,
                height=new_height,  # Exact height change
                fill_color=LOW_TEMP_COLOR,
                fill_opacity=0.3,
                stroke_opacity=0
            ).move_to([temp_rect.get_x(), temp_rect.get_y() - height_change/2, 0])  # Move down by half the height change
            
            # Create heat transfer arrows from gas to cold reservoir
            heat_arrows = VGroup()
            for i in range(4):
                arrow = Arrow(
                    start=new_main_temp_rect.get_bottom() + RIGHT*(i-1.5)*0.4,
                    end=piston_system.get_bottom() + RIGHT*(i-1.5)*0.4,
                    color=LOW_TEMP_COLOR,
                    buff=0.1,
                    max_tip_length_to_length_ratio=0.15
                )
                heat_arrows.add(arrow)
            
            q_l_label = MathTex("Q_L", color=LOW_TEMP_COLOR).next_to(heat_arrows, LEFT)
            
            self.play(
                Create(point_c),
                Write(label_c),
                Create(path_bc),
                Create(heat_arrows),
                Transform(temp_rect, new_main_temp_rect),  # Transform both color and size
                piston_system[1].animate.shift(DOWN * height_change),  # Move piston down
                piston_system[2].animate.shift(DOWN * height_change),  # Move weights down with piston
                Write(q_l_label),
                run_time=tracker.duration/5
            )

            # Create small system at point C
            piston_system_c = piston_system.copy().scale(0.4)
            temp_rect_c = new_main_temp_rect.copy().scale(0.4)
            
            # Position the small system
            piston_system_c.next_to(point_c, RIGHT, buff=0.1)
            # Align temperature rectangle with bottom of piston system
            temp_rect_c.move_to(
                [
                    piston_system_c.get_center()[0],  # Same x coordinate
                    piston_system_c.get_bottom()[1] + temp_rect_c.height/2,  # Align bottom and move up by half height
                    0
                ]
            )
            
            # Show the small system
            self.play(
                Create(piston_system_c),
                Create(temp_rect_c),
                run_time=tracker.duration/5
            )

        # Point D - Reversible Adiabatic Compression
        with self.voiceover(text="The fourth and last step is called the Reversible Adiabatic Compression. Now the low energy sink is removed and insulation is placed back on the cylinder head. The gas continues to be compressed downward and it goes back to its initial state. In other words, the temperature rises from TL to TH which means the cycle is now complete. The area inside this closed path shows us the net work done during the cycle. Keep in mind that the Carnot heat-engine cycle is a reversible cycle, so every step can be reversed.") as tracker:
            # Remove cold reservoir and add insulation
            self.play(
                FadeOut(heat_arrows),
                FadeOut(q_l_label),
                Create(insulation),
                run_time=tracker.duration/5
            )

            # Create point D and isothermal path from C to D
            point_d = Dot(axes.c2p(2.4, 0.45), color=YELLOW)
            label_d = MathTex("D").next_to(point_d, DOWN+LEFT)
            
            # Create isothermal path C to D
            path_cd = CurvedArrow(
                start_point=point_c.get_center(),
                end_point=point_d.get_center(),
                angle=-TAU/8,
                color=YELLOW,
                tip_length=0.2
            )

            # Create adiabatic path D to A
            path_da = CurvedArrow(
                start_point=point_d.get_center(),
                end_point=point_a.get_center(),
                angle=-TAU/8,
                color=YELLOW,
                tip_length=0.2
            )

            # Calculate compression for main view
            compression_ratio = 0.5  # V_D/V_C = 2/4 = 0.5
            height_change = temp_rect.height * (1 - compression_ratio)
            
            # Create new temperature rectangle for main view with higher temperature
            compressed_temp_rect = Rectangle(
                width=temp_rect.width,
                height=temp_rect.height * compression_ratio,
                fill_color=HIGH_TEMP_COLOR,  # Temperature increases during adiabatic compression
                fill_opacity=0.3,
                stroke_opacity=0
            ).move_to([temp_rect.get_x(), temp_rect.get_y() - height_change/2, 0])

            self.play(
                Create(point_d),
                Write(label_d),
                Create(path_cd),
                Create(path_da),
                Transform(temp_rect, compressed_temp_rect),
                piston_system[1].animate.shift(DOWN * height_change),  # Move piston down
                piston_system[2].animate.shift(DOWN * height_change),  # Move weights down with piston
                run_time=tracker.duration/5
            )

            # Create small system at point D - fixed scaling issue
            piston_system_d = piston_system.copy()  # Copy first
            piston_system_d.scale(0.4)  # Then scale the copy
            temp_rect_d = compressed_temp_rect.copy()  # Copy first
            temp_rect_d.scale(0.4)  # Then scale the copy
            
            # Position the small system
            piston_system_d.next_to(point_d, DOWN, buff=0.1)
            # Align temperature rectangle with bottom of piston system
            temp_rect_d.move_to(
                [
                    piston_system_d.get_center()[0],  # Same x coordinate
                    piston_system_d.get_bottom()[1] + temp_rect_d.height/2,  # Align bottom and move up by half height
                    0
                ]
            )
            
            # Add temperature label (now at T_H since temperature increased)
            temp_label_d = MathTex("T_H", color=HIGH_TEMP_COLOR).scale(0.4)
            temp_label_d.next_to(piston_system_d, UP, buff=0.1)
            
            # Show the small system
            self.play(
                Create(piston_system_d),
                Create(temp_rect_d),
                Write(temp_label_d),
                run_time=tracker.duration/5
            )

        # Animate all paths and arrows
        self.play(
            Create(path_ab),
            Create(path_bc),
            Create(path_cd),
            Create(path_da),
            run_time=tracker.duration/4
        )

    def section5(self):
        # First recreate the PV diagram if running independently
        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.2, 0.2],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True},
        ).to_edge(LEFT, buff=1)

        # Add labels
        x_label = MathTex("V").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("p").next_to(axes.y_axis.get_end(), UP)
        
        # Create points
        point_a = Dot(axes.c2p(2.0, 1.0), color=YELLOW)
        point_b = Dot(axes.c2p(3.5, 0.45), color=YELLOW)
        point_c = Dot(axes.c2p(4.0, 0.25), color=YELLOW)
        point_d = Dot(axes.c2p(2.4, 0.45), color=YELLOW)
        
        # Add labels to points
        label_a = MathTex("A").next_to(point_a, UP+RIGHT).scale(0.7)
        label_b = MathTex("B").next_to(point_b, UP+RIGHT).scale(0.7)
        label_c = MathTex("C").next_to(point_c, DOWN+RIGHT).scale(0.7)
        label_d = MathTex("D").next_to(point_d, DOWN+LEFT).scale(0.7)
        
        # Create paths
        path_ab = CurvedArrow(
            start_point=point_a.get_center(),
            end_point=point_b.get_center(),
            angle=TAU/8,
            color=YELLOW,
            tip_length=0.2
        )
        path_bc = CurvedArrow(
            start_point=point_b.get_center(),
            end_point=point_c.get_center(),
            angle=TAU/8,
            color=YELLOW,
            tip_length=0.2
        )
        path_cd = CurvedArrow(
            start_point=point_c.get_center(),
            end_point=point_d.get_center(),
            angle=-TAU/8,
            color=YELLOW,
            tip_length=0.2
        )
        path_da = CurvedArrow(
            start_point=point_d.get_center(),
            end_point=point_a.get_center(),
            angle=-TAU/8,
            color=YELLOW,
            tip_length=0.2
        )

        # Create the complete diagram first
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Create(point_a),
            Create(point_b),
            Create(point_c),
            Create(point_d),
            Write(label_a),
            Write(label_b),
            Write(label_c),
            Write(label_d),
            Create(path_ab),
            Create(path_bc),
            Create(path_cd),
            Create(path_da),
            run_time=2
        )

        with self.voiceover(text="We've just seen in the Carnot cycle how the system absorbs heat Q_H from the high-temperature reservoir and releases heat Q_L to the low-temperature reservoir. Now, is there a specific relationship between these two heat quantities? Could this relationship depend solely on the temperatures?") as tracker:
            self.wait(tracker.duration)

        # Create labels for isothermal processes
        isothermal_high = Text("Isothermal", font_size=25, color=RED).next_to(path_ab.get_center(), UP, buff=0.3)
        isothermal_low = Text("Isothermal", font_size=25, color=BLUE).next_to(path_cd.get_center(), DOWN, buff=0.3)

        # Create temperature labels
        temp_high = MathTex("T_H", color=RED).next_to(isothermal_high, UP, buff=0.1)
        temp_low = MathTex("T_L", color=BLUE).next_to(isothermal_low, DOWN, buff=0.1)

        with self.voiceover(text="Let's begin with the two isothermal parts of the Carnot cycle — one at high temperature T_H, the other at low temperature T_L.") as tracker:
            # Highlight isothermal processes
            self.play(
                path_ab.animate.set_color(RED),
                path_cd.animate.set_color(BLUE),
                Write(isothermal_high),
                Write(isothermal_low),
                Write(temp_high),
                Write(temp_low),
                run_time=tracker.duration
            )

        # Create First Law equations
        first_law_eq1 = MathTex("Q = \\Delta U + W").scale(0.9).to_edge(RIGHT, buff=1.5).shift(UP).scale(0.7)
        first_law_eq2 = MathTex("\\Downarrow").next_to(first_law_eq1, DOWN, buff=0.3).scale(0.7)
        first_law_eq3 = MathTex("Q = W").next_to(first_law_eq2, DOWN, buff=0.3).scale(0.7)

        with self.voiceover(text="During an isothermal process, the internal energy of an ideal gas doesn't change, because the temperature stays constant. So, by the First Law of Thermodynamics:") as tracker:
            self.play(
                Write(first_law_eq1),
                run_time=tracker.duration/2
            )
            self.play(
                Write(first_law_eq2),
                Write(first_law_eq3),
                run_time=tracker.duration/2
            )

        with self.voiceover(text="In other words, the heat absorbed equals the work done by the gas. That work is given by integrating pressure over a volume change.") as tracker:
            self.wait(tracker.duration)

        # Remove first_law_eq1 and first_law_eq2, keep first_law_eq3 and move it up
        self.play(
            FadeOut(first_law_eq1),
            FadeOut(first_law_eq2),
            first_law_eq3.animate.shift(UP * 4),
            run_time=1
        )

        # Create ideal gas law equations
        ideal_gas_eq1 = MathTex("pV = nRT").next_to(first_law_eq3, DOWN+LEFT, buff=0.5).scale(0.7)
        ideal_gas_eq2 = MathTex("\\Rightarrow p = \\frac{nRT}{V}").next_to(ideal_gas_eq1, RIGHT, buff=0.3).scale(0.7)

        with self.voiceover(text="To evaluate this, we express the pressure using the ideal gas law. Do you remember it?") as tracker:
            self.play(
                Write(ideal_gas_eq1),
                Write(ideal_gas_eq2),
                run_time=tracker.duration
            )

        # Create high temperature process equation
        high_temp_eq = MathTex(
            "Q_H = \\int_{a}^{b} p \\, dV = \\int_{a}^{b} \\frac{nRT_H}{V} \\, dV = nRT_H \\ln \\left( \\frac{V_B}{V_A} \\right)"
        ).scale(0.7).next_to(ideal_gas_eq1, DOWN, buff=0.8)

        with self.voiceover(text="So for the high-temperature isothermal expansion from point A to point B:") as tracker:
            # Highlight path A to B again
            self.play(
                path_ab.animate.set_stroke(width=6),
                run_time=tracker.duration/2
            )
            self.play(
                Write(high_temp_eq),
                run_time=tracker.duration/2
            )

        # Create low temperature process equation
        low_temp_eq = MathTex(
            "Q_L = -\\int_{V_C}^{V_D} p \\, dV = -\\int_{V_C}^{V_D} \\frac{nRT_L}{V} \\, dV = -nRT_L \\ln \\left( \\frac{V_D}{V_C} \\right)"
        ).scale(0.7).next_to(high_temp_eq, DOWN, buff=0.5)

        with self.voiceover(text="Likewise, during the isothermal compression at temperature T_L, from point C to D, the system releases heat:") as tracker:
            # Highlight path C to D
            self.play(
                path_ab.animate.set_stroke(width=2),  # Reset A to B stroke width
                path_cd.animate.set_stroke(width=6),
                run_time=tracker.duration/2
            )
            self.play(
                Write(low_temp_eq),
                run_time=tracker.duration/2
            )

        with self.voiceover(text="The negative sign here reflects that heat is leaving the system.") as tracker:
            # Highlight the negative sign
            negative_sign = low_temp_eq.get_part_by_tex("-").copy().set_color(RED)
            self.play(
                path_cd.animate.set_stroke(width=2),  # Reset C to D stroke width
                negative_sign.animate,
                run_time=tracker.duration
            )

            # Remove all previous equations
            self.play(
                *[FadeOut(mob) for mob in [
                    first_law_eq3, ideal_gas_eq1, ideal_gas_eq2,
                    high_temp_eq, low_temp_eq, negative_sign
                ]],
                run_time=1
            )

            # Create grid lines covering the entire area
            horizontal_lines = VGroup(*[
                Line(
                    axes.c2p(2.0, y),
                    axes.c2p(4.0, y),
                    stroke_width=1,
                    stroke_opacity=0.3
                )
                for y in np.arange(0.25, 1.0, 0.1)
            ])

            vertical_lines = VGroup(*[
                Line(
                    axes.c2p(x, 0.25),
                    axes.c2p(x, 1.0),
                    stroke_width=1,
                    stroke_opacity=0.3
                )
                for x in np.arange(2.0, 4.0, 0.2)
            ])

            # Create the path for clipping using the same curves as the original paths
            cycle_path = VMobject()
            
            # Helper function to get points along a curved arrow path
            def get_curved_path_points(start, end, angle):
                # Create a temporary CurvedArrow to get its path
                temp_arrow = CurvedArrow(
                    start_point=start,
                    end_point=end,
                    angle=angle,
                    color=YELLOW,
                    tip_length=0  # No arrow tip needed
                )
                # Get the points from the curve (excluding the arrow tip)
                return temp_arrow.get_points()[:-1]  # Exclude the last point to avoid overlap
            
            # Start from point A
            cycle_path.start_new_path(point_a.get_center())
            
            # Add path A to B (angle=TAU/8)
            ab_points = get_curved_path_points(point_a.get_center(), point_b.get_center(), TAU/8)
            cycle_path.append_points(ab_points)
            
            # Add path B to C (angle=TAU/8)
            bc_points = get_curved_path_points(point_b.get_center(), point_c.get_center(), TAU/8)
            cycle_path.append_points(bc_points)
            
            # Add path C to D (angle=-TAU/8)
            cd_points = get_curved_path_points(point_c.get_center(), point_d.get_center(), -TAU/8)
            cycle_path.append_points(cd_points)
            
            # Add path D to A (angle=-TAU/8)
            da_points = get_curved_path_points(point_d.get_center(), point_a.get_center(), -TAU/8)
            cycle_path.append_points(da_points)
            
            cycle_path.close_path()

            # Create the filled area using the curved path
            area = cycle_path.copy()
            area.set_fill(YELLOW, opacity=0.2)
            area.set_stroke(width=0)

            # Group grid lines
            grid = VGroup(horizontal_lines, vertical_lines)
            
            # Create clipped grid using Intersection
            clipped_grid = VGroup()
            for line in grid:
                clipped_line = Intersection(line, cycle_path)
                clipped_line.set_stroke(width=1, opacity=0.3)
                clipped_grid.add(clipped_line)

            with self.voiceover(text="Before we go further, take a closer look at the Carnot cycle on the pressure–volume diagram. The four processes form a closed loop — and the area enclosed by this loop represents the net work output of the engine.") as tracker:
                self.play(
                    FadeIn(area),
                    Create(clipped_grid),
                    run_time=tracker.duration
                )

            with self.voiceover(text="Why? Because the area under any curve on a P-V diagram equals the work done in that process. So the total work done in the entire cycle — W net — is exactly the area inside the loop.") as tracker:
                # Highlight the area by pulsing the opacity
                self.play(
                    area.animate.set_fill(opacity=0.4),
                    run_time=tracker.duration/2
                )
                self.play(
                    area.animate.set_fill(opacity=0.2),
                    run_time=tracker.duration/2
                )

            # Create work equation
            work_eq = MathTex(
                "W_{\\text{net}} = Q_H + Q_L \\quad (\\text{since } Q_L < 0)"
            ).scale(0.7).to_edge(RIGHT, buff=1)

            with self.voiceover(text="This visual interpretation connects our heat input and output directly to mechanical work. So the area is equal to useful work.") as tracker:
                self.play(
                    Write(work_eq),
                    area.animate.set_fill(opacity=0.3),
                    run_time=tracker.duration
                )

            # Clear previous equations and reset path colors
            self.play(
                FadeOut(work_eq),
                path_ab.animate.set_color(YELLOW),
                path_cd.animate.set_color(YELLOW),
                run_time=1
            )

            # Create adiabatic labels
            adiabatic_expansion = Text("Adiabatic", font_size=25, color=GREEN).next_to(path_bc.get_center(), RIGHT, buff=0.3)
            adiabatic_compression = Text("Adiabatic", font_size=25, color=GREEN).next_to(path_da.get_center(), LEFT, buff=0.3)

            # Create adiabatic equation
            adiabatic_eq = MathTex(
                "TV^{\\gamma - 1} = \\text{constant}"
            ).scale(0.7).to_edge(RIGHT, buff=1)

            with self.voiceover(text="Now let's bring in the adiabatic steps of the cycle. These are the steps where no heat is transferred, but the gas still expands or compresses. They follow:") as tracker:
                # Highlight adiabatic paths and show labels
                self.play(
                    path_bc.animate.set_color(GREEN),
                    path_da.animate.set_color(GREEN),
                    path_bc.animate.set_stroke(width=6),
                    path_da.animate.set_stroke(width=6),
                    Write(adiabatic_expansion),
                    Write(adiabatic_compression),
                    run_time=tracker.duration/2
                )
                self.play(
                    Write(adiabatic_eq),
                    run_time=tracker.duration/2
                )

            # Create volume ratio equations
            volume_ratios = MathTex(
                "T_H V_b^{\\gamma - 1} &= T_L V_c^{\\gamma - 1} \\\\",
                "T_H V_a^{\\gamma - 1} &= T_L V_d^{\\gamma - 1}"
            ).scale(0.7).next_to(adiabatic_eq, DOWN, buff=0.5)

            with self.voiceover(text="For the adiabatic expansion from point b to c, and the adiabatic compression from d to a, we have:") as tracker:
                self.play(
                    Write(volume_ratios),
                    run_time=tracker.duration
                )

            with self.voiceover(text="These allow us to relate the volume ratios in the Q_H and Q_L expressions.") as tracker:
                # Reset path stroke width
                self.play(
                    path_bc.animate.set_stroke(width=2),
                    path_da.animate.set_stroke(width=2),
                    run_time=tracker.duration
                )

            # Clear previous equations but keep the diagram
            self.play(
                FadeOut(adiabatic_eq),
                FadeOut(volume_ratios),
                run_time=1
            )

            # Show heat equations divided by temperature
            heat_temp_ratios = MathTex(
                "\\frac{Q_H}{T_H} &= mR \\ln \\left( \\frac{V_b}{V_a} \\right), \\\\",
                "\\frac{Q_L}{T_L} &= -mR \\ln \\left( \\frac{V_c}{V_d} \\right)"
            ).scale(0.7).to_edge(RIGHT, buff=1)

            with self.voiceover(text="Now watch this: if we take our expressions for heat and divide them by their respective temperatures, we get:") as tracker:
                self.play(
                    Write(heat_temp_ratios),
                    run_time=tracker.duration
                )

            # Show volume ratio relationship
            volume_relationship = MathTex(
                "\\frac{V_b}{V_a} = \\frac{V_c}{V_d}"
            ).scale(0.7).next_to(heat_temp_ratios, DOWN, buff=0.5)

            with self.voiceover(text="But from the adiabatic relations, we know that these volume ratios are equal:") as tracker:
                self.play(
                    Write(volume_relationship),
                    run_time=tracker.duration
                )

            # Final equation
            final_equation = MathTex(
                "\\frac{Q_H}{T_H} + \\frac{Q_L}{T_L} = 0"
            ).scale(0.7).next_to(volume_relationship, DOWN, buff=0.5)

            with self.voiceover(text="So the two logarithms are equal and opposite. This leads us to a profound result: The ratio of heat to temperature for the high-temperature reservoir exactly balances the ratio for the low-temperature reservoir. This is not just a mathematical curiosity — it's a fundamental property of all reversible heat engines, and it points to a deep connection between heat flow and temperature in thermodynamic processes.") as tracker:
                self.play(
                    Write(final_equation),
                    run_time=tracker.duration/3
                )
                
                # Highlight the equation by scaling it up briefly
                self.play(
                    final_equation.animate.scale(1.2),
                    run_time=tracker.duration/3
                )
                
                self.play(
                    final_equation.animate.scale(1/1.2),  # Scale back to original size
                    run_time=tracker.duration/3
                )

    def section6(self):
        # Start with the previous result
        previous_equation = MathTex(
            "\\frac{Q_H}{T_H} + \\frac{Q_L}{T_L} = 0"
        ).scale(0.8).to_edge(UP, buff=1)

        with self.voiceover(text="This result is extremely important — it leads us directly to the concept of entropy.") as tracker:
            self.play(
                Write(previous_equation),
                run_time=tracker.duration
            )

        # Define entropy formally
        entropy_definition = MathTex(
            "dS = \\frac{dQ}{T}"
        ).scale(0.8)
        
        entropy_text = Text(
            "Entropy Change",
            font_size=30,
            color=BLUE
        ).next_to(entropy_definition, UP, buff=0.3)

        with self.voiceover(text="We define entropy change dS as the amount of heat transferred, divided by the temperature at which it happens.") as tracker:
            self.play(
                Write(entropy_definition),
                Write(entropy_text),
                run_time=tracker.duration
            )

        # Apply to Carnot cycle
        carnot_entropy = MathTex(
            "dS_H + dS_L = 0"
        ).scale(0.8).next_to(entropy_definition, DOWN, buff=0.5)

        with self.voiceover(text="So, for the entire reversible Carnot cycle, the total entropy change is zero.") as tracker:
            self.play(
                Write(carnot_entropy),
                run_time=tracker.duration/2
            )

        with self.voiceover(text="In other words: A reversible cycle produces no net change in entropy — it's perfectly balanced.") as tracker:
            # Create a balance scale visualization
            scale_left = Line(LEFT*2, ORIGIN).set_color(YELLOW)
            scale_right = Line(ORIGIN, RIGHT*2).set_color(YELLOW)
            scale_center = Dot(ORIGIN, color=YELLOW)
            scale = VGroup(scale_left, scale_right, scale_center)
            scale.next_to(carnot_entropy, DOWN, buff=0.8)
            
            self.play(
                Create(scale),
                run_time=tracker.duration
            )

        # Clear previous animations except the title
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != previous_equation],
            run_time=1
        )

        # Create entropy visualization
        with self.voiceover(text="But what is entropy, really? Entropy measures how spread out or dispersed energy becomes. When we add heat to a system, we're increasing the number of ways the system's molecules can move around — and that's an increase in entropy.") as tracker:
            # Create particle system visualization
            particles_ordered = VGroup(*[
                Dot(radius=0.05, color=BLUE) for _ in range(20)
            ]).arrange_in_grid(4, 5, buff=0.2)
            particles_ordered.to_edge(LEFT, buff=2)
            
            particles_disordered = VGroup(*[
                Dot(radius=0.05, color=RED).move_to(
                    particles_ordered.get_center() + 
                    RIGHT * np.random.uniform(-2, 2) +
                    UP * np.random.uniform(-1, 1)
                ) for _ in range(20)
            ]).next_to(particles_ordered, RIGHT, buff=2)
            
            arrow = Arrow(particles_ordered.get_center(), particles_disordered.get_center())
            heat_text = Text("Heat", font_size=25, color=RED).next_to(arrow, UP)
            
            self.play(
                Create(particles_ordered),
                run_time=tracker.duration/3
            )
            
            self.play(
                Create(arrow),
                Write(heat_text),
                run_time=tracker.duration/3
            )
            
            self.play(
                Create(particles_disordered),
                run_time=tracker.duration/3
            )

        with self.voiceover(text="If you add the same amount of heat to a cold system, the energy causes a bigger change — because it disrupts a more ordered state. That's why dQ/T is larger when T is small.") as tracker:
            # Clear previous animations
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
            
            # Create two systems side by side
            cold_system = Rectangle(height=3, width=2.5, color=BLUE)
            hot_system = Rectangle(height=3, width=2.5, color=RED)
            systems = VGroup(cold_system, hot_system).arrange(RIGHT, buff=2)
            
            # Create ordered particles for cold system (grid arrangement)
            cold_particles = VGroup(*[
                Dot(radius=0.05, color=BLUE) for _ in range(25)
            ]).arrange_in_grid(5, 5, buff=0.2)
            cold_particles.move_to(cold_system)
            
            # Create more random particles for hot system
            hot_particles = VGroup(*[
                Dot(radius=0.05, color=RED).move_to(
                    hot_system.get_center() + 
                    RIGHT * np.random.uniform(-1, 1) +
                    UP * np.random.uniform(-1, 1)
                ) for _ in range(25)
            ])
            
            # Labels
            cold_label = MathTex("T_L", color=BLUE).next_to(cold_system, UP)
            hot_label = MathTex("T_H", color=RED).next_to(hot_system, UP)
            
            # Initial entropy values
            cold_entropy = MathTex("S_1", color=BLUE).next_to(cold_system, DOWN)
            hot_entropy = MathTex("S_2", color=RED).next_to(hot_system, DOWN)
            
            # Show initial state
            self.play(
                Create(systems),
                Write(cold_label),
                Write(hot_label),
                Write(cold_entropy),
                Write(hot_entropy),
                run_time=tracker.duration/4
            )
            
            self.play(
                LaggedStart(*[Create(p) for p in cold_particles]),
                LaggedStart(*[Create(p) for p in hot_particles]),
                run_time=tracker.duration/4
            )
            
            # Add same amount of heat to both systems
            heat_arrow_cold = Arrow(
                cold_system.get_left() + LEFT,
                cold_system.get_left(),
                color=YELLOW,
                max_tip_length_to_length_ratio=0.15
            )
            heat_arrow_hot = Arrow(
                hot_system.get_left() + LEFT,
                hot_system.get_left(),
                color=YELLOW,
                max_tip_length_to_length_ratio=0.15
            )
            
            dq_text_cold = MathTex("dQ", color=YELLOW).next_to(heat_arrow_cold, LEFT)
            dq_text_hot = MathTex("dQ", color=YELLOW).next_to(heat_arrow_hot, LEFT)
            
            self.play(
                Create(heat_arrow_cold),
                Create(heat_arrow_hot),
                Write(dq_text_cold),
                Write(dq_text_hot),
                run_time=tracker.duration/4
            )
            
            # Animate particles becoming more disordered
            cold_particles_final = VGroup(*[
                Dot(radius=0.05, color=BLUE).move_to(
                    cold_system.get_center() + 
                    RIGHT * np.random.uniform(-1, 1) +
                    UP * np.random.uniform(-1, 1)
                ) for _ in range(25)
            ])
            
            hot_particles_final = VGroup(*[
                Dot(radius=0.05, color=RED).move_to(
                    hot_system.get_center() + 
                    RIGHT * np.random.uniform(-1.1, 1.1) +
                    UP * np.random.uniform(-1.1, 1.1)
                ) for _ in range(25)
            ])
            
            # Show entropy change
            cold_entropy_final = MathTex("S_1 + \\frac{dQ}{T_L}", color=BLUE).next_to(cold_system, DOWN)
            hot_entropy_final = MathTex("S_2 + \\frac{dQ}{T_H}", color=RED).next_to(hot_system, DOWN)
            
            self.play(
                Transform(cold_particles, cold_particles_final),
                Transform(hot_particles, hot_particles_final),
                Transform(cold_entropy, cold_entropy_final),
                Transform(hot_entropy, hot_entropy_final),
                run_time=tracker.duration/4
            )
            
            # Add explanation text
            explanation = VGroup(
                Text("Same heat (dQ)", font_size=25, color=YELLOW),
                Text("→ Bigger entropy change in cold system", font_size=25),
                MathTex("\\frac{dQ}{T_L} > \\frac{dQ}{T_H}")
            ).arrange(DOWN, buff=0.3).to_edge(DOWN)
            
            self.play(
                Write(explanation),
                run_time=1
            )

        # Clear for next part
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

        # Create Carnot cycle entropy explanation
        with self.voiceover(text="In the Carnot cycle: We absorb heat Q_H at high temperature T_H, increasing entropy by Q_H/T_H. We release heat Q_L at lower temperature T_L, decreasing entropy by -Q_L/T_L. And because the process is reversible, these two changes cancel exactly.") as tracker:
            # Clear previous animations
            # Create PV diagram on the left side
            axes = Axes(
                x_range=[0, 5, 1],
                y_range=[0, 1.2, 0.2],
                x_length=4,
                y_length=4,
                axis_config={"include_tip": True},
            ).to_edge(LEFT, buff=1)

            # Add labels to axes
            x_label = MathTex("V").next_to(axes.x_axis.get_end(), RIGHT)
            y_label = MathTex("p").next_to(axes.y_axis.get_end(), UP)
            
            # Create points for the cycle
            point_a = Dot(axes.c2p(2.0, 1.0), color=YELLOW)
            point_b = Dot(axes.c2p(3.5, 0.45), color=YELLOW)
            point_c = Dot(axes.c2p(4.0, 0.25), color=YELLOW)
            point_d = Dot(axes.c2p(2.4, 0.45), color=YELLOW)
            
            # Add labels to points
            label_a = MathTex("A").next_to(point_a, UP+RIGHT).scale(0.7)
            label_b = MathTex("B").next_to(point_b, UP+RIGHT).scale(0.7)
            label_c = MathTex("C").next_to(point_c, DOWN+RIGHT).scale(0.7)
            label_d = MathTex("D").next_to(point_d, DOWN+LEFT).scale(0.7)
            
            # Create paths with different colors for isothermal and adiabatic processes
            path_ab = CurvedArrow(
                start_point=point_a.get_center(),
                end_point=point_b.get_center(),
                angle=TAU/8,
                color=RED,  # High temperature isothermal
                tip_length=0.2
            )
            path_bc = CurvedArrow(
                start_point=point_b.get_center(),
                end_point=point_c.get_center(),
                angle=TAU/8,
                color=GREEN,  # Adiabatic
                tip_length=0.2
            )
            path_cd = CurvedArrow(
                start_point=point_c.get_center(),
                end_point=point_d.get_center(),
                angle=-TAU/8,
                color=BLUE,  # Low temperature isothermal
                tip_length=0.2
            )
            path_da = CurvedArrow(
                start_point=point_d.get_center(),
                end_point=point_a.get_center(),
                angle=-TAU/8,
                color=GREEN,  # Adiabatic
                tip_length=0.2
            )

            # Create labels for processes
            iso_high = Text("Isothermal (T_H)", font_size=20, color=RED).next_to(path_ab, UP, buff=0.2)
            iso_low = Text("Isothermal (T_L)", font_size=20, color=BLUE).next_to(path_cd, DOWN, buff=0.2)
            
            # Show PV diagram
            self.play(
                Create(axes),
                Write(x_label),
                Write(y_label),
                run_time=tracker.duration/4
            )
            
            self.play(
                Create(point_a),
                Create(point_b),
                Create(point_c),
                Create(point_d),
                Write(label_a),
                Write(label_b),
                Write(label_c),
                Write(label_d),
            )

            # Create entropy equations on the right side
            carnot_entropy_eq = VGroup(
                MathTex("\\text{High temp:} \\quad \\Delta S_H = \\frac{Q_H}{T_H}", color=RED),
                MathTex("\\text{Low temp:} \\quad \\Delta S_L = \\frac{Q_L}{T_L}", color=BLUE),
                MathTex("\\text{Total:} \\quad \\Delta S_{total} = \\frac{Q_H}{T_H} + \\frac{Q_L}{T_L} = 0")
            ).arrange(DOWN, buff=0.5).to_edge(RIGHT)

            # Show isothermal expansion and corresponding entropy increase
            self.play(
                Create(path_ab),
                Write(iso_high),
                Write(carnot_entropy_eq[0]),
                run_time=tracker.duration/6
            )

            # Show adiabatic expansion
            self.play(
                Create(path_bc),
                run_time=tracker.duration/6
            )

            # Show isothermal compression and corresponding entropy decrease
            self.play(
                Create(path_cd),
                Write(iso_low),
                Write(carnot_entropy_eq[1]),
                run_time=tracker.duration/6
            )

            # Show adiabatic compression and total entropy equation
            self.play(
                Create(path_da),
                Write(carnot_entropy_eq[2]),
                run_time=tracker.duration/6
            )

            # Add arrows connecting equations to cycle parts
            arrow_high = Arrow(
                carnot_entropy_eq[0].get_left() + LEFT * 0.5,
                path_ab.get_center(),
                color=RED,
                max_tip_length_to_length_ratio=0.15
            )
            
            arrow_low = Arrow(
                carnot_entropy_eq[1].get_left() + LEFT * 0.5,
                path_cd.get_center(),
                color=BLUE,
                max_tip_length_to_length_ratio=0.15
            )

            self.play(
                Create(arrow_high),
                Create(arrow_low),
            )

        with self.voiceover(text="In the real world, no engine is perfectly reversible. There's always some friction, heat loss, or turbulence — and those make energy spread out even more. So in any irreversible process, the total entropy increases.") as tracker:
            # Create real-world effects visualization
            effects = VGroup(
                Text("Friction", font_size=25, color=YELLOW),
                Text("Heat Loss", font_size=25, color=RED),
                Text("Turbulence", font_size=25, color=BLUE)
            ).arrange(RIGHT, buff=1).next_to(carnot_entropy_eq, DOWN, buff=0.5).scale(0.7)
            
            arrow_increase = Arrow(LEFT, RIGHT, color=GREEN)
            increase_text = MathTex("\\Delta S_{total} > 0").next_to(arrow_increase, RIGHT)
            
            increase_group = VGroup(arrow_increase, increase_text).next_to(effects, DOWN)
            
            self.play(
                Write(effects),
                run_time=tracker.duration/2
            )
            self.play(
                Create(arrow_increase),
                Write(increase_text),
            )
        # Final summary
        with self.voiceover(text="Entropy tracks the irreversibility of a process. If the process is reversible, the total entropy change is zero. If it's irreversible, the total entropy must increase. Entropy gives us the direction of time — and defines the limits of what we can do with energy.") as tracker:
            summary = VGroup(
                Text("Entropy and Irreversibility", font_size=35, color=YELLOW),
                MathTex("\\text{Reversible:} \\quad \\Delta S_{total} = 0"),
                MathTex("\\text{Irreversible:} \\quad \\Delta S_{total} > 0"),
                Text("→ Direction of Time", font_size=30),
                Text("→ Limits of Energy Conversion", font_size=30)
            ).arrange(DOWN, buff=0.4)
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

            self.play(
                FadeOut(carnot_entropy_eq),
                FadeOut(effects),
                FadeOut(arrow_increase),
                FadeOut(increase_text),
                run_time=tracker.duration/5
            )
            
            self.play(
                Write(summary),
                run_time=tracker.duration*4/5
            )

    def section7(self):
        # Start with Carnot cycle review
        with self.voiceover(text="So far, we've seen that entropy helps us understand the limits of what's possible in energy conversion. A reversible Carnot cycle produces no net entropy. But in real-world, irreversible processes — entropy always increases.") as tracker:
            # Create PV diagram of Carnot cycle
            axes = Axes(
                x_range=[0, 5, 1],
                y_range=[0, 1.2, 0.2],
                x_length=5,
                y_length=5,
                axis_config={"include_tip": True},
            ).to_edge(LEFT, buff=1)

            # Add labels
            x_label = MathTex("V").next_to(axes.x_axis.get_end(), RIGHT)
            y_label = MathTex("p").next_to(axes.y_axis.get_end(), UP)
            
            # Create points and paths
            points = {
                'A': [2.0, 1.0],
                'B': [3.5, 0.45],
                'C': [4.0, 0.25],
                'D': [2.4, 0.45]
            }
            
            dots = {}
            labels = {}
            for point, coords in points.items():
                dots[point] = Dot(axes.c2p(*coords), color=YELLOW)
                labels[point] = MathTex(point).next_to(dots[point], UP+RIGHT if point in ['A','B'] else DOWN+RIGHT).scale(0.7)

            paths = {
                'AB': CurvedArrow(dots['A'].get_center(), dots['B'].get_center(), angle=TAU/8, color=RED),
                'BC': CurvedArrow(dots['B'].get_center(), dots['C'].get_center(), angle=TAU/8, color=GREEN),
                'CD': CurvedArrow(dots['C'].get_center(), dots['D'].get_center(), angle=-TAU/8, color=BLUE),
                'DA': CurvedArrow(dots['D'].get_center(), dots['A'].get_center(), angle=-TAU/8, color=GREEN)
            }

            # Show diagram
            self.play(
                Create(axes),
                Write(x_label),
                Write(y_label),
                *[Create(dot) for dot in dots.values()],
                *[Write(label) for label in labels.values()],
                *[Create(path) for path in paths.values()],
                run_time=tracker.duration
            )

        with self.voiceover(text="This brings us to one of the most profound principles in all of physics — the Second Law of Thermodynamics.") as tracker:
            title = Text("Second Law of Thermodynamics", color=YELLOW).to_edge(UP)
            
            self.play(
                Write(title),
                run_time=tracker.duration
            )

        # Kelvin-Planck Statement
        with self.voiceover(text="The first version of the second law focuses on heat engines. It states: It is impossible to devise a cyclically operating device whose sole effect is to absorb heat from a single thermal reservoir and perform an equivalent amount of work.") as tracker:
            # Clear previous animations except title
            self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title], run_time=0.5)
            
            # Create engine visualization
            engine = Rectangle(height=2, width=3, color=WHITE)
            reservoir = Rectangle(height=1, width=4, color=RED, fill_opacity=0.3)
            
            # Position elements
            reservoir.next_to(engine, UP, buff=0.5)
            
            # Labels
            engine_label = Text("Heat Engine", font_size=25).move_to(engine)
            reservoir_label = MathTex("T_H").next_to(reservoir, RIGHT)
            
            # Arrows for impossible process
            heat_in = Arrow(reservoir.get_bottom(), engine.get_top(), color=RED)
            work_out = Arrow(engine.get_right(), engine.get_right() + RIGHT * 2, color=GREEN)
            
            # Cross out the impossible process
            cross = Cross(VGroup(engine, heat_in, work_out))
            
            # Show elements
            self.play(
                Create(engine),
                Create(reservoir),
                Write(engine_label),
                Write(reservoir_label),
                Create(heat_in),
                Create(work_out),
                run_time=tracker.duration/2
            )
            
            self.play(
                Create(cross),
                run_time=tracker.duration/2
            )

        # Clausius Statement
        with self.voiceover(text="The second version focuses on heat transfer. It states: It is impossible to construct a cyclically operating device whose sole effect is to transfer heat from a colder body to a hotter body.") as tracker:
            # Clear previous
            self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title], run_time=0.5)
            
            # Create hot and cold reservoirs
            hot_res = Rectangle(height=1.5, width=2, color=RED, fill_opacity=0.3)
            cold_res = Rectangle(height=1.5, width=2, color=BLUE, fill_opacity=0.3)
            
            # Position side by side
            VGroup(hot_res, cold_res).arrange(RIGHT, buff=2)
            
            # Labels
            hot_label = MathTex("T_H").next_to(hot_res, UP)
            cold_label = MathTex("T_L").next_to(cold_res, UP)
            
            # Impossible heat transfer arrow
            heat_arrow = Arrow(cold_res.get_right(), hot_res.get_left(), color=RED)
            
            # Cross out impossible process
            cross2 = Cross(VGroup(hot_res, cold_res, heat_arrow))
            
            self.play(
                Create(hot_res),
                Create(cold_res),
                Write(hot_label),
                Write(cold_label),
                Create(heat_arrow),
                run_time=tracker.duration/2
            )
            
            self.play(
                Create(cross2),
                run_time=tracker.duration/2
            )

        # Entropy Statement
        with self.voiceover(text="The third version is the most general and the most powerful — formulated in terms of entropy. In any cyclic process, the total entropy of the system and its surroundings either increases or remains unchanged; it never decreases.") as tracker:
            # Clear previous
            self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title], run_time=0.5)
            
            # Create universe representation
            universe = Circle(radius=2, color=BLUE)
            system = Circle(radius=0.5, color=YELLOW).move_to(universe.get_center())
            
            # Entropy arrows (always increasing)
            arrows = VGroup(*[
                Arrow(
                    system.get_center(),
                    universe.point_at_angle(angle),
                    color=RED_A
                ) for angle in np.linspace(0, TAU, 8)
            ])
            
            # Entropy equation
            entropy_eq = MathTex(
                "ds = \\frac{\\delta q}{T} + ds_{irr} > \\frac{\\delta q}{T}"
            ).next_to(universe, DOWN, buff=0.5)
            
            self.play(
                Create(universe),
                Create(system),
                run_time=tracker.duration/3
            )
            
            self.play(
                LaggedStart(*[Create(arrow) for arrow in arrows]),
                run_time=tracker.duration/3
            )
            
            self.play(
                Write(entropy_eq),
                run_time=tracker.duration/3
            )

        # Final wrap-up
        with self.voiceover(text="All three versions of the Second Law say the same thing in different ways: You can't get more than what you put in — and you'll probably get less. That missing piece? It's entropy — and it tells us not just how energy moves, but what we can never do with it.") as tracker:
            # Create summary boxes
            statements = VGroup(
                Text("1. No perfect heat engine", font_size=25),
                Text("2. No spontaneous heat flow to higher T", font_size=25),
                Text("3. Entropy always increases", font_size=25)
            ).arrange(DOWN, buff=0.5)
            
            arrow = Arrow(UP, DOWN, color=YELLOW)
            conclusion = Text("Nature's Universal Limitation", color=YELLOW, font_size=30)
            
            VGroup(statements, arrow, conclusion).arrange(DOWN, buff=1)
            
            self.play(
                FadeOut(universe),
                FadeOut(system),
                FadeOut(arrows),
                FadeOut(entropy_eq),
            )
            
            self.play(
                Write(statements),
                Create(arrow),
                Write(conclusion),
            )

if __name__ == "__main__":
    from manim import *
    config.disable_caching = False
    config.quality = "high_quality"
    scene = CarnotProcessScene()
    scene.render()