from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class Determinants(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections
        self.section1()  # Recap & Transition into Determinants
        self.clear()
        self.section2()  # Area Change via Scaling Matrix
        self.clear()
        self.section3()  # Shear Transformation and Preserving Area
        self.clear()
        self.section4()  # From Unit Square to Any Shape
        self.clear()
        self.section5()  # What is the Determinant?
        self.clear()
        self.section6()  # What Does It Mean When det(A) = 0?
        self.clear()
        self.section7()  # Negative Determinants and Orientation Flipping
        self.clear()
        self.section8()  # From Positive to Negative Determinants
        self.clear()
        self.section9()  # Determinants in Three Dimensions
        self.clear()
        self.section10()  # Zero Determinant in Three Dimensions
        self.clear()
        self.section11()  # Orientation in 3D - Right-Hand Rule
        self.clear()
        self.section12()  # Computing the Determinant of a 2×2 Matrix
        self.clear()
        self.section13()  # Determinants for Larger Matrices
        self.clear()
        self.section14()  # The Determinant of a Product and Looking Ahead
        
    def section1(self):
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
        title = Text("Understanding Determinants", color=WHITE)
        subtitle = Text("How Transformations Scale Space", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Hello again! Now that you have a solid visual intuition for what linear transformations are and how they're represented with matrices, let's dive deeper.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show unit square and basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i} = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j} = \\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\end{bmatrix}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="In this scene, we'll explore how much a linear transformation stretches or squishes space. We'll use area as our guide.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(Create(unit_square))
            self.wait(1)
        
        # Frame 3: Mathematical setup
        math_setup = MathTex(
            "T: \\mathbb{R}^2 \\to \\mathbb{R}^2",
            "\\quad",
            "A \\in \\mathbb{R}^{2\\times2}"
        ).next_to(title_group, DOWN)
        
        area_equation = MathTex(
            "\\text{Area}_{\\text{after}} = \\det(A) \\cdot \\text{Area}_{\\text{before}}"
        ).next_to(math_setup, DOWN)
        
        with self.voiceover(text="This idea leads us to one of the most meaningful quantities in linear algebra: The Determinant.") as tracker:
            self.play(Write(math_setup))
            self.play(Write(area_equation))
            self.wait(1)
        
        # Frame 4: Show example transformations
        # 1. Scaling transformation
        def scale_transform(point, sx=2, sy=0.5):
            x, y, z = point
            return [sx*x, sy*y, z]
        
        # 2. Shear transformation
        def shear_transform(point, k=1):
            x, y, z = point
            return [x + k*y, y, z]
        
        # 3. Rotation transformation
        def rotate_transform(point, angle=PI/4):
            x, y, z = point
            return [
                x*np.cos(angle) - y*np.sin(angle),
                x*np.sin(angle) + y*np.cos(angle),
                z
            ]
        
        # Create grid points for transformation
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="A matrix transformation doesn't just move vectors around — it can change the size of regions in space. Let's look at some examples:") as tracker:
            # Keep original grid faintly visible
            faded_grid = grid.copy()
            self.add(faded_grid)
            
            # Show scaling transformation
            self.play(
                *[dot.animate.move_to(scale_transform(dot.get_center())) 
                  for dot in grid_points],
                unit_square.animate.apply_function(lambda p: scale_transform(p)),
                i_hat.animate.put_start_and_end_on(ORIGIN, scale_transform([1, 0, 0])),
                j_hat.animate.put_start_and_end_on(ORIGIN, scale_transform([0, 1, 0])),
                i_hat_label.animate.next_to(scale_transform([1, 0, 0]), RIGHT),
                j_hat_label.animate.next_to(scale_transform([0, 1, 0]), UP),
                run_time=2
            )
            self.wait(1)
            
            # Show shear transformation
            self.play(
                *[dot.animate.move_to(shear_transform(dot.get_center())) 
                  for dot in grid_points],
                unit_square.animate.apply_function(lambda p: shear_transform(p)),
                i_hat.animate.put_start_and_end_on(ORIGIN, shear_transform([1, 0, 0])),
                j_hat.animate.put_start_and_end_on(ORIGIN, shear_transform([0, 1, 0])),
                i_hat_label.animate.next_to(shear_transform([1, 0, 0]), RIGHT),
                j_hat_label.animate.next_to(shear_transform([0, 1, 0]), UP),
                run_time=2
            )
            self.wait(1)
            
            # Show rotation transformation
            self.play(
                *[dot.animate.move_to(rotate_transform(dot.get_center())) 
                  for dot in grid_points],
                unit_square.animate.apply_function(lambda p: rotate_transform(p)),
                i_hat.animate.put_start_and_end_on(ORIGIN, rotate_transform([1, 0, 0])),
                j_hat.animate.put_start_and_end_on(ORIGIN, rotate_transform([0, 1, 0])),
                i_hat_label.animate.next_to(rotate_transform([1, 0, 0]), RIGHT),
                j_hat_label.animate.next_to(rotate_transform([0, 1, 0]), UP),
                run_time=2
            )
        
        # Frame 5: Key questions
        questions = VGroup(
            Text("• Does it enlarge regions?", color=WHITE).scale(0.6),
            Text("• Does it shrink them?", color=WHITE).scale(0.6),
            Text("• Does it collapse them entirely?", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="Understanding how much area or volume changes gives deep geometric insight into what that matrix is doing.") as tracker:
            self.play(Write(questions))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section2(self):
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
        title = Text("Area Change via Scaling Matrix", color=WHITE)
        subtitle = Text("A Simple Example of Area Transformation", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Let's start with a simple example of a linear transformation that clearly stretches space.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show matrix and initial vectors
        matrix = MathTex(
            "A = \\begin{bmatrix} 3 & 0 \\\\ 0 & 2 \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        # Create initial basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        area_before = MathTex(
            "\\text{Area}_{\\text{before}} = 1 \\times 1 = 1"
        ).next_to(matrix, DOWN)
        
        with self.voiceover(text="Consider this matrix. It scales the unit vector i-hat by 3 in the x-direction, and j-hat by 2 in the y-direction.") as tracker:
            self.play(Create(grid))
            self.play(Write(matrix))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(
                Create(unit_square),
                Write(area_before)
            )
            self.wait(1)
        
        # Frame 3: Apply transformation
        def scale_transform(point):
            x, y, z = point
            return [3*x, 2*y, z]
        
        # Create transformed vectors and square
        transformed_i = Arrow(start=ORIGIN, end=[3, 0, 0], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[0, 2, 0], color=BLUE, buff=0)
        
        transformed_i_label = MathTex("A\\vec{i} = \\begin{bmatrix} 3 \\\\ 0 \\\\ 0 \\end{bmatrix}", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("A\\vec{j} = \\begin{bmatrix} 0 \\\\ 2 \\\\ 0 \\end{bmatrix}", color=BLUE).next_to(transformed_j.get_end(), UP)
        
        transformed_square = Polygon(
            ORIGIN, [3, 0, 0], [3, 2, 0], [0, 2, 0],
            color=YELLOW
        )
        
        area_after = MathTex(
            "\\text{Area}_{\\text{after}} = 3 \\times 2 = 6"
        ).next_to(area_before, DOWN)
        
        with self.voiceover(text="After applying the transformation, the unit square becomes a rectangle with side lengths 3 and 2.") as tracker:
            # Keep original grid faintly visible
            faded_grid = grid.copy()
            self.add(faded_grid)
            
            # Transform the vectors and square
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(i_hat_label, transformed_i_label),
                ReplacementTransform(j_hat_label, transformed_j_label),
                ReplacementTransform(unit_square, transformed_square),
                Write(area_after)
            )
            self.wait(1)
        
        # Frame 4: Show determinant calculation
        det_calc = MathTex(
            "\\det\\begin{bmatrix} 3 & 0 \\\\ 0 & 2 \\end{bmatrix}",
            "&=", "3 \\cdot 2 - 0 \\cdot 0", "\\\\",
            "&=", "6"
        ).next_to(area_after, DOWN)
        
        scaling_factor = MathTex(
            "\\text{Scaling Factor} = \\det(A) = 6"
        ).next_to(det_calc, DOWN)
        
        with self.voiceover(text="The determinant of this matrix is 6, which exactly matches how much the area has increased.") as tracker:
            self.play(Write(det_calc))
            self.play(Write(scaling_factor))
            self.wait(1)
        
        # Frame 5: Show general formula
        general_formula = MathTex(
            "\\text{Area}(AR) = |\\det(A)| \\cdot \\text{Area}(R)"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="This is no coincidence. For any region R, the determinant tells us exactly how much the transformation scales its area.") as tracker:
            self.play(Write(general_formula))
            self.wait(2)
        
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
        
        # Frame 1: Introduction
        title = Text("Shear Transformation and Preserving Area", color=WHITE)
        subtitle = Text("Change Shape, Not Size", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now let's look at a transformation that changes shape, but not area.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show shear matrix and initial vectors
        matrix = MathTex(
            "B = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        # Create initial basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW        )
        
        with self.voiceover(text="Consider this matrix. It defines a shear transformation where i-hat stays in place, but j-hat slides over by one unit in the x-direction.") as tracker:
            self.play(Create(grid))
            self.play(Write(matrix))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(Create(unit_square))
            self.wait(1)
        
        # Frame 3: Apply shear transformation
        def shear_transform(point):
            x, y, z = point
            return [x + y, y, z]
        
        # Create transformed vectors and parallelogram
        transformed_i = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)  # i_hat stays same
        transformed_j = Arrow(start=ORIGIN, end=[1, 1, 0], color=BLUE, buff=0)  # j_hat slides
        
        transformed_i_label = MathTex("B\\vec{i} = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("B\\vec{j} = \\begin{bmatrix} 1 \\\\ 1 \\\\ 0 \\end{bmatrix}", color=BLUE).next_to(transformed_j.get_end(), RIGHT)
        
        transformed_square = Polygon(
            ORIGIN, [1, 0, 0], [2, 1, 0], [1, 1, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="Let's watch how this transformation affects our unit square.") as tracker:
            # Keep original grid faintly visible
            faded_grid = grid.copy()
            self.add(faded_grid)
            
            # Transform the vectors and square
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(i_hat_label, transformed_i_label),
                ReplacementTransform(j_hat_label, transformed_j_label),
                ReplacementTransform(unit_square, transformed_square),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Show base and height measurements
        base_line = Line(ORIGIN, [1, 0, 0], color=GREEN)
        height_line = Line([1, 0, 0], [1, 1, 0], color=GREEN)
        
        base_label = MathTex("\\text{base} = 1", color=GREEN).next_to(base_line, DOWN)
        height_label = MathTex("\\text{height} = 1", color=GREEN).next_to(height_line, RIGHT)
        
        area_calc = MathTex(
            "\\text{Area}_{\\text{after}} = \\text{base} \\times \\text{height} = 1 \\times 1 = 1"
        ).next_to(matrix, DOWN)
        
        with self.voiceover(text="The square becomes a parallelogram. But notice: the base is still 1, and the height — measured perpendicularly — is also still 1.") as tracker:
            self.play(
                Create(base_line),
                Create(height_line),
                Write(base_label),
                Write(height_label)
            )
            self.play(Write(area_calc))
            self.wait(1)
        
        # Frame 5: Show determinant calculation
        det_calc = MathTex(
            "\\det\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}",
            "&=", "(1)(1) - (1)(0)", "\\\\",
            "&=", "1"
        ).next_to(area_calc, DOWN)
        
        with self.voiceover(text="When we calculate the determinant, we get exactly 1, confirming that this transformation preserves area.") as tracker:
            self.play(Write(det_calc))
            self.wait(1)
        
        # Frame 6: Key insights
        insights = VGroup(
            Text("Key Insights:", color=YELLOW).scale(0.7),
            Text("• Transformations can change shape but not area", color=WHITE).scale(0.6),
            Text("• det(B) = 1 means area is preserved", color=WHITE).scale(0.6),
            Text("• Shearing distorts without stretching", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="This shows us something profound: a transformation can dramatically change the shape of a region while keeping its area exactly the same.") as tracker:
            self.play(Write(insights))
            self.wait(2)
        
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
        title = Text("From Unit Square to Any Shape", color=WHITE)
        subtitle = Text("The Power of Uniform Scaling", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now, let's see why understanding how a transformation affects the unit square tells us everything about how it affects any shape.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Create unit square and arbitrary shape
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        # Create a blob-like shape using bezier curves
        blob = VMobject(color=BLUE)
        blob.set_points_smoothly([
            [-1, -1, 0],
            [-0.5, -1.5, 0],
            [0.5, -1.2, 0],
            [1, -0.5, 0],
            [1.2, 0.5, 0],
            [0.5, 1.2, 0],
            [-0.5, 0.8, 0],
            [-1, -1, 0]
        ])
        
        # Create small squares to fill the blob
        small_squares = VGroup()
        square_size = 0.2
        for x in np.arange(-1.2, 1.4, square_size):
            for y in np.arange(-1.5, 1.4, square_size):
                square = Square(
                    side_length=square_size,
                    color=BLUE_E,
                    stroke_width=0.5
                ).move_to([x, y, 0])
                if blob.get_all_points().any():  # Check if point is inside blob
                    small_squares.add(square)
        
        with self.voiceover(text="Consider any region in the plane. We can approximate it by filling it with tiny squares.") as tracker:
            self.play(Create(grid))
            self.play(Create(blob))
            self.play(Create(small_squares))
            self.wait(1)
        
        # Define transformation matrix
        matrix = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 2 \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        def transform(point):
            x, y, z = point
            return [2*x + y, 2*y, z]
        
        with self.voiceover(text="When we apply a linear transformation, each of these tiny squares gets transformed in exactly the same way.") as tracker:
            self.play(Write(matrix))
            self.play(
                blob.animate.apply_function(transform),
                *[square.animate.apply_function(transform) for square in small_squares],
                run_time=2
            )
            self.wait(1)
        
        # Show mathematical formulation
        area_equation = MathTex(
            "\\text{Area}_{\\text{after}} = |\\det(A)| \\cdot \\text{Area}_{\\text{before}}"
        ).next_to(matrix, DOWN)
        
        with self.voiceover(text="The key insight is that the ratio of areas after and before the transformation is the same for every region, and this ratio is exactly the absolute value of the determinant.") as tracker:
            self.play(Write(area_equation))
            self.wait(1)
        
        # Key ideas
        key_ideas = VGroup(
            Text("• Each small square transforms uniformly", color=WHITE).scale(0.5),
            Text("• Area scaling is consistent everywhere", color=WHITE).scale(0.5),
            Text("• Determinant captures this universal scaling", color=WHITE).scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="This is why the determinant is so powerful: it tells us how much any region's area will change under the transformation.") as tracker:
            self.play(Write(key_ideas))
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
        title = Text("What is the Determinant?", color=WHITE)
        subtitle = Text("The Geometric Meaning", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Let's now put a name to this magical number that tells us how areas scale under a linear transformation.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Mathematical Definition
        definition = MathTex(
            "\\text{For any region } R:\\\\",
            "\\text{Area}(T(R)) = |\\det(A)| \\cdot \\text{Area}(R)"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="That number is called the determinant. If a matrix A represents a linear transformation, then the determinant of A tells you how much this transformation scales area by.") as tracker:
            self.play(Create(grid))
            self.play(Write(definition))
            self.wait(1)
        
        # Frame 3: Examples with different matrices
        # Example 1: Scaling
        def scaling_transform(point):
            x, y, z = point
            return [2*x, 3*y, z]
        
        scaling_matrix = MathTex(
            "A_1 = \\begin{bmatrix} 2 & 0 \\\\ 0 & 3 \\end{bmatrix}",
            "\\quad \\det(A_1) = 6"
        ).next_to(definition, DOWN)
        
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="Let's look at some examples. When we scale by 2 in x and 3 in y, the determinant is 6, meaning every area gets multiplied by 6.") as tracker:
            self.play(Write(scaling_matrix))
            self.play(Create(unit_square))
            self.play(
                unit_square.animate.apply_function(scaling_transform),
                run_time=2
            )
            self.wait(1)
        
        # Example 2: Shearing
        def shear_transform(point):
            x, y, z = point
            return [x + y, y, z]
        
        shear_matrix = MathTex(
            "A_2 = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}",
            "\\quad \\det(A_2) = 1"
        ).next_to(scaling_matrix, DOWN)
        
        with self.voiceover(text="A shear transformation changes shape but preserves area, giving us a determinant of 1.") as tracker:
            self.play(Write(shear_matrix))
            self.play(
                unit_square.animate.apply_function(shear_transform),
                run_time=2
            )
            self.wait(1)
        
        # Example 3: Flattening
        def flatten_transform(point):
            x, y, z = point
            return [x, 0, z]
        
        flatten_matrix = MathTex(
            "A_3 = \\begin{bmatrix} 1 & 0 \\\\ 0 & 0 \\end{bmatrix}",
            "\\quad \\det(A_3) = 0"
        ).next_to(shear_matrix, DOWN)
        
        with self.voiceover(text="When a transformation collapses space onto a line or point, the determinant becomes zero, indicating total loss of area.") as tracker:
            self.play(Write(flatten_matrix))
            self.play(
                unit_square.animate.apply_function(flatten_transform),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Key Ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Determinant = Signed Area Scaling Factor", color=WHITE).scale(0.6),
            Text("• Works for ALL shapes, not just squares", color=WHITE).scale(0.6),
            Text("• det(A) = 0 means complete collapse", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="The determinant is not just a number you compute from a matrix. It's a geometric property that tells you how the transformation scales space. Even before you compute it, you can see what it represents!") as tracker:
            self.play(Write(key_ideas))
            self.wait(2)
        
        # Frame 5: Geometric Definition
        geometric_def = MathTex(
            "\\det(A) = \\text{Area of transformed unit square (signed)}"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="In particular, if we just look at what happens to the unit square, its transformed area gives us the determinant.") as tracker:
            self.play(Write(geometric_def))
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
        title = Text("What Does It Mean When the Determinant Is Zero?", color=WHITE)
        subtitle = Text("Understanding Singular Transformations", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Let's talk about a very important case: What does it mean when the determinant equals zero?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show example matrix
        matrix = MathTex(
            "A = \\begin{bmatrix} 1 & 2 \\\\ 2 & 4 \\end{bmatrix}",
            "\\quad \\det(A) = 1 \\cdot 4 - 2 \\cdot 2 = 0"
        ).next_to(title_group, DOWN)
        
        # Create initial basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="Consider this matrix. Notice that its second column is just twice the first column.") as tracker:
            self.play(Create(grid))
            self.play(Write(matrix))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(Create(unit_square))
            self.wait(1)
        
        # Frame 3: Apply transformation
        def collapse_transform(point):
            x, y, z = point
            return [x + 2*y, 2*x + 4*y, z]
        
        # Create transformed vectors
        transformed_i = Arrow(start=ORIGIN, end=[1, 2, 0], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[2, 4, 0], color=BLUE, buff=0)
        
        transformed_i_label = MathTex("A\\vec{i} = \\begin{bmatrix} 1 \\\\ 2 \\\\ 0 \\end{bmatrix}", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("A\\vec{j} = \\begin{bmatrix} 2 \\\\ 4 \\\\ 0 \\end{bmatrix} = 2A\\vec{i}", color=BLUE).next_to(transformed_j.get_end(), RIGHT)
        
        # Create grid points for transformation
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="When we apply this transformation, watch what happens to our basis vectors and the grid.") as tracker:
            # Keep original grid faintly visible
            faded_grid = grid.copy()
            self.add(faded_grid)
            
            # Transform everything
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(i_hat_label, transformed_i_label),
                ReplacementTransform(j_hat_label, transformed_j_label),
                *[dot.animate.move_to(collapse_transform(dot.get_center())) 
                  for dot in grid_points],
                unit_square.animate.apply_function(collapse_transform),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Show linear dependence
        dependence = MathTex(
            "\\text{Second column} = 2 \\times \\text{First column}",
            "\\implies \\text{Linear Dependence}"
        ).next_to(matrix, DOWN)
        
        collapse_line = Line(
            start=[-5, -10, 0],
            end=[5, 10, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="The transformed basis vectors lie on the same line. This means the entire space gets collapsed onto this line.") as tracker:
            self.play(Write(dependence))
            self.play(Create(collapse_line))
            self.wait(1)
        
        # Frame 5: Key implications
        implications = VGroup(
            Text("When det(A) = 0:", color=YELLOW).scale(0.7),
            Text("• Space collapses to lower dimension", color=WHITE).scale(0.6),
            Text("• Transformation is not invertible", color=WHITE).scale(0.6),
            Text("• Columns are linearly dependent", color=WHITE).scale(0.6),
            Text("• All areas become zero", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="A zero determinant means the transformation collapses the entire space into a lower dimension. The transformation loses information and cannot be reversed.") as tracker:
            self.play(Write(implications))
            self.wait(1)
        
        # Frame 6: Mathematical formulation
        math_summary = MathTex(
            "\\det(A) = 0",
            "\\implies",
            "\\begin{cases} \\text{Area}(A(R)) = 0 \\\\ \\text{rank}(A) < 2 \\\\ A \\text{ is not invertible} \\end{cases}"
        ).scale(0.9).to_edge(DOWN)
        
        with self.voiceover(text="This has profound implications: every region's area becomes zero, the matrix rank is less than full, and the transformation cannot be undone.") as tracker:
            self.play(Write(math_summary))
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
        title = Text("Negative Determinants and Orientation Flipping", color=WHITE)
        subtitle = Text("When Space Gets Mirrored", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="So far, we've talked about how the determinant tells us how much a transformation scales area. But there's one more twist: What does it mean when the determinant is negative?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show initial basis vectors and orientation
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i} = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j} = \\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\end{bmatrix}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        # Add curved arrow to show orientation
        orientation_arc = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI/2,
            color=GREEN
        )
        orientation_label = Text("Standard\nOrientation", color=GREEN).scale(0.4).next_to(orientation_arc, RIGHT)
        
        with self.voiceover(text="Let's start with our standard basis vectors. Notice how j-hat is to the left of i-hat when rotating counterclockwise. This defines our standard orientation.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(Create(unit_square))
            self.play(Create(orientation_arc), Write(orientation_label))
            self.wait(1)
        
        # Frame 3: Show example matrix and transformation
        matrix = MathTex(
            "A = \\begin{bmatrix} 1 & 1 \\\\ 2 & -1 \\end{bmatrix}",
            "\\quad \\det(A) = (1)(-1) - (1)(2) = -3"
        ).next_to(title_group, DOWN)
        
        def flip_transform(point):
            x, y, z = point
            return [x + y, 2*x - y, z]
        
        # Create transformed vectors
        transformed_i = Arrow(start=ORIGIN, end=[1, 2, 0], color=RED, buff=0)
        transformed_j = Arrow(start=ORIGIN, end=[1, -1, 0], color=BLUE, buff=0)
        
        transformed_i_label = MathTex("A\\vec{i} = \\begin{bmatrix} 1 \\\\ 2 \\\\ 0 \\end{bmatrix}", color=RED).next_to(transformed_i.get_end(), RIGHT)
        transformed_j_label = MathTex("A\\vec{j} = \\begin{bmatrix} 1 \\\\ -1 \\\\ 0 \\end{bmatrix}", color=BLUE).next_to(transformed_j.get_end(), RIGHT)
        
        # Create grid points for transformation
        grid_points = VGroup()
        for x in np.linspace(-4, 4, 17):
            for y in np.linspace(-4, 4, 17):
                point = Dot(point=[x, y, 0], color=BLUE_A, radius=0.05)
                grid_points.add(point)
        
        with self.voiceover(text="Consider this transformation. Watch what happens to our basis vectors and how the orientation changes.") as tracker:
            self.play(Write(matrix))
            
            # Keep original grid faintly visible
            faded_grid = grid.copy()
            self.add(faded_grid)
            
            # Transform everything
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(i_hat_label, transformed_i_label),
                ReplacementTransform(j_hat_label, transformed_j_label),
                *[dot.animate.move_to(flip_transform(dot.get_center())) 
                  for dot in grid_points],
                unit_square.animate.apply_function(flip_transform),
                FadeOut(orientation_arc),
                FadeOut(orientation_label),
                run_time=2
            )
            self.wait(1)
        
        # Show new orientation
        flipped_arc = Arc(
            radius=0.5,
            start_angle=np.arctan2(2, 1),  # Angle of transformed i
            angle=-np.arctan2(3, 2),  # Angle between transformed vectors
            color=RED
        )
        flipped_label = Text("Flipped\nOrientation", color=RED).scale(0.4).next_to(flipped_arc, RIGHT)
        
        with self.voiceover(text="Notice how j-hat now ends up to the right of i-hat. The space has been flipped, like turning over a sheet of paper.") as tracker:
            self.play(Create(flipped_arc), Write(flipped_label))
            self.wait(1)
        
        # Frame 4: Show area scaling and orientation
        area_explanation = VGroup(
            MathTex("|\\det(A)| = 3", "\\quad \\text{(Area scale factor)}"),
            MathTex("\\text{sign}(\\det(A)) < 0", "\\quad \\text{(Orientation flip)}")
        ).arrange(DOWN).next_to(matrix, DOWN)
        
        with self.voiceover(text="The absolute value of the determinant, 3, tells us how much area is scaled. The negative sign tells us that the orientation has been flipped.") as tracker:
            self.play(Write(area_explanation))
            self.wait(1)
        
        # Frame 5: Key ideas
        key_ideas = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• |det(A)| = area scaling", color=WHITE).scale(0.6),
            Text("• sign(det(A)) = orientation", color=WHITE).scale(0.6),
            Text("• Negative = space flipped", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="The determinant carries two pieces of information: its magnitude tells us about area scaling, while its sign tells us about orientation.") as tracker:
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
        title = Text("From Positive to Negative Determinants", color=WHITE)
        subtitle = Text("A Continuous Journey Through Zero", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Here's a fascinating way to think about why a negative determinant makes sense: Imagine gradually moving i-hat closer and closer to j-hat.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Create initial basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create parallelogram
        parallelogram = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        # Add angle label
        angle_arc = Arc(
            radius=0.3,
            start_angle=0,
            angle=PI/2,
            color=GREEN
        )
        angle_label = MathTex("\\theta = 90°", color=GREEN).scale(0.6).next_to(angle_arc, RIGHT)
        
        # Add determinant value tracker
        det_value = DecimalNumber(
            1.0,
            show_ellipsis=True,
            num_decimal_places=2,
            include_sign=True,
        ).to_edge(RIGHT)
        det_label = Text("det(A) = ", color=WHITE).scale(0.8).next_to(det_value, LEFT)
        
        with self.voiceover(text="Let's start with our standard basis vectors at right angles. The determinant is positive one.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label)
            )
            self.play(
                Create(parallelogram),
                Create(angle_arc),
                Write(angle_label),
                Write(det_label),
                Write(det_value)
            )
            self.wait(1)
        
        # Function to update the scene as angle changes
        def update_scene(angle):
            # Update i_hat position
            new_i = [np.cos(angle), np.sin(angle), 0]
            i_hat.put_start_and_end_on(ORIGIN, new_i)
            i_hat_label.next_to(i_hat.get_end(), RIGHT)
            
            # Update parallelogram
            new_parallelogram = Polygon(
                ORIGIN, new_i, 
                [new_i[0] + j_hat.get_end()[0], new_i[1] + j_hat.get_end()[1], 0],
                j_hat.get_end(),
                color=YELLOW
            )
            
            # Update angle arc and label
            new_angle_arc = Arc(
                radius=0.3,
                start_angle=0,
                angle=angle if angle > 0 else angle + 2*PI,
                color=GREEN if angle > 0 else RED
            )
            new_angle_label = MathTex(f"\\theta = {int(angle*180/PI)}°", 
                                     color=GREEN if angle > 0 else RED).scale(0.6).next_to(new_angle_arc, RIGHT)
            
            # Calculate and update determinant
            det = np.sin(angle)  # Determinant is sin(θ) for unit vectors
            det_value.set_value(det)
            det_value.set_color(GREEN if det > 0 else RED if det < 0 else WHITE)
            
            return new_parallelogram, new_angle_arc, new_angle_label
        
        # Animate the transition
        angles = [PI/2 - i*PI/12 for i in range(13)]  # From 90° to -60°
        
        with self.voiceover(text="Watch what happens as we rotate i-hat closer to j-hat. The parallelogram gets thinner, and the determinant approaches zero.") as tracker:
            for angle in angles[:7]:  # First half: approach alignment
                new_para, new_arc, new_label = update_scene(angle)
                self.play(
                    Transform(parallelogram, new_para),
                    Transform(angle_arc, new_arc),
                    Transform(angle_label, new_label),
                    run_time=0.5
                )
        
        with self.voiceover(text="When the vectors align, the parallelogram collapses to a line, and the determinant becomes zero.") as tracker:
            new_para, new_arc, new_label = update_scene(0)
            self.play(
                Transform(parallelogram, new_para),
                Transform(angle_arc, new_arc),
                Transform(angle_label, new_label),
                run_time=1
            )
            self.wait(1)
        
        with self.voiceover(text="As i-hat continues past j-hat, the orientation flips, and the determinant becomes negative.") as tracker:
            for angle in angles[7:]:  # Second half: cross over
                new_para, new_arc, new_label = update_scene(angle)
                self.play(
                    Transform(parallelogram, new_para),
                    Transform(angle_arc, new_arc),
                    Transform(angle_label, new_label),
                    run_time=0.5
                )
        
        # Add key insights
        insights = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Determinant varies continuously", color=WHITE).scale(0.6),
            Text("• Zero marks the transition point", color=WHITE).scale(0.6),
            Text("• Sign change reflects orientation flip", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="The determinant varies continuously as vectors rotate. A negative determinant is the natural result of passing through zero, preserving both area scaling and orientation information.") as tracker:
            self.play(Write(insights))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section9(self):
        # Create 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Frame 1: Introduction
        title = Text("Determinants in Three Dimensions", color=WHITE)
        subtitle = Text("Scaling Volume", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Everything we've said about determinants in two dimensions — area scaling and orientation — has a beautiful analog in three dimensions.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show initial unit cube and basis vectors
        # Create basis vectors
        i_hat = Arrow3D(
            start=ORIGIN,
            end=[1, 0, 0],
            color=RED
        )
        j_hat = Arrow3D(
            start=ORIGIN,
            end=[0, 1, 0],
            color=GREEN
        )
        k_hat = Arrow3D(
            start=ORIGIN,
            end=[0, 0, 1],
            color=BLUE
        )
        
        # Create labels for basis vectors
        i_label = MathTex("\\vec{i}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_label = MathTex("\\vec{j}", color=GREEN).next_to(j_hat.get_end(), UP)
        k_label = MathTex("\\vec{k}", color=BLUE).next_to(k_hat.get_end(), OUT)
        
        # Create unit cube
        unit_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        )
        
        with self.voiceover(text="In 3D, the determinant tells you how much a linear transformation scales volumes. Let's start with our unit cube, spanned by our standard basis vectors.") as tracker:
            self.play(Create(axes))
            self.play(
                Create(i_hat), Create(j_hat), Create(k_hat),
                Write(i_label), Write(j_label), Write(k_label)
            )
            self.play(Create(unit_cube))
            self.wait(1)
        
        # Frame 3: Show mathematical setup
        math_setup = MathTex(
            "\\text{Volume}(T(R)) = |\\det(A)| \\times \\text{Volume}(R)"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Just like in two dimensions, the determinant tells us exactly how volumes scale under the transformation.") as tracker:
            self.play(Write(math_setup))
            self.wait(1)
        
        # Frame 4: Example transformation
        # Define transformation matrix
        matrix = MathTex(
            "A = \\begin{bmatrix} 2 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}"
        ).next_to(math_setup, DOWN)
        
        def transform_3d(point):
            x, y, z = point
            return [2*x, y, z]
        
        # Create transformed vectors and cube
        transformed_i = Arrow3D(start=ORIGIN, end=[2, 0, 0], color=RED)
        transformed_j = Arrow3D(start=ORIGIN, end=[0, 1, 0], color=GREEN)
        transformed_k = Arrow3D(start=ORIGIN, end=[0, 0, 1], color=BLUE)
        
        transformed_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        ).apply_matrix([[2, 0, 0], [0, 1, 0], [0, 0, 1]])
        
        with self.voiceover(text="Let's look at an example. This matrix stretches space by a factor of 2 along the x-axis, turning our cube into a parallelepiped.") as tracker:
            self.play(Write(matrix))
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(k_hat, transformed_k),
                ReplacementTransform(unit_cube, transformed_cube),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Show volume calculation
        volume_calc = MathTex(
            "\\det(A) = 2 \\times 1 \\times 1 = 2",
            "\\quad \\text{Volume doubled!}"
        ).next_to(matrix, DOWN)
        
        with self.voiceover(text="The determinant is 2, which means all volumes are doubled by this transformation.") as tracker:
            self.play(Write(volume_calc))
            self.wait(1)
        
        # Frame 6: Key insights
        insights = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• |det(A)| = volume scaling factor", color=WHITE).scale(0.6),
            Text("• Cube becomes parallelepiped", color=WHITE).scale(0.6),
            Text("• Same principles as 2D, but with volume", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="The key insight is that determinants work the same way in three dimensions: the magnitude tells us about volume scaling, while the sign tells us about orientation.") as tracker:
            self.play(Write(insights))
            self.wait(2)
        
        # Frame 7: Show parallelepiped definition
        parallelepiped_def = VGroup(
            Text("Parallelepiped:", color=YELLOW).scale(0.7),
            Text("• 3D analog of parallelogram", color=WHITE).scale(0.6),
            Text("• Six parallelogram faces", color=WHITE).scale(0.6),
            Text("• Parallel edges remain parallel", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="A parallelepiped is the three-dimensional analog of a parallelogram. It has six faces, each a parallelogram, and its edges remain parallel under transformation.") as tracker:
            self.play(Write(parallelepiped_def))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section10(self):
        # Create 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Frame 1: Introduction
        title = Text("Zero Determinant in Three Dimensions", color=WHITE)
        subtitle = Text("Collapse of Volume", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Let's now ask: What does it mean when a 3D transformation has determinant zero?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show initial unit cube and basis vectors
        # Create basis vectors
        i_hat = Arrow3D(
            start=ORIGIN,
            end=[1, 0, 0],
            color=RED
        )
        j_hat = Arrow3D(
            start=ORIGIN,
            end=[0, 1, 0],
            color=GREEN
        )
        k_hat = Arrow3D(
            start=ORIGIN,
            end=[0, 0, 1],
            color=BLUE
        )
        
        # Create labels for basis vectors
        i_label = MathTex("\\vec{v}_1", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_label = MathTex("\\vec{v}_2", color=GREEN).next_to(j_hat.get_end(), UP)
        k_label = MathTex("\\vec{v}_3", color=BLUE).next_to(k_hat.get_end(), OUT)
        
        # Create unit cube
        unit_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        )
        
        with self.voiceover(text="Just like in two dimensions, it means the transformation collapses the entire 3D space into a lower-dimensional object. No more volume.") as tracker:
            self.play(Create(axes))
            self.play(
                Create(i_hat), Create(j_hat), Create(k_hat),
                Write(i_label), Write(j_label), Write(k_label)
            )
            self.play(Create(unit_cube))
            self.wait(1)
        
        # Frame 3: Show example matrix
        matrix = MathTex(
            "A = \\begin{bmatrix} 1 & 2 & 3 \\\\ 2 & 4 & 6 \\\\ 0 & 0 & 0 \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        dependence = MathTex(
            "\\vec{v}_2 = 2\\vec{v}_1, \\quad \\vec{v}_3 = 3\\vec{v}_1"
        ).next_to(matrix, DOWN)
        
        with self.voiceover(text="Consider this matrix. Notice that the second column is twice the first, and the third column is three times the first. The columns are linearly dependent.") as tracker:
            self.play(Write(matrix))
            self.play(Write(dependence))
            self.wait(1)
        
        # Frame 4: Show transformation
        def collapse_transform(point):
            x, y, z = point
            return [x + 2*y + 3*z, 2*x + 4*y + 6*z, 0]
        
        # Create transformed vectors
        transformed_i = Arrow3D(start=ORIGIN, end=[1, 2, 0], color=RED)
        transformed_j = Arrow3D(start=ORIGIN, end=[2, 4, 0], color=GREEN)
        transformed_k = Arrow3D(start=ORIGIN, end=[3, 6, 0], color=BLUE)
        
        # Create grid points for transformation
        grid_points = VGroup()
        for x in np.linspace(-2, 2, 9):
            for y in np.linspace(-2, 2, 9):
                for z in np.linspace(-2, 2, 9):
                    point = Dot3D(point=[x, y, z], color=BLUE_A, radius=0.05)
                    grid_points.add(point)
        
        with self.voiceover(text="Watch what happens when we apply this transformation. The entire space collapses onto a plane.") as tracker:
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(k_hat, transformed_k),
                *[dot.animate.move_to(collapse_transform(dot.get_center())) 
                  for dot in grid_points],
                unit_cube.animate.apply_function(collapse_transform),
                run_time=3
            )
            self.wait(1)
        
        # Frame 5: Show determinant calculation
        det_calc = MathTex(
            "\\det(A) = 0",
            "\\implies",
            "\\text{Volume} = 0"
        ).next_to(dependence, DOWN)
        
        with self.voiceover(text="The determinant is zero, which means all volumes are collapsed to zero.") as tracker:
            self.play(Write(det_calc))
            self.wait(1)
        
        # Frame 6: Key implications
        implications = VGroup(
            Text("When det(A) = 0 in 3D:", color=YELLOW).scale(0.7),
            Text("• Space collapses to plane, line, or point", color=WHITE).scale(0.6),
            Text("• Columns are linearly dependent", color=WHITE).scale(0.6),
            Text("• Transformation is not invertible", color=WHITE).scale(0.6),
            Text("• All volumes become zero", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="A zero determinant in three dimensions means the transformation loses at least one dimension. The transformation cannot be undone, and all volumes become zero.") as tracker:
            self.play(Write(implications))
            self.wait(2)
        
        # Frame 7: Mathematical summary
        math_summary = MathTex(
            "\\det(A) = 0",
            "\\implies",
            "\\begin{cases} \\text{Volume}(T(R)) = 0 \\\\ \\text{rank}(A) < 3 \\\\ \\text{Image is } \\leq \\text{2D} \\end{cases}"
        ).scale(0.9).to_edge(DOWN)
        
        with self.voiceover(text="This has profound implications: every region's volume becomes zero, the matrix rank is less than full, and the image is confined to a lower-dimensional space.") as tracker:
            self.play(Write(math_summary))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section11(self):
        # Create 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Frame 1: Introduction
        title = Text("Orientation in 3D", color=WHITE)
        subtitle = Text("The Right-Hand Rule and Determinants", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="In three dimensions, orientation becomes even more interesting. We use something called the Right-Hand Rule to understand it.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show standard basis and right-hand rule
        # Create basis vectors
        i_hat = Arrow3D(
            start=ORIGIN,
            end=[1, 0, 0],
            color=RED
        )
        j_hat = Arrow3D(
            start=ORIGIN,
            end=[0, 1, 0],
            color=GREEN
        )
        k_hat = Arrow3D(
            start=ORIGIN,
            end=[0, 0, 1],
            color=BLUE
        )
        
        # Create labels for basis vectors
        i_label = MathTex("\\vec{i}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_label = MathTex("\\vec{j}", color=GREEN).next_to(j_hat.get_end(), UP)
        k_label = MathTex("\\vec{k}", color=BLUE).next_to(k_hat.get_end(), OUT)
        
        # Create unit cube
        unit_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        )
        
        # Create right-hand rule visualization
        right_hand_rule = Text(
            "Right-Hand Rule:\nIndex → i\nMiddle → j\nThumb → k",
            color=YELLOW
        ).scale(0.6).to_edge(RIGHT)
        
        with self.voiceover(text="Here's how the right-hand rule works: Point your index finger along i-hat, your middle finger along j-hat, and your thumb will naturally point along k-hat. This defines the positive orientation of space.") as tracker:
            self.play(Create(axes))
            self.play(
                Create(i_hat), Create(j_hat), Create(k_hat),
                Write(i_label), Write(j_label), Write(k_label)
            )
            self.play(Create(unit_cube))
            self.play(Write(right_hand_rule))
            self.wait(1)
        
        # Frame 3: Show example of orientation-preserving transformation
        matrix_A = MathTex(
            "A = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}",
            "\\quad \\det(A) = 1"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Let's start with the identity transformation. It preserves orientation, and its determinant is positive one.") as tracker:
            self.play(Write(matrix_A))
            self.wait(1)
        
        # Frame 4: Show example of orientation-flipping transformation
        matrix_B = MathTex(
            "B = \\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & -1 & 0 \\\\ 0 & 0 & 1 \\end{bmatrix}",
            "\\quad \\det(B) = -1"
        ).next_to(matrix_A, DOWN)
        
        def flip_transform(point):
            x, y, z = point
            return [x, -y, z]
        
        # Create transformed vectors
        transformed_i = Arrow3D(start=ORIGIN, end=[1, 0, 0], color=RED)
        transformed_j = Arrow3D(start=ORIGIN, end=[0, -1, 0], color=GREEN)
        transformed_k = Arrow3D(start=ORIGIN, end=[0, 0, 1], color=BLUE)
        
        transformed_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        ).apply_matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        
        with self.voiceover(text="Now, let's apply a reflection across the x-z plane. Watch how this flips the orientation, making the right-hand rule impossible to satisfy.") as tracker:
            self.play(Write(matrix_B))
            self.play(
                ReplacementTransform(i_hat, transformed_i),
                ReplacementTransform(j_hat, transformed_j),
                ReplacementTransform(k_hat, transformed_k),
                ReplacementTransform(unit_cube, transformed_cube),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Show orientation implications
        orientation_rules = VGroup(
            Text("Orientation Rules:", color=YELLOW).scale(0.7),
            Text("• Right-hand rule works → det(A) > 0", color=WHITE).scale(0.6),
            Text("• Must use left hand → det(A) < 0", color=WHITE).scale(0.6),
            Text("• Space collapses → det(A) = 0", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="The sign of the determinant tells us whether the transformation preserves or flips the orientation of space.") as tracker:
            self.play(Write(orientation_rules))
            self.wait(1)
        
        # Frame 6: Show mathematical summary
        math_summary = MathTex(
            "\\text{det}(A) > 0", "&\\iff \\text{ Orientation preserved}\\\\",
            "\\text{det}(A) < 0", "&\\iff \\text{ Orientation flipped}"
        ).next_to(orientation_rules, DOWN)
        
        with self.voiceover(text="A positive determinant means the right-hand rule still works after transformation. A negative determinant means we need to switch to our left hand.") as tracker:
            self.play(Write(math_summary))
            self.wait(2)
        
        # Frame 7: Key insights
        insights = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• Right-hand rule defines orientation", color=WHITE).scale(0.6),
            Text("• Determinant sign indicates preservation", color=WHITE).scale(0.6),
            Text("• Reflections flip orientation", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="The right-hand rule gives us a physical way to check orientation, while the determinant's sign provides the mathematical confirmation.") as tracker:
            self.play(Write(insights))
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
        title = Text("Computing the Determinant of a 2×2 Matrix", color=WHITE)
        subtitle = Text("The Geometric Meaning Behind the Formula", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now that we understand what the determinant means, let's see how to actually compute it. We'll start with the simplest case: a two-by-two matrix.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show the formula
        matrix = MathTex(
            "A = \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        formula = MathTex(
            "\\det(A) = ad - bc"
        ).next_to(matrix, DOWN)
        
        with self.voiceover(text="For a matrix A with entries a, b, c, and d, the determinant is given by this formula: a d minus b c. But where does this formula come from?") as tracker:
            self.play(Create(grid))
            self.play(Write(matrix))
            self.play(Write(formula))
            self.wait(1)
        
        # Frame 3: Show initial basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        
        i_hat_label = MathTex("\\vec{i} = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}", color=RED).next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\vec{j} = \\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\end{bmatrix}", color=BLUE).next_to(j_hat.get_end(), UP)
        
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        with self.voiceover(text="Let's build some geometric intuition. Start with our unit square and standard basis vectors.") as tracker:
            self.play(
                Create(i_hat), Create(j_hat),
                Write(i_hat_label), Write(j_hat_label),
                Create(unit_square)
            )
            self.wait(1)
        
        # Frame 4: Show transformation - diagonal case first
        def diagonal_transform(point):
            x, y, z = point
            return [2*x, 1.5*y, z]  # Example values a=2, d=1.5
        
        diagonal_matrix = MathTex(
            "A_1 = \\begin{bmatrix} 2 & 0 \\\\ 0 & 1.5 \\end{bmatrix}",
            "\\quad \\det(A_1) = 2 \\cdot 1.5 = 3"
        ).next_to(formula, DOWN)
        
        with self.voiceover(text="Let's start with the simplest case: a diagonal matrix. Here, b and c are zero, and the determinant is just the product of a and d.") as tracker:
            self.play(Write(diagonal_matrix))
            self.play(
                unit_square.animate.apply_function(diagonal_transform),
                i_hat.animate.put_start_and_end_on(ORIGIN, [2, 0, 0]),
                j_hat.animate.put_start_and_end_on(ORIGIN, [0, 1.5, 0]),
                i_hat_label.animate.next_to([2, 0, 0], RIGHT),
                j_hat_label.animate.next_to([0, 1.5, 0], UP),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Show transformation - shear case
        def shear_transform(point):
            x, y, z = point
            return [2*x + y, 1.5*y, z]  # Example values a=2, b=1, c=0, d=1.5
        
        shear_matrix = MathTex(
            "A_2 = \\begin{bmatrix} 2 & 1 \\\\ 0 & 1.5 \\end{bmatrix}",
            "\\quad \\det(A_2) = 2 \\cdot 1.5 - 1 \\cdot 0 = 3"
        ).next_to(diagonal_matrix, DOWN)
        
        with self.voiceover(text="Now let's add some shear by making b non-zero. The parallelogram gets slanted, but notice how the determinant formula accounts for this.") as tracker:
            self.play(Write(shear_matrix))
            self.play(
                unit_square.animate.apply_function(shear_transform),
                i_hat.animate.put_start_and_end_on(ORIGIN, [2, 0, 0]),
                j_hat.animate.put_start_and_end_on(ORIGIN, [1, 1.5, 0]),
                i_hat_label.animate.next_to([2, 0, 0], RIGHT),
                j_hat_label.animate.next_to([1, 1.5, 0], RIGHT),
                run_time=2
            )
            self.wait(1)
        
        # Frame 6: Show general case
        def general_transform(point):
            x, y, z = point
            return [2*x + y, x + 1.5*y, z]  # Example values a=2, b=1, c=1, d=1.5
        
        general_matrix = MathTex(
            "A_3 = \\begin{bmatrix} 2 & 1 \\\\ 1 & 1.5 \\end{bmatrix}",
            "\\quad \\det(A_3) = 2 \\cdot 1.5 - 1 \\cdot 1 = 2"
        ).next_to(shear_matrix, DOWN)
        
        with self.voiceover(text="Finally, in the general case where all entries are non-zero, the determinant formula captures both the stretching and the skewing of space.") as tracker:
            self.play(Write(general_matrix))
            self.play(
                unit_square.animate.apply_function(general_transform),
                i_hat.animate.put_start_and_end_on(ORIGIN, [2, 1, 0]),
                j_hat.animate.put_start_and_end_on(ORIGIN, [1, 1.5, 0]),
                i_hat_label.animate.next_to([2, 1, 0], RIGHT),
                j_hat_label.animate.next_to([1, 1.5, 0], RIGHT),
                run_time=2
            )
            self.wait(1)
        
        # Frame 7: Show area calculation
        area_calc = VGroup(
            Text("Area Calculation:", color=YELLOW).scale(0.7),
            MathTex("\\text{Area} = |\\det(A)| = |ad - bc|"),
            Text("• ad: basic rectangle area", color=WHITE).scale(0.6),
            Text("• bc: correction for skewing", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="The determinant formula ad minus bc gives us the area of the transformed unit square. The ad term represents basic stretching, while bc corrects for the skewing effect.") as tracker:
            self.play(Write(area_calc))
            self.wait(1)
        
        # Frame 8: Key insights
        insights = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• det(A) = ad - bc comes from area", color=WHITE).scale(0.6),
            Text("• Formula captures stretching and skewing", color=WHITE).scale(0.6),
            Text("• No memorization needed with geometry!", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="The key insight is that the determinant formula naturally arises from calculating the area of the transformed unit square. Understanding this geometric picture makes the formula intuitive!") as tracker:
            self.play(Write(insights))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section13(self):
        # Create 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Frame 1: Introduction
        title = Text("Determinants for Larger Matrices", color=WHITE)
        subtitle = Text("Focus on Meaning, Not Just Formulas", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Now, what about larger matrices, like three-by-three or even bigger? Yes, there are formulas you can memorize, but honestly — and this is important: Understanding what the determinant means is far more important than memorizing how to compute it.") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show 3×3 matrix
        matrix = MathTex(
            "A = \\begin{bmatrix} a & b & c \\\\ d & e & f \\\\ g & h & i \\end{bmatrix}"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="Still, let's quickly sketch what computation looks like for a three-by-three matrix.") as tracker:
            self.play(Create(axes))
            self.play(Write(matrix))
            self.wait(1)
        
        # Frame 3: Show determinant formula
        det_formula = MathTex(
            "\\det(A) = &a(ei-fh) \\\\",
            "&-b(di-fg) \\\\",
            "&+c(dh-eg)"
        ).next_to(matrix, DOWN)
        
        # Create highlighting rectangles for each term
        first_minor = SurroundingRectangle(matrix[0][5:9], color=RED)  # Highlight ei-fh block
        second_minor = SurroundingRectangle(matrix[0][4:8], color=BLUE)  # Highlight di-fg block
        third_minor = SurroundingRectangle(matrix[0][3:7], color=GREEN)  # Highlight dh-eg block
        
        with self.voiceover(text="The determinant is computed by taking each element in the first row, multiplying it by the determinant of its corresponding two-by-two minor, and alternating signs.") as tracker:
            self.play(Write(det_formula))
            self.play(
                Create(first_minor),
                Create(second_minor),
                Create(third_minor),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Show geometric meaning
        # Create unit cube
        unit_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        )
        
        # Define a transformation matrix
        transform_matrix = [[2, 0.5, 0.3], [0.5, 1.5, 0.2], [0.3, 0.2, 1.8]]
        
        # Create transformed cube
        transformed_cube = Cube(
            side_length=1,
            stroke_width=2,
            stroke_color=WHITE
        ).apply_matrix(transform_matrix)
        
        geometric_meaning = VGroup(
            Text("Geometric Meaning:", color=YELLOW).scale(0.7),
            Text("• Volume Scaling = |det(A)|", color=WHITE).scale(0.6),
            Text("• Orientation Flip = sign(det(A))", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="But the beauty isn't in the formula — it's in what the determinant means geometrically: how volumes are scaled and how orientation behaves in three dimensions.") as tracker:
            self.play(Create(unit_cube))
            self.play(
                ReplacementTransform(unit_cube, transformed_cube),
                Write(geometric_meaning),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Show warning about formulas
        warning = VGroup(
            Text("⚠️ Important Note:", color=RED).scale(0.7),
            Text("Don't get lost in the algebra —", color=WHITE).scale(0.6),
            Text("focus on the geometric meaning!", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="Here's the key takeaway: Don't get lost in the algebra. The formulas are just tools to compute what really matters: the geometric transformation of space.") as tracker:
            self.play(Write(warning))
            self.wait(1)
        
        # Frame 6: Show conceptual summary
        summary = VGroup(
            Text("Key Ideas:", color=YELLOW).scale(0.7),
            Text("• 3×3 det: messy computation, beautiful meaning", color=WHITE).scale(0.6),
            Text("• Measures volume scaling and orientation", color=WHITE).scale(0.6),
            Text("• Visual understanding > Formula memorization", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(warning, DOWN, buff=1)
        
        with self.voiceover(text="Remember: three-by-three determinants might have messy computations, but their meaning is beautiful. They tell us exactly how volumes scale and how orientation changes in three-dimensional space.") as tracker:
            self.play(Write(summary))
            self.wait(1)
        
        # Frame 7: Show practical advice
        advice = MathTex(
            "\\text{Intuition} > \\text{Memorization}",
            "\\quad \\text{in Linear Algebra}"
        ).scale(1.2).to_edge(DOWN)
        
        with self.voiceover(text="In linear algebra, building intuition is far more valuable than memorizing formulas. Let the geometry guide your understanding.") as tracker:
            self.play(Write(advice))
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
        title = Text("The Determinant of a Product and Looking Ahead", color=WHITE)
        subtitle = Text("A Beautiful Multiplicative Property", color=YELLOW).scale(0.6)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        with self.voiceover(text="Before we wrap up, here's a fun question to think about: If you multiply two matrices together, what happens to their determinants?") as tracker:
            self.play(Write(title_group))
            self.wait(0.5)
        
        # Move title to top
        self.play(
            title_group.animate.scale(0.8).to_edge(UP)
        )
        
        # Frame 2: Show the formula
        formula = MathTex(
            "\\det(AB) = \\det(A) \\times \\det(B)"
        ).next_to(title_group, DOWN)
        
        with self.voiceover(text="The answer is beautifully simple: The determinant of the product equals the product of the determinants.") as tracker:
            self.play(Create(grid))
            self.play(Write(formula))
            self.wait(1)
        
        # Frame 3: Demonstrate with transformations
        # Create unit square
        unit_square = Polygon(
            ORIGIN, [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=YELLOW
        )
        
        # Define first transformation (matrix A)
        def transform_A(point):
            x, y, z = point
            return [2*x, 1.5*y, z]  # det(A) = 3
        
        # Define second transformation (matrix B)
        def transform_B(point):
            x, y, z = point
            return [x + y, 2*y, z]  # det(B) = 2
        
        matrix_A = MathTex(
            "A = \\begin{bmatrix} 2 & 0 \\\\ 0 & 1.5 \\end{bmatrix}",
            "\\quad \\det(A) = 3"
        ).next_to(formula, DOWN)
        
        matrix_B = MathTex(
            "B = \\begin{bmatrix} 1 & 1 \\\\ 0 & 2 \\end{bmatrix}",
            "\\quad \\det(B) = 2"
        ).next_to(matrix_A, DOWN)
        
        with self.voiceover(text="Let's see this visually. First, matrix A scales space by a factor of 3.") as tracker:
            self.play(Write(matrix_A))
            self.play(Create(unit_square))
            self.play(
                unit_square.animate.apply_function(transform_A),
                run_time=2
            )
            self.wait(1)
        
        with self.voiceover(text="Then matrix B further transforms the space, scaling areas by a factor of 2.") as tracker:
            self.play(Write(matrix_B))
            self.play(
                unit_square.animate.apply_function(transform_B),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Show the compounding effect
        result = MathTex(
            "\\det(AB) = 3 \\times 2 = 6",
            "\\quad \\text{(Total area scaling)}"
        ).next_to(matrix_B, DOWN)
        
        with self.voiceover(text="The total effect compounds: the final area is six times the original, which is exactly the product of the individual scaling factors.") as tracker:
            self.play(Write(result))
            self.wait(1)
        
        # Frame 5: Quick recap montage
        recap_title = Text("What We've Learned About Determinants:", color=YELLOW).scale(0.7)
        recap_points = VGroup(
            Text("• Measure scaling of area/volume", color=WHITE).scale(0.6),
            Text("• Capture orientation flips", color=WHITE).scale(0.6),
            Text("• Zero means dimensional collapse", color=WHITE).scale(0.6),
            Text("• Multiply under composition", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        recap_group = VGroup(recap_title, recap_points).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        with self.voiceover(text="Over these scenes, we've discovered that determinants measure how space is transformed. They tell us about scaling, orientation, dimensional collapse, and how transformations combine.") as tracker:
            self.play(Write(recap_group))
            self.wait(1)
        
        # Frame 6: Looking ahead
        future_applications = VGroup(
            Text("Looking Ahead:", color=YELLOW).scale(0.7),
            Text("• Solving systems of equations", color=WHITE).scale(0.6),
            Text("• Finding eigenvalues", color=WHITE).scale(0.6),
            Text("• Change of variables in calculus", color=WHITE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="These ideas will be crucial for solving systems of equations, finding eigenvalues, and even in multivariable calculus.") as tracker:
            self.play(Write(future_applications))
            self.wait(1)
        
        # Frame 7: Final message
        final_message = VGroup(
            Text("The Determinant:", color=YELLOW).scale(0.8),
            Text("One number that captures", color=WHITE).scale(0.6),
            Text("the essence of a linear transformation", color=WHITE).scale(0.6)
        ).arrange(DOWN).to_edge(DOWN)
        
        with self.voiceover(text="The determinant isn't just about calculating numbers from matrices. It's about seeing how linear transformations reshape space, and how these changes interact when transformations combine. It's about space, stretching, folding, flipping, collapsing — all encoded in a single number.") as tracker:
            self.play(Write(final_message))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

if __name__ == "__main__":
    scene = Determinants()
    scene.render() 