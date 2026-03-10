from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Set background
        background = Rectangle(
            width=14, height=8,
            fill_color=[DARK_BLUE, "#001122"],
            fill_opacity=1,
            stroke_width=0
        )
        self.add(background)
        
        # ==================== BEAT 1: Header with Linearity Properties ====================
        # Create objects BEFORE voiceover
        general_mapping_label = Text("T: V → W", color=WHITE, font_size=44)
        general_mapping_label.move_to(np.array([0.0, 3.27, 0]))
        
        property_equations = VGroup(
            MathTex(r"T(\mathbf{u}+\mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})", color=WHITE, font_size=40),
            MathTex(r"T(c\mathbf{u}) = c T(\mathbf{u})", color=WHITE, font_size=40)
        )
        property_equations.arrange(DOWN, buff=0.5)
        property_equations.move_to(np.array([0.0, 1.99, 0]))
        
        linearity_brace = Brace(property_equations, DOWN, color=YELLOW)
        linearity_brace.move_to(np.array([0.0, 0.82, 0]))
        
        linearity_label = Text("Linearity", color=YELLOW, font_size=34)
        linearity_label.next_to(linearity_brace, DOWN, buff=0.2)
        
        # Voiceover beat 1
        with self.voiceover(text="We've reached the end of our journey through linear transformations. Let's summarize the core ideas.") as tracker:
            self.play(FadeIn(general_mapping_label))
            self.play(FadeIn(property_equations))
            self.play(Create(linearity_brace), Write(linearity_label))
        
        self.wait(0.5)
        
        # ==================== BEAT 2: Example Icons ====================
        # Create icon objects
        icon_scaling = VGroup(
            Square(side_length=0.5, fill_color=BLUE_D, fill_opacity=0.7, stroke_color=WHITE),
            Square(side_length=1.0, fill_color=BLUE_D, fill_opacity=0.7, stroke_color=WHITE).shift(RIGHT*2),
            Arrow(start=LEFT*0.5, end=RIGHT*1.5, color=GREEN, buff=0, stroke_width=3)
        )
        icon_scaling.move_to(np.array([-3.43, -1.06, 0]))
        
        icon_rotation = VGroup(
            Square(side_length=0.5, fill_color=BLUE_D, fill_opacity=0.7, stroke_color=WHITE),
            Square(side_length=0.5, fill_color=BLUE_D, fill_opacity=0.7, stroke_color=WHITE)
                .rotate(PI/2).shift(RIGHT*2),
            Arrow(start=LEFT*0.5, end=RIGHT*1.5, color=GREEN, buff=0, stroke_width=3)
        )
        icon_rotation.move_to(np.array([0.0, -1.06, 0]))
        
        icon_shear = VGroup(
            Square(side_length=0.5, fill_color=BLUE_D, fill_opacity=0.7, stroke_color=WHITE),
            Polygon(
                [-0.25, -0.25, 0],
                [0.75, -0.25, 0],
                [0.5, 0.25, 0],
                [-0.5, 0.25, 0],
                fill_color=BLUE_D,
                fill_opacity=0.7,
                stroke_color=WHITE
            ).shift(RIGHT*2),
            Arrow(start=LEFT*0.5, end=RIGHT*1.5, color=GREEN, buff=0, stroke_width=3)
        )
        icon_shear.move_to(np.array([3.43, -1.06, 0]))
        
        # Voiceover beat 2
        with self.voiceover(text="First, a linear transformation is a function between vector spaces that preserves vector addition and scalar multiplication. This structure-preserving nature is its defining feature.") as tracker:
            self.play(FadeIn(icon_scaling, shift=UP), FadeIn(icon_rotation, shift=UP), FadeIn(icon_shear, shift=UP))
            self.play(Indicate(icon_scaling, scale_factor=1.2, color=YELLOW))
            self.play(Indicate(icon_rotation, scale_factor=1.2, color=YELLOW))
            self.play(Indicate(icon_shear, scale_factor=1.2, color=YELLOW))
        
        self.wait(0.5)
        
        # ==================== BEAT 3: Matrix Representation ====================
        # Fade out icons, create matrix representation objects
        self.play(
            FadeOut(icon_scaling),
            FadeOut(icon_rotation),
            FadeOut(icon_shear)
        )
        
        # Create domain and codomain planes
        domain_plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3
            },
            x_length=4,
            y_length=4
        )
        domain_plane.move_to(np.array([-3.43, 0.70, 0]))
        
        codomain_plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3
            },
            x_length=4,
            y_length=4
        )
        codomain_plane.move_to(np.array([3.43, 0.70, 0]))
        
        # Basis vectors and images
        basis_i = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + RIGHT*1.5,
            color=BLUE_D,
            buff=0,
            stroke_width=4
        )
        
        basis_j = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + UP*1.5,
            color=MAROON,
            buff=0,
            stroke_width=4
        )
        
        image_a = Arrow(
            start=codomain_plane.get_center(),
            end=codomain_plane.get_center() + np.array([2, 1, 0]),
            color=BLUE_D,
            buff=0,
            stroke_width=4
        )
        
        image_b = Arrow(
            start=codomain_plane.get_center(),
            end=codomain_plane.get_center() + np.array([-1, 2, 0]),
            color=MAROON,
            buff=0,
            stroke_width=4
        )
        
        # Mapping arrows
        map_arrow_i = DashedLine(
            start=basis_i.get_end(),
            end=image_a.get_end(),
            color=GREEN,
            stroke_width=2
        )
        
        map_arrow_j = DashedLine(
            start=basis_j.get_end(),
            end=image_b.get_end(),
            color=GREEN,
            stroke_width=2
        )
        
        # Matrix and label
        matrix_A = Matrix(
            [[2, -1], [1, 2]],
            bracket_color=WHITE,
            element_alignment_corner=DOWN
        )
        matrix_A.scale(0.8)
        matrix_A.move_to(np.array([0.0, 0.70, 0]))
        
        matrix_label = Text("A = [T(î) T(ĵ)]", color=WHITE, font_size=24)
        matrix_label.next_to(matrix_A, DOWN, buff=0.5)
        
        # Voiceover beat 3
        with self.voiceover(text="Second, in finite dimensions, every linear transformation can be represented by a matrix. The columns of this matrix are simply the images of the basis vectors.") as tracker:
            self.play(FadeIn(domain_plane), FadeIn(codomain_plane))
            self.play(Create(basis_i), Create(basis_j))
            self.play(Create(image_a), Create(image_b))
            self.play(Create(map_arrow_i), Create(map_arrow_j))
            self.play(Write(matrix_A))
            self.play(Write(matrix_label))
            # Pulse columns in sync with vectors
            self.play(
                matrix_A.get_columns()[0].animate.set_color(BLUE_D),
                matrix_A.get_columns()[1].animate.set_color(MAROON)
            )
            self.play(
                matrix_A.get_columns()[0].animate.set_color(WHITE),
                matrix_A.get_columns()[1].animate.set_color(WHITE)
            )
        
        self.wait(0.5)
        
        # ==================== BEAT 4: Composition ====================
        # Create composition objects
        matrix_B = Matrix(
            [[1, 0], [1, 1]],
            bracket_color=WHITE,
            element_alignment_corner=DOWN
        )
        matrix_B.scale(0.8)
        matrix_B.move_to(np.array([-1.0, -1.06, 0]))
        
        multiply_dot = MathTex(r"\cdot", font_size=36)
        multiply_dot.next_to(matrix_B, RIGHT, buff=0.2)
        
        matrix_C = Matrix(
            [[1, -1], [3, 1]],
            bracket_color=YELLOW,
            element_alignment_corner=DOWN
        )
        matrix_C.scale(0.8)
        equals = MathTex(r"=", font_size=36)
        equals.next_to(multiply_dot, RIGHT, buff=0.2)
        matrix_C.next_to(equals, RIGHT, buff=0.2)
        
        composition_eq = MathTex(r"T \circ S \leftrightarrow A B", color=WHITE, font_size=32)
        composition_eq.move_to(np.array([0.0, -2.62, 0]))
        
        # Voiceover beat 4
        with self.voiceover(text="Third, composing two linear transformations corresponds to multiplying their matrices. The order of application matches the order of multiplication.") as tracker:
            # Move matrix_A left
            self.play(matrix_A.animate.shift(LEFT*2), matrix_label.animate.shift(LEFT*2))
            
            # Show B and multiplication
            self.play(FadeIn(matrix_B, shift=UP))
            self.play(Write(multiply_dot))
            self.play(Write(equals))
            self.play(FadeIn(matrix_C, shift=UP))
            
            # Quick flow animation
            flow_vector = Dot(color=YELLOW, radius=0.08)
            flow_vector.move_to(domain_plane.get_center() + LEFT*2)
            
            self.play(
                flow_vector.animate.move_to(matrix_B.get_center()),
                run_time=1.5
            )
            self.play(
                flow_vector.animate.move_to(matrix_A.get_center()),
                run_time=1.5
            )
            self.play(
                flow_vector.animate.move_to(matrix_C.get_center()),
                run_time=1.5
            )
            self.play(FadeOut(flow_vector))
            
            self.play(Write(composition_eq))
        
        self.wait(0.5)
        
        # ==================== BEAT 5: Kernel and Image ====================
        # Clean up matrices
        self.play(
            FadeOut(matrix_A),
            FadeOut(matrix_B),
            FadeOut(matrix_C),
            FadeOut(multiply_dot),
            FadeOut(equals),
            FadeOut(composition_eq),
            FadeOut(matrix_label)
        )
        
        # Create kernel and image objects
        kernel_line = Line(
            start=domain_plane.get_center() + np.array([-2, -1, 0]),
            end=domain_plane.get_center() + np.array([2, 1, 0]),
            color=PURPLE,
            stroke_width=6
        )
        
        image_region = Polygon(
            codomain_plane.get_center() + np.array([-1, -0.5, 0]),
            codomain_plane.get_center() + np.array([1, 0.5, 0]),
            codomain_plane.get_center() + np.array([2, 2.5, 0]),
            codomain_plane.get_center() + np.array([0, 1.5, 0]),
            fill_color=BLUE_D,
            fill_opacity=0.3,
            stroke_color=BLUE_D,
            stroke_width=2
        )
        
        kernel_label = Text("Ker(T)", color=YELLOW, font_size=24)
        kernel_label.next_to(kernel_line, UP, buff=0.5)
        
        image_label = Text("Im(T)", color=YELLOW, font_size=24)
        image_label.next_to(image_region, UP, buff=0.5)
        
        rank_nullity_eq = MathTex(
            r"\dim(V) = \text{nullity} + \text{rank}",
            color=WHITE,
            font_size=32
        )
        rank_nullity_eq.move_to(np.array([0.0, -1.06, 0]))
        
        # Voiceover beat 5
        with self.voiceover(text="Fourth, every transformation defines two key subspaces. The kernel, in the domain, is what gets mapped to zero. The image, in the codomain, is all possible outputs.") as tracker:
            self.play(Create(kernel_line))
            self.play(Create(image_region))
            self.play(Write(kernel_label), Write(image_label))
            self.play(Write(rank_nullity_eq))
        
        self.wait(0.5)
        
        # ==================== BEAT 6: Invertibility ====================
        # Create invertibility objects
        kernel_point = Dot(
            point=domain_plane.get_center(),
            color=PURPLE,
            radius=0.1
        )
        
        full_image = Rectangle(
            width=codomain_plane.get_width(),
            height=codomain_plane.get_height(),
            fill_color=BLUE_D,
            fill_opacity=0.2,
            stroke_color=BLUE_D,
            stroke_width=2
        )
        full_image.move_to(codomain_plane.get_center())
        
        # Bring back matrix A
        matrix_A_return = Matrix(
            [[2, -1], [1, 2]],
            bracket_color=WHITE,
            element_alignment_corner=DOWN
        )
        matrix_A_return.scale(0.8)
        matrix_A_return.move_to(np.array([0.0, 0.70, 0]))
        
        det_display = MathTex(r"\det(A) \neq 0", color=YELLOW, font_size=32)
        det_display.next_to(matrix_A_return, DOWN, buff=0.5)
        
        inverse_label = Text("T^{-1}: W → V", color=YELLOW, font_size=32)
        inverse_label.move_to(np.array([0.0, 2.5, 0]))
        
        matrix_A_inv = Matrix(
            [[0.4, 0.2], [-0.2, 0.4]],
            bracket_color=WHITE,
            element_alignment_corner=DOWN
        )
        matrix_A_inv.scale(0.8)
        matrix_A_inv.next_to(matrix_A_return, RIGHT, buff=0.5)
        
        # Voiceover beat 6
        with self.voiceover(text="Finally, a transformation is invertible if it is one-to-one and onto—meaning a trivial kernel and a full image. This is equivalent to its matrix having a non-zero determinant.") as tracker:
            # Transform kernel and image
            self.play(ReplacementTransform(kernel_line, kernel_point))
            self.play(ReplacementTransform(image_region, full_image))
            
            # Show matrix and determinant
            self.play(Write(matrix_A_return))
            self.play(Write(det_display))
            self.play(Indicate(det_display, scale_factor=1.3))
            
            # Show inverse
            self.play(Write(inverse_label))
            self.play(Write(matrix_A_inv))
        
        self.wait(0.5)
        
        # ==================== BEAT 7: Summary Row ====================
        # Clean up everything except header
        cleanup_group = VGroup(
            domain_plane, codomain_plane,
            basis_i, basis_j, image_a, image_b,
            map_arrow_i, map_arrow_j,
            kernel_point,  # kernel_line was transformed into kernel_point
            full_image,    # image_region was transformed into full_image
            kernel_label, image_label,
            rank_nullity_eq,
            matrix_A_return, det_display,
            inverse_label, matrix_A_inv
        )
        
        self.play(FadeOut(cleanup_group))
        
        # Create summary icons
        icon_matrix = Square(side_length=0.4, stroke_color=WHITE)
        icon_matrix.move_to(np.array([-3.43, -2.62, 0]))
        
        icon_composition = VGroup(
            Arrow(start=LEFT*0.3, end=RIGHT*0.3, color=GREEN, buff=0),
            Arrow(start=RIGHT*0.3, end=RIGHT*0.9, color=GREEN, buff=0)
        )
        icon_composition.move_to(np.array([0.0, -2.62, 0]))
        
        icon_subspaces = VGroup(
            Line(
                start=np.array([-0.3, -0.2, 0]),
                end=np.array([0.3, 0.2, 0]),
                color=PURPLE,
                stroke_width=4
            ),
            Polygon(
                [-0.2, -0.1, 0],
                [0.2, -0.1, 0],
                [0.3, 0.3, 0],
                [-0.1, 0.3, 0],
                fill_color=BLUE_D,
                fill_opacity=0.3,
                stroke_color=BLUE_D
            )
        )
        icon_subspaces.move_to(np.array([3.43, -2.62, 0]))
        
        # Voiceover beat 7
        with self.voiceover(text="These concepts—linearity, matrix representation, composition, kernel and image, and invertibility—form the foundation of linear algebra. They provide the language to describe transformations of space, solve systems of equations, and understand data in higher dimensions.") as tracker:
            self.play(
                FadeIn(icon_matrix, shift=UP),
                FadeIn(icon_composition, shift=UP),
                FadeIn(icon_subspaces, shift=UP)
            )
        
        self.wait(0.5)
        
        # ==================== BEAT 8: Final Title ====================
        # Voiceover beat 8
        with self.voiceover(text="From mapping vectors to manipulating matrices, linear transformations give us a powerful and consistent framework for navigating the world of linear spaces.") as tracker:
            self.play(
                Indicate(icon_matrix, scale_factor=1.2),
                Indicate(icon_composition, scale_factor=1.2),
                Indicate(icon_subspaces, scale_factor=1.2)
            )
        
        # Final cleanup and title
        final_cleanup = VGroup(
            general_mapping_label,
            property_equations,
            linearity_brace,
            linearity_label,
            icon_matrix,
            icon_composition,
            icon_subspaces
        )
        
        self.play(FadeOut(final_cleanup))
        
        # Brighten background
        bright_background = Rectangle(
            width=14, height=8,
            fill_color=["#334477", DARK_BLUE],
            fill_opacity=1,
            stroke_width=0
        )
        self.play(Transform(background, bright_background))
        
        final_title = Text("Linear Transformations", color=YELLOW, font_size=72)
        final_title.move_to(np.array([0.0, 0.0, 0]))
        
        with self.voiceover(text="This concludes our introduction to linear transformations.") as tracker:
            self.play(FadeIn(final_title, shift=UP))
        
        self.wait(2)
        self.play(FadeOut(final_title), FadeOut(background))
        self.wait(1)