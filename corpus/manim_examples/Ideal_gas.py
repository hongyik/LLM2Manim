from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class IdealGas(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections in sequence with smooth transitions
        self.section0()
        self.section1()  # Introduction to Gas Particles
        self.clear()
        
        self.section2()  # Understanding Gas Variables
        self.clear()
        
        self.section3()  # The Ideal Gas Law
        self.clear()
        
        self.section5()  # Key Assumptions
        self.clear()
        
        self.section11()  # bigpicture
        self.clear()
    def section0(self):
            # Create persistent equations group for upper left corner
            persistent_eq1 = MathTex("PV = nR_uT", font_size=24).set_color(YELLOW)
            persistent_eq2 = MathTex("\\frac{PV}{NT} = k_b", font_size=24)
            eq = VGroup(persistent_eq1, persistent_eq2).arrange(DOWN, buff=0.3)
            eq.to_corner(UR, buff=0.5)
            
            self.play(
                FadeIn(eq)
            )
    def section1(self):
        # Create the container box
        box = Cube(side_length=4)
        box.set_stroke(WHITE, 2)
        box.set_fill(BLUE_E, opacity=0.2)
        
        # Create particles with initial velocities
        num_particles = 20
        particles = VGroup()
        particle_velocities = []  # Store velocities for each particle
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.1)
            particle.set_fill(YELLOW, opacity=0.8)
            # Random initial position within the box
            x = np.random.uniform(-1.8, 1.8)
            y = np.random.uniform(-1.8, 1.8)  # Allow full height movement
            z = np.random.uniform(-1.8, 1.8)
            particle.move_to([x, y, z])
            particles.add(particle)
            
            # Initialize with random velocity (constant speed)
            speed = 0.15
            theta = np.random.uniform(0, 2 * np.pi)  # Random direction in x-y plane
            phi = np.random.uniform(0, np.pi)  # Random direction in z
            vx = speed * np.sin(phi) * np.cos(theta)
            vy = speed * np.sin(phi) * np.sin(theta)
            vz = speed * np.cos(phi)
            particle_velocities.append(np.array([vx, vy, vz]))
        
        # Create text
        title = Text("Gases are made of tiny particles in constant motion", font_size=24)
        title.to_edge(UP)
        
        # Animation sequence
        with self.voiceover(
            "Let's begin with a gas — one of the fundamental states of matter."
        ):
            self.play(Create(box))
            self.wait()
            
        with self.voiceover(
            "Unlike solids or liquids, the particles in a gas are far apart and move freely."
        ):
            self.play(FadeIn(particles))
            self.wait()
            
        with self.voiceover(
            "They're constantly moving in straight lines until they collide with walls or each other — each following Newton's laws of motion."
        ):
            # Animate particles with proper physics
            for _ in range(50):
                for i, particle in enumerate(particles):
                    # Get current position and velocity
                    pos = particle.get_center()
                    vel = particle_velocities[i]
                    
                    # Update position based on velocity
                    new_pos = pos + vel
                    
                    # Check for collisions with walls
                    # X-axis collision
                    if abs(new_pos[0]) > 1.8:
                        vel[0] = -vel[0]  # Reverse x velocity
                        new_pos[0] = np.sign(new_pos[0]) * 1.8
                    
                    # Y-axis collision
                    if abs(new_pos[1]) > 1.8:
                        vel[1] = -vel[1]  # Reverse y velocity
                        new_pos[1] = np.sign(new_pos[1]) * 1.8
                    
                    # Z-axis collision
                    if abs(new_pos[2]) > 1.8:
                        vel[2] = -vel[2]  # Reverse z velocity
                        new_pos[2] = np.sign(new_pos[2]) * 1.8
                    
                    # Update particle position and velocity
                    particle.move_to(new_pos)
                    particle_velocities[i] = vel
                
                self.wait(0.1)
            
        with self.voiceover(
            "To describe how gases behave, we need to track a few important variables. Let's explore each one and see how they work together..."
        ):
            # Create variable labels with explanations
            variables = VGroup(
                Text("P: Pressure", font_size=24),
                Text("V: Volume", font_size=24),
                Text("T: Temperature", font_size=24),
                Text("n: Number of moles", font_size=24)
            )
            variables.arrange(RIGHT, buff=1)
            variables.to_edge(DOWN)
            
            # Fade out particles and show variables with a smooth transition
            self.play(
                FadeOut(particles, run_time=1.5),
                FadeIn(variables, run_time=1.5)
            )
            
            # Add anticipatory animation for next section
            self.play(
                variables.animate.scale(1.2).set_color(YELLOW),
                run_time=1
            )
            self.wait(1)
            self.play(
                variables.animate.scale(1/1.2).set_color(WHITE),
                run_time=1
            )
            self.wait(1)

    def section2(self):
        # Create title and subtitle
        title = Text("Gas Variables in Motion: A Guided Tour Through the Gas Laws", font_size=36)
        subtitle = Text("Understanding how pressure, volume, temperature, and moles work together", font_size=24)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        
        # Create the main container
        container = Cube(side_length=3)
        container.set_stroke(WHITE, 2)
        container.set_fill(BLUE_E, opacity=0.2)
        
        # Create movable board/piston as a rectangle (plane)
        board = Rectangle(width=3, height=0.05)  # Width matches container width, small height for piston thickness
        board.set_stroke(WHITE, 2)
        board.set_fill(GRAY, opacity=0.8)  # Add fill to make it look more solid
        board.move_to(container.get_center())
        
        # Create variable axes with specific values
        axes_group = VGroup()
        # Initial values: P=1 atm, V=2 L, T=300 K, n=0.081 mol (adjusted to match PV = nRT)
        initial_values = {
            "P": 1.0,  # atm
            "V": 2.0,  # L
            "T": 300,  # K
            "n": 0.081  # mol (adjusted to match PV = nRT)
        }
        
        # Create axes for each variable
        for var, unit, range_info in [
            ("P", "atm", (0, 5, 1)),  # Pressure: 0-5 atm
            ("V", "L", (0, 5, 1)),    # Volume: 0-5 L
            ("T", "K", (0, 1500, 300)), # Temperature: 0-1500 K
            ("n", "mol", (0, 0.3, 0.05))  # Moles: 0-0.3 mol
        ]:
            # Create number line
            number_line = NumberLine(
                x_range=range_info,
                include_numbers=True,
                numbers_with_elongated_ticks=range_info[0::2],
                decimal_number_config={"num_decimal_places": 2},
                length=4,
                font_size=12
            )
            
            # Add label
            label = Text(f"{var} ({unit})", font_size=16)
            label.next_to(number_line, UP)
            
            # Add current value dot
            dot = Dot(color=YELLOW, radius=0.05)
            dot.move_to(number_line.n2p(initial_values[var]))
            
            # Add current value text
            value_text = Text(f"{initial_values[var]:.3f}", font_size=16)
            value_text.next_to(dot, UP, buff=0.1)
            
            # Group everything
            axis_group = VGroup(number_line, label, dot, value_text)
            axes_group.add(axis_group)
        
        axes_group.arrange(DOWN, buff=0.5)
        axes_group.to_edge(RIGHT)
        
        # Create particles based on initial values
        particles = VGroup()
        particle_velocities = []  # Store velocities for each particle
        num_particles = int(initial_values["n"] * 6.022e23 / 1e22)  # Reduced scaling factor
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.08)
            particle.set_fill(YELLOW, opacity=0.8)
            x = np.random.uniform(-1.4, 1.4)
            y = np.random.uniform(-1.4, 0.4)  # Keep below board
            z = np.random.uniform(-1.4, 1.4)
            particle.move_to([x, y, z])
            particles.add(particle)
            
            # Initialize with random velocity (constant speed)
            speed = 0.15
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            vx = speed * np.sin(phi) * np.cos(theta)
            vy = speed * np.sin(phi) * np.sin(theta)
            vz = speed * np.cos(phi)
            particle_velocities.append(np.array([vx, vy, vz]))

        # Create particle updater function
        def update_particles(particles, dt):
            bounds = 1.4
            y_upper_bound = board.get_center()[1] - 0.1
            
            for i, particle in enumerate(particles):
                pos = particle.get_center()
                vel = particle_velocities[i]
                new_pos = pos + vel
                
                # Check for collisions with walls and board
                if abs(new_pos[0]) > bounds:
                    vel[0] = -vel[0]
                    new_pos[0] = np.sign(new_pos[0]) * bounds
                
                if new_pos[1] > y_upper_bound:
                    vel[1] = -vel[1]
                    new_pos[1] = y_upper_bound
                elif new_pos[1] < -bounds:
                    vel[1] = -vel[1]
                    new_pos[1] = -bounds
                
                if abs(new_pos[2]) > bounds:
                    vel[2] = -vel[2]
                    new_pos[2] = np.sign(new_pos[2]) * bounds
                
                # Check for collisions with other particles
                for j, other_particle in enumerate(particles):
                    if i != j:
                        other_pos = other_particle.get_center()
                        distance = np.linalg.norm(new_pos - other_pos)
                        if distance < 0.16:  # Sum of particle radii
                            vel, particle_velocities[j] = particle_velocities[j], vel
                            new_pos = pos + vel
                
                particle.move_to(new_pos)
                particle_velocities[i] = vel

        # Create 2D axes for each gas law relationship
        # Boyle's Law axes (P vs V)
        boyle_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": True}
        )
        boyle_labels = boyle_axes.get_axis_labels(x_label="V (L)", y_label="P (atm)")
        boyle_group = VGroup(boyle_axes, boyle_labels)
        
        # Charles's Law axes (V vs T)
        charles_axes = Axes(
            x_range=[0, 1500, 300],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": True}
        )
        charles_labels = charles_axes.get_axis_labels(x_label="T (K)", y_label="V (L)")
        charles_group = VGroup(charles_axes, charles_labels)
        
        # Avogadro's Law axes (V vs n)
        avogadro_axes = Axes(
            x_range=[0, 0.3, 0.05],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": True}
        )
        avogadro_labels = avogadro_axes.get_axis_labels(x_label="n (mol)", y_label="V (L)")
        avogadro_group = VGroup(avogadro_axes, avogadro_labels)
        
        # Gay-Lussac's Law axes (P vs T)
        gay_lussac_axes = Axes(
            x_range=[0, 1500, 300],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": True}
        )
        gay_lussac_labels = gay_lussac_axes.get_axis_labels(x_label="T (K)", y_label="P (atm)")
        gay_lussac_group = VGroup(gay_lussac_axes, gay_lussac_labels)
        
        # Position for all graphs (left down corner)
        graph_position = DOWN * 2 + LEFT * 4
        
        # Scale all graphs
        for graph in [boyle_group, charles_group, avogadro_group, gay_lussac_group]:
            graph.scale(0.8)
            graph.move_to(graph_position)
        
        # Animation sequence
        with self.voiceover(
        """
        To understand how gases behave, we study four essential variables: 
        Pressure, the force gas particles exert when they collide with container walls. 
        Volume, the space the gas occupies. 
        Temperature, which reflects how fast the particles are moving — their kinetic energy. 
        And moles, which simply count how many gas particles we have.

        Each of these variables influences the others in predictable ways. 
        By changing one while holding others constant, we uncover the fundamental laws of gas behavior — the building blocks of the Ideal Gas Law.
        """        ):
            self.play(Write(title), Write(subtitle))
            self.play(Create(container), Create(board), Create(particles))
            self.play(Create(axes_group))
            self.play(FadeOut(title), FadeOut(subtitle))
            
            # Add particle updater
            particles.add_updater(update_particles)
            self.wait(3)
            
        # Boyle's Law demonstration
        with self.voiceover(
            """
            Let's begin with Boyle's Law — the relationship between pressure and volume.
            We'll hold temperature and gas amount constant. Now, we compress the gas by pushing the piston downward.

            As the available volume shrinks, gas particles collide with the walls more frequently, and with the same energy.
            This results in a rise in pressure.

            Boyle's Law tells us that pressure and volume are inversely proportional. When one goes up, the other goes down — always keeping their product constant.
            """        ):
            # Add Boyle's Law title and graph
            boyle_title = Text("Boyle's Law: P ∝ 1/V", font_size=24)
            boyle_title.to_corner(UP + LEFT)
            
            self.play(
                Write(boyle_title),
                FadeIn(boyle_group)
            )
            
            # Create Boyle's Law curve
            boyle_curve = boyle_axes.plot(
                lambda x: 2/x,
                x_range=[0.8, 4],
                color=YELLOW
            )
            
            # Update values for Boyle's Law
            new_values = {
                "P": 2.0,  # atm
                "V": 1.0,  # L
                "T": 300,  # K (unchanged)
                "n": 0.081   # mol (unchanged)
            }
            boyle_tex=MathTex(r"P_1V_1=P_2V_2")
            boyle_tex.next_to(boyle_curve,UP,buff=2)
            # Move board down to decrease volume
            self.play(
                board.animate.move_to(container.get_center() + DOWN * 0.65),  # Move board down
                axes_group[0][2].animate.move_to(axes_group[0][0].n2p(new_values["P"])),  # P increases
                axes_group[1][2].animate.move_to(axes_group[1][0].n2p(new_values["V"])),  # V decreases
                axes_group[0][3].animate.become(Text(f"{new_values['P']:.3f}", font_size=16).next_to(axes_group[0][2], UP, buff=0.1)),
                axes_group[1][3].animate.become(Text(f"{new_values['V']:.3f}", font_size=16).next_to(axes_group[1][2], UP, buff=0.1)),
                Create(boyle_curve),
                Create(boyle_tex),
                run_time=2
            )
            # Add flash effect for changed values
            self.play(
                Flash(axes_group[0][2], color=RED, line_length=0.2, flash_radius=0.3),
                Flash(axes_group[1][2], color=RED, line_length=0.2, flash_radius=0.3),
                axes_group[0][3].animate.set_color(RED),
                axes_group[1][3].animate.set_color(RED),
                run_time=0.5
            )
            self.play(
                axes_group[0][3].animate.set_color(WHITE),
                axes_group[1][3].animate.set_color(WHITE),
                run_time=0.5
            )
            self.wait(3)
            
        # Charles's Law demonstration
        with self.voiceover(
            """
            Now, we explore Charles's Law — the connection between temperature and volume, while keeping pressure constant.
            As we heat the gas, the particles begin to move faster — they carry more kinetic energy.
            To maintain the same pressure, the gas must expand, giving particles more room to move and reducing the frequency of wall collisions.

            Charles's Law shows that volume is directly proportional to temperature, as long as pressure and moles stay fixed.
            """        ):
            # Fade out Boyle's graph and show Charles's graph
            self.play(
                FadeOut(boyle_group),
                FadeOut(boyle_curve),
                FadeOut(boyle_title),
                FadeOut(boyle_tex)
            )
            
            charles_title = Text("Charles's Law: V ∝ T", font_size=24)
            charles_title.to_corner(UP + LEFT)
            
            self.play(
                Write(charles_title),
                FadeIn(charles_group)
            )
            
            # Create Charles's Law curve
            p_const = 2.0  # Constant pressure
            charles_curve = charles_axes.plot(
                lambda x: x/300,  # Linear relationship V = kT
                x_range=[0, 1200],
                color=BLUE
            )
            
            # Update values for Charles's Law
            new_values = {
                "P": 2.0,  # atm (unchanged)
                "V": 2.0,  # L (doubled)
                "T": 600,  # K (doubled to maintain P)
                "n": 0.081   # mol (unchanged)
            }
            charles_tex=MathTex(r"V_1/T_1=V_2/T_2")
            charles_tex.next_to(charles_curve,UP,buff=2)
            # Move board up to increase volume and increase particle speeds
            self.play(
                board.animate.move_to(container.get_center()),  # Move board up
                axes_group[1][2].animate.move_to(axes_group[1][0].n2p(new_values["V"])),  # V increases
                axes_group[2][2].animate.move_to(axes_group[2][0].n2p(new_values["T"])),  # T increases
                axes_group[1][3].animate.become(Text(f"{new_values['V']:.3f}", font_size=16).next_to(axes_group[1][2], UP, buff=0.1)),
                axes_group[2][3].animate.become(Text(f"{new_values['T']:.3f}", font_size=16).next_to(axes_group[2][2], UP, buff=0.1)),
                Create(charles_curve),
                Create(charles_tex),
                run_time=2
            )
            # Add flash effect for changed values
            self.play(
                Flash(axes_group[1][2], color=BLUE, line_length=0.2, flash_radius=0.3),
                Flash(axes_group[2][2], color=BLUE, line_length=0.2, flash_radius=0.3),
                axes_group[1][3].animate.set_color(BLUE),
                axes_group[2][3].animate.set_color(BLUE),
                run_time=0.5
            )
            self.play(
                axes_group[1][3].animate.set_color(WHITE),
                axes_group[2][3].animate.set_color(WHITE),
                run_time=0.5
            )
            
            # Increase particle speeds for higher temperature
            for vel in particle_velocities:
                vel *= 1.5  # Increase speed by 50%
            
            self.wait(3)
            
        # Avogadro's Law demonstration
        with self.voiceover(
            """
            Let's add more gas while keeping pressure and temperature constant — this is Avogadro's Law.
            
            As we introduce more particles into the system, the number of collisions with the walls would increase — unless the volume increases too.
            To maintain constant pressure, the volume expands, allowing particles to spread out.

            Avogadro's Law tells us that volume is directly proportional to the number of moles — or in simpler terms, more gas means more space is needed.
            """
        ):
            # Fade out Charles's graph and show Avogadro's graph
            self.play(
                FadeOut(charles_group),
                FadeOut(charles_curve),
                FadeOut(charles_title),
                FadeOut(charles_tex)
            )
            
            avogadro_title = Text("Avogadro's Law: V ∝ n", font_size=24)
            avogadro_title.to_corner(UP + LEFT)
            
            self.play(
                Write(avogadro_title),
                FadeIn(avogadro_group)
            )
            
            # Create Avogadro's Law curve
            avogadro_curve = avogadro_axes.plot(
                lambda x: 10*x,  # Linear relationship V = kn
                x_range=[0, 0.3],
                color=PURPLE
            )
            # Update values for Avogadro's Law
            new_values = {
                "P": 2.0,  # atm (unchanged)
                "V": 4.0,  # L (doubled)
                "T": 600,  # K (unchanged)
                "n": 0.162   # mol (doubled)
            }
            avogadro_tex=MathTex(r"V_1/n_1=V_2/n_2")
            avogadro_tex.next_to(avogadro_curve,UP,buff=2)
            # Add more particles
            for _ in range(num_particles):
                particle = Sphere(radius=0.08)
                particle.set_fill(YELLOW, opacity=0.8)
                x = np.random.uniform(-1.4, 1.4)
                y = np.random.uniform(-1.4, 0.4)  # Keep below board
                z = np.random.uniform(-1.4, 1.4)
                particle.move_to([x, y, z])
                particles.add(particle)
                
                # Initialize with random velocity
                speed = 0.15
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                vx = speed * np.sin(phi) * np.cos(theta)
                vy = speed * np.sin(phi) * np.sin(theta)
                vz = speed * np.cos(phi)
                particle_velocities.append(np.array([vx, vy, vz]))
            
            # Move board up to increase volume
            self.play(
                board.animate.move_to(container.get_top()),  # Move board up
                axes_group[1][2].animate.move_to(axes_group[1][0].n2p(new_values["V"])),  # V increases
                axes_group[3][2].animate.move_to(axes_group[3][0].n2p(new_values["n"])),  # n increases
                axes_group[1][3].animate.become(Text(f"{new_values['V']:.3f}", font_size=16).next_to(axes_group[1][2], UP, buff=0.1)),
                axes_group[3][3].animate.become(Text(f"{new_values['n']:.3f}", font_size=16).next_to(axes_group[3][2], UP, buff=0.1)),
                Create(avogadro_curve),
                Create(avogadro_tex),
                run_time=2
            )
            
            # Add flash effect for changed values
            self.play(
                #FadeOut(board),
                Flash(axes_group[1][2], color=PURPLE, line_length=0.2, flash_radius=0.3),
                Flash(axes_group[3][2], color=PURPLE, line_length=0.2, flash_radius=0.3),
                axes_group[1][3].animate.set_color(PURPLE),
                axes_group[3][3].animate.set_color(PURPLE),
                run_time=0.5
            )
            self.play(
                axes_group[1][3].animate.set_color(WHITE),
                axes_group[3][3].animate.set_color(WHITE),
                run_time=0.5
            )
            
            self.wait(3)
            
        # Gay-Lussac's Law demonstration
        with self.voiceover(
            """
            Finally, we look at Gay-Lussac's Law — the link between pressure and temperature, with volume and moles held constant.

            When we heat a gas in a rigid container, the particles move faster but don't have more space.
            This means they strike the container walls more often and with greater force — raising the pressure.

            Gay-Lussac's Law tells us that pressure increases directly with temperature when volume stays fixed.
            This is exactly why pressure builds in a sealed can left in the sun.
            """        ):
            # Fade out Avogadro's graph and show Gay-Lussac's graph
            self.play(
                FadeOut(avogadro_group),
                FadeOut(avogadro_curve),
                FadeOut(avogadro_title),
                FadeOut(avogadro_tex)
            )
            
            gay_lussac_title = Text("Gay-Lussac's Law: P ∝ T", font_size=24)
            gay_lussac_title.to_corner(UP + LEFT)
            
            self.play(
                Write(gay_lussac_title),
                FadeIn(gay_lussac_group)
            )
            
            # Create Gay-Lussac's Law curve
            v_const = 4.0  # Constant volume
            gay_lussac_curve = gay_lussac_axes.plot(
                lambda x: x/300,  # Linear relationship P = kT
                x_range=[0, 1200],
                color=GREEN
            )
            
            # Update values for Gay-Lussac's Law
            new_values = {
                "P": 4.0,  # atm (doubled)
                "V": 4.0,  # L (unchanged)
                "T": 1200,  # K (doubled)
                "n": 0.162   # mol (unchanged)
            }
            gay_lussac_tex=MathTex(r"P_1/T_1=P_2/T_2")
            gay_lussac_tex.next_to(gay_lussac_curve,UP,buff=2)
            # Increase temperature and pressure
            self.play(
                axes_group[0][2].animate.move_to(axes_group[0][0].n2p(new_values["P"])),  # P increases
                axes_group[2][2].animate.move_to(axes_group[2][0].n2p(new_values["T"])),  # T increases
                axes_group[0][3].animate.become(Text(f"{new_values['P']:.3f}", font_size=16).next_to(axes_group[0][2], UP, buff=0.1)),
                axes_group[2][3].animate.become(Text(f"{new_values['T']:.3f}", font_size=16).next_to(axes_group[2][2], UP, buff=0.1)),
                Create(gay_lussac_curve),
                Create(gay_lussac_tex),
                run_time=2
            )
            # Add flash effect for changed values
            self.play(
                Flash(axes_group[0][2], color=YELLOW, line_length=0.2, flash_radius=0.3),
                Flash(axes_group[2][2], color=YELLOW, line_length=0.2, flash_radius=0.3),
                axes_group[0][3].animate.set_color(YELLOW),
                axes_group[2][3].animate.set_color(YELLOW),
                run_time=0.5
            )
            self.play(
                axes_group[0][3].animate.set_color(WHITE),
                axes_group[2][3].animate.set_color(WHITE),
                run_time=0.5
            )
            
            # Increase particle speeds for higher temperature
            for vel in particle_velocities:
                vel *= 1.5  # Increase speed by 50%
            
            # At the end of the animation, fade out the last curve
            self.play(FadeOut(gay_lussac_curve),FadeOut(gay_lussac_tex))
            
        # Remove particle updater at the end
        particles.remove_updater(update_particles)
    def section3(self):
        # Create title and subtitle
        title = Text("From Particles to Moles: Deriving the Ideal Gas Law", font_size=36)
        subtitle = Text("How microscopic motion becomes a macroscopic law", font_size=24)
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        
        # Create whiteboard background
        board = Rectangle(height=6, width=10)
        board.set_fill(WHITE, opacity=0.1)
        board.set_stroke(WHITE, 2)
        
        # Animation sequence
        with self.voiceover(
            "Let's begin at the molecular level. Gas particles are constantly in motion, bouncing around and colliding with the walls of their container. Each collision exerts a tiny force, and when you add up all these microscopic impacts, they result in the pressure we observe on a macroscopic scale."
        ):
            self.play(Write(title), Write(subtitle))
            self.play(Create(board))
            
            # Create particle visualization
            particles = VGroup()
            particle_velocities = []  # Store velocities for each particle
            num_particles = 5  # Reduced from 20
            
            for _ in range(num_particles):
                particle = Sphere(radius=0.08)
                particle.set_fill(YELLOW, opacity=0.8)
                x = np.random.uniform(-1.4, 1.4)
                y = np.random.uniform(-1.4, 1.4)
                z = np.random.uniform(-1.4, 1.4)
                particle.move_to([x, y, z])
                particles.add(particle)
                
                # Initialize with random velocity (constant speed)
                speed = 0.15
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                vx = speed * np.sin(phi) * np.cos(theta)
                vy = speed * np.sin(phi) * np.sin(theta)
                vz = speed * np.cos(phi)
                particle_velocities.append(np.array([vx, vy, vz]))
            
            # Create container
            container = Cube(side_length=3)
            container.set_stroke(WHITE, 2)
            container.set_fill(BLUE_E, opacity=0.2)
            
            self.play(Create(container), Create(particles))
            
            # Create particle updater function
            def update_particles(particles, dt):
                bounds = 1.4
                for i, particle in enumerate(particles):
                    pos = particle.get_center()
                    vel = particle_velocities[i]
                    new_pos = pos + vel
                    
                    # Check for collisions with walls
                    if abs(new_pos[0]) > bounds:
                        vel[0] = -vel[0]  # Reverse x velocity
                        new_pos[0] = np.sign(new_pos[0]) * bounds
                    
                    if abs(new_pos[1]) > bounds:
                        vel[1] = -vel[1]  # Reverse y velocity
                        new_pos[1] = np.sign(new_pos[1]) * bounds
                    
                    if abs(new_pos[2]) > bounds:
                        vel[2] = -vel[2]  # Reverse z velocity
                        new_pos[2] = np.sign(new_pos[2]) * bounds
                    
                    particle.move_to(new_pos)
                    particle_velocities[i] = vel
            
            # Add particle updater
            particles.add_updater(update_particles)
            self.wait(2)
            
        with self.voiceover(
            "This microscopic behavior is described by the equation: pressure times volume equals capital N times k sub b times temperature. Here, N stands for the total number of gas particles, k sub b is Boltzmann's constant, and temperature reflects the average kinetic energy of the particles. This equation connects individual molecular motion to bulk properties like pressure and volume."
        ):
            # Show first equation
            eq1 = MathTex("PV = Nk_bT")
            eq1.scale(1.0)
            eq1.to_edge(LEFT, buff=1)
            
            # Add variable explanations using MathTex
            n_expl = MathTex("N: \\text{ number of molecules}", font_size=24)
            kb_expl = MathTex("k_b: \\text{ Boltzmann's constant} = 1.38 \\times 10^{-23} \\text{ J/K}", font_size=24)
            explanations1 = VGroup(n_expl, kb_expl)
            explanations1.arrange(DOWN, aligned_edge=LEFT)
            explanations1.next_to(eq1, DOWN, buff=0.3)
            
            self.play(Write(eq1))
            self.play(Write(explanations1))

            # Create transition to new board
            new_board = Rectangle(height=6, width=10)
            new_board.set_fill(WHITE, opacity=0.1)
            new_board.set_stroke(WHITE, 2)
            
            # Fade out old elements and create new board
            self.play(
                FadeOut(container),
                FadeOut(particles),
                FadeOut(title),
                FadeOut(subtitle),
                FadeOut(board),
                FadeIn(new_board)
            )
            self.clear()
            # Move equation to upper left of new board
            eq1.move_to(new_board.get_corner(UL) + RIGHT*2 + DOWN*1)
            explanations1.next_to(eq1, DOWN, buff=0.3)
            
            self.play(
                eq1.animate.move_to(new_board.get_corner(UL) + RIGHT*2 + DOWN*1),
                explanations1.animate.next_to(eq1, DOWN, buff=0.3)
            )
                
        with self.voiceover(
            "Instead of counting individual molecules, we usually group them into moles. Using Avogadro's number, we write capital N equals lowercase n times N sub A. Here, lowercase n is the number of moles, and N sub A is Avogadro's number — approximately six point zero two two times ten to the twenty-third particles per mole. This conversion allows us to go from counting molecules to using a more manageable unit."
        ):
            # Show Avogadro's number relationship
            avogadro = MathTex("N = nN_A")
            avogadro.scale(1.0)
            avogadro.next_to(explanations1, DOWN, buff=0.3)
            
            # Add explanation using MathTex
            na_expl = MathTex("N_A: \\text{ Avogadro's number} = 6.022 \\times 10^{23} \\text{ mol}^{-1}", font_size=24)
            na_expl.next_to(avogadro, DOWN, buff=0.3)
            
            self.play(Write(avogadro), Write(na_expl))
            
            # Show substitution step
            subst_step = MathTex("PV = (nN_A)k_bT")
            subst_step.scale(1.0)
            subst_step.next_to(na_expl, DOWN, buff=0.3)
            
            self.play(Write(subst_step))
            
        with self.voiceover(
            "Now, if we substitute n times N sub A into the earlier equation, we get: pressure times volume equals n times N sub A times k sub b times temperature. Since the product of Avogadro's number and Boltzmann's constant appears so frequently, we define it as a new constant: R sub u, the universal gas constant. So we arrive at the familiar form of the ideal gas law: pressure times volume equals n times R sub u times temperature."
        ):
            # Show universal gas constant definition
            ru_def = MathTex("R_u = N_Ak_b")
            ru_def.scale(1.0)
            ru_def.next_to(subst_step, DOWN, buff=0.3)
            
            # Add explanation using MathTex
            ru_expl = MathTex("R_u: \\text{ universal gas constant} = 8.314 \\text{ J/(mol·K)}", font_size=24)
            ru_expl.next_to(ru_def, DOWN, buff=0.3)
            
            self.play(Write(ru_def), Write(ru_expl))
            
            # Show final molar form
            eq3 = MathTex("PV = nR_uT")
            eq3.scale(1.0)
            eq3.to_edge(UR, buff=2)
            
            self.play(Write(eq3))
            
        with self.voiceover(
            "Sometimes, it's more practical to describe the gas by its mass instead of the number of moles.  Using the molar mass capital M, we can write: n equals lowercase m divided by capital M. Here, lowercase m is the total mass of the gas in kilograms, and capital M is the molar mass in kilograms per mole."
        ):
            # Show mass relationship
            mass_eq = MathTex("n = \\frac{m}{M}")
            mass_eq.scale(1.0)
            mass_eq.next_to(eq3, DOWN, buff=0.3)
            
            # Add explanations using MathTex
            m_expl = MathTex("m: \\text{ mass (kg)}", font_size=24)
            M_expl = MathTex("M: \\text{ molar mass (kg/mol)}", font_size=24)
            mass_expl = VGroup(m_expl, M_expl)
            mass_expl.arrange(DOWN, aligned_edge=LEFT)
            mass_expl.next_to(mass_eq, DOWN, buff=0.3)
            
            self.play(Write(mass_eq), Write(mass_expl))
            
            # Show substitution step
            subst_step2 = MathTex("PV = \\frac{m}{M}R_uT")
            subst_step2.scale(1.0)
            subst_step2.next_to(mass_expl, DOWN, buff=0.3)
            
            self.play(Write(subst_step2))
            
        with self.voiceover(
            "Substituting mass over molar mass into the ideal gas law, we get: pressure times volume equals lowercase m divided by capital M times R sub u times temperature. We define R, the specific gas constant, as R sub u divided by M. This constant is different for each gas and allows us to write the equation in a mass-based form: pressure times volume equals mass times R times temperature."
        ):
            # Show specific gas constant definition
            r_def = MathTex("R = \\frac{R_u}{M}")
            r_def.scale(1.0)
            r_def.next_to(subst_step2, DOWN, buff=0.3)
            
            # Add explanation using MathTex
            r_expl = MathTex("R: \\text{ specific gas constant (J/(kg·K))}", font_size=24)
            r_expl.next_to(r_def, DOWN, buff=0.3)
            
            self.play(Write(r_def), Write(r_expl))
            
            # Show final mass-based form
            eq5 = MathTex("PV = mRT")
            eq5.scale(1.0)
            eq5.next_to(r_expl, DOWN, buff=0.3)
            
            self.play(Write(eq5))
            
        with self.voiceover(
            "To go one step further, we introduce the concept of density, represented by the Greek letter rho.  Density is defined as mass divided by volume.  If we divide both sides of the equation by volume, we get: pressure equals rho times R times temperature.  This version is especially useful in engineering, where we often work with density rather than mass or moles."
        ):
            # Show density definition
            density_def = MathTex("\\rho = \\frac{m}{V}")
            density_def.scale(1.0)
            density_def.next_to(eq5, DOWN, buff=0.3)
            
            # Add explanation using MathTex
            rho_expl = MathTex("\\rho: \\text{ density (kg/m}^3\\text{)}", font_size=24)
            rho_expl.next_to(density_def, DOWN, buff=0.3)
            
            # Fade out left part and show density and specific volume forms
            self.play(
                FadeOut(eq1),
                FadeOut(explanations1),
                FadeOut(avogadro),
                FadeOut(na_expl),
                FadeOut(subst_step),
                FadeOut(ru_def),
                FadeOut(ru_expl),
                FadeOut(eq3),
                FadeOut(mass_eq),
                FadeOut(mass_expl),
                FadeOut(subst_step2),
                FadeOut(r_def),
                FadeOut(r_expl),
                FadeOut(eq5)
            )
            
            # Show density form
            density_eq = MathTex("P = \\rho RT")
            density_eq.scale(1.0)
            density_eq.to_edge(LEFT, buff=2)
            
            # Show specific volume form
            spec_vol_eq = MathTex("Pv = RT")
            spec_vol_eq.scale(1.0)
            spec_vol_eq.next_to(density_eq, RIGHT, buff=0.3)
            
            self.play(
                Write(density_def),
                Write(rho_expl),
                Write(density_eq),
                Write(spec_vol_eq)
            )
            
        with self.voiceover(
            "Finally, we can define specific volume, represented by lowercase v, as the inverse of density — that is, one divided by rho. Substituting this into the previous form, we get: pressure equals R times temperature divided by specific volume. Rewriting, we arrive at: pressure times specific volume equals R times temperature. This compact version is common in thermodynamics and fluid mechanics."
        ):
            # Show specific volume definition
            spec_vol_def = MathTex("v = \\frac{1}{\\rho}")
            spec_vol_def.scale(1.0)
            spec_vol_def.next_to(density_eq, DOWN, buff=0.3)
            
            # Add explanation using MathTex
            v_expl = MathTex("v: \\text{ specific volume (m}^3\\text{/kg)}", font_size=24)
            v_expl.next_to(spec_vol_def, RIGHT, buff=0.3)
            
            self.play(Write(spec_vol_def), Write(v_expl))
            
            # Show substitution step
            subst_step4 = MathTex("P = \\frac{1}{v}RT")
            subst_step4.scale(1.0)
            subst_step4.next_to(v_expl, DOWN, buff=0.3)
            
            # Show final specific volume form
            spec_vol_eq = MathTex("Pv = RT")
            spec_vol_eq.scale(1.0)
            spec_vol_eq.next_to(subst_step4, RIGHT, buff=0.3)
            
            self.play(Write(subst_step4), Write(spec_vol_eq))
            
            # Add summary table
        with self.voiceover(
                "Let's summarize all the different forms of the Ideal Gas Law and the important constants we've discussed."
            ):
                self.clear()
                # Create table title
                table_title = Text("Summary of Ideal Gas Law Forms", font_size=28)
                table_title.to_edge(UP, buff=0.5)
                
                # Create table headers
                headers = VGroup(
                    Text("Form", font_size=24),
                    Text("Equation", font_size=24),
                    Text("Variables", font_size=24)
                ).arrange(RIGHT, buff=1)
                headers.next_to(table_title, DOWN, buff=0.5)
                
                # Create table rows
                rows = VGroup(
                    # Molecular form
                    VGroup(
                        Text("Molecular", font_size=20),
                        MathTex("PV = Nk_bT", font_size=20),
                        Text("N: number of molecules", font_size=20)
                    ),
                    # Molar form
                    VGroup(
                        Text("Molar", font_size=20),
                        MathTex("PV = nR_uT", font_size=20),
                        Text("n: number of moles", font_size=20)
                    ),
                    # Mass-based form
                    VGroup(
                        Text("Mass-based", font_size=20),
                        MathTex("PV = mRT", font_size=20),
                        Text("m: mass (kg)", font_size=20)
                    ),
                    # Density form
                    VGroup(
                        Text("Density", font_size=20),
                        MathTex("P = \\rho RT", font_size=20),
                        Text("ρ: density (kg/m³)", font_size=20)
                    ),
                    # Specific volume form
                    VGroup(
                        Text("Specific volume", font_size=20),
                        MathTex("Pv = RT", font_size=20),
                        Text("v: specific volume (m³/kg)", font_size=20)
                    )
                )
                
                # Arrange rows vertically
                for i, row in enumerate(rows):
                    row.arrange(RIGHT, buff=1)
                    row.next_to(headers, DOWN, buff=0.3 + i*0.4)
                
                # Create constants section
                constants_title = Text("Important Constants", font_size=28)
                constants_title.next_to(rows[-1], DOWN, buff=1)
                
                constants = VGroup(
                    MathTex("k_b = 1.38 \\times 10^{-23} \\text{ J/K}", font_size=20),
                    MathTex("N_A = 6.022 \\times 10^{23} \\text{ mol}^{-1}", font_size=20),
                    MathTex("R_u = 8.314 \\text{ J/(mol·K)}", font_size=20),
                    MathTex("R = \\frac{R_u}{M} \\text{ J/(kg·K)}", font_size=20)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
                constants.next_to(constants_title, DOWN, buff=0.5)
                
                # Animate everything
                self.play(
                    Write(table_title),
                    Write(headers)
                )
                self.play(Write(rows))
                self.play(
                    Write(constants_title),
                    Write(constants)
                )
                self.wait(2)
                
                # Fade out everything
                self.play(
                    FadeOut(table_title),
                    FadeOut(headers),
                    FadeOut(rows),
                    FadeOut(constants_title),
                    FadeOut(constants)
                )
        
    def section5(self):
        # Title and main equation
        equation = MathTex("PV = nR_uT").scale(1.5)
        header = Text("What assumptions make this law work?", font_size=36).to_edge(UP)

        self.play(Write(equation))
        self.play(FadeOut(equation), Write(header))

        # ===============================
        # Assumption 1: Point Particles
        # ===============================
        with self.voiceover(
            "Assumption one: Gas particles are treated as point-like. "
            "They are so small compared to the container that we assume they occupy no volume. "
            "This means all of the container's space is available for the particles to move freely."
        ):
            # Left: Point particles (blue dots)
            point_particles = VGroup()
            for _ in range(20):
                dot = Dot(radius=0.05, color=BLUE)
                dot.move_to([np.random.uniform(-2, 0), np.random.uniform(-1, 1), 0])
                point_particles.add(dot)

            # Right: Finite-size particles (red spheres)
            volume_particles = VGroup()
            for _ in range(8):
                sphere = Sphere(radius=0.25)
                sphere.set_fill(RED, opacity=0.8)
                sphere.move_to([np.random.uniform(1, 3), np.random.uniform(-1, 1), 0])
                volume_particles.add(sphere)

            # Combine left and right
            vol_box = VGroup(point_particles, volume_particles).arrange(RIGHT, buff=2)
            self.play(FadeIn(vol_box))
            self.wait(1)

        with self.voiceover(
            "This assumption works well when gas is sparse. "
            "But under high pressure, particles become crowded and their size matters — reducing the free space."
        ):
            self.play(volume_particles.animate.arrange_in_grid(rows=2, cols=4, buff=0.4).shift(RIGHT * 1.5))
            self.wait(1)
            self.play(FadeOut(vol_box))

        # ===============================
        # Assumption 2: No Intermolecular Forces
        # ===============================
        with self.voiceover(
            "Assumption two: We ignore any attractive or repulsive forces between particles. "
            "They move in straight lines until they collide. "
            "No long-range forces act between them. This simplifies the motion greatly."
        ):
            force_particles = VGroup()
            for _ in range(10):
                p = Sphere(radius=0.1)
                p.set_fill(GREEN, opacity=0.8)
                p.move_to([np.random.uniform(-2, 2), np.random.uniform(-1, 1), 0])
                force_particles.add(p)

            self.play(FadeIn(force_particles))

            # Animate free motion (no interactions)
            for _ in range(20):
                for p in force_particles:
                    dx, dy = np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1)
                    p.shift([dx, dy, 0])
                self.wait(0.05)

        with self.voiceover(
            "In reality, particles do attract each other, especially at low temperatures. "
            "This leads to deviations from ideal gas behavior."
        ):
            # Animate attraction: move all to center
            for p in force_particles:
                self.play(p.animate.move_to(ORIGIN), run_time=0.2)
            self.wait(1)
            self.play(FadeOut(force_particles))

        # ===============================
        # Assumption 3: Dilute Gas
        # ===============================
        with self.voiceover(
            "Assumption three: The gas must be dilute. "
            "This means the particles are far apart, making interactions rare and justifying our previous assumptions. "
            "In the dilute limit, all the container volume is available and molecules rarely collide."
        ):
            dilute_particles = VGroup()
            for _ in range(10):
                p = Dot(radius=0.06, color=YELLOW)
                p.move_to([np.random.uniform(-3, 3), np.random.uniform(-2, 2), 0])
                dilute_particles.add(p)

            self.play(FadeIn(dilute_particles))
            self.wait(1)

        with self.voiceover(
            "If gas becomes dense, particles are more likely to collide or interact — violating ideal behavior."
        ):
            self.play(dilute_particles.animate.arrange_in_grid(rows=2, cols=5, buff=0.3).shift(DOWN * 0.5))
            self.wait(1)
            self.play(FadeOut(dilute_particles))

        # ===============================
        # Summary
        # ===============================
        with self.voiceover(
            "These three assumptions — point particles, no intermolecular forces, and low density — "
            "form the foundation of the ideal gas law. "
            "They help us model gases accurately under normal conditions. "
            "But in extreme situations, like high pressure or low temperature, we need more advanced models."
        ):
            summary_box = VGroup(
                Text("Ideal Gas Assumptions", font_size=28).set_color(YELLOW),
                Text("1. Particles have no volume", font_size=24),
                Text("2. No forces between particles", font_size=24),
                Text("3. Gas is dilute (low density)", font_size=24)
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)

            self.play(FadeIn(summary_box))
            self.wait(2)


    def section6(self): 
        # Title and subheading
        title = Text("Ideal vs. Real Gases: When Physics Gets Messy", font_size=36)
        subheading = Text("The Ideal Gas Law is a powerful approximation — but it's not perfect", font_size=24)
        title.to_edge(UP)
        subheading.next_to(title, DOWN)

        self.play(Write(title), Write(subheading))

        # Create side-by-side containers
        ideal_box = Rectangle(height=2, width=2).set_stroke(WHITE, 2).set_fill(BLUE_E, opacity=0.2)
        ideal_label = Text("Ideal Gas", font_size=24).next_to(ideal_box, UP)
        ideal_particles = VGroup()
        for _ in range(15):
            particle = Sphere(radius=0.05).set_fill(YELLOW, opacity=0.8)
            x, y, z = np.random.uniform(-0.8, 0.8), np.random.uniform(-0.8, 0.8), np.random.uniform(-0.4, 0.4)
            particle.move_to([x, y, z])
            ideal_particles.add(particle)
        ideal_group = VGroup(ideal_label, ideal_box, ideal_particles)

        real_box = Rectangle(height=2, width=2).set_stroke(WHITE, 2).set_fill(RED_E, opacity=0.2)
        real_label = Text("Real Gas", font_size=24).next_to(real_box, UP)
        real_particles = VGroup()
        for _ in range(15):
            particle = Sphere(radius=0.08).set_fill(RED, opacity=0.8)
            x, y, z = np.random.uniform(-0.8, 0.8), np.random.uniform(-0.8, 0.8), np.random.uniform(-0.4, 0.4)
            particle.move_to([x, y, z])
            real_particles.add(particle)
        real_group = VGroup(real_label, real_box, real_particles)

        comparison = VGroup(ideal_group, real_group).arrange(RIGHT, buff=2)
        self.play(Create(comparison))

        with self.voiceover(
            "In the ideal gas model, we imagine particles that are tiny, don't interact, and move freely through the entire container. "
            "But real gas particles have volume, and when they're packed together, that space matters."
        ):
            # Animate motion
            for _ in range(10):
                for particle in ideal_particles:
                    particle.shift([np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1), 0])
                for particle in real_particles:
                    particle.shift([np.random.uniform(-0.05, 0.05), np.random.uniform(-0.05, 0.05), 0])
                self.wait(0.1)

        with self.voiceover(
            "Real particles also attract each other — especially at low temperatures. These interactions reduce the pressure, deviating from ideal predictions."
        ):
            for particle in real_particles:
                if np.random.random() < 0.3:
                    particle.set_fill(RED, opacity=0.8)
                else:
                    particle.set_fill(BLUE, opacity=0.8)
            self.wait(1)

        with self.voiceover(
            "At high pressure, particles get crowded. The assumptions of ideal behavior begin to break down — and the Ideal Gas Law becomes inaccurate."
        ):
            self.play(real_box.animate.scale(0.85), run_time=1)
            self.wait(1)

        # P-V graph comparison
        with self.voiceover(
            "This becomes clear if we compare pressure and volume. Ideal gases follow a simple inverse curve. Real gases deviate — especially at low volumes."
        ):
            axes = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], axis_config={"include_tip": True})
            labels = axes.get_axis_labels(x_label="V", y_label="P")
            ideal_graph = axes.plot(lambda x: 4/x, x_range=[0.8, 4], color=YELLOW)
            real_graph = axes.plot(lambda x: 4/x + 0.5*np.exp(-x), x_range=[0.8, 4], color=RED)
            graph_group = VGroup(axes, labels, ideal_graph, real_graph).scale(0.5).to_edge(DOWN)
            self.play(Create(graph_group))

        with self.voiceover(
            "To correct for this, scientists developed more realistic models. One famous example is the Van der Waals equation. "
            "It adds terms to adjust for attraction and particle volume."
        ):
            vdw_eq = MathTex("(P + \\frac{an^2}{V^2})(V - nb) = nRT").next_to(graph_group, UP)
            a_note = Text("a: attraction correction", font_size=20)
            b_note = Text("b: volume correction", font_size=20)
            notes = VGroup(a_note, b_note).arrange(DOWN, aligned_edge=LEFT).next_to(vdw_eq, RIGHT)
            self.play(Write(vdw_eq), Write(notes))

        with self.voiceover(
            "Even though real gases can behave unpredictably under extreme conditions, the Ideal Gas Law still works remarkably well — and gives us the foundation to explore more complex systems."
        ):
            self.play(FadeOut(comparison), FadeOut(graph_group), FadeOut(vdw_eq), FadeOut(notes))
            self.wait(1)
    def section11(self):
        # Title
        title = Text("Ideal Gas Law: Summary", font_size=36)
        title.to_edge(UP)
        
        # Main equation
        equation = MathTex("PV = nR_uT").scale(2).set_color(YELLOW)
        
        with self.voiceover(
            "Let's review the big picture. The Ideal Gas Law connects pressure, volume, temperature, and the amount of gas "
            "in a single elegant equation: P V equals n R_u T."
        ):
            self.play(Write(title))
            self.play(Write(equation))
            self.wait(1)
        
        # Create the equation visualization with boxed variables
        with self.voiceover(
            "We can visualize the fundamental relationship as an equation. "
            "Let me show you how pressure times volume divided by the number of molecules times temperature equals Boltzmann's constant."
        ):
            self.play(FadeOut(equation), title.animate.scale(0.8).to_corner(UL))
            
            # Create boxes for each variable in the equation PV/NT = k_b
            box_size = 1.0
            
            # Create boxes for each variable
            p_box = Rectangle(width=box_size, height=box_size, color=WHITE, stroke_width=3)
            v_box = Rectangle(width=box_size, height=box_size, color=WHITE, stroke_width=3)
            n_box = Rectangle(width=box_size, height=box_size, color=WHITE, stroke_width=3)
            t_box = Rectangle(width=box_size, height=box_size, color=WHITE, stroke_width=3)
            
            # Create variable labels
            p_label = MathTex("P", font_size=48)
            v_label = MathTex("V", font_size=48)
            n_label = MathTex("N", font_size=48)
            t_label = MathTex("T", font_size=48)
            
            # Create VGroups for each box and its label
            p_group = VGroup(p_box, p_label)
            v_group = VGroup(v_box, v_label)
            n_group = VGroup(n_box, n_label)
            t_group = VGroup(t_box, t_label)
            
            # Center labels in their boxes
            p_label.move_to(p_box.get_center())
            v_label.move_to(v_box.get_center())
            n_label.move_to(n_box.get_center())
            t_label.move_to(t_box.get_center())
            
            # Position boxes to form the equation PV/NT = k_b
            # Arrange PV in numerator
            pv_group = VGroup(p_group, v_group).arrange(RIGHT, buff=0.2)
            
            # Arrange NT in denominator
            nt_group = VGroup(n_group, t_group).arrange(RIGHT, buff=0.2)
            nt_group.next_to(pv_group, DOWN, buff=0.5)
            
            # Create fraction line
            fraction_line = Line(
                start=pv_group.get_left() + LEFT*0.3,
                end=pv_group.get_right() + RIGHT*0.3,
                stroke_width=3
            )
            fraction_line.move_to((pv_group.get_bottom() + nt_group.get_top()) / 2)
            
            # Create equals sign and k_b
            equals = MathTex("=", font_size=48)
            kb = MathTex("k_b", font_size=48)
            
            # Position the complete equation
            fraction_group = VGroup(pv_group, fraction_line, nt_group)
            equation_group = VGroup(fraction_group, equals, kb).arrange(RIGHT, buff=0.8)
            
            # Add the three different forms of the equation to the right
            eq_forms = VGroup(
                MathTex("PV = Nk_bT", font_size=28),
                MathTex("= nR_uT", font_size=28),
                MathTex("= mRT", font_size=28)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            eq_forms.next_to(equation_group, RIGHT, buff=2)
            
            self.play(Create(equation_group), Write(eq_forms))
            self.wait(1)
        
        # Boyle's Law (P and V)
        with self.voiceover(
            "First, let's see Boyle's Law - the relationship between pressure and volume. "
            "When temperature and number of molecules stay constant, pressure and volume are inversely related."
        ):
            # Create Boyle's law connections - highlight P and V boxes
            boyle_outline_p = Rectangle(width=box_size+0.2, height=box_size+0.2, color=RED, stroke_width=5)
            boyle_outline_v = Rectangle(width=box_size+0.2, height=box_size+0.2, color=RED, stroke_width=5)
            boyle_outline_p.move_to(p_group.get_center())
            boyle_outline_v.move_to(v_group.get_center())
            
            # Curved connection between P and V
            boyle_curve = ArcBetweenPoints(
                p_group.get_center() + RIGHT*0.3, 
                v_group.get_center() + LEFT*0.3,
                angle=PI/3, color=RED, stroke_width=8
            )
            
            boyle_label = Text("Boyle's law", font_size=24, color=RED)
            boyle_label.next_to(boyle_curve, UP, buff=0.8)
            
            self.play(
                Create(boyle_outline_p),
                Create(boyle_outline_v),
                Create(boyle_curve),
                Write(boyle_label)
            )
            self.wait(2)
        
        # Charles's Law (V and T)
        with self.voiceover(
            "Next is Charles's Law - volume and temperature are directly proportional "
            "when pressure and number of molecules remain constant."
        ):
            charles_outline_v = Rectangle(width=box_size+0.2, height=box_size+0.2, color=BLUE, stroke_width=5)
            charles_outline_v.move_to(v_group.get_center())
            charles_outline_t = Rectangle(width=box_size+0.2, height=box_size+0.2, color=BLUE, stroke_width=5)
            charles_outline_t.move_to(t_group.get_center())
            
            # Curved connection between V and T
            charles_curve = ArcBetweenPoints(
                v_group.get_center() + DOWN*0.3 + RIGHT*0.2, 
                t_group.get_center() + UP*0.3 + RIGHT*0.2,
                angle=-PI/3, color=BLUE, stroke_width=8
            )
            
            charles_label = Text("Charles' law", font_size=24, color=BLUE)
            charles_label.next_to(charles_curve, RIGHT, buff=0.6)
            
            self.play(
                Create(charles_outline_v),
                Create(charles_outline_t),
                Create(charles_curve),
                Write(charles_label)
            )
            self.wait(2)
        
        # Avogadro's Law (V and N)
        with self.voiceover(
            "Avogadro's Law shows that volume is proportional to the number of molecules "
            "when pressure and temperature are held constant."
        ):
            avogadro_outline_v = Rectangle(width=box_size+0.2, height=box_size+0.2, color=GREEN, stroke_width=5)
            avogadro_outline_v.move_to(v_group.get_center())
            avogadro_outline_n = Rectangle(width=box_size+0.2, height=box_size+0.2, color=GREEN, stroke_width=5)
            avogadro_outline_n.move_to(n_group.get_center())
            
            # Curved connection between V and N
            avogadro_curve = ArcBetweenPoints(
                v_group.get_center() + DOWN*0.3 + LEFT*0.2, 
                n_group.get_center() + UP*0.3 + LEFT*0.2,
                angle=PI/3, color=GREEN, stroke_width=8
            )
            
            avogadro_label = Text("Avogadro's law", font_size=24, color=GREEN)
            avogadro_label.next_to(avogadro_curve, LEFT, buff=0.6)
            
            self.play(
                Create(avogadro_outline_v),
                Create(avogadro_outline_n),
                Create(avogadro_curve),
                Write(avogadro_label)
            )
            self.wait(2)
        
        # Gay-Lussac's Law (P and T)
        with self.voiceover(
            "Finally, Gay-Lussac's Law connects pressure and temperature directly "
            "when volume and number of molecules stay constant."
        ):
            gay_lussac_outline_p = Rectangle(width=box_size+0.2, height=box_size+0.2, color=YELLOW, stroke_width=5)
            gay_lussac_outline_p.move_to(p_group.get_center())
            gay_lussac_outline_t = Rectangle(width=box_size+0.2, height=box_size+0.2, color=YELLOW, stroke_width=5)
            gay_lussac_outline_t.move_to(t_group.get_center())
            
            # Curved connection between P and T
            gay_lussac_curve = ArcBetweenPoints(
                p_group.get_center() + DOWN*0.3, 
                t_group.get_center() + UP*0.3,
                angle=-PI/3, color=YELLOW, stroke_width=8
            )
            
            gay_lussac_label = Text("Gay-Lussac's law", font_size=24, color=YELLOW)
            gay_lussac_label.next_to(gay_lussac_curve, DOWN, buff=1.0)
            
            self.play(
                Create(gay_lussac_outline_p),
                Create(gay_lussac_outline_t),
                Create(gay_lussac_curve),
                Write(gay_lussac_label)
            )
            self.wait(2)
        
        # Show all connections together
        with self.voiceover(
            "Together, these four relationships form the complete picture. "
            "All four gas laws are unified in the elegant equation we see here."
        ):
            # Highlight all connections briefly
            all_outlines = VGroup(
                boyle_outline_p, boyle_outline_v,
                charles_outline_v, charles_outline_t,
                avogadro_outline_v, avogadro_outline_n,
                gay_lussac_outline_p, gay_lussac_outline_t
            )
            all_curves = VGroup(boyle_curve, charles_curve, avogadro_curve, gay_lussac_curve)
            all_labels = VGroup(boyle_label, charles_label, avogadro_label, gay_lussac_label)
            
            self.play(
                all_outlines.animate.set_stroke(width=8),
                all_curves.animate.set_stroke(width=12),
                run_time=1.5
            )
            self.wait(1)
            
            # Transform to show the most common form
            final_equation = MathTex("PV = nR_uT").scale(1.8).set_color(YELLOW)
            final_equation.move_to(equation_group.get_center())
            
            self.play(
                FadeOut(all_outlines),
                FadeOut(all_curves),
                FadeOut(all_labels),
                Transform(equation_group, final_equation)
            )
            self.wait(1)

        # Explain the different forms and constants
        with self.voiceover(
            "These three forms represent the same fundamental relationship. "
            "The molecular form uses capital N for the number of molecules and k_b as Boltzmann's constant. "
            "The molar form uses lowercase n for the number of moles and R_u as the universal gas constant. "
            "The mass-based form uses m for mass and R as the specific gas constant, which varies for each gas."
        ):
            # Show explanations for the different constants
            const_explanations = VGroup(
                MathTex("k_b = 1.38 \\times 10^{-23} \\text{ J/K}", font_size=24).set_color(BLUE),
                MathTex("R_u = 8.314 \\text{ J/(mol·K)}", font_size=24).set_color(GREEN),
                MathTex("R = \\frac{R_u}{M} \\text{ J/(kg·K)}", font_size=24).set_color(ORANGE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            const_explanations.to_edge(RIGHT, buff=1)
            self.play(Transform(eq_forms, const_explanations))
            self.wait(2)

        # Breakdown of variables for the equation form
        with self.voiceover(
            "The equation shows the molecular form with capital N representing the number of molecules. "
            "However, in engineering and science, we also commonly use the molar form with lowercase n for moles. "
            "Here, P is pressure, V is volume, N is the number of molecules, and T is temperature."
        ):
            variable_descriptions = VGroup(
                Text("P: Pressure (Pa)", font_size=24),
                Text("V: Volume (m³)", font_size=24),
                Text("N: Number of molecules", font_size=24),
                Text("k_b: Boltzmann constant = 1.38×10⁻²³ J/K", font_size=24),
                Text("T: Temperature (K)", font_size=24)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            variable_descriptions.next_to(const_explanations, DOWN, buff=0.8)
            
            self.play(FadeIn(variable_descriptions))
            self.wait(1)

        # Show assumptions
        with self.voiceover(
            "But remember, this equation depends on key assumptions. We treat particles as having no volume, assume no forces between them, and say that collisions are elastic. "
            "It also works best when the gas is dilute, and molecules are far apart."
        ):
            assumptions = VGroup(
                Text("Assumptions:", font_size=28, color=BLUE),
                Text("• Particles have no volume (point particles)", font_size=20),
                Text("• No intermolecular forces", font_size=20),
                Text("• Collisions are elastic", font_size=20),
                Text("• Gas is dilute and in random motion", font_size=20)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            assumptions.next_to(variable_descriptions, DOWN, buff=0.8)
            
            self.play(FadeIn(assumptions))
            self.wait(1)

        # Show when ideal gas law works
        with self.voiceover(
            "Under normal conditions — low pressure and high temperature — these assumptions hold, and the law gives accurate results."
        ):
            when_valid = Text("Works well at low pressure and high temperature", font_size=20, color=GREEN)
            when_valid.next_to(assumptions, DOWN, buff=0.8)
            self.play(FadeIn(when_valid))

        with self.voiceover(
            "But when gases are compressed or cooled, particles interact more — and the Ideal Gas Law begins to fail."
        ):
            when_invalid = Text("Breaks down at high pressure or low temperature", font_size=20, color=RED)
            when_invalid.next_to(when_valid, DOWN, buff=0.3)
            self.play(FadeIn(when_invalid))

        with self.voiceover(
            "Still, the Ideal Gas Law is a powerful approximation that underpins much of thermodynamics, chemistry, and engineering. "
            "It's the starting point for understanding how gases behave — and where more advanced models begin."
        ):
            closing = Text(
                "Despite limitations, the Ideal Gas Law remains a powerful and widely-used tool in science and engineering.",
                font_size=20
            )
            closing.next_to(when_invalid, DOWN, buff=1).scale(0.9)
            self.play(FadeIn(closing))
            self.wait(2)

if __name__ == "__main__":
    from manim import config
    config.quality = "high_quality"
    config.disable_caching = False

    scene = IdealGas()
    scene.render()
