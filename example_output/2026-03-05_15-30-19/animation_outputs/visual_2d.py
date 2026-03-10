from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Create dark blue gradient background
        background = Rectangle(
            width=14, height=8,
            fill_color=["#000033", "#000055"],
            fill_opacity=1,
            stroke_width=0
        )
        self.add(background)
        
        # ==================== BEAT 1: Introduction ====================
        # Create coordinate planes
        domain_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3,
                "stroke_width": 1
            },
            axis_config={"stroke_color": LIGHT_GRAY, "stroke_width": 2}
        )
        domain_plane.move_to(np.array([-3.43, 0.70, 0]))
        
        v_label = Text("V = R²", color=WHITE, font_size=24)
        v_label.move_to(np.array([-5.0, 2.5, 0]))
        
        # Create property equations (small and translucent reference)
        additivity = MathTex(r"T(\vec{u}+\vec{v})=T(\vec{u})+T(\vec{v})", 
                           font_size=20, color=WHITE)
        homogeneity = MathTex(r"T(c\vec{u})=cT(\vec{u})", 
                            font_size=20, color=WHITE)
        property_equations = VGroup(additivity, homogeneity)
        property_equations.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        property_equations.set_opacity(0.5)
        property_equations.move_to(np.array([-5.5, 1.5, 0]))
        
        # Create square shape in V
        shape_S = Polygon(
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=2
        )
        shape_S.move_to(np.array([-3.43, 0.70, 0]))
        
        shape_label = Text("Shape S", color=BLUE_C, font_size=20)
        shape_label.move_to(np.array([-4.5, 1.7, 0]))
        
        # Create codomain plane on right
        codomain_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3,
                "stroke_width": 1
            },
            axis_config={"stroke_color": LIGHT_GRAY, "stroke_width": 2}
        )
        codomain_plane.move_to(np.array([3.43, 0.70, 0]))
        
        w_label = Text("W = R²", color=WHITE, font_size=24)
        w_label.move_to(np.array([2.0, 2.5, 0]))
        
        mapping_label = Text("T: V → W", color=WHITE, font_size=28)
        mapping_label.move_to(np.array([0, 2.8, 0]))
        
        # Voiceover beat 1
        with self.voiceover(text="Let's visualize some linear transformations in two dimensions. We'll start with a simple shape to see how it gets mapped.") as tracker:
            self.play(FadeIn(domain_plane), FadeIn(v_label), FadeIn(property_equations))
            self.play(FadeIn(shape_S), Write(shape_label))
            self.play(FadeIn(codomain_plane), FadeIn(w_label), Write(mapping_label))
        
        self.wait(0.5)
        
        # ==================== BEAT 2: Scaling Transformation ====================
        # Create scaling equation
        scale_eq = MathTex(r"T(\vec{x}) = k\vec{x}", color=WHITE, font_size=36)
        scale_eq.move_to(np.array([0, -1.5, 0]))
        
        k_value = MathTex(r"k = 2", color=YELLOW, font_size=32)
        k_value.next_to(scale_eq, RIGHT, buff=0.5)
        
        # Create mapping arrow
        mapping_arrow = Arrow(
            start=domain_plane.get_right() + RIGHT*0.2,
            end=codomain_plane.get_left() + LEFT*0.2,
            color=PURE_GREEN,
            buff=0,
            stroke_width=3
        )
        
        # Create scaled square in W
        scaled_shape = Polygon(
            [0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0],
            color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=2
        )
        scaled_shape.move_to(np.array([3.43, 0.70, 0]))
        
        scaled_label = Text("T(S)", color=BLUE_C, font_size=20)
        scaled_label.move_to(np.array([4.5, 1.7, 0]))
        
        with self.voiceover(text="First, consider a uniform scaling. This transformation stretches or shrinks space equally in all directions.") as tracker:
            self.play(Indicate(shape_S, scale_factor=1.2, color=YELLOW))
            self.play(Write(scale_eq), Write(k_value))
            self.play(Create(mapping_arrow))
            self.play(FadeIn(scaled_shape), Write(scaled_label))
        
        self.wait(0.5)
        
        # ==================== BEAT 3: Highlight scaling property ====================
        # Create vector from origin to (1,1) in V
        corner_vector_v = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(1, 1),
            color=BLUE_C,
            buff=0,
            stroke_width=3
        )
        
        # Create green tracing arrow for the mapping
        trace_arrow = Arrow(
            start=domain_plane.c2p(1, 1),
            end=codomain_plane.c2p(2, 2),
            color=PURE_GREEN,
            buff=0,
            stroke_width=2
        )
        
        # Create vector in W
        corner_vector_w = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(2, 2),
            color=BLUE_C,
            buff=0,
            stroke_width=3
        )
        
        with self.voiceover(text="Notice how every point in the original square is moved to a point twice as far from the origin. This satisfies our linearity properties: scaling the input scales the output by the same factor.") as tracker:
            self.play(FadeOut(scale_eq), FadeOut(k_value))
            self.play(Create(corner_vector_v))
            self.play(Create(trace_arrow))
            self.play(Transform(corner_vector_v.copy(), corner_vector_w))
            self.play(Indicate(property_equations[1], color=YELLOW))
        
        self.wait(0.5)
        
        # Clean up for next transformation
        self.play(
            FadeOut(corner_vector_v),
            FadeOut(corner_vector_w),
            FadeOut(trace_arrow),
            FadeOut(scaled_shape),
            FadeOut(scaled_label),
            FadeOut(mapping_arrow)
        )
        
        # ==================== BEAT 4: Rotation Transformation ====================
        # Create rotation equation
        rotate_eq = MathTex(r"T(\vec{x}) = R_{\theta}\vec{x}", color=WHITE, font_size=36)
        rotate_eq.move_to(np.array([0, -1.5, 0]))
        
        theta_value = MathTex(r"\theta = 90^\circ", color=YELLOW, font_size=32)
        theta_value.next_to(rotate_eq, RIGHT, buff=0.5)
        
        # Create rotated square in W
        rotated_shape = Polygon(
            [0, 0, 0], [0, 1, 0], [-1, 1, 0], [-1, 0, 0],
            color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=2
        )
        rotated_shape.move_to(np.array([3.43, 0.70, 0]))
        
        # Create rotated grid for W
        rotated_grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3,
                "stroke_width": 1
            },
            axis_config={"stroke_color": LIGHT_GRAY, "stroke_width": 2}
        )
        rotated_grid.rotate(90 * DEGREES)
        rotated_grid.move_to(np.array([3.43, 0.70, 0]))
        
        with self.voiceover(text="Next, a rotation. This transformation turns the entire space around the origin by a fixed angle.") as tracker:
            self.play(Write(rotate_eq), Write(theta_value))
            self.play(FadeIn(shape_S))
            self.play(Create(mapping_arrow))
            self.play(FadeIn(rotated_shape))
            self.play(Transform(codomain_plane, rotated_grid))
        
        self.wait(0.5)
        
        # ==================== BEAT 5: Demonstrate rotation additivity ====================
        # Create vectors in V
        vector_u = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(1, 0),
            color=BLUE_C,
            buff=0,
            stroke_width=3
        )
        
        vector_v = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(0, 1),
            color=MAROON_C,
            buff=0,
            stroke_width=3
        )
        
        vector_sum = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(1, 1),
            color=PURPLE_C,
            buff=0,
            stroke_width=3
        )
        
        # Create transformed vectors in W
        T_u = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(0, 1),
            color=BLUE_C,
            buff=0,
            stroke_width=3
        )
        
        T_v = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(-1, 0),
            color=MAROON_C,
            buff=0,
            stroke_width=3
        )
        
        T_sum = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(-1, 1),
            color=PURPLE_C,
            buff=0,
            stroke_width=3
        )
        
        with self.voiceover(text="Rotation preserves the shape and size of objects, only changing their orientation. It, too, is linear—adding two vectors and then rotating gives the same result as rotating them first and then adding.") as tracker:
            self.play(FadeOut(rotate_eq), FadeOut(theta_value))
            self.play(Create(vector_u), Create(vector_v))
            self.play(Create(vector_sum))
            
            # Animate rotation of vectors
            vector_group = VGroup(vector_u, vector_v, vector_sum)
            self.play(Rotate(vector_group, angle=90*DEGREES, about_point=domain_plane.c2p(0, 0)))
            
            # Show transformed vectors in W
            self.play(Create(T_u), Create(T_v), Create(T_sum))
            
            # Highlight additivity property
            self.play(Indicate(property_equations[0], color=YELLOW))
        
        self.wait(0.5)
        
        # Clean up for next transformation
        self.play(
            FadeOut(vector_group),
            FadeOut(T_u), FadeOut(T_v), FadeOut(T_sum),
            FadeOut(rotated_shape),
            FadeOut(mapping_arrow)
        )
        
        # Restore original grid in W
        original_grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3,
                "stroke_width": 1
            },
            axis_config={"stroke_color": LIGHT_GRAY, "stroke_width": 2}
        )
        original_grid.move_to(np.array([3.43, 0.70, 0]))
        self.play(Transform(codomain_plane, original_grid))
        
        # ==================== BEAT 6: Shear Transformation ====================
        # Create shear equation
        shear_eq = MathTex(
            r"T(\vec{x}) = \begin{bmatrix} 1 & s \\ 0 & 1 \end{bmatrix}\vec{x}", 
            color=WHITE, font_size=36
        )
        shear_eq.move_to(np.array([0, -1.5, 0]))
        
        s_value = MathTex(r"s = 1", color=YELLOW, font_size=32)
        s_value.next_to(shear_eq, RIGHT, buff=0.5)
        
        # Create sheared shape in W
        sheared_shape = Polygon(
            [0, 0, 0], [1, 0, 0], [2, 1, 0], [1, 1, 0],
            color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=2
        )
        sheared_shape.move_to(np.array([3.43, 0.70, 0]))
        
        # Create sheared grid for W
        sheared_grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_opacity": 0.3,
                "stroke_width": 1
            },
            axis_config={"stroke_color": LIGHT_GRAY, "stroke_width": 2}
        )
        # Apply shear transformation to grid
        sheared_grid.apply_function(
            lambda p: np.array([
                p[0] + p[1],  # x' = x + y (since s=1)
                p[1],
                p[2]
            ])
        )
        sheared_grid.move_to(np.array([3.43, 0.70, 0]))
        
        with self.voiceover(text="Finally, a shear transformation. This slants space, like pushing the top of a deck of cards.") as tracker:
            self.play(Write(shear_eq), Write(s_value))
            self.play(FadeIn(shape_S))
            self.play(Create(mapping_arrow))
            self.play(FadeIn(sheared_shape))
            self.play(Transform(codomain_plane, sheared_grid))
        
        self.wait(0.5)
        
        # ==================== BEAT 7: Show grid point movement ====================
        # Create grid of points in V
        grid_points = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                point = Dot(
                    domain_plane.c2p(i, j),
                    color=BLUE_C,
                    radius=0.04
                )
                grid_points.add(point)
        
        # Create transformed points in W
        transformed_points = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                point = Dot(
                    codomain_plane.c2p(i + j, j),  # Apply shear: x' = x + y
                    color=BLUE_C,
                    radius=0.04
                )
                transformed_points.add(point)
        
        with self.voiceover(text="Shear distorts angles but keeps lines straight and parallel. It's a clear visual example of linearity: the image of the entire grid is just a skewed version of the original, with the origin fixed.") as tracker:
            self.play(FadeOut(shape_S), FadeOut(shear_eq), FadeOut(s_value))
            self.play(FadeIn(grid_points))
            
            # Create green arrows showing movement
            arrows = VGroup()
            for point, t_point in zip(grid_points, transformed_points):
                arrow = Arrow(
                    start=point.get_center(),
                    end=t_point.get_center(),
                    color=PURE_GREEN,
                    buff=0.1,
                    stroke_width=1,
                    max_tip_length_to_length_ratio=0.15
                )
                arrows.add(arrow)
            
            self.play(Create(arrows), run_time=2)
            self.play(Transform(grid_points, transformed_points), FadeOut(arrows))
        
        self.wait(0.5)
        
        # ==================== BEAT 8: Show example icons ====================
        # Clean up
        self.play(
            FadeOut(grid_points),
            FadeOut(sheared_shape),
            FadeOut(mapping_arrow)
        )
        
        # Restore original grid in W
        self.play(Transform(codomain_plane, original_grid))
        
        # Create example icons
        icon_scaling = Polygon(
            [0, 0, 0], [0.5, 0, 0], [0.5, 0.5, 0], [0, 0.5, 0],
            color=BLUE_C, fill_opacity=0.2, stroke_width=1
        )
        icon_scaling.move_to(np.array([-4, -2.5, 0]))
        
        icon_rotation = Polygon(
            [0, 0, 0], [0.5, 0, 0], [0.5, 0.5, 0], [0, 0.5, 0],
            color=BLUE_C, fill_opacity=0.2, stroke_width=1
        )
        icon_rotation.move_to(np.array([-2, -2.5, 0]))
        
        icon_shear = Polygon(
            [0, 0, 0], [0.5, 0, 0], [0.75, 0.5, 0], [0.25, 0.5, 0],
            color=BLUE_C, fill_opacity=0.2, stroke_width=1
        )
        icon_shear.move_to(np.array([0, -2.5, 0]))
        
        example_icons = VGroup(icon_scaling, icon_rotation, icon_shear)
        
        with self.voiceover(text="These are just a few examples. The key takeaway is that any linear transformation in 2D will map the grid lines to other straight, evenly spaced lines, always leaving the origin fixed.") as tracker:
            self.play(FadeIn(example_icons))
            self.wait(1)
            self.play(FadeOut(example_icons))
        
        self.wait(0.5)
        
        # ==================== BEAT 9: Hint at matrix representation ====================
        matrix_bracket = Text("[", color=WHITE, font_size=60)
        matrix_bracket.move_to(np.array([0, 0.70, 0]))
        
        with self.voiceover(text="But how do we describe these transformations precisely? For that, we need a powerful tool: the matrix.") as tracker:
            self.play(FadeIn(matrix_bracket))
            
            # Create gentle arrow pointing right
            hint_arrow = Arrow(
                start=matrix_bracket.get_right() + LEFT*0.2,
                end=matrix_bracket.get_right() + RIGHT*0.5,
                color=PURE_GREEN,
                buff=0,
                stroke_width=2
            )
            self.play(Create(hint_arrow))
            self.wait(1)
        
        # Final cleanup
        self.wait(1)
        container = VGroup(
            domain_plane, v_label, property_equations,
            codomain_plane, w_label, mapping_label,
            matrix_bracket, hint_arrow
        )
        self.play(FadeOut(container))
        self.wait(1)