from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np
import random

class IdealGas2(VoiceoverScene, ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections
        self.section1()
        self.clear()
        self.section2()
        self.clear()
        self.section3()
        self.clear()
        self.section4()
        self.clear()
        self.section5()

    def update_particles(self, particles, room, dt):
        # Get room dimensions
        room_width = room.width/2
        room_height = room.height/2
        room_depth = room.depth/2
        
        # Update each particle's position
        for i, particle in enumerate(particles):
            pos = particle.get_center()
            vel = self.particle_velocities[i]  # Using the instance variable
            new_pos = pos + vel
            
            # Check for collisions with room walls and bounce
            # X direction (accounting for room position at x=-3)
            if abs(new_pos[0] + 3) > room_width:
                vel[0] = -vel[0]
                new_pos[0] = np.sign(new_pos[0]) * (room_width - 3)
            
            # Y direction
            if abs(new_pos[1]) > room_height:
                vel[1] = -vel[1]
                new_pos[1] = np.sign(new_pos[1]) * room_height
            
            # Z direction
            if abs(new_pos[2]) > room_depth:
                vel[2] = -vel[2]
                new_pos[2] = np.sign(new_pos[2]) * room_depth
            
            # Update particle position
            particle.move_to(new_pos)
            self.particle_velocities[i] = vel  # Update the instance variable

    def section1(self):
        # Create container box (black instead of blue)
        box = Cube(side_length=4)
        box.set_stroke(WHITE, 2)
        box.set_fill(BLACK, opacity=0.2)
        
        # Create particles with initial velocities
        num_particles = 4
        particles = VGroup()
        self.particle_velocities = []
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.08)
            particle.set_fill(WHITE, opacity=0.8)
            # Random initial position within the box
            x = np.random.uniform(-1.8, 1.8)
            y = np.random.uniform(-1.8, 1.8)
            z = np.random.uniform(-1.8, 1.8)
            particle.move_to([x, y, z])
            particles.add(particle)
            
            # Initialize with random velocity
            speed = 0.15
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            vx = speed * np.sin(phi) * np.cos(theta)
            vy = speed * np.sin(phi) * np.sin(theta)
            vz = speed * np.cos(phi)
            self.particle_velocities.append(np.array([vx, vy, vz]))
        
        # Create particle updater function
        def update_particles(particles, dt):
            bounds = 1.8
            for i, particle in enumerate(particles):
                pos = particle.get_center()
                vel = self.particle_velocities[i]
                new_pos = pos + vel
                
                # Check for collisions with walls
                if abs(new_pos[0]) > bounds:
                    vel[0] = -vel[0]
                    new_pos[0] = np.sign(new_pos[0]) * bounds
                
                if abs(new_pos[1]) > bounds:
                    vel[1] = -vel[1]
                    new_pos[1] = np.sign(new_pos[1]) * bounds
                
                if abs(new_pos[2]) > bounds:
                    vel[2] = -vel[2]
                    new_pos[2] = np.sign(new_pos[2]) * bounds
                
                particle.move_to(new_pos)
                self.particle_velocities[i] = vel
        
        # Initial narration with particles
        with self.voiceover(
            "In our previous lesson, we explored how ideal gases behave, and how pressure, volume, and temperature are linked by the ideal gas law."
        ):
            self.play(Create(box))
            particles.add_updater(update_particles)
            self.play(Create(particles))
            self.wait(2)
        
        # Create subtitle
        subtitle = Text("Quick Recap: The Ideal Gas State Equations", font_size=32)
        subtitle.to_edge(UP)
        
        with self.voiceover(
            "Let's now review the different forms of this equation, each useful in different situations."
        ):
            self.play(
                FadeOut(box),
                FadeOut(particles),
                Write(subtitle)
            )
        
        # 1. Density Form
        density_title = Text("1. Density Form", font_size=24, color=RED)
        density_eq = MathTex("p = \\rho RT")
        density_vars = VGroup(
            MathTex("p: \\text{ pressure in } \\text{Pa}"),
            MathTex("\\rho: \\text{ mass density in } \\text{kg/m}^3"),
            MathTex("R: \\text{ specific gas constant in } \\text{J/kg}\\cdot\\text{K}"),
            MathTex("T: \\text{ absolute temperature in } \\text{K}")
        ).arrange(DOWN, aligned_edge=LEFT)
        density_group = VGroup(density_title, density_eq, density_vars).arrange(DOWN, buff=0.3)
        density_group.next_to(subtitle, DOWN, buff=1)
        
        with self.voiceover("This is the density form, where we express the relationship using mass densi"):
            self.play(Write(density_group))
            self.wait(1)
            self.play(FadeOut(density_group))
        
        # 2. Specific Volume Form
        specific_title = Text("2. Specific Volume Form", font_size=24, color=RED)
        specific_eq = MathTex("pv = RT")
        specific_vars = VGroup(
            MathTex("v = \\frac{1}{\\rho}: \\text{ specific volume in } \\text{m}^3\\text{/kg}"),
            Text("Reminder: 'specific' means 'per unit mass'", font_size=20),
            MathTex("p, R, T: \\text{ same as above}")
        ).arrange(DOWN, aligned_edge=LEFT)
        specific_group = VGroup(specific_title, specific_eq, specific_vars).arrange(DOWN, buff=0.3)
        specific_group.next_to(subtitle, DOWN, buff=1)
        
        with self.voiceover("Next, we have the specific volume form, which focuses on volume per unit mass — often useful in fluid mechanics."):
            self.play(Write(specific_group))
            self.wait(1)
            self.play(FadeOut(specific_group))
        
        # 3. Molar Form
        molar_title = Text("3. Molar Form", font_size=24, color=RED)
        molar_eq = MathTex("pV = nR_uT = mRT")
        molar_vars = VGroup(
            MathTex("V: \\text{ total volume in } \\text{m}^3"),
            MathTex("n: \\text{ number of moles}"),
            MathTex("R_u: \\text{ universal gas constant } \\approx 8.314 \\text{ J/mol}\\cdot\\text{K}"),
            MathTex("m: \\text{ total mass in } \\text{kg}"),
            MathTex("R: \\text{ specific gas constant}"),
            MathTex("T: \\text{ temperature in } \\text{K}")
        ).arrange(DOWN, aligned_edge=LEFT)
        molar_group = VGroup(molar_title, molar_eq, molar_vars).arrange(DOWN, buff=0.3)
        molar_group.next_to(subtitle, DOWN, buff=1)
        
        with self.voiceover("Here's the molar form, where we calculate properties based on total moles or total mass."):
            self.play(Write(molar_group))
            self.wait(1)
            self.play(FadeOut(molar_group))
        
        # 4. Molecular Form
        molecular_title = Text("4. Molecular Form", font_size=24, color=RED)
        molecular_eq = MathTex("pV = Nk_bT")
        molecular_vars = VGroup(
            MathTex("N: \\text{ total number of molecules}"),
            MathTex("k_b: \\text{ Boltzmann constant } = 1.38 \\times 10^{-23} \\text{ J/K}"),
            MathTex("p, V, T: \\text{ as before}")
        ).arrange(DOWN, aligned_edge=LEFT)
        molecular_group = VGroup(molecular_title, molecular_eq, molecular_vars).arrange(DOWN, buff=0.3)
        molecular_group.next_to(subtitle, DOWN, buff=1)
        
        with self.voiceover("And finally, the molecular form connects directly to the number of molecules and Boltzmann's constant — useful in statistical physics.."):
            self.play(Write(molecular_group))
            self.wait(1)
            self.play(FadeOut(molecular_group))
        
        # Closing line
        with self.voiceover(
            "These forms give us flexibility, depending on whether we're studying gases from a macroscopic or microscopic perspective. Now let's move forward."
        ):
            self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(subtitle))

    def section2(self):
        # Start with 3D setup
        cube = VGroup()
        side_length = 4
        half = side_length / 2

        # Front face
        front = Rectangle(width=side_length, height=side_length, stroke_color=WHITE, fill_opacity=0.1)
        front.move_to(OUT * half)

        # Back face
        back = Rectangle(width=side_length, height=side_length, stroke_color=WHITE, fill_opacity=0.1)
        back.move_to(IN * half)

        # Left face
        left = Rectangle(width=side_length, height=side_length, stroke_color=WHITE, fill_opacity=0.1)
        left.rotate(PI / 2, axis=UP)
        left.move_to(LEFT * half)

        # Right face
        right = Rectangle(width=side_length, height=side_length, stroke_color=WHITE, fill_opacity=0.1)
        right.rotate(PI / 2, axis=UP)
        right.move_to(RIGHT * half)

        # Top face
        top = Rectangle(width=side_length, height=side_length, stroke_color=WHITE, fill_opacity=0.1)
        top.rotate(PI / 2, axis=RIGHT)
        top.move_to(UP * half)

        # Bottom face
        bottom = Rectangle(width=side_length, height=side_length, stroke_color=WHITE, fill_opacity=0.1)
        bottom.rotate(PI / 2, axis=RIGHT)
        bottom.move_to(DOWN * half)

        # Add all to the group
        for face in [front, back, left, right, top, bottom]:
            cube.add(face)

        # Center and show
        cube.move_to(ORIGIN)
        
        # Create 3D particles
        num_particles = 4
        particles = VGroup()
        self.particle_velocities = []
        
        for _ in range(num_particles):
            particle = Sphere(radius=0.15)
            particle.set_fill(WHITE, opacity=0.8)
            x = np.random.uniform(-1.8, 1.8)
            y = np.random.uniform(-1.8, 1.8)
            z = np.random.uniform(-1.8, 1.8)
            particle.move_to([x, y, z])
            particles.add(particle)
            
            speed = 0.3
            theta = np.random.uniform(0, 2 * PI)
            phi = np.random.uniform(0, PI)
            vx = speed * np.sin(phi) * np.cos(theta)
            vy = speed * np.sin(phi) * np.sin(theta)
            vz = speed * np.cos(phi)
            self.particle_velocities.append(np.array([vx, vy, vz]))
        
        def update_3d_particles(particles, dt):
            bounds = 1.8
            for i, particle in enumerate(particles):
                pos = particle.get_center()
                vel = self.particle_velocities[i]
                new_pos = pos + vel
                
                if abs(new_pos[0]) > bounds:
                    vel[0] = -vel[0]
                    new_pos[0] = np.sign(new_pos[0]) * bounds
                if abs(new_pos[1]) > bounds:
                    vel[1] = -vel[1]
                    new_pos[1] = np.sign(new_pos[1]) * bounds
                if abs(new_pos[2]) > bounds:
                    vel[2] = -vel[2]
                    new_pos[2] = np.sign(new_pos[2]) * bounds
                
                particle.move_to(new_pos)
                self.particle_velocities[i] = vel
        
        # Initial 3D scene setup
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(1.0)
        
        with self.voiceover("Let's zoom into the microscopic world of an ideal gas. Here, particles move randomly, colliding with the walls and each other."):
            self.play(
                Create(cube),
                run_time=1
            )
            particles.add_updater(update_3d_particles)
            self.play(Create(particles))
            self.wait(2)

        # Transition to 2D view
        with self.voiceover(
            "Here we see just particles moving around randomly — "
            "colliding with the walls and with each other."
        ):
            # Remove 3D updater
            particles.clear_updaters()
            
            # Create 2D box and particles
            box = Rectangle(width=4, height=4, stroke_color=WHITE, fill_color=BLACK, fill_opacity=0.2)
            
            # Create 2D particles with velocity arrows
            particles_2d = VGroup()
            velocity_arrows = VGroup()
            particle_velocities_2d = []
            
            for i in range(num_particles):
                # Convert 3D particle positions to 2D
                old_pos = particles[i].get_center()
                new_pos = [old_pos[0], old_pos[1], 0]
                
                particle = Sphere(radius=0.15)
                particle.set_fill(WHITE, opacity=0.8)
                particle.move_to(new_pos)
                particles_2d.add(particle)
                
                # Create 2D velocity
                speed = 0.15
                angle = np.random.uniform(0, 2 * PI)
                vx = speed * np.cos(angle)
                vy = speed * np.sin(angle)
                velocity = np.array([vx, vy, 0])
                particle_velocities_2d.append(velocity)
                
                arrow = Arrow(
                    start=new_pos,
                    end=new_pos + velocity * 3,
                    color=YELLOW,
                    buff=0.1
                )
                velocity_arrows.add(arrow)
            
            # Create new 2D scene
            self.play(
                Create(box),
                Create(particles_2d),
                Create(velocity_arrows),
                run_time=2
            )
            
            # Update references
            particles = particles_2d
        
        def update_2d_particles_and_arrows(group, dt):
            particles, arrows = group
            bounds = 1.8
            for i, (particle, arrow) in enumerate(zip(particles, arrows)):
                pos = particle.get_center()
                vel = particle_velocities_2d[i]
                new_pos = pos + vel
                
                if abs(new_pos[0]) > bounds:
                    vel[0] = -vel[0]
                    new_pos[0] = np.sign(new_pos[0]) * bounds
                if abs(new_pos[1]) > bounds:
                    vel[1] = -vel[1]
                    new_pos[1] = np.sign(new_pos[1]) * bounds
                
                particle.move_to(new_pos)
                arrow.put_start_and_end_on(
                    new_pos,
                    new_pos + vel * 3
                )
                particle_velocities_2d[i] = vel
        
        particle_system = VGroup(particles, velocity_arrows)
        particle_system.add_updater(update_2d_particles_and_arrows)
        
        # Continue with the rest of the animation as before...
        # Remove updater temporarily for zoom
        particle_system.clear_updaters()
        
        with self.voiceover(
            "In an ideal gas, these particles are in constant motion. "
            "The internal energy of an ideal gas comes entirely from this molecular motion — specifically, from the kinetic energy of its molecules."
        ):
            # Zoom camera using move_camera
            self.play(
                FadeOut(VGroup(*particles[2:]), VGroup(*velocity_arrows[2:])),
                run_time=2
            )
            
        # Enhanced energy types explanation
        energy_title = Text("Types of Molecular Energy", font_size=28, color=YELLOW)
        energy_title.center()
        energy_title.to_edge(UP)
        
        with self.voiceover(
            "Let's break this energy into its different components, which are key to understanding heat capacities."
        ):
            self.clear()
            self.play(Write(energy_title))
            self.wait(0.5)
        
        # Enhanced translational energy demonstration
        with self.voiceover(
            "Let's start with translational energy. This is the energy associated with the movement "
            "of the entire molecule through space. It's the kinetic energy from position changes "
            "as molecules travel from one location to another."
            "In fact, the average translational energy of all the molecules is directly related to temperature. As we heat the gas, particles move faster, raising this energy."
        ):
            # Create definition box for translational energy with integrated description
            trans_def_title = Text("TRANSLATIONAL ENERGY", font_size=32, color=BLUE)
            trans_def_text = Text("Energy from position changes (movement through space)", font_size=26)
            trans_def_text2 = Text("To move from one location to another location", font_size=24)
            trans_def_box = VGroup(trans_def_title, trans_def_text, trans_def_text2).arrange(DOWN, buff=0.3)
            trans_def_box.to_edge(UP)
            
            # Create a single atom with trajectory
            single_atom = Sphere(radius=0.4, color=BLUE)
            single_atom.move_to(LEFT * 4)
            
            # Create trajectory path
            trajectory = DashedLine(
                start=LEFT * 4,
                end=RIGHT * 4,
                color=BLUE,
                dash_length=0.2
            )
            
            # Create position markers
            pos1 = Dot(point=LEFT * 2.5, color=YELLOW, radius=0.1)
            pos2 = Dot(point=ORIGIN, color=YELLOW, radius=0.1)
            pos3 = Dot(point=RIGHT * 2.5, color=YELLOW, radius=0.1)
            
            pos_labels = VGroup(
                Text("Position 1", font_size=22).next_to(pos1, UP),
                Text("Position 2", font_size=22).next_to(pos2, UP),
                Text("Position 3", font_size=22).next_to(pos3, UP)
            )
            
            # Create velocity arrow
            velocity_arrow = Arrow(
                start=single_atom.get_center(),
                end=single_atom.get_center() + RIGHT * 1.0,
                color=RED,
                buff=0.2,
                stroke_width=4
            )
            velocity_label = Text("v", font_size=28, color=RED).next_to(velocity_arrow, UP)
            
            self.play(
                Transform(energy_title,trans_def_box),
                Create(trajectory),
                Create(pos1),
                Create(pos2),
                Create(pos3),
                Write(pos_labels)
            )
            
            self.play(Create(single_atom))
            self.play(Create(velocity_arrow), Write(velocity_label))
            
            # Animate the atom moving along the trajectory
            self.play(
                single_atom.animate.move_to(RIGHT * 4),
                velocity_arrow.animate.move_to(RIGHT * 3),
                velocity_label.animate.move_to(RIGHT * 3 + UP * 0.5),
                run_time=3,
                rate_func=linear
            )
            
            # Show energy formula
            energy_formula = MathTex("E_{trans} = \\frac{1}{2}mv^2", font_size=32, color=BLUE)
            energy_formula.to_edge(DOWN)
            
            self.play(Write(energy_formula))
            self.wait(2)
        
        # Enhanced rotational energy demonstration
        with self.voiceover(
            "But molecules don't just move in straight lines. Some can also spin. This is called rotational energy."
            "For diatomic molecules like hydrogen, they can rotate around axes perpendicular to the bond between atoms. This spinning also stores energy."        ):
            # Transform to rotational demonstration
            self.clear()
            
            # Create definition box for rotational energy with integrated description
            rot_def_title = Text("ROTATIONAL KINETIC ENERGY", font_size=32, color=GREEN)
            rot_def_text = Text("Energy from spinning motion (around molecular axis)", font_size=26)
            rot_def_text2 = Text("Rotational kinetic energy is the energy due to the rotation about the center of mass", font_size=24)
            rot_def_box = VGroup(rot_def_title, rot_def_text, rot_def_text2).arrange(DOWN, buff=0.3)
            rot_def_box.to_edge(UP)
            
            # Create a diatomic molecule for rotation demonstration
            atom1 = Sphere(radius=0.3, color=WHITE)
            atom2 = Sphere(radius=0.3, color=WHITE)
            atom2.next_to(atom1, RIGHT, buff=0.6)
            
            # Create bond
            bond = Line(
                start=atom1.get_center(),
                end=atom2.get_center(),
                color=YELLOW,
                stroke_width=6
            )
            
            molecule = VGroup(atom1, atom2, bond)
            molecule.move_to(ORIGIN)
            
            # Create center of mass marker
            cm_dot = Dot(point=ORIGIN, color=RED, radius=0.1)
            cm_label = Text("CM", font_size=22, color=RED).next_to(cm_dot, UP)
            
            # Create rotation axis
            axis_line = DashedLine(
                start=UP * 1.0,
                end=DOWN * 1.0,
                color=GREEN,
                dash_length=0.2
            )
            axis_label = Text("Rotation Axis", font_size=22, color=GREEN).next_to(axis_line, RIGHT)
            
            # Create angular velocity arrow
            omega_arrow = CurvedArrow(
                start_point=atom1.get_center() + UP * 0.8,
                end_point=atom2.get_center() + UP * 0.8,
                angle=TAU/2,
                color=GREEN,
                stroke_width=5
            )
            omega_label = Text("ω", font_size=28, color=GREEN).next_to(omega_arrow, UP)
            
            self.play(
                Write(rot_def_box),
                Create(molecule),
                Create(cm_dot),
                Write(cm_label),
                Create(axis_line),
                Write(axis_label)
            )
            
            self.play(Create(omega_arrow), Write(omega_label))
            
            # Animate rotation
            self.play(
                Rotating(molecule, radians=2*PI, run_time=3, rate_func=linear),
                run_time=3
            )
            
            # Show energy formula
            rot_energy_formula = MathTex("E_{rot} = \\frac{1}{2}I\\omega^2", font_size=32, color=GREEN)
            rot_energy_formula.to_edge(DOWN)
            
            self.play(Write(rot_energy_formula))
            self.wait(2)
        
        # Enhanced vibrational energy demonstration
        with self.voiceover(
            "Finally, let's explore vibrational energy in detail. This is the energy associated with the stretching and compressing of bonds between atoms."
            "For diatomic molecules like hydrogen, this involves the atoms moving back and forth along the bond axis."
            "Vibrational energy becomes important at high temperatures, when molecules have enough energy to excite these vibrations."        ):
            # Transform to vibrational demonstration
            self.clear()
            
            # Create definition box for vibrational energy with integrated description
            vib_def_title = Text("VIBRATIONAL KINETIC ENERGY", font_size=32, color=RED)
            vib_def_text = Text("Energy from bond stretching (interatomic forces)", font_size=26)
            vib_def_text2 = Text("The total energy due to vibrations is the sum of the potential energy", font_size=24)
            vib_def_text3 = Text("associated with interactions causing the vibrations and the kinetic energy of the vibrations", font_size=24)
            vib_def_box = VGroup(vib_def_title, vib_def_text, vib_def_text2, vib_def_text3).arrange(DOWN, buff=0.3)
            vib_def_box.to_edge(UP)
            
            # Create vibrating diatomic molecule
            vib_atom1 = Sphere(radius=0.3, color=WHITE)
            vib_atom2 = Sphere(radius=0.3, color=WHITE)
            vib_atom2.next_to(vib_atom1, RIGHT, buff=0.6)
            
            # Create spring-like bond
            vib_bond = Line(
                start=vib_atom1.get_center(),
                end=vib_atom2.get_center(),
                color=RED,
                stroke_width=6
            )
            
            vib_molecule = VGroup(vib_atom1, vib_atom2, vib_bond)
            vib_molecule.move_to(ORIGIN)
            
            # Create equilibrium position indicator
            eq_line = DashedLine(
                start=LEFT * 1.0,
                end=RIGHT * 1.0,
                color=YELLOW,
                dash_length=0.2
            )
            eq_label = Text("Equilibrium", font_size=22, color=YELLOW).next_to(eq_line, UP)
            
            # Create force arrows
            force1 = Arrow(
                start=vib_atom1.get_center() + LEFT * 0.4,
                end=vib_atom1.get_center(),
                color=RED,
                buff=0.1,
                stroke_width=4
            )
            force2 = Arrow(
                start=vib_atom2.get_center(),
                end=vib_atom2.get_center() + RIGHT * 0.4,
                color=RED,
                buff=0.1,
                stroke_width=4
            )
            
            self.play(
                Write(vib_def_box),
                Create(vib_molecule),
                Create(eq_line),
                Write(eq_label)
            )
            
            # Animate vibration with force arrows
            for _ in range(3):
                # Stretch
                self.play(
                    vib_atom1.animate.shift(LEFT * 0.2),
                    vib_atom2.animate.shift(RIGHT * 0.2),
                    vib_bond.animate.stretch_to_fit_width(1.0),
                    Create(force1),
                    Create(force2),
                    rate_func=there_and_back,
                    run_time=1
                )
                # Compress
        self.play(
                    vib_atom1.animate.shift(RIGHT * 0.2),
                    vib_atom2.animate.shift(LEFT * 0.2),
                    vib_bond.animate.stretch_to_fit_width(0.2),
                    FadeOut(force1),
                    FadeOut(force2),
                    rate_func=there_and_back,
                    run_time=1
                )
            
            # Show energy formula
        vib_energy_formula = MathTex("E_{vib} = \\frac{1}{2}k(r-r_0)^2 + \\frac{1}{2}\\mu v^2", font_size=28, color=RED)
        vib_energy_formula.to_edge(DOWN)
            
        self.play(Write(vib_energy_formula))
        self.wait(2)
        
        
        # Return to overview
        with self.voiceover(
           "Together, translational, rotational, and vibrational motions make up the microscopic energy of a gas."
            "Now that we understand these different types of motion, we’re ready to see how they affect heat capacity — how much energy a gas needs to change its temperature."
        ):
            # Transform back to overview
            self.play(
                FadeOut(vib_def_box),
                FadeOut(vib_molecule),
                FadeOut(eq_line),
                FadeOut(eq_label),
                FadeOut(vib_energy_formula),
                run_time=1
            )
        
            # Recreate the original scene
            box = Rectangle(width=4, height=4, stroke_color=WHITE, fill_color=BLACK, fill_opacity=0.2)
            particles_2d = VGroup()
            velocity_arrows_2d = VGroup()
            
            for i in range(2):
                particle = Sphere(radius=0.15)
                particle.set_fill(WHITE, opacity=0.8)
                particle.move_to([(-1 + i*2), 0, 0])
                particles_2d.add(particle)
                
                arrow = Arrow(
                    start=particle.get_center(),
                    end=particle.get_center() + np.array([0.3, 0, 0]),
                    color=YELLOW,
                    buff=0.1
                )
                velocity_arrows_2d.add(arrow)
            
            self.play(
                Create(box),
                Create(particles_2d),
                Create(velocity_arrows_2d),
                run_time=2
            )

    def section3(self):
        # PART 1: Enthalpy Definition
        enthalpy_title = Text("Enthalpy: Definition", font_size=36, color=YELLOW)
        enthalpy_eq = MathTex(r"H = E + pV", font_size=40).set_color(TEAL)
        enthalpy_expl = VGroup(
            Text("H: enthalpy", font_size=26),
            Text("E: internal energy", font_size=26),
            Text("pV: pressure-volume work", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT)
        enthalpy_group = VGroup(enthalpy_title, enthalpy_eq, enthalpy_expl).arrange(DOWN, buff=0.3)
        enthalpy_group.to_edge(UP)
        with self.voiceover(
            "Now that we understand the different ways molecules store energy, let's build the next concept: enthalpy."
            "Enthalpy helps us simplify energy calculations, especially when gases are allowed to expand."            
            "We define enthalpy as:H=E+PV where:E is the internal energy (everything happening inside the molecules),p V is the energy required to make room for the system — that is, the work needed to push against the surrounding pressure to occupy space."):
            self.play(Write(enthalpy_group))
            self.wait(2)
        self.play(FadeOut(enthalpy_group), run_time=1)

        with self.voiceover("Why do we need this new quantity? Because many real-world processes happen at constant pressure. For example, heating air in an open room or boiling water in a pot. In these cases, it's much more convenient to track enthalpy rather than internal energy alone."):
            self.wait(2)

        # PART 2: Define Heat Capacities Using Enthalpy
        hc_title = Text("Heat Capacity: General Definition", font_size=34, color=YELLOW)
        hc_eq = MathTex(r"C = \left(\frac{\partial Q}{\partial T}\right)", font_size=36)
        hc_group = VGroup(hc_title, hc_eq).arrange(DOWN, buff=0.3)
        hc_group.to_edge(UP)

        with self.voiceover(
            "Now let's define heat capacity. Heat capacity is the amount of energy needed to raise the temperature of a substance by one degree. It's a measure of how much energy a substance can store."
            "Mathematically, we write:C=∂Q∂T where Q is the heat added to the system and T is the temperature change."):
            self.play(Write(hc_group))
            self.wait(1)
        
        # Add distinction between specific and total heat capacity
        distinction_text = Text("Heat Capacity Types:", font_size=28, color=BLUE)
        specific_text = Text("Specific (per unit mass)", font_size=24, color=GREEN)
        total_text = Text("Total (for entire system)", font_size=24, color=RED)
        distinction_group = VGroup(distinction_text, specific_text, total_text).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        distinction_group.next_to(hc_group, DOWN, buff=0.4)
        with self.voiceover(
            "There are two ways to talk about heat capacity:Total heat capacity, which applies to the entire system,Specific heat capacity, which is per unit mass of material."
            "This distinction helps us compare different substances regardless of how much material we have."):
            self.play(Write(distinction_group))
            self.wait(1)

        # Constant Volume - specific and total
        cv_title = Text("At Constant Volume:", font_size=30, color=GREEN)
        cv_specific = VGroup(
            MathTex(r"c_v = \frac{1}{m}\left(\frac{\partial Q}{\partial T}\right)_V = \left(\frac{\partial e}{\partial T}\right)_V", font_size=34),
            Text("(specific heat capacity at constant volume)", font_size=20)
        ).arrange(DOWN, buff=0.1)
        cv_total = VGroup(
            MathTex(r"C_V = \left(\frac{\partial Q}{\partial T}\right)_V = m c_v", font_size=34),
            Text("(total heat capacity at constant volume)", font_size=20)
        ).arrange(DOWN, buff=0.1)
        cv_box = VGroup(cv_title, cv_specific, cv_total).arrange(DOWN, buff=0.3)
        cv_box.next_to(distinction_group, DOWN, buff=0.6)
        
        with self.voiceover(
           "Let's first consider a process at constant volume — where the container is rigid, and the gas cannot expand."
           "In this case, no work can be done because volume doesn't change. All the heat goes directly into increasing internal energy."
           "We define specific heat at constant volume as:cv=∂Q∂T|V=∂e∂T|V"
           "And total heat capacity at constant volume as:CV=∂Q∂T|V=mcv"):
            self.play(Write(cv_box))
            self.wait(1)

        # Constant Pressure - specific and total
        cp_title = Text("At Constant Pressure:", font_size=30, color=RED)
        cp_specific = VGroup(
            MathTex(r"c_p = \frac{1}{m}\left(\frac{\partial Q}{\partial T}\right)_P = \left(\frac{\partial h}{\partial T}\right)_P", font_size=34),
            Text("(specific heat capacity at constant pressure)", font_size=20)
        ).arrange(DOWN, buff=0.1)
        cp_total = VGroup(
            MathTex(r"C_P = \left(\frac{\partial Q}{\partial T}\right)_P = m c_p", font_size=34),
            Text("(total heat capacity at constant pressure)", font_size=20)
        ).arrange(DOWN, buff=0.1)
        cp_box = VGroup(cp_title, cp_specific, cp_total).arrange(DOWN, buff=0.3)
        cp_box.next_to(cv_box, DOWN, buff=0.6)
        
        with self.voiceover("Similarly, for constant pressure, we have specific heat capacity cp and total heat capacity CP."
            "Now let's examine a constant pressure process."
            "When pressure is constant, the gas can expand as we add heat. Part of the heat increases internal energy, but some of it goes into doing expansion work."
            "Here, enthalpy becomes very useful, because at constant pressure:dQ=dH"
            "HENCE, we define specific heat at constant pressure as:cp=∂Q∂T|P=∂h∂T|P"
            "And total heat capacity at constant pressure as:CP=∂Q∂T|P=mcP"):
            self.play(Write(cp_box))
            self.wait(1)

        # Relationship between specific heat capacities
        relation_title = Text("Relationship (Ideal Gas):", font_size=30, color=YELLOW)
        relation_specific = MathTex(r"c_p = c_v + R", font_size=34)
        relation_total = MathTex(r"C_P = C_V + mR", font_size=34)
        relation_box = VGroup(relation_title, relation_specific, relation_total).arrange(DOWN, buff=0.3)
        relation_box.next_to(cp_box, DOWN, buff=0.6)
        
        with self.voiceover(
            "For an ideal gas, the relationship between specific heat capacities involves the gas constant R, while the total heat capacities involve mass times R."):
            self.play(Write(relation_box))
            self.wait(2)

        # Clear for next section
        self.play(
            FadeOut(hc_group),
            FadeOut(distinction_group),
            FadeOut(cv_box),
            FadeOut(cp_box),
            FadeOut(relation_box)
        )

        # PART 3: Derive Cp vs Cv Relation (Ideal Gas)
        derive_title = Text("Cp vs Cv Relation (Ideal Gas)", font_size=34, color=YELLOW)
        ig_eq1 = MathTex(r"pV = nRT", font_size=34)
        ig_eq2 = MathTex(r"\left(\frac{\partial (pV)}{\partial T}\right)_P = nR", font_size=34)
        cp_cv_eq = MathTex(r"C_P = \left(\frac{\partial E}{\partial T}\right) + \left(\frac{\partial (pV)}{\partial T}\right)_P", font_size=34)
        cp_cv_final = MathTex(r"C_P = C_V + nR", font_size=36).set_color(PURPLE)
        cp_cv_per_mole = MathTex(r"C_P = C_V + R", font_size=36).set_color(PURPLE)
        derive_group = VGroup(
            derive_title, ig_eq1, ig_eq2, cp_cv_eq, cp_cv_final, cp_cv_per_mole
        ).arrange(DOWN, buff=0.2)
        derive_group.to_edge(UP)
        with self.voiceover("For an ideal gas, pV equals nRT. The derivative of pV with respect to T at constant pressure is nR. Substitute into the heat capacity relation to get Cp equals Cv plus nR, or per mole, Cp equals Cv plus R."):
            self.play(Write(derive_group))
            self.wait(2)
        self.play(FadeOut(derive_group), run_time=1)

        # PART 4: Introduce Gamma
        gamma_title = Text("Heat Capacity Ratio: Gamma", font_size=34, color=YELLOW)
        gamma_eq = MathTex(r"\gamma = \frac{C_P}{C_V}", font_size=36).set_color(ORANGE)
        gamma_eq2 = MathTex(r"C_P = \gamma C_V", font_size=34)
        gamma_eq3 = MathTex(r"C_P - C_V = R", font_size=34)
        gamma_group = VGroup(gamma_title, gamma_eq, gamma_eq2, gamma_eq3).arrange(DOWN, buff=0.2)
        gamma_group.to_edge(UP)
        with self.voiceover("The heat capacity ratio gamma is very important for many thermodynamic processes."):
            self.play(Write(gamma_group))
            self.wait(2)
        self.play(FadeOut(gamma_group), run_time=1)

        # 1. Neutral container
        container = Rectangle(width=3, height=4, stroke_color=WHITE)
        self.play(Create(container))
        self.wait(1)

        # 2. Fix volume (cv)
        volume_text = Text("VOLUME", font_size=36)
        volume_text.next_to(container, UP)
        
        # Use PNG image for lock
        lock_img = ImageMobject("dataset/AE302/images/lock.png")
        lock_img.scale(0.15)  # Adjust scale as needed
        lock_img.next_to(volume_text, RIGHT, buff=0.1)
        
        cv_subtitle = Text("Constant Volume Process (c_V)", font_size=30, color=GREEN).to_edge(UP)
        
        # Detailed equations for constant volume process
        cv_equations = VGroup(
            MathTex(r"\text{For ideal diatomic gas }(H_2):").set_color(GREEN),
            MathTex(r"f = 5 \text{ (3 trans. + 2 rot. DOF)}"),
            MathTex(r"C_V = \frac{f}{2}R = \frac{5}{2}R"),
            MathTex(r"R = 8.314 \text{ J/(mol}\cdot\text{K)}"),
            MathTex(r"M_{H_2} = 2.016 \text{ g/mol} = 0.002016 \text{ kg/mol}"),
            MathTex(r"c_v = \frac{C_V}{M} = \frac{5}{2}\cdot\frac{8.314}{0.002016}"),
            MathTex(r"c_v = 10{,}312 \text{ J/(kg}\cdot\text{K)}"),
            MathTex(r"c_v = 10.31 \text{ kJ/(kg}\cdot\text{K)}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cv_equations.scale(0.7)
        cv_equations.next_to(container, LEFT, buff=0.5)
        
        info = MathTex(r"\text{Hydrogen Gas }H_2\text{, }1\text{ kg, }\Delta T = 1\text{°C}", font_size=28)
        info.next_to(container, RIGHT, buff=0.5)
        
        # Initial setup with volume text animation and equations
        with self.voiceover(
            "In a constant volume process, we fix the volume of the container. "
            "Let's examine how this affects the thermodynamic equations."
        ):
            self.play(Write(volume_text))
            self.wait(0.5)
            self.play(FadeIn(lock_img))
            self.play(
                Write(cv_subtitle),
                Write(cv_equations),
                Write(info)
            )
        
        # Animate heat increase with color only
        with self.voiceover(
            "As we add heat to the system, since the volume cannot change, "
            "all the energy goes into increasing the internal energy of the gas. "
            "This is shown by the increasing temperature and molecular motion."
        ):
            n_steps = 8
            for i in range(n_steps):
                self.play(
                    container.animate.set_fill(
                        color=interpolate_color(BLACK, RED, (i+1)/n_steps),
                        opacity=0.1 + 0.5*(i+1)/n_steps
                    ),
                    run_time=0.3
                )
                self.wait(0.1)
        
        self.wait(1)
        
        # Reset everything
        self.play(
            FadeOut(volume_text),
            FadeOut(lock_img),
            FadeOut(cv_subtitle),
            FadeOut(cv_equations),
            FadeOut(info),
            container.animate.set_fill(None, opacity=0.0)
        )

        # 3. Reset
        self.wait(0.5)

        # 4. Fix pressure (cp)
        cp_subtitle = Text("Constant Pressure Process (c_P)", font_size=30, color=RED).to_edge(UP)
        
        # Detailed equations for constant pressure process
        cp_equations = VGroup(
            MathTex(r"\text{For ideal diatomic gas }(H_2):").set_color(RED),
            MathTex(r"C_P = C_V + R = \frac{7}{2}R"),
            MathTex(r"R = 8.314 \text{ J/(mol}\cdot\text{K)}"),
            MathTex(r"M_{H_2} = 2.016 \text{ g/mol} = 0.002016 \text{ kg/mol}"),
            MathTex(r"c_p = \frac{C_P}{M} = \frac{7}{2}\cdot\frac{8.314}{0.002016}"),
            MathTex(r"c_p = 14{,}437 \text{ J/(kg}\cdot\text{K)}"),
            MathTex(r"c_p = 14.44 \text{ kJ/(kg}\cdot\text{K)}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cp_equations.scale(0.7)
        cp_equations.next_to(container, RIGHT, buff=0.5)
        
        info2 = MathTex(r"\text{Hydrogen Gas }H_2\text{, }1\text{ kg, }\Delta T = 1\text{°C}", font_size=28)
        info2.next_to(container, LEFT, buff=0.5)
        
        # Initial setup for constant pressure process
        original_height = container.height
        with self.voiceover(
            "In a constant pressure process, the pressure remains fixed while the volume is allowed to change. "
            "This process is described by a different set of equations that account for both internal energy changes "
            "and the work done in expanding the gas."
        ):
            self.play(
                Write(cp_subtitle),
                Write(cp_equations),
                Write(info2)
            )
            self.wait(0.5)

        # Animate the constant pressure process
        n_steps = 8
        with self.voiceover(
            "As we add heat to the system, the gas expands to maintain constant pressure. "
            "The specific heat capacity cp is larger than cv because the system needs additional "
            "energy to perform the expansion work while achieving the same temperature change."
        ):
            for i in range(n_steps):
                self.play(
                    container.animate.set_fill(
                        color=interpolate_color(BLACK, RED, (i+1)/n_steps),
                        opacity=0.1 + 0.5*(i+1)/n_steps
                    ).stretch_to_fit_height(original_height * (1 + 0.15*(i+1)/n_steps)),
                    run_time=0.3
                )
                self.wait(0.1)

        # Reset everything with voiceover
        with self.voiceover(
            "Now that we've seen both processes individually, let's reset and compare them side by side."
        ):
            self.play(
                FadeOut(cp_subtitle),
                FadeOut(cp_equations),
                FadeOut(info2),
                container.animate.set_fill(None, opacity=0.0).stretch_to_fit_height(original_height)
            )

        # 5. Side-by-side comparison (simplified)
        cv_container = Rectangle(width=2, height=4, stroke_color=WHITE)
        cv_container.move_to(LEFT * 4)
        cv_label = Text("Constant Volume", font_size=24, color=GREEN)
        cv_label.next_to(cv_container, DOWN)
        
        # Volume text and lock for constant volume
        cv_volume_text = Text("VOLUME", font_size=28)
        cv_volume_text.next_to(cv_container, UP, buff=0.2)
        lock_img_comparison = ImageMobject("dataset/AE302/images/lock.png")
        lock_img_comparison.scale(0.12)
        lock_img_comparison.next_to(cv_volume_text, RIGHT, buff=0.1)

        # Right side - Constant Pressure
        cp_container = Rectangle(width=2, height=4, stroke_color=WHITE)
        cp_container.move_to(RIGHT * 4)
        cp_label = Text("Constant Pressure", font_size=24, color=RED)
        cp_label.next_to(cp_container, DOWN)
        
        # Pressure text and gauge for constant pressure
        cp_pressure_text = Text("PRESSURE", font_size=28)
        cp_pressure_text.next_to(cp_container, UP, buff=0.5)

        title = Text("Heat Capacity Comparison", font_size=36).to_edge(UP)
        
        # Final relationship for comparison
        comparison_eq = VGroup(
            MathTex(r"c_p - c_v = \frac{R}{M}").set_color(YELLOW),
            MathTex(r"\gamma = \frac{c_p}{c_v} = \frac{7}{5}").set_color(YELLOW)
        ).arrange(DOWN, buff=0.3)
        comparison_eq.next_to(title, DOWN)
        
        # Create the comparison scene with voiceover
        with self.voiceover(
            "Let's examine both processes simultaneously to understand their key differences. "
            "On the left, we have the constant volume process, where all heat input goes into "
            "increasing the internal energy. On the right, we have the constant pressure process, "
            "where the heat input is split between internal energy and expansion work."
        ):
            self.play(
                FadeOut(container),
                Create(cv_container),
                Create(cp_container),
                Write(cv_label),
                Write(cp_label),
                Write(title)
            )
            self.wait(0.5)
            
            self.play(
                Write(cv_volume_text),
                Write(cp_pressure_text)
            )
            self.play(
                FadeIn(lock_img_comparison) #,
            )

        # Animate both processes simultaneously with detailed explanation
        n_steps = 8
        with self.voiceover(
            "As we add the same amount of heat to both systems, observe the differences. "
            "The constant volume process reaches a higher temperature since all heat goes into internal energy, "
            "while the constant pressure process reaches a lower temperature as some energy is used for expansion work."
        ):
            for i in range(n_steps):
                # Calculate temperature ratios based on cp/cv relationship
                # For diatomic gas (H2), cp/cv = 7/5, so for same heat input:
                # Tv/Tp = cp/cv = 7/5 = 1.4
                cv_temp_ratio = (i+1)/n_steps  # Full temperature rise
                cp_temp_ratio = cv_temp_ratio * (5/7)  # Lower temperature rise due to work

                self.play(
                    cv_container.animate.set_fill(
                        color=interpolate_color(BLACK, RED, cv_temp_ratio),
                        opacity=0.1 + 0.5*cv_temp_ratio
                    ),
                    cp_container.animate.set_fill(
                        color=interpolate_color(BLACK, RED, cp_temp_ratio),
                        opacity=0.1 + 0.5*cp_temp_ratio
                    ).stretch_to_fit_height(4 * (1 + 0.15*(i+1)/n_steps)),
                    run_time=0.3
                )
                self.wait(0.1)

        # Show final relationships with mathematical explanation
        with self.voiceover(
            "Let's understand why gamma, the ratio of specific heats, is always greater than one. "
            "Since cp equals cv plus the gas constant R over mass, cp is always larger than cv. "
            "For our diatomic hydrogen gas, gamma equals seven-fifths or 1.4, "
            "which represents the additional energy needed for expansion work at constant pressure."
        ):
            # First show cp > cv relationship
            relationship_eq = VGroup(
                MathTex(r"c_p = c_v + \frac{R}{M}").set_color(YELLOW),
                MathTex(r"\gamma = \frac{c_p}{c_v} = \frac{c_v + R/M}{c_v} = 1 + \frac{R}{Mc_v}").set_color(YELLOW),
                MathTex(r"\therefore \gamma > 1 \text{ always}").set_color(YELLOW),
                MathTex(r"\text{For }H_2: \gamma = \frac{7}{5} = 1.4").set_color(YELLOW)
            ).arrange(DOWN, buff=0.3)
            relationship_eq.next_to(title, DOWN)
            
            self.play(Write(relationship_eq))
            self.wait(2)

        # Clear scene with concluding remark
        with self.voiceover(
            "This fundamental property, gamma greater than one, is crucial for many thermodynamic processes, "
            "including the efficiency of heat engines and the behavior of shock waves."
        ):
            self.play(
                *[FadeOut(mob) for mob in [
                    cv_container, cp_container, cv_label, cp_label, title,
                    cv_volume_text, lock_img_comparison, cp_pressure_text,
                    relationship_eq
                ]]
            )

    def section4(self):
        # Title Scene at the top
        title = Text("Real-World Applications", font_size=36)
        title.to_edge(UP, buff=0.5)

        # Create a transparent room (5m x 7m x 3.3m)
        # Scale down by factor of 2 for better visualization
        width, length, height = 5/2, 7/2, 3.3/2  # Scaled dimensions in Manim units
        room = ThreeDBox(width=width, height=height, depth=length)
        room.set_fill(opacity=0.1)  # Make it transparent
        room.set_stroke(WHITE, opacity=1)  # White edges
        room.move_to([-3, 0, 0])  # Move room to left side
        
        # Room labels with actual dimensions
        room_labels = VGroup(
            Text("5 m", font_size=16),
            Text("7 m", font_size=16),
            Text("3.3 m", font_size=16)
        )
        room_labels[0].next_to(room, RIGHT, buff=0.2)  # Width
        room_labels[1].next_to(room, UP, buff=0.2)     # Length
        room_labels[2].next_to(room, LEFT, buff=0.2)   # Height

        # Key information display - moved to right side
        key_info = VGroup(
            Text("Room Dimensions:", font_size=16, color=YELLOW),
            MathTex("5\\text{ m} \\times 7\\text{ m} \\times 3.3\\text{ m}").scale(0.5),
            Text("Conditions:", font_size=16, color=YELLOW),
            MathTex("P = 1\\text{ atm}, \\quad T = 25\\text{°C}").scale(0.5)
        ).arrange(DOWN, buff=0.3)
        key_info.next_to(title, LEFT, buff=0.8).shift(DOWN)

        # Initial animation with problem introduction
        with self.voiceover(
            "Let's solve a real-world problem. Consider a rectangular room with dimensions "
            "5 meters by 7 meters, and a height of 3.3 meters. The air inside is at "
            "atmospheric pressure and 25 degrees Celsius. "
            "Calculate the internal energy and enthalpy of the air in the room."
        ):
            self.play(Write(title))
            self.play(
                Create(room),
                Write(room_labels),
                Write(key_info)
            )
            # Initial color fill animation to represent air at room temperature
            self.play(
                room.animate.set_fill(color=interpolate_color(BLUE, RED, 0.3), opacity=0.2),
                run_time=2
            )

        # Show derivation first
        derivation_title = Text("Step-by-Step Solution:", font_size=16, color=YELLOW)
        derivation_title.next_to(title, DOWN+RIGHT*0.6, buff=0.5)

        # Step 1: Calculate volume
        volume_calc = VGroup(
            Text("1. Room Volume:", font_size=16),
            MathTex("V = 5\\text{ m} \\times 7\\text{ m} \\times 3.3\\text{ m} = 115.5\\text{ m}^3").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        volume_calc.next_to(derivation_title, DOWN, buff=0.5).shift(LEFT*2.5)

        with self.voiceover(
            "First, we calculate the room volume. This tells us how much space the air occupies."
        ):
            self.play(Write(derivation_title))
            self.play(Write(volume_calc))
            # Highlight volume calculation with color change
            self.play(
                room.animate.set_fill(color=BLUE, opacity=0.3),
                run_time=1
            )

        # Step 2: Calculate mass using ideal gas law
        mass_calc = VGroup(
            Text("2. Air Mass:", font_size=16),
            MathTex("PV = mRT").scale(0.5),
            MathTex("m = \\frac{PV}{RT} = \\frac{(101325\\text{ Pa})(115.5\\text{ m}^3)}{(287\\text{ J/kg·K})(298\\text{ K})} = 137.8\\text{ kg}").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        mass_calc.next_to(volume_calc, DOWN, buff=0.3)

        with self.voiceover(
            "Using the ideal gas law, we can find the mass of air in the room. "
            "At atmospheric pressure and room temperature, we have about 138 kilograms of air."
        ):
            self.play(Write(mass_calc))
            # Represent increasing density with darker color
            self.play(
                room.animate.set_fill(color=BLUE, opacity=0.5),
                run_time=1
            )

        # Step 3: Calculate internal energy
        energy_calc = VGroup(
            Text("3. Internal Energy:", font_size=16),
            MathTex("E = mc_vT").scale(0.5),
            MathTex("c_v = \\frac{R}{\\gamma-1} = \\frac{287}{1.4-1} = 717.5\\text{ J/kg·K}").scale(0.5),
            MathTex("E = (137.8\\text{ kg})(717.5\\text{ J/kg·K})(298\\text{ K}) = 2.92\\times10^7\\text{ J}").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        energy_calc.next_to(mass_calc, DOWN, buff=0.3)

        with self.voiceover(
            "For internal energy, we use E equals m cv T. The specific heat at constant volume "
            "represents the energy needed to raise the temperature when we don't let the gas expand."
        ):
            self.play(Write(energy_calc))
            # Show increasing internal energy with warmer color
            self.play(
                room.animate.set_fill(color=interpolate_color(BLUE, RED, 0.6), opacity=0.5),
                run_time=2
            )

        # Step 4: Calculate enthalpy
        enthalpy_calc = VGroup(
            Text("4. Enthalpy:", font_size=16),
            MathTex("H = mc_pT").scale(0.5),
            MathTex("c_p = c_v + R = 717.5 + 287 = 1004.5\\text{ J/kg·K}").scale(0.5),
            MathTex("H = (137.8\\text{ kg})(1004.5\\text{ J/kg·K})(298\\text{ K}) = 4.08\\times10^7\\text{ J}").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        enthalpy_calc.next_to(energy_calc, DOWN, buff=0.3)

        with self.voiceover(
            "Finally, enthalpy adds the potential for the gas to do work. That's why we use cp instead of cv. "
            "The difference, R, represents the additional energy available for expansion work."
        ):
            self.play(Write(enthalpy_calc))
            # Show final state with full energy content
            self.play(
                room.animate.set_fill(color=RED, opacity=0.6),
                run_time=2
            )

        # Final results box
        results = VGroup(
            Text("Final Results:", font_size=20, color=YELLOW),
            MathTex("E = 2.92\\times10^7\\text{ J}"),
            MathTex("H = 4.08\\times10^7\\text{ J}")
        ).arrange(DOWN, buff=0.2)
        results.next_to(room, DOWN, buff=0.5)

        with self.voiceover(
            "Our calculations show that the internal energy is 2.92 times 10 to the 7th Joules, "
            "and the enthalpy is 4.08 times 10 to the 7th Joules. The difference between these values "
            "represents the potential work energy stored in the gas under constant pressure conditions."
        ):
            self.play(Write(results))
            self.wait(2)

        # Clear scene
        self.play(
            *[FadeOut(mob) for mob in [
                title, room, room_labels, key_info,
                derivation_title, volume_calc, mass_calc,
                energy_calc, enthalpy_calc, results
            ]]
        )

    def section5(self):
        # PART 1: Formal Statement of the Law
        title = Text("First Law of Thermodynamics", font_size=36, color=YELLOW)
        title.to_edge(UP)

        # Formal statement
        formal_statement = Text(
            "Conservation of Energy in Thermodynamic Systems",
            font_size=24
        ).next_to(title, DOWN)

        # Main equation
        main_eq = MathTex("\\delta e = \\delta q + \\delta w").scale(1.2)
        main_eq.next_to(formal_statement, DOWN, buff=0.5)

        # Terms explanation
        terms = VGroup(
            MathTex("\\delta e:\\text{ change in internal energy}"),
            MathTex("\\delta q:\\text{ heat added to system}"),
            MathTex("\\delta w:\\text{ work done by surroundings}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        terms.next_to(main_eq, DOWN, buff=0.5)

        with self.voiceover(
           "Before we continue, let's remind ourselves what is actually happening inside the gas when we add heat."
            "Heat increases the speed of the molecules — that's the internal energy increase."
            "But if the gas is allowed to expand, some of this energy also gets used to push against the surrounding pressure — this is the work term."
            "This balance between energy going into molecular motion and expansion is exactly what the First Law describes."
            "The First Law of Thermodynamics is a formal statement of the principle of conservation of energy as applied to thermodynamic systems."
        ):
            self.play(Write(title))
            self.play(Write(formal_statement))
            self.play(Write(main_eq))
            self.play(Write(terms))
            self.wait(1)
        with self.voiceover(
            "These ideas form the foundation for everything that follows in thermodynamics — from heat engines and refrigerators, to atmospheric science and chemical reactions."
            "And at the center of it all stands the First Law of Thermodynamics:the universal rule that energy can change form — between heat, work, and internal energy — but it can never be created or destroyed."
            "Understanding this law gives us the power to analyze, predict, and control energy transformations in the physical world."
        ):
            self.play(
                FadeOut(formal_statement),
                FadeOut(terms)
            )
            self.wait(1)

        

class ThreeDBox(VGroup):
    def __init__(self, width=2, height=2, depth=2, **kwargs):
        super().__init__(**kwargs)
        
        # Store dimensions
        self.width = width
        self.height = height
        self.depth = depth
        
        # Create the vertices
        vertices = np.array([
            [0, 0, 0],
            [width, 0, 0],
            [width, height, 0],
            [0, height, 0],
            [0, 0, depth],
            [width, 0, depth],
            [width, height, depth],
            [0, height, depth],
        ])
        
        # Create edges
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
            (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting edges
        ]
        
        # Add all lines to the VGroup
        for start, end in edges:
            self.add(Line3D(
                start=vertices[start],
                end=vertices[end],
                color=WHITE
            ))

if __name__ == "__main__":
    from manim import config
    #config.quality = "low_quality"
    config.quality = "high_quality"
    config.disable_caching = False

    scene = IdealGas2()
    scene.render() 