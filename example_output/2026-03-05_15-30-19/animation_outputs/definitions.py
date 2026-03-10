from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np

class GenScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(KokoroService(voice="af_sarah", lang="en-us"))
        
        # Colors from consistency ledger
        vector_space_plane_color = LIGHT_GRAY
        input_vector_color = BLUE_C
        mapping_arrow_color = PURE_GREEN
        general_label_color = WHITE
        highlight_color = YELLOW  # Using YELLOW since BRIGHT_YELLOW not in valid colors
        second_vector_color = MAROON_C
        sum_vector_color = PURPLE_C
        scaled_vector_color = "#FFAA66"  # Light orange
        scalar_color = YELLOW
        
        # Create dark blue gradient background
        background = Rectangle(width=14, height=8, fill_color="#000033", fill_opacity=1, stroke_width=0)
        background.move_to(ORIGIN)
        self.add(background)
        
        # --- Create all objects for the scene ---
        
        # Domain and codomain planes
        domain_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": vector_space_plane_color,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            axis_config={
                "stroke_color": vector_space_plane_color,
                "stroke_width": 2,
                "stroke_opacity": 0.7
            }
        )
        domain_plane.move_to(np.array([-3.43, 0.70, 0]))
        
        codomain_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": vector_space_plane_color,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            axis_config={
                "stroke_color": vector_space_plane_color,
                "stroke_width": 2,
                "stroke_opacity": 0.7
            }
        )
        codomain_plane.move_to(np.array([3.43, 0.70, 0]))
        
        # Labels for the planes
        label_V = Text("V", color=general_label_color, font_size=36)
        label_V.move_to(np.array([-3.43, 2.50, 0]))
        
        label_W = Text("W", color=general_label_color, font_size=36)
        label_W.move_to(np.array([3.43, 2.50, 0]))
        
        # General mapping label (faint)
        general_mapping_label = Text("T: V → W", color=general_label_color, font_size=28)
        general_mapping_label.set_opacity(0.3)
        general_mapping_label.move_to(np.array([0, -2.00, 0]))
        
        # --- Beat 0: Setup ---
        self.play(
            FadeIn(domain_plane),
            FadeIn(codomain_plane),
            FadeIn(label_V),
            FadeIn(label_W),
            FadeIn(general_mapping_label)
        )
        self.wait(0.5)
        
        # --- Beat 1: Additivity - vectors in V ---
        # Create vectors u and v in V (domain plane)
        vector_u = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(1, 1),
            color=input_vector_color,
            buff=0,
            stroke_width=4
        )
        label_u = Text("u", color=input_vector_color, font_size=24)
        label_u.move_to(domain_plane.c2p(1.2, 1.2))
        
        vector_v = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(2, -1),
            color=second_vector_color,
            buff=0,
            stroke_width=4
        )
        label_v = Text("v", color=second_vector_color, font_size=24)
        label_v.move_to(domain_plane.c2p(2.2, -1.2))
        
        # Create sum vector (will appear later)
        vector_sum = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(3, 0),
            color=sum_vector_color,
            buff=0,
            stroke_width=4
        )
        label_sum = Text("u+v", color=sum_vector_color, font_size=24)
        label_sum.move_to(domain_plane.c2p(3.2, 0.2))
        
        with self.voiceover(text="Two simple rules make a transformation linear. The first is additivity: transforming a sum of vectors is the same as transforming them individually and then summing the results.") as tracker:
            self.play(
                Create(vector_u),
                Write(label_u),
                Create(vector_v),
                Write(label_v)
            )
            
            # Animate tip-to-tail addition
            # Move v to the tip of u
            vector_v_copy = vector_v.copy()
            label_v_copy = label_v.copy()
            self.play(
                vector_v_copy.animate.shift(vector_u.get_end() - vector_v_copy.get_start()),
                label_v_copy.animate.shift(vector_u.get_end() - vector_v_copy.get_start())
            )
            
            # Fade in the sum vector from origin to (3, 0)
            self.play(
                FadeIn(vector_sum),
                Write(label_sum)
            )
            self.play(
                FadeOut(vector_v_copy),
                FadeOut(label_v_copy)
            )
        self.wait(0.5)
        
        # --- Beat 2: Additivity equation and mapping to W ---
        # Additivity equation
        additivity_eq = MathTex(
            r"T(\vec{u} + \vec{v}) = T(\vec{u}) + T(\vec{v})",
            color=general_label_color,
            font_size=36
        )
        additivity_eq.move_to(np.array([0, 2.62, 0]))
        
        # Mapping arrow from u+v to W
        mapping_arrow1 = Arrow(
            start=domain_plane.c2p(3, 0),
            end=codomain_plane.c2p(-2, 0),
            color=mapping_arrow_color,
            buff=0.1,
            stroke_width=3
        )
        
        # Transformed vectors in W (codomain plane)
        T_u = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(0, 2),
            color=input_vector_color,
            buff=0,
            stroke_width=4
        )
        label_T_u = Text("T(u)", color=input_vector_color, font_size=24)
        label_T_u.move_to(codomain_plane.c2p(-0.3, 2.2))
        
        T_v = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(3, -1),
            color=second_vector_color,
            buff=0,
            stroke_width=4
        )
        label_T_v = Text("T(v)", color=second_vector_color, font_size=24)
        label_T_v.move_to(codomain_plane.c2p(3.2, -1.2))
        
        T_sum = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(3, 1),
            color=sum_vector_color,
            buff=0,
            stroke_width=4
        )
        label_T_sum = Text("T(u+v)", color=sum_vector_color, font_size=24)
        label_T_sum.move_to(codomain_plane.c2p(3.2, 1.2))
        
        with self.voiceover(text="Formally, for any vectors u and v in V, T of u plus v equals T of u plus T of v.") as tracker:
            # Show equation
            self.play(Write(additivity_eq))
            
            # Pulse T(u+v) part of equation and vector u+v
            self.play(
                additivity_eq[0][:7].animate.set_color(highlight_color),
                vector_sum.animate.set_stroke(color=highlight_color, width=6),
                label_sum.animate.set_color(highlight_color),
                run_time=0.5
            )
            self.play(
                additivity_eq[0][:7].animate.set_color(general_label_color),
                vector_sum.animate.set_stroke(color=sum_vector_color, width=4),
                label_sum.animate.set_color(sum_vector_color),
                run_time=0.5
            )
            
            # Show mapping arrow and T(u+v) in W
            self.play(GrowArrow(mapping_arrow1))
            self.play(
                Create(T_sum),
                Write(label_T_sum)
            )
            
            # Pulse T(u)+T(v) part of equation
            self.play(
                additivity_eq[0][8:].animate.set_color(highlight_color),
                run_time=0.5
            )
            self.play(
                additivity_eq[0][8:].animate.set_color(general_label_color),
                run_time=0.5
            )
            
            # Show T(u) and T(v) in W
            self.play(
                Create(T_u),
                Write(label_T_u),
                Create(T_v),
                Write(label_T_v)
            )
            
            # Animate tip-to-tail addition in W
            T_v_copy = T_v.copy()
            label_T_v_copy = label_T_v.copy()
            self.play(
                T_v_copy.animate.shift(T_u.get_end() - T_v_copy.get_start()),
                label_T_v_copy.animate.shift(T_u.get_end() - T_v_copy.get_start())
            )
            
            # Show that the resultant matches T(u+v)
            self.play(
                T_sum.animate.set_stroke(color=highlight_color, width=6),
                label_T_sum.animate.set_color(highlight_color),
                run_time=0.5
            )
            self.play(
                T_sum.animate.set_stroke(color=sum_vector_color, width=4),
                label_T_sum.animate.set_color(sum_vector_color),
                run_time=0.5
            )
            self.play(
                FadeOut(T_v_copy),
                FadeOut(label_T_v_copy)
            )
        self.wait(0.5)
        
        # --- Beat 3: Transition to homogeneity ---
        # Scalar label
        scalar_c = MathTex("c", color=scalar_color, font_size=32)
        scalar_c.move_to(domain_plane.c2p(-0.5, -0.5))
        
        # Scaled vector c*u
        vector_cu = Arrow(
            start=domain_plane.c2p(0, 0),
            end=domain_plane.c2p(2, 2),
            color=scaled_vector_color,
            buff=0,
            stroke_width=4
        )
        label_cu = MathTex("c\\vec{u}", color=scaled_vector_color, font_size=24)
        label_cu.move_to(domain_plane.c2p(2.2, 2.2))
        
        # Keep original u faint for comparison
        vector_u_faint = vector_u.copy()
        vector_u_faint.set_stroke(opacity=0.3)
        label_u_faint = label_u.copy()
        label_u_faint.set_opacity(0.3)
        
        with self.voiceover(text="The second rule is homogeneity, or scaling. Transforming a scaled vector is the same as scaling the transformed vector.") as tracker:
            # Fade out additivity-specific elements
            self.play(
                FadeOut(additivity_eq),
                FadeOut(mapping_arrow1),
                FadeOut(vector_v),
                FadeOut(label_v),
                FadeOut(vector_sum),
                FadeOut(label_sum),
                FadeOut(T_v),
                FadeOut(label_T_v),
                FadeOut(T_sum),
                FadeOut(label_T_sum)
            )
            
            # Fade in scalar and scale u
            self.play(FadeIn(scalar_c))
            
            # Show original u faintly
            self.add(vector_u_faint, label_u_faint)
            self.remove(vector_u, label_u)
            
            # Scale u to get c*u
            self.play(
                TransformFromCopy(vector_u_faint, vector_cu),
                TransformFromCopy(label_u_faint, label_cu)
            )
        self.wait(0.5)
        
        # --- Beat 4: Homogeneity equation and mapping ---
        # Homogeneity equation
        homogeneity_eq = MathTex(
            r"T(c\vec{u}) = c T(\vec{u})",
            color=general_label_color,
            font_size=36
        )
        homogeneity_eq.move_to(np.array([0, 2.62, 0]))
        
        # Mapping arrow from c*u to W
        mapping_arrow2 = Arrow(
            start=domain_plane.c2p(2, 2),
            end=codomain_plane.c2p(-1, 2),
            color=mapping_arrow_color,
            buff=0.1,
            stroke_width=3
        )
        
        # T(c*u) in W
        T_cu = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(0, 4),
            color=scaled_vector_color,
            buff=0,
            stroke_width=4
        )
        label_T_cu = MathTex("T(c\\vec{u})", color=scaled_vector_color, font_size=24)
        label_T_cu.move_to(codomain_plane.c2p(-0.8, 4.2))
        
        # c*T(u) - will scale T(u) by 2
        T_u_scaled = Arrow(
            start=codomain_plane.c2p(0, 0),
            end=codomain_plane.c2p(0, 4),
            color=scaled_vector_color,
            buff=0,
            stroke_width=4
        )
        
        with self.voiceover(text="Formally, for any scalar c and any vector u, T of c times u equals c times T of u.") as tracker:
            # Show equation
            self.play(Write(homogeneity_eq))
            
            # Pulse T(c*u) part
            self.play(
                homogeneity_eq[0][:6].animate.set_color(highlight_color),
                vector_cu.animate.set_stroke(color=highlight_color, width=6),
                label_cu.animate.set_color(highlight_color),
                run_time=0.5
            )
            self.play(
                homogeneity_eq[0][:6].animate.set_color(general_label_color),
                vector_cu.animate.set_stroke(color=scaled_vector_color, width=4),
                label_cu.animate.set_color(scaled_vector_color),
                run_time=0.5
            )
            
            # Show mapping arrow and T(c*u) in W
            self.play(GrowArrow(mapping_arrow2))
            self.play(
                Create(T_cu),
                Write(label_T_cu)
            )
            
            # Pulse c*T(u) part
            self.play(
                homogeneity_eq[0][7:].animate.set_color(highlight_color),
                run_time=0.5
            )
            self.play(
                homogeneity_eq[0][7:].animate.set_color(general_label_color),
                run_time=0.5
            )
            
            # Scale T(u) by 2 to get c*T(u)
            T_u_copy = T_u.copy()
            self.play(
                Transform(T_u_copy, T_u_scaled),
                label_T_u.animate.next_to(T_u_scaled, LEFT, buff=0.1)
            )
            
            # Show that the scaled T(u) matches T(c*u)
            self.play(
                T_cu.animate.set_stroke(color=highlight_color, width=6),
                label_T_cu.animate.set_color(highlight_color),
                run_time=0.5
            )
            self.play(
                T_cu.animate.set_stroke(color=scaled_vector_color, width=4),
                label_T_cu.animate.set_color(scaled_vector_color),
                run_time=0.5
            )
            
            self.remove(T_u_copy)
        self.wait(0.5)
        
        # --- Beat 5: Combine both properties ---
        # Property equations group
        additivity_eq_final = MathTex(
            r"T(\vec{u} + \vec{v}) = T(\vec{u}) + T(\vec{v})",
            color=general_label_color,
            font_size=32
        )
        
        homogeneity_eq_final = MathTex(
            r"T(c\vec{u}) = c T(\vec{u})",
            color=general_label_color,
            font_size=32
        )
        
        property_equations = VGroup(additivity_eq_final, homogeneity_eq_final)
        property_equations.arrange(DOWN, buff=0.5)
        property_equations.move_to(np.array([0, 0.82, 0]))
        
        # Brace and label
        property_brace = Brace(property_equations, DOWN, color=highlight_color)
        property_label = Text("Properties of Linearity", color=highlight_color, font_size=28)
        property_label.next_to(property_brace, DOWN, buff=0.2)
        
        with self.voiceover(text="Together, these properties—additivity and homogeneity—define linearity. They mean the transformation preserves vector addition and scalar multiplication.") as tracker:
            # Fade out homogeneity-specific elements
            self.play(
                FadeOut(homogeneity_eq),
                FadeOut(mapping_arrow2),
                FadeOut(scalar_c),
                FadeOut(vector_cu),
                FadeOut(label_cu),
                FadeOut(vector_u_faint),
                FadeOut(label_u_faint),
                FadeOut(T_u),
                FadeOut(label_T_u),
                FadeOut(T_cu),
                FadeOut(label_T_cu)
            )
            
            # Show both equations together
            self.play(FadeIn(property_equations))
            self.play(Create(property_brace))
            self.play(Write(property_label))
        self.wait(0.5)
        
        # --- Beat 6: Transition to next part ---
        # New larger plane for next scene
        new_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": vector_space_plane_color,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            axis_config={
                "stroke_color": vector_space_plane_color,
                "stroke_width": 2,
                "stroke_opacity": 0.7
            }
        )
        new_plane.scale(0.9)
        new_plane.move_to(np.array([0, 0, 0]))
        
        # Down arrow icon
        down_arrow = Arrow(
            start=ORIGIN,
            end=[0, -1, 0],
            color=general_label_color,
            buff=0,
            stroke_width=3
        )
        down_arrow.move_to(np.array([0, -2.62, 0]))
        
        # Persistent summary header (equations moved to top left)
        summary_header = VGroup(
            additivity_eq_final.copy(),
            homogeneity_eq_final.copy()
        )
        summary_header.arrange(DOWN, buff=0.3)
        summary_header.scale(0.6)
        summary_header.to_corner(UL, buff=0.5)
        
        with self.voiceover(text="With this definition in hand, let's see what these linear transformations look like in action.") as tracker:
            # Fade out old scene elements
            self.play(
                FadeOut(domain_plane),
                FadeOut(codomain_plane),
                FadeOut(label_V),
                FadeOut(label_W),
                FadeOut(general_mapping_label),
                FadeOut(property_brace),
                FadeOut(property_label)
            )
            
            # Move equations to top left and fade in new plane
            self.play(
                Transform(property_equations, summary_header),
                FadeIn(new_plane),
                FadeIn(down_arrow)
            )
        
        self.wait(1)
        
        # Cleanup - fade everything out
        container = VGroup(property_equations, new_plane, down_arrow)
        self.play(FadeOut(container))
        self.wait(1)