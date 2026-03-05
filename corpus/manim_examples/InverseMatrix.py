from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class Inversematrix(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections
        self.section1()  # Introduction
        self.clear()
        self.section3()  # Understanding Linear Systems
        self.clear()
        self.section4_5()  # From Linear Systems to Matrices and Geometric Interpretation
        self.clear()
        self.section6()  # Case 1: Nonzero Determinant
        self.clear()
        self.section7()  # Reverse Transformation and Inverse Matrix
        self.clear()
        self.section8()  # Concrete Geometric Examples
        self.clear()
        self.section9()  # Solving Linear Systems with Inverse
        self.clear()
        self.section10_11()  # Zero Determinant Cases

    def section1(self):
        # Frame 1: Main Title
        main_title = Text("The Geometry of Linear Systems", color=WHITE)
        subtitle = Text("Inverses, Column Space, Rank, and Null Space", color=YELLOW).scale(0.7)
        title_group = VGroup(main_title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Throughout this series, we've explored matrix and vector operations by thinking visually, treating them as transformations of space rather than just dry computations.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Flow Diagram
        # Create nodes
        matrix_node = Circle(radius=0.5).set_fill(BLUE)
        matrix_text = Text("Matrix", color=WHITE).scale(0.4)
        matrix_group = VGroup(matrix_node, matrix_text)
        
        transform_node = Circle(radius=0.7).set_fill(GREEN)
        transform_text = Text("Linear\nTransformation", color=WHITE).scale(0.4)
        transform_group = VGroup(transform_node, transform_text)
        
        vectors_node = Circle(radius=0.5).set_fill(RED)
        vectors_text = Text("New\nVectors", color=WHITE).scale(0.4)
        vectors_group = VGroup(vectors_node, vectors_text)
        
        # Arrange nodes
        flow_diagram = VGroup(matrix_group, transform_group, vectors_group).arrange(RIGHT, buff=1)
        
        # Add arrows
        arrow1 = Arrow(matrix_node.get_right(), transform_node.get_left())
        arrow2 = Arrow(transform_node.get_right(), vectors_node.get_left())
        
        flow_complete = VGroup(flow_diagram, arrow1, arrow2).next_to(title_group, DOWN, buff=1)
        
        with self.voiceover(text="This video is no exception. Today, we'll extend that intuition to cover four important concepts:") as tracker:
            self.play(Create(flow_complete))
            self.wait(1)
        
        # Frame 3: Four Key Concepts
        concepts = VGroup(
            Text("• Inverse matrices: how to undo a transformation", color=WHITE),
            Text("• Column space: understanding where vectors can land", color=WHITE),
            Text("• Rank: measuring how much space 'collapses'", color=WHITE),
            Text("• Null space: identifying vectors that vanish", color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        
        concepts.next_to(flow_complete, DOWN, buff=1)
        
        with self.voiceover(text="Inverse matrices: how to undo a transformation, Column space: understanding where vectors can land after transformation, Rank: measuring how much the space 'collapses' under a transformation, and Null space: identifying which vectors get flattened into nothingness.") as tracker:
            self.play(Write(concepts), run_time=4)
            self.wait(1)
        
        # Frame 4: Philosophy Box
        philosophy_box = VGroup(
            Text("Our Philosophy:", color=YELLOW).scale(0.7),
            Text("• Visual understanding > Memorizing algorithms", color=WHITE).scale(0.6),
            Text("• Build intuition, not computation", color=WHITE).scale(0.6),
            Text("• Focus on meaning, not mechanics", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        philosophy_box.to_edge(LEFT).shift(DOWN)
        
        with self.voiceover(text="Before we begin, a small note: We won't be focusing on calculation techniques like Gaussian elimination or how to row-reduce matrices. Instead, our focus here is on the geometric intuition — the mental imagery that lets you see transformations, not just compute them.") as tracker:
            self.play(Write(philosophy_box))
            self.wait(1)
        
        # Frame 5: Applications
        applications = VGroup(
            Text("Real-world Applications:", color=YELLOW).scale(0.7),
            Text("• Robotics", color=WHITE).scale(0.6),
            Text("• Computer Graphics", color=WHITE).scale(0.6),
            Text("• Physics Simulations", color=WHITE).scale(0.6),
            Text("• Data Analysis", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        applications.to_edge(RIGHT).shift(DOWN)
        
        with self.voiceover(text="In fact, in practical settings like engineering, computer science, and physics, we usually rely on computers to handle the tedious calculations. What matters most is knowing what these calculations mean.") as tracker:
            self.play(Write(applications))
            self.wait(1)
        
        # Frame 6: Transition to next scene
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        ).scale(0.3)
        
        plane.next_to(applications, DOWN, buff=1)
        
        with self.voiceover(text="So let's begin by seeing why linear algebra is such a powerful tool across almost every technical field.") as tracker:
            self.play(
                Create(plane),
                plane.animate.scale(3).move_to(ORIGIN),
                FadeOut(flow_complete),
                FadeOut(concepts),
                FadeOut(philosophy_box),
                FadeOut(applications),
                FadeOut(title_group),
                run_time=2
            )
            self.wait(1)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section3(self):
        # Frame 1: Introduction to Variables
        title = Text("Understanding Linear Systems", color=WHITE)
        subtitle = Text("A Visual Journey", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Imagine you have a collection of unknowns — numbers you want to find — and a collection of equations that relate them.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Scale Visualization
        # Create two balance scales
        def create_scale():
            base = Line(LEFT, RIGHT, color=WHITE)
            pivot = Triangle().scale(0.2).set_fill(WHITE)
            pivot.next_to(base, UP, buff=0)
            return VGroup(base, pivot)
        
        scale1 = create_scale()
        scale2 = create_scale()
        scales = VGroup(scale1, scale2).arrange(DOWN, buff=2)
        
        with self.voiceover(text="In some situations, those relationships are simple: Each variable is just scaled by a constant number, and these scaled versions are added together.") as tracker:
            self.play(Create(scales))
            self.wait(1)
        
        # Frame 3: Linear System Example
        equations = MathTex(
            "3", "x", "+", "2", "y", "=", "5", "\\\\",
            "4", "x", "-", "y", "=", "6"
        )
        
        # Color the coefficients and variables
        equations[0].set_color(RED)    # 3
        equations[1].set_color(RED)    # x
        equations[3].set_color(BLUE)   # 2
        equations[4].set_color(BLUE)   # y
        equations[8].set_color(RED)    # 4
        equations[9].set_color(RED)    # x
        equations[11].set_color(BLUE)  # y
        
        with self.voiceover(text="For example, here's a system involving two unknowns, x and y:") as tracker:
            self.play(Write(equations))
            self.wait(1)
        
        # Frame 4: Highlight Linear Structure
        linear_structure = VGroup(
            Text("Linear System Properties:", color=YELLOW).scale(0.7),
            Text("• Variables appear alone", color=WHITE).scale(0.6),
            Text("• Only scaling and addition", color=WHITE).scale(0.6),
            Text("• No products or powers", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="Notice how clean and structured this is: Each variable appears only by itself, scaled by some constant, and all terms are added up.") as tracker:
            self.play(Write(linear_structure))
            self.wait(1)
        
        # Frame 5: Nonlinear Example (crossed out)
        nonlinear_system = MathTex(
            "\\text{Not Linear:} \\\\",
            "x^2 + y = 5 \\quad \\text{(Quadratic)} \\\\",
            "xy - 3 = 2 \\quad \\text{(Product)}"
        ).set_color(RED_E)
        
        cross = VGroup(
            Line(UP + LEFT, DOWN + RIGHT, color=RED),
            Line(UP + RIGHT, DOWN + LEFT, color=RED)
        ).scale(2)
        
        nonlinear_group = VGroup(nonlinear_system, cross)
        nonlinear_group.next_to(linear_structure, RIGHT, buff=2)
        
        with self.voiceover(text="Importantly, there's no funny business — no variables multiplied together, no variables raised to powers, no sine or exponential functions sneaking in.") as tracker:
            self.play(Write(nonlinear_system))
            self.play(Create(cross))
            self.wait(1)
        
        # Frame 6: Matrix Preview
        matrix_preview = MathTex(
            "\\begin{bmatrix} 3 & 2 \\\\ 4 & -1 \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} 5 \\\\ 6 \\end{bmatrix}"
        ).to_edge(DOWN)
        
        with self.voiceover(text="Linear systems are special because they allow a very elegant mathematical treatment — and because, as you'll see soon, they naturally tie into matrix multiplication.") as tracker:
            self.play(Write(matrix_preview))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section4_5(self):
        # Frame 1: Start with system of equations
        title = Text("From Equations to Matrices", color=WHITE)
        subtitle = Text("A Geometric Journey", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        equations = MathTex(
            "3", "x", "+", "2", "y", "=", "5", "\\\\",
            "4", "x", "-", "y", "=", "6"
        )
        
        with self.voiceover(text="Now, when you look at a system of equations like this one, you might notice something beautiful: It can be neatly packaged using matrices and vectors.") as tracker:
            self.play(Write(title_group))
            self.play(title_group.animate.scale(0.8).to_edge(UP))
            self.play(Write(equations))
            self.wait(1)
        
        # Frame 2: Transform into matrix form
        # Create matrix components
        matrix_equation = MathTex(
            "\\begin{bmatrix} 3 & 2 \\\\ 4 & -1 \\end{bmatrix}",
            "\\begin{bmatrix} x \\\\ y \\end{bmatrix}",
            "=",
            "\\begin{bmatrix} 5 \\\\ 6 \\end{bmatrix}"
        ).arrange(RIGHT)

        # Color the elements after creation
        matrix_equation[0].set_color(RED)
        matrix_equation[1].set_color(BLUE)

        with self.voiceover(text="Here's how: Gather all the scaling constants into a matrix. Arrange all the unknown variables into a vector. And put all the constants on the right-hand side into another vector.") as tracker:
            # Highlight and move coefficients
            self.play(
                equations[0:2].animate.set_color(RED),
                equations[3:5].animate.set_color(BLUE),
                equations[6:8].animate.set_color(RED),
                equations[9:11].animate.set_color(BLUE),
            )
            self.play(
                TransformFromCopy(equations, matrix_equation),
                FadeOut(equations)
            )
            self.wait(1)
        
        # Frame 3: Show compact notation
        compact_notation = MathTex("A\\mathbf{x} = \\mathbf{v}")
        notation_explanation = VGroup(
            Text("where:", color=WHITE).scale(0.7),
            Text("A is the coefficient matrix", color=WHITE).scale(0.6),
            Text("x is the unknowns vector", color=WHITE).scale(0.6),
            Text("v is the constants vector", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        notation_group = VGroup(compact_notation, notation_explanation).arrange(DOWN, buff=0.5)
        notation_group.next_to(matrix_equation, DOWN, buff=1)
        
        with self.voiceover(text="We can summarize this compactly as A x equals v, where A is the coefficient matrix, x is the unknowns vector, and v is the constants vector.") as tracker:
            self.play(Write(notation_group))
            self.wait(1)
        
        # Frame 4: Geometric interpretation
        # Create grid for transformation
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Define transformation matrix
        matrix = [[3, 2], [4, -1]]
        def transform_point(point):
            x, y, z = point
            return [3*x + 2*y, 4*x - y, z]
        
        with self.voiceover(text="Now, this is much more than just a notational convenience. It reveals a deep, beautiful geometric meaning behind solving systems of equations.") as tracker:
            self.play(
                FadeOut(matrix_equation),
                FadeOut(notation_group),
                Create(grid)
            )
            self.wait(1)
        
        # Show transformation
        transformed_grid = grid.copy().apply_function(transform_point)
        
        # Create vector v
        v_vector = Arrow(ORIGIN, [5, 6, 0], color=YELLOW, buff=0)
        v_label = MathTex("\\mathbf{v}", color=YELLOW).next_to(v_vector.get_end(), RIGHT)
        
        with self.voiceover(text="Think of the matrix A not just as a table of numbers, but as a linear transformation — a rule for how space itself gets stretched, rotated, squished, or skewed.") as tracker:
            self.play(
                ReplacementTransform(grid, transformed_grid),
                Create(v_vector),
                Write(v_label),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Solving interpretation
        solving_text = VGroup(
            Text("Solving Ax = v means:", color=YELLOW).scale(0.7),
            Text("Which input vector x", color=WHITE).scale(0.6),
            Text("gets transformed to v?", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        # Add "rewind" effect
        rewind_arrow = CurvedArrow(
            v_vector.get_end(), ORIGIN,
            angle=-TAU/4,
            color=GREEN
        )
        
        with self.voiceover(text="Solving the equation A x equals v is like asking: 'Which input vector x will be transformed into the output vector v?' Instead of juggling a mess of equations, you can now visualize the problem: Imagine taking all of space, applying the transformation represented by A, and asking, 'Where did v come from originally?'") as tracker:
            self.play(Write(solving_text))
            self.play(Create(rewind_arrow))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section6(self):
        # Frame 1: Introduction
        title = Text("Case 1: Nonzero Determinant", color=WHITE)
        subtitle = Text("Unique Solutions and Invertibility", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now, how we think about solutions to the equation A x equals v depends heavily on one crucial property of the matrix A: its determinant.") as tracker:
            self.play(Write(title_group))
            self.play(title_group.animate.scale(0.8).to_edge(UP))
            self.wait(1)
        
        # Frame 2: Determinant Recall
        det_formula = MathTex(
            "\\det(A) = \\text{scaling factor of area/volume}"
        ).next_to(title_group, DOWN)
        
        # Create grid for transformation
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Define transformation matrix with det = 2
        matrix = [[2, 0], [0, 1]]  # det = 2
        def transform_point(point):
            x, y, z = point
            return [2*x, y, z]
        
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW        )
        
        with self.voiceover(text="Recall from earlier intuition: The determinant measures how the transformation associated with A scales area or volume.") as tracker:
            self.play(Write(det_formula))
            self.play(Create(grid), Create(unit_square))
            self.wait(1)
        
        # Show transformation
        transformed_grid = grid.copy().apply_function(transform_point)
        transformed_square = unit_square.copy().apply_function(transform_point)
        
        area_label = MathTex("\\text{Area} \\times 2").next_to(transformed_square, RIGHT)
        
        with self.voiceover(text="If the determinant is nonzero, it means that the transformation doesn't squish all of space into a lower dimension. No collapsing onto a line or a point.") as tracker:
            self.play(
                ReplacementTransform(grid, transformed_grid),
                ReplacementTransform(unit_square, transformed_square),
                Write(area_label),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: Unique Solution Statement
        unique_solution = MathTex(
            "\\text{If } \\det(A) \\neq 0,",
            "\\text{ then for every } \\mathbf{v},",
            "\\exists! \\mathbf{x}",
            "\\text{ such that }",
            "A\\mathbf{x} = \\mathbf{v}"
        ).arrange(RIGHT, buff=0.2).scale(0.8)
        
        unique_solution.next_to(transformed_grid, UP)
        
        with self.voiceover(text="And here's the beautiful result: Whenever det(A) is not zero, for any vector v you choose, there exists exactly one and only one vector x that maps to it under A.") as tracker:
            self.play(Write(unique_solution))
            self.wait(1)
        
        # Frame 4: Visualization of Unique Solution
        # Create target vector v
        v_vector = Arrow(ORIGIN, [3, 2, 0], color=YELLOW, buff=0)
        v_label = MathTex("\\mathbf{v}", color=YELLOW).next_to(v_vector.get_end(), RIGHT)
        
        # Create original vector x
        x_vector = Arrow(ORIGIN, [1.5, 2, 0], color=GREEN, buff=0)
        x_label = MathTex("\\mathbf{x}", color=GREEN).next_to(x_vector.get_end(), RIGHT)
        
        with self.voiceover(text="In other words, the transformation is invertible. Every output comes from exactly one unique input.") as tracker:
            self.play(Create(v_vector), Write(v_label))
            self.play(Create(x_vector), Write(x_label))
            
            # Add curved arrow to show inverse relationship
            inverse_arrow = CurvedArrow(
                v_vector.get_end(), x_vector.get_end(),
                angle=-TAU/4,
                color=WHITE
            )
            self.play(Create(inverse_arrow))
            self.wait(1)
        
        # Frame 5: Mathematical Solution
        solution_eq = MathTex(
            "\\mathbf{x} = A^{-1}\\mathbf{v}"
        ).to_edge(RIGHT)
        
        inverse_explanation = VGroup(
            Text("• Transformation is invertible", color=WHITE).scale(0.6),
            Text("• Every output has unique input", color=WHITE).scale(0.6),
            Text("• Solution found by inverse matrix", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(solution_eq, DOWN)
        
        with self.voiceover(text="Mathematically, solving for x becomes as simple as multiplying by A inverse. Visually, imagine you have a complex stretching and twisting of space. You point to a spot — your vector v — and ask: 'If I run the movie backwards, where did this point originate?' Thanks to nonzero determinant, you know there's exactly one answer.") as tracker:
            self.play(Write(solution_eq))
            self.play(Write(inverse_explanation))
            
            # Animate "rewinding" transformation
            self.play(
                Indicate(v_vector, color=YELLOW),
                Indicate(inverse_arrow, color=WHITE),
                Indicate(x_vector, color=GREEN),
                run_time=2
            )
            self.wait(2)
        
        # Frame 6: Key Points Summary
        key_points = VGroup(
            Text("Key Points:", color=YELLOW).scale(0.7),
            Text("• det(A) ≠ 0 → No collapse of space", color=WHITE).scale(0.6),
            Text("• One-to-one correspondence", color=WHITE).scale(0.6),
            Text("• Inverse transformation exists", color=WHITE).scale(0.6),
            Text("• Unique solution guaranteed", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="This property is fundamental. It means that if you can measure an output v, you can always recover where it came from by applying the inverse of A.") as tracker:
            self.play(Write(key_points))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section7(self):
        # Frame 1: Introduction
        title = Text("Reverse Transformation and Inverse Matrix", color=WHITE)
        subtitle = Text("Undoing Linear Transformations", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="When a matrix A has a nonzero determinant, we know it represents an invertible transformation. But what exactly is the nature of this inverse transformation?") as tracker:
            self.play(Write(title_group))
            self.play(title_group.animate.scale(0.8).to_edge(UP))
            self.wait(1)
        
        # Frame 2: Inverse Matrix Definition
        inverse_def = MathTex(
            "A^{-1}", "\\text{ is the inverse matrix that undoes }", "A"
        )
        
        with self.voiceover(text="Mathematically, we call it the inverse matrix, denoted by A inverse.") as tracker:
            self.play(Write(inverse_def))
            self.wait(1)
        
        # Frame 3: Core Property
        core_property = MathTex(
            "A^{-1}A = I",
            "\\quad \\text{where } I \\text{ is the identity matrix}"
        ).next_to(inverse_def, DOWN)
        
        identity_matrix = MathTex(
            "I = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}"
        ).next_to(core_property, DOWN)
        
        with self.voiceover(text="The defining property of the inverse is very simple but extremely powerful: If you first apply A to a vector and then apply A inverse, you land right back where you started.") as tracker:
            self.play(Write(core_property))
            self.play(Write(identity_matrix))
            self.wait(1)
        
        # Frame 4: Rotation Example
        # Create grid for transformation
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Create vector to transform
        vector = Arrow(ORIGIN, [2, 1, 0], color=YELLOW, buff=0)
        vector_label = MathTex("\\mathbf{v}", color=YELLOW).next_to(vector.get_end(), RIGHT)
        
        # Define rotation transformations
        def rotate_ccw(point):
            x, y, z = point
            return [-y, x, z]  # 90° CCW
        
        def rotate_cw(point):
            x, y, z = point
            return [y, -x, z]  # 90° CW
        
        with self.voiceover(text="To help build some geometric intuition, think about simple transformations: If A is a 90-degree counterclockwise rotation, A inverse is a 90-degree clockwise rotation.") as tracker:
            self.play(
                FadeOut(inverse_def),
                FadeOut(core_property),
                FadeOut(identity_matrix),
                Create(grid),
                Create(vector),
                Write(vector_label)
            )
            
            # Show CCW rotation
            rotated_grid = grid.copy().apply_function(rotate_ccw)
            rotated_vector = vector.copy().apply_function(rotate_ccw)
            rotated_label = MathTex("A\\mathbf{v}", color=YELLOW).next_to(rotated_vector.get_end(), RIGHT)
            
            self.play(
                ReplacementTransform(grid, rotated_grid),
                ReplacementTransform(vector, rotated_vector),
                ReplacementTransform(vector_label, rotated_label),
                run_time=2
            )
            
            # Show CW rotation (inverse)
            original_grid = grid.copy()
            original_vector = vector.copy()
            original_label = vector_label.copy()
            
            self.play(
                ReplacementTransform(rotated_grid, original_grid),
                ReplacementTransform(rotated_vector, original_vector),
                ReplacementTransform(rotated_label, original_label),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Shear Example
        def shear_right(point):
            x, y, z = point
            return [x + y, y, z]
        
        def shear_left(point):
            x, y, z = point
            return [x - y, y, z]
        
        with self.voiceover(text="If A is a rightward shear that shifts vectors horizontally, A inverse is a leftward shear that undoes the shift.") as tracker:
            # Show right shear
            sheared_grid = grid.copy().apply_function(shear_right)
            sheared_vector = vector.copy().apply_function(shear_right)
            sheared_label = MathTex("A\\mathbf{v}", color=YELLOW).next_to(sheared_vector.get_end(), RIGHT)
            
            self.play(
                ReplacementTransform(original_grid, sheared_grid),
                ReplacementTransform(original_vector, sheared_vector),
                ReplacementTransform(original_label, sheared_label),
                run_time=2
            )
            
            # Show left shear (inverse)
            self.play(
                ReplacementTransform(sheared_grid, original_grid),
                ReplacementTransform(sheared_vector, original_vector),
                ReplacementTransform(sheared_label, original_label),
                run_time=2
            )
            self.wait(1)
        
        # Frame 6: Solution Formula
        solution_formula = MathTex(
            "\\mathbf{x} = A^{-1}\\mathbf{v}",
            "\\quad \\text{(Solution to } A\\mathbf{x} = \\mathbf{v}\\text{)}"
        ).to_edge(DOWN)
        
        with self.voiceover(text="Thus, when solving the system A x equals v, we can find the unknown vector x simply by applying the inverse transformation to v.") as tracker:
            self.play(Write(solution_formula))
            self.wait(1)
        
        # Frame 7: Key Points Summary
        key_points = VGroup(
            Text("Key Points:", color=YELLOW).scale(0.7),
            Text("• A⁻¹ undoes what A does", color=WHITE).scale(0.6),
            Text("• A⁻¹A = I (identity)", color=WHITE).scale(0.6),
            Text("• Solution x = A⁻¹v", color=WHITE).scale(0.6),
            Text("• Geometric meaning: rewind transformation", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="In other words: Finding x is the same as rewinding the transformation and tracing the target v backward through space.") as tracker:
            self.play(Write(key_points))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section8(self):
        # Frame 1: Introduction
        title = Text("Concrete Geometric Examples", color=WHITE)
        subtitle = Text("Visualizing Inverse Transformations", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="To make the concept of an inverse transformation more vivid, let's look at a few simple examples where the transformation A and its inverse A inverse are easy to visualize.") as tracker:
            self.play(Write(title_group))
            self.play(title_group.animate.scale(0.8).to_edge(UP))
            self.wait(1)
        
        # Frame 2: Rotation Example Setup
        rotation_matrices = VGroup(
            MathTex("A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}"),
            MathTex("A^{-1} = \\begin{bmatrix} 0 & 1 \\\\ -1 & 0 \\end{bmatrix}")
        ).arrange(RIGHT, buff=1)
        
        # Create grid for transformation
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        ).scale(0.5)
        
        # Create a square to track
        square = Square(side_length=1, color=YELLOW)
        
        # Define rotation transformations
        def rotate_ccw(point):
            x, y, z = point
            return [-y, x, z]  # 90° CCW
        
        def rotate_cw(point):
            x, y, z = point
            return [y, -x, z]  # 90° CW
        
        with self.voiceover(text="First, imagine that A rotates space 90 degrees counterclockwise around the origin. Then the inverse A inverse would rotate everything 90 degrees clockwise to undo it.") as tracker:
            self.play(Write(rotation_matrices))
            self.play(
                rotation_matrices.animate.scale(0.8).to_edge(RIGHT),
                Create(grid),
                Create(square)
            )
            self.wait(1)
        
        # Show rotation sequence
        rotated_grid = grid.copy().apply_function(rotate_ccw)
        rotated_square = square.copy().apply_function(rotate_ccw)
        
        with self.voiceover(text="Let's see this in action. First, we apply A, rotating everything counterclockwise by 90 degrees.") as tracker:
            self.play(
                ReplacementTransform(grid, rotated_grid),
                ReplacementTransform(square, rotated_square),
                run_time=2
            )
            self.wait(1)
        
        # Show inverse rotation
        original_grid = grid.copy()
        original_square = square.copy()
        
        with self.voiceover(text="Then we apply A inverse, rotating clockwise by 90 degrees, which brings everything back to its original position.") as tracker:
            self.play(
                ReplacementTransform(rotated_grid, original_grid),
                ReplacementTransform(rotated_square, original_square),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: Shear Example
        shear_matrices = VGroup(
            MathTex("A = \\begin{bmatrix} 1 & k \\\\ 0 & 1 \\end{bmatrix}"),
            MathTex("A^{-1} = \\begin{bmatrix} 1 & -k \\\\ 0 & 1 \\end{bmatrix}")
        ).arrange(RIGHT, buff=1)
        
        # Define shear transformations
        def shear_right(point, k=1):
            x, y, z = point
            return [x + k*y, y, z]
        
        def shear_left(point, k=1):
            x, y, z = point
            return [x - k*y, y, z]
        
        with self.voiceover(text="Next, think about a shear transformation. For example, a rightward shear might push all points horizontally based on their vertical position, dragging vertical lines diagonally to the right.") as tracker:
            self.play(
                FadeOut(rotation_matrices),
                Write(shear_matrices)
            )
            self.play(shear_matrices.animate.scale(0.8).to_edge(RIGHT))
            
            # Show right shear
            sheared_grid = grid.copy().apply_function(lambda p: shear_right(p, k=1))
            sheared_square = square.copy().apply_function(lambda p: shear_right(p, k=1))
            
            self.play(
                ReplacementTransform(original_grid, sheared_grid),
                ReplacementTransform(original_square, sheared_square),
                run_time=2
            )
            self.wait(1)
        
        with self.voiceover(text="The inverse transformation would perform a leftward shear, undoing that slant and restoring the grid to vertical lines.") as tracker:
            # Show left shear (inverse)
            self.play(
                ReplacementTransform(sheared_grid, original_grid),
                ReplacementTransform(sheared_square, original_square),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Key Points Summary
        key_points = VGroup(
            Text("Key Points:", color=YELLOW).scale(0.7),
            Text("• Rotation: inverse rotates opposite way", color=WHITE).scale(0.6),
            Text("• Shear: inverse shears opposite direction", color=WHITE).scale(0.6),
            Text("• A⁻¹ always perfectly undoes A", color=WHITE).scale(0.6),
            Text("• Result: return to original state", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        with self.voiceover(text="In each case, the pattern is clear: whatever distortion A applies to space, A inverse precisely cancels it out, returning everything to its original configuration. This is the essence of invertibility in linear transformations.") as tracker:
            self.play(
                FadeOut(shear_matrices),
                Write(key_points)
            )
            
            # Show one final transformation cycle
            self.play(
                ReplacementTransform(original_grid, sheared_grid),
                ReplacementTransform(original_square, sheared_square),
                run_time=1
            )
            self.play(
                ReplacementTransform(sheared_grid, original_grid),
                ReplacementTransform(sheared_square, original_square),
                run_time=1
            )
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section9(self):
        # Frame 1: Introduction
        title = Text("Solving Linear Systems by Applying the Inverse", color=WHITE)
        subtitle = Text("A Geometric Approach", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now that we understand what an inverse matrix A inverse is and what it does geometrically, let's come back to the central question: How do we actually solve a system like A x equals v?") as tracker:
            self.play(Write(title_group))
            self.play(title_group.animate.scale(0.8).to_edge(UP))
            self.wait(1)
        
        # Frame 2: Core Equation
        system_eq = MathTex("A\\mathbf{x} = \\mathbf{v}")
        solution_eq = MathTex("\\mathbf{x} = A^{-1}\\mathbf{v}")
        equations = VGroup(system_eq, solution_eq).arrange(DOWN, buff=0.5)
        
        with self.voiceover(text="If the matrix A is invertible — meaning its determinant is nonzero — solving the system is beautifully simple: Just apply the inverse transformation to the vector v.") as tracker:
            self.play(Write(system_eq))
            self.play(Write(solution_eq))
            self.wait(1)
        
        # Frame 3: Geometric Visualization
        # Create grid and vectors
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        ).scale(0.7)
        
        # Create vectors
        x_vector = Arrow(ORIGIN, [1, 2, 0], color=GREEN, buff=0)
        x_label = MathTex("\\mathbf{x}", color=GREEN).next_to(x_vector.get_end(), RIGHT)
        
        # Define transformation (example: rotation + stretch)
        def transform(point):
            x, y, z = point
            return [2*x - y, x + 2*y, z]
        
        def inverse_transform(point):
            x, y, z = point
            return [(2*x + y)/5, (-x + 2*y)/5, z]
        
        with self.voiceover(text="Geometrically, A stretches, skews, and rotates space to map x onto v.") as tracker:
            self.play(
                FadeOut(equations),
                Create(grid),
                Create(x_vector),
                Write(x_label)
            )
            
            # Show forward transformation
            transformed_grid = grid.copy().apply_function(transform)
            transformed_vector = x_vector.copy().apply_function(transform)
            v_label = MathTex("\\mathbf{v}", color=YELLOW).next_to(transformed_vector.get_end(), RIGHT)
            
            self.play(
                ReplacementTransform(grid, transformed_grid),
                ReplacementTransform(x_vector, transformed_vector),
                ReplacementTransform(x_label, v_label),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Applying the Inverse
        with self.voiceover(text="A inverse undoes that distortion, tracing back to find the original x.") as tracker:
            # Show inverse transformation
            self.play(
                transformed_grid.animate.apply_function(inverse_transform),
                transformed_vector.animate.apply_function(inverse_transform),
                ReplacementTransform(v_label, x_label),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Mathematical Process
        process = VGroup(
            MathTex("A\\mathbf{x} = \\mathbf{v}"),
            MathTex("A^{-1}(A\\mathbf{x}) = A^{-1}\\mathbf{v}"),
            MathTex("(A^{-1}A)\\mathbf{x} = A^{-1}\\mathbf{v}"),
            MathTex("I\\mathbf{x} = A^{-1}\\mathbf{v}"),
            MathTex("\\mathbf{x} = A^{-1}\\mathbf{v}")
        ).arrange(DOWN, buff=0.3)
        
        with self.voiceover(text="This method hinges on one crucial assumption: That A actually has an inverse — which is only true if the determinant of A is not zero.") as tracker:
            self.play(
                FadeOut(transformed_grid),
                FadeOut(transformed_vector),
                FadeOut(x_label),
                Write(process)
            )
            self.wait(1)
        
        # Frame 6: Key Points
        key_points = VGroup(
            Text("Key Points:", color=YELLOW).scale(0.7),
            Text("• Solution: x = A⁻¹v", color=WHITE).scale(0.6),
            Text("• Geometrically: rewind the transformation", color=WHITE).scale(0.6),
            Text("• Requires det(A) ≠ 0", color=WHITE).scale(0.6),
            Text("• Clean, direct solution method", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        condition = MathTex(
            "\\text{Requires: }",
            "\\det(A) \\neq 0"
        ).set_color(YELLOW).next_to(key_points, DOWN, buff=0.5)
        
        with self.voiceover(text="Instead of needing messy equation-solving techniques or elimination methods, the inverse gives a direct, clean solution.") as tracker:
            self.play(
                Write(key_points),
                Write(condition)
            )
            self.wait(2)
        
        # Frame 7: Preview of Next Topic
        next_topic = Text("Next: What happens when det(A) = 0?", color=YELLOW).scale(0.7)
        next_topic.to_edge(DOWN)
        
        with self.voiceover(text="We'll see later what happens when that's not the case.") as tracker:
            self.play(Write(next_topic))
            self.wait(1)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section10_11(self):
        # Frame 1: Introduction
        title = Text("Zero Determinant: When No Inverse Exists", color=WHITE)
        subtitle = Text("But Solutions May Still Exist", color=YELLOW).scale(0.7)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="When the determinant of a matrix A is zero, it means the transformation associated with A collapses space into a lower dimension.") as tracker:
            self.play(Write(title_group))
            self.play(title_group.animate.scale(0.8).to_edge(UP))
            self.wait(1)
        
        # Frame 2: Collapsing Space Visualization
        # Create 2D grid
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        ).scale(0.7)
        
        # Define collapse transformation (onto y=x line)
        def collapse_to_line(point):
            x, y, z = point
            k = (x + y) / 2
            return [k, k, z]
        
        with self.voiceover(text="A 2D plane might squish into a 1D line. A 3D space might flatten onto a plane, or even collapse down to a point.") as tracker:
            self.play(Create(grid))
            
            # Show collapse transformation
            collapsed_grid = grid.copy().apply_function(collapse_to_line)
            self.play(
                ReplacementTransform(grid, collapsed_grid),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: No Inverse Exists
        no_inverse = MathTex(
            "\\text{If } \\det(A) = 0 \\text{, then } A^{-1} \\text{ does not exist}"
        ).next_to(collapsed_grid, UP)
        
        with self.voiceover(text="As a result, A cannot have an inverse. There's no way to 'undo' a collapse — you can't take a line and uniquely expand it back into a plane.") as tracker:
            self.play(Write(no_inverse))
            self.wait(1)
        
        # Frame 4: Solutions on Collapsed Space
        # Create vectors
        v_on_line = Arrow(ORIGIN, [2, 2, 0], color=YELLOW, buff=0)
        v_off_line = Arrow(ORIGIN, [2, 3, 0], color=RED, buff=0)
        
        # Create multiple solution vectors
        solution_vectors = VGroup(
            Arrow(ORIGIN, [1, 3, 0], color=GREEN, buff=0),
            Arrow(ORIGIN, [2, 2, 0], color=GREEN, buff=0),
            Arrow(ORIGIN, [3, 1, 0], color=GREEN, buff=0)
        )
        
        with self.voiceover(text="However — and this is important — even though an inverse doesn't exist, it might still be possible to solve the system A x equals v, but only under special circumstances.") as tracker:
            # Show vector on the line (solvable case)
            self.play(
                Create(v_on_line),
                Write(MathTex("\\mathbf{v}_1", color=YELLOW).next_to(v_on_line.get_end(), RIGHT))
            )
            
            # Show multiple solutions
            self.play(Create(solution_vectors))
            self.wait(1)
        
        with self.voiceover(text="The key condition is that v must happen to land exactly inside the space that everything collapsed onto.") as tracker:
            # Show vector off the line (unsolvable case)
            self.play(
                Create(v_off_line),
                Write(MathTex("\\mathbf{v}_2", color=RED).next_to(v_off_line.get_end(), RIGHT))
            )
            self.wait(1)
        
        # Frame 5: Mathematical Summary
        summary = VGroup(
            MathTex("\\text{When } \\det(A) = 0:"),
            MathTex("\\bullet \\text{ If } \\mathbf{v} \\in \\text{Col}(A) \\rightarrow \\text{ infinitely many solutions}"),
            MathTex("\\bullet \\text{ If } \\mathbf{v} \\notin \\text{Col}(A) \\rightarrow \\text{ no solutions}")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8)
        
        summary.to_edge(RIGHT)
        
        with self.voiceover(text="When v lies on that collapsed space, you often get infinitely many solutions, not just one. That's because many different vectors x might get squashed into the same output v. But if v lies off the collapsed subspace — even slightly — there's no solution at all.") as tracker:
            self.play(Write(summary))
            
            # Highlight the two cases
            self.play(
                Indicate(v_on_line, color=YELLOW),
                Indicate(solution_vectors, color=GREEN)
            )
            self.play(
                Indicate(v_off_line, color=RED)
            )
            self.wait(2)
        
        # Frame 6: Key Points
        key_points = VGroup(
            Text("Key Points:", color=YELLOW).scale(0.7),
            Text("• det(A) = 0 → space collapses", color=WHITE).scale(0.6),
            Text("• No inverse exists", color=WHITE).scale(0.6),
            Text("• Solutions exist if v in Col(A)", color=WHITE).scale(0.6),
            Text("• Usually infinitely many solutions", color=WHITE).scale(0.6),
            Text("• No solutions if v outside Col(A)", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        key_points.to_edge(LEFT)
        
        with self.voiceover(text="To summarize: When the determinant is zero, the transformation collapses space. No inverse exists, but solutions may exist if and only if v lies in the column space. And when solutions exist, there are usually infinitely many of them.") as tracker:
            self.play(Write(key_points))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

if __name__ == "__main__":
    scene = Inversematrix()
    scene.render()