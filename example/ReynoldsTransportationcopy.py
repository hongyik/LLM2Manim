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
            text="Welcome back, fluid enthusiasts! Today, we're unlocking the Reynolds "
            "Transport Theorem—a game-changer for analyzing fluid systems. Ever wondered "
            "how engineers predict forces on airplanes or design water pumps? RTT is "
            "their secret weapon. Let's dive in!"
        ) as tracker:
            # Create title
            title = Text("Reynolds Transport Theorem:", font_size=48)
            subtitle = Text("Bridging Fluid Perspectives", font_size=36)
            title_group = VGroup(title, subtitle).arrange(DOWN)
            
            # Create background animation (flowing particles)
            box = Cube(side_length=4, fill_opacity=0.1, stroke_width=2)
            particles = VGroup(*[Dot() for _ in range(20)])
            
            # Distribute particles randomly within the cube
            for particle in particles:
                particle.move_to(np.array([
                    np.random.uniform(-1.5, 1.5),
                    np.random.uniform(-1.5, 1.5),
                    np.random.uniform(-1.5, 1.5)
                ]))
            
            # Animate title and background
            self.play(Write(title_group))
            self.play(
                Create(box),
                *[Create(p) for p in particles]
            )
            
            # Animate particles flowing
            self.play(
                *[
                    p.animate.shift(
                        np.array([
                            np.random.uniform(-1, 1),
                            np.random.uniform(-1, 1),
                            np.random.uniform(-1, 1)
                        ])
                    )
                    for p in particles
                ],
                run_time=2,
                rate_func=rate_functions.linear
            )

        # Transition to Lagrangian vs Eulerian view
        with self.voiceover(
            text="RTT connects two worlds: tracking a moving fluid parcel—the Lagrangian "
            "view—and observing a fixed region of space—the Eulerian view. It answers: "
            "How do properties like mass or momentum change in a system versus a control volume?"
        ) as tracker:
            # Clear previous scene
            self.play(FadeOut(title_group), FadeOut(box), FadeOut(particles))
            
            # Create split screen
            line = Line(UP * 3, DOWN * 3)
            
            # Lagrangian view (left side)
            lagrangian_title = Text("Lagrangian View", font_size=36).move_to(LEFT * 3 + UP * 2)
            lagrangian_particles = VGroup(*[Dot() for _ in range(10)]).arrange_in_grid(
                rows=2, cols=5, buff=0.5
            ).move_to(LEFT * 3)
            
            # Eulerian view (right side)
            eulerian_title = Text("Eulerian View", font_size=36).move_to(RIGHT * 3 + UP * 2)
            control_volume = Square(side_length=3, fill_opacity=0.1).move_to(RIGHT * 3)
            
            # Show both views
            self.play(
                Create(line),
                Write(lagrangian_title),
                Write(eulerian_title),
                Create(control_volume),
                *[Create(p) for p in lagrangian_particles]
            )
            
            # Animate Lagrangian particles moving together
            self.play(
                lagrangian_particles.animate.shift(DOWN + RIGHT),
                run_time=2
            )

        # Scene 2: Core Formula and Derivation
        with self.voiceover(
            text="Here's the RTT equation. Let's dissect it: First, we have the total "
            "rate of change of a property in your fluid system. Then, how much accumulates "
            "inside your fixed control volume. Finally, what's carried in or out by flow "
            "across the volume's surface. RTT stitches these together!"
        ) as tracker:
            # Clear previous scene
            self.play(
                *[FadeOut(mob) for mob in self.mobjects]
            )

            # Create the equation components using LaTeX
            eq_system = MathTex(r"\frac{DB_{sys}}{Dt}", color=RED)
            eq_equals = MathTex("=")
            eq_accum = MathTex(r"\frac{\partial}{\partial t}\int_{CV} \beta\rho \,dV", color=BLUE)
            eq_plus = MathTex("+")
            eq_flux = MathTex(r"\int_{CS} \beta\rho(\vec{v}\cdot\vec{n}) \,dA", color=GREEN)

            # Arrange equation components
            equation = VGroup(eq_system, eq_equals, eq_accum, eq_plus, eq_flux)\
                .arrange(RIGHT, buff=0.2)\
                .scale(0.8)

            # Add labels
            labels = VGroup(
                Text("System Change", color=RED, font_size=24),
                Text("Accumulation", color=BLUE, font_size=24),
                Text("Net Flux", color=GREEN, font_size=24)
            )

            # Position labels above their respective terms
            labels[0].next_to(eq_system, UP, buff=0.5)
            labels[1].next_to(eq_accum, UP, buff=0.5)
            labels[2].next_to(eq_flux, UP, buff=0.5)

            # Animate equation appearance
            self.play(Write(equation))
            self.play(Write(labels))

            # Create visual aids for the terms
            cv_box = Square(side_length=2, fill_opacity=0.1)
            arrows_in = [
                Arrow(
                    start=cv_box.get_corner(UL) + LEFT,
                    end=cv_box.get_corner(UL),
                    color=GREEN
                ),
                Arrow(
                    start=cv_box.get_corner(DL) + LEFT,
                    end=cv_box.get_corner(DL),
                    color=GREEN
                )
            ]
            arrows_out = [
                Arrow(
                    start=cv_box.get_corner(UR),
                    end=cv_box.get_corner(UR) + RIGHT,
                    color=RED
                ),
                Arrow(
                    start=cv_box.get_corner(DR),
                    end=cv_box.get_corner(DR) + RIGHT,
                    color=RED
                )
            ]

            # Create simplified version
            simple_eq = MathTex(
                r"\text{System Change}", 
                "=", 
                r"\text{Accumulation}", 
                "+", 
                r"\text{Net Outflow}"
            ).scale(0.8)

            # Transition to simplified equation
            self.wait()
            self.play(
                FadeOut(equation),
                FadeOut(labels),
                FadeIn(simple_eq.to_edge(UP)),
                Create(cv_box)
            )

            # Animate arrows
            self.play(
                *[GrowArrow(arrow) for arrow in arrows_in + arrows_out],
                run_time=2
            )

            # Animate arrows pulsing to show flow
            self.play(
                *[
                    arrow.animate.set_opacity(0.5)
                    for arrow in arrows_in + arrows_out
                ],
                rate_func=there_and_back,
                run_time=2,
                repeat=2
            )

        # Scene 3: Fish Tank Analogy
        with self.voiceover(
            text="Imagine tracking dye in a fish tank: The dye concentration changes "
            "inside the tank over time through accumulation. Meanwhile, dye enters via "
            "the hose and exits through the drain. RTT? It's your math tool to predict "
            "the total dye change by combining these two effects!"
        ) as tracker:
            # Clear previous scene
            self.play(
                *[FadeOut(mob) for mob in self.mobjects]
            )

            # Create fish tank
            tank = VGroup(
                # Main tank rectangle
                Rectangle(height=4, width=5, fill_opacity=0.1, fill_color=BLUE_E),
                # Water surface
                Line(LEFT*2.5 + UP*1.8, RIGHT*2.5 + UP*1.8, color=BLUE),
            )

            # Create inlet hose
            inlet = VGroup(
                # Hose
                Rectangle(height=0.3, width=1.5, fill_opacity=1, color=GRAY),
                # Flow direction arrow
                Arrow(LEFT*0.5, RIGHT*0.5, color=RED).move_to(UP*1.5)
            ).move_to(tank.get_top() + UP*0.5 + LEFT*1.5)

            # Create drain
            drain = VGroup(
                # Drain hole
                Circle(radius=0.2, color=GRAY),
                # Flow direction arrow
                Arrow(UP*0.5, DOWN*0.5, color=RED)
            ).move_to(tank.get_bottom() + DOWN*0.5)

            # Create dye particles (dots)
            n_particles = 20
            dye_particles = VGroup(*[
                Dot(color=RED, radius=0.05) 
                for _ in range(n_particles)
            ])

            # Position particles randomly in upper part of tank
            for particle in dye_particles:
                particle.move_to(np.array([
                    np.random.uniform(-2, 2),  # x position
                    np.random.uniform(0, 1.5),  # y position
                    0
                ]))

            # Create labels
            title = Text("Fish Tank Analogy", font_size=36).to_edge(UP)
            labels = VGroup(
                Text("Inflow", font_size=24, color=RED).next_to(inlet, LEFT),
                Text("Outflow", font_size=24, color=RED).next_to(drain, DOWN),
                Text("Control Volume", font_size=24).next_to(tank, RIGHT)
            )

            # Initial animation
            self.play(
                Create(tank),
                Create(inlet),
                Create(drain),
                Write(title),
                Write(labels)
            )

            # Add dye particles
            self.play(Create(dye_particles))

            # Animate dye spreading and flowing
            def particle_movement(particle):
                # Random movement with downward bias
                dx = np.random.uniform(-0.5, 0.5)
                dy = np.random.uniform(-1, 0.2)
                return particle.animate.shift(RIGHT*dx + UP*dy)

            # First movement animation
            self.play(
                *[particle_movement(p) for p in dye_particles],
                run_time=2
            )

            # Add new particles from inlet
            new_particles = VGroup(*[
                Dot(color=RED, radius=0.05).move_to(
                    inlet.get_bottom() + DOWN*0.1 + RIGHT*np.random.uniform(-0.2, 0.2)
                )
                for _ in range(5)
            ])

            # Second movement animation with new particles
            self.play(
                FadeIn(new_particles),
                *[particle_movement(p) for p in dye_particles],
                *[particle_movement(p) for p in new_particles],
                run_time=2
            )

            # Remove particles near drain
            drain_particles = VGroup(*[
                p for p in dye_particles + new_particles
                if np.linalg.norm(p.get_center() - drain.get_center()) < 0.5
            ])
            
            self.play(
                FadeOut(drain_particles),
                *[particle_movement(p) for p in dye_particles + new_particles
                  if p not in drain_particles],
                run_time=2
            )

            # Add RTT equation reminder
            rtt_reminder = MathTex(
                r"\frac{DB_{sys}}{Dt}", "=",
                r"\underbrace{\frac{\partial}{\partial t}\int_{CV} \beta\rho \,dV}_{\text{Dye accumulation}}",
                "+",
                r"\underbrace{\int_{CS} \beta\rho(\vec{v}\cdot\vec{n}) \,dA}_{\text{Dye flow in/out}}"
            ).scale(0.6).to_edge(DOWN)

            self.play(Write(rtt_reminder))

        # Scene 4: Pipe Bend Example
        with self.voiceover(
            text="Let's compute the force on this pipe bend using RTT. First, we'll "
            "define our control volume enclosing the bend. Then we'll apply RTT to "
            "momentum, where beta equals velocity. For steady flow, the accumulation "
            "term becomes zero, and the forces come purely from the momentum flux!"
        ) as tracker:
            # Clear previous scene
            self.play(
                *[FadeOut(mob) for mob in self.mobjects]
            )

            # Create pipe bend using arcs and lines
            inlet_pipe = Rectangle(height=0.8, width=2, fill_opacity=1, fill_color=BLUE_E)
            
            # Create the bend using Arc
            bend = ArcBetweenPoints(
                start=inlet_pipe.get_right(),
                end=inlet_pipe.get_right() + DOWN*2,
                angle=-PI/2
            )
            
            outlet_pipe = Rectangle(height=2, width=0.8, fill_opacity=1, fill_color=BLUE_E)\
                .next_to(bend.get_end(), DOWN, buff=0)

            # Group pipe components
            pipe = VGroup(inlet_pipe, bend, outlet_pipe)
            
            # Create control volume (dashed rectangle around bend)
            cv = DashedVMobject(
                Rectangle(
                    height=3.5,
                    width=2.5,
                    color=RED
                )
            ).move_to(pipe)

            # Create velocity vectors
            v1 = Arrow(
                LEFT, RIGHT, 
                color=YELLOW,
                max_tip_length_to_length_ratio=0.15
            ).next_to(inlet_pipe.get_left(), LEFT)
            v1_label = MathTex(r"\vec{v}_1", color=YELLOW).next_to(v1, UP)

            v2 = Arrow(
                UP, DOWN,
                color=YELLOW,
                max_tip_length_to_length_ratio=0.15
            ).next_to(outlet_pipe.get_bottom(), DOWN)
            v2_label = MathTex(r"\vec{v}_2", color=YELLOW).next_to(v2, RIGHT)

            # Create force vectors
            f1 = Arrow(
                RIGHT, LEFT,
                color=RED,
                max_tip_length_to_length_ratio=0.15
            ).next_to(inlet_pipe.get_left(), LEFT, buff=1)
            f1_label = MathTex(r"\vec{F}_1", color=RED).next_to(f1, UP)

            f2 = Arrow(
                DOWN, UP,
                color=RED,
                max_tip_length_to_length_ratio=0.15
            ).next_to(outlet_pipe.get_bottom(), DOWN, buff=1)
            f2_label = MathTex(r"\vec{F}_2", color=RED).next_to(f2, RIGHT)

            # Create title and RTT momentum equation
            title = Text("Pipe Bend Example", font_size=36).to_edge(UP)
            
            momentum_rtt = MathTex(
                r"\sum \vec{F}", "=",
                r"\frac{\partial}{\partial t}\int_{CV} \vec{v}\rho \,dV",
                "+",
                r"\int_{CS} \vec{v}\rho(\vec{v}\cdot\vec{n}) \,dA"
            ).scale(0.8).next_to(title, DOWN)

            steady_flow = MathTex(
                r"\text{Steady Flow: }", 
                r"\frac{\partial}{\partial t}\int_{CV} \vec{v}\rho \,dV = 0"
            ).scale(0.7).next_to(momentum_rtt, DOWN)

            # Initial scene setup
            self.play(
                Write(title),
                Create(pipe)
            )

            # Add control volume
            self.play(Create(cv))

            # Add velocity vectors
            self.play(
                GrowArrow(v1),
                Write(v1_label),
                GrowArrow(v2),
                Write(v2_label)
            )

            # Show RTT equation
            self.play(Write(momentum_rtt))
            self.play(Write(steady_flow))

            # Add force vectors
            self.play(
                GrowArrow(f1),
                Write(f1_label),
                GrowArrow(f2),
                Write(f2_label)
            )

            # Create flowing particles to show fluid motion
            particles = VGroup(*[
                Dot(radius=0.05, color=WHITE)
                for _ in range(10)
            ])

            # Function to create particle path
            def create_particle_path():
                path = VMobject()
                path.set_points_smoothly([
                    inlet_pipe.get_left(),
                    inlet_pipe.get_right(),
                    outlet_pipe.get_top(),
                    outlet_pipe.get_bottom()
                ])
                return path

            # Animate particles along the pipe
            for particle in particles:
                path = create_particle_path()
                particle.move_to(path.get_start())
                self.add(particle)
                self.play(
                    MoveAlongPath(particle, path),
                    run_time=1.5,
                    rate_func=linear
                )
                self.remove(particle)

            # Final result
            result = MathTex(
                r"\sum \vec{F}", "=",
                r"\dot{m}(\vec{v}_2 - \vec{v}_1)"
            ).scale(0.8).next_to(steady_flow, DOWN, buff=0.5)

            self.play(Write(result))

        # Scene 5: Real-World Applications
        with self.voiceover(
            text="Where is RTT used? Everywhere! In rocket engines, thrust comes from "
            "momentum flux out the nozzle. Wind turbines harness angular momentum flux "
            "for power. And in medicine, RTT helps model blood flow dynamics. Master RTT, "
            "and you'll see fluids in a whole new light!"
        ) as tracker:
            # Clear previous scene
            self.play(
                *[FadeOut(mob) for mob in self.mobjects]
            )

            # Create title
            title = Text("Real-World Applications", font_size=36).to_edge(UP)
            self.play(Write(title))

            # Create three columns for applications
            def create_rocket():
                body = Rectangle(height=2, width=0.8, fill_opacity=1, color=GRAY)
                nozzle = Triangle(fill_opacity=1, color=GRAY).scale(0.4)\
                    .next_to(body, DOWN, buff=0)
                flames = VGroup(*[
                    Triangle(fill_opacity=0.8, color=RED_A)
                    .scale(0.3)
                    .rotate(PI)
                    for _ in range(3)
                ]).arrange(RIGHT, buff=-0.2)\
                    .next_to(nozzle, DOWN)
                return VGroup(body, nozzle, flames)

            def create_wind_turbine():
                tower = Rectangle(height=3, width=0.3, fill_opacity=1, color=GRAY)
                hub = Circle(radius=0.2, fill_opacity=1, color=GRAY)
                blades = VGroup(*[
                    Rectangle(height=0.2, width=1.5, fill_opacity=1, color=BLUE_E)
                    .rotate(angle)
                    for angle in [0, 2*PI/3, 4*PI/3]
                ])
                hub.move_to(tower.get_top())
                blades.move_to(hub.get_center())
                return VGroup(tower, hub, blades)

            def create_artery():
                # Create a path for the artery
                path = VMobject()
                path.set_points_smoothly([
                    ORIGIN, 
                    RIGHT, 
                    RIGHT + UP, 
                    RIGHT * 2 + UP
                ])

                # Create the artery walls
                artery_wall = VMobject()
                upper_wall = []
                lower_wall = []

                for alpha in np.linspace(0, 1, 20):
                    point = path.point_from_proportion(alpha)
                    # Get direction along the path
                    if alpha + 0.01 <= 1:
                        next_point = path.point_from_proportion(alpha + 0.01)
                        direction = next_point - point
                    else:
                        prev_point = path.point_from_proportion(alpha - 0.01)
                        direction = point - prev_point
                    
                    # Compute normal direction
                    normal = np.array([-direction[1], direction[0], 0])
                    normal = normal / np.linalg.norm(normal) * 0.2
                    
                    # Store upper and lower points
                    upper_wall.append(point + normal)
                    lower_wall.append(point - normal)

                # Create the artery wall path
                artery_wall.set_points_smoothly(upper_wall + lower_wall[::-1])

                artery_wall.set_stroke(color=RED, width=2)

                return VGroup(path, artery_wall)

            # Create application examples
            rocket = create_rocket().scale(0.8)
            turbine = create_wind_turbine().scale(0.8)
            artery = create_artery().scale(0.8)

            # Create labels and equations
            rocket_label = Text("Rocket Engines", font_size=24)
            turbine_label = Text("Wind Turbines", font_size=24)
            artery_label = Text("Blood Flow", font_size=24)

            rocket_eq = MathTex(r"F_{thrust} = \dot{m}v_{exit}").scale(0.7)
            turbine_eq = MathTex(r"\tau = \frac{d}{dt}(I\omega)").scale(0.7)
            flow_eq = MathTex(r"\dot{Q} = \frac{\partial V}{\partial t}").scale(0.7)

            # Create application groups
            apps = VGroup(
                VGroup(rocket, rocket_label, rocket_eq),
                VGroup(turbine, turbine_label, turbine_eq),
                VGroup(artery, artery_label, flow_eq)
            ).arrange(RIGHT, buff=1.5).next_to(title, DOWN, buff=0.8)

            # Animate each application
            for i, (app, label, eq) in enumerate(apps):
                self.play(
                    Create(app),
                    Write(label.next_to(app, DOWN)),
                    Write(eq.next_to(label, DOWN))
                )

                # Add specific animations for each application
                if i == 0:  # Rocket
                    self.play(
                        FadeIn(app[2]),  # Animate flames
                        rate_func=there_and_back,
                        run_time=1
                    )
                elif i == 1:  # Wind turbine
                    # Fix: Access the blades directly from the turbine object
                    blades = app[2]  # turbine[blades]
                    self.play(
                        Rotate(blades, angle=PI),  # Rotate blades
                        run_time=2
                    )
                else:  # Blood flow
                    artery_path = app[0]  # Get the path component
                    blood_cells = VGroup(*[
                        Dot(color=RED, radius=0.05)
                        for _ in range(5)
                    ])
                    
                    for cell in blood_cells:
                        cell.move_to(artery_path.get_start())
                        self.add(cell)
                        self.play(
                            MoveAlongPath(cell, artery_path),
                            run_time=1,
                            rate_func=linear
                        )
                        self.remove(cell)
            # Create summary box
            summary = VGroup(
                Text("RTT Applications:", font_size=24),
                Text("• Thrust Calculation", font_size=20),
                Text("• Power Generation", font_size=20),
                Text("• Biomedical Flow", font_size=20)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

            # Fade out applications and center summary
            self.play(
                FadeOut(apps)            )
            
            # Center and animate summary
            summary.move_to(ORIGIN)
            self.play(
                Write(summary),
                run_time=2
            )

            # Create separator and continue with the rest of the scene
            separator = Line(LEFT*6, RIGHT*6, color=GRAY)\
                .next_to(summary, DOWN, buff=1)

        # Scene 6: Recap and Call-to-Action
        with self.voiceover(
            text="Remember the Material Derivative? It tracks changes for a single "
            "particle. RTT scales this up to entire systems—tying particles to control "
            "volumes. Fluid mechanics just got simpler! Smash that like button if RTT "
        ) as tracker:
            # Clear previous scene
            self.play(
                *[FadeOut(mob) for mob in self.mobjects]
            )

            # Create comparison between Material Derivative and RTT
            title = Text("Material Derivative vs. RTT", font_size=36).to_edge(UP)

            # Material Derivative side
            material_title = Text("Material Derivative", font_size=28, color=BLUE)
            material_eq = MathTex(
                r"\frac{D\phi}{Dt} = \frac{\partial \phi}{\partial t} + \vec{v} \cdot \nabla\phi"
            ).scale(0.6)
            material_desc = Text("Single Particle", font_size=24)
            
            material_group = VGroup(material_title, material_eq, material_desc)\
                .arrange(DOWN, buff=0.5)\
                .to_edge(LEFT*1.5, buff=1)\
            # RTT side
            rtt_title = Text("Reynolds Transport", font_size=28, color=GREEN)
            rtt_eq = MathTex(
                r"\frac{DB_{sys}}{Dt} = \frac{\partial}{\partial t}\int_{CV} \beta\rho \,dV + \int_{CS} \beta\rho(\vec{v}\cdot\vec{n}) \,dA"
            ).scale(0.6)
            rtt_desc = Text("Entire System", font_size=24)
            
            rtt_group = VGroup(rtt_title, rtt_eq, rtt_desc)\
                .arrange(DOWN, buff=0.5)\
                .to_edge(RIGHT*1.5, buff=1)\

            # Create single particle visualization
            particle = Dot(color=BLUE)
            arrow = Arrow(LEFT, RIGHT, color=BLUE)
            single_particle = VGroup(particle, arrow)\
                .next_to(material_desc, DOWN)
            # Create system visualization
            cv = Square(side_length=2, color=GREEN)
            particles = VGroup(*[
                Dot(color=GREEN).move_to(
                    np.array([
                        np.random.uniform(-0.8, 0.8),
                        np.random.uniform(-0.8, 0.8),
                        0
                    ])
                )
                for _ in range(10)
            ])
            system = VGroup(cv, particles)\
                .next_to(rtt_desc, DOWN)

            # Animate comparison
            self.play(Write(title))
            self.play(
                Write(material_group),
                Write(rtt_group)
            )
            self.play(
                Create(single_particle),
                Create(system)
            )

            # Animate particle movement
            self.play(
                particle.animate.shift(RIGHT*2),
                *[p.animate.shift(RIGHT*0.5 + UP*0.3) for p in particles],
                run_time=2
            )
            # Final pause
            self.wait(2)
