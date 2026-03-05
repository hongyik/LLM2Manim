from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class LinearTransformations(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections
        self.section1()  # Introduction to Linear Transformations
        self.clear()
        self.section2()  # What is a Transformation?
        self.clear()
        self.section3()  # Visualizing Transformations (All Vectors)
        self.clear()
        self.section4()  # What Makes a Transformation Linear?
        self.clear()
        self.section5()  # How to Describe a Transformation? (Basis Vectors)
        self.clear()
        self.section6()  # Deduce Where Other Vectors Go
        self.clear()
        self.section7()  # Generalizing to Any Vector (x,y)
        self.clear()
        self.section8()  # Packaging Information into a Matrix
        self.clear()
        self.section9()  # Matrix-Vector Multiplication
        self.clear()
        self.section10()  # General 2×2 Matrix Transformation
        self.clear()
        self.section11()  # Example 1: Rotation by 90°
        self.clear()
        self.section12()  # Example 2: Shear Transformation
        self.clear()
        self.section14()  # Linearly Dependent Basis Vectors

    def section1(self):
        # Start with black screen and title
        title = Text("Linear Transformations and Matrices", color=WHITE)
        
        with self.voiceover(text="If I had to choose just one topic that makes all of the others in linear algebra start to click — and which too often goes unlearned the first time a student takes the subject — it would be this one:") as tracker:
            self.play(Write(title))
            self.wait(1)
        
        with self.voiceover(text="The idea of a linear transformation and its relation to matrices.") as tracker:
            self.play(
                title.animate.scale(0.8).to_edge(UP)
            )
            self.wait(1)
        
        # Create grid and vectors
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Create several vectors in different directions
        vectors_data = [
            ([2, 1, 0], RED),
            ([1, 2, 0], BLUE),
            ([-1, 2, 0], GREEN),
            ([2, -1, 0], YELLOW),
            ([0, 2, 0], PURPLE)
        ]
        
        vectors = VGroup()
        for end_point, color in vectors_data:
            vector = Arrow(start=ORIGIN, end=end_point, color=color, buff=0)
            vectors.add(vector)
        
        with self.voiceover(text="In this video, we're going to focus on:") as tracker:
            self.play(
                FadeIn(grid),
                Create(vectors),
                run_time=2
            )
            self.wait(1)
        
        # Create subtitles
        subtitles = VGroup(
            Text("2D Transformations", color=YELLOW).scale(0.7),
            Text("Matrix-Vector Multiplication", color=BLUE).scale(0.7),
            Text("Building Intuition", color=GREEN).scale(0.7)
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT)
        
        # Show each subtitle with corresponding narration
        with self.voiceover(text="How these transformations look in two dimensions.") as tracker:
            self.play(Write(subtitles[0]))
            self.wait(0.5)
        
        with self.voiceover(text="How they relate to matrix-vector multiplication.") as tracker:
            self.play(Write(subtitles[1]))
            self.wait(0.5)
        
        with self.voiceover(text="And importantly, how to understand it intuitively — without memorization.") as tracker:
            self.play(Write(subtitles[2]))
            self.wait(0.5)
        
        # Add transformation notation
        transform_notation = MathTex(
            "T: \\mathbb{R}^2 \\to \\mathbb{R}^2"
        ).next_to(grid, UP)
        
        mapping_notation = MathTex(
            "\\mathbf{v} \\mapsto T(\\mathbf{v})"
        ).next_to(transform_notation, DOWN)
        
        # Create pulsating animation for vectors
        def pulsate(vectors, scale_factor=1.1, duration=2):
            animations = []
            for vector in vectors:
                animations.append(
                    vector.animate.scale(scale_factor)
                )
            return AnimationGroup(*animations)
        
        # Show transformation notation with light opacity
        with self.voiceover(text="We'll build up to understanding how vectors transform under linear maps.") as tracker:
            self.play(
                Write(transform_notation),
                Write(mapping_notation)
            )
            
            # Add subtle pulsating animation to vectors
            self.play(
                pulsate(vectors),
                rate_func=there_and_back,
                run_time=2
            )
            self.wait(1)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section2(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Start with a title and explanation
        title = Text("What is a Transformation?", color=WHITE)
        subtitle = Text("A function that takes vectors as input and produces vectors as output", 
                       color=YELLOW).scale(0.6)
        
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Let's start with a fundamental question: What exactly is a transformation?") as tracker:
            self.play(Write(title))
            self.wait(0.5)
            self.play(Write(subtitle))
            self.wait(1)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show input and output vectors
        with self.voiceover(text="A transformation is like a machine that takes a vector as input...") as tracker:
            self.play(Create(grid))
            
            # Create input vector
            input_vector = Arrow(start=ORIGIN, end=[2, 1], color=BLUE, buff=0)
            input_label = MathTex("\\vec{v}", color=BLUE).next_to(input_vector.get_end(), RIGHT)
            
            self.play(
                Create(input_vector),
                Write(input_label)
            )
            self.wait(1)
        
        # Show transformation process
        process_box = Rectangle(height=2, width=3, color=YELLOW)
        process_text = Text("T", color=YELLOW).move_to(process_box)
        process_group = VGroup(process_box, process_text).next_to(input_vector, RIGHT)
        
        with self.voiceover(text="...processes it according to some rule we call T...") as tracker:
            self.play(
                Create(process_box),
                Write(process_text)
            )
            self.wait(1)
        
        # Show output vector
        output_vector = Arrow(start=ORIGIN, end=[-1, 2], color=RED, buff=0)
        output_label = MathTex("T(\\vec{v})", color=RED).next_to(output_vector.get_end(), RIGHT)
        
        with self.voiceover(text="...and produces another vector as output.") as tracker:
            self.play(
                Create(output_vector),
                Write(output_label)
            )
            self.wait(1)
        
        # Frame 3: Compare Function vs Transformation
        comparison = VGroup(
            Text("Function", color=YELLOW).scale(0.7),
            Text("→ Numbers to numbers", color=WHITE).scale(0.6),
            Text("Transformation", color=YELLOW).scale(0.7),
            Text("→ Vectors to vectors", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="While a regular function maps numbers to numbers, a transformation maps vectors to vectors.") as tracker:
            self.play(Write(comparison))
            self.wait(1)
        
        # Frame 4: Show formal definition
        self.play(
            *[FadeOut(mob) for mob in [comparison, process_group]],
            input_vector.animate.shift(LEFT * 2),
            input_label.animate.shift(LEFT * 2),
            output_vector.animate.shift(RIGHT * 2),
            output_label.animate.shift(RIGHT * 2)
        )
        
        formal_def = MathTex(
            "T: \\mathbb{R}^2 \\to \\mathbb{R}^2",
            "\\quad \\vec{v} \\mapsto T(\\vec{v})"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Formally, we write this as T mapping from R-two to R-two, taking a vector v to its transformed version T of v.") as tracker:
            self.play(Write(formal_def))
            self.wait(1)
        
        # Frame 5: Emphasize visual nature
        with self.voiceover(text="The beauty of transformations is that we can visualize them. We can see how they move and change vectors in space.") as tracker:
            # Animate the transformation
            self.play(
                input_vector.animate.shift(RIGHT * 2),
                input_label.animate.shift(RIGHT * 2),
                output_vector.animate.shift(LEFT * 2),
                output_label.animate.shift(LEFT * 2),
                run_time=2
            )
            self.wait(1)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section3(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Start with multiple arrows
        title = Text("Visualizing Transformations", color=WHITE)
        subtitle = Text("From Individual Vectors to All Space", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="So how should we think about transformations not just for one vector, but for all vectors?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Create multiple vectors at different points
        vectors_data = [
            ([2, 1, 0], RED),
            ([1, 2, 0], BLUE),
            ([-1, 2, 0], GREEN),
            ([2, -1, 0], YELLOW),
            ([0, 2, 0], PURPLE),
            ([-2, -1, 0], ORANGE),
            ([1, -2, 0], PINK)
        ]
        
        vectors = VGroup()
        vector_tips = VGroup()
        
        with self.voiceover(text="Here's a powerful idea:") as tracker:
            self.play(Create(grid))
            
            # Create all vectors and their tip dots
            for end_point, color in vectors_data:
                vector = Arrow(start=ORIGIN, end=end_point, color=color, buff=0)
                tip_dot = Dot(point=end_point, color=color)
                vectors.add(vector)
                vector_tips.add(tip_dot)
            
            self.play(Create(vectors))
            self.wait(1)
        
        # Frame 2: Transition to points
        point_explanation = MathTex(
            "\\text{Each point } (x,y) \\mapsto T(x,y)"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Instead of visualizing each vector as an arrow, think of it as a point — the tip of the arrow.") as tracker:
            self.play(Write(point_explanation))
            self.play(
                Create(vector_tips)
            )
            self.wait(1)
            
            self.play(FadeOut(vectors))
        
        # Frame 3: Create grid of points
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="That way, imagining a transformation becomes imagining every point in space moving to another point.") as tracker:
            self.play(
                FadeOut(vector_tips),
                FadeIn(grid_points, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Apply transformation
        # Create a copy of the original grid to keep as reference
        transformed_points = grid_points.copy()
        
        # Define a simple transformation (e.g., shear)
        def transform_point(point):
            x, y, z = point
            return [x + 0.5*y, y, z]
        
        with self.voiceover(text="And for transformations in two dimensions, a great trick is to visualize how an infinite grid of points moves.") as tracker:
            self.play(
                *[dot.animate.move_to(transform_point(dot.get_center())) 
                  for dot in transformed_points],
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Highlight deformation effects
        highlight_points = VGroup()
        for x in [-2, 0, 2]:
            for y in [-2, 0, 2]:
                point = Dot(point=transform_point([x, y, 0]), color=YELLOW, radius=0.08)
                highlight_points.add(point)
        
        with self.voiceover(text="Watching this happen gives a beautiful feeling — it's like squishing and morphing space itself.") as tracker:
            self.play(
                FadeIn(highlight_points),
                run_time=1
            )
            
            # Add flowing animation to emphasize deformation
            self.play(
                highlight_points.animate.set_color(RED),
                run_time=1
            )
            self.wait(1)
        
        # Frame 6: Show mathematical notation
        transformation_eq = MathTex(
            "(x', y') = T(x, y)",
            "\\quad \\text{for all points } (x,y)"
        ).next_to(point_explanation, DOWN)
        
        with self.voiceover(text="This visualization helps us understand how transformations affect all of space, not just individual vectors.") as tracker:
            self.play(Write(transformation_eq))
            self.wait(1)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section4(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("What Makes a Transformation Linear?", color=WHITE)
        
        with self.voiceover(text="So far, we've seen how a transformation moves points in space. But what makes a transformation linear?") as tracker:
            self.play(Write(title))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title.animate.scale(0.8).to_edge(UP)
        )
        
        # Show initial grid
        with self.voiceover(text="Visually, a transformation is linear if it satisfies two key properties:") as tracker:
            self.play(Create(grid))
            self.wait(1)
        
        # Frame 2: State the two properties
        properties = VGroup(
            Text("1. Keep lines straight", color=YELLOW).scale(0.7),
            Text("2. Keep origin fixed", color=YELLOW).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="First, it must keep lines straight — no curves allowed. Second, it must keep the origin fixed — the point (0,0) must stay exactly where it is.") as tracker:
            self.play(Write(properties))
            self.wait(1)
        
        # Frame 3: Show violation 1 - Curved Lines
        def nonlinear_transform1(point):
            x, y, _ = point
            # Create a transformation that curves lines
            return [x + 0.1*y**2, y + 0.1*x**2, 0]
        
        curved_grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                curved_grid_points.add(point)
        
        with self.voiceover(text="Let's take a closer look at what happens when either of these properties is broken.") as tracker:
            # Keep original grid faintly visible
            self.add(grid)
            
            # Apply nonlinear transformation
            self.play(
                *[dot.animate.move_to(nonlinear_transform1(dot.get_center())) 
                  for dot in curved_grid_points],
                run_time=2
            )
        
        violation1_text = Text("Not Linear: Curved lines", color=RED).scale(0.7).next_to(properties, DOWN, buff=1)
        
        # Highlight a curved line
        curved_line = VMobject()
        curved_line.set_points_smoothly([
            nonlinear_transform1([x, 2, 0]) for x in np.linspace(-4, 4, 30)
        ])
        curved_line.set_color(RED)
        
        with self.voiceover(text="In this transformation, lines become curves — a clear violation of linearity.") as tracker:
            self.play(Write(violation1_text))
            self.play(Create(curved_line))
            self.wait(1)
        
        # Clear for next example
        self.play(
            *[FadeOut(mob) for mob in [curved_grid_points, curved_line, violation1_text]]
        )
        
        # Frame 4: Show violation 2 - Moving Origin
        def nonlinear_transform2(point):
            x, y, _ = point
            # Create a transformation that moves origin
            return [x + 1, y + 1, 0]
        
        shifted_grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                shifted_grid_points.add(point)
        
        with self.voiceover(text="Here's another violation: when the origin moves.") as tracker:
            self.play(
                *[dot.animate.move_to(nonlinear_transform2(dot.get_center())) 
                  for dot in shifted_grid_points],
                run_time=2
            )
        
        # Highlight moved origin
        origin_dot = Dot(point=nonlinear_transform2([0, 0, 0]), color=RED)
        violation2_text = Text("Not Linear: Origin moved", color=RED).scale(0.7).next_to(properties, DOWN, buff=1)
        
        with self.voiceover(text="Even though lines stay straight, moving the origin breaks linearity.") as tracker:
            self.play(
                Create(origin_dot),
                Write(violation2_text)
            )
            self.wait(1)
        
        # Clear for next example
        self.play(
            *[FadeOut(mob) for mob in [shifted_grid_points, origin_dot, violation2_text]]
        )
        
        # Frame 5: Show subtle violation - Hidden Curves
        def nonlinear_transform3(point):
            x, y, _ = point
            # Create a transformation that curves diagonals
            return [x, y + 0.1*x**2, 0]
        
        subtle_grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                subtle_grid_points.add(point)
        
        with self.voiceover(text="Sometimes the violation is subtle. Here, horizontal and vertical lines stay straight...") as tracker:
            self.play(
                *[dot.animate.move_to(nonlinear_transform3(dot.get_center())) 
                  for dot in subtle_grid_points],
                run_time=2
            )
        
        # Show diagonal line becoming curved
        diagonal_points = [nonlinear_transform3([t, t, 0]) for t in np.linspace(-3, 3, 30)]
        curved_diagonal = VMobject()
        curved_diagonal.set_points_smoothly(diagonal_points)
        curved_diagonal.set_color(RED)
        
        with self.voiceover(text="...but watch what happens to this diagonal line — it curves!") as tracker:
            self.play(Create(curved_diagonal))
            
            violation3_text = Text("Still Not Linear: Diagonal line curved", color=RED).scale(0.7).next_to(properties, DOWN, buff=1)
            self.play(Write(violation3_text))
            self.wait(1)
        
        # Clear for final example
        self.play(
            *[FadeOut(mob) for mob in [subtle_grid_points, curved_diagonal, violation3_text]]
        )
        
        # Frame 6: Show valid linear transformation
        def linear_transform(point):
            x, y, _ = point
            # Create a valid linear transformation (e.g., rotation and scaling)
            theta = PI/6  # 30 degrees
            return [
                x*np.cos(theta) - y*np.sin(theta),
                x*np.sin(theta) + y*np.cos(theta),
                0
            ]
        
        linear_grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                linear_grid_points.add(point)
        
        with self.voiceover(text="Finally, here's a true linear transformation: lines stay straight, and the origin stays fixed.") as tracker:
            self.play(
                *[dot.animate.move_to(linear_transform(dot.get_center())) 
                  for dot in linear_grid_points],
                run_time=2
            )
        
        # Show formal conditions
        formal_conditions = MathTex(
            "\\text{A transformation } T \\text{ is linear if:}",
            "\\\\",
            "T(cv) = cT(v)",
            "\\quad \\text{for all scalars } c",
            "\\\\",
            "T(u+v) = T(u) + T(v)",
            "\\quad \\text{for all vectors } u,v"
        ).scale(0.7).to_edge(RIGHT)
        
        with self.voiceover(text="These visual rules correspond to important algebraic properties that define linear transformations.") as tracker:
            self.play(Write(formal_conditions))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section5(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("How to Describe a Transformation?", color=WHITE)
        subtitle = Text("Using Basis Vectors", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now that we know what a linear transformation is, here's the next big question:") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        with self.voiceover(text="How can we describe a linear transformation numerically? After all, if you wanted a computer to animate this, you couldn't just say 'squish space' — you need numbers!") as tracker:
            self.play(Create(grid))
            self.wait(1)
        
        # Frame 2: Show basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\hat{\\imath}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        basis_def = MathTex(
            "\\hat{\\imath} = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix},",
            "\\quad",
            "\\hat{\\jmath} = \\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Amazingly, it's enough to know just two things:") as tracker:
            self.play(
                Create(i_hat),
                Create(j_hat),
                Write(i_hat_label),
                Write(j_hat_label),
                Write(basis_def)
            )
            self.wait(1)
        
        # Frame 3: Highlight basis vectors individually
        with self.voiceover(text="Where the basis vector i-hat — pointing along the x-axis — lands.") as tracker:
            self.play(
                i_hat.animate.set_color(RED),
                i_hat_label.animate.set_color(RED),
                j_hat.animate.set_opacity(0.3),
                j_hat_label.animate.set_opacity(0.3)
            )
            self.wait(1)
        
        with self.voiceover(text="Where the basis vector j-hat — pointing along the y-axis — lands.") as tracker:
            self.play(
                j_hat.animate.set_color(BLUE),
                j_hat_label.animate.set_color(BLUE),
                i_hat.animate.set_opacity(0.3),
                i_hat_label.animate.set_opacity(0.3)
            )
            self.wait(1)
        
        # Reset opacities
        self.play(
            i_hat.animate.set_opacity(1),
            j_hat.animate.set_opacity(1),
            i_hat_label.animate.set_opacity(1),
            j_hat_label.animate.set_opacity(1)
        )
        
        # Frame 4: Apply transformation
        def transform_basis(point):
            x, y, z = point
            # Example transformation: rotation + scaling
            return [x - y, x + y, z]
        
        transformed_i = Arrow(
            start=ORIGIN,
            end=transform_basis([1, 0, 0]),
            color=RED,
            buff=0
        )
        transformed_j = Arrow(
            start=ORIGIN,
            end=transform_basis([0, 1, 0]),
            color=BLUE,
            buff=0
        )
        
        transformed_i_label = MathTex("T(\\hat{\\imath})", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("T(\\hat{\\jmath})", color=BLUE).next_to(transformed_j.get_end(), UP)
        
        transformed_basis = MathTex(
            "T(\\hat{\\imath}) = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix},",
            "\\quad",
            "T(\\hat{\\jmath}) = \\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}"
        ).next_to(basis_def, DOWN)
        
        with self.voiceover(text="That's it! Track those two, and you know everything about the transformation.") as tracker:
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(i_hat_label, transformed_i_label),
                ReplacementTransform(j_hat_label, transformed_j_label),
                Write(transformed_basis)
            )
            self.wait(1)
        
        # Frame 5: Show grid transformation
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="Every other point's motion depends entirely on where these two basis vectors go.") as tracker:
            # Keep original grid faintly visible
            self.add(grid)
            
            # Transform grid points
            self.play(
                *[dot.animate.move_to(transform_basis(dot.get_center())) 
                  for dot in grid_points],
                run_time=2
            )
        
        # Frame 6: Show before and after comparison
        comparison = VGroup(
            Text("Before:", color=YELLOW).scale(0.7),
            MathTex("\\hat{\\imath} = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix},",
                    "\\quad",
                    "\\hat{\\jmath} = \\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix}"),
            Text("After:", color=YELLOW).scale(0.7),
            MathTex("T(\\hat{\\imath}) = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix},",
                    "\\quad",
                    "T(\\hat{\\jmath}) = \\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix}")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="These two vectors completely determine how the transformation affects every point in space.") as tracker:
            self.play(Write(comparison))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section6(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Deduce Where Other Vectors Go", color=WHITE)
        subtitle = Text("Using Transformed Basis Vectors", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now that we know where i-hat and j-hat land after the transformation, here's the beautiful part:") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show original and transformed basis vectors
        # Original basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        i_hat_label = MathTex("\\hat{\\imath}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Transformed basis vectors
        transformed_i = Arrow(start=ORIGIN, end=[1, -2, 0], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[3, 0, 0], color=BLUE, buff=0)
        transformed_i_label = MathTex("T(\\hat{\\imath})", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("T(\\hat{\\jmath})", color=BLUE).next_to(transformed_j.get_end(), UP)
        
        with self.voiceover(text="We can figure out where any other vector goes!") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.wait(1)
            
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(i_hat_label, transformed_i_label),
                ReplacementTransform(j_hat_label, transformed_j_label)
            )
            self.wait(1)
        
        # Frame 3: Show example vector as combination
        example_vector = Arrow(start=ORIGIN, end=[-1, 2, 0], color=YELLOW, buff=0)
        example_label = MathTex("\\mathbf{v} = -1\\hat{\\imath} + 2\\hat{\\jmath}").next_to(title_group, DOWN)
        
        # Components visualization
        i_component = Arrow(start=ORIGIN, end=[-1, 0, 0], color=RED, buff=0)
        j_component = Arrow(start=[-1, 0, 0], end=[-1, 2, 0], color=BLUE, buff=0)
        
        with self.voiceover(text="Remember, any vector can be written as a combination of i-hat and j-hat. For example, let's consider the vector v equals negative one i-hat plus two j-hat.") as tracker:
            self.play(
                Create(example_vector),
                Write(example_label)
            )
            self.play(
                Create(i_component),
                Create(j_component)
            )
            self.wait(1)
        
        # Frame 4: Show transformation computation
        computation = MathTex(
            "T(\\mathbf{v})", "&=", "-1 \\cdot T(\\hat{\\imath})", "+", "2 \\cdot T(\\hat{\\jmath})", "\\\\",
            "&=", "-1 \\cdot (1,-2)", "+", "2 \\cdot (3,0)", "\\\\",
            "&=", "(-1,2)", "+", "(6,0)", "\\\\",
            "&=", "(5,2)"
        ).scale(0.8).to_edge(RIGHT)
        
        # Transform the example vector
        transformed_vector = Arrow(start=ORIGIN, end=[5, 2, 0], color=YELLOW, buff=0)
        
        with self.voiceover(text="After the transformation, the new position of v will be: negative one times wherever i-hat lands, plus two times wherever j-hat lands.") as tracker:
            self.play(Write(computation))
            self.wait(1)
        
        # Frame 5: Show transformation components
        transformed_i_component = Arrow(start=ORIGIN, end=[-1, 2, 0], color=RED, buff=0)
        transformed_j_component = Arrow(start=[-1, 2, 0], end=[5, 2, 0], color=BLUE, buff=0)
        
        with self.voiceover(text="In other words, it keeps the same linear combination, but now based on the new locations of i-hat and j-hat.") as tracker:
            self.play(
                ReplacementTransform(example_vector, transformed_vector),
                Create(transformed_i_component),
                Create(transformed_j_component)
            )
            self.wait(1)
        
        # Frame 6: Emphasize the key idea
        key_idea = VGroup(
            Text("Key Idea:", color=YELLOW).scale(0.7),
            Text("• Track only basis vectors", color=WHITE).scale(0.6),
            Text("• All other vectors follow", color=WHITE).scale(0.6),
            Text("• Preserves linear combinations", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="This preserves the structure of space — linear combinations before and after match.") as tracker:
            self.play(Write(key_idea))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section7(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Generalizing to Any Vector (x,y)", color=WHITE)
        subtitle = Text("The Power of Linear Combinations", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="So far, we saw how specific vectors transform by following where i-hat and j-hat move. But we can go even further!") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show generic vector and basis vectors
        with self.voiceover(text="For any vector with coordinates (x,y), we can figure out exactly where it will land using the same idea.") as tracker:
            self.play(Create(grid))
            
            # Create generic vector with label
            generic_vector = Arrow(start=ORIGIN, end=[2, 1], color=YELLOW, buff=0)
            generic_label = MathTex("(x,y)", color=YELLOW).next_to(generic_vector.get_end(), RIGHT)
            
            # Create basis vectors and their transformed versions
            i_hat = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)
            j_hat = Arrow(start=ORIGIN, end=[0, 1], color=BLUE, buff=0)
            
            self.play(
                Create(generic_vector),
                Write(generic_label),
                Create(i_hat),
                Create(j_hat)
            )
            self.wait(1)
        
        # Frame 3: Show basis vector transformations
        transformed_i = Arrow(start=ORIGIN, end=[1, -2], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[3, 0], color=BLUE, buff=0)
        
        basis_transform = MathTex(
            "T(\\hat{\\imath}) = (1,-2)", "\\quad",
            "T(\\hat{\\jmath}) = (3,0)"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Let's recall where our basis vectors land:") as tracker:
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                Write(basis_transform)
            )
            self.wait(1)
        
        # Frame 4: Show computation steps
        computation = MathTex(
            "T(x,y)", "&=", "x \\cdot T(\\hat{\\imath})", "+", "y \\cdot T(\\hat{\\jmath})", "\\\\",
            "&=", "x \\cdot (1,-2)", "+", "y \\cdot (3,0)", "\\\\",
            "&=", "(x,-2x)", "+", "(3y,0)", "\\\\",
            "&=", "(x+3y,-2x)"
        ).scale(0.8).to_edge(RIGHT)
        
        with self.voiceover(text="The transformed position is simply: x times where i-hat lands, plus y times where j-hat lands.") as tracker:
            self.play(Write(computation))
            self.wait(1)
        
        # Frame 5: Animate the transformation
        def transform_point(point):
            x, y, _ = point
            return [x + 3*y, -2*x, 0]
        
        # Create grid points
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="Let's see how this formula transforms the entire space:") as tracker:
            # Keep original grid faintly visible
            self.add(grid)
            
            # Transform grid points
            self.play(
                *[dot.animate.move_to(transform_point(dot.get_center())) 
                  for dot in grid_points],
                generic_vector.animate.put_start_and_end_on(ORIGIN, transform_point([2, 1, 0])),
                generic_label.animate.next_to(transform_point([2, 1, 0]), RIGHT),
                run_time=2
            )
        
        # Frame 6: Show general formula
        general_formula = MathTex(
            "\\text{For any transformation:}", "\\\\",
            "T(\\hat{\\imath}) = (a,c)", "\\quad",
            "T(\\hat{\\jmath}) = (b,d)", "\\\\",
            "\\boxed{T(x,y) = (ax+by, cx+dy)}"
        ).scale(0.7).to_edge(LEFT)
        
        with self.voiceover(text="This gives us a beautiful general formula. For any linear transformation, if we know where i-hat and j-hat go, we can find where every vector lands.") as tracker:
            self.play(Write(general_formula))
            self.wait(1)
        
        # Frame 7: Emphasize key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Transformation depends only on x and y", color=WHITE).scale(0.6),
            Text("• Formula is linear - no curves or jumps", color=WHITE).scale(0.6),
            Text("• Basis vectors determine everything", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(general_formula, DOWN, buff=1)
        
        with self.voiceover(text="The formula is linear in x and y — no curves, no sudden jumps. This is the essence of linear transformations.") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section8(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Packaging Information into a Matrix", color=WHITE)
        subtitle = Text("The Elegant Connection", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now here's the really exciting part: All the information we've been using — the new positions of i-hat and j-hat — can be neatly packaged into a simple object called a matrix.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show basis vectors and their transformations
        # Original basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1], color=BLUE, buff=0)
        
        # Transformed basis vectors
        transformed_i = Arrow(start=ORIGIN, end=[1, -2], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[3, 0], color=BLUE, buff=0)
        
        # Labels for transformed vectors
        i_transform = MathTex(
            "T(\\hat{\\imath}) = (1,-2)",
            color=RED
        ).to_edge(LEFT).shift(UP)
        
        j_transform = MathTex(
            "T(\\hat{\\jmath}) = (3,0)",
            color=BLUE
        ).to_edge(LEFT)
        
        with self.voiceover(text="Specifically, we organize the transformed basis vectors into the columns of a two-by-two matrix.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                run_time=1
            )
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                Write(i_transform),
                Write(j_transform),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: Show matrix formation
        matrix = MathTex(
            "A = ",
            "\\begin{bmatrix} 1 & 3 \\\\ -2 & 0 \\end{bmatrix}"
        ).scale(1.5).to_edge(RIGHT)
        
        # Color the columns of the matrix
        matrix[1][1:3].set_color(RED)    # First column
        matrix[1][3:5].set_color(BLUE)   # Second column
        
        with self.voiceover(text="Here's what it looks like.") as tracker:
            self.play(Write(matrix))
            self.wait(1)
        
        # Frame 4: Animate packaging of vectors into matrix
        # Create vector representations that will move into matrix
        vector1 = MathTex("\\begin{bmatrix} 1 \\\\ -2 \\end{bmatrix}", color=RED)
        vector2 = MathTex("\\begin{bmatrix} 3 \\\\ 0 \\end{bmatrix}", color=BLUE)
        
        vectors_group = VGroup(vector1, vector2).arrange(RIGHT, buff=1).next_to(matrix, LEFT, buff=2)
        
        with self.voiceover(text="The first column comes from where i-hat landed, and the second column from where j-hat landed.") as tracker:
            self.play(
                TransformFromCopy(i_transform, vector1),
                TransformFromCopy(j_transform, vector2)
            )
            self.wait(1)
            
            # Animate vectors moving into matrix
            self.play(
                vector1.animate.move_to(matrix[1][1:3]),
                vector2.animate.move_to(matrix[1][3:5]),
                run_time=2
            )
        
        # Frame 5: Show general form
        general_case = VGroup(
            MathTex("\\text{General case:}"),
            MathTex("T(\\hat{\\imath}) = (a,c)", "\\quad", "T(\\hat{\\jmath}) = (b,d)"),
            MathTex("A = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}")
        ).arrange(DOWN, buff=0.5).to_edge(LEFT)
        
        with self.voiceover(text="This gives us a beautiful general form. For any linear transformation, we can package its effect on the basis vectors into a two-by-two matrix.") as tracker:
            self.play(Write(general_case))
            self.wait(1)
        
        # Frame 6: Show transformation effect
        def matrix_transform(point):
            x, y, _ = point
            return [x + 3*y, -2*x, 0]
        
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="And this matrix completely captures how the transformation deforms space.") as tracker:
            # Keep original grid faintly visible
            self.add(grid)
            
            # Transform grid points
            self.play(
                *[dot.animate.move_to(matrix_transform(dot.get_center())) 
                  for dot in grid_points],
                run_time=2
            )
        
        # Frame 7: Emphasize key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Matrix columns = transformed basis vectors", color=WHITE).scale(0.6),
            Text("• Matrix structure encodes transformation", color=WHITE).scale(0.6),
            Text("• Simple way to store complex behavior", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="A matrix is just a way of storing where the basis vectors land. This is why matrices have the structure they do — it encodes the transformation of space!") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section9(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Matrix-Vector Multiplication", color=WHITE)
        subtitle = Text("The Mechanics of Transformation", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now that we've packaged our transformation into a matrix, how do we actually use it?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show matrix and vector
        matrix = MathTex(
            "A = ",
            "\\begin{bmatrix} 1 & 3 \\\\ -2 & 0 \\end{bmatrix}"
        ).scale(1.2)
        
        vector = MathTex(
            "\\mathbf{x} = ",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}"
        ).scale(1.2).next_to(matrix, RIGHT, buff=1)
        
        labels = VGroup(
            Text("Matrix = Transformation", color=YELLOW).scale(0.6),
            Text("Vector = Input", color=YELLOW).scale(0.6)
        ).arrange(DOWN, buff=0.5).next_to(VGroup(matrix, vector), DOWN)
        
        with self.voiceover(text="Suppose you're given a vector and a matrix. How does multiplying the matrix by the vector tell you where that vector lands after the transformation?") as tracker:
            self.play(
                Write(matrix),
                Write(vector),
                Write(labels)
            )
            self.wait(1)
        
        # Frame 3: First column calculation
        first_column = MathTex(
            "x \\cdot",
            "\\begin{bmatrix} 1 \\\\ -2 \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} x \\\\ -2x \\end{bmatrix}"
        ).scale(1.2).to_edge(LEFT)
        first_column[1].set_color(RED)
        
        with self.voiceover(text="Here's the beautiful part: Matrix-vector multiplication exactly mirrors what we've been doing. You scale the first column by x...") as tracker:
            # Highlight first column of matrix
            matrix[1][1:3].set_color(RED)
            self.play(Write(first_column))
            self.wait(1)
        
        # Frame 4: Second column calculation
        second_column = MathTex(
            "y \\cdot",
            "\\begin{bmatrix} 3 \\\\ 0 \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} 3y \\\\ 0 \\end{bmatrix}"
        ).scale(1.2).next_to(first_column, RIGHT, buff=1)
        second_column[1].set_color(BLUE)
        
        with self.voiceover(text="...and the second column by y...") as tracker:
            # Highlight second column of matrix
            matrix[1][3:5].set_color(BLUE)
            self.play(Write(second_column))
            self.wait(1)
        
        # Frame 5: Show addition
        addition = MathTex(
            "\\begin{bmatrix} x \\\\ -2x \\end{bmatrix}",
            "+",
            "\\begin{bmatrix} 3y \\\\ 0 \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} x + 3y \\\\ -2x \\end{bmatrix}"
        ).scale(1.2).to_edge(RIGHT)
        addition[0].set_color(RED)
        addition[2].set_color(BLUE)
        
        with self.voiceover(text="...then add them together.") as tracker:
            self.play(Write(addition))
            self.wait(1)
        
        # Frame 6: Show complete multiplication
        complete_mult = MathTex(
            "\\begin{bmatrix} 1 & 3 \\\\ -2 & 0 \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} 1x + 3y \\\\ -2x + 0y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} x + 3y \\\\ -2x \\end{bmatrix}"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="This gives us the complete matrix-vector multiplication.") as tracker:
            self.play(Write(complete_mult))
            self.wait(1)
        
        # Frame 7: Demonstrate with transformation
        def matrix_transform(point):
            x, y, _ = point
            return [x + 3*y, -2*x, 0]
        
        # Create grid points
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        # Example vector
        example_vector = Arrow(start=ORIGIN, end=[2, 1], color=YELLOW, buff=0)
        
        with self.voiceover(text="Let's see this in action. The matrix multiplication tells us exactly where each vector lands under the transformation.") as tracker:
            self.play(
                *[FadeOut(mob) for mob in [matrix, vector, labels, first_column, second_column, addition]],
                Create(grid),
                Create(example_vector)
            )
            
            # Transform grid and vector
            self.play(
                *[dot.animate.move_to(matrix_transform(dot.get_center())) 
                  for dot in grid_points],
                example_vector.animate.put_start_and_end_on(ORIGIN, matrix_transform([2, 1, 0])),
                run_time=2
            )
        
        # Frame 8: Key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Matrix columns = transformed basis vectors", color=WHITE).scale(0.6),
            Text("• Multiplication = weighted combination", color=WHITE).scale(0.6),
            Text("• Matrix encodes entire transformation", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="Matrix-vector multiplication is just a weighted combination of the matrix columns — which are our transformed basis vectors! This is why matrix multiplication implements the transformation we visualized.") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section10(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("General 2×2 Matrix Transformation", color=WHITE)
        subtitle = Text("The Complete Picture", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now let's step back and look at the most general case.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show generic matrix
        generic_matrix = MathTex(
            "A = ",
            "\\begin{bmatrix} A & B \\\\ C & D \\end{bmatrix}"
        ).scale(1.2)
        
        matrix_labels = VGroup(
            MathTex("\\text{First column } = T(\\hat{\\imath}) = (A,C)", color=RED),
            MathTex("\\text{Second column } = T(\\hat{\\jmath}) = (B,D)", color=BLUE)
        ).arrange(DOWN, buff=0.5).next_to(generic_matrix, DOWN)
        
        with self.voiceover(text="For any two-by-two matrix, not just our specific example, the same story holds: The matrix describes where the basis vectors go.") as tracker:
            self.play(Write(generic_matrix))
            self.play(Write(matrix_labels))
            self.wait(1)
        
        # Frame 3: Show basis vector transformations
        # Original basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1], color=BLUE, buff=0)
        
        # Generic transformed basis vectors (example transformation)
        transformed_i = Arrow(start=ORIGIN, end=[2, 1], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[-1, 2], color=BLUE, buff=0)
        
        with self.voiceover(text="The first column tells us where i-hat lands, and the second column tells us where j-hat lands.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat)
            )
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j)
            )
            self.wait(1)
        
        # Frame 4: Show transformation steps
        step_by_step = VGroup(
            MathTex("\\text{Step 1: Multiply } x \\text{ by first column}"),
            MathTex("x \\times (A,C) = (Ax,Cx)", color=RED),
            MathTex("\\text{Step 2: Multiply } y \\text{ by second column}"),
            MathTex("y \\times (B,D) = (By,Dy)", color=BLUE),
            MathTex("\\text{Step 3: Add the results}"),
            MathTex("(Ax,Cx) + (By,Dy) = (Ax+By,Cx+Dy)")
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT)
        
        with self.voiceover(text="Then for any vector (x,y), the transformation follows a simple recipe: Multiply x by the first column, multiply y by the second column, and add the results together.") as tracker:
            self.play(Write(step_by_step))
            self.wait(1)
        
        # Frame 5: Show complete matrix multiplication
        complete_mult = MathTex(
            "\\begin{bmatrix} A & B \\\\ C & D \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} Ax + By \\\\ Cx + Dy \\end{bmatrix}"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="That's matrix-vector multiplication — and it's exactly how two-D linear transformations work!") as tracker:
            self.play(Write(complete_mult))
            self.wait(1)
        
        # Frame 6: Show different types of transformations
        def rotation_matrix(theta):
            return np.array([[np.cos(theta), -np.sin(theta)],
                            [np.sin(theta), np.cos(theta)]])
        
        def shear_matrix(k):
            return np.array([[1, k],
                            [0, 1]])
        
        def scale_matrix(sx, sy):
            return np.array([[sx, 0],
                            [0, sy]])
        
        # Create grid points
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        # Keep original grid faintly visible
        self.add(grid)
        
        with self.voiceover(text="Let's see some examples of what different matrices can do to space:") as tracker:
            # Rotation
            matrix_text = MathTex("\\text{Rotation:}")
            self.play(Write(matrix_text))
            theta = PI/3
            rot_matrix = rotation_matrix(theta)
            self.play(
                *[dot.animate.move_to([rot_matrix[0,0]*x + rot_matrix[0,1]*y,
                                     rot_matrix[1,0]*x + rot_matrix[1,1]*y, 0])
                  for dot in grid_points for x, y, _ in [dot.get_center()]],
                run_time=2
            )
            self.wait(1)
            
            # Shear
            self.play(matrix_text.animate.become(MathTex("\\text{Shear:}")))
            shear_matrix_val = shear_matrix(1)
            self.play(
                *[dot.animate.move_to([shear_matrix_val[0,0]*x + shear_matrix_val[0,1]*y,
                                     shear_matrix_val[1,0]*x + shear_matrix_val[1,1]*y, 0])
                  for dot in grid_points for x, y, _ in [dot.get_center()]],
                run_time=2
            )
            self.wait(1)
            
            # Scale
            self.play(matrix_text.animate.become(MathTex("\\text{Scale:}")))
            scale_matrix_val = scale_matrix(2, 0.5)
            self.play(
                *[dot.animate.move_to([scale_matrix_val[0,0]*x + scale_matrix_val[0,1]*y,
                                     scale_matrix_val[1,0]*x + scale_matrix_val[1,1]*y, 0])
                  for dot in grid_points for x, y, _ in [dot.get_center()]],
                run_time=2
            )
        
        # Frame 7: Key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Matrix columns = where basis vectors go", color=WHITE).scale(0.6),
            Text("• Transformation = linear combination", color=WHITE).scale(0.6),
            Text("• Any 2×2 matrix = some transformation", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="Every two-by-two matrix represents some transformation, and every transformation can be understood through where it sends the basis vectors.") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section11(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Example 1: Rotation by 90°", color=WHITE)
        subtitle = Text("A Concrete Example of Matrix Transformation", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="To make all of this more concrete, let's walk through a real example: A rotation by 90 degrees counterclockwise.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show original basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\hat{\\imath}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        with self.voiceover(text="How can we describe this rotation as a matrix? Well, just like before, we track where i-hat and j-hat land.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.wait(1)
        
        # Frame 3: Animate rotation
        def rotate_90(point):
            x, y, z = point
            return [-y, x, z]
        
        # Create rotated basis vectors
        rotated_i = Arrow(start=ORIGIN, end=[0, 1], color=RED, buff=0)
        rotated_j = Arrow(start=ORIGIN, end=[-1, 0], color=BLUE, buff=0)
        
        rotated_i_label = MathTex("T(\\hat{\\imath}) = (0,1)", color=RED).next_to(rotated_i.get_end(), UP)
        rotated_j_label = MathTex("T(\\hat{\\jmath}) = (-1,0)", color=BLUE).next_to(rotated_j.get_end(), LEFT)
        
        with self.voiceover(text="Let's think about it carefully. After rotating 90 degrees: i-hat, which originally points along the positive x-axis, now points straight up along the positive y-axis.") as tracker:
            self.play(
                ReplacementTransform(i_hat, rotated_i),
                ReplacementTransform(i_hat_label, rotated_i_label)
            )
            self.wait(1)
        
        with self.voiceover(text="And j-hat, which originally points along the positive y-axis, now points left along the negative x-axis.") as tracker:
            self.play(
                ReplacementTransform(j_hat, rotated_j),
                ReplacementTransform(j_hat_label, rotated_j_label)
            )
            self.wait(1)
        
        # Frame 4: Show matrix formation
        matrix = MathTex(
            "\\text{Rotation Matrix} = ",
            "\\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}"
        ).scale(1.2)
        
        matrix_explanation = VGroup(
            Text("First column = new î", color=RED).scale(0.6),
            Text("Second column = new ĵ", color=BLUE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        matrix_group = VGroup(matrix, matrix_explanation).arrange(DOWN).to_edge(RIGHT)
        
        with self.voiceover(text="Now we can package this information into our matrix. The first column comes from where i-hat landed, and the second column from where j-hat landed.") as tracker:
            self.play(Write(matrix_group))
            self.wait(1)
        
        # Frame 5: Demonstrate transformation
        # Create grid points
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        # Example vector
        example_vector = Arrow(start=ORIGIN, end=[2, 1], color=YELLOW, buff=0)
        example_label = MathTex("(x,y)", color=YELLOW).next_to(example_vector.get_end(), RIGHT)
        
        with self.voiceover(text="Let's see this transformation in action.") as tracker:
            self.play(
                Create(example_vector),
                Write(example_label)
            )
            
            # Transform grid and vector
            self.play(
                *[dot.animate.move_to(rotate_90(dot.get_center())) 
                  for dot in grid_points],
                example_vector.animate.put_start_and_end_on(ORIGIN, rotate_90([2, 1, 0])),
                example_label.animate.next_to(rotate_90([2, 1, 0]), RIGHT),
                run_time=2
            )
        
        # Frame 6: Show matrix multiplication
        multiplication = MathTex(
            "\\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} -y \\\\ x \\end{bmatrix}"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="When we multiply any vector (x,y) by this matrix, it rotates the vector exactly 90 degrees counterclockwise.") as tracker:
            self.play(Write(multiplication))
            self.wait(1)
        
        # Frame 7: Key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Simple rotation = 2×2 matrix", color=WHITE).scale(0.6),
            Text("• Matrix columns = rotated basis vectors", color=WHITE).scale(0.6),
            Text("• Multiplication = rotation of any vector", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="A simple rotation can be fully described by a two-by-two matrix. This is just one example of how matrices capture transformations of space.") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section12(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Example 2: Shear Transformation", color=WHITE)
        subtitle = Text("Sliding Space Along One Axis", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now let's look at another common type of linear transformation: a shear.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        with self.voiceover(text="In a shear, one direction stays fixed, while the other direction slides.") as tracker:
            self.play(Create(grid))
            self.wait(1)
        
        # Frame 2: Show original basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\hat{\\imath}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        with self.voiceover(text="Here's an example: i-hat stays exactly where it was — it doesn't move.") as tracker:
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.wait(1)
        
        # Frame 3: Show shear transformation
        def shear_transform(point):
            x, y, z = point
            return [x + y, y, z]
        
        # Create sheared basis vectors
        sheared_i = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)  # i_hat stays same
        sheared_j = Arrow(start=ORIGIN, end=[1, 1], color=BLUE, buff=0)  # j_hat shifts right
        
        sheared_i_label = MathTex("T(\\hat{\\imath}) = (1,0)", color=RED).next_to(sheared_i.get_end(), RIGHT)
        sheared_j_label = MathTex("T(\\hat{\\jmath}) = (1,1)", color=BLUE).next_to(sheared_j.get_end(), RIGHT)
        
        with self.voiceover(text="But j-hat shifts sideways, moving to the position (1,1).") as tracker:
            self.play(
                ReplacementTransform(i_hat, sheared_i),
                ReplacementTransform(i_hat_label, sheared_i_label)
            )
            self.play(
                ReplacementTransform(j_hat, sheared_j),
                ReplacementTransform(j_hat_label, sheared_j_label)
            )
            self.wait(1)
        
        # Frame 4: Show grid transformation
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="Let's visualize what that does to space. Watch how vertical lines start leaning to the right, while horizontal lines remain horizontal.") as tracker:
            # Keep original grid faintly visible
            self.add(grid)
            
            # Transform grid points
            self.play(
                *[dot.animate.move_to(shear_transform(dot.get_center())) 
                  for dot in grid_points],
                run_time=2
            )
        
        # Frame 5: Show matrix formation
        matrix = MathTex(
            "\\text{Shear Matrix} = ",
            "\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}"
        ).scale(1.2)
        
        matrix_explanation = VGroup(
            Text("First column = where î lands (1,0)", color=RED).scale(0.6),
            Text("Second column = where ĵ lands (1,1)", color=BLUE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        matrix_group = VGroup(matrix, matrix_explanation).arrange(DOWN).to_edge(RIGHT)
        
        with self.voiceover(text="Now let's package this transformation into a matrix. The first column shows where i-hat landed, and the second column shows where j-hat landed.") as tracker:
            self.play(Write(matrix_group))
            self.wait(1)
        
        # Frame 6: Show example computation
        example_vector = Arrow(start=ORIGIN, end=[2, 1], color=YELLOW, buff=0)
        example_label = MathTex("(2,1)", color=YELLOW).next_to(example_vector.get_end(), RIGHT)
        
        computation = MathTex(
            "\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}",
            "\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} 2+1 \\\\ 0+1 \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} 3 \\\\ 1 \\end{bmatrix}"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="Let's see how this matrix transforms a specific vector, say (2,1).") as tracker:
            self.play(
                Create(example_vector),
                Write(example_label)
            )
            self.play(Write(computation))
            
            # Transform the example vector
            self.play(
                example_vector.animate.put_start_and_end_on(ORIGIN, shear_transform([2, 1, 0])),
                example_label.animate.next_to(shear_transform([2, 1, 0]), RIGHT)
            )
            self.wait(1)
        
        # Frame 7: Show general formula
        general_formula = MathTex(
            "\\text{For any } (x,y):\\\\",
            "\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} x + y \\\\ y \\end{bmatrix}"
        ).scale(0.8).to_edge(LEFT)
        
        with self.voiceover(text="In general, this shear transformation adds the y-coordinate to the x-coordinate, while keeping y unchanged.") as tracker:
            self.play(Write(general_formula))
            self.wait(1)
        
        # Frame 8: Key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Shear slides space along one axis", color=WHITE).scale(0.6),
            Text("• Lines remain straight (linearity)", color=WHITE).scale(0.6),
            Text("• Matrix columns = transformed basis", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(general_formula, DOWN, buff=1)
        
        with self.voiceover(text="A shear transformation slides space along one axis, while keeping lines straight and evenly spaced — satisfying linearity. And once again, the columns of the matrix tell us exactly where the basis vectors go.") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section14(self):
        # Create initial grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Introduction
        title = Text("Linearly Dependent Basis Vectors", color=WHITE)
        subtitle = Text("The Collapse of Space", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="We've seen how linear transformations stretch, rotate, and shear space. But what if something more drastic happens?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show the matrix with dependent columns
        matrix = MathTex(
            "A = ",
            "\\begin{bmatrix} 2 & 4 \\\\ 1 & 2 \\end{bmatrix}",
            "\\quad \\text{(Note: column 2 is 2× column 1)}"
        ).scale(1.2)
        
        with self.voiceover(text="Suppose the transformed basis vectors — the columns of the matrix — are linearly dependent. That means one of them is just a multiple of the other.") as tracker:
            self.play(Write(matrix))
            self.wait(1)
        
        # Frame 3: Show basis vectors and their dependent transformation
        i_hat = Arrow(start=ORIGIN, end=[1, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\hat{\\imath}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create transformed basis vectors
        transformed_i = Arrow(start=ORIGIN, end=[2, 1], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[4, 2], color=BLUE, buff=0)
        
        transformed_i_label = MathTex("T(\\hat{\\imath}) = (2,1)", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("T(\\hat{\\jmath}) = (4,2) = 2\\cdot(2,1)", color=BLUE).next_to(transformed_j.get_end(), RIGHT)
        
        with self.voiceover(text="Let's see what happens to our basis vectors. i-hat goes to (2,1)...") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(i_hat_label, transformed_i_label)
            )
            self.wait(1)
        
        with self.voiceover(text="...and j-hat goes to (4,2), which is exactly twice the first vector! Both vectors lie along the same line.") as tracker:
            self.play(
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(j_hat_label, transformed_j_label)
            )
            self.wait(1)
        
        # Frame 4: Show collapse of space
        def collapse_transform(point):
            x, y, _ = point
            # Transform that collapses space onto the line defined by (2,1)
            return [2*x + 4*y, x + 2*y, 0]
        
        # Create grid points
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        # Create the target line
        target_line = Line(
            start=[-5*2, -5*1, 0],
            end=[5*2, 5*1, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="When this happens, the transformation squashes all of space onto a single line. This is a dramatic collapse — we go from two dimensions to one.") as tracker:
            # Show target line
            self.play(Create(target_line))
            
            # Transform grid points
            self.play(
                *[dot.animate.move_to(collapse_transform(dot.get_center())) 
                  for dot in grid_points],
                run_time=3
            )
        
        # Frame 5: Show example vectors getting mapped
        example_vectors = VGroup()
        example_points = [(1,0), (1,1), (0,1), (-1,1)]
        for x, y in example_points:
            vector = Arrow(
                start=ORIGIN,
                end=[x, y],
                color=GREEN,
                buff=0
            )
            example_vectors.add(vector)
        
        transformed_vectors = VGroup()
        for x, y in example_points:
            end_point = collapse_transform([x, y, 0])
            vector = Arrow(
                start=ORIGIN,
                end=end_point,
                color=GREEN,
                buff=0
            )
            transformed_vectors.add(vector)
        
        with self.voiceover(text="Different input vectors now get mapped to points along the same line. Information about the original position is lost in the direction perpendicular to this line.") as tracker:
            self.play(Create(example_vectors))
            self.play(
                ReplacementTransform(example_vectors, transformed_vectors)
            )
            self.wait(1)
        
        # Frame 6: Show mathematical formulation
        formula = MathTex(
            "T(x,y)", "&=", "x \\cdot (2,1)", "+", "y \\cdot (4,2)", "\\\\",
            "&=", "(2x + 4y, x + 2y)", "\\\\",
            "&=", "(2,1) \\cdot (x + 2y)"
        ).scale(0.8).to_edge(RIGHT)
        
        with self.voiceover(text="Mathematically, every output can be written as some scalar multiple of the vector (2,1). The two-dimensional input gets compressed into a one-dimensional output.") as tracker:
            self.play(Write(formula))
            self.wait(1)
        
        # Frame 7: Key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Dependent columns → dimension reduction", color=WHITE).scale(0.6),
            Text("• Space collapses to a line", color=WHITE).scale(0.6),
            Text("• Information is lost", color=WHITE).scale(0.6),
            Text("• Transformation is rank-deficient", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="This is called a rank-deficient transformation. It reduces the dimension of space, and in doing so, loses information about the original vectors.") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

if __name__ == "__main__":
    scene = LinearTransformations()
    scene.render() 