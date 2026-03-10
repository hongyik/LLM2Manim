from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Color definitions from ledger
        LIGHT_GRAY = "#DDDDDD"
        BLUE_C = "#87CEEB"
        PURE_GREEN = "#00FF00"
        YELLOW = "#FFFF00"
        BRIGHT_YELLOW = "#FFFF00"
        WHITE = "#FFFFFF"
        PURPLE_C = "#9370DB"
        PINK = "#FF00FF"
        
        # ========== BEAT 0: SET UP INITIAL SCENE ==========
        # Create planes
        domain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.5,
                "stroke_width": 1
            },
            axis_config={"color": LIGHT_GRAY}
        )
        domain_plane.move_to(np.array([-3.43, 0.70, 0]))  # left side
        
        codomain_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.5,
                "stroke_width": 1
            },
            axis_config={"color": LIGHT_GRAY}
        )
        codomain_plane.move_to(np.array([3.43, 0.70, 0]))  # right side
        
        # Create labels
        general_mapping_label = Text("T: V → W", color=WHITE, font_size=36)
        general_mapping_label.move_to(np.array([0, 3.27, 0]))
        
        property_equations = VGroup(
            MathTex(r"T(\vec{u}+\vec{v}) = T(\vec{u}) + T(\vec{v})", color=WHITE, font_size=24),
            MathTex(r"T(c\vec{u}) = c T(\vec{u})", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        property_equations.move_to(np.array([-3.43, 1.99, 0]))
        
        v_label = Text("V", color=WHITE, font_size=32)
        v_label.next_to(domain_plane, UP, buff=0.2)
        
        w_label = Text("W", color=WHITE, font_size=32)
        w_label.next_to(codomain_plane, UP, buff=0.2)
        
        # Create objects that will be used later (initially hidden)
        image_label = Text("Image(T)", color=BRIGHT_YELLOW, font_size=32)
        image_label.next_to(codomain_plane, UP, buff=0.2).shift(RIGHT * 2)
        image_label.set_opacity(0)
        
        kernel_label = Text("Kernel(T)", color=BRIGHT_YELLOW, font_size=32)
        kernel_label.next_to(domain_plane, UP, buff=0.2).shift(RIGHT * 2)
        kernel_label.set_opacity(0)
        
        # Create initial scene
        with self.voiceover(text="Every linear transformation defines two fundamental subspaces: the kernel and the image. Let's start with the image, also called the range.") as tracker:
            self.play(
                Create(domain_plane),
                Create(codomain_plane),
                Write(general_mapping_label),
                Write(property_equations),
                Write(v_label),
                Write(w_label)
            )
        
        self.wait(0.5)
        
        # ========== BEAT 1: INTRODUCE IMAGE ==========
        # Brighten codomain plane and pulse W label
        codomain_plane_bright = codomain_plane.copy()
        codomain_plane_bright.set_stroke(opacity=1)
        
        with self.voiceover(text="The image of T is the set of all possible outputs. It's every vector in W that you can get by applying T to some vector in V.") as tracker:
            self.play(
                Transform(codomain_plane, codomain_plane_bright),
                Indicate(w_label),
                FadeIn(image_label)
            )
            
            # Create cloud of dots in V
            dots_v = VGroup()
            for _ in range(30):
                x = np.random.uniform(-4, 4)
                y = np.random.uniform(-4, 4)
                # Convert coordinates to position on the plane
                # Assuming the plane is properly scaled with x_range=[-5,5] and y_range=[-5,5]
                x_pos = domain_plane.get_center()[0] + x * (domain_plane.width / 10)
                y_pos = domain_plane.get_center()[1] + y * (domain_plane.height / 10)
                dot = Dot(color=BLUE_C, radius=0.05).move_to(
                    np.array([x_pos, y_pos, 0])
                )
                dot.set_opacity(0.3)
                dots_v.add(dot)
            
            self.play(FadeIn(dots_v))
            
            # Animate multiple mappings
            for _ in range(5):
                # Select a random dot in V (ensure valid index)
                idx = np.random.randint(0, len(dots_v))
                input_dot = dots_v[idx].copy()
                input_dot.set_opacity(1)
                
                # Calculate transformed position (using example transformation)
                pos = input_dot.get_center() - domain_plane.get_center()
                x, y = pos[0], pos[1]
                
                # Apply transformation: A = [[1.5, -0.5], [0.5, 2]]
                tx = 1.5*x - 0.5*y
                ty = 0.5*x + 2*y
                
                output_pos = codomain_plane.get_center() + np.array([tx, ty, 0])
                output_dot = Dot(color=BLUE_C, radius=0.05).move_to(output_pos)
                
                # Create arrow
                arrow = Arrow(
                    start=input_dot.get_center(),
                    end=output_dot.get_center(),
                    color=PURE_GREEN,
                    stroke_width=4,
                    buff=0.1
                )
                
                self.play(
                    input_dot.animate.set_opacity(1),
                    GrowArrow(arrow),
                    FadeIn(output_dot)
                )
                self.play(
                    FadeOut(arrow),
                    FadeOut(input_dot)
                )
        
        self.wait(0.5)
        
        # ========== BEAT 2: FORMALIZE IMAGE ==========
        # Create matrix and parallelogram
        matrix_A = MathTex(
            r"A = \begin{bmatrix} 1.5 & -0.5 \\ 0.5 & 2 \end{bmatrix}",
            color=WHITE,
            font_size=36
        )
        matrix_A.move_to(np.array([0, -1.5, 0]))
        matrix_A.set_opacity(0)
        
        # Create parallelogram for image (basis vectors transformed)
        basis1 = np.array([1, 0, 0])
        basis2 = np.array([0, 1, 0])
        
        # Transform basis vectors
        t_basis1 = np.array([1.5, 0.5, 0])
        t_basis2 = np.array([-0.5, 2, 0])
        
        # Create parallelogram vertices
        vertices = [
            codomain_plane.get_center(),
            codomain_plane.get_center() + t_basis1,
            codomain_plane.get_center() + t_basis1 + t_basis2,
            codomain_plane.get_center() + t_basis2
        ]
        
        image_region = Polygon(
            *vertices,
            color=BLUE_C,
            fill_color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=2
        )
        image_region.set_opacity(0)
        
        image_math_label = MathTex(
            r"\text{Im}(T) = \{ T(\vec{x}) \mid \vec{x} \in V \}",
            color=WHITE,
            font_size=32
        )
        image_math_label.next_to(matrix_A, DOWN, buff=0.3)
        image_math_label.set_opacity(0)
        
        with self.voiceover(text="Formally, the image is written as Im(T) or T(V). It's a subspace of the codomain W.") as tracker:
            self.play(FadeOut(dots_v))
            
            self.play(
                FadeIn(matrix_A),
                FadeIn(image_math_label)
            )
            
            self.play(
                Create(image_region)
            )
            
            # Pulse the parallelogram
            self.play(
                image_region.animate.set_fill(opacity=0.3).set_stroke(width=3),
                run_time=0.5
            )
            self.play(
                image_region.animate.set_fill(opacity=0.2).set_stroke(width=2),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # ========== BEAT 3: INTRODUCE KERNEL ==========
        # Create zero points
        zero_dot_w = Dot(color=YELLOW, radius=0.08).move_to(codomain_plane.get_center())
        zero_dot_w.set_opacity(0)
        
        zero_dot_v = Dot(color=YELLOW, radius=0.08).move_to(domain_plane.get_center())
        zero_dot_v.set_opacity(0)
        
        # Dim the image region
        image_region_dim = image_region.copy()
        image_region_dim.set_fill(opacity=0.1)
        image_region_dim.set_stroke(opacity=0.5)
        
        with self.voiceover(text="Now, the kernel, or null space. This is the set of inputs that get mapped to the zero vector in W.") as tracker:
            self.play(
                Transform(image_region, image_region_dim),
                FadeIn(zero_dot_w),
                FadeIn(zero_dot_v),
                Indicate(v_label),
                FadeIn(kernel_label)
            )
            
            # Highlight zero points
            self.play(
                zero_dot_w.animate.scale(1.5),
                zero_dot_v.animate.scale(1.5),
                run_time=0.5
            )
            self.play(
                zero_dot_w.animate.scale(2/3),
                zero_dot_v.animate.scale(2/3),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # ========== BEAT 4: SHOW KERNEL VECTORS ==========
        # Create kernel vectors (both along same line: multiples of (1, -3))
        kernel_vector1 = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + np.array([1, -3, 0]),
            color=PURPLE_C,
            stroke_width=4,
            buff=0
        )
        kernel_vector1.set_opacity(0)
        
        kernel_vector2 = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + np.array([2, -6, 0]),
            color=PURPLE_C,
            stroke_width=4,
            buff=0
        )
        kernel_vector2.set_opacity(0)
        
        with self.voiceover(text="The kernel consists of all vectors x in V such that T(x) equals the zero vector. It answers the question: what gets completely crushed to zero?") as tracker:
            # Show first kernel vector
            self.play(FadeIn(kernel_vector1))
            
            # Create mapping arrow to zero
            arrow1 = Arrow(
                start=kernel_vector1.get_end(),
                end=zero_dot_w.get_center(),
                color=PURE_GREEN,
                stroke_width=4,
                buff=0.1
            )
            self.play(GrowArrow(arrow1))
            self.play(FadeOut(arrow1))
            
            # Show second kernel vector
            self.play(FadeIn(kernel_vector2))
            
            arrow2 = Arrow(
                start=kernel_vector2.get_end(),
                end=zero_dot_w.get_center(),
                color=PURE_GREEN,
                stroke_width=4,
                buff=0.1
            )
            self.play(GrowArrow(arrow2))
            self.play(FadeOut(arrow2))
        
        self.wait(0.5)
        
        # ========== BEAT 5: FORMALIZE KERNEL ==========
        # Create kernel line
        kernel_line = Line(
            start=domain_plane.get_center() + np.array([-4, 12, 0]),
            end=domain_plane.get_center() + np.array([4, -12, 0]),
            color=PURPLE_C,
            stroke_width=6
        )
        kernel_line.set_opacity(0)
        
        kernel_math_label = MathTex(
            r"\text{Ker}(T) = \{ \vec{x} \in V \mid T(\vec{x}) = \vec{0} \}",
            color=WHITE,
            font_size=32
        )
        kernel_math_label.next_to(image_math_label, DOWN, buff=0.3)
        kernel_math_label.set_opacity(0)
        
        with self.voiceover(text="Formally, the kernel is written as Ker(T) or N(T). It is a subspace of the domain V.") as tracker:
            # Transform vectors into line
            self.play(
                ReplacementTransform(VGroup(kernel_vector1, kernel_vector2), kernel_line),
                FadeIn(kernel_math_label)
            )
            
            # Pulse the line
            self.play(
                kernel_line.animate.set_stroke(width=8),
                run_time=0.5
            )
            self.play(
                kernel_line.animate.set_stroke(width=6),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # ========== BEAT 6: SHOW BOTH TOGETHER ==========
        # Brighten both regions
        image_region_bright = image_region.copy()
        image_region_bright.set_fill(opacity=0.3)
        image_region_bright.set_stroke(opacity=1, width=3)
        
        # Create non-kernel vector
        non_kernel_vector = Arrow(
            start=domain_plane.get_center(),
            end=domain_plane.get_center() + np.array([2, 1, 0]),
            color=BLUE_C,
            stroke_width=4,
            buff=0
        )
        non_kernel_vector.set_opacity(0)
        
        # Calculate its transformation
        x, y = 2, 1
        tx = 1.5*x - 0.5*y
        ty = 0.5*x + 2*y
        non_kernel_output = Dot(
            color=BLUE_C,
            radius=0.08
        ).move_to(codomain_plane.get_center() + np.array([tx, ty, 0]))
        
        with self.voiceover(text="Let's see both together. The kernel lives in the domain, the image in the codomain. They reveal fundamental properties: if the kernel is only the zero vector, the transformation is one-to-one. If the image is all of W, it is onto.") as tracker:
            self.play(
                Transform(image_region, image_region_bright),
                Indicate(kernel_line),
                Indicate(matrix_A)
            )
            
            # Show kernel vector mapping
            kernel_point = kernel_line.point_from_proportion(0.7)
            arrow_kernel = Arrow(
                start=kernel_point,
                end=zero_dot_w.get_center(),
                color=PURE_GREEN,
                stroke_width=4,
                buff=0.1
            )
            self.play(GrowArrow(arrow_kernel))
            self.play(FadeOut(arrow_kernel))
            
            # Show non-kernel vector mapping
            self.play(FadeIn(non_kernel_vector))
            arrow_non_kernel = Arrow(
                start=non_kernel_vector.get_end(),
                end=non_kernel_output.get_center(),
                color=PURE_GREEN,
                stroke_width=4,
                buff=0.1
            )
            self.play(GrowArrow(arrow_non_kernel))
            self.play(FadeIn(non_kernel_output))
            self.play(FadeOut(arrow_non_kernel))
        
        self.wait(0.5)
        
        # ========== BEAT 7: RANK-NULLITY THEOREM ==========
        nullity_label = Text("dim(Ker(T)) = nullity", color=PURPLE_C, font_size=28)
        nullity_label.next_to(domain_plane, DOWN, buff=0.5).align_to(domain_plane, LEFT)
        nullity_label.set_opacity(0)
        
        rank_label = Text("dim(Im(T)) = rank", color=BLUE_C, font_size=28)
        rank_label.next_to(codomain_plane, DOWN, buff=0.5).align_to(codomain_plane, RIGHT)
        rank_label.set_opacity(0)
        
        rank_nullity_eq = MathTex(
            r"\text{dim}(V) = \text{nullity} + \text{rank}",
            color=WHITE,
            font_size=36
        )
        rank_nullity_eq.move_to(np.array([0, -2.5, 0]))
        rank_nullity_eq.set_opacity(0)
        
        numeric_eq = MathTex(r"2 = 1 + 1", color=WHITE, font_size=36)
        numeric_eq.next_to(rank_nullity_eq, DOWN, buff=0.3)
        numeric_eq.set_opacity(0)
        
        with self.voiceover(text="The dimensions of these subspaces are deeply connected. The dimension of the domain V equals the dimension of the kernel plus the dimension of the image. This is the Rank-Nullity Theorem, a central result in linear algebra.") as tracker:
            self.play(
                FadeIn(nullity_label),
                FadeIn(rank_label)
            )
            
            self.play(
                Write(rank_nullity_eq),
                Write(numeric_eq),
                Indicate(property_equations)
            )
            
            # Show the dimensions match
            self.play(
                nullity_label.animate.set_color(BRIGHT_YELLOW),
                rank_label.animate.set_color(BRIGHT_YELLOW),
                run_time=0.5
            )
            self.play(
                nullity_label.animate.set_color(PURPLE_C),
                rank_label.animate.set_color(BLUE_C),
                run_time=0.5
            )
        
        self.wait(0.5)
        
        # ========== BEAT 8: VISUALIZE COLLAPSE AND STRETCH ==========
        with self.voiceover(text="The kernel and image give us a complete picture of what a linear transformation does: it collapses the kernel to a point, and it maps the rest of the space onto the image.") as tracker:
            # Create a perpendicular line to kernel
            perp_direction = np.array([3, 1, 0])  # Perpendicular to kernel line direction (1, -3)
            perp_line = Line(
                start=domain_plane.get_center() - perp_direction,
                end=domain_plane.get_center() + perp_direction,
                color=BLUE_C,
                stroke_width=4
            )
            
            # Show kernel collapse
            self.play(
                kernel_line.animate.scale(0.1).move_to(zero_dot_v),
                run_time=1.5
            )
            
            # Show perpendicular line stretching to image
            self.play(
                Transform(perp_line, image_region),
                run_time=1.5
            )
            
            self.play(FadeOut(perp_line))
        
        self.wait(0.5)
        
        # ========== BEAT 9: TRANSITION TO INVERTIBILITY ==========
        # Create inverse label
        inverse_label = Text("T^{-1}", color=PINK, font_size=40)
        inverse_label.move_to(general_mapping_label.get_center())
        inverse_label.set_opacity(0)
        
        # Create arrow icon
        arrow_icon = Arrow(
            start=LEFT * 2,
            end=RIGHT * 2,
            color=WHITE,
            stroke_width=3
        )
        arrow_icon.next_to(general_mapping_label, DOWN, buff=0.5)
        arrow_icon.set_opacity(0)
        
        # Group for cleanup
        all_objects = VGroup(
            domain_plane, codomain_plane, general_mapping_label,
            property_equations, v_label, w_label, image_label,
            kernel_label, zero_dot_w, zero_dot_v, matrix_A,
            image_math_label, image_region, kernel_math_label,
            kernel_line, nullity_label, rank_label,
            rank_nullity_eq, numeric_eq, non_kernel_vector,
            non_kernel_output
        )
        
        with self.voiceover(text="When is a linear transformation reversible? That's the question of invertibility, which we explore next.") as tracker:
            # Fade out most objects
            self.play(FadeOut(all_objects))
            
            # Show inverse label briefly
            self.play(FadeIn(inverse_label))
            self.wait(0.3)
            self.play(FadeOut(inverse_label))
            
            # Show arrow pointing to next scene
            self.play(FadeIn(arrow_icon))
            self.wait(0.5)
            self.play(FadeOut(arrow_icon))
        
        self.wait(1)