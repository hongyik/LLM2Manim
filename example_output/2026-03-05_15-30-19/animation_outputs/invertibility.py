from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Colors from consistency ledger
        VECTOR_SPACE_PLANE_COLOR = LIGHT_GRAY
        INPUT_VECTOR_COLOR = BLUE_C
        OUTPUT_VECTOR_COLOR = BLUE_C
        MAPPING_ARROW_COLOR = "#00FF00"  # PURE_GREEN
        NUMERIC_MAPPING_COLOR = YELLOW
        GENERAL_LABEL_COLOR = WHITE
        HIGHLIGHT_COLOR = YELLOW
        SECOND_VECTOR_COLOR = "#C32148"  # MAROON_C
        SCALAR_COLOR = YELLOW
        KERNEL_LINE_COLOR = PURPLE_C
        IMAGE_REGION_COLOR = BLUE_C
        INVERSE_ARROW_COLOR = PINK
        
        # Create domain and codomain planes (V and W)
        domain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": VECTOR_SPACE_PLANE_COLOR, "stroke_opacity": 0.2},
            axis_config={"color": WHITE}
        ).move_to(np.array([-3.43, 0.70, 0]))
        
        codomain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": VECTOR_SPACE_PLANE_COLOR, "stroke_opacity": 0.2},
            axis_config={"color": WHITE}
        ).move_to(np.array([3.43, 0.70, 0]))
        
        # General mapping label
        general_mapping_label = MathTex(r"T: V \to W", color=GENERAL_LABEL_COLOR, font_size=36)
        general_mapping_label.move_to(np.array([0, 0.70, 0]))
        
        # Property equations (faint in top-left)
        property_equations = VGroup(
            MathTex(r"T(\vec{u}+\vec{v})=T(\vec{u})+T(\vec{v})", font_size=20),
            MathTex(r"T(c\vec{u})=cT(\vec{u})", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT)
        property_equations.set_opacity(0.3)
        property_equations.move_to(np.array([-5.5, 2.5, 0]))
        
        # Mapping arrow between planes
        mapping_arrow = Arrow(
            start=domain_plane.get_right(),
            end=codomain_plane.get_left(),
            color=MAPPING_ARROW_COLOR,
            buff=0.2
        )
        
        # ========== BEAT 1: Introduction to invertibility ==========
        with self.voiceover(text="We've seen how a linear transformation can collapse some vectors to zero and map others onto its image. This leads to a natural question: when is a linear transformation reversible?") as tracker:
            self.play(
                Create(domain_plane),
                Create(codomain_plane),
                Write(general_mapping_label),
                FadeIn(property_equations),
                Create(mapping_arrow)
            )
        
        self.wait(0.5)
        
        # Pulse the mapping label
        invertible_label = Text("Invertible", color=HIGHLIGHT_COLOR, font_size=36)
        invertible_label.move_to(np.array([0, 3.27, 0]))
        
        with self.voiceover(text="Now, let's explore invertibility") as tracker:
            # Add temporary T^{-1} hint
            inverse_hint = MathTex(r"T^{-1}", color=HIGHLIGHT_COLOR, font_size=32)
            inverse_hint.next_to(general_mapping_label, UP, buff=0.3)
            self.play(Write(inverse_hint))
            self.wait(0.5)
            self.play(FadeOut(inverse_hint))
            self.play(FadeIn(invertible_label, shift=UP))
        
        # ========== BEAT 2: Defining inverse transformation ==========
        self.wait(0.5)
        
        # Create vector x in V
        vector_x = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + np.array([2, 1, 0]),
            color=INPUT_VECTOR_COLOR,
            buff=0
        )
        vector_x_label = MathTex(r"\vec{x}", color=INPUT_VECTOR_COLOR, font_size=24)
        vector_x_label.next_to(vector_x.get_end(), UP+RIGHT, buff=0.1)
        
        # T(x) in W (image of (2,1) under A = [[1.5, -0.5], [0.5, 2]])
        # Compute A * [2, 1] = [1.5*2 + (-0.5)*1, 0.5*2 + 2*1] = [2.5, 3]
        vector_Tx = Arrow(
            start=codomain_plane.get_center(),
            end=codomain_plane.get_center() + np.array([2.5, 3, 0]),
            color=OUTPUT_VECTOR_COLOR,
            buff=0
        )
        vector_Tx_label = MathTex(r"T(\vec{x})", color=OUTPUT_VECTOR_COLOR, font_size=24)
        vector_Tx_label.next_to(vector_Tx.get_end(), UP+RIGHT, buff=0.1)
        
        # Inverse arrow from T(x) back to x
        inverse_arrow = Arrow(
            start=vector_Tx.get_end(),
            end=vector_x.get_end(),
            color=INVERSE_ARROW_COLOR,
            buff=0,
            stroke_width=3
        )
        
        # Undo equation
        undo_label = MathTex(r"T^{-1}(T(\vec{x})) = \vec{x}", color=GENERAL_LABEL_COLOR, font_size=28)
        undo_label.move_to(np.array([0, -2.0, 0]))
        
        with self.voiceover(text="A linear transformation T: V → W is invertible if there exists another linear transformation, called its inverse, that perfectly undoes T's action.") as tracker:
            self.play(Create(vector_x), Write(vector_x_label))
            self.play(GrowArrow(mapping_arrow.copy().set_opacity(0.7)))
            self.play(Create(vector_Tx), Write(vector_Tx_label))
            self.play(GrowArrow(inverse_arrow))
            self.play(
                Flash(vector_x, color=HIGHLIGHT_COLOR, line_length=0.3),
                vector_x.animate.set_color(HIGHLIGHT_COLOR)
            )
            self.play(Write(undo_label))
        
        # ========== BEAT 3: Formal definition ==========
        self.wait(0.5)
        
        # Clean up previous vectors
        self.play(
            FadeOut(vector_x), FadeOut(vector_x_label),
            FadeOut(vector_Tx), FadeOut(vector_Tx_label),
            FadeOut(inverse_arrow), FadeOut(undo_label)
        )
        
        # Inverse mapping label
        inverse_mapping_label = MathTex(r"T^{-1}: W \to V", color=GENERAL_LABEL_COLOR, font_size=28)
        inverse_mapping_label.next_to(general_mapping_label, DOWN, buff=0.5)
        
        # Composition equations
        comp_left = MathTex(r"T^{-1} \circ T = I_V", color=GENERAL_LABEL_COLOR, font_size=32)
        comp_right = MathTex(r"T \circ T^{-1} = I_W", color=GENERAL_LABEL_COLOR, font_size=32)
        
        comp_left.move_to(np.array([-2.5, -1.5, 0]))
        comp_right.move_to(np.array([2.5, -1.5, 0]))
        
        # Identity symbols
        I_V = MathTex(r"I_V", color=SCALAR_COLOR, font_size=32).move_to(comp_left[-2:])
        I_W = MathTex(r"I_W", color=SCALAR_COLOR, font_size=32).move_to(comp_right[-2:])
        
        with self.voiceover(text="Formally, an inverse T⁻¹ is a linear transformation from W back to V, such that composing T then T⁻¹ gives the identity on W, and T⁻¹ then T gives the identity on V.") as tracker:
            self.play(FadeIn(inverse_mapping_label, shift=DOWN))
            self.play(Write(comp_left), Write(comp_right))
            self.play(
                Flash(I_V, color=SCALAR_COLOR),
                Flash(I_W, color=SCALAR_COLOR)
            )
        
        # ========== BEAT 4: Kernel and image conditions ==========
        self.wait(0.5)
        
        # Kernel: trivial (just a dot)
        kernel_dot = Dot(radius=0.08, color=KERNEL_LINE_COLOR)
        kernel_dot.move_to(domain_plane.get_center())
        kernel_label = MathTex(r"\text{Ker}(T) = \{\vec{0}\}", color=HIGHLIGHT_COLOR, font_size=28)
        kernel_label.next_to(kernel_dot, DOWN, buff=0.5)
        
        # Image: entire W plane
        image_region = Rectangle(
            width=codomain_plane.width,
            height=codomain_plane.height,
            color=IMAGE_REGION_COLOR,
            fill_opacity=0.2,
            stroke_width=2
        )
        image_region.move_to(codomain_plane.get_center())
        image_label = MathTex(r"\text{Im}(T) = W", color=HIGHLIGHT_COLOR, font_size=28)
        image_label.move_to(codomain_plane.get_center())
        
        # Rank-nullity theorem
        rn_theorem = MathTex(r"\dim(V) = \text{nullity} + \text{rank}", color=GENERAL_LABEL_COLOR, font_size=24)
        rn_theorem.move_to(np.array([5.0, 2.5, 0]))
        rn_example = MathTex(r"2 = 0 + 2", color=SCALAR_COLOR, font_size=24)
        rn_example.next_to(rn_theorem, DOWN, buff=0.3)
        
        with self.voiceover(text="When does such an inverse exist? It requires T to be both one-to-one and onto. In the language of kernel and image: the kernel must be trivial, and the image must be all of W.") as tracker:
            self.play(Create(kernel_dot), Write(kernel_label))
            self.play(FadeIn(image_region), Write(image_label))
            self.play(
                Flash(kernel_label, color=HIGHLIGHT_COLOR),
                Flash(image_label, color=HIGHLIGHT_COLOR)
            )
            self.play(Write(rn_theorem), Write(rn_example))
        
        # ========== BEAT 5: Matrix representation ==========
        self.wait(0.5)
        
        # Clean up previous labels
        self.play(
            FadeOut(inverse_mapping_label),
            FadeOut(comp_left), FadeOut(comp_right),
            FadeOut(kernel_dot), FadeOut(kernel_label),
            FadeOut(image_region), FadeOut(image_label),
            FadeOut(rn_theorem), FadeOut(rn_example)
        )
        
        # Matrix A
        matrix_A = Matrix(
            [[1.5, -0.5], [0.5, 2]],
            color=GENERAL_LABEL_COLOR,
            element_alignment_corner=DOWN
        )
        matrix_A_label = MathTex(r"A", font_size=24).next_to(matrix_A, UP, buff=0.2)
        matrix_A.move_to(np.array([-2.0, -2.0, 0]))
        matrix_A_label.move_to(matrix_A.get_center() + UP*0.5)
        
        # Inverse matrix A^{-1} (approximate values)
        matrix_A_inv = Matrix(
            [[0.615, 0.154], [-0.154, 0.462]],
            color=HIGHLIGHT_COLOR,
            element_alignment_corner=DOWN
        )
        matrix_A_inv_label = MathTex(r"A^{-1}", color=HIGHLIGHT_COLOR, font_size=24).next_to(matrix_A_inv, UP, buff=0.2)
        matrix_A_inv.move_to(np.array([2.0, -2.0, 0]))
        matrix_A_inv_label.move_to(matrix_A_inv.get_center() + UP*0.5)
        
        # Matrix equations
        matrix_eq1 = MathTex(r"A A^{-1} = I", color=GENERAL_LABEL_COLOR, font_size=32)
        matrix_eq2 = MathTex(r"A^{-1} A = I", color=GENERAL_LABEL_COLOR, font_size=32)
        matrix_eq1.move_to(np.array([0, -1.0, 0]))
        matrix_eq2.next_to(matrix_eq1, DOWN, buff=0.5)
        
        # Identity matrix
        I_matrix = Matrix([[1, 0], [0, 1]], color=SCALAR_COLOR)
        I_matrix.move_to(matrix_eq1.get_right() + RIGHT*1.5)
        
        with self.voiceover(text="Now, recall the matrix representation. If T is represented by a matrix A, then applying T is multiplying by A. The inverse transformation T⁻¹, if it exists, must correspond to multiplying by a matrix that undoes A—the inverse matrix A⁻¹.") as tracker:
            self.play(FadeIn(matrix_A, shift=UP), Write(matrix_A_label))
            self.play(FadeIn(matrix_A_inv, shift=UP), Write(matrix_A_inv_label))
            self.play(Write(matrix_eq1), Write(matrix_eq2))
            self.play(
                Flash(I_matrix, color=SCALAR_COLOR),
                FadeIn(I_matrix)
            )
        
        # ========== BEAT 6: Determinant condition ==========
        self.wait(0.5)
        
        # Determinant bracket around A
        det_bracket = SurroundingRectangle(matrix_A, color=WHITE, buff=0.2)
        det_label = MathTex(r"\det(A) \neq 0", color=SCALAR_COLOR, font_size=28)
        det_label.next_to(matrix_A, DOWN, buff=0.8)
        
        # Determinant calculation
        det_calc = MathTex(
            r"\det\begin{bmatrix}1.5 & -0.5\\0.5 & 2\end{bmatrix} = (1.5)(2) - (-0.5)(0.5) = 3.25",
            color=SCALAR_COLOR,
            font_size=24
        )
        det_calc.next_to(det_label, DOWN, buff=0.5)
        
        with self.voiceover(text="Therefore, a linear transformation T is invertible if and only if its matrix A is an invertible or non-singular square matrix. This requires the determinant of A to be non-zero.") as tracker:
            self.play(Create(det_bracket))
            self.play(Write(det_label))
            self.play(Transform(det_label, det_calc))
            self.play(Flash(det_calc[-3:], color=HIGHLIGHT_COLOR))
        
        # ========== BEAT 7: Geometric interpretation ==========
        self.wait(0.5)
        
        # Clean up matrices and determinant
        self.play(
            FadeOut(matrix_A_inv), FadeOut(matrix_A_inv_label),
            FadeOut(matrix_eq1), FadeOut(matrix_eq2),
            FadeOut(I_matrix),
            FadeOut(det_bracket)
        )
        
        # Basis vectors in V
        basis_i = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + np.array([1, 0, 0]),
            color=INPUT_VECTOR_COLOR,
            buff=0,
            stroke_width=3
        )
        basis_i_label = MathTex(r"\hat{i}", color=INPUT_VECTOR_COLOR, font_size=20)
        basis_i_label.next_to(basis_i.get_end(), RIGHT, buff=0.1)
        
        basis_j = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + np.array([0, 1, 0]),
            color=SECOND_VECTOR_COLOR,
            buff=0,
            stroke_width=3
        )
        basis_j_label = MathTex(r"\hat{j}", color=SECOND_VECTOR_COLOR, font_size=20)
        basis_j_label.next_to(basis_j.get_end(), UP, buff=0.1)
        
        # Images of basis vectors in W (columns of A)
        image_a = Arrow(
            start=codomain_plane.get_center(),
            end=codomain_plane.get_center() + np.array([1.5, 0.5, 0]),
            color=INPUT_VECTOR_COLOR,
            buff=0,
            stroke_width=3
        )
        image_a_label = MathTex(r"T(\hat{i})", color=INPUT_VECTOR_COLOR, font_size=20)
        image_a_label.next_to(image_a.get_end(), RIGHT, buff=0.1)
        
        image_b = Arrow(
            start=codomain_plane.get_center(),
            end=codomain_plane.get_center() + np.array([-0.5, 2, 0]),
            color=SECOND_VECTOR_COLOR,
            buff=0,
            stroke_width=3
        )
        image_b_label = MathTex(r"T(\hat{j})", color=SECOND_VECTOR_COLOR, font_size=20)
        image_b_label.next_to(image_b.get_end(), LEFT, buff=0.1)
        
        # Parallelogram formed by T(i) and T(j)
        parallelogram = Polygon(
            codomain_plane.get_center(),
            codomain_plane.get_center() + np.array([1.5, 0.5, 0]),
            codomain_plane.get_center() + np.array([1, 2.5, 0]),  # T(i) + T(j)
            codomain_plane.get_center() + np.array([-0.5, 2, 0]),
            color=IMAGE_REGION_COLOR,
            fill_opacity=0.2,
            stroke_width=2
        )
        
        area_label = MathTex(r"\text{Area} = |\det(A)|", color=SCALAR_COLOR, font_size=24)
        area_label.next_to(parallelogram, RIGHT, buff=0.5)
        
        with self.voiceover(text="Geometrically, a non-zero determinant means the transformation preserves the dimension of the space—it doesn't collapse it into a lower dimension. Our basis vectors T(i-hat) and T(j-hat) must be linearly independent, spanning all of W.") as tracker:
            self.play(Create(basis_i), Write(basis_i_label))
            self.play(Create(basis_j), Write(basis_j_label))
            self.play(Create(image_a), Write(image_a_label))
            self.play(Create(image_b), Write(image_b_label))
            self.play(FadeIn(parallelogram))
            self.play(Write(area_label))
        
        # ========== BEAT 8: Singular (non-invertible) example ==========
        self.wait(0.5)
        
        # Transform to singular matrix
        singular_matrix = Matrix(
            [[1, 2], [2, 4]],
            color=GENERAL_LABEL_COLOR,
            element_alignment_corner=DOWN
        )
        singular_matrix.move_to(matrix_A.get_center())
        
        zero_det = MathTex(r"1\cdot4 - 2\cdot2 = 0", color=NUMERIC_MAPPING_COLOR, font_size=24)
        zero_det.next_to(singular_matrix, DOWN, buff=0.8)
        
        # Show that inverse doesn't exist
        not_exists = MathTex(r"\nexists", color=RED, font_size=36)
        not_exists.move_to(matrix_A_inv.get_center())
        
        # Make image vectors collinear
        image_b_collinear = Arrow(
            start=codomain_plane.get_center(),
            end=codomain_plane.get_center() + np.array([2, 4, 0]),  # 2 * T(i) = 2 * (1.5, 0.5) = (3, 1) but using new matrix
            color=SECOND_VECTOR_COLOR,
            buff=0,
            stroke_width=3
        )
        image_b_collinear_label = MathTex(r"T(\hat{j})", color=SECOND_VECTOR_COLOR, font_size=20)
        image_b_collinear_label.next_to(image_b_collinear.get_end(), UP, buff=0.1)
        
        with self.voiceover(text="If the determinant were zero, the matrix would not be invertible. The transformation would collapse space, its kernel would be non-trivial, and it could not be reversed.") as tracker:
            self.play(Transform(matrix_A, singular_matrix))
            self.play(Transform(det_label, zero_det))
            self.play(Flash(zero_det[-1:], color=NUMERIC_MAPPING_COLOR))
            self.play(
                Transform(image_b, image_b_collinear),
                Transform(image_b_label, image_b_collinear_label)
            )
            self.play(FadeIn(not_exists))
            self.play(
                parallelogram.animate.set_fill(opacity=0.05),
                area_label.animate.set_opacity(0.3)
            )
        
        # ========== BEAT 9: Return to invertible case ==========
        self.wait(0.5)
        
        # Restore invertible matrix
        matrix_A_restored = Matrix(
            [[1.5, -0.5], [0.5, 2]],
            color=GENERAL_LABEL_COLOR,
            element_alignment_corner=DOWN
        )
        matrix_A_restored.move_to(matrix_A.get_center())
        
        matrix_A_inv_restored = Matrix(
            [[0.615, 0.154], [-0.154, 0.462]],
            color=HIGHLIGHT_COLOR,
            element_alignment_corner=DOWN
        )
        matrix_A_inv_restored.move_to(matrix_A_inv.get_center())
        
        # Double-headed bijective arrow
        bijective_arrow = DoubleArrow(
            start=domain_plane.get_right(),
            end=codomain_plane.get_left(),
            color=MAPPING_ARROW_COLOR,
            buff=0.2,
            stroke_width=3
        )
        
        with self.voiceover(text="Invertibility is a powerful concept. It tells us when a system of linear equations has a unique solution, and when a transformation can be undone without loss of information.") as tracker:
            self.play(
                FadeOut(singular_matrix),
                FadeOut(zero_det),
                FadeOut(not_exists),
                FadeOut(image_b_collinear),
                FadeOut(image_b_collinear_label),
                FadeOut(parallelogram),
                FadeOut(area_label)
            )
            self.play(
                FadeIn(matrix_A_restored),
                FadeIn(matrix_A_inv_restored)
            )
            self.play(Transform(mapping_arrow, bijective_arrow))
        
        # ========== BEAT 10: Final clean-up ==========
        self.wait(0.5)
        
        # Fade out everything except planes and main label
        all_mobjects = VGroup(*self.mobjects)
        to_keep = VGroup(domain_plane, codomain_plane, general_mapping_label)
        to_fade = VGroup()
        
        for mob in self.mobjects:
            if mob not in [domain_plane, codomain_plane, general_mapping_label]:
                to_fade.add(mob)
        
        bijective_label = MathTex(r"T: V \leftrightarrow W", color=HIGHLIGHT_COLOR, font_size=36)
        bijective_label.move_to(general_mapping_label.get_center())
        
        with self.voiceover(text="We've now covered the core ideas of linear transformations: from definition and visualization, to matrices, composition, subspaces, and invertibility.") as tracker:
            self.play(FadeOut(to_fade))
            self.play(Transform(general_mapping_label, bijective_label))
        
        # ========== BEAT 11: Hold for final summary ==========
        self.wait(0.5)
        
        with self.voiceover(text="Let's bring it all together in a final summary.") as tracker:
            self.play(*[Flash(mob, color=HIGHLIGHT_COLOR, line_length=0.2) 
                       for mob in [domain_plane, codomain_plane, general_mapping_label]])
        
        self.wait(2)