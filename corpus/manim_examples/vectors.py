from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np


class VectorInterpretationsScene(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections
        self.section1()
        self.wait(1)
        self.clear()
        self.section2()
        self.wait(1)
        self.clear()
        self.section3()
        self.wait(1)
        self.clear()
        self.section4()
        self.wait(1)
    def section1(self):
        # Opening Scene
        vector_text = Text("VECTOR", font_size=72)
        
        with self.voiceover(text="Welcome to our exploration of vectors, the fundamental building blocks of linear algebra. Let's examine three different perspectives on what vectors are and how they're used.") as tracker:
            self.play(Write(vector_text))
            self.wait(tracker.duration)
        
        # Split into three paths
        physics = Text("Physics", font_size=36, color=BLUE)
        cs = Text("Computer Science", font_size=36, color=GREEN)
        math = Text("Mathematics", font_size=36, color=RED)
        
        # Position the labels
        physics.next_to(vector_text, UP, buff=1)
        cs.next_to(vector_text, LEFT, buff=1)
        math.next_to(vector_text, RIGHT, buff=1)
        
        # Create connecting lines
        line1 = Line(vector_text.get_top(), physics.get_bottom())
        line2 = Line(vector_text.get_left(), cs.get_right())
        line3 = Line(vector_text.get_right(), math.get_left())
        
        with self.voiceover(text="We'll explore vectors from three distinct but related perspectives: the physics perspective, the computer science perspective, and the mathematician's perspective.") as tracker:
            self.play(
                Transform(vector_text, VGroup(physics, cs, math)),
                Create(line1),
                Create(line2),
                Create(line3)
            )
            self.wait(tracker.duration)
        
        self.clear()
        
        # Physics Perspective
        title = Text("1. Physics Perspective", font_size=36, color=BLUE)
        self.play(Write(title))
        
        # Create a clean 2D space with grid
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        
        # Create initial vector
        vector = Arrow(start=ORIGIN, end=[3, 2, 0], color=BLUE)
        vector_label = MathTex(r"\vec{v}").next_to(vector.get_end(), RIGHT)
        
        with self.voiceover(text="First, imagine you're a physics student. A vector is a directed arrow — it has length and direction, and that's all that matters.") as tracker:
            self.play(FadeOut(title))
            self.play(Create(grid))
            self.play(Create(vector))
            self.play(Write(vector_label))
            self.wait(tracker.duration)
        
        # Create multiple vectors with same properties
        vectors = VGroup(
            Arrow(start=[-2, -1, 0], end=[1, 1, 0], color=BLUE),
            Arrow(start=[2, -2, 0], end=[5, 0, 0], color=BLUE),
            Arrow(start=[-3, 1, 0], end=[0, 3, 0], color=BLUE)
        )
        
        with self.voiceover(text="The arrow can move anywhere in space, but as long as it points the same way and is the same length, it's still the same vector.") as tracker:
            self.play(Create(vectors))
            self.wait(tracker.duration)
        
        # Transition to 3D
        self.play(FadeOut(grid), FadeOut(vectors), FadeOut(vector))
        
        # Create 3D coordinate system
        axes = ThreeDAxes()
        vector_3d = Arrow3D(start=ORIGIN, end=[2, 1, 1], color=BLUE)
        
        # Set up camera for 3D view
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        with self.voiceover(text="In two dimensions, vectors lie on a flat plane. In three dimensions, they live in the space around us. Let's see how vectors exist in our three-dimensional world.") as tracker:
            self.play(Create(axes))
            self.play(Create(vector_3d))
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(1)
        
        # Stop camera rotation and reset view
        self.stop_ambient_camera_rotation()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        self.move_camera(zoom=1)
        
        self.clear()
        
        # Computer Science Perspective
        title = Text("2. Computer Science Perspective", font_size=36, color=GREEN)
        self.play(Write(title))
        
        # Create table
        table = Table(
            [["Square Footage", "Price"],
             ["2600", "$300,000"]],
            include_outer_lines=True
        )
        
        with self.voiceover(text="Now, from a computer science lens, a vector isn't an arrow—it's a list of numbers. Think of it like data: a way to represent an object using measurements.") as tracker:
            self.play(FadeOut(title))
            self.play(Create(table))
            self.wait(1)
        # Create vector representation
        vector = MathTex(r"\begin{bmatrix} 2600 \\ 300000 \end{bmatrix}")
        vector_label = Text("2D vector: A list with two elements", font_size=24).next_to(vector, DOWN)
        
        with self.voiceover(text="You might model a house as a vector: One number for square footage, one for price. In this view, order matters.") as tracker:
            self.play(ReplacementTransform(table, vector))
            self.play(Write(vector_label))
            self.wait(1)
        
        # Show order switching
        flipped_vector = MathTex(r"\begin{bmatrix} 300000 \\ 2600 \end{bmatrix}")
        warning = Text("Meaning flipped!", color=RED).next_to(flipped_vector, DOWN)
        
        with self.voiceover(text="Switch the numbers, and the meaning changes entirely.") as tracker:
            self.play(FadeOut(vector_label))
            self.play(ReplacementTransform(vector, flipped_vector))
            self.play(Write(warning))
            self.wait(1)
        
        self.clear()
        
        # Mathematicians Perspective
        title = Text("3. Mathematician's Perspective", font_size=36, color=RED)
        self.play(Write(title))
        
        # Create abstract symbols with more mathematical notation
        symbols = VGroup(
            MathTex(r"\vec{v} + \vec{w} = \vec{v+w}"),
            MathTex(r"c \cdot \vec{v} = \begin{bmatrix} c \cdot v_1 \\ c \cdot v_2 \end{bmatrix}"),
            MathTex(r"a\vec{v} + b\vec{w} = \begin{bmatrix} a v_1 + b w_1 \\ a v_2 + b w_2 \end{bmatrix}")
        ).arrange(DOWN, buff=0.5)
        
        # Add explanation text
        explanation = VGroup(
            Text("Vector Addition", font_size=24, color=BLUE).next_to(symbols[0], LEFT),
            Text("Scalar Multiplication", font_size=24, color=GREEN).next_to(symbols[1], LEFT),
            Text("Linear Combination", font_size=24, color=RED).next_to(symbols[2], LEFT)
        )
        
        with self.voiceover(text="The mathematician steps back and asks: What makes a vector a vector? To a mathematician, a vector is anything you can add and scale. These two fundamental operations define what it means to be a vector.") as tracker:
            self.play(FadeOut(title))
            self.play(Write(symbols[0]))
            self.play(Write(explanation[0]))
            self.wait(0.5)
            self.play(Write(symbols[1]))
            self.play(Write(explanation[1]))
            self.wait(0.5)
            self.play(Write(symbols[2]))
            self.play(Write(explanation[2]))
            self.wait(1)
        
        self.clear()
        
        # Show examples of different vector spaces
        examples_title = Text("Examples of Vector Spaces", font_size=36, color=YELLOW)
        self.play(Write(examples_title))
        
        # Create example groups
        geometric = VGroup(
            Text("Geometric Vectors", font_size=24, color=BLUE),
            Arrow(start=ORIGIN, end=[2, 1, 0], color=BLUE)
        ).arrange(DOWN)
        
        numerical = VGroup(
            Text("Numerical Vectors", font_size=24, color=GREEN),
            MathTex(r"\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}")
        ).arrange(DOWN)
        
        functional = VGroup(
            Text("Function Vectors", font_size=24, color=RED),
            MathTex(r"f(x) = ax + b")
        ).arrange(DOWN)
        
        # Arrange examples
        examples = VGroup(geometric, numerical, functional).arrange(RIGHT, buff=1)
        examples.next_to(examples_title, DOWN, buff=1)
        
        with self.voiceover(text="Vectors can take many forms. They can be geometric arrows in space, lists of numbers, or even functions. What matters is that they follow the rules of vector addition and scalar multiplication.") as tracker:
            self.play(FadeOut(examples_title))
            self.play(Write(geometric))
            self.wait(0.5)
            self.play(Write(numerical))
            self.wait(0.5)
            self.play(Write(functional))
            self.wait(1)
        
        self.clear()
        
        # Show scalar multiplication
        vector = Arrow(start=ORIGIN, end=[1, 1, 0], color=BLUE)
        scalar = MathTex("2 \cdot").next_to(vector, LEFT)
        sign=MathTex("=").next_to(vector, RIGHT)
        result = Arrow(start=ORIGIN, end=[2, 2, 0], color=GREEN).next_to(sign, RIGHT)
        
        with self.voiceover(text="Let's look at scalar multiplication. When we multiply a vector by a number, we scale its magnitude while preserving its direction. This operation must work for any vector in the space.") as tracker:
            self.play(Create(vector))
            self.play(Write(scalar))
            self.play(Write(sign))
            self.play(Create(result))
            self.wait(1)
        self.clear()
        # Show vector addition
        v1 = Arrow(start=ORIGIN, end=[1, 2, 0], color=BLUE)
        v2 = Arrow(start=v1.get_end(), end=[3, 1, 0], color=GREEN)
        v_sum = Arrow(start=ORIGIN, end=[3, 1, 0], color=RED)
        
        with self.voiceover(text="Vector addition combines two vectors to produce a new vector. The sum must also be a valid vector in the space. This closure property is essential to the definition of a vector space.") as tracker:
            self.play(Create(v1))
            self.play(Create(v2))
            self.play(Create(v_sum))
            self.wait(1)
        self.clear()

    def section2(self):
        # Scene 1: Building the Axes
        title = Text("Coordinate Systems", font_size=36, color=YELLOW)
        self.play(Write(title))
        
        with self.voiceover(text="Now that we have a sense of what vectors are, let's place them into context—literally. To interpret a vector geometrically, we need a coordinate system—a space in which movement and direction make sense. Let's start simple, in two dimensions.") as tracker:
            self.play(FadeOut(title))
            
            # Create axes with consistent unit length
            axes = Axes(
                x_range=[-5, 5, 1],
                y_range=[-5, 5, 1],
                axis_config={"color": BLUE},
                x_axis_config={"numbers_to_include": range(-5, 6)},
                y_axis_config={"numbers_to_include": range(-5, 6)},
                x_length=10,
                y_length=10,
            )
            
            # Create labels
            x_label = axes.get_x_axis_label("x")
            y_label = axes.get_y_axis_label("y")
            origin_label = MathTex("(0,0)").next_to(ORIGIN, DOWN+LEFT, buff=0.1)
            
            # Create origin dot
            origin_dot = Dot(color=YELLOW).scale(1.2)
            
            # Animate creation
            self.play(Create(axes))
            self.play(Write(x_label), Write(y_label))
            self.play(Create(origin_dot), Write(origin_label))
            self.wait(1)
        
        # Scene 2: Tick Marks and Grid
        with self.voiceover(text="We choose some distance to represent the unit '1', and mark it off on each axis. Connecting these gives us a grid—a map for positioning vectors.") as tracker:
            # Create grid with same unit length as axes
            grid = NumberPlane(
                x_range=[-5, 5, 1],
                y_range=[-5, 5, 1],
                x_length=10,
                y_length=10,
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            )
            self.play(Create(grid))
            self.wait(1)
        
        # Scene 3: Introducing a Vector in the Plane
        with self.voiceover(text="A vector like this one tells you how to move from the origin: First, go 3 units right, then 2 units up. This arrow is the geometric picture of the vector.") as tracker:
            # Create vector
            vector = Arrow(start=ORIGIN, end=[3, 2, 0], color=RED, buff=0)
            vector_label = MathTex(r"\vec{v} = \begin{bmatrix} 3 \\ 2 \end{bmatrix}").next_to(vector.get_end(), RIGHT)
            
            # Create movement indicators
            x_movement = Arrow(start=ORIGIN, end=[3, 0, 0], color=BLUE, buff=0)
            y_movement = Arrow(start=[3, 0, 0], end=[3, 2, 0], color=GREEN, buff=0)
            
            # Animate
            self.play(Create(x_movement))
            self.play(Create(y_movement))
            self.play(Transform(x_movement, vector), Transform(y_movement, vector))
            self.play(Write(vector_label))
            self.wait(1)
        
        # Scene 4: Sign and Direction
        with self.voiceover(text="Positive x-values move us to the right, and positive y-values go up. Negative values? They flip direction: left and down.") as tracker:
            # Create negative vector
            neg_vector = Arrow(start=ORIGIN, end=[-4, -2, 0], color=RED, buff=0)
            neg_label = MathTex(r"\vec{w} = \begin{bmatrix} -4 \\ -2 \end{bmatrix}").next_to(neg_vector.get_end(), LEFT)
            
            # Animate
            self.play(FadeOut(vector), FadeOut(vector_label))
            self.play(Create(neg_vector))
            self.play(Write(neg_label))
            self.wait(1)
        
        # Scene 5: Conventions
        with self.voiceover(text="To distinguish vectors from points, we write vectors vertically, like this. Every vector corresponds to exactly one pair of numbers, and vice versa.") as tracker:
            # Create point and vector comparison
            point = Dot([3, 2, 0], color=BLACK)
            point_label = MathTex("(3,2)").next_to(point, LEFT)
            vector = Arrow(start=ORIGIN, end=[3, 2, 0], color=RED, buff=0)
            vector_label = MathTex(r"\begin{bmatrix} 3 \\ 2 \end{bmatrix}").next_to(vector.get_end(), RIGHT)
            
            # Animate
            self.play(FadeOut(neg_vector), FadeOut(neg_label))
            self.play(Create(point), Write(point_label))
            self.play(Create(vector), Write(vector_label))
            self.wait(1)
        
        # Scene 6: Concept Check
        with self.voiceover(text="Let's test your understanding.What's the vector that moves\n4 units down and 7 units to the right?") as tracker:
            # Clean up previous vectors
            self.play(FadeOut(point), FadeOut(point_label), FadeOut(vector), FadeOut(vector_label))
            
            # Show question
            question = Text("What's the vector that moves\n4 units down and 7 units to the right?", 
                          font_size=36, 
                          color=YELLOW).to_edge(UP)
            self.play(Write(question))
            
            # Pause for thinking
            self.wait(3)  # Give audience time to think
            
            # Show answer directly on axes
            answer_vector = Arrow(start=ORIGIN, end=[7, -4, 0], color=GREEN, buff=0)
            answer_label = MathTex(r"\begin{bmatrix} 7 \\ -4 \end{bmatrix}").next_to(answer_vector.get_end(), RIGHT)
            
            # Create movement indicators
            x_movement = Arrow(start=ORIGIN, end=[7, 0, 0], color=BLUE, buff=0)
            y_movement = Arrow(start=[7, 0, 0], end=[7, -4, 0], color=RED, buff=0)
            self.play(Create(x_movement))
            self.play(Create(y_movement))
        with self.voiceover(text="The answer is the vector with components 7 and negative 4. This means moving 7 units to the right and 4 units down.") as tracker2:
                # Show the movement step by step
                self.play(Transform(x_movement, answer_vector), Transform(y_movement, answer_vector))
                self.play(Write(answer_label))
                self.wait(1)
        self.clear()
        # Scene 7: Expanding to 3D
        with self.voiceover(text="To step into 3D space, we add one more axis: the z-axis, perpendicular to both x and y. Now a vector has three components, each telling you how far to move along each direction.") as tracker:
            # Clear 2D scene
            self.play(FadeOut(answer_vector), FadeOut(answer_label), FadeOut(grid), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(origin_dot), FadeOut(origin_label))

            # Create 3D axes
            axes_3d = ThreeDAxes()
            vector_3d = Arrow3D(start=ORIGIN, end=[2, 1, 3], color=RED)
            
            # Set up camera for 3D view
            self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
            
            # Create labels
            x_label_3d = axes_3d.get_x_axis_label("x")
            y_label_3d = axes_3d.get_y_axis_label("y")
            z_label_3d = axes_3d.get_z_axis_label("z")
            
            # Create vector label and position it correctly in 3D space
            vector_label_3d = MathTex(r"\begin{bmatrix} 2 \\ 1 \\ 3 \end{bmatrix}")
            # Position at the end of the vector but shifted to the y-z plane
            vector_label_3d.move_to([0, 1, 3])  # x=0 puts it on y-z plane
            # Rotate to face the camera
            vector_label_3d.rotate(75 * DEGREES, axis=RIGHT)
            vector_label_3d.rotate(-45 * DEGREES, axis=UP)
            # Shift slightly for better visibility
            vector_label_3d.shift(0.5 * RIGHT)
            
            # Animate
            self.play(Create(axes_3d))
            self.play(Write(x_label_3d), Write(y_label_3d), Write(z_label_3d))
            self.play(Create(vector_3d))
            self.play(Write(vector_label_3d))
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(1)

        # Transition to Next Section
        with self.voiceover(text="Now that we can picture vectors in space, the next step is to understand how they combine. Let's look at vector addition.") as tracker:
            # Stop camera rotation and reset view
            self.stop_ambient_camera_rotation()
            self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
            self.move_camera(zoom=1)
            self.clear()

    def section3(self):
        # Scene 1: Tip-to-Tail Addition
        title = Text("Vector Addition", font_size=36, color=YELLOW)
        self.play(Write(title))
        
        with self.voiceover(text="Now that we can place vectors inside a coordinate system, let's explore how to combine them. One of the most fundamental operations in linear algebra is vector addition. Let's start with the geometric picture.") as tracker:
            self.play(FadeOut(title))
            
            # Create grid
            grid = NumberPlane(
                x_range=[-5, 5, 1],
                y_range=[-5, 5, 1],
                x_length=10,
                y_length=10,
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            )
            self.play(Create(grid))
            
            # Create first vector u
            u = Arrow(start=ORIGIN, end=[1, 2, 0], color=BLUE, buff=0)
            u_label = MathTex(r"\vec{u} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}").to_edge(LEFT)
            
            # Create second vector v
            v = Arrow(start=ORIGIN, end=[3, -1, 0], color=GREEN, buff=0)
            v_label = MathTex(r"\vec{v} = \begin{bmatrix} 3 \\ -1 \end{bmatrix}").next_to(u_label, RIGHT)
            
            # Animate first vector
            self.play(Create(u))
            self.play(Write(u_label))
            
            # Animate second vector
            self.play(Create(v))
            self.play(Write(v_label))
            
            # Move v to tip of u
            v_moved = v.copy()
            v_moved.shift(u.get_end())
            self.play(Transform(v, v_moved))
            self.wait(1)
            # Create sum vector
            sum_vector = Arrow(start=ORIGIN, end=[4, 1, 0], color=RED, buff=0)
            sum_label = MathTex(r"\vec{u} + \vec{v} = \begin{bmatrix} 4 \\ 1 \end{bmatrix}").next_to(sum_vector.get_end(), RIGHT)
            
        with self.voiceover(text="To add two vectors, place the tail of the second vector at the tip of the first. Then draw a new arrow from the origin to the end of this chain. That new arrow is the sum. Why does this make sense? Think of vectors as movements. First move along u, then move along v. The result is the combined movement: u plus v.") as tracker2:
                self.play(Create(sum_vector))
                self.play(Write(sum_label))
                self.wait(tracker2.duration)
            
        self.clear()
        # Scene 3: Algebraic Addition
        with self.voiceover(text="Algebraically, we just add each component. The x-components add together, and the y-components add together. It's the same result we got geometrically.") as tracker:            
            # Create component-wise addition
            u_comp = MathTex(r"\vec{u} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}")
            v_comp = MathTex(r"\vec{v} = \begin{bmatrix} 3 \\ -1 \end{bmatrix}")
            plus = MathTex("+")
            equals = MathTex("=")
            result = MathTex(r"\begin{bmatrix} 4 \\ 1 \end{bmatrix}")
            
            # Arrange components
            components = VGroup(u_comp, plus, v_comp, equals, result).arrange(RIGHT)
            
            # Show step-by-step addition
            self.play(Write(components))
            self.wait(1)
        # Scene 4: General Rule
        with self.voiceover(text="In general, vector addition just means adding the corresponding x and y values.") as tracker:
            # Clear previous components
            self.play(FadeOut(components))
            
            # Show general formula
            general_formula = MathTex(
                r"\begin{bmatrix} x_1 \\ y_1 \end{bmatrix} + \begin{bmatrix} x_2 \\ y_2 \end{bmatrix} = \begin{bmatrix} x_1 + x_2 \\ y_1 + y_2 \end{bmatrix}"
            )
            self.play(Write(general_formula))
            self.wait(1)
        
        # Scene 5: Concept Check
        with self.voiceover(text="Let's test your understanding. Add these vectors and think about the resulting movement.") as tracker:
            # Clear formula
            self.play(FadeOut(general_formula))
            self.move_camera(zoom=0.4)
            self.play(Create(grid))
            
            # Show question
            question = MathTex(
                r"\begin{bmatrix} 4 \\ -2 \end{bmatrix} + \begin{bmatrix} 6 \\ 2 \end{bmatrix} = ?"
            ).to_edge(UP)
            self.play(Write(question))
            
            # Create first vector
            v1 = Arrow(start=ORIGIN, end=[4, -2, 0], color=BLUE, buff=0)
            v1_label = MathTex(r"\begin{bmatrix} 4 \\ -2 \end{bmatrix}").next_to(v1.get_end(), RIGHT)
            
            # Create second vector
            v2 = Arrow(start=ORIGIN, end=[6, 2, 0], color=GREEN, buff=0)
            v2_label = MathTex(r"\begin{bmatrix} 6 \\ 2 \end{bmatrix}").next_to(v2.get_end(), RIGHT)
            
            # Show vectors
            self.play(Create(v1), Write(v1_label))
            self.play(Create(v2), Write(v2_label))
            
            # Pause for thinking
            self.wait(3)
            
            # Move second vector to tip of first
            v2_moved = v2.copy()
            v2_moved.shift(v1.get_end())
            self.play(Transform(v2, v2_moved))
            
            # Show result vector
            result_vector = Arrow(start=ORIGIN, end=[10, 0, 0], color=RED, buff=0)
            result_label = MathTex(r"\begin{bmatrix} 10 \\ 0 \end{bmatrix}").next_to(result_vector.get_end(), UP)
            
        with self.voiceover(text="The correct answer is 10 steps to the right, and no vertical movement.") as tracker2:
                self.play(Create(result_vector))
                self.play(Write(result_label))                    
        # Transition to Next Section
        with self.voiceover(text="We've seen how to combine vectors. Next, let's explore how to stretch, shrink, or flip them—with something called scalar multiplication.") as tracker:
            # Clear everything
            self.play(FadeOut(question), FadeOut(v1), FadeOut(v2), FadeOut(v1_label), FadeOut(v2_label), 
                     FadeOut(result_vector), FadeOut(result_label), FadeOut(grid))
            self.move_camera(zoom=1)
            self.clear()


    def section4(self):
        # Scene 1: Doubling a Vector
        title = Text("Scalar Multiplication", font_size=36, color=YELLOW)
        self.play(Write(title))
        
        with self.voiceover(text="So far, we've seen how to combine vectors with addition. Now let's explore how to scale a vector—stretching it, shrinking it, or flipping it entirely. This is called scalar multiplication. A scalar is just a fancy word for a regular number. And when you multiply a vector by a scalar, you're changing its magnitude, and possibly its direction.") as tracker:
            self.play(FadeOut(title))
            
            # Create grid
            grid = NumberPlane(
                x_range=[-5, 5, 1],
                y_range=[-5, 5, 1],
                x_length=10,
                y_length=10,
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            )
            self.play(Create(grid))
            
            # Create original vector
            v = Arrow(start=ORIGIN, end=[2, 1, 0], color=BLUE, buff=0)
            v_label = MathTex(r"\vec{v} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}").next_to(v.get_end(), RIGHT)
            
            # Create scalar multiplication expression
            scalar_expr = MathTex(r"2 \cdot \vec{v} = 2 \cdot \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}").to_edge(UP)
            
            # Create scaled vector
            scaled_v = Arrow(start=ORIGIN, end=[4, 2, 0], color=RED, buff=0)
            self.play(Create(v), Write(v_label))
            self.play(Write(scalar_expr))
        with self.voiceover(text="Multiply a vector by 2, and it stretches to twice the length—like zooming out in its direction.") as tracker2:
                self.play(Transform(v, scaled_v))
        
        # Scene 2: Shrinking a Vector
        with self.voiceover(text="Similarly, multiply by a number less than 1, and the vector gets shorter—you're squishing it toward the origin.") as tracker:
            # Reset vector
            self.play(FadeOut(v), FadeOut(v_label), FadeOut(scalar_expr))
            v = Arrow(start=ORIGIN, end=[2, 1, 0], color=BLUE, buff=0)
            v_label = MathTex(r"\vec{v} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}").next_to(v.get_end(), RIGHT)
            
            # Create scalar multiplication expression
            scalar_expr = MathTex(r"\frac{1}{3} \cdot \vec{v} = \begin{bmatrix} \frac{2}{3} \\ \frac{1}{3} \end{bmatrix}").to_edge(UP)
            
            # Create scaled vector
            scaled_v = Arrow(start=ORIGIN, end=[2/3, 1/3, 0], color=RED, buff=0)
            
            self.play(Create(v), Write(v_label))
            self.play(Write(scalar_expr))
            self.play(Transform(v, scaled_v))
        self.clear()
        # Scene 3: Negative Scalars
        with self.voiceover(text="A negative scalar does two things: It flips the vector, and then scales it just like a positive number.") as tracker:
            # Reset vector
            self.play(Create(grid))
            v = Arrow(start=ORIGIN, end=[2, 1, 0], color=BLUE, buff=0)
            v_label = MathTex(r"\vec{v} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}").next_to(v.get_end(), RIGHT)
            
            # Create scalar multiplication expression
            scalar_expr = MathTex(r"-1.5 \cdot \vec{v} = \begin{bmatrix} -3 \\ -1.5 \end{bmatrix}").to_edge(UP)
            
            # Create scaled vector
            scaled_v = Arrow(start=ORIGIN, end=[-3, -1.5, 0], color=RED, buff=0)
            
            self.play(Create(v), Write(v_label))
            self.play(Write(scalar_expr))
            self.play(Transform(v, scaled_v))
        
        # Scene 4: General Rule
        with self.voiceover(text="In terms of components, scalar multiplication means multiplying every entry of the vector by the scalar.") as tracker:
            # Clear previous scene
            self.play(FadeOut(v), FadeOut(v_label), FadeOut(scalar_expr))
            
            # Create general formula
            general_formula = MathTex(
                r"a \cdot \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} a \cdot x \\ a \cdot y \end{bmatrix}"
            ).to_edge(UP)
            
            # Create number line
            number_line = NumberLine(x_range=[-2, 2, 0.5], length=8, include_numbers=True)
            dot = Dot(color=YELLOW)
            
            # Animate
            self.play(Write(general_formula))
            self.play(Create(number_line))
            self.play(Create(dot))
            
            # Animate dot moving and vector scaling
            for a in [-1.5, -1, -0.5, 0.5, 1, 1.5]:
                self.play(dot.animate.move_to(number_line.n2p(a)))
                self.wait(0.5)
            
        self.clear()
        # Scene 5: Concept Check
        with self.voiceover(text="Let's solve one together. What is 1/3 times the vector with components 12 and 9?") as tracker:
            self.play(Create(grid))
            self.move_camera(zoom=0.4)
            # Show question
            question = MathTex(
                r"\frac{1}{3} \cdot \begin{bmatrix} 12 \\ 9 \end{bmatrix} = ?"
            ).to_corner(UL)
            self.play(Write(question))
            
            # Create original vector with consistent scale
            v = Arrow(start=ORIGIN, end=[12, 9, 0], color=BLUE, buff=0, stroke_width=4)
            v_label = MathTex(r"\begin{bmatrix} 12 \\ 9 \end{bmatrix}").next_to(v.get_end(), RIGHT)
            
            # Create scaled vector with consistent scale
            scaled_v = Arrow(start=ORIGIN, end=[4, 3, 0], color=RED, buff=0, stroke_width=4)
            scaled_label = MathTex(r"\begin{bmatrix} 4 \\ 3 \end{bmatrix}").next_to(scaled_v.get_end(), RIGHT)
            self.play(Create(v), Write(v_label))

            self.wait(3)
            with self.voiceover(text="The answer is the vector with components 4 and 3.") as tracker2:
                self.play(Transform(v, scaled_v))
                self.play(Write(scaled_label))
                self.wait(tracker2.duration)
            
        self.clear()
        # Scene 6: Real-World Analogy
        with self.voiceover(text="In physics and graphics, scaling vectors models real-world change—like boosting thrust, changing velocity, or flipping direction.") as tracker:
            # Clear previous scene
            self.play(FadeOut(question), FadeOut(v), FadeOut(v_label), FadeOut(scaled_label), FadeOut(grid))
            
            # Create rocket and force vector
            force = Arrow(start=ORIGIN, end=[2, 0, 0], color=RED, buff=0, stroke_width=4)

            # Group with force vector
            rocket_force = VGroup(force)
            
            # Animate scaling
            self.play(Create(rocket_force))
            
            # Scale up
            scaled_force = Arrow(start=ORIGIN, end=[4, 0, 0], color=RED, buff=0)
            self.play(Transform(force, scaled_force))
            
            # Flip direction
            flipped_force = Arrow(start=ORIGIN, end=[-4, 0, 0], color=RED, buff=0)
            self.play(Transform(force, flipped_force))        
        # Transition to Next Section
        with self.voiceover(text="We've now seen how to both add vectors and scale them. These two operations form the foundation of linear algebra.thank you for watching") as tracker:
            # Clear everything
            self.play(FadeOut(rocket_force))
            self.clear()

if __name__ == "__main__":
    scene = VectorInterpretationsScene()
    scene.render()