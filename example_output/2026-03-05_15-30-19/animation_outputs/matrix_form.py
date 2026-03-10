from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Color definitions from ledger
        general_label_color = WHITE
        highlight_color = YELLOW
        input_vector_color = BLUE_C
        second_vector_color = "#8B0000"  # MAROON equivalent
        sum_vector_color = PURPLE_C
        scalar_color = YELLOW
        mapping_arrow_color = GREEN
        
        # ============================================
        # BEAT 0: Setup from previous scene (Step 3)
        # ============================================
        
        # Create domain plane (left)
        domain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            color=LIGHT_GRAY
        )
        domain_plane.move_to(np.array([-3.43, 0.70, 0]))
        
        # Create codomain plane (right)
        codomain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            color=LIGHT_GRAY
        )
        codomain_plane.move_to(np.array([3.43, 0.70, 0]))
        
        # Labels for planes
        v_label = Text("V = R²", color=WHITE, font_size=24)
        v_label.move_to(np.array([-3.43, 3.0, 0]))
        
        w_label = Text("W = R²", color=WHITE, font_size=24)
        w_label.move_to(np.array([3.43, 3.0, 0]))
        
        # General mapping label
        general_mapping_label = Text("T: V → W", color=general_label_color, font_size=32)
        general_mapping_label.move_to(np.array([0, 3.27, 0]))
        
        # Property equations (faint, top-left)
        property_eq1 = MathTex(r"T(\vec{u}+\vec{v})=T(\vec{u})+T(\vec{v})", color=general_label_color)
        property_eq2 = MathTex(r"T(c\vec{u})=cT(\vec{u})", color=general_label_color)
        property_equations = VGroup(property_eq1, property_eq2).arrange(DOWN, aligned_edge=LEFT)
        property_equations.set_opacity(0.3)
        property_equations.move_to(np.array([-5.0, 3.0, 0]))
        
        # Create example icons (will flash)
        # Scaling icon
        scaling_square = Square(side_length=0.5, color=BLUE_C, fill_opacity=0.3)
        scaling_arrow = Arrow(ORIGIN, [0.5, 0, 0], color=BLUE_C, buff=0)
        scaling_icon = VGroup(scaling_square, scaling_arrow)
        scaling_icon.move_to(np.array([-5.5, -2.5, 0]))
        
        # Rotation icon
        rotation_square = Square(side_length=0.5, color=BLUE_C, fill_opacity=0.3)
        rotation_arrow = Arc(radius=0.3, angle=PI/3, color=BLUE_C)
        rotation_icon = VGroup(rotation_square, rotation_arrow)
        rotation_icon.move_to(np.array([5.5, 2.5, 0]))
        
        # Shear icon
        shear_square = Square(side_length=0.5, color=BLUE_C, fill_opacity=0.3)
        shear_line = Line([0, -0.25, 0], [0.25, -0.25, 0], color=BLUE_C)
        shear_icon = VGroup(shear_square, shear_line)
        shear_icon.move_to(np.array([5.5, -2.5, 0]))
        
        # Matrix brackets (empty initially)
        left_bracket = Tex("[", color=general_label_color, font_size=72)
        right_bracket = Tex("]", color=general_label_color, font_size=72)
        brackets = VGroup(left_bracket, right_bracket).arrange(RIGHT, buff=0.8)
        brackets.move_to(np.array([0, 0.70, 0]))
        
        # Matrix representation label
        matrix_label = Text("Matrix Representation", color=highlight_color, font_size=28)
        matrix_label.move_to(np.array([0, 2.0, 0]))
        
        # Show existing setup
        self.add(domain_plane, codomain_plane, v_label, w_label, 
                 general_mapping_label, property_equations)
        
        # ============================================
        # BEAT 1: "We've seen what linear transformations do..."
        # ============================================
        
        with self.voiceover(text="We've seen what linear transformations do. To compute them precisely, we need a concrete representation. For finite-dimensional spaces like R², every linear transformation can be captured by a simple grid of numbers: a matrix.") as tracker:
            self.play(
                FadeIn(scaling_icon),
                FadeIn(rotation_icon),
                FadeIn(shear_icon)
            )
            self.wait(0.5)
            self.play(
                FadeOut(scaling_icon),
                FadeOut(rotation_icon),
                FadeOut(shear_icon),
                run_time=0.5
            )
            self.play(
                Create(left_bracket),
                Create(right_bracket)
            )
            self.play(Write(matrix_label))
        
        self.wait(0.5)
        
        # ============================================
        # BEAT 2: "The key idea is this..."
        # ============================================
        
        # Create basis vectors in V
        i_hat = Arrow(start=ORIGIN, end=[1, 0, 0], color=input_vector_color, buff=0)
        j_hat = Arrow(start=ORIGIN, end=[0, 1, 0], color=second_vector_color, buff=0)
        i_label = MathTex(r"\hat{i}", color=input_vector_color, font_size=24)
        j_label = MathTex(r"\hat{j}", color=second_vector_color, font_size=24)
        
        # Position basis vectors on domain plane
        i_hat.move_to(np.array([-3.43, 0.70, 0]))
        j_hat.move_to(np.array([-3.43, 0.70, 0]))
        i_label.next_to(i_hat.get_end(), RIGHT, buff=0.1)
        j_label.next_to(j_hat.get_end(), UP, buff=0.1)
        
        with self.voiceover(text="The key idea is this: a linear transformation is completely determined by what it does to the basis vectors. In R², the standard basis is i-hat and j-hat.") as tracker:
            self.play(
                domain_plane.animate.set_stroke(opacity=1.0),
                codomain_plane.animate.set_stroke(opacity=0.3)
            )
            self.play(
                GrowArrow(i_hat),
                Write(i_label),
                GrowArrow(j_hat),
                Write(j_label)
            )
            # Gentle pulse
            self.play(
                i_hat.animate.scale(1.1),
                j_hat.animate.scale(1.1),
                run_time=0.5
            )
            self.play(
                i_hat.animate.scale(1/1.1),
                j_hat.animate.scale(1/1.1),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # ============================================
        # BEAT 3: "If we know where T sends i-hat and j-hat..."
        # ============================================
        
        # Generic vector x in V
        vector_x = Arrow(start=ORIGIN, end=[2, 1.5, 0], color=sum_vector_color, buff=0)
        vector_x.move_to(np.array([-3.43, 0.70, 0]))
        x_label = MathTex(r"\vec{x}", color=sum_vector_color, font_size=24)
        x_label.next_to(vector_x.get_end(), RIGHT+UP, buff=0.1)
        
        # Decomposition equation
        decomposition_eq = MathTex(r"\vec{x} = x_1\hat{i} + x_2\hat{j}", color=general_label_color, font_size=28)
        decomposition_eq.move_to(np.array([-3.43, -1.5, 0]))
        
        with self.voiceover(text="If we know where T sends i-hat and j-hat, we can find where it sends any vector. Because any vector x can be written as a combination x₁ i-hat plus x₂ j-hat. By linearity, T(x) must be x₁ T(i-hat) plus x₂ T(j-hat).") as tracker:
            self.play(GrowArrow(vector_x), Write(x_label))
            
            # Show scaled i_hat component
            i_scaled = i_hat.copy().scale(2).set_opacity(0.6).set_color(input_vector_color)
            i_scaled.move_to(np.array([-3.43, 0.70, 0]))
            self.play(Create(i_scaled), run_time=0.75)
            
            # Show scaled j_hat component
            j_scaled = j_hat.copy().scale(1.5).set_opacity(0.6).set_color(second_vector_color)
            j_scaled.move_to(np.array([-3.43, 0.70, 0]) + [2, 0, 0])
            self.play(Create(j_scaled), run_time=0.75)
            
            self.play(Write(decomposition_eq))
            
            # Emphasize property equations
            self.play(
                property_equations.animate.set_opacity(1.0),
                run_time=0.5
            )
            self.play(
                property_equations.animate.set_opacity(0.3),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # Clean up temporary scaled vectors
        self.remove(i_scaled, j_scaled)
        
        # ============================================
        # BEAT 4: "So, let's see where T maps our basis vectors..."
        # ============================================
        
        # Brighten codomain plane
        self.play(codomain_plane.animate.set_stroke(opacity=1.0))
        
        # Create images of basis vectors in W
        vector_a = Arrow(start=ORIGIN, end=[1.5, 0.5, 0], color=input_vector_color, buff=0)
        vector_b = Arrow(start=ORIGIN, end=[-0.5, 2, 0], color=second_vector_color, buff=0)
        vector_a.move_to(np.array([3.43, 0.70, 0]))
        vector_b.move_to(np.array([3.43, 0.70, 0]))
        
        a_label = MathTex(r"T(\hat{i})", color=input_vector_color, font_size=24)
        b_label = MathTex(r"T(\hat{j})", color=second_vector_color, font_size=24)
        a_label.next_to(vector_a.get_end(), RIGHT+UP, buff=0.1)
        b_label.next_to(vector_b.get_end(), LEFT+UP, buff=0.1)
        
        # Also show a and b as labels
        a_text = MathTex(r"\vec{a}", color=input_vector_color, font_size=20)
        b_text = MathTex(r"\vec{b}", color=second_vector_color, font_size=20)
        a_text.next_to(vector_a.get_end(), DOWN, buff=0.1)
        b_text.next_to(vector_b.get_end(), DOWN, buff=0.1)
        
        # Mapping arrows from V to W
        map_i_to_a = Arrow(
            start=np.array([-3.43, 0.70, 0]) + [1, 0, 0],
            end=np.array([3.43, 0.70, 0]) + [1.5, 0.5, 0],
            color=mapping_arrow_color,
            buff=0,
            stroke_width=2
        )
        
        map_j_to_b = Arrow(
            start=np.array([-3.43, 0.70, 0]) + [0, 1, 0],
            end=np.array([3.43, 0.70, 0]) + [-0.5, 2, 0],
            color=mapping_arrow_color,
            buff=0,
            stroke_width=2
        )
        
        with self.voiceover(text="So, let's see where T maps our basis vectors. Suppose T sends i-hat to some new vector a, and j-hat to some new vector b, both in W.") as tracker:
            self.play(
                GrowArrow(vector_a),
                Write(a_label),
                GrowArrow(vector_b),
                Write(b_label)
            )
            self.play(
                Write(a_text),
                Write(b_text)
            )
            self.play(
                GrowArrow(map_i_to_a),
                GrowArrow(map_j_to_b)
            )
        
        self.wait(0.5)
        
        # ============================================
        # BEAT 5: "Now, the matrix for T is simply the grid..."
        # ============================================
        
        # Create the matrix
        matrix_A = MathTex(
            r"A = \begin{bmatrix} 1.5 & -0.5 \\ 0.5 & 2 \end{bmatrix}",
            color=general_label_color,
            font_size=36
        )
        matrix_A.move_to(np.array([0, 0.70, 0]))
        
        # Columns label
        columns_label = Text("Columns are T(î) and T(ĵ)", color=highlight_color, font_size=24)
        columns_label.move_to(np.array([0, -0.5, 0]))
        
        with self.voiceover(text="Now, the matrix for T is simply the grid where we write the coordinates of a and b as columns. The first column is a, the second column is b.") as tracker:
            # Transform brackets into matrix
            self.play(
                FadeOut(left_bracket),
                FadeOut(right_bracket),
                Write(matrix_A)
            )
            
            # Highlight first column
            first_col = matrix_A[0][5:8]  # "1.5 & 0.5"
            self.play(
                first_col.animate.set_color(input_vector_color),
                run_time=0.5
            )
            
            # Arrow from vector a to first column
            arrow_a_to_col = Arrow(
                start=vector_a.get_end() + LEFT * 0.5,
                end=matrix_A.get_left() + RIGHT * 0.3,
                color=input_vector_color,
                buff=0.1,
                stroke_width=1.5
            )
            self.play(Create(arrow_a_to_col), run_time=0.5)
            self.play(FadeOut(arrow_a_to_col), run_time=0.5)
            
            # Highlight second column
            second_col = matrix_A[0][9:12]  # "-0.5 & 2"
            self.play(
                second_col.animate.set_color(second_vector_color),
                run_time=0.5
            )
            
            # Arrow from vector b to second column
            arrow_b_to_col = Arrow(
                start=vector_b.get_end() + RIGHT * 0.5,
                end=matrix_A.get_right() + LEFT * 0.3,
                color=second_vector_color,
                buff=0.1,
                stroke_width=1.5
            )
            self.play(Create(arrow_b_to_col), run_time=0.5)
            self.play(FadeOut(arrow_b_to_col), run_time=0.5)
            
            # Reset colors
            self.play(
                first_col.animate.set_color(general_label_color),
                second_col.animate.set_color(general_label_color)
            )
            
            self.play(Write(columns_label))
        
        self.wait(0.5)
        
        # ============================================
        # BEAT 6: "To apply the transformation to any vector x..."
        # ============================================
        
        # Coordinate vector for x
        coord_vector = MathTex(r"\begin{bmatrix} 2 \\ 1.5 \end{bmatrix}", color=scalar_color, font_size=28)
        coord_vector.next_to(vector_x, DOWN, buff=0.5)
        
        # Multiplication equation
        mult_eq = MathTex(
            r"A\vec{x} = \begin{bmatrix} 1.5 & -0.5 \\ 0.5 & 2 \end{bmatrix} \begin{bmatrix} 2 \\ 1.5 \end{bmatrix}",
            color=general_label_color,
            font_size=36
        )
        mult_eq.move_to(np.array([0, 0.70, 0]))
        
        # Result equation
        result_eq = MathTex(
            r"= \begin{bmatrix} 1.5 \\ 4 \end{bmatrix}",
            color=general_label_color,
            font_size=36
        )
        result_eq.next_to(mult_eq, DOWN, buff=0.3)
        
        # Vector result in W
        result_vector = Arrow(
            start=ORIGIN,
            end=[1.5, 4, 0],
            color=sum_vector_color,
            buff=0
        )
        result_vector.move_to(np.array([3.43, 0.70, 0]))
        result_label = MathTex(r"T(\vec{x})", color=sum_vector_color, font_size=24)
        result_label.next_to(result_vector.get_end(), RIGHT+UP, buff=0.1)
        
        with self.voiceover(text="To apply the transformation to any vector x, we multiply the matrix A by the coordinate vector of x. This computation, matrix-vector multiplication, exactly performs the linear combination x₁ times the first column plus x₂ times the second column.") as tracker:
            # Pulse vector x
            self.play(
                vector_x.animate.scale(1.2),
                x_label.animate.scale(1.2),
                run_time=0.3
            )
            self.play(
                vector_x.animate.scale(1/1.2),
                x_label.animate.scale(1/1.2),
                run_time=0.3
            )
            
            self.play(Write(coord_vector))
            
            # Move matrix left, show multiplication
            self.play(
                matrix_A.animate.shift(LEFT * 2),
                FadeOut(columns_label)
            )
            
            # Show coordinate vector moving right
            coord_vector_copy = coord_vector.copy()
            self.play(
                coord_vector_copy.animate.move_to(np.array([0, 0.70, 0]) + RIGHT * 2)
            )
            
            # Show multiplication dot
            mult_dot = MathTex(r"\cdot", font_size=36, color=general_label_color)
            mult_dot.move_to(np.array([0, 0.70, 0]))
            self.play(Write(mult_dot))
            
            # Transform into multiplication equation
            self.play(
                Transform(matrix_A, mult_eq),
                Transform(coord_vector_copy, mult_eq),
                FadeOut(mult_dot)
            )
            
            # Show scaled columns in W
            # Scale first column by 2
            scaled_a = vector_a.copy().scale(2).set_color("#FFAA66")  # light orange
            self.play(Create(scaled_a), run_time=0.75)
            
            # Scale second column by 1.5
            scaled_b = vector_b.copy().scale(1.5).set_color("#FFAA66")
            self.play(Create(scaled_b), run_time=0.75)
            
            # Show addition tip-to-tail
            tip_to_tail = scaled_b.copy().shift(scaled_a.get_end() - scaled_b.get_start())
            self.play(
                scaled_b.animate.shift(scaled_a.get_end() - scaled_b.get_start()),
                run_time=1
            )
            
            # Show result vector
            self.play(
                GrowArrow(result_vector),
                Write(result_label)
            )
            
            # Show numerical result
            self.play(Write(result_eq))
        
        self.wait(0.5)
        
        # ============================================
        # BEAT 7: "This works for every linear transformation..."
        # ============================================
        
        # Clean up temporary objects
        temp_objects = VGroup(
            vector_x, x_label, coord_vector, coord_vector_copy,
            scaled_a, scaled_b, result_label, result_eq
        )
        
        with self.voiceover(text="This works for every linear transformation. The matrix columns are always the images of the basis vectors. And because any vector is a combination of the basis, the matrix tells us everything about T.") as tracker:
            self.play(FadeOut(temp_objects))
            
            # Sweeping highlight
            highlight_rect = Rectangle(
                width=14, height=6,
                stroke_color=highlight_color,
                stroke_width=2,
                fill_opacity=0.1,
                fill_color=highlight_color
            )
            self.play(Create(highlight_rect), run_time=1.5)
            self.play(FadeOut(highlight_rect))
        
        self.wait(0.5)
        
        # ============================================
        # BEAT 8: "This correspondence is powerful..."
        # ============================================
        
        # Create smaller copies of matrix A
        matrix_A_small = matrix_A.copy().scale(0.5)
        matrix_A_small_top_left = matrix_A_small.copy()
        matrix_A_small_top_right = matrix_A_small.copy()
        matrix_A_small_top_left.move_to(np.array([-4, 3, 0]))
        matrix_A_small_top_right.move_to(np.array([4, 3, 0]))
        
        # Second matrix B for composition hint
        matrix_B = MathTex(r"B", color=general_label_color, font_size=36, opacity=0.8)
        matrix_B.next_to(matrix_A, RIGHT, buff=0.5)
        mult_dot2 = MathTex(r"\cdot", color=general_label_color, font_size=36)
        mult_dot2.next_to(matrix_A, RIGHT, buff=0.2)
        
        arrow_icon = Arrow(
            start=mult_dot2.get_center() + RIGHT * 0.5,
            end=mult_dot2.get_center() + RIGHT * 1.0,
            color=GREEN,
            buff=0,
            stroke_width=1.5
        )
        
        with self.voiceover(text="This correspondence is powerful. It means we can study linear transformations by studying matrices.") as tracker:
            self.play(
                matrix_A.animate.scale(0.7)
            )
            self.play(
                Transform(matrix_A.copy(), matrix_A_small_top_left),
                Transform(matrix_A.copy(), matrix_A_small_top_right)
            )
        
        self.wait(0.5)
        
        with self.voiceover(text="And what happens when we apply one transformation after another? That leads us to composition.") as tracker:
            self.play(
                Write(mult_dot2),
                Write(matrix_B),
                Create(arrow_icon)
            )
        
        # ============================================
        # Final cleanup
        # ============================================
        self.wait(0.5)
        
        # Group everything for final fadeout
        all_objects = VGroup(
            domain_plane, codomain_plane, v_label, w_label,
            general_mapping_label, property_equations,
            i_hat, j_hat, i_label, j_label,
            vector_a, vector_b, a_label, b_label, a_text, b_text,
            map_i_to_a, map_j_to_b,
            matrix_A, matrix_A_small_top_left, matrix_A_small_top_right,
            mult_dot2, matrix_B, arrow_icon,
            decomposition_eq
        )
        
        self.play(*[FadeOut(obj) for obj in all_objects])
        self.wait(1)