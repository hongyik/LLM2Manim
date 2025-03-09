from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Initialize the GTTS service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))

        title = Text("Material Derivative", font_size=48)
        with self.voiceover(text="Let's learn about the Material Derivative.") as tracker:
            self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        definition = Tex(
            r"The Material Derivative is the derivative of a quantity ",
            r"with respect to a moving reference frame.",
            font_size=36
        )
        
        with self.voiceover(
            text="The Material Derivative is a fundamental concept that helps us understand "
            "how quantities change when measured from a moving reference frame."
        ) as tracker:
            self.play(Write(definition))
        
        self.wait(0.5)
        
        with self.voiceover(
            text="This is particularly important when studying fluid dynamics, "
            "heat transfer, and other phenomena where motion plays a crucial role."
        ) as tracker:
            self.wait(2)
        
        self.play(FadeOut(title), FadeOut(definition))
        #the material derivative of some quantity Q could be temperature could be velocity is basically the rate of change of Q belonging to a certain particle moving within a material or a substance the material derivative
        #  by the way is denoted by DQ by DT but the D's are now capitalized as opposed to the regular ordinary derivative 
        # Material Derivative Introduction with synchronized voiceover
        explanation1 = Tex(
            r"The material derivative of some quantity $Q$\\",
            r"(like temperature or velocity)\\",
            r"is the rate of change of $Q$\\",
            r"for a particle moving within a material or substance",
            font_size=36
        ).arrange(DOWN, aligned_edge=LEFT)
        
        notation = MathTex(
            r"\frac{DQ}{Dt}",  # Capital D notation
            r"\quad \text{vs.} \quad",
            r"\frac{dQ}{dt}",  # Regular derivative
            font_size=48
        )
        
        # Animate with voiceover
        with self.voiceover(
            text="The material derivative of some quantity Q could be temperature or velocity. "
            "It's basically the rate of change of Q belonging to a certain particle moving within "
            "a material or substance."
        ) as tracker:
            self.play(Write(explanation1[0]))
            self.play(Write(explanation1[1]))
            self.play(Write(explanation1[2:]))
        
        # Move explanation up and show notation
        with self.voiceover(
            text="By the way, the material derivative is denoted by DQ by DT, "
            "where the D's are capitalized, as opposed to the regular ordinary derivative."
                    ) as tracker:
            self.play(explanation1.animate.to_edge(UP))
            self.play(Write(notation))
            self.play(
                notation[0].animate.set_color(YELLOW),
                notation[1].animate.set_color(RED),
                notation[2].animate.set_color(BLUE)
            )
        self.wait(0.5)
        
        # Clean up
        self.play(
            FadeOut(explanation1),
            FadeOut(notation)
        )
        
        # Material Derivative equation demonstration
        equation = MathTex(
            r"\frac{D Q}{D t}", r"=", r"\frac{\partial Q}{\partial t}", r"+", r"\mathbf{v} \cdot \nabla Q",
            font_size=48
        ).center()  # Center the equation vertically
        
        # Labels for each term
        total_change = Text("Total Change", font_size=24, color=YELLOW)
        temporal_change = Text("Temporal Change\n(Change at fixed position)", font_size=24, color=RED)
        convective_change = Text("Convective Change\n(Change due to motion)", font_size=24, color=BLUE)
        
        # Position labels - temporal change above, others below
        total_change.next_to(equation[0], DOWN, buff=0.75)
        temporal_change.next_to(equation[2], UP, buff=0.75)  # Changed to UP
        convective_change.next_to(equation[4], DOWN, buff=0.75)
        
        # Arrows connecting terms to labels
        arrow1 = Arrow(start=equation[0].get_bottom(), end=total_change.get_top(), color=YELLOW)
        arrow2 = Arrow(start=equation[2].get_top(), end=temporal_change.get_bottom(), color=RED)  # Changed direction
        arrow3 = Arrow(start=equation[4].get_bottom(), end=convective_change.get_top(), color=BLUE)
        
        with self.voiceover(
            text="The material derivative can be broken down into two main components."
        ):
            self.play(Write(equation))
            self.wait(0.5)
        
        with self.voiceover(
            text="The left side represents the total rate of change of quantity Q "
            "following a moving particle."
        ):
            self.play(
                equation[0].animate.set_color(YELLOW),
                Create(arrow1),
                Write(total_change)
            )
        
        with self.voiceover(
            text="The first term on the right is the temporal change term. "
            "It represents how Q changes with time at a fixed position."
        ):
            self.play(
                equation[2].animate.set_color(RED),
                Create(arrow2),
                Write(temporal_change)
            )
        
        with self.voiceover(
            text="The second term is the convective change term. "
            "It accounts for changes in Q due to the particle's motion through space, "
            "where v is the velocity and nabla Q is the spatial gradient of Q."
        ):
            self.play(
                equation[4].animate.set_color(BLUE),
                Create(arrow3),
                Write(convective_change)
            )
        
        self.wait(1)
        
        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in [
                equation, total_change, temporal_change, convective_change,
                arrow1, arrow2, arrow3
            ]]
        )

        # Temperature example
        # an example of an important material derivative is temperature if I have a fluid in space with a fluid particle P inside that fluid the material derivative of P's temperature tells me how quickly the temperature changes as my particle moves around in this fluid or in this material now in general the temperature of the particle p is a function of the position of P given by XP YP and zp as well as a function of time this function just shows that there could be an external source of heat that's changing the temperature of this fluid from the outside as a function of time that's why the t is inside the brackets

         # Temperature example
        temp_title = Text("Temperature Example", font_size=36)
        
        with self.voiceover(
            text="Let's look at an important example of the material derivative: temperature."
        ):
            self.play(Write(temp_title))
        
        # Create fluid container and setup
        container = Rectangle(height=4, width=6, color=BLUE)
        container.set_fill(BLUE_E, opacity=0.3)
        
        particle = Dot(color=YELLOW)
        particle.move_to(container.get_center() + LEFT*2 + DOWN)
        
        temp_gradient = Rectangle(height=4, width=6)
        temp_gradient.set_fill(
            color=[RED_A, RED_C, RED_E], 
            opacity=[0.3, 0.5, 0.7]
        )
        temp_gradient.move_to(container.get_center())
        
        p_label = Tex("P", font_size=24).next_to(particle, UP*0.5)
        temp_label = Tex("T(x,y,z,t)", font_size=24).to_edge(RIGHT)
        
        with self.voiceover(
            text="If we have a fluid in space with a fluid particle P inside, "
            "the material derivative of P's temperature tells us how quickly "
            "the temperature changes as our particle moves around in this fluid."
        ):
            self.play(
                FadeIn(container),
                FadeIn(temp_gradient),
                Create(particle),
                Write(p_label)
            )
            self.play(Write(temp_label))
        
        with self.voiceover(
            text="In general, the temperature of particle P is a function of its position, "
            "given by x, y, and z coordinates, as well as time. "
            "The time dependence shows that there could be external sources "
            "changing the fluid's temperature from the outside."
        ):
            movement = [
                particle.animate.shift(RIGHT*3 + UP),
                p_label.animate.shift(RIGHT*3 + UP)
            ]
            self.play(*movement, run_time=3)
        
        self.wait(0.5)
        
        # Cleanup
        self.play(
            FadeOut(container),
            FadeOut(temp_gradient),
            FadeOut(particle),
            FadeOut(p_label),
            FadeOut(temp_label),
            FadeOut(temp_title)
        )

        #3D coordinate graph demonstration

        #Intuiation with different senarios

        #example 1
        # Set up 3D coordinate system first
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        
        # Create camera orientation
        # self.set_camera_orientation(
        #     phi=75 * DEGREES,    # Angle from positive z-axis (vertical angle)
        #     theta=30 * DEGREES,  # Rotation around z-axis (horizontal angle)
        #     gamma=0 * DEGREES,   # Camera rotation
        #     zoom=1.0            # Zoom level
        # )
        
        # Labels for axes with better 3D positioning adjusted for camera angle
        x_label = axes.get_x_axis_label("x")
        x_label.rotate(90 * DEGREES, axis=RIGHT)
        x_label.shift(IN * 0.5 + RIGHT * 0.5)
        
        y_label = axes.get_y_axis_label("y")
        y_label.rotate(90 * DEGREES, axis=UP)
        y_label.shift(OUT * 0.5 + UP * 0.2)
        
        z_label = axes.get_z_axis_label("z").rotate(90 * DEGREES)
        
        # Group labels for easier manipulation
        labels = VGroup(x_label, y_label, z_label)        
        # Create transparent cube for container
        cube = Cube(side_length=4, fill_opacity=0.1, stroke_width=1)
        cube.set_color(BLUE)
        
        # Add coordinate grid lines for better depth perception
        grid_xy = NumberPlane(
            x_range=[-2, 2], y_range=[-2, 2],
            background_line_style={"stroke_opacity": 0.2}
        ).set_stroke(width=0.5)
        grid_xz = grid_xy.copy().rotate(90 * DEGREES, RIGHT)
        grid_yz = grid_xy.copy().rotate(90 * DEGREES, UP)
        
        # Show coordinate system and container first
        with self.voiceover(
            text="Let's visualize this in three dimensions."
        ):
            self.play(
                Create(axes),
                Create(grid_xy),
                Create(grid_xz),
                Create(grid_yz),
                Write(labels),
                Create(cube)
            )
        
        # Now add particle and its movement
        particle_3d = Sphere(radius=0.1, color=YELLOW)
        particle_3d.move_to(axes.c2p(-1, -1, -1))
        p_label_3d = MathTex("P", color=YELLOW).next_to(particle_3d, UP+RIGHT+OUT)
        
        with self.voiceover(
            text="Consider a particle P in this space."
        ):
            self.play(
                Create(particle_3d),
                Write(p_label_3d)
            )
        
        # Create path for particle movement
        def get_particle_movement(t):
            return axes.c2p(
                2 * np.cos(t) - 1,  
                2 * np.sin(t) - 1,  
                np.sin(2*t)         
            )
        
        def update_label(mob):
            mob.next_to(particle_3d, UP+RIGHT+OUT)
        
        p_label_3d.add_updater(update_label)
        
        # Animate particle movement while keeping coordinate system visible
        with self.voiceover(
            text="As the particle moves through the fluid, its position changes in all three dimensions, "
            "affecting how it experiences temperature changes in the system."
        ):
            self.play(
                MoveAlongPath(
                    particle_3d,
                    ParametricFunction(
                        get_particle_movement,
                        t_range=[0, 2*PI],
                        color=YELLOW_A
                    )
                ),
                run_time=6,
                rate_func=linear
            )
        
        p_label_3d.clear_updaters()
        
        # Instead of removing particle, move the entire system to the left
        coordinate_system_group = VGroup(
            axes, cube, grid_xy, grid_xz, grid_yz,
            labels,
            particle_3d, p_label_3d
        )
        
        with self.voiceover(
            text="Now, let's derive the mathematical expression for the material derivative, "
            "keeping our moving particle in mind."
        ):
            self.play(
                coordinate_system_group.animate.scale(0.6).to_edge(LEFT)
            )
        
        # # Then reset camera to normal position
        #     self.move_camera(
        #         phi=0 * DEGREES,    # Reset to front view
        #         theta=0 * DEGREES,  # Reset to front view
        #         gamma=0 * DEGREES,  # No rotation
        #         zoom=1.0,
        #         run_time=1.5
        #     )
        # Start the derivation on the right side
        # Step 1: Position definition
        step1 = MathTex(
            r"T_p = T_p[x_p(t), y_p(t), z_p(t), t]",
            font_size=32
        ).to_edge(UP)#.shift(RIGHT * 3)  # Position at top and right side
        
        with self.voiceover(
            text="First, we define the temperature of the moving particle P "
            "by noting its position coordinates as functions of time."
        ):
            self.play(Write(step1))
        
        # Step 2: Chain Rule (single line)
        step2 = MathTex(
            r"\frac{dT_p}{dt} = \frac{\partial T_p}{\partial t} + "
            r"\left(\frac{\partial T_p}{\partial x_p}\right)\frac{dx_p}{dt} + "
            r"\left(\frac{\partial T_p}{\partial y_p}\right)\frac{dy_p}{dt} + "
            r"\left(\frac{\partial T_p}{\partial z_p}\right)\frac{dz_p}{dt}",
            font_size=32
        ).next_to(step1, DOWN, buff=0.7)
        
        with self.voiceover(
            text="Using the chain rule, we express the total time derivative "
            "as the sum of partial derivatives with respect to each variable."
        ):
            self.play(Write(step2))
        
        # Step 3: Velocity substitution (single line)
        step3 = MathTex(
            r"\frac{dx_p}{dt} = v_x, \quad \frac{dy_p}{dt} = v_y, \quad \frac{dz_p}{dt} = v_z",
            font_size=32
        ).next_to(step2, DOWN, buff=0.7)
        
        with self.voiceover(
            text="We recognize these time derivatives as components of the particle's velocity."
        ):
            self.play(Write(step3))
        
        # Step 4: Substituted form (single line)
        step4 = MathTex(
            r"\frac{dT_p}{dt} = \frac{\partial T_p}{\partial t} + "
            r"v_x\frac{\partial T_p}{\partial x_p} + "
            r"v_y\frac{\partial T_p}{\partial y_p} + "
            r"v_z\frac{\partial T_p}{\partial z_p}",
            font_size=32
        ).next_to(step3, DOWN, buff=0.7)
        
        with self.voiceover(
            text="Substituting these velocities gives us this expanded form."
        ):
            self.play(Write(step4))
        
        # Step 5: Final compact form
        step5 = MathTex(
            r"\frac{DT_p}{Dt} = \frac{\partial T_p}{\partial t} + \mathbf{v} \cdot \nabla T_p",
            font_size=36
        ).next_to(step4, DOWN, buff=0.7)
        
        with self.voiceover(
            text="Finally, we can write this succinctly using vector notation, "
            "where v dot nabla T_p represents the spatial variation term."
        ):
            self.play(
                Write(step5),
                step5.animate.set_color_by_tex_to_color_map({
                    r"\frac{DT_p}{Dt}": YELLOW,
                    r"\frac{\partial T_p}{\partial t}": RED,
                    r"\mathbf{v} \cdot \nabla T_p": BLUE
                })
            )
        
        self.wait(1)
        self.play(
            FadeOut(coordinate_system_group),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(step4),
            FadeOut(step5),
        )
        self.wait(2)
    # Senario 1
            # Create a pipe visualization
        pipe = Rectangle(height=2, width=6, color=WHITE)
        pipe.set_fill(opacity=0)
        
        # Create temperature gradient
        gradient = Rectangle(height=2, width=6)
        gradient.set_fill(
            color=[BLUE_C, RED_C], 
            opacity=[0.3, 0.7]
        )
        gradient.move_to(pipe.get_center())
        
        # Temperature labels
        temp_200 = MathTex("200K", color=BLUE).next_to(pipe, LEFT)
        temp_300 = MathTex("300K", color=RED).next_to(pipe, RIGHT)
        
        # Particle P
        particle = Dot(color=YELLOW)
        particle.move_to(pipe.get_left() + RIGHT * 0.5)
        p_label = MathTex("P", color=YELLOW).next_to(particle, UP)
        
        # Show setup with voiceover
        with self.voiceover(
            text="Consider a rectangular pipe with a temperature gradient. "
            "The left end is maintained at 200 Kelvin by a cooler, "
            "while the right end is kept at 300 Kelvin by a heat source."
        ):
            self.play(
                Create(pipe),
                FadeIn(gradient),
                Write(temp_200),
                Write(temp_300)
            )
        
        with self.voiceover(
            text="Let's place a fluid particle P at the left end of the pipe."
        ):
            self.play(
                Create(particle),
                Write(p_label)
            )
        
        # Show material derivative equation for this case
        eq1 = MathTex(
            r"\frac{DT}{Dt} = \frac{\partial T}{\partial t} + \mathbf{v} \cdot \nabla T",
            font_size=36
        ).to_edge(UP)
        
        with self.voiceover(
            text="In this scenario, if we don't change the temperature settings over time, "
            "the partial derivative of temperature with respect to time is zero."
        ):
            self.play(Write(eq1))
            self.play(eq1[0][8:19].animate.set_color(RED))  # Highlight ∂T/∂t term
        
        # Show steady state condition
        steady_state = MathTex(
            r"\frac{\partial T}{\partial t} = 0 \quad \text{(steady state)}",
            font_size=32
        ).next_to(eq1, DOWN)
        
        with self.voiceover(
            text="And if the fluid is stationary, all velocity terms are also zero."
        ):
            self.play(Write(steady_state))
        
        # Show zero velocity condition
        zero_vel = MathTex(
            r"\mathbf{v} = \mathbf{0} \quad \text{(stationary fluid)}",
            font_size=32
        ).next_to(steady_state, DOWN)
        
        with self.voiceover(
            text="Therefore, even though the temperature varies with position along the pipe, "
            "the material derivative is zero."
        ):
            self.play(Write(zero_vel))
        
        # Final result
        result = MathTex(
            r"\frac{DT}{Dt} = 0",
            font_size=36
        ).next_to(zero_vel, DOWN)
        
        with self.voiceover(
            text="This means the particle's temperature remains constant at its fixed position, "
            "which makes intuitive sense since it's not moving and the temperature profile isn't changing."
        ):
            self.play(Write(result))
            self.wait(1)
        
        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in [
                pipe, gradient, temp_200, temp_300,
                particle, p_label,
                eq1, steady_state, zero_vel, result
            ]]
        )
    #Senario 2
            # Create pipe visualization for second scenario
        pipe = Rectangle(height=2, width=6, color=WHITE)
        pipe.set_fill(opacity=0)
        
        # Initial temperature gradient
        gradient = Rectangle(height=2, width=6)
        gradient.set_fill(
            color=[BLUE_C, RED_C], 
            opacity=[0.3, 0.7]
        )
        gradient.move_to(pipe.get_center())
        
        # Temperature labels (will be updated)
        temp_left = MathTex("200K", color=BLUE).next_to(pipe, LEFT)
        temp_right = MathTex("300K", color=RED).next_to(pipe, RIGHT)
        
        # Particle P (stationary)
        particle = Dot(color=YELLOW)
        particle.move_to(pipe.get_left() + RIGHT * 0.5)
        p_label = MathTex("P", color=YELLOW).next_to(particle, UP)
        
        # Show initial setup
        with self.voiceover(
            text="In our second scenario, let's keep particle P stationary at the left end, "
            "but now we'll uniformly change the temperature from 200 Kelvin to 250 Kelvin over 10 seconds."
        ):
            self.play(
                Create(pipe),
                FadeIn(gradient),
                Write(temp_left),
                Write(temp_right),
                Create(particle),
                Write(p_label)
            )
        
        # Animate temperature change
        temp_tracker = ValueTracker(200)
        temp_left.add_updater(
            lambda m: m.become(
                MathTex(f"{int(temp_tracker.get_value())}K", color=interpolate_color(BLUE, YELLOW, 
                    (temp_tracker.get_value()-200)/50)).next_to(pipe, LEFT)
            )
        )
        
        with self.voiceover(
            text="As we increase the temperature at the left end, "
            "the particle experiences this temperature change directly."
        ):
            self.play(
                temp_tracker.animate.set_value(250),
                gradient.animate.set_fill(
                    color=[YELLOW, RED_C],
                    opacity=[0.3, 0.7]
                ),
                run_time=3
            )
        
        # Show material derivative equation for this case
        eq1 = MathTex(
            r"\frac{DT}{Dt} = \frac{\partial T}{\partial t} + \mathbf{v} \cdot \nabla T",
            font_size=36
        ).to_edge(UP)
        
        with self.voiceover(
            text="In this case, while the velocity terms are still zero since the particle isn't moving..."
        ):
            self.play(Write(eq1))
        
        # Show velocity condition
        vel_eq = MathTex(
            r"\mathbf{v} = \mathbf{0} \quad \rightarrow \quad \mathbf{v} \cdot \nabla T = 0",
            font_size=32
        ).next_to(eq1, DOWN)
        
        self.play(Write(vel_eq))
        
        # Show temperature rate
        temp_rate = MathTex(
            r"\frac{\partial T}{\partial t} = \frac{250K - 200K}{10s} = 5 \frac{K}{s}",
            font_size=32
        ).next_to(vel_eq, DOWN)
        
        with self.voiceover(
            text="The partial derivative of temperature with respect to time is now 5 Kelvin per second, "
            "as the temperature increases from 200 to 250 Kelvin over 10 seconds."
        ):
            self.play(Write(temp_rate))
        
        # Final result
        result = MathTex(
            r"\frac{DT}{Dt} = 5 \frac{K}{s}",
            font_size=36
        ).next_to(temp_rate, DOWN)
        
        with self.voiceover(
            text="Therefore, the material derivative equals 5 Kelvin per second, "
            "which matches our intuition about how quickly the particle's temperature is changing."
        ):
            self.play(Write(result))
        
        self.wait(1)
        
        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in [
                pipe, gradient, temp_left, temp_right,
                particle, p_label,
                eq1, vel_eq, temp_rate, result
            ]]
        )
    #senario 3
            # Create pipe visualization for third scenario
        pipe = Rectangle(height=2, width=6, color=WHITE)
        pipe.set_fill(opacity=0)
        
        # Temperature gradient (steady)
        gradient = Rectangle(height=2, width=6)
        gradient.set_fill(
            color=[BLUE_C, RED_C], 
            opacity=[0.3, 0.7]
        )
        gradient.move_to(pipe.get_center())
        
        # Temperature labels
        temp_left = MathTex("200K", color=BLUE).next_to(pipe, LEFT)
        temp_right = MathTex("300K", color=RED).next_to(pipe, RIGHT)
        
        # Particle P (will move)
        particle = Dot(color=YELLOW)
        particle.move_to(pipe.get_left() + RIGHT * 0.5)
        p_label = MathTex("P", color=YELLOW).next_to(particle, UP)
        
        # Show setup
        with self.voiceover(
            text="In our third scenario, let's return to our original pipe with steady temperatures, "
            "but now we'll move particle P from the left end to the right end over 10 seconds."
        ):
            self.play(
                Create(pipe),
                FadeIn(gradient),
                Write(temp_left),
                Write(temp_right),
                Create(particle),
                Write(p_label)
            )
        
        # Material derivative equation
        eq1 = MathTex(
            r"\frac{DT}{Dt} = \frac{\partial T}{\partial t} + \mathbf{v} \cdot \nabla T",
            font_size=36
        ).to_edge(UP)
        
        with self.voiceover(
            text="In the material derivative equation, since the temperature profile is steady..."
        ):
            self.play(Write(eq1))
        
        # Show steady state condition
        steady_state = MathTex(
            r"\frac{\partial T}{\partial t} = 0 \quad \text{(steady profile)}",
            font_size=32
        ).next_to(eq1, DOWN)
        
        self.play(Write(steady_state))
        
        # Show velocity components
        vel_components = MathTex(
            r"v_y = v_z = 0, \quad v_x = \frac{6\text{ units}}{10\text{ s}} = 0.6 \text{ units/s}",
            font_size=32
        ).next_to(steady_state, DOWN)
        
        with self.voiceover(
            text="The particle only moves in the x direction, with a velocity of 0.6 units per second."
        ):
            self.play(Write(vel_components))
        
        # Add updater for particle label
        p_label.add_updater(lambda m: m.next_to(particle, UP))
        
        # Move particle
        with self.voiceover(
            text="As the particle moves through the temperature gradient, "
            "it experiences a temperature change of 100 Kelvin over 10 seconds."
        ):
            self.play(
                particle.animate.move_to(pipe.get_right() + LEFT * 0.5),
                run_time=3
            )
        
        # Final rate equation
        rate_eq = MathTex(
            r"\frac{DT}{Dt} = v_x \frac{\partial T}{\partial x} = "
            r"0.6 \cdot \frac{300K - 200K}{6\text{ units}} = 10 \frac{K}{s}",
            font_size=32
        ).next_to(vel_components, DOWN)
        
        with self.voiceover(
            text="This gives us a material derivative of 10 Kelvin per second, "
            "which is the product of the particle's velocity and the temperature gradient."
        ):
            self.play(Write(rate_eq))
        
        # Note about velocity effect
        velocity_note = MathTex(
            r"\text{Higher }v_x \text{ or } \frac{\partial T}{\partial x} \implies \text{ Higher } \frac{DT}{Dt}",
            font_size=32
        ).next_to(rate_eq, DOWN)
        
        with self.voiceover(
            text="If the particle moved faster, or if the temperature gradient were steeper, "
            "the rate of temperature change would be even greater."
        ):
            self.play(Write(velocity_note))
        
        self.wait(1)
        
        # Cleanup
        p_label.clear_updaters()
        self.play(
            *[FadeOut(mob) for mob in [
                pipe, gradient, temp_left, temp_right,
                particle, p_label,
                eq1, steady_state, vel_components, rate_eq, velocity_note
            ]]
        )
    # Senario 4       
    # Create pipe visualization for final scenario
        pipe = Rectangle(height=2, width=6, color=WHITE)
        pipe.set_fill(opacity=0)
        
        # Initial temperature gradient
        gradient = Rectangle(height=2, width=6)
        gradient.set_fill(
            color=[BLUE_C, RED_C], 
            opacity=[0.3, 0.7]
        )
        gradient.move_to(pipe.get_center())
        
        # Temperature labels (will be updated)
        temp_left = MathTex("200K", color=BLUE).next_to(pipe, LEFT)
        temp_right = MathTex("300K", color=RED).next_to(pipe, RIGHT)
        
        # Particle P (will move)
        particle = Dot(color=YELLOW)
        particle.move_to(pipe.get_left() + RIGHT * 0.5)
        p_label = MathTex("P", color=YELLOW).next_to(particle, UP)
        
        # Show setup
        with self.voiceover(
            text="In our final scenario, we'll combine both effects: "
            "the particle will move to the right while we simultaneously "
            "increase the left end temperature from 200 to 250 Kelvin."
        ):
            self.play(
                Create(pipe),
                FadeIn(gradient),
                Write(temp_left),
                Write(temp_right),
                Create(particle),
                Write(p_label)
            )
        
        # Setup temperature tracker and updater
        temp_tracker = ValueTracker(200)
        temp_left.add_updater(
            lambda m: m.become(
                MathTex(f"{int(temp_tracker.get_value())}K", 
                color=interpolate_color(BLUE, YELLOW, 
                    (temp_tracker.get_value()-200)/50)).next_to(pipe, LEFT)
            )
        )
        p_label.add_updater(lambda m: m.next_to(particle, UP))
        
        # Material derivative equation
        eq1 = MathTex(
            r"\frac{DT}{Dt} = \frac{\partial T}{\partial t} + \mathbf{v} \cdot \nabla T",
            font_size=36
        ).to_edge(UP)
        
        # Animate combined motion and heating
        with self.voiceover(
            text="As the particle moves through the pipe and the temperature profile changes, "
            "both terms in the material derivative become important."
        ):
            self.play(
                particle.animate.move_to(pipe.get_right() + LEFT * 0.5),
                temp_tracker.animate.set_value(250),
                gradient.animate.set_fill(
                    color=[YELLOW, RED_C],
                    opacity=[0.3, 0.7]
                ),
                Write(eq1),
                run_time=4
            )
        
        # Show the two contributions
        temporal_term = MathTex(
            r"\frac{\partial T}{\partial t} = 5 \frac{K}{s}",
            r"\text{ (heating)}",
            font_size=32
        ).next_to(eq1, DOWN)
        
        spatial_term = MathTex(
            r"\mathbf{v} \cdot \nabla T = 10 \frac{K}{s}",
            r"\text{ (motion)}",
            font_size=32
        ).next_to(temporal_term, DOWN)
        
        with self.voiceover(
            text="The temporal term contributes 5 Kelvin per second due to heating, "
            "while the spatial term adds 10 Kelvin per second due to motion."
        ):
            self.play(
                Write(temporal_term),
                temporal_term[0].animate.set_color(RED)
            )
            self.play(
                Write(spatial_term),
                spatial_term[0].animate.set_color(BLUE)
            )
        
        # Total rate
        total_rate = MathTex(
            r"\frac{DT}{Dt} = 15 \frac{K}{s}",
            r"\text{ (total rate)}",
            font_size=36
        ).next_to(spatial_term, DOWN)
        
        with self.voiceover(
            text="Adding these contributions gives us the total rate of "
            "temperature change experienced by the particle: 15 Kelvin per second."
        ):
            self.play(
                Write(total_rate),
                total_rate[0].animate.set_color(YELLOW)
            )
        
        # Final explanation
        explanation = Text(
            "The material derivative combines both effects:",
            font_size=24
        ).next_to(total_rate, DOWN, buff=0.5)
        
        points = VGroup(
            Text("• Changes due to motion in non-uniform fields", font_size=24),
            Text("• Changes due to time-varying fields", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(explanation, DOWN)
        
        with self.voiceover(
            text="This demonstrates how the material derivative captures both "
            "the effect of motion through non-uniform fields and "
            "the effect of time-varying fields themselves."
        ):
            self.play(
                Write(explanation),
                Write(points)
            )
        
        self.wait(1)
        
        # Cleanup
        temp_left.clear_updaters()
        p_label.clear_updaters()
        self.play(
            *[FadeOut(mob) for mob in [
                pipe, gradient, temp_left, temp_right,
                particle, p_label, eq1, temporal_term, 
                spatial_term, total_rate, explanation, points
            ]]
        )
        # Conclusion
        # Create final summary equation
        final_eq = MathTex(
            r"\frac{DQ}{Dt} = \frac{\partial Q}{\partial t} + \mathbf{v} \cdot \nabla Q",
            font_size=48
        )

        # Create circular motion path for a particle
        radius = 1.5
        particle = Dot(color=YELLOW)
        
        def get_particle_pos(t):
            return np.array([
                radius * np.cos(t),
                radius * np.sin(t),
                0
            ])
        
        # Create gradient background
        gradient_field = Rectangle(
            width=4, height=4,
            fill_opacity=0.3,
            stroke_width=0
        ).set_fill(
            color=[BLUE_A, RED_A],
            opacity=[0.2, 0.4]
        ).shift(UP * 0.5)

        with self.voiceover(
            text="Hopefully these examples have given you a good intuition for the material derivative "
            "and how it combines both the effects of motion through non-uniform fields "
            "and the direct changes of those fields over time. "
            "This powerful concept is essential for understanding fluid dynamics, heat transfer, "
            "and many other physical phenomena involving moving reference frames."
        ):
            # Show equation first
            self.play(Write(final_eq))
            self.play(final_eq.animate.to_edge(UP))
            
            # Add gradient field and particle
            self.play(
                FadeIn(gradient_field),
                FadeIn(particle)
            )
            
            # Animate particle motion while gradient changes color
            self.play(
                MoveAlongPath(
                    particle,
                    ParametricFunction(
                        lambda t: final_eq.get_center() + get_particle_pos(t),
                        t_range=[0, 4*PI],
                        color=YELLOW_A
                    )
                ),
                gradient_field.animate.set_fill(
                    color=[RED_A, BLUE_A],
                    opacity=[0.4, 0.2]
                ),
                run_time=8,
                rate_func=linear
            )
            
            self.play(
                *[FadeOut(mob) for mob in [final_eq, gradient_field, particle]]
            )