from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # ============================================================================
        # INITIAL STATE: Two dimmed planes, matrices A and B with dot, property equations
        # ============================================================================
        
        # Create two planes (from Step 4) - initially dimmed
        domain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": LIGHT_GRAY, "stroke_opacity": 0.2, "stroke_width": 1},
            axis_config={"color": LIGHT_GRAY, "stroke_opacity": 0.3}
        ).move_to(np.array([-2.5, 0, 0]))
        
        codomain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": LIGHT_GRAY, "stroke_opacity": 0.2, "stroke_width": 1},
            axis_config={"color": LIGHT_GRAY, "stroke_opacity": 0.3}
        ).move_to(np.array([2.5, 0, 0]))
        
        two_planes = VGroup(domain_plane, codomain_plane)
        
        # Matrix A (from Step 4)
        matrix_A_data = [[2, 1], [1, 3]]
        matrix_A = Matrix(
            matrix_A_data,
            v_buff=0.8,
            h_buff=1.2,
            bracket_h_buff=0.1,
            bracket_v_buff=0.2,
            element_to_mobject_config={"color": WHITE}
        ).move_to(np.array([0, 0, 0]))
        matrix_A.set_color(WHITE)
        matrix_A_label = MathTex(r"A = [T(\hat{i})\ T(\hat{j})]", font_size=24, color=WHITE)
        matrix_A_label.next_to(matrix_A, DOWN, buff=0.3)
        
        # Matrix B (styled like A)
        matrix_B_data = [[1, -1], [2, 0]]
        matrix_B = Matrix(
            matrix_B_data,
            v_buff=0.8,
            h_buff=1.2,
            bracket_h_buff=0.1,
            bracket_v_buff=0.2,
            element_to_mobject_config={"color": WHITE}
        ).move_to(np.array([3.5, 0, 0]))
        matrix_B.set_color(WHITE)
        
        # Dot between matrices
        dot_label = MathTex(r"\cdot", font_size=48, color=WHITE)
        dot_label.move_to(np.array([1.75, 0, 0]))
        
        # Property equations (faint)
        property_equations = MathTex(
            r"T(u+v)=T(u)+T(v)", r"\quad", r"T(cu)=cT(u)",
            font_size=24,
            color=WHITE
        )
        property_equations.set_opacity(0.3)
        property_equations.move_to(np.array([-5.5, 3.0, 0]))
        
        # Group everything for initial state
        initial_group = VGroup(two_planes, matrix_A, matrix_A_label, matrix_B, dot_label, property_equations)
        
        # Beat 0: "We now understand..." (0:00-0:08)
        # ----------------------------------------------------------------------------
        with self.voiceover(text="We now understand that a linear transformation can be represented by a matrix.") as tracker:
            self.play(FadeIn(two_planes))
        
        # Create third plane U (further left)
        plane_U = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": LIGHT_GRAY, "stroke_opacity": 0.2, "stroke_width": 1},
            axis_config={"color": LIGHT_GRAY, "stroke_opacity": 0.3}
        ).move_to(np.array([-7.5, 0, 0]))
        
        # Labels for planes
        label_U = MathTex(r"U = \mathbb{R}^2", font_size=24, color=WHITE)
        label_U.move_to(np.array([-7.5, 2.5, 0]))
        
        label_V = MathTex(r"V = \mathbb{R}^2", font_size=24, color=WHITE)
        label_V.move_to(np.array([-2.5, 2.5, 0]))
        
        label_W = MathTex(r"W = \mathbb{R}^2", font_size=24, color=WHITE)
        label_W.move_to(np.array([2.5, 2.5, 0]))
        
        # Mapping arrows
        arrow_S = Arrow(
            start=plane_U.get_right() + LEFT * 0.2,
            end=domain_plane.get_left() + RIGHT * 0.2,
            color=GREEN,
            buff=0.1,
            stroke_width=3
        )
        arrow_S.move_to(np.array([-5, 0, 0]))
        
        arrow_T = Arrow(
            start=domain_plane.get_right() + LEFT * 0.2,
            end=codomain_plane.get_left() + RIGHT * 0.2,
            color=GREEN,
            buff=0.1,
            stroke_width=3
        )
        arrow_T.move_to(np.array([0, 0, 0]))
        
        arrow_composite = DashedLine(
            start=plane_U.get_right() + LEFT * 0.2,
            end=codomain_plane.get_left() + RIGHT * 0.2,
            color=GREEN,
            stroke_width=3
        )
        arrow_composite.move_to(np.array([-2.5, 0, 0]))
        
        # Mapping labels
        label_S = MathTex(r"S: U \to V", font_size=20, color=WHITE)
        label_S.next_to(arrow_S, UP, buff=0.1)
        
        label_T = MathTex(r"T: V \to W", font_size=20, color=WHITE)
        label_T.next_to(arrow_T, UP, buff=0.1)
        
        label_composite = MathTex(r"T \circ S", font_size=24, color=YELLOW)
        label_composite.next_to(arrow_composite, DOWN, buff=0.2)
        
        with self.voiceover(text="But what happens when we apply two transformations in sequence? This is called composition.") as tracker:
            self.play(FadeIn(plane_U), Write(label_U))
            self.play(Transform(label_V.copy().clear_updaters(), label_V))  # Relabel V
            self.play(Create(arrow_S), Write(label_S))
            self.play(Create(arrow_T), Write(label_T))
            self.play(Create(arrow_composite), Write(label_composite))
        
        self.wait(0.5)
        
        # Beat 1: "Suppose we have a transformation S..." (0:08-0:18)
        # ----------------------------------------------------------------------------
        # Vector x on U
        vec_x = Arrow(
            start=plane_U.c2p(0, 0, 0),
            end=plane_U.c2p(1, 2, 0),
            color=BLUE_C,
            buff=0,
            stroke_width=4
        )
        label_x = MathTex(r"\vec{x}", font_size=20, color=BLUE_C)
        label_x.next_to(vec_x.get_end(), RIGHT, buff=0.1)
        
        # S(x) on V
        vec_Sx = Arrow(
            start=domain_plane.c2p(0, 0, 0),
            end=domain_plane.c2p(1.5, 2.5, 0),  # S(1,2) = (1.5, 2.5) approx
            color=BLUE_C,
            buff=0,
            stroke_width=4
        )
        
        # T(S(x)) on W
        vec_TSx = Arrow(
            start=codomain_plane.c2p(0, 0, 0),
            end=codomain_plane.c2p(3, 4, 0),  # T(S(1,2)) approx
            color=BLUE_C,
            buff=0,
            stroke_width=4
        )
        
        # Composite equation
        eq_composite_action = MathTex(
            r"(T \circ S)(\vec{x}) = T(S(\vec{x}))",
            font_size=28,
            color=WHITE
        )
        eq_composite_action.move_to(np.array([0, -2.5, 0]))
        
        with self.voiceover(text="Suppose we have a transformation S from space U to V, followed by a transformation T from V to W.") as tracker:
            self.play(FadeIn(vec_x), Write(label_x))
        
        self.wait(0.5)
        
        with self.voiceover(text="The composition, denoted T circle S, maps directly from U to W by applying S first, then T.") as tracker:
            # Show S mapping
            arrow_S_copy = arrow_S.copy().set_color(GREEN).set_opacity(0.7)
            self.play(GrowArrow(arrow_S_copy), run_time=1.5)
            self.play(FadeIn(vec_Sx))
            self.play(FadeOut(arrow_S_copy))
            
            # Show T mapping
            arrow_T_copy = arrow_T.copy().set_color(GREEN).set_opacity(0.7)
            self.play(GrowArrow(arrow_T_copy), run_time=1.5)
            self.play(FadeIn(vec_TSx))
            self.play(FadeOut(arrow_T_copy))
            
            # Pulse composite arrow and show equation
            self.play(
                arrow_composite.animate.set_stroke(width=5, opacity=1).set_color(YELLOW),
                Write(eq_composite_action)
            )
            self.play(
                arrow_composite.animate.set_stroke(width=3, opacity=1).set_color(GREEN),
            )
        
        self.wait(0.5)
        
        # Beat 2: "Crucially, if both S and T are linear..." (0:18-0:30)
        # ----------------------------------------------------------------------------
        # Create two vectors u and v from x
        vec_u = Arrow(
            start=plane_U.c2p(0, 0, 0),
            end=plane_U.c2p(1, 1, 0),
            color=BLUE_C,
            buff=0,
            stroke_width=4
        )
        vec_v = Arrow(
            start=plane_U.c2p(0, 0, 0),
            end=plane_U.c2p(0.5, 1.5, 0),
            color=MAROON_C,
            buff=0,
            stroke_width=4
        )
        
        # Step equations for additivity
        step_equations = MathTex(
            r"(T\circ S)(u+v) = T(S(u+v)) = T(S(u)+S(v)) = T(S(u)) + T(S(v))",
            font_size=20,
            color=WHITE
        )
        step_equations.move_to(np.array([0, -3.5, 0]))
        
        with self.voiceover(text="Crucially, if both S and T are linear, then their composition T∘S is also linear.") as tracker:
            self.play(property_equations.animate.set_opacity(1))
            self.play(Flash(property_equations, color=YELLOW, flash_radius=1.2))
        
        self.wait(0.5)
        
        with self.voiceover(text="The properties of additivity and homogeneity carry through.") as tracker:
            # Transform x into u and v
            self.play(
                Transform(vec_x, vec_u),
                FadeIn(vec_v, shift=RIGHT*0.5)
            )
            
            # Show mapping of u+v through S and T (simplified)
            arrow_S_flash = ShowPassingFlash(
                arrow_S.copy().set_stroke(width=6, color=GREEN, opacity=0.8),
                time_width=1.5,
                run_time=2
            )
            arrow_T_flash = ShowPassingFlash(
                arrow_T.copy().set_stroke(width=6, color=GREEN, opacity=0.8),
                time_width=1.5,
                run_time=2
            )
            self.play(arrow_S_flash, arrow_T_flash)
            
            # Show step equations
            self.play(Write(step_equations))
        
        self.wait(0.5)
        
        # Clean up vectors and equations
        self.play(
            FadeOut(vec_x), FadeOut(vec_v), FadeOut(vec_Sx), FadeOut(vec_TSx),
            FadeOut(label_x), FadeOut(eq_composite_action), FadeOut(step_equations)
        )
        
        # Beat 3: "Now, since S and T are linear..." (0:30-0:45)
        # ----------------------------------------------------------------------------
        # Move matrix A under T label
        new_matrix_A_pos = np.array([0, -1.5, 0])
        new_label_A_pos = np.array([0, -2.3, 0])
        
        # Create matrix B label
        matrix_B_label = MathTex(r"B = [S(\hat{i})\ S(\hat{j})]", font_size=24, color=WHITE)
        matrix_B_label.next_to(matrix_B, DOWN, buff=0.3)
        
        # Basis vectors on U
        vec_i = Arrow(
            start=plane_U.c2p(0, 0, 0),
            end=plane_U.c2p(1, 0, 0),
            color=BLUE_C,
            buff=0,
            stroke_width=4
        )
        vec_j = Arrow(
            start=plane_U.c2p(0, 0, 0),
            end=plane_U.c2p(0, 1, 0),
            color=MAROON_C,
            buff=0,
            stroke_width=4
        )
        
        with self.voiceover(text="Now, since S and T are linear, they have matrix representations.") as tracker:
            self.play(
                matrix_A.animate.move_to(new_matrix_A_pos),
                matrix_A_label.animate.move_to(new_label_A_pos)
            )
        
        self.wait(0.5)
        
        with self.voiceover(text="Let A be the matrix for T, and B be the matrix for S.") as tracker:
            self.play(FadeIn(matrix_B_label))
            self.play(FadeIn(vec_i), FadeIn(vec_j))
        
        self.wait(0.5)
        
        # Beat 4: "What is the matrix for the composition T∘S?" (0:45-1:00)
        # ----------------------------------------------------------------------------
        # Highlight first column of B
        first_col_box = SurroundingRectangle(
            matrix_B.get_columns()[0],
            color=YELLOW,
            buff=0.1,
            stroke_width=2
        )
        
        label_Si_col = MathTex(
            r"S(\hat{i}) = \text{first column of } B",
            font_size=20,
            color=YELLOW
        )
        label_Si_col.next_to(matrix_B, RIGHT, buff=1.0)
        
        with self.voiceover(text="What is the matrix for the composition T∘S? It is given by the product of their matrices: A times B. Let's see why.") as tracker:
            self.play(FadeOut(vec_j))  # Reduce clutter
            self.play(Indicate(vec_i, color=YELLOW, scale_factor=1.3))
        
        self.wait(0.5)
        
        with self.voiceover(text="Focus on i-hat.") as tracker:
            # Show S mapping i-hat
            arrow_S_i = GrowArrow(
                Arrow(
                    start=vec_i.get_end(),
                    end=domain_plane.c2p(1, 2, 0),  # S(i-hat) = first col of B
                    color=GREEN,
                    buff=0,
                    stroke_width=3
                ),
                run_time=1.5
            )
            self.play(arrow_S_i)
            
            # Highlight first column of B
            self.play(Create(first_col_box), Write(label_Si_col))
        
        self.wait(0.5)
        
        # Beat 5: "But applying T to S(i-hat)..." (1:00-1:15)
        # ----------------------------------------------------------------------------
        # Show T mapping S(i-hat)
        eq_T_S_i = MathTex(
            r"(T \circ S)(\hat{i}) = A \times (\text{Column 1 of } B)",
            font_size=20,
            color=YELLOW
        )
        eq_T_S_i.move_to(np.array([0, -3.0, 0]))
        
        # Extract first column as vector
        col1_vector = Matrix(
            [[1], [2]],  # First column of B
            v_buff=0.8,
            h_buff=1.2,
            bracket_h_buff=0.1,
            bracket_v_buff=0.2,
            element_to_mobject_config={"color": YELLOW}
        ).scale(0.8)
        col1_vector.next_to(matrix_A, LEFT, buff=0.5)
        
        # Matrix-vector multiplication animation
        mult_result = Matrix(
            [[4], [7]],  # A * first column of B
            v_buff=0.8,
            h_buff=1.2,
            bracket_h_buff=0.1,
            bracket_v_buff=0.2,
            element_to_mobject_config={"color": BLUE_C}
        ).scale(0.8)
        mult_result.next_to(matrix_A, RIGHT, buff=0.5)
        
        mult_dot = MathTex(r"\cdot", font_size=36, color=WHITE)
        mult_dot.move_to(np.array([-0.5, 0, 0]))
        
        mult_group = VGroup(col1_vector, mult_dot, matrix_A.copy(), MathTex(r"=", font_size=36), mult_result)
        mult_group.arrange(RIGHT, buff=0.3).move_to(np.array([0, -2.0, 0]))
        
        with self.voiceover(text="But applying T to S(i-hat) is just multiplying matrix A by the vector S(i-hat). And S(i-hat) is the first column of B.") as tracker:
            # Show T mapping arrow
            arrow_T_Si = GrowArrow(
                Arrow(
                    start=domain_plane.c2p(1, 2, 0),
                    end=codomain_plane.c2p(4, 7, 0),  # T(S(i-hat)) approx
                    color=GREEN,
                    buff=0,
                    stroke_width=3
                ),
                run_time=1.5
            )
            self.play(arrow_T_Si)
            self.play(Write(eq_T_S_i))
        
        self.wait(0.5)
        
        with self.voiceover(text="So the result is A times the first column of B.") as tracker:
            # Show matrix-vector multiplication
            self.play(
                Transform(matrix_A.copy(), mult_group[2]),
                FadeIn(col1_vector),
                FadeIn(mult_dot),
                FadeIn(mult_group[3]),
                FadeIn(mult_result)
            )
        
        self.wait(0.5)
        
        # Beat 6: "Similarly, for j-hat..." (1:15-1:30)
        # ----------------------------------------------------------------------------
        # Bring back j-hat and repeat for second column
        vec_j_return = vec_j.copy()
        second_col_box = SurroundingRectangle(
            matrix_B.get_columns()[1],
            color=MAROON_C,
            buff=0.1,
            stroke_width=2
        )
        
        eq_T_S_j = MathTex(
            r"(T \circ S)(\hat{j}) = A \times (\text{Column 2 of } B)",
            font_size=20,
            color=MAROON_C
        )
        eq_T_S_j.move_to(np.array([0, -3.5, 0]))
        
        # Build matrix C from columns
        matrix_C_data = [[4, -2], [7, -1]]  # A * B
        matrix_C = Matrix(
            matrix_C_data,
            v_buff=0.8,
            h_buff=1.2,
            bracket_h_buff=0.1,
            bracket_v_buff=0.2,
            element_to_mobject_config={"color": YELLOW}
        )
        matrix_C.set_color(YELLOW)
        matrix_C.move_to(np.array([0, 1.5, 0]))
        
        # Matrix multiplication equation
        eq_C_equals_AB = MathTex(
            r"C = A B",
            font_size=36,
            color=WHITE
        )
        eq_C_equals_AB.move_to(np.array([0, 0.5, 0]))
        
        with self.voiceover(text="Similarly, for j-hat, (T∘S)(j-hat) equals A times the second column of B.") as tracker:
            self.play(FadeIn(vec_j_return))
            self.play(Indicate(vec_j_return, color=MAROON_C, scale_factor=1.3))
            self.play(Create(second_col_box))
            self.play(Write(eq_T_S_j))
        
        self.wait(0.5)
        
        with self.voiceover(text="Therefore, the matrix for T∘S has columns A times col1 of B and A times col2 of B. This is exactly the definition of the matrix product A times B.") as tracker:
            # Build matrix C column by column
            col1_C = matrix_C.get_columns()[0].copy()
            col2_C = matrix_C.get_columns()[1].copy()
            
            col1_C.set_opacity(0)
            col2_C.set_opacity(0)
            
            self.add(matrix_C)
            self.play(col1_C.animate.set_opacity(1))
            self.wait(0.3)
            self.play(col2_C.animate.set_opacity(1))
            
            # Show full matrix multiplication
            self.play(Write(eq_C_equals_AB))
            
            # Animate dot product computation for one entry
            entry_highlight = SurroundingRectangle(
                matrix_C.get_entries()[0],  # Top-left entry
                color=YELLOW,
                buff=0.05,
                stroke_width=2
            )
            self.play(Create(entry_highlight))
            self.play(FadeOut(entry_highlight))
        
        self.wait(0.5)
        
        # Clean up intermediate objects
        self.play(
            FadeOut(first_col_box), FadeOut(second_col_box),
            FadeOut(label_Si_col), FadeOut(eq_T_S_i), FadeOut(eq_T_S_j),
            FadeOut(mult_group), FadeOut(vec_i), FadeOut(vec_j_return)
        )
        
        # Beat 7: "The order matters..." (1:30-1:40)
        # ----------------------------------------------------------------------------
        # Swap matrices to show non-commutativity
        swapped_A_pos = matrix_B.get_center()
        swapped_B_pos = matrix_A.get_center()
        
        not_equal = MathTex(r"\neq", font_size=48, color=RED)
        not_equal.move_to(np.array([0, -1.5, 0]))
        
        with self.voiceover(text="The order matters: A times B represents applying B first, then A.") as tracker:
            # Swap positions
            self.play(
                matrix_A.animate.move_to(swapped_A_pos),
                matrix_B.animate.move_to(swapped_B_pos),
                run_time=1.5
            )
            self.play(Write(not_equal))
            self.play(Flash(not_equal, color=RED, flash_radius=0.8))
            
            # Return to correct order and pulse
            self.play(
                matrix_A.animate.move_to(new_matrix_A_pos),
                matrix_B.animate.move_to(np.array([3.5, 0, 0])),
                FadeOut(not_equal)
            )
            self.play(
                eq_C_equals_AB.animate.set_color(YELLOW).scale(1.2),
                run_time=0.5
            )
            self.play(
                eq_C_equals_AB.animate.set_color(WHITE).scale(1/1.2),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # Beat 8: "This correspondence is a cornerstone..." (1:40-1:50)
        # ----------------------------------------------------------------------------
        with self.voiceover(text="This correspondence is a cornerstone of linear algebra. It allows us to analyze complex transformations by breaking them down and multiplying their matrices.") as tracker:
            # Fade out planes
            self.play(
                FadeOut(plane_U), FadeOut(domain_plane), FadeOut(codomain_plane),
                FadeOut(label_U), FadeOut(label_V), FadeOut(label_W),
                FadeOut(arrow_S), FadeOut(arrow_T), FadeOut(arrow_composite),
                FadeOut(label_S), FadeOut(label_T), FadeOut(label_composite),
                FadeOut(property_equations)
            )
            
            # Bring matrices to center and show arrows
            self.play(
                matrix_A.animate.move_to(np.array([-2, 0, 0])),
                matrix_B.animate.move_to(np.array([0, 0, 0])),
                matrix_C.animate.move_to(np.array([2, 0, 0])),
                matrix_A_label.animate.move_to(np.array([-2, -1, 0])),
                matrix_B_label.animate.move_to(np.array([0, -1, 0])),
                eq_C_equals_AB.animate.move_to(np.array([0, 1, 0]))
            )
            
            # Show arrows between matrices
            arrow_AB = Arrow(
                start=matrix_A.get_right(),
                end=matrix_B.get_left(),
                color=GREEN,
                buff=0.2,
                stroke_width=3
            )
            arrow_BC = Arrow(
                start=matrix_B.get_right(),
                end=matrix_C.get_left(),
                color=GREEN,
                buff=0.2,
                stroke_width=3
            )
            arrow_AC = DashedLine(
                start=matrix_A.get_top() + UP * 0.2,
                end=matrix_C.get_top() + UP * 0.2,
                color=YELLOW,
                stroke_width=2
            )
            
            self.play(Create(arrow_AB))
            self.play(Create(arrow_BC))
            self.play(Create(arrow_AC))
        
        self.wait(0.5)
        
        # Beat 9: "Next, we'll look at two fundamental subspaces..." (1:50-1:55)
        # ----------------------------------------------------------------------------
        with self.voiceover(text="Next, we'll look at two fundamental subspaces linked to any linear transformation: its kernel and image.") as tracker:
            # Fade out matrices
            self.play(
                FadeOut(matrix_A), FadeOut(matrix_B), FadeOut(matrix_C),
                FadeOut(matrix_A_label), FadeOut(matrix_B_label),
                FadeOut(eq_C_equals_AB),
                FadeOut(arrow_AB), FadeOut(arrow_BC), FadeOut(arrow_AC)
            )
            
            # Bring back two planes (empty)
            domain_plane_clean = NumberPlane(
                x_range=[-5, 5, 1],
                y_range=[-3, 3, 1],
                background_line_style={"stroke_color": LIGHT_GRAY, "stroke_opacity": 0.3, "stroke_width": 1},
                axis_config={"color": LIGHT_GRAY}
            ).move_to(np.array([-3, 0, 0]))
            
            codomain_plane_clean = NumberPlane(
                x_range=[-5, 5, 1],
                y_range=[-3, 3, 1],
                background_line_style={"stroke_color": LIGHT_GRAY, "stroke_opacity": 0.3, "stroke_width": 1},
                axis_config={"color": LIGHT_GRAY}
            ).move_to(np.array([3, 0, 0]))
            
            general_mapping_label = MathTex(r"T: V \to W", font_size=32, color=WHITE)
            general_mapping_label.move_to(np.array([0, 2.5, 0]))
            
            # Gentle arrow pointing right
            arrow_icon = Arrow(
                start=np.array([5, 0, 0]),
                end=np.array([6.5, 0, 0]),
                color=WHITE,
                buff=0,
                stroke_width=2
            )
            
            self.play(
                FadeIn(domain_plane_clean),
                FadeIn(codomain_plane_clean),
                Write(general_mapping_label)
            )
            self.play(Create(arrow_icon))
        
        self.wait(1)
        
        # Final cleanup
        self.play(
            FadeOut(domain_plane_clean),
            FadeOut(codomain_plane_clean),
            FadeOut(general_mapping_label),
            FadeOut(arrow_icon)
        )
        self.wait(1)