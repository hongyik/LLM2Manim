from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np
import os
import pathlib

class Thermodynamics_Introduction(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Create a local cache directory
        cache_dir = pathlib.Path("./voiceover_cache")
        cache_dir.mkdir(exist_ok=True)
        
        # Configure voiceover service with local cache
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af",
            cache_dir=cache_dir
        ))
        self.section1()
        self.clear()
        self.section2()
        self.clear()
        self.section3()
        self.clear()
        self.section4()
        self.clear()
        self.section5()
        self.clear()
        self.section6()
        self.clear()
        self.section7()
        self.clear()


    def section1(self):
        # Title slide
        title = Text("Thermodynamics: overview", font_size=40)
        title.to_edge(UP)
        
        # Create left side group (Boltzmann name)
        boltzmann_name = Text("Ludwig Boltzmann\n(1844-1906)", font_size=30)
        boltzmann_group = Group(boltzmann_name)
        boltzmann_group.to_edge(LEFT, buff=1)  # Position to left side
        
        # Create the container box
        box = Cube(side_length=4)
        box.set_stroke(WHITE, 2)
        box.set_fill(BLUE_E, opacity=0.2)
        
        # Create particles with initial velocities
        num_particles = 10
        particles = VGroup()
        particle_velocities = []  # Store velocities for each particle
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.08)  # Slightly smaller radius to avoid overcrowding
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

        # Create particle updater function
        def update_particles(particles, dt):
            bounds = 1.8
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
                
                # # Check for collisions with other particles
                # for j, other_particle in enumerate(particles):
                #     if i != j:
                #         other_pos = other_particle.get_center()
                #         distance = np.linalg.norm(new_pos - other_pos)
                #         if distance < 0.2:  # Sum of particle radii
                #             vel, particle_velocities[j] = particle_velocities[j], vel
                #             new_pos = pos + vel
                
                particle.move_to(new_pos)
                particle_velocities[i] = vel
        
        # Animation sequence
        with self.voiceover(text="Hey there! Welcome to statistical thermodynamics! You might be wondering what thermodynamics is and why we should even care about it. Well, it's actually all around us - from the engines in our cars to the air we breathe, and even the processes that keep us alive!") as tracker:
            self.play(Write(title))
            self.play(title.animate.scale(0.8).to_corner(UL))

        with self.voiceover(text="Now, I want to introduce you to someone pretty important - this is Ludwig Boltzmann. He was one of the pioneers in this field, but even he found it quite challenging to wrap his head around some of these concepts.") as tracker:
            self.play(FadeIn(boltzmann_group))
            self.wait(1)
            
        # Transition to particle simulation
        with self.voiceover(text="Here's the thing that makes thermodynamics so tricky - it deals with mind-bogglingly large numbers. Just take a single breath - you've just inhaled more molecules than there are stars in the known universe! And they're all bouncing around like this...") as tracker:
            # Fade out portrait and quote
            self.play(
                FadeOut(boltzmann_group),
                run_time=1
            )
            
            # Add particle simulation
            self.play(Create(box))
            particles.add_updater(update_particles)
            self.play(Create(particles))
            self.wait(2)
            
        with self.voiceover(text="Now, trying to track each molecule would be like trying to count every grain of sand on Earth - it's just not going to happen! That's where the genius of thermodynamics comes in - instead of tracking individual molecules, we look at how they behave as a group.") as tracker:
            # Remove particle motion before fadeout
            particles.remove_updater(update_particles)
            self.play(
                FadeOut(particles),
                FadeOut(box),
                run_time=2
            )
            
        # Clean up with grouped animation
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )
        
    def section2(self):
        # Title and subtitle
        subtitle = Text("Microscopic Chaos", font_size=36)
        subtitle.to_corner(UL)
        
        # Create the container box
        box = Cube(side_length=4)
        box.set_stroke(WHITE, 2)
        box.set_fill(BLUE_E, opacity=0.1)
        
        # Create particles with momentum vectors
        num_particles = 10
        # 30 particles
        particles = VGroup()
        momentum_arrows = VGroup()
        particle_velocities = []
        
        for _ in range(num_particles):
            # Create particle
            particle = Sphere(radius=0.1)
            particle.set_fill(YELLOW, opacity=0.8)
            
            # Random initial position
            x = np.random.uniform(-1.8, 1.8)
            y = np.random.uniform(-1.8, 1.8)
            z = np.random.uniform(-1.8, 1.8)
            particle.move_to([x, y, z])
            
            # Initialize velocity
            speed = 0.15
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            vel = np.array([
                speed * np.sin(phi) * np.cos(theta),
                speed * np.sin(phi) * np.sin(theta),
                speed * np.cos(phi)
            ])
            particle_velocities.append(vel)
            
            # Create momentum arrow
            arrow = Arrow3D(
                start=[x, y, z],
                end=[x + vel[0], y + vel[1], z + vel[2]],
                color=BLUE
            )
            
            particles.add(particle)
            momentum_arrows.add(arrow)
        
        # Labels for position and momentum
        pos_label = MathTex("\\text{Position: } q_i \\in \\mathbb{R}^3", font_size=36)
        mom_label = MathTex("\\text{Momentum: } p_i \\in \\mathbb{R}^3", font_size=36)
        labels = VGroup(pos_label, mom_label).arrange(DOWN, aligned_edge=LEFT)
        labels.to_edge(RIGHT)
        
        # Component vectors for detailed view
        def create_component_arrows(point, scale=1):
            x_arrow = Arrow3D(start=point, end=point + np.array([scale, 0, 0]), color=RED)
            y_arrow = Arrow3D(start=point, end=point + np.array([0, scale, 0]), color=GREEN)
            z_arrow = Arrow3D(start=point, end=point + np.array([0, 0, scale]), color=BLUE)
            return VGroup(x_arrow, y_arrow, z_arrow)
        
        # Component labels
        def create_component_labels(prefix):
            return VGroup(
                MathTex(f"{prefix}_x", color=RED, font_size=24),
                MathTex(f"{prefix}_y", color=GREEN, font_size=24),
                MathTex(f"{prefix}_z", color=BLUE, font_size=24)
            ).arrange(DOWN, buff=0.2)

        # Store initial camera position
        initial_phi = self.camera.phi
        initial_theta = self.camera.theta
        
        # Numbers highlighting
        numbers_per_particle = Text("6 numbers per particle", font_size=36)
        avogadro = MathTex("N \\approx 6.02 \\times 10^{23}", font_size=36)
        total_vars = Text("Total = 6N variables", font_size=36, color=RED)
        numbers_group = VGroup(numbers_per_particle, avogadro, total_vars).arrange(DOWN)
        numbers_group.to_edge(LEFT)

        def update_particles_and_arrows(particles, dt):
            for i, (particle, arrow) in enumerate(zip(particles, momentum_arrows)):
                pos = particle.get_center()
                vel = particle_velocities[i]
                new_pos = pos + vel
                
                # Check for collisions with walls
                bounds = 1.8
                for j in range(3):
                    if abs(new_pos[j]) > bounds:
                        vel[j] = -vel[j]
                        new_pos[j] = np.sign(new_pos[j]) * bounds
                
                # Update particle position
                particle.move_to(new_pos)
                
                # Update momentum arrow
                arrow.put_start_and_end_on(
                    new_pos,
                    new_pos + vel
                )
                
                particle_velocities[i] = vel

        # Animation sequence
        with self.voiceover(text="Let's dive a bit deeper into what's happening at the microscopic level. You know how when you're watching a crowd from far away, you can't see individual people but you can still tell what the crowd is doing? That's kind of what we're doing here with molecules."):
            self.play(Write(subtitle))
            self.play(Create(box))
            self.play(Create(particles))
            self.play(Create(momentum_arrows))
            
            # Add updater for continuous motion
            particles.add_updater(lambda m, dt: update_particles_and_arrows(particles, dt))
            self.wait(2)

        with self.voiceover(text="Now, here's something cool - each of these tiny molecules has what we call a position and momentum. Think of it like a GPS coordinate plus the direction and speed it's moving. That's six numbers we need to track for just one particle!"):
            # First show the general labels
            self.play(Write(labels))
            
            # Choose a particle to focus on (the first one)
            focus_particle = particles[0]
            focus_pos = focus_particle.get_center()
            
            # Move camera to focus position
            self.set_camera_orientation(phi=45 * DEGREES, theta=45 * DEGREES)
            self.move_camera(frame_center=focus_pos, zoom=2.5)
            self.wait(1)
            
            # Show position components
            pos_arrows = create_component_arrows(focus_pos, 0.5)
            pos_labels = create_component_labels("q")
            pos_labels.next_to(focus_pos, RIGHT)
            
            self.play(
                Create(pos_arrows, lag_ratio=0.2),
                Write(pos_labels),
                run_time=1.5
            )
            self.wait(0.5)
            
            # Show momentum components
            mom_arrows = create_component_arrows(focus_pos, 0.5)
            for arrow in mom_arrows:
                arrow.shift(UP * 0.5)  # Offset momentum arrows up slightly
            mom_labels = create_component_labels("p")
            mom_labels.next_to(pos_labels, RIGHT, buff=0.5)
            
            self.play(
                Create(mom_arrows, lag_ratio=0.2),
                Write(mom_labels),
                run_time=1.5
            )
            
            # Return to original view
            self.set_camera_orientation(phi=initial_phi, theta=initial_theta)
            self.move_camera(frame_center=ORIGIN, zoom=1)
            self.wait(1)
            
            # Fade out the detailed view
            self.play(
                FadeOut(pos_arrows),
                FadeOut(mom_arrows),
                FadeOut(pos_labels),
                FadeOut(mom_labels),
                run_time=1
            )
            
            self.play(Write(numbers_per_particle))
            self.wait(1)

        with self.voiceover(text="Now here's something incredible about the scale we're dealing with. Avogadro's number tells us there are 602 sextillion molecules in a tiny amount of gas. When we multiply that by six numbers per molecule, the complexity becomes astronomical!"):
            self.play(Write(avogadro))
            self.play(Write(total_vars))
            self.wait(1)

        # Matrix visualization for complexity
        matrix = Matrix([[f"q_{i}{j}" for j in ["x", "y", "z"]] + [f"p_{i}{j}" for j in ["x", "y", "z"]] 
                        for i in range(5)])  # Show first 5 particles
        matrix.scale(0.5)
        matrix.next_to(numbers_group, DOWN, buff=1)
        
        with self.voiceover(text="Tracking every single molecule would be like monitoring every person's exact location and movement on Earth at every moment. This is where thermodynamics shows its brilliance by helping us see the big picture."):
            # Quick matrix flash
            self.play(FadeIn(matrix))
            self.wait(0.5)
            self.play(FadeOut(matrix))
            
            # Final message
            impossible = Text("We cannot track each particle...", font_size=36)
            solution = Text("But we can understand the average.", font_size=36, color=GREEN)
            messages = VGroup(impossible, solution).arrange(DOWN)
            messages.to_edge(DOWN)
            
            self.play(Write(impossible))
            self.wait(0.5)
            self.play(Write(solution))
            self.wait(1)

        # Clean up
        particles.remove_updater(update_particles_and_arrows)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
    def section3(self):
        # Title
        subtitle = Text("The Macroscopic View", font_size=36)
        subtitle.to_corner(UL)
        
        # Create a transparent box with particles (similar to previous section)
        box = Cube(side_length=4)
        box.set_stroke(WHITE, 2)
        box.set_fill(BLUE_E, opacity=0.2)
        
        # Create fewer particles for initial view
        num_particles = 10
        particles = VGroup()
        particle_velocities = []
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.1)
            particle.set_fill(YELLOW, opacity=0.8)
            x = np.random.uniform(-1.8, 1.8)
            y = np.random.uniform(-1.8, 1.8)
            z = np.random.uniform(-1.8, 1.8)
            particle.move_to([x, y, z])
            particles.add(particle)
            
            speed = 0.15
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            vel = np.array([
                speed * np.sin(phi) * np.cos(theta),
                speed * np.sin(phi) * np.sin(theta),
                speed * np.cos(phi)
            ])
            particle_velocities.append(vel)
            
        def update_particles(particles, dt):
            bounds = 1.8
            for i, particle in enumerate(particles):
                pos = particle.get_center()
                vel = particle_velocities[i]
                new_pos = pos + vel
                
                for j in range(3):
                    if abs(new_pos[j]) > bounds:
                        vel[j] = -vel[j]
                        new_pos[j] = np.sign(new_pos[j]) * bounds
                
                particle.move_to(new_pos)
                particle_velocities[i] = vel
        
        # Create macroscopic cube (solid)
        macro_box = Cube(side_length=4)
        macro_box.set_fill(BLUE_E, opacity=0.8)
        macro_box.set_stroke(WHITE, 2)
        
        # Create variable labels with icons
        def create_variable_label(symbol, name, color=WHITE):
            return VGroup(
                MathTex(symbol, color=color, font_size=48),
                Text(f"= {name}", font_size=32, color=color)
            ).arrange(RIGHT, buff=0.2)
        
        T_label = create_variable_label("T", "Temperature", RED)
        P_label = create_variable_label("P", "Pressure", BLUE)
        V_label = create_variable_label("V", "Volume", GREEN)
        N_label = create_variable_label("N", "Number of particles", YELLOW)
        
        # Arrange labels around the cube
        T_label.next_to(macro_box, UP, buff=0.5)
        P_label.next_to(macro_box, LEFT, buff=1)
        V_label.next_to(macro_box, RIGHT, buff=1)
        N_label.next_to(macro_box, DOWN, buff=0.5)
        
        # Create comparison text
        micro_text = VGroup(
            Text("Microscopic:", font_size=36),
            MathTex("6N \\text{ variables}", font_size=36)
        ).arrange(RIGHT)
        
        macro_text = VGroup(
            Text("Macroscopic:", font_size=36),
            MathTex("T, P, V, N", font_size=36)
        ).arrange(RIGHT)
        
        comparison = VGroup(micro_text, macro_text).arrange(DOWN, buff=0.5)
        comparison.to_edge(RIGHT)
        
        # Create PVT axes
        axes = ThreeDAxes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            z_range=[0, 4, 1],
            x_length=3,
            y_length=3,
            z_length=3
        )
        axes_labels = VGroup(
            MathTex("P").next_to(axes.get_z_axis(), UP),
            MathTex("V").next_to(axes.get_x_axis(), RIGHT),
            MathTex("T").next_to(axes.get_y_axis(), RIGHT)
        )
        
        state_dot = Sphere(radius=0.1).set_color(RED)
        state_dot.move_to(axes.c2p(2, 2, 2))
        
        # Animation sequence
        with self.voiceover(text="Alright, here's where things get really interesting! Instead of getting lost in all those individual molecules, thermodynamics gives us a brilliant shortcut - we can look at the big picture, what we call the 'macroscopic view'."):
            self.play(Write(subtitle))
            # self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
            self.play(Create(box))
            particles.add_updater(update_particles)
            self.play(Create(particles))
            self.wait(2)
            
            # Fade out particles and transform box
            particles.remove_updater(update_particles)
            self.play(
                FadeOut(particles),
                Transform(box, macro_box)
            )
            self.wait(1)
        
        with self.voiceover(text="Think about it like this - when you're cooking, you don't need to know what each molecule in your pot is doing. You just need to know a few key things: how hot it is (that's temperature), how much space it takes up (that's volume), how hard the molecules are hitting the walls (that's pressure), and how much stuff you've got in there (that's the number of particles). But here's the catch - we can only define these variables when the system is in equilibrium, when things have settled down."):
            # Show macroscopic variables
            self.play(Write(T_label))
            self.wait(0.5)
            self.play(Write(V_label))
            self.wait(0.5)
            self.play(Write(P_label))
            self.wait(0.5)
            self.play(Write(N_label))
            self.wait(1)
        
        with self.voiceover(text="And here's why this is so amazing - instead of tracking billions of molecules, each with its own position and speed, we only need to keep track of a few numbers. It's like instead of knowing what every person in a city is doing, we just need to know the city's population, average income, and a few other key statistics. This massive simplification is what makes thermodynamics so powerful!"):
            # Show comparison
            self.play(Write(comparison))
            self.wait(2)
        
        with self.voiceover(text="And here's a sneak peek at some other state variables we'll use later in the course, like entropy and chemical potential. Don't worry if these sound mysterious right now - we'll explain what each of them means when the time comes. Just remember - all these variables only make sense when our system is in equilibrium. That's why understanding equilibrium is so crucial!"):
            # Show additional variables
            additional_note = MathTex(
                r"\text{Note: While these are the main state variables, there are many others like density,} \\ \text{chemical potential, and composition that can also describe system state.}",
                font_size=16
            )
            additional_note.next_to(N_label, DOWN, buff=0.5)
            self.play(Write(additional_note))
            self.wait(1)
        
        with self.voiceover(text="And here's the amazing part - we've just turned a system that needed trillions upon trillions of numbers to describe it into something we can understand with just a few simple measurements. Pretty neat, right?"):
            # Show comparison
            self.play(Write(comparison))
            self.wait(2)
        
        with self.voiceover(text="These are what we call our macroscopic variables - they're like the CliffsNotes version of what's happening with all those molecules. And the best part? We can actually measure these things in real life!"):
            # Move camera to show PVT space
            #self.move_camera(phi=0, theta=-90 * DEGREES)
            self.play(
                FadeOut(box),
                FadeOut(T_label),
                FadeOut(P_label),
                FadeOut(V_label),
                FadeOut(N_label),
                FadeOut(additional_note),
                FadeOut(comparison)
            )
            
            # Show PVT space
            self.play(
                Create(axes),
                Write(axes_labels)
            )
            self.play(Create(state_dot))
            
            # Add final label
            final_text = Text("A macrostate", font_size=36)
            final_text.next_to(state_dot, RIGHT)
            self.play(Write(final_text))
            self.wait(1)
        
        # Clean up
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
    def section4(self):
        # Scene 1: Title and Initial View
        title = Text("State Variables vs. State Functions", font_size=40)
        subtitle = Text("From Microscopic Chaos to Macroscopic Order", font_size=32)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        title_group.to_edge(UP)
        
        # Create microscopic view (particle box) with dynamic particles
        micro_box = Cube(side_length=3)
        micro_box.set_stroke(RED_E, 2)
        micro_box.set_fill(RED_E, opacity=0.1)
        micro_box.shift(LEFT * 3)  # Move box to left side
        
        # Create particles with dynamic motion
        particles = VGroup()
        particle_velocities = []
        num_particles = 10
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.1)
            particle.set_fill(RED, opacity=0.8)
            
            # Random position within bounds (adjusted for left position)
            x = np.random.uniform(-1.3, 1.3) - 3  # Offset by 3 to match box position
            y = np.random.uniform(-1.3, 1.3)
            z = np.random.uniform(-1.3, 1.3)
            particle.move_to([x, y, z])
            particles.add(particle)
            
            # Initialize velocity with random direction
            speed = 0.15
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            vx = speed * np.sin(phi) * np.cos(theta)
            vy = speed * np.sin(phi) * np.sin(theta)
            vz = speed * np.cos(phi)
            particle_velocities.append(np.array([vx, vy, vz]))
        
        def update_particles(particles, dt):
            bounds = 1.3  # Slightly smaller than box size for better visibility
            box_center = np.array([-3, 0, 0])  # Center of the shifted box
            for i, particle in enumerate(particles):
                pos = particle.get_center() - box_center
                vel = particle_velocities[i]
                new_pos = pos + vel
                
                # Check for collisions with walls
                for j in range(3):
                    if abs(new_pos[j]) > bounds:
                        vel[j] = -vel[j]
                        new_pos[j] = np.sign(new_pos[j]) * bounds
                
                # Check for collisions with other particles
                for j, other_particle in enumerate(particles):
                    if i != j:
                        other_pos = other_particle.get_center() - box_center
                        distance = np.linalg.norm(new_pos - other_pos)
                        if distance < 0.2:  # Sum of particle radii
                            vel, particle_velocities[j] = particle_velocities[j], vel
                            new_pos = pos + vel
                
                particle.move_to(new_pos + box_center)
                particle_velocities[i] = vel
        
        micro_view = VGroup(micro_box, particles)
        micro_label = Text("Microscopic View", font_size=32, color=RED)
        micro_label.next_to(micro_box, DOWN)
        
        # Create right-side text content with proper wrapping and positioning
        state_var_def = Text(
            "State variables are coordinates describing\nthe system's position in current state\nor state space.",
            font_size=24,
            line_spacing=1.2
        ).to_edge(RIGHT, buff=0.5)
        
        def create_state_var(symbol, name, color=BLUE):
            return VGroup(
                MathTex(symbol, font_size=36, color=color),
                Text(f"= {name}", font_size=32)
            ).arrange(RIGHT, buff=0.2)
        
        state_vars = VGroup(
            create_state_var("T", "Temperature"),
            create_state_var("P", "Pressure"),
            create_state_var("V", "Volume"),
            create_state_var("N", "Number of particles")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        state_vars.next_to(state_var_def, DOWN, buff=0.5)
        
        additional_note = Text(
            "Note: While these are the main state\nvariables, there are many others like\ndensity, chemical potential, and\ncomposition that can also describe\nsystem state.",
            font_size=24,
            line_spacing=1.2
        )
        additional_note.next_to(state_vars, DOWN, buff=0.5)
        
        # Right-aligned text group
        right_text_group = VGroup(state_var_def, state_vars, additional_note)
        right_text_group.to_edge(RIGHT, buff=0.5)
        
        # State Functions definitions
        state_func_def = Text(
            "State functions are measurable properties\nthat depend only on the current state variables.",
            font_size=24,
            line_spacing=1.2
        )

        def create_state_func(equation, description):
            return VGroup(
                MathTex(equation, font_size=32),
                Text(description, font_size=24, color=GREY_A)
            ).arrange(RIGHT, buff=0.5)

        state_funcs = VGroup(
            create_state_func("U = U(T, V)", "Internal Energy: Total energy of the system"),
            create_state_func("H = U + PV", "Enthalpy: Energy needed at constant pressure"),
            create_state_func("S = S(T, V)", "Entropy: Measure of system disorder"),
            create_state_func("G = H - TS", "Gibbs Energy: Available work at constant T,P")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        # Animation sequence
        with self.voiceover(text="Now, let's talk about two really important concepts in thermodynamics - state variables and state functions. Don't worry if these terms sound a bit intimidating - I'll break them down for you in a way that makes sense."):
            self.play(Write(title_group))
            self.wait(0.5)
            
            # Show initial views and state variable definition
            self.play(
                Create(micro_box),
                Create(particles),
                Write(micro_label)
            )
            # Add particle updater for continuous motion
            particles.add_updater(lambda m, dt: update_particles(m, dt))
            
            # Animate text appearance on the right
            self.play(Write(state_var_def))
            self.wait(0.5)
            self.play(Write(state_vars))
            self.wait(0.5)
            self.play(Write(additional_note))
            self.wait(2)
        
        with self.voiceover(text="You know how when you're using GPS, it tells you exactly where you are using latitude and longitude? Well, state variables are kind of like that for thermodynamics - they tell us exactly where our system is, but instead of using coordinates on a map, we use things like temperature, pressure, and volume."):
            # Remove particle updater before fadeout
            particles.remove_updater(update_particles)
            # Show state functions
            self.play(
                FadeOut(micro_box),
                FadeOut(particles),
                FadeOut(micro_label),
                FadeOut(right_text_group),
                Write(state_func_def.to_edge(RIGHT, buff=0.5))
            )
            self.play(
                Write(state_funcs.next_to(state_func_def, DOWN, buff=0.5))
            )
            self.wait(2)

        # Final summary
        summary = Text(
            "Thermodynamics turns microscopic chaos\ninto a few elegant numbers.",
            font_size=36,
            line_spacing=1.5
        ).to_edge(DOWN)
        
        with self.voiceover(text="Pretty amazing, right? We've taken this chaotic microscopic world where everything seems random and unpredictable, and turned it into something we can actually work with using just a few elegant numbers. That's the real magic of thermodynamics!"):
            self.play(FadeOut(state_funcs), Write(summary))
            self.wait(2)
        
        # Clean up
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
    def section5(self):
        # Title
        subtitle = Text("Thermal Equilibrium", font_size=36)
        subtitle.to_corner(UL)
        
        # Create thermometer class
        class Thermometer(VGroup):
            def __init__(self, height=2, temp_percentage=0.5, color=RED):
                super().__init__()
                # Create bulb
                self.bulb = Circle(radius=0.2, fill_opacity=1, color=color)
                # Create stem
                self.stem = Rectangle(height=height, width=0.1, fill_opacity=1)
                self.stem.next_to(self.bulb, UP, buff=0)
                # Create temperature line
                temp_height = height * temp_percentage
                self.temp_line = Rectangle(
                    height=temp_height,
                    width=0.08,
                    fill_opacity=1,
                    color=color
                )
                self.temp_line.move_to(self.stem)
                self.temp_line.align_to(self.stem, DOWN)
                # Add all components
                self.add(self.bulb, self.stem, self.temp_line)
                self.total_height = height
            
            def set_temperature(self, percentage, color):
                new_height = self.total_height * percentage
                self.temp_line.become(
                    Rectangle(
                        height=new_height,
                        width=0.08,
                        fill_opacity=1,
                        color=color
                    ).move_to(self.stem).align_to(self.stem, DOWN)
                )
                self.bulb.set_color(color)
        
        # Create cubes with particles
        def create_cube_system(color, speed_factor=1.0, num_particles=10):  # Increased from 4 to 12
            # Create cube
            cube = Cube(side_length=2)
            cube.set_stroke(color, 2)
            cube.set_fill(color, opacity=0.2)
            
            particles = VGroup()
            particle_velocities = []
            
            # Calculate cube bounds (in cube's coordinate system)
            cube_side = 1  # Half the side length since cube is centered
            
            for _ in range(num_particles):
                particle = Sphere(radius=0.08)  # Slightly smaller radius
                particle.set_fill(color, opacity=0.8)
                
                # Random position within cube bounds
                x = np.random.uniform(-cube_side, cube_side)
                y = np.random.uniform(-cube_side, cube_side)
                z = np.random.uniform(-cube_side, cube_side)
                
                # Position particle relative to cube's center
                particle.move_to(cube.get_center() + np.array([x, y, z]))
                particles.add(particle)
                
                # Random velocity scaled by speed_factor
                speed = 0.1 * speed_factor
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                vx = speed * np.sin(phi) * np.cos(theta)
                vy = speed * np.sin(phi) * np.sin(theta)
                vz = speed * np.cos(phi)
                particle_velocities.append(np.array([vx, vy, vz]))
            
            system = VGroup(cube, particles)
            return system, particle_velocities
        
        # Create hot and cold systems
        hot_system, hot_velocities = create_cube_system(RED, speed_factor=2.0)
        cold_system, cold_velocities = create_cube_system(BLUE, speed_factor=0.5)
        
        # Position systems at the same height
        hot_system.move_to(LEFT * 3 + UP * 0)  # Explicitly set y-coordinate to 0
        cold_system.move_to(RIGHT * 3 + UP * 0)  # Explicitly set y-coordinate to 0
        
        # Create thermometers
        hot_therm = Thermometer(color=RED)
        cold_therm = Thermometer(color=BLUE)
        hot_therm.next_to(hot_system, LEFT)
        cold_therm.next_to(cold_system, RIGHT)
        hot_therm.set_temperature(0.8, RED)  # Hot starts at 80%
        cold_therm.set_temperature(0.2, BLUE)  # Cold starts at 20%
        
        # Particle update function
        def update_particles(particles, velocities, dt):
            cube_center = particles.get_parent_system().get_center()
            cube_side = 1  # Half the side length
            
            for i, particle in enumerate(particles):
                pos = particle.get_center() - cube_center  # Position relative to cube center
                vel = velocities[i]
                new_pos = pos + vel
                
                # Check for collisions with cube walls
                for j in range(3):
                    if abs(new_pos[j]) > cube_side:
                        vel[j] = -vel[j]
                        new_pos[j] = np.sign(new_pos[j]) * cube_side
                
                # Update particle position relative to cube
                particle.move_to(cube_center + new_pos)
                velocities[i] = vel
        
        # Function to update system temperature visualization
        def update_system_temperature(system, particles, temp_value, thermometer):
            # Calculate color based on temperature
            color = interpolate_color(BLUE, RED, temp_value)
            # Update cube color
            system[0].set_stroke(color, 2)
            system[0].set_fill(color, opacity=0.2)
            # Update particle colors
            for particle in particles:
                particle.set_fill(color, opacity=0.8)
            # Update thermometer
            thermometer.set_temperature(temp_value, color)
        
        # Animation sequence
        with self.voiceover(text="Now that we understand the basics of thermodynamics, you might be wondering - how do we actually measure temperature? I mean, when you stick a thermometer in your coffee, how does it know what temperature to show? This brings us to a super important concept called thermal equilibrium."):
            self.play(Write(subtitle))
            
            # Show initial systems
            self.play(
                Create(hot_system),
                Create(cold_system),
                Create(hot_therm),
                Create(cold_therm)
            )
            
            # Add updaters for particle motion
            hot_system[1].get_parent_system = lambda: hot_system[0]
            cold_system[1].get_parent_system = lambda: cold_system[0]
            
            hot_system[1].add_updater(
                lambda m, dt: update_particles(m, hot_velocities, dt)
            )
            cold_system[1].add_updater(
                lambda m, dt: update_particles(m, cold_velocities, dt)
            )
            self.wait(2)
        
        with self.voiceover(text="Let's do a fun experiment to understand this. When you put a thermometer in something hot, the mercury inside the thermometer starts moving faster - just like these particles here. And when you put it in something cold, the particles slow down."):
            self.wait(3)
        
        # Bring systems together
        with self.voiceover(text="The key idea is that when two things are in contact, their particles will eventually reach the same average speed - that's what we call thermal equilibrium. It's like nature's way of finding balance. This is exactly how your thermometer works - it reaches the same temperature as whatever you're measuring!"):
            # Move systems together
            self.play(
                hot_system.animate.shift(RIGHT * 2),
                hot_therm.animate.shift(RIGHT * 2),
                cold_system.animate.shift(LEFT * 2),
                cold_therm.animate.shift(LEFT * 2)
            )
            
            # Gradually equalize temperatures
            steps = 30
            for i in range(steps):
                # Calculate interpolation factor
                t = (i + 1) / steps
                
                # Calculate temperatures
                hot_temp = 0.8 - 0.3 * t  # Hot cools down from 0.8 to 0.5
                cold_temp = 0.2 + 0.3 * t  # Cold warms up from 0.2 to 0.5
                
                # Calculate target speed (average of initial speeds)
                target_speed = 0.1 * (2.0 + 0.5) / 2  # Average of hot and cold initial speeds
                
                # Update velocities to converge to target speed
                for j in range(len(hot_velocities)):
                    # Get current speed
                    hot_speed = np.linalg.norm(hot_velocities[j])
                    cold_speed = np.linalg.norm(cold_velocities[j])
                    
                    # Calculate new speeds
                    new_hot_speed = hot_speed + (target_speed - hot_speed) * 0.1
                    new_cold_speed = cold_speed + (target_speed - cold_speed) * 0.1
                    
                    # Update velocities while preserving direction
                    if hot_speed > 0:
                        hot_velocities[j] = hot_velocities[j] * (new_hot_speed / hot_speed)
                    if cold_speed > 0:
                        cold_velocities[j] = cold_velocities[j] * (new_cold_speed / cold_speed)
                
                # Update system visualizations
                update_system_temperature(hot_system, hot_system[1], hot_temp, hot_therm)
                update_system_temperature(cold_system, cold_system[1], cold_temp, cold_therm)
                
                self.wait(0.1)
        
        with self.voiceover(text="And there you have it! Both systems have reached what we call thermal equilibrium - they've found their happy medium where all the particles are moving with the same average speed. It's like everyone at the party finally agreed on the same dance tempo!"):
            self.wait(2)
        
        # Clean up
        hot_system[1].remove_updater(update_particles)
        cold_system[1].remove_updater(update_particles)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
    def section6(self):
        # Title
        title = Text("The Zeroth Law of Thermodynamics", font_size=40)
        subtitle = Text("A foundational principle of temperature", font_size=32)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP)

        # Create thermometer class
        class Thermometer(VGroup):
            def __init__(self, height=2, temp_percentage=0.5, color=RED):
                super().__init__()
                # Create bulb
                self.bulb = Circle(radius=0.2, fill_opacity=1, color=color)
                # Create stem
                self.stem = Rectangle(height=height, width=0.1, fill_opacity=1)
                self.stem.next_to(self.bulb, UP, buff=0)
                # Create temperature line
                temp_height = height * temp_percentage
                self.temp_line = Rectangle(
                    height=temp_height,
                    width=0.08,
                    fill_opacity=1,
                    color=color
                )
                self.temp_line.move_to(self.stem)
                self.temp_line.align_to(self.stem, DOWN)
                # Add all components
                self.add(self.bulb, self.stem, self.temp_line)
                self.total_height = height
            
            def set_temperature(self, percentage, color):
                new_height = self.total_height * percentage
                self.temp_line.become(
                    Rectangle(
                        height=new_height,
                        width=0.08,
                        fill_opacity=1,
                        color=color
                    ).move_to(self.stem).align_to(self.stem, DOWN)
                )
                self.bulb.set_color(color)

        # Create a system class that combines cube and thermometer
        class ThermalSystem(VGroup):
            def __init__(self, label, initial_temp=0.5, cube_size=2):
                super().__init__()
                # Create cube
                self.cube = Cube(side_length=cube_size)
                
                # Calculate initial color
                initial_color = interpolate_color(BLUE, RED, initial_temp)
                self.cube.set_fill(initial_color, opacity=0.4)
                self.cube.set_stroke(initial_color, 2)
                
                # Create thermometer
                self.thermometer = Thermometer(height=2, temp_percentage=initial_temp, color=initial_color)
                self.thermometer.next_to(self.cube, RIGHT)
                
                # Add label
                self.label = Text(label, font_size=36)
                self.label.next_to(self.cube, DOWN)
                
                # Add all components
                self.add(self.cube, self.thermometer, self.label)
            
            def update_temperature(self, temp_value):
                color = interpolate_color(BLUE, RED, temp_value)
                self.cube.set_fill(color, opacity=0.4)
                self.cube.set_stroke(color, 2)
                self.thermometer.set_temperature(temp_value, color)

        # Create three systems with different initial temperatures
        system_A = ThermalSystem("A", initial_temp=0.8)  # Hot
        system_C = ThermalSystem("C", initial_temp=0.3)  # Medium
        system_B = ThermalSystem("B", initial_temp=0.55)  # Same as C's final temp
        
        # Position systems in a triangle
        system_A.move_to(UP * 2)
        system_B.move_to(LEFT * 3 + DOWN * 2)
        system_C.move_to(RIGHT * 3 + DOWN * 2)

        # Create connection arrows
        arrow_AC = Arrow(
            system_A.cube.get_bottom(),
            system_C.cube.get_top(),
            buff=0.3,
            color=YELLOW
        )
        arrow_BC = Arrow(
            system_B.cube.get_right(),
            system_C.cube.get_left(),
            buff=0.3,
            color=YELLOW
        )
        arrow_AB = DashedLine(
            system_A.cube.get_left(),
            system_B.cube.get_top(),
            color=YELLOW,
            dash_length=0.2
        ).add_tip()

        # Create equation for temperature equality
        eq1 = MathTex("T_A = T_C", color=YELLOW)
        eq2 = MathTex("T_B = T_C", color=YELLOW)
        eq3 = MathTex("\\therefore T_A = T_B", color=GREEN)
        equations = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.5)
        equations.to_edge(RIGHT)

        # Historical note text
        historical_note = Text(
            '"It\'s called the Zeroth Law because scientists realized\n'
            'they needed it to define temperature, but they had already named\n'
            'the First and Second Laws. So they jokingly named this one \'Zeroth\' to fit it in!"',
            font_size=21,
            line_spacing=1.3
        )
        historical_note.to_edge(DOWN)

        # Animation sequence
        with self.voiceover(text="Now, I'm going to tell you about something with a really funny name - the Zeroth Law of Thermodynamics. Yes, you heard that right - zeroth, not first! Don't worry, I'll explain why it has such a weird name in a minute."):
            self.play(Write(title_group))
            self.wait(1)

        with self.voiceover(text="Let's play a little game. We have three systems: A, B, and C. Think of them like three different cups of coffee, each at their own temperature."):
            #self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
            self.play(
                FadeOut(title_group),
                Create(system_A),
                Create(system_B),
                Create(system_C)
            )
            self.wait(2)

        with self.voiceover(text="Now, let's say cup A and cup C sit next to each other for a while. Just like we saw before, they'll eventually reach the same temperature."):
            self.play(Create(arrow_AC))
            self.play(Write(eq1))
            
            # Animate temperature equalization between A and C
            final_temp = 0.55  # Final equilibrium temperature
            steps = 20
            for t in range(steps):
                alpha = t / (steps - 1)
                temp_A = 0.8 - (0.25 * alpha)  # A cools from 0.8 to 0.55
                temp_C = 0.3 + (0.25 * alpha)  # C warms from 0.3 to 0.55
                system_A.update_temperature(temp_A)
                system_C.update_temperature(temp_C)
                self.wait(0.1)

        with self.voiceover(text="And if cup B also sits next to cup C for a while, they'll reach the same temperature too."):
            self.play(Create(arrow_BC))
            self.play(Write(eq2))
            
            # No temperature change needed since B is already at equilibrium temperature
            self.wait(1)

        with self.voiceover(text="Here's where it gets interesting - the Zeroth Law tells us that if A and C are at the same temperature, and B and C are at the same temperature, then A and B must also be at the same temperature! It's like if two people are the same height as a third person, they must be the same height as each other."):
            self.play(
                Create(arrow_AB),
                Write(eq3)
            )
            self.wait(1)

        # Group all visual elements and move them up
        visual_group = VGroup(
            system_A, system_B, system_C,
            arrow_AC, arrow_BC, arrow_AB,
            equations
        )

        # Add historical note with animation
        with self.voiceover(text="And about that weird name - here's a funny bit of science history. Scientists had already named the First and Second Laws when they realized they needed this one to make everything work. But since it was more fundamental than the First Law, they couldn't call it the Third Law. So they just said 'Hey, let's call it the Zeroth Law!' Pretty clever, right?"):
            self.play(
                visual_group.animate.scale(0.7).shift(UP * 1.5),
                Write(historical_note),
                run_time=2
            )
            self.wait(2)

        # Final message about temperature
        final_message = Text(
            "This law allows us to define temperature\n"
            "as a consistent, measurable quantity",
            font_size=28,
            color=YELLOW
        ).next_to(historical_note, UP)

        with self.voiceover(text="This simple idea might seem obvious, but it's actually super important - it's what allows us to use thermometers and be confident that when we say something is 70 degrees, that means the same thing everywhere!"):
            self.play(Write(final_message))
            self.wait(2)

        # Clean up
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section7(self):
        # Title
        title = Text("The Temperature Field", font_size=40)
        temp_eq = MathTex("T = T(x, y, z, t)", font_size=36)
        title_group = VGroup(title, temp_eq).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP)

        # Create a custom heatmap class
        class TemperatureField(VGroup):
            def __init__(self, width=4, height=3, resolution=50):
                super().__init__()
                self.resolution = resolution
                self.width = width
                self.height = height
                
                # Create mesh grid
                x = np.linspace(-width/2, width/2, resolution)
                y = np.linspace(-height/2, height/2, resolution)
                self.X, self.Y = np.meshgrid(x, y)
                
                # Initialize temperature field
                self.T = np.zeros((resolution, resolution))
                self.pixels = VGroup()
                
                # Create pixel grid
                dx = width/resolution
                dy = height/resolution
                for i in range(resolution):
                    for j in range(resolution):
                        pixel = Rectangle(
                            width=dx,
                            height=dy,
                            fill_opacity=1,
                            stroke_width=0
                        )
                        pixel.move_to([x[j], y[i], 0])
                        self.pixels.add(pixel)
                
                self.add(self.pixels)
            
            def update_temperature(self, temp_func):
                self.T = temp_func(self.X, self.Y)
                for i in range(self.resolution):
                    for j in range(self.resolution):
                        temp = self.T[i, j]
                        color = self.temperature_to_color(temp)
                        self.pixels[i * self.resolution + j].set_fill(color)
            
            def temperature_to_color(self, temp):
                # Map temperature to color (blue=cold, red=hot)
                return interpolate_color(BLUE, RED, (temp + 1) / 2)

        # Create GTE section
        gte_title = Text("Global Thermal Equilibrium (GTE)", font_size=26)
        gte_eq1 = MathTex("\\nabla T = \\vec{0}", font_size=32)
        gte_eq2 = MathTex("\\frac{\\partial T}{\\partial t} = 0", font_size=32)
        gte_eqs = VGroup(gte_eq1, gte_eq2).arrange(DOWN, buff=0.3)
        
        # Create GTE heatmap
        gte_field = TemperatureField()
        def gte_temp(x, y):
            return np.full_like(x, 0.5)  # Uniform temperature
        
        gte_field.update_temperature(gte_temp)
        gte_group = VGroup(gte_title, gte_eqs, gte_field).arrange(DOWN, buff=0.5)
        gte_group.to_edge(LEFT)

        # Create LTE section
        lte_title = Text("Local Thermal Equilibrium (LTE)", font_size=26)
        lte_eq1 = MathTex("\\nabla_\\eta T \\approx \\vec{0}", font_size=32)
        lte_eq2 = MathTex("\\frac{\\partial T}{\\partial \\tau} \\approx 0", font_size=32)
        lte_eqs = VGroup(lte_eq1, lte_eq2).arrange(DOWN, buff=0.3)
        
        # Create LTE heatmap
        lte_field = TemperatureField()
        def lte_temp(x, y, t=0):
            gradient = np.sin(x + 0.1 * np.sin(2*t))  # Gradient with small time fluctuation
            local_fluctuation = 0.1 * np.sin(5*x + 7*y + t)  # Small local variations
            return gradient + local_fluctuation
        
        lte_field.update_temperature(lambda x, y: lte_temp(x, y))
        lte_group = VGroup(lte_title, lte_eqs, lte_field).arrange(DOWN, buff=0.5)
        lte_group.to_edge(RIGHT)

        # Create zoom box for LTE
        zoom_box = Square(side_length=0.5, color=YELLOW)
        zoom_box.move_to(lte_field)
        
        # Create zoomed view
        zoomed_field = TemperatureField(width=1, height=1, resolution=20)
        zoomed_field.scale(2)
        zoomed_field.next_to(lte_field, DOWN)
        zoom_label = Text("Local region", font_size=24)
        zoom_label.next_to(zoomed_field, UP)

        # Animation sequence
        with self.voiceover(text="Let's talk about something really cool - how temperature actually spreads through space. You know how when you open the oven, you can feel the heat coming out? That's because temperature isn't just a single number - it can be different at different places and change over time."):
            self.play(Write(title_group))
            self.wait(1)

        with self.voiceover(text="Sometimes, everything's nice and steady - like when your coffee has been sitting out for a while and it's the same temperature everywhere. Scientists call this 'Global Thermal Equilibrium', or GTE for short. It's like when everyone in a crowd is moving at the same speed."):
            self.play(
                Write(gte_title),
                Write(gte_eqs)
            )
            self.play(Create(gte_field))
            self.wait(2)

        with self.voiceover(text="But life isn't always that simple! Sometimes things are only balanced in small areas - like when you're heating soup and some parts are hotter than others, but each tiny region is pretty steady on its own. We call this 'Local Thermal Equilibrium' or LTE. It's like having different groups in a crowd moving at their own pace."):
            self.play(
                Write(lte_title),
                Write(lte_eqs)
            )
            self.play(Create(lte_field))
            
            # Animate local fluctuations
            for t in range(20):
                lte_field.update_temperature(lambda x, y: lte_temp(x, y, t*0.2))
                self.wait(0.1)

        with self.voiceover(text="Let's zoom in on one of these small regions. See how even though the whole pot of soup might have different temperatures, this little bit right here stays pretty steady? That's the magic of local equilibrium!"):
            self.play(Create(zoom_box))
            self.play(
                Create(zoomed_field),
                Write(zoom_label)
            )
            
            # Animate zoomed view with minimal fluctuations
            for t in range(20):
                local_temp = lambda x, y: lte_temp(x/4, y/4, t*0.2)
                zoomed_field.update_temperature(local_temp)
                self.wait(0.1)

        # Final message
        final_message = Text(
            "This idea lets us use thermodynamics\n"
            "even in non-uniform systems",
            font_size=32
        ).to_edge(DOWN)

        with self.voiceover(text="And this is why thermodynamics is so powerful - even when things aren't perfectly uniform, like in most real-world situations, we can still use these ideas to understand what's going on. Pretty amazing how nature works, isn't it?"):
            self.play(Write(final_message))
            self.wait(2)

        # Clean up
        self.play(*[FadeOut(mob) for mob in self.mobjects])

if __name__ == "__main__":
    from manim import config
    config.quality = "high_quality"
    config.disable_caching = True
    scene = Thermodynamics_Introduction()
    scene.render()

