from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class TransformationMatrices(VoiceoverScene,ThreeDScene):
    def construct(self):
        # Configure voiceover service
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        
        # Run sections
        self.section1()  # Basis vectors and coordinates
        self.clear()
        self.section2()  # Concept of Basis
        self.clear()
        self.section3()  # Changing basis vectors
        self.clear()
        self.section4()  # Linear Combinations and Span
        self.clear()
        self.section5()  # What "Linear" Means
        self.clear()
        self.section6()  # Thinking in Terms of Points
        self.clear()
        self.section7()  # Span in 3D Space
        self.clear()
        self.section8()  # Adding a Third Vector and Linear Independence
        self.clear()
        self.section9()  # Linear Dependence and Independence
        self.clear()
        self.section10()  # Definition of a Basis
        self.clear()

    def section1(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Empty plane with i-hat
        with self.voiceover(text="When we describe a vector like (3, -2), we often think of it as just a pair of numbers. But there's a deeper way to understand these numbers: Each number scales a special vector in a coordinate system.") as tracker:
            self.play(Create(grid))
            self.wait(1)
        
        # Create and show i-hat
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        i_hat_label = MathTex("\\hat{\\imath} = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix}").next_to(i_hat.get_end(), RIGHT)
        
        with self.voiceover(text="In two dimensions, there are two especially important vectors. First, the unit vector along the x-axis, called i-hat.") as tracker:
            self.play(Create(i_hat))
            self.play(Write(i_hat_label))
            self.wait(1)
        
        # Frame 2: Add j-hat
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=GREEN, buff=0)
        j_hat_label = MathTex("\\hat{\\jmath} = \\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix}").next_to(j_hat.get_end(), UP)
        
        with self.voiceover(text="And the unit vector along the y-axis, called j-hat. These two unit vectors have length 1, and they point purely along their respective axes.") as tracker:
            self.play(Create(j_hat))
            self.play(Write(j_hat_label))
            self.wait(1)
        
        # Frame 3: Show vector decomposition
        # First show the target vector
        vector = Arrow(start=ORIGIN, end=[3, -2, 0], color=YELLOW, buff=0)
        vector_label = MathTex("\\vec{v} = \\begin{bmatrix} 3 \\\\ -2 \\end{bmatrix}").next_to(vector.get_end(), RIGHT)
        
        with self.voiceover(text="Now, let's see how the vector (3, -2) can be built from these basis vectors.") as tracker:
            self.play(Create(vector), Write(vector_label))
            self.wait(1)
        
        # Show scaling of i-hat
        scaled_i = Arrow(start=ORIGIN, end=[3, 0, 0], color=RED, buff=0)
        i_scaling = MathTex("3\\hat{\\imath}").next_to(scaled_i.get_end(), DOWN)
        
        with self.voiceover(text="First, we scale i-hat by 3, stretching it to three units along the x-axis.") as tracker:
            self.play(Transform(i_hat.copy(), scaled_i))
            self.play(Write(i_scaling))
            self.wait(1)
        
        # Show scaling of j-hat
        scaled_j = Arrow(start=[3, 0, 0], end=[3, -2, 0], color=GREEN, buff=0)
        j_scaling = MathTex("(-2)\\hat{\\jmath}").next_to(scaled_j, RIGHT)
        
        with self.voiceover(text="Then, we scale j-hat by negative 2, which means going two units down.") as tracker:
            self.play(Transform(j_hat.copy(), scaled_j))
            self.play(Write(j_scaling))
            self.wait(1)
        
        # Show the final equation
        equation = MathTex(
            "\\vec{v}", "=", "3\\hat{\\imath}", "+", "(-2)\\hat{\\jmath}", "=",
            "\\begin{bmatrix} 3 \\\\ -2 \\end{bmatrix}"
        ).to_edge(UP)
        
        with self.voiceover(text="So our vector is really the sum of these two scaled basis vectors: three i-hat plus negative two j-hat.") as tracker:
            self.play(Write(equation))
            self.wait(2)

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
        
        # Create basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=GREEN, buff=0)
        i_hat_label = MathTex("\\hat{\\imath}").next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}").next_to(j_hat.get_end(), UP)
        
        # Show initial setup
        with self.voiceover(text="The two special vectors we just saw, i-hat and j-hat, do something more than just help describe individual vectors.") as tracker:
            self.play(
                Create(grid),
                Create(i_hat),
                Create(j_hat),
                Write(i_hat_label),
                Write(j_hat_label)
            )
            self.wait(1)
        
        # Show basis definition
        basis_def = MathTex("\\text{Basis} = \\left\\{ \\hat{\\imath}, \\hat{\\jmath} \\right\\}").to_edge(UP)
        with self.voiceover(text="Together, they form a basis for the entire 2D space.") as tracker:
            self.play(Write(basis_def))
            self.wait(1)
        
        # Show example vectors
        vectors_data = [
            ([2, 3, 0], RED_A),
            ([4, -1, 0], YELLOW_A),
            ([-1, 2, 0], PURPLE_A)
        ]
        
        for end_point, color in vectors_data:
            vector = Arrow(start=ORIGIN, end=end_point, color=color, buff=0)
            # Create component vectors
            x_component = Arrow(start=ORIGIN, end=[end_point[0], 0, 0], color=RED, buff=0)
            y_component = Arrow(start=[end_point[0], 0, 0], end=end_point, color=GREEN, buff=0)
            
            with self.voiceover(text=f"We can create any vector by scaling i-hat and j-hat appropriately and adding them together.") as tracker:
                self.play(
                    Create(vector),
                    Create(x_component),
                    Create(y_component),
                    run_time=2
                )
                self.wait(0.5)
                self.play(
                    FadeOut(vector),
                    FadeOut(x_component),
                    FadeOut(y_component)
                )
        
        # Show the general vector expression
        general_expr = MathTex(
            "\\forall \\vec{v} \\in \\mathbb{R}^2, \\quad \\vec{v} = a\\hat{\\imath} + b\\hat{\\jmath}, \\quad \\text{for some} \\quad a,b \\in \\mathbb{R}"
        ).next_to(basis_def, DOWN)
        
        with self.voiceover(text="In mathematical terms, every vector in the plane can be written as a linear combination of i-hat and j-hat.") as tracker:
            self.play(Write(general_expr))
            self.wait(1)
        
        # Create a lattice effect to show span
        dots = VGroup()
        for i in range(-3, 4):
            for j in range(-3, 4):
                dot = Dot(point=[i, j, 0], color=BLUE_A)
                dots.add(dot)
        
        with self.voiceover(text="This means we can reach any point in the plane by scaling these basis vectors appropriately.") as tracker:
            self.play(
                FadeIn(dots, lag_ratio=0.1),
                run_time=3
            )
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section3(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Create original basis vectors
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=GREEN, buff=0)
        i_hat_label = MathTex("\\hat{\\imath}").next_to(i_hat.get_end(), RIGHT)
        j_hat_label = MathTex("\\hat{\\jmath}").next_to(j_hat.get_end(), UP)
        
        # Show initial setup
        with self.voiceover(text="Now here's an interesting thought: We didn't have to choose i-hat and j-hat as our basis vectors.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(i_hat),
                Create(j_hat),
                Write(i_hat_label),
                Write(j_hat_label)
            )
            self.wait(1)
        
        # Create new basis vectors b1 and b2
        b1 = Arrow(start=ORIGIN, end=[1, 2, 0], color=YELLOW, buff=0)
        b2 = Arrow(start=ORIGIN, end=[2, -1, 0], color=PURPLE, buff=0)
        b1_label = MathTex("\\vec{b}_1").next_to(b1.get_end(), UP+RIGHT)
        b2_label = MathTex("\\vec{b}_2").next_to(b2.get_end(), RIGHT)
        
        # Show new basis vectors definition
        basis_def = MathTex(
            "\\vec{b}_1 = \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}, \\quad",
            "\\vec{b}_2 = \\begin{bmatrix} 2 \\\\ -1 \\end{bmatrix}"
        ).to_edge(UP)
        
        with self.voiceover(text="We could have picked two completely different vectors — say, one pointing up and to the right, and another pointing down and to the right.") as tracker:
            self.play(
                FadeOut(i_hat),
                FadeOut(j_hat),
                FadeOut(i_hat_label),
                FadeOut(j_hat_label)
            )
            self.play(
                Create(b1),
                Create(b2),
                Write(b1_label),
                Write(b2_label),
                Write(basis_def)
            )
            self.wait(1)
        
        # Demonstrate vector construction with new basis
        target_point = [2, 1, 0]  # Example vector to reach
        # Calculate coefficients (a=1, b=0.5 in this example)
        scaled_b1 = Arrow(start=ORIGIN, end=np.array([1, 2, 0]), color=YELLOW, buff=0)
        scaled_b2 = Arrow(
            start=scaled_b1.get_end(),
            end=scaled_b1.get_end() + np.array([1, -0.5, 0]),
            color=PURPLE,
            buff=0
        )
        result_vector = Arrow(start=ORIGIN, end=target_point, color=WHITE, buff=0)
        
        vector_eq = MathTex(
            "\\vec{v} = a\\vec{b}_1 + b\\vec{b}_2",
            "\\quad \\text{for some} \\quad a, b \\in \\mathbb{R}"
        ).next_to(basis_def, DOWN)
        
        with self.voiceover(text="As long as these two vectors aren't pointing in exactly the same direction, we can still reach every point in the plane by scaling and adding them.") as tracker:
            self.play(Write(vector_eq))
            self.play(
                Create(scaled_b1),
                Create(scaled_b2),
                Create(result_vector)
            )
            self.wait(1)
        
        # Create lattice with new basis
        dots = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                point = np.array([1, 2, 0]) * i + np.array([2, -1, 0]) * j
                dot = Dot(point=point, color=YELLOW_A)
                dots.add(dot)
        
        with self.voiceover(text="Different pairs of vectors can serve as a basis. The coordinates we assign to vectors depend on which basis we choose.") as tracker:
            self.play(
                FadeIn(dots, lag_ratio=0.1),
                run_time=3
            )
            self.wait(1)
        
        # Split screen comparison
        # Move current setup to the right
        right_group = VGroup(
            grid, b1, b2, b1_label, b2_label,
            dots, scaled_b1, scaled_b2, result_vector
        )
        right_group.generate_target()
        right_group.target.shift(RIGHT * 3)
        
        # Create left side with original basis
        left_grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        ).shift(LEFT * 3)
        
        left_i_hat = Arrow(start=left_grid.get_origin(), end=left_grid.get_origin() + [1, 0, 0], color=RED, buff=0)
        left_j_hat = Arrow(start=left_grid.get_origin(), end=left_grid.get_origin() + [0, 1, 0], color=GREEN, buff=0)
        
        # Create dots for standard basis
        std_dots = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                point = left_grid.get_origin() + np.array([i, j, 0])
                dot = Dot(point=point, color=BLUE_A)
                std_dots.add(dot)
        
        with self.voiceover(text="Let's compare how the same space looks with different bases.") as tracker:
            self.play(
                MoveToTarget(right_group),
                Create(left_grid),
                Create(left_i_hat),
                Create(left_j_hat),
                FadeIn(std_dots, lag_ratio=0.1)
            )
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section4(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Start with two independent vectors
        v1 = Arrow(start=ORIGIN, end=[2, 1, 0], color=RED, buff=0)
        v2 = Arrow(start=ORIGIN, end=[0, 2, 0], color=BLUE, buff=0)
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), RIGHT)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), UP)
        
        with self.voiceover(text="Whenever you scale two vectors and add them together, the result is called a linear combination.") as tracker:
            self.play(Create(grid))
            self.play(
                Create(v1),
                Create(v2),
                Write(v1_label),
                Write(v2_label)
            )
            self.wait(1)
        
        # Show linear combination definition
        linear_comb = MathTex(
            "a\\vec{v}_1 + b\\vec{v}_2",
            "\\quad \\text{where} \\quad a, b \\in \\mathbb{R}"
        ).to_edge(UP)
        
        # Frame 2: Demonstrate a single linear combination
        a, b = 1.5, 0.75  # Example coefficients
        scaled_v1 = Arrow(start=ORIGIN, end=np.array([2, 1, 0]) * a, color=RED, buff=0)
        scaled_v2_start = scaled_v1.get_end()
        scaled_v2_end = scaled_v1.get_end() + np.array([0, 2, 0]) * b
        scaled_v2 = Arrow(start=scaled_v2_start, end=scaled_v2_end, color=BLUE, buff=0)
        result = Arrow(start=ORIGIN, end=scaled_v2_end, color=YELLOW, buff=0)
        
        with self.voiceover(text="If you ask, 'What are all the possible vectors I can reach by scaling and adding two given vectors?' — that's called their span.") as tracker:
            self.play(Write(linear_comb))
            self.play(
                Transform(v1.copy(), scaled_v1),
                run_time=1
            )
            self.play(
                Create(scaled_v2),
                run_time=1
            )
            self.play(Create(result))
            self.wait(1)
        
        # Show span definition
        span_def = MathTex(
            "\\text{span}\\{\\vec{v}_1, \\vec{v}_2\\} = \\{a\\vec{v}_1 + b\\vec{v}_2 \\mid a, b \\in \\mathbb{R}\\}"
        ).next_to(linear_comb, DOWN)
        
        # Frame 3: Show span filling the plane
        dots = VGroup()
        for i in np.linspace(-2, 2, 20):
            for j in np.linspace(-2, 2, 20):
                point = np.array([2, 1, 0]) * i + np.array([0, 2, 0]) * j
                dot = Dot(point=point, color=YELLOW_A, radius=0.05)
                dots.add(dot)
        
        with self.voiceover(text="A linear combination is one single operation: scaling and adding two vectors. The span is the set of all vectors you can reach with every possible choice of scalars.") as tracker:
            self.play(Write(span_def))
            self.play(
                FadeIn(dots, lag_ratio=0.1),
                run_time=3
            )
            self.wait(1)
        
        # Frame 4: Show dependent vectors case
        self.play(
            *[FadeOut(mob) for mob in [dots, scaled_v1, scaled_v2, result]],
            run_time=1
        )
        
        # Create dependent vectors
        dep_v1 = Arrow(start=ORIGIN, end=[2, 1, 0], color=RED, buff=0)
        dep_v2 = Arrow(start=ORIGIN, end=[4, 2, 0], color=BLUE, buff=0)
        dep_v1_label = MathTex("\\vec{v}_1").next_to(dep_v1.get_end(), UP)
        dep_v2_label = MathTex("\\vec{v}_2").next_to(dep_v2.get_end(), UP)
        
        with self.voiceover(text="When vectors are aligned or parallel, we call them dependent. Their span is restricted to a single line through the origin.") as tracker:
            self.play(
                Transform(v1, dep_v1),
                Transform(v2, dep_v2),
                Transform(v1_label, dep_v1_label),
                Transform(v2_label, dep_v2_label)
            )
            
            # Create line of dependent span
            line_dots = VGroup()
            for t in np.linspace(-2, 2, 20):
                point = np.array([2, 1, 0]) * t
                dot = Dot(point=point, color=RED_A, radius=0.05)
                line_dots.add(dot)
            
            self.play(
                FadeIn(line_dots, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Frame 5: Conceptual summary
        summary = VGroup(
            Text("Independent vectors:", color=GREEN).scale(0.7),
            Text("→ Span entire plane", color=GREEN).scale(0.7),
            Text("Dependent vectors:", color=RED).scale(0.7),
            Text("→ Span only a line", color=RED).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="In two dimensions, a pair of independent vectors can reach everywhere, but aligned vectors trap you on a single line.") as tracker:
            self.play(Write(summary))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section5(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Start with two independent vectors
        v1 = Arrow(start=ORIGIN, end=[2, 1, 0], color=RED, buff=0)
        v2 = Arrow(start=ORIGIN, end=[1, 2, 0], color=BLUE, buff=0)
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), RIGHT)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), UP)
        
        with self.voiceover(text="You might wonder — why do we call it a linear combination? What does this have to do with lines?") as tracker:
            self.play(Create(grid))
            self.play(
                Create(v1),
                Create(v2),
                Write(v1_label),
                Write(v2_label)
            )
            self.wait(1)
        
        # Show linear combination with fixed b
        fixed_b_eq = MathTex(
            "\\vec{v}(a) = a\\vec{v}_1 + b\\vec{v}_2",
            "\\quad \\text{with fixed} \\quad b"
        ).to_edge(UP)
        
        # Frame 2 & 3: Fix b and vary a
        b = 1  # Fixed value for b
        fixed_v2_scaled = Arrow(
            start=ORIGIN,
            end=np.array([1, 2, 0]) * b,
            color=BLUE_A,
            buff=0
        )
        
        # Create dots to show the line traced by varying a
        line_dots_a = VGroup()
        for a in np.linspace(-2, 2, 30):
            point = np.array([2, 1, 0]) * a + np.array([1, 2, 0]) * b
            dot = Dot(point=point, color=RED_A, radius=0.05)
            line_dots_a.add(dot)
        
        with self.voiceover(text="Here's one way to think about it: Imagine fixing one scalar, say b, and letting the other scalar, a, vary freely.") as tracker:
            self.play(Write(fixed_b_eq))
            self.play(Create(fixed_v2_scaled))
            self.play(
                FadeIn(line_dots_a, lag_ratio=0.1),
                run_time=2
            )
        
        # Animate a moving vector to show the line being traced
        def get_moving_vector(t):
            a = np.cos(t) * 2  # Vary a between -2 and 2
            end_point = np.array([2, 1, 0]) * a + np.array([1, 2, 0]) * b
            return Arrow(start=ORIGIN, end=end_point, color=YELLOW, buff=0)
        
        moving_vector = get_moving_vector(0)
        with self.voiceover(text="As you change a, the tip of the resulting vector traces out a straight line in space.") as tracker:
            self.play(Create(moving_vector))
            for t in np.linspace(0, TAU, 30):
                new_vector = get_moving_vector(t)
                self.play(
                    Transform(moving_vector, new_vector),
                    run_time=0.1,
                    rate_func=linear
                )
        
        # Frame 4: Now fix a and vary b
        self.play(FadeOut(line_dots_a), FadeOut(moving_vector))
        
        fixed_a_eq = MathTex(
            "\\vec{v}(b) = a\\vec{v}_1 + b\\vec{v}_2",
            "\\quad \\text{with fixed} \\quad a"
        ).next_to(fixed_b_eq, DOWN)
        
        a = 1  # Now fix a
        fixed_v1_scaled = Arrow(
            start=ORIGIN,
            end=np.array([2, 1, 0]) * a,
            color=RED_A,
            buff=0
        )
        
        # Create dots for the second line
        line_dots_b = VGroup()
        for b in np.linspace(-2, 2, 30):
            point = np.array([2, 1, 0]) * a + np.array([1, 2, 0]) * b
            dot = Dot(point=point, color=BLUE_A, radius=0.05)
            line_dots_b.add(dot)
        
        with self.voiceover(text="Similarly, fixing a and varying b also traces a line — just in a different direction.") as tracker:
            self.play(Write(fixed_a_eq))
            self.play(Create(fixed_v1_scaled))
            self.play(
                FadeIn(line_dots_b, lag_ratio=0.1),
                run_time=2
            )
        
        # Frame 5: Show full span for independent vectors
        span_dots = VGroup()
        for i in np.linspace(-2, 2, 20):
            for j in np.linspace(-2, 2, 20):
                point = np.array([2, 1, 0]) * i + np.array([1, 2, 0]) * j
                dot = Dot(point=point, color=YELLOW_A, radius=0.05)
                span_dots.add(dot)
        
        with self.voiceover(text="If the vectors are independent, varying both a and b freely gives you the entire plane.") as tracker:
            self.play(
                FadeOut(fixed_v1_scaled),
                FadeOut(fixed_v2_scaled),
                FadeOut(line_dots_b)
            )
            self.play(
                FadeIn(span_dots, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Frame 6: Special case with dependent vectors
        self.play(
            FadeOut(span_dots),
            FadeOut(fixed_b_eq),
            FadeOut(fixed_a_eq)
        )
        
        # Transform to dependent vectors
        dep_v1 = Arrow(start=ORIGIN, end=[2, 1, 0], color=RED, buff=0)
        dep_v2 = Arrow(start=ORIGIN, end=[4, 2, 0], color=BLUE, buff=0)
        dep_v1_label = MathTex("\\vec{v}_1").next_to(dep_v1.get_end(), UP)
        dep_v2_label = MathTex("\\vec{v}_2").next_to(dep_v2.get_end(), UP)
        
        # Show single line for dependent case
        dep_line_dots = VGroup()
        for t in np.linspace(-2, 2, 30):
            point = np.array([2, 1, 0]) * t
            dot = Dot(point=point, color=RED_A, radius=0.05)
            dep_line_dots.add(dot)
        
        with self.voiceover(text="But if the vectors are dependent, no matter how you vary a and b, you're stuck on a single line.") as tracker:
            self.play(
                Transform(v1, dep_v1),
                Transform(v2, dep_v2),
                Transform(v1_label, dep_v1_label),
                Transform(v2_label, dep_v2_label)
            )
            self.play(
                FadeIn(dep_line_dots, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Add final summary
        summary = VGroup(
            Text("Linear combinations trace lines", color=YELLOW).scale(0.7),
            Text("when varying one scalar", color=YELLOW).scale(0.7),
            Text("Independent vectors:", color=GREEN).scale(0.7),
            Text("→ Can reach entire plane", color=GREEN).scale(0.7),
            Text("Dependent vectors:", color=RED).scale(0.7),
            Text("→ Stuck on one line", color=RED).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="This connection to straight lines is why we call them linear combinations. It's a fundamental property that leads to many important concepts in linear algebra.") as tracker:
            self.play(Write(summary))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section6(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Show multiple vectors as arrows
        vectors_data = [
            ([2, 1, 0], RED),
            ([1, 2, 0], BLUE),
            ([-1, 2, 0], GREEN),
            ([3, -1, 0], YELLOW),
            ([0, 3, 0], PURPLE),
            ([-2, -1, 0], ORANGE),
            ([1, -2, 0], PINK)
        ]
        
        vectors = VGroup()
        vector_tips = VGroup()
        
        with self.voiceover(text="So far, we've been visualizing vectors as arrows starting from the origin.") as tracker:
            self.play(Create(grid))
            
            # Create all vectors and their tip dots
            for end_point, color in vectors_data:
                vector = Arrow(start=ORIGIN, end=end_point, color=color, buff=0)
                tip_dot = Dot(point=end_point, color=color)
                vectors.add(vector)
                vector_tips.add(tip_dot)
            
            self.play(
                Create(vectors),
                run_time=2
            )
            self.wait(1)
        
        with self.voiceover(text="But when you're dealing with a collection of vectors, it can get messy and crowded to draw all those arrows.") as tracker:
            # Add a few more vectors to emphasize crowding
            extra_vectors = VGroup()
            for i in range(5):
                angle = np.random.uniform(0, TAU)
                length = np.random.uniform(1, 3)
                end_point = [length * np.cos(angle), length * np.sin(angle), 0]
                vector = Arrow(start=ORIGIN, end=end_point, color=GRAY, buff=0)
                extra_vectors.add(vector)
            
            self.play(Create(extra_vectors))
            self.wait(1)
        
        # Frame 2: Transition to points
        with self.voiceover(text="Instead, it's often easier to represent vectors as points: Place a dot where the tip of the vector would be.") as tracker:
            # Create dots at vector tips
            self.play(
                Create(vector_tips),
                FadeOut(vectors),
                FadeOut(extra_vectors),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: Emphasize points with glowing effect
        glowing_dots = VGroup()
        for dot in vector_tips:
            glow = Dot(
                dot.get_center(),
                color=dot.get_color(),
                radius=0.2            )
            glowing_dots.add(glow)
        
        with self.voiceover(text="Always imagine the tail stays at the origin. In this way, thinking about many vectors together becomes much cleaner.") as tracker:
            self.play(
                FadeIn(glowing_dots),
                vector_tips.animate.set_color(WHITE),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Show different spans
        # Clear previous points
        self.play(
            FadeOut(vector_tips),
            FadeOut(glowing_dots)
        )
        
        # Show line of points (collinear vectors)
        line_dots = VGroup()
        for t in np.linspace(-3, 3, 30):
            point = np.array([2, 1, 0]) * t
            dot = Dot(point=point, color=RED_A, radius=0.05)
            line_dots.add(dot)
        
        # Show plane of points (independent vectors)
        plane_dots = VGroup()
        for i in np.linspace(-2, 2, 15):
            for j in np.linspace(-2, 2, 15):
                point = np.array([2, 1, 0]) * i + np.array([-1, 2, 0]) * j
                dot = Dot(point=point, color=BLUE_A, radius=0.05)
                plane_dots.add(dot)
        
        # Show the line span first
        with self.voiceover(text="A line of points represents the span of two collinear vectors.") as tracker:
            self.play(
                FadeIn(line_dots, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Then show the plane span
        with self.voiceover(text="A filled plane of points represents the span of two independent vectors.") as tracker:
            self.play(
                FadeOut(line_dots),
                FadeIn(plane_dots, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Add final summary
        summary = VGroup(
            Text("Vectors as Points:", color=YELLOW).scale(0.7),
            Text("→ Cleaner visualization", color=YELLOW).scale(0.7),
            Text("→ Better for collections", color=YELLOW).scale(0.7),
            Text("Line of points:", color=RED).scale(0.7),
            Text("→ Dependent vectors", color=RED).scale(0.7),
            Text("Plane of points:", color=BLUE).scale(0.7),
            Text("→ Independent vectors", color=BLUE).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="This way of thinking about vectors as points helps us visualize spans and collections more easily, preparing us for more advanced concepts in linear algebra.") as tracker:
            self.play(Write(summary))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section7(self):
        # Create 3D scene
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Add labels for axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        # Frame 1: Show 3D coordinate system
        with self.voiceover(text="Now, let's take these ideas into three dimensions.") as tracker:
            self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
            self.play(
                Create(axes),
                Write(labels),
                run_time=2
            )
            self.wait(1)
        
        # Frame 2: Plot two independent vectors
        v1 = Arrow3D(
            start=ORIGIN,
            end=[2, 1, 2],  # upward-right
            color=RED
        )
        v2 = Arrow3D(
            start=ORIGIN,
            end=[1, -2, 1],  # forward-left
            color=BLUE
        )
        
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), UP+RIGHT)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), LEFT)
        
        with self.voiceover(text="What happens if you take two vectors in 3D space that don't point in the same direction?") as tracker:
            self.play(
                Create(v1),
                Create(v2),
                Write(v1_label),
                Write(v2_label)
            )
            self.wait(1)
        
        # Show span definition
        span_def = MathTex(
            "\\text{span}\\{ \\vec{v}_1, \\vec{v}_2 \\} = \\{ a\\vec{v}_1 + b\\vec{v}_2 \\mid a, b \\in \\mathbb{R} \\}"
        ).to_edge(UP)
        
        # Frame 3: Demonstrate a single linear combination
        a, b = 1.5, 0.75  # Example coefficients
        scaled_v1 = Arrow3D(
            start=ORIGIN,
            end=np.array([2, 1, 2]) * a,
            color=RED_A
        )
        scaled_v2_start = scaled_v1.get_end()
        scaled_v2_end = scaled_v1.get_end() + np.array([1, -2, 1]) * b
        scaled_v2 = Arrow3D(
            start=scaled_v2_start,
            end=scaled_v2_end,
            color=BLUE_A
        )
        result = Arrow3D(
            start=ORIGIN,
            end=scaled_v2_end,
            color=YELLOW
        )
        
        with self.voiceover(text="If you scale and add them together — forming linear combinations — you won't fill the whole 3D space yet.") as tracker:
            self.play(Write(span_def))
            self.play(
                Transform(v1.copy(), scaled_v1),
                run_time=1
            )
            self.play(
                Create(scaled_v2),
                Create(result),
                run_time=1
            )
            self.wait(1)
        
        # Frame 4: Show the plane being swept out
        # Create a grid of points to represent the plane
        plane_points = VGroup()
        for i in np.linspace(-2, 2, 15):
            for j in np.linspace(-2, 2, 15):
                point = np.array([2, 1, 2]) * i + np.array([1, -2, 1]) * j
                dot = Dot3D(point=point, color=YELLOW_A, radius=0.05)
                plane_points.add(dot)
        
        # Create a semi-transparent surface
        plane = Surface(
            lambda u, v: np.array([
                2*u + v,
                u - 2*v,
                2*u + v
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            checkerboard_colors=[YELLOW_A]        )
        
        with self.voiceover(text="Instead, the tips of the resulting vectors trace out a flat sheet — a two-dimensional plane cutting through the origin.") as tracker:
            self.play(
                FadeOut(scaled_v1),
                FadeOut(scaled_v2),
                FadeOut(result)
            )
            self.play(
                FadeIn(plane_points, lag_ratio=0.1),
                Create(plane),
                run_time=3
            )
            self.wait(1)
        
        # Frame 5: Emphasize 2D nature in 3D space
        # Rotate camera to show different angles
        with self.voiceover(text="Although you are in three dimensions, the span of two vectors only fills a 2D surface, the plane.") as tracker:
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(3)
            self.stop_ambient_camera_rotation()
        
        # Add final summary
        summary = VGroup(
            Text("In 3D Space:", color=YELLOW).scale(0.7),
            Text("Two independent vectors:", color=WHITE).scale(0.7),
            Text("→ Span a plane", color=BLUE).scale(0.7),
            Text("Three needed to fill space", color=GREEN).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="This shows us that we need three independent vectors to fill the whole three-dimensional space.") as tracker:
            self.play(Write(summary))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section8(self):
        # Create 3D scene
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Add labels for axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        # Frame 1: Start with two vectors spanning a plane
        v1 = Arrow3D(start=ORIGIN, end=[2, 1, 0], color=RED)
        v2 = Arrow3D(start=ORIGIN, end=[0, 2, 1], color=BLUE)
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), RIGHT)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), UP)
        
        # Create plane spanned by v1 and v2
        plane = Surface(
            lambda u, v: np.array([
                2*u + 0*v,
                u + 2*v,
                0*u + v
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            checkerboard_colors=[BLUE_A]
        )
        
        with self.voiceover(text="Now, what happens if we add a third vector into the mix in 3D space?") as tracker:
            self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
            self.play(
                Create(axes),
                Write(labels),
                Create(v1),
                Create(v2),
                Write(v1_label),
                Write(v2_label),
                Create(plane),
                run_time=2
            )
            self.wait(1)
        
        # Show linear combination equation
        linear_comb = MathTex(
            "a\\vec{v}_1 + b\\vec{v}_2 + c\\vec{v}_3",
            "\\quad \\text{with} \\quad a, b, c \\in \\mathbb{R}"
        ).to_edge(UP)
        
        # Frame 2: Add dependent third vector
        v3_dep = Arrow3D(
            start=ORIGIN,
            end=[1, 1.5, 0.5],  # Linear combination of v1 and v2
            color=GREEN
        )
        v3_dep_label = MathTex("\\vec{v}_3").next_to(v3_dep.get_end(), RIGHT+UP)
        
        with self.voiceover(text="We can again form linear combinations — this time by scaling all three vectors and adding them together.") as tracker:
            self.play(Write(linear_comb))
            self.play(
                Create(v3_dep),
                Write(v3_dep_label)
            )
            self.wait(1)
        
        # Show that dependent vector doesn't expand span
        with self.voiceover(text="If the third vector lies within the plane spanned by the first two, it doesn't unlock any new directions — you're still stuck in the same plane.") as tracker:
            # Create points to show span remains in plane
            plane_points = VGroup()
            for i in np.linspace(-1, 1, 10):
                for j in np.linspace(-1, 1, 10):
                    point = np.array([2, 1, 0]) * i + np.array([0, 2, 1]) * j
                    dot = Dot3D(point=point, color=YELLOW_A, radius=0.05)
                    plane_points.add(dot)
        
            self.play(
                FadeIn(plane_points, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: Switch to independent third vector
        self.play(
            FadeOut(v3_dep),
            FadeOut(v3_dep_label),
            FadeOut(plane_points)
        )
        
        v3_ind = Arrow3D(
            start=ORIGIN,
            end=[0, 1, 2],  # Points significantly out of the plane
            color=GREEN
        )
        v3_ind_label = MathTex("\\vec{v}_3").next_to(v3_ind.get_end(), UP)
        
        with self.voiceover(text="But if the third vector points outside the plane, it unlocks the entire three-dimensional space!") as tracker:
            self.play(
                Create(v3_ind),
                Write(v3_ind_label)
            )
            
            # Create points filling 3D space
            space_points = VGroup()
            for i in np.linspace(-1, 1, 5):
                for j in np.linspace(-1, 1, 5):
                    for k in np.linspace(-1, 1, 5):
                        point = (np.array([2, 1, 0]) * i + 
                                np.array([0, 2, 1]) * j +
                                np.array([0, 1, 2]) * k)
                        dot = Dot3D(point=point, color=YELLOW_A, radius=0.05)
                        space_points.add(dot)
        
            self.play(
                FadeIn(space_points, lag_ratio=0.1),
                FadeOut(plane),
                run_time=3
            )
            self.wait(1)
        
        # Frame 4: Split screen comparison
        # Move current setup to the right
        right_group = VGroup(
            axes, v1, v2, v3_ind, space_points,
            v1_label, v2_label, v3_ind_label
        )
        
        with self.voiceover(text="Now, you can reach every point in 3D by linear combinations.") as tracker:
            # Rotate camera to show the full 3D effect
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(3)
            self.stop_ambient_camera_rotation()
        
        # Add final summary
        summary = VGroup(
            Text("Third Vector:", color=YELLOW).scale(0.7),
            Text("In the plane:", color=RED).scale(0.7),
            Text("→ Still 2D span", color=RED).scale(0.7),
            Text("Out of plane:", color=GREEN).scale(0.7),
            Text("→ Full 3D span", color=GREEN).scale(0.7),
            Text("Linear Independence:", color=BLUE).scale(0.7),
            Text("→ Adds new dimension", color=BLUE).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="This shows us how linear independence determines whether a vector adds a new dimension to the span.") as tracker:
            self.play(Write(summary))
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section9(self):
        # Create 3D scene
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Add labels for axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        # Frame 1: Show three vectors in 3D
        v1 = Arrow3D(start=ORIGIN, end=[2, 1, 1], color=RED)
        v2 = Arrow3D(start=ORIGIN, end=[1, 2, 0], color=BLUE)
        v3 = Arrow3D(start=ORIGIN, end=[3, 3, 1], color=GREEN)  # This will be dependent
        
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), RIGHT)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), UP)
        v3_label = MathTex("\\vec{v}_3").next_to(v3.get_end(), LEFT)
        
        with self.voiceover(text="Let's now be a little more precise: When we say vectors are linearly dependent, we mean:") as tracker:
            self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
            self.play(
                Create(axes),
                Write(labels),
                Create(v1),
                Create(v2),
                Create(v3),
                Write(v1_label),
                Write(v2_label),
                Write(v3_label),
                run_time=2
            )
            self.wait(1)
        
        # Show formal definition
        dependence_def = MathTex(
            "\\exists \\, a_1, a_2, \\ldots, a_n \\, \\text{not all zero}",
            "\\quad \\text{such that} \\quad",
            "a_1\\vec{v}_1 + a_2\\vec{v}_2 + \\cdots + a_n\\vec{v}_n = \\vec{0}"
        ).to_edge(UP)
        
        with self.voiceover(text="There is some way to scale and add them together to get the zero vector, without all scalars being zero.") as tracker:
            self.play(Write(dependence_def))
            self.wait(1)
        
        # Frame 2: Demonstrate dependent case
        # Create scaled vectors for a combination that equals zero
        # For example: 2v₁ - v₂ - v₃ = 0
        scaled_v1 = Arrow3D(start=ORIGIN, end=np.array([2, 1, 1]) * 2, color=RED_A)
        scaled_v2 = Arrow3D(
            start=scaled_v1.get_end(),
            end=scaled_v1.get_end() - np.array([1, 2, 0]),
            color=BLUE_A
        )
        scaled_v3 = Arrow3D(
            start=scaled_v2.get_end(),
            end=ORIGIN,  # Should end at origin to show dependence
            color=GREEN_A
        )
        
        # Show coefficients
        coefficients = MathTex(
            "2\\vec{v}_1 - \\vec{v}_2 - \\vec{v}_3 = \\vec{0}"
        ).next_to(dependence_def, DOWN)
        
        with self.voiceover(text="For example, we can scale the first vector by 2, subtract the second vector, and subtract the third vector to get back to zero.") as tracker:
            self.play(Write(coefficients))
            self.play(
                Transform(v1.copy(), scaled_v1),
                run_time=1
            )
            self.play(
                Create(scaled_v2),
                run_time=1
            )
            self.play(
                Create(scaled_v3),
                run_time=1
            )
            self.wait(1)
        
        # Frame 3: Show independent case
        self.play(
            *[FadeOut(mob) for mob in [scaled_v1, scaled_v2, scaled_v3, coefficients]],
            run_time=1
        )
        
        # Create new independent vectors
        ind_v1 = Arrow3D(start=ORIGIN, end=[1, 0, 0], color=RED)
        ind_v2 = Arrow3D(start=ORIGIN, end=[0, 1, 0], color=BLUE)
        ind_v3 = Arrow3D(start=ORIGIN, end=[0, 0, 1], color=GREEN)
        
        independence_def = MathTex(
            "a_1\\vec{v}_1 + a_2\\vec{v}_2 + a_3\\vec{v}_3 = \\vec{0}",
            "\\quad \\Rightarrow \\quad",
            "a_1 = a_2 = a_3 = 0"
        ).next_to(dependence_def, DOWN)
        
        with self.voiceover(text="On the other hand, vectors are linearly independent if the only way to get the zero vector is by setting all scalars to zero.") as tracker:
            self.play(
                Transform(v1, ind_v1),
                Transform(v2, ind_v2),
                Transform(v3, ind_v3),
                Transform(v1_label, MathTex("\\vec{v}_1").next_to(ind_v1.get_end(), RIGHT)),
                Transform(v2_label, MathTex("\\vec{v}_2").next_to(ind_v2.get_end(), UP)),
                Transform(v3_label, MathTex("\\vec{v}_3").next_to(ind_v3.get_end(), OUT)),
                Write(independence_def),
                run_time=2
            )
            self.wait(1)
        
        # Frame 4: Conceptual summary
        summary = VGroup(
            Text("Linear Dependence:", color=RED).scale(0.7),
            Text("→ Some vector is redundant", color=RED).scale(0.7),
            Text("→ Can be written as", color=RED).scale(0.7),
            Text("   combination of others", color=RED).scale(0.7),
            Text("Linear Independence:", color=GREEN).scale(0.7),
            Text("→ No redundancy", color=GREEN).scale(0.7),
            Text("→ Each vector adds", color=GREEN).scale(0.7),
            Text("   something new", color=GREEN).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="In summary: dependence means redundancy - some vector could be removed without losing anything. Independence means each vector contributes something unique that can't be achieved by the others.") as tracker:
            self.play(Write(summary))
            
            # Rotate camera to emphasize 3D nature
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(3)
            self.stop_ambient_camera_rotation()
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

    def section10(self):
        # Create grid and axes
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
            }
        )
        
        # Frame 1: Recap of key concepts
        title = Text("What makes a Basis?", color=YELLOW).scale(0.8).to_edge(UP)
        
        with self.voiceover(text="Now, let's bring everything together.") as tracker:
            self.play(
                Create(grid),
                Write(title)
            )
            self.wait(1)
        
        # Show formal definition
        basis_def = VGroup(
            MathTex("\\text{A set } \\{\\vec{v}_1, \\vec{v}_2, \\ldots, \\vec{v}_n\\} \\text{ is a basis if:}"),
            Text("1. They are linearly independent", color=BLUE).scale(0.7),
            Text("2. Their span covers the entire space", color=GREEN).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN)
        
        with self.voiceover(text="A basis of a space is a set of vectors that satisfies two important properties: They are linearly independent — no redundancy among them. Their span covers the entire space.") as tracker:
            self.play(Write(basis_def))
            self.wait(1)
        
        # Frame 2: Show 2D basis example
        self.play(
            *[FadeOut(mob) for mob in [basis_def]],
            run_time=1
        )
        
        # Create 2D basis vectors
        v1_2d = Arrow(start=ORIGIN, end=[1, 0, 0], color=RED, buff=0)
        v2_2d = Arrow(start=ORIGIN, end=[0, 1, 0], color=BLUE, buff=0)
        v1_2d_label = MathTex("\\vec{v}_1").next_to(v1_2d.get_end(), RIGHT)
        v2_2d_label = MathTex("\\vec{v}_2").next_to(v2_2d.get_end(), UP)
        
        # Create lattice points to show span
        dots_2d = VGroup()
        for i in np.linspace(-2, 2, 15):
            for j in np.linspace(-2, 2, 15):
                point = np.array([1, 0, 0]) * i + np.array([0, 1, 0]) * j
                dot = Dot(point=point, color=YELLOW_A, radius=0.05)
                dots_2d.add(dot)
        
        with self.voiceover(text="In 2D: Two independent vectors form a basis.") as tracker:
            self.play(
                Create(v1_2d),
                Create(v2_2d),
                Write(v1_2d_label),
                Write(v2_2d_label)
            )
            self.play(
                FadeIn(dots_2d, lag_ratio=0.1),
                run_time=2
            )
            self.wait(1)
        
        # Frame 3: Transition to 3D
        self.clear()
        
        # Create 3D scene
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # Add labels for axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        # Create 3D basis vectors
        v1_3d = Arrow3D(start=ORIGIN, end=[1, 0, 0], color=RED)
        v2_3d = Arrow3D(start=ORIGIN, end=[0, 1, 0], color=BLUE)
        v3_3d = Arrow3D(start=ORIGIN, end=[0, 0, 1], color=GREEN)
        
        v1_3d_label = MathTex("\\vec{v}_1").next_to(v1_3d.get_end(), RIGHT)
        v2_3d_label = MathTex("\\vec{v}_2").next_to(v2_3d.get_end(), UP)
        v3_3d_label = MathTex("\\vec{v}_3").next_to(v3_3d.get_end(), OUT)
        
        with self.voiceover(text="In 3D: Three independent vectors form a basis.") as tracker:
            self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
            self.play(
                Create(axes),
                Write(labels),
                Create(v1_3d),
                Create(v2_3d),
                Create(v3_3d),
                Write(v1_3d_label),
                Write(v2_3d_label),
                Write(v3_3d_label),
                run_time=2
            )
            
            # Create points filling 3D space
            space_points = VGroup()
            for i in np.linspace(-1, 1, 5):
                for j in np.linspace(-1, 1, 5):
                    for k in np.linspace(-1, 1, 5):
                        point = np.array([1, 0, 0]) * i + np.array([0, 1, 0]) * j + np.array([0, 0, 1]) * k
                        dot = Dot3D(point=point, color=YELLOW_A, radius=0.05)
                        space_points.add(dot)
        
            self.play(
                FadeIn(space_points, lag_ratio=0.1),
                run_time=2
            )
            
            # Rotate camera to show the full 3D effect
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(3)
            self.stop_ambient_camera_rotation()
        
        # Frame 4: Building blocks concept
        building_blocks = VGroup(
            Text("A basis gives you:", color=YELLOW).scale(0.7),
            Text("→ Minimal set of vectors", color=WHITE).scale(0.7),
            Text("→ No redundancy", color=BLUE).scale(0.7),
            Text("→ Reaches everywhere", color=GREEN).scale(0.7),
            Text("→ Perfect building blocks", color=RED).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        
        with self.voiceover(text="In short: A basis gives you the minimal set of building blocks needed to reach every point in the space.") as tracker:
            self.play(Write(building_blocks))
            self.wait(2)
        
        # Frame 5: Transition hint to matrices
        matrix_hint = MathTex(
            "\\begin{bmatrix} \\vec{v}_1 & \\vec{v}_2 & \\vec{v}_3 \\end{bmatrix}",
            "\\quad \\text{leads to matrices...}"
        ).to_edge(UP)
        
        with self.voiceover(text="Each basis gives us a way to organize information about space — leading naturally to the idea of matrices.") as tracker:
            self.play(
                FadeOut(space_points),
                Write(matrix_hint)
            )
            self.wait(2)
        
        # Final cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        
if __name__ == "__main__":
    scene = TransformationMatrices()
    scene.render()

