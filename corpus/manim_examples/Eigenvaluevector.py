from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv.koko import KokoroService
import numpy as np

class EigenvalueVectorScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        # Configure voiceover service with detailed voice instructions.
        self.set_speech_service(KokoroService(
            model_path="kokoro-v0_19.onnx",
            voices_path="voices.bin",
            voice="af"
        ))
        # Run each section
        self.ConceptualIntroduction()
        self.clear()
        self.NumericalExampleIntroduction()
        self.clear()
        self.SearchForEigenvectors()
        self.clear()
        self.FindingEigenvalues()
    def ConceptualIntroduction(self):
        ##############################
        # New Scene 0: Conceptual Introduction
        ##############################
        # Create introduction text
        intro_text = VGroup(
            Text("Eigenvalues & Eigenvectors", font_size=48, color=YELLOW),
            Text("Key Concepts in Linear Transformation", font_size=36),
        ).arrange(DOWN, buff=0.5).to_edge(UP)

        definition_text = VGroup(
            Text("Eigenvectors:", color=BLUE, font_size=32),
            Text("Directions that maintain their orientation during transformation", 
                 font_size=24),
            Text("Eigenvalues:", color=RED, font_size=32),
            Text("Scaling factors that show how much eigenvectors stretch/shrink", 
                 font_size=24)
        ).arrange(DOWN, buff=0.3).center()

        applications = VGroup(
            Text("Applications:", color=GREEN, font_size=32),
            Text("• System Stability Analysis", font_size=24),
            Text("• Quantum Physics", font_size=24),
            Text("• Machine Learning", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        applications.next_to(definition_text, DOWN, buff=0.5)

        # Mathematical definition
        math_def = MathTex(
            "A\\vec{v} = \\lambda\\vec{v}",
            font_size=36
        )
        math_explanation = Text(
            "Where A is the transformation matrix,\n"
            "λ (lambda) is the eigenvalue, and\n"
            "v is the eigenvector",
            font_size=24
        )
        math_group = VGroup(math_def, math_explanation).arrange(DOWN, buff=0.3)

        # Animate introduction sequence
        with self.voiceover(text="Welcome to an exploration of eigenvalues and eigenvectors, fundamental concepts in linear algebra."):
            self.play(Write(intro_text))
            self.wait(1)

        with self.voiceover(text="Eigenvectors are special directions that remain unchanged during a transformation, even if they get longer or shorter."):
            self.play(
                Write(definition_text[:2]),
                run_time=2
            )
            self.wait(1)

        with self.voiceover(text="Eigenvalues tell us exactly how much these vectors stretch or shrink during the transformation."):
            self.play(
                Write(definition_text[2:]),
                run_time=2
            )
            self.wait(1)

        with self.voiceover(text="These concepts are crucial in many fields, including system stability analysis, quantum physics, and machine learning."):
            self.play(Write(applications))
            self.wait(2)

        with self.voiceover(text="Mathematically, we express this relationship using the equation A v equals lambda v, where lambda represents the eigenvalue."):
            self.play(
                FadeOut(applications),
                ReplacementTransform(definition_text, math_group)
            )
            self.wait(2)

        # Transition to the main visualization
        with self.voiceover(text="Let's visualize these concepts to better understand how they work."):
            self.play(
                FadeOut(intro_text),
                FadeOut(definition_text),
                FadeOut(math_group)
            )
    def NumericalExampleIntroduction(self):
        ##############################
        # New Scene: Numerical Example Introduction
        ##############################
        # Define our matrix (same as we'll use later)
        matrix = [[2, 1], 
                 [1, 2]]
        # Calculate eigenvalues and eigenvectors (same as we'll use later)
        eigenvals, eigenvecs = np.linalg.eig(matrix)
        # Normalize eigenvectors for better visualization
        eigenvecs = eigenvecs * np.sqrt(2)#np.linalg.norm(eigenvecs, axis=0)
        
        # Add an example of a non-eigenvector
        non_eigen_vector = np.array([1, 0])  # unit vector along x-axis
        transformed_non_eigen = np.dot(matrix, non_eigen_vector)
        
        # Create title and matrix A (will stay throughout the scene)
        numerical_title = Text("Numerical Example", font_size=36).to_edge(UP)
        
        # Matrix A will stay on the left side (keep its position)
        matrix_example = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}",
            font_size=36
        ).to_edge(LEFT).shift(UP * 2)
        math_def = MathTex(
            "A\\vec{v} = \\lambda\\vec{v}",
            font_size=36
        ).to_edge(LEFT).shift(DOWN * 1.5)
        # Move coordinate system slightly left
        mini_axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": True}
        ).shift(LEFT * 1.5)  # Added shift left
        
        # Adjust equation positions to align with shifted coordinate system
        non_eigen_calc = MathTex(
            "\\text{Non-eigenvector:}\\\\"
            "\\vec{w} = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix}",
            font_size=32
        ).shift(RIGHT * 3 + UP * 2)  # Adjusted from .to_edge(RIGHT)
        
        non_eigen_transform = MathTex(
            "A\\vec{w} = "
            f"\\begin{{bmatrix}} {transformed_non_eigen[0]:.2f} \\\\ {transformed_non_eigen[1]:.2f} \\end{{bmatrix}}",
            font_size=32
        ).next_to(non_eigen_calc, DOWN, buff=0.5)
        
        # Update positions for eigenvector equations
        eigen1_calc = MathTex(
            "\\text{Eigenvector 1:}\\\\"
            f"\\vec{{v}}_1 = \\begin{{bmatrix}} {eigenvecs[0,0]:.2f} \\\\ {eigenvecs[1,0]:.2f} \\end{{bmatrix}}",
            font_size=32
        ).shift(RIGHT * 3 + UP * 2)  # Adjusted from .to_edge(RIGHT)
        
        eigen1_multiply = MathTex(
            "A\\vec{v}_1 &= "
            f"\\begin{{bmatrix}} 2 & 1 \\\\ 1 & 2 \\end{{bmatrix}}"
            f"\\begin{{bmatrix}} {eigenvecs[0,0]:.2f} \\\\ {eigenvecs[1,0]:.2f} \\end{{bmatrix}} \\\\"
            "&= "
            f"\\begin{{bmatrix}} (2 \\cdot {eigenvecs[0,0]:.2f}) + (1 \\cdot {eigenvecs[1,0]:.2f}) \\\\ (1 \\cdot {eigenvecs[0,0]:.2f}) + (2 \\cdot {eigenvecs[1,0]:.2f}) \\end{{bmatrix}} \\\\"
            "&= "
            f"\\begin{{bmatrix}} {eigenvals[0]*eigenvecs[0,0]:.2f} \\\\ {eigenvals[0]*eigenvecs[1,0]:.2f} \\end{{bmatrix}} \\\\"
            f"&= {eigenvals[0]:.2f}\\begin{{bmatrix}} {eigenvecs[0,0]:.2f} \\\\ {eigenvecs[1,0]:.2f} \\end{{bmatrix}} \\\\"
            "&= \\lambda_1\\vec{v}_1",
            font_size=28
        ).next_to(eigen1_calc, DOWN, buff=0.5)
        
        # Update positions for second eigenvector equations
        eigen2_calc = MathTex(
            "\\text{Eigenvector 2:}\\\\"
            f"\\vec{{v}}_2 = \\begin{{bmatrix}} {eigenvecs[0,1]:.2f} \\\\ {eigenvecs[1,1]:.2f} \\end{{bmatrix}}",
            font_size=32
        ).shift(RIGHT * 3 + UP * 2)  # Adjusted from .to_edge(RIGHT)
        
        eigen2_multiply = MathTex(
            "A\\vec{v}_2 &= "
            f"\\begin{{bmatrix}} 2 & 1 \\\\ 1 & 2 \\end{{bmatrix}}"
            f"\\begin{{bmatrix}} {eigenvecs[0,1]:.2f} \\\\ {eigenvecs[1,1]:.2f} \\end{{bmatrix}} \\\\"
            "&= "
            f"\\begin{{bmatrix}} (2 \\cdot {eigenvecs[0,1]:.2f}) + (1 \\cdot {eigenvecs[1,1]:.2f}) \\\\ (1 \\cdot {eigenvecs[0,1]:.2f}) + (2 \\cdot {eigenvecs[1,1]:.2f}) \\end{{bmatrix}} \\\\"
            "&= "
            f"\\begin{{bmatrix}} {eigenvals[1]*eigenvecs[0,1]:.2f} \\\\ {eigenvals[1]*eigenvecs[1,1]:.2f} \\end{{bmatrix}} \\\\"
            f"&= {eigenvals[1]:.2f}\\begin{{bmatrix}} {eigenvecs[0,1]:.2f} \\\\ {eigenvecs[1,1]:.2f} \\end{{bmatrix}} \\\\"
            "&= \\lambda_2\\vec{v}_2",
            font_size=28
        ).next_to(eigen2_calc, DOWN, buff=0.5)
        
        # Update final summary position
        final_summary = MathTex(
            "\\text{Eigenvalues:}\\quad"
            f"\\lambda_1 = {eigenvals[0]:.2f},\\quad"
            f"\\lambda_2 = {eigenvals[1]:.2f}",
            font_size=32
        ).shift(RIGHT * 3 + UP * 2)  # Adjusted from .to_edge(RIGHT)
        
        # Animation sequence
        with self.voiceover(text="Let's look at a concrete numerical example. Here, we have a transformation matrix A that we'll use to illustrate the behavior of both eigenvectors and non-eigenvectors. Notice that our matrix is displayed on the left and our mini coordinate system is set up to clearly show how vectors change under this transformation."):
            self.play(
                Write(numerical_title),
                Write(matrix_example),
                Write(math_def)
            )
            self.wait(0.5)
            self.play(Create(mini_axes))
        
        # Show non-eigenvector example
        mini_non_eigen = Arrow(
            mini_axes.c2p(0, 0),
            mini_axes.c2p(1, 0),
            color=BLUE,
            buff=0
        )
        mini_transformed = Arrow(
            mini_axes.c2p(0, 0),
            mini_axes.c2p(transformed_non_eigen[0], transformed_non_eigen[1]),
            color=BLUE,
            buff=0
        )
        
        with self.voiceover(text="First, we consider a vector that is not an eigenvector. Here, we use the unit vector along the x-axis,vector w equal to 1 and 0. Notice how this vector is initially aligned with the x-axis."):
            self.play(
                Write(non_eigen_calc),
                Create(mini_non_eigen)
            )
            self.wait(0.5)
        
        with self.voiceover(text="When we multiply this non-eigenvector by the matrix A, both its direction and length change. This behavior confirms that it is not an eigenvector—eigenvectors, as we will see, only scale without changing direction."):
            self.play(
                Write(non_eigen_transform),
                Create(mini_transformed)
            )
            self.wait(1)
        
        # Create first eigenvector visualization
        eigen1_original = Arrow(
            mini_axes.c2p(0, 0),
            mini_axes.c2p(eigenvecs[0,0], eigenvecs[1,0]),
            color=YELLOW,
            buff=0
        )
        eigen1_transformed = Arrow(
            mini_axes.c2p(0, 0),
            mini_axes.c2p(eigenvals[0]*eigenvecs[0,0], eigenvals[0]*eigenvecs[1,0]),
            color=YELLOW_A,
            buff=0
        )
        
        with self.voiceover(text=f"Then in comparison, let's look at our first eigenvector and see what happens when we multiply it by matrix A."):
            self.play(
                ReplacementTransform(non_eigen_calc, eigen1_calc),
                FadeOut(non_eigen_transform),
                ReplacementTransform(mini_non_eigen, eigen1_original)
            )
            self.wait(1)
        
        with self.voiceover(text="Watch the multiplication process step by step.The animation shows the detailed multiplication process, where every term is calculated. "):
            self.play(
                Write(eigen1_multiply),
                run_time=3
            )
            self.wait(1)
        
        with self.voiceover(text=f"The result is exactly {eigenvals[0]:.2f} times our original vector. This scaling factor is our eigenvalue.Notice how the direction of the eigenvector remains unchanged—only its length scales by the eigenvalue lambda."):
            self.play(
                Create(eigen1_transformed)
            )
            self.wait(1)

        # Create second eigenvector visualization (add this before the voiceover section)
        eigen2_original = Arrow(
            mini_axes.c2p(0, 0),
            mini_axes.c2p(eigenvecs[0,1], eigenvecs[1,1]),
            color=RED,
            buff=0
        )
        eigen2_transformed = Arrow(
            mini_axes.c2p(0, 0),
            mini_axes.c2p(eigenvals[1]*eigenvecs[0,1], eigenvals[1]*eigenvecs[1,1]),
            color=RED_A,
            buff=0
        )
        
        with self.voiceover(text=f"Now let's look at our second eigenvector and its multiplication process."):
            self.play(
                ReplacementTransform(eigen1_calc, eigen2_calc),
                ReplacementTransform(eigen1_multiply, eigen2_multiply),
                ReplacementTransform(eigen1_original, eigen2_original),
            )
            self.wait(1)
            
        with self.voiceover(text=f"When matrix A multiplies eigenvector v2, the result is simply lambda2 times v2. This confirms that v2 is indeed an eigenvector since its direction is preserved and only its magnitude changes according to lambda2."):
            self.play(
                Create(eigen2_transformed)
            )
            self.wait(1)

        # Show both eigenvectors together
        with self.voiceover(text="To summarize, this numerical example clearly demonstrates the key property of eigenvectors and eigenvalues. A non-eigenvector, when transformed by matrix A, changes both direction and length. In contrast, the eigenvectors maintain their direction and are simply scaled by their corresponding eigenvalues. This relationship is captured by the equation A v equals lambda v, which is fundamental to understanding linear transformations."):
            self.play(
                ReplacementTransform(eigen2_calc, final_summary),
                FadeOut(eigen2_transformed)  # Added this to clean up
            )
            self.wait(2)
    def SearchForEigenvectors(self):
        ##############################
        # Scene 1: Setup – Establish Grid and Axes with Random Vectors
        ##############################
        # Create axes and grid with matching dimensions
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,  # Explicitly set length
            y_length=10,  # Explicitly set length
            axis_config={"include_numbers": False}
        )
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,  # Match with axes length
            y_length=10,  # Match with axes length
            background_line_style={
                "stroke_opacity": 0.4,
                "stroke_width": 1,
                "stroke_color": GREY
            }
        )
        
        # Create random vectors during initial setup
        random_vector1 = Arrow(ORIGIN, [2, 1, 0], color=BLUE, buff=0)
        random_vector2 = Arrow(ORIGIN, [-1, 2, 0], color=GREEN, buff=0)
        vector_labels = VGroup(
            MathTex("\\vec{v}_1", color=BLUE).next_to(random_vector1.get_end(), RIGHT),
            MathTex("\\vec{v}_2", color=GREEN).next_to(random_vector2.get_end(), LEFT)
        )
        
        origin_dot = Dot(ORIGIN, color=YELLOW)
        origin_label = Text("(0,0)", font_size=24).next_to(origin_dot, DOWN+RIGHT, buff=0.5)
        initial_title = Text("Initial Grid with Random Vectors", font_size=36).to_edge(UP)

        # Modified setup animation sequence
        with self.voiceover(text="For more intuitive understanding, We begin with a standard coordinate system, complete with clearly marked axes and an evenly spaced grid. This familiar setting provides a reference frame for all our upcoming transformations."):
            self.play(
                Create(axes),
                Create(grid),
                Create(origin_dot),
                Write(origin_label),
                Write(initial_title)
            )
            self.play(
                Create(random_vector1),
                Create(random_vector2),
                Write(vector_labels)
            )
            self.wait(1)

        with self.voiceover(text="To illustrate how typical vectors behave under transformation, we add two random vectors. Notice one vector, shown in blue, and another, in green. Their initial positions and directions are arbitrary, serving as examples of general vectors in the plane."):
            self.play(
                random_vector1.animate.set_color(BLUE),
                random_vector2.animate.set_color(GREEN)
            )
            self.wait(1)
        ##############################
        # Scene 2: Introduce the Transformation Matrix
        ##############################
        # Define the transformation matrix and display it.
        matrix = [[2, 1], 
                  [1, 2]]
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}",
            font_size=36
        ).to_corner(UL)
        matrix_title = Text("Transformation Matrix A", font_size=24).next_to(matrix_tex, UP)
        
        with self.voiceover(text="Back to our transformation matrix A. This matrix encapsulates the linear transformation we are studying. Every vector in our plane will be multiplied by this matrix, and we will observe how that multiplication alters their direction and magnitude."):
            self.play(
                Write(matrix_tex),
                Write(matrix_title)
            )
            self.wait(1)

        ##############################
        # Scene 3: Apply the Transformation
        ##############################
        transform_label = MathTex("\\text{Applying Transformation: } x \\mapsto Ax", font_size=36)
        transform_label.to_edge(UP)
        axes.set_style(
            stroke_opacity=0.2,
            stroke_color=GREY_C
        )
        transformed_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,  # Match with original axes
            y_length=10,  # Match with original axes
            axis_config={"include_numbers": False}
        )
        with self.voiceover(text="Watch closely as we apply the transformation x to Ax. Notice how the grid itself deforms—squares become parallelograms—indicating the global effect of our matrix. Simultaneously, the random vectors also change, both in their lengths and orientations."):
            self.play(ReplacementTransform(initial_title, transform_label))
            self.play(
                grid.animate.apply_matrix(matrix),
                Create(transformed_axes.apply_matrix(matrix)),
                FadeOut(axes),
                random_vector1.animate.apply_matrix(matrix),
                random_vector2.animate.apply_matrix(matrix),
                vector_labels[0].animate.next_to(random_vector1.get_end(), RIGHT),
                vector_labels[1].animate.next_to(random_vector2.get_end(), LEFT),
                run_time=3
            )
            self.wait(1)

        with self.voiceover(text="Observe that these typical vectors change dramatically—they rotate and stretch differently. This is the expected behavior for most vectors under a linear transformation."):
            self.play(
                Indicate(random_vector1, color=BLUE_A),
                Indicate(random_vector2, color=GREEN_A),
                run_time=2
            )
            self.wait(1)
        ##############################
        # Scene 5: Search for Eigenvectors Using a Rotating Vector
        ##############################
        # Fade out the random vectors to focus on finding eigenvectors.
        with self.voiceover(text="Now, let's search for those special directions: the eigenvectors. Unlike the random vectors, eigenvectors maintain their orientation under transformation and only scale in length."):
            self.play(
                FadeOut(random_vector1),
                FadeOut(random_vector2),
                FadeOut(vector_labels)
            )
        self.wait(1)
        ##############################
        # Scene 6: Detailed Eigenvector and Eigenvalue Demonstration
        ##############################
        # Calculate eigenvalues and eigenvectors first
        eigenvals, eigenvecs = np.linalg.eig(matrix)
        # Normalize eigenvectors for better visualization
        eigenvecs = eigenvecs / np.linalg.norm(eigenvecs, axis=0)

        # Create rotating vector with transformation visualization
        rotating_vector = Arrow(ORIGIN, [1, 0, 0], color=WHITE, buff=0)
        transformed_vector = Arrow(ORIGIN, [1, 0, 0], color=YELLOW_A, buff=0, stroke_opacity=0.5)
        
        with self.voiceover(text="Let's rotate a vector and watch how it transforms. For most directions, the transformed vector differs from the original. However, when the transformed vector points in the same direction as the original, even if scaled, we've found an eigenvector. In those moments, the vector's direction is preserved while its magnitude changes."):
            self.play(Create(rotating_vector), Create(transformed_vector))
            
            # Animate rotation with transformation
            for angle in np.linspace(0, 2*PI, 160):  # 1-degree increments (more points)
                rotated_direction = np.array([np.cos(angle), np.sin(angle), 0])
                transformed_direction = np.dot(matrix, rotated_direction[:2])
                
                # Check if close to eigenvector direction
                is_near_eigenvector = False
                for eigenvec in eigenvecs.T:
                    if np.abs(np.cross(rotated_direction[:2], eigenvec)) < 0.015:
                        is_near_eigenvector = True
                        break
                
                self.play(
                    rotating_vector.animate.put_start_and_end_on(ORIGIN, rotated_direction),
                    transformed_vector.animate.put_start_and_end_on(
                        ORIGIN, 
                        [transformed_direction[0], transformed_direction[1], 0]
                    ),
                    run_time=0.1 if not is_near_eigenvector else 0.3
                )
                
                if is_near_eigenvector:
                    self.play(Flash(rotating_vector), run_time=0.3)
                    self.wait(0.3)

        # Step 3: Show eigenvectors clearly
        eigenvector1 = Arrow(ORIGIN, [eigenvecs[0,0], eigenvecs[1,0], 0], color=YELLOW, buff=0)
        eigenvector2 = Arrow(ORIGIN, [eigenvecs[0,1], eigenvecs[1,1], 0], color=RED, buff=0)
        
        # Create dashed copies for original length reference
        dashed_eigen1 = DashedVMobject(eigenvector1.copy())
        dashed_eigen2 = DashedVMobject(eigenvector2.copy())
        
        # Labels for eigenvectors
        eigen_labels = VGroup(
            Text("Eigenvector 1", color=YELLOW, font_size=12),
            Text("Eigenvector 2", color=RED, font_size=12)
        )
        eigen_labels[0].next_to(eigenvector1, UP)
        eigen_labels[1].next_to(eigenvector2, DOWN)
        
        with self.voiceover(text="These are our eigenvectors - the special directions we found where vectors maintain their orientation."):
            self.play(
                FadeOut(rotating_vector),
                FadeOut(transformed_vector),
                Create(eigenvector1),
                Create(eigenvector2),
                Create(dashed_eigen1),
                Create(dashed_eigen2),
                Write(eigen_labels)
            )

        # Step 4: Demonstrate eigenvalues
        eigenvalue_labels = VGroup(
            MathTex(f"\\lambda_1 = {eigenvals[0]:.2f}", color=YELLOW),
            MathTex(f"\\lambda_2 = {eigenvals[1]:.2f}", color=RED)
        ).arrange(DOWN, buff=0.5).to_corner(UR)
        
        #create scaled eigenvector
        scaled_eigen1 = Arrow(ORIGIN, [eigenvals[0]*eigenvecs[0,0], eigenvals[0]*eigenvecs[1,0], 0], color=YELLOW, buff=0)
        scaled_eigen2 = Arrow(ORIGIN, [eigenvals[1]*eigenvecs[0,1], eigenvals[1]*eigenvecs[1,1], 0], color=RED, buff=0)
        with self.voiceover(text=f"Watch how each eigenvector scales by its eigenvalue. The first eigenvector scales by {eigenvals[0]:.2f}"):
            self.play(
                Write(eigenvalue_labels[0]),
                ReplacementTransform(eigenvector1, scaled_eigen1),
                FadeOut(eigenvector1),
                run_time=2
            )
            self.wait(1)
            
        with self.voiceover(text=f"And the second eigenvector scales by {eigenvals[1]:.2f}"):
            self.play(
                Write(eigenvalue_labels[1]),
                ReplacementTransform(eigenvector2, scaled_eigen2),
                FadeOut(eigenvector2),
                run_time=2
            )
            self.wait(1)

        # After finding the eigenvectors, add this section before the final equation
        # Create reverse eigenvectors
        reverse_eigen1 = Arrow(ORIGIN, [-eigenvecs[0,0], -eigenvecs[1,0], 0], color=YELLOW_D, buff=0)
        reverse_eigen2 = Arrow(ORIGIN, [-eigenvecs[0,1], -eigenvecs[1,1], 0], color=RED_D, buff=0)
        
        # Create scaled reverse eigenvectors
        scaled_reverse_eigen1 = Arrow(ORIGIN, [-eigenvals[0]*eigenvecs[0,0], -eigenvals[0]*eigenvecs[1,0], 0], color=YELLOW_D, buff=0)
        scaled_reverse_eigen2 = Arrow(ORIGIN, [-eigenvals[1]*eigenvecs[0,1], -eigenvals[1]*eigenvecs[1,1], 0], color=RED_D, buff=0)
        
        # Labels for reverse eigenvectors
        reverse_labels = VGroup(
            Text("Reverse Direction 1", color=YELLOW_D, font_size=12),
            Text("Reverse Direction 2", color=RED_D, font_size=12)
        )
        reverse_labels[0].next_to(reverse_eigen1, UP)
        reverse_labels[1].next_to(reverse_eigen2, DOWN)

        with self.voiceover(text="Interestingly, the reverse directions of our eigenvectors also maintain their orientation under transformation. These reversed vectors are also eigenvectors with the same eigenvalue, because the eigenvalue equation A(-v) = λ(-v) still holds true."):
            self.play(
                Create(reverse_eigen1),
                Create(reverse_eigen2),
                Write(reverse_labels)
            )
            self.wait(1)

        with self.voiceover(text=f"Just like their positive counterparts, these reversed eigenvectors scale by the same eigenvalues. The first eigenvector and its reverse both scale by {eigenvals[0]:.2f}. This is because multiplying by -1 doesn't change the eigenvalue relationship."):
            self.play(
                ReplacementTransform(reverse_eigen1, scaled_reverse_eigen1),
                run_time=2
            )
            self.wait(1)

        with self.voiceover(text=f"Similarly, both the second eigenvector and its reverse scale by {eigenvals[1]:.2f}. The negative direction is just as valid an eigenvector as the positive direction."):
            self.play(
                ReplacementTransform(reverse_eigen2, scaled_reverse_eigen2),
                run_time=2
            )
            self.wait(1)

        with self.voiceover(text="This symmetry reveals a fundamental property: eigenvectors come in pairs of opposite directions. Each line through the origin in an eigenvector direction represents a one-dimensional eigenspace, where every non-zero vector along that line is an eigenvector with the same eigenvalue."):
            # Create dashed lines connecting the pairs of eigenvectors
            eigen_line1 = DashedLine(
                start=scaled_reverse_eigen1.get_end(),
                end=scaled_eigen1.get_end(),
                color=YELLOW_D
            )
            eigen_line2 = DashedLine(
                start=scaled_reverse_eigen2.get_end(),
                end=scaled_eigen2.get_end(),
                color=RED_D
            )
            self.play(
                Create(eigen_line1),
                Create(eigen_line2)
            )
            self.wait(2)

        # Continue with the final equation as before
        final_equation = MathTex("A\\vec{v} = \\lambda\\vec{v}")
        equation_explanation = Text(
            "The transformation matrix A times an eigenvector v\n"
            "equals the same vector scaled by its eigenvalue λ",
            font_size=24
        )
        final_group = VGroup(final_equation, equation_explanation).arrange(DOWN, buff=0.3)
        final_group.shift(DOWN*2+RIGHT*3)
        
        with self.voiceover(text="This relationship is captured perfectly in the eigenvalue equation: A v equals lambda v. The transformation of an eigenvector is simply a scaling by its eigenvalue."):
            self.play(
                Write(final_group)
            )
            self.wait(2)

    def FindingEigenvalues(self):
        ##############################
        # Scene 7: How to Find Eigenvalues and Eigenvectors
        ##############################
        title = Text("How do we find these eigen-things?", font_size=36).to_edge(UP)
        
        # Use our matrix from previous examples
        matrix = [[2, 1], 
                  [1, 2]]
        
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}",
            font_size=36
        ).to_corner(UL)
        
        with self.voiceover(text="Now let's explore how to find eigenvalues and eigenvectors mathematically. We start with our familiar matrix A."):
            self.play(Write(title), Write(matrix_tex))
            self.wait(1)
        
        # Step 1: Show the eigenvalue equation
        step1 = MathTex("A\\vec{v} = \\lambda\\vec{v}")
        
        with self.voiceover(text="We start with the fundamental eigenvalue equation: A times vector v equals lambda times vector v."):
            self.play(Write(step1))
            self.wait(1)
        
        # Step 2: Add identity matrix
        step2 = MathTex("A\\vec{v} = \\lambda I \\vec{v}")
        
        with self.voiceover(text="Next, we introduce the identity matrix I to better manage the scalar lambda."):
            self.play(ReplacementTransform(step1, step2))
            self.wait(1)
        
        # Step 3: Move everything to LHS
        step3 = MathTex("A\\vec{v} - \\lambda I \\vec{v} = \\vec{0}")
        step3_alt = MathTex("(A - \\lambda I)\\vec{v} = \\vec{0}")
        
        with self.voiceover(text="We rearrange to bring all terms to the left-hand side, factoring out vector v."):
            self.play(ReplacementTransform(step2, step3))
            self.wait(1)
            self.play(ReplacementTransform(step3, step3_alt))
            self.wait(1)
        
        # Step 4: Explain non-trivial solutions
        explanation = Text(
            "For non-trivial solutions (v ≠ 0),\nwe need det(A - λI) = 0", 
            font_size=28
        ).next_to(step3_alt, DOWN, buff=0.5)
        
        with self.voiceover(text="For the equation to have non-trivial solutions where vector v is not zero, the determinant of A minus lambda I must equal zero."):
            self.play(Write(explanation))
            self.wait(1)
        
        # Step 5: Set up the characteristic equation
        identity = MathTex("I = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}")
        lambda_identity = MathTex("\\lambda I = \\begin{bmatrix} \\lambda & 0 \\\\ 0 & \\lambda \\end{bmatrix}")
        
        step5_setup = VGroup(identity, lambda_identity).arrange(DOWN, buff=0.3)
        step5_setup.next_to(explanation, DOWN, buff=0.5)
        
        with self.voiceover(text="Let's look at what lambda times the identity matrix means."):
            self.play(Write(step5_setup))
            self.wait(1)
        
        # Step 6: Form A - λI
        step6 = MathTex(
            "A - \\lambda I = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix} - "
            "\\begin{bmatrix} \\lambda & 0 \\\\ 0 & \\lambda \\end{bmatrix} = "
            "\\begin{bmatrix} 2-\\lambda & 1 \\\\ 1 & 2-\\lambda \\end{bmatrix}"
        )
        step6.next_to(step5_setup, DOWN, buff=0.5)
        
        with self.voiceover(text="Now we subtract lambda I from our matrix A, giving us a matrix with lambda terms on the main diagonal."):
            self.play(Write(step6))
            self.wait(1)
        
        # Step 7: Determinant calculation
        step7 = MathTex(
            "\\det(A - \\lambda I) = \\det\\begin{bmatrix} 2-\\lambda & 1 \\\\ 1 & 2-\\lambda \\end{bmatrix} = 0"
        )
        step7_calc = MathTex(
            "(2-\\lambda)(2-\\lambda) - (1)(1) = 0"
        )
        step7_expand = MathTex(
            "(2-\\lambda)^2 - 1 = 0"
        )
        step7_quadratic = MathTex(
            "\\lambda^2 - 4\\lambda + 3 = 0"
        )
        
        determinant_group = VGroup(step7, step7_calc, step7_expand, step7_quadratic).arrange(DOWN, buff=0.3)
        
        # Clean up the screen for better focus
        with self.voiceover(text="To find eigenvalues, we calculate the determinant of A minus lambda I and set it equal to zero."):
            self.play(
                FadeOut(step5_setup),
                FadeOut(step6),
                FadeOut(step3_alt),
                FadeOut(explanation),
                Write(step7)
            )
            self.wait(1)
        
        with self.voiceover(text="Computing this determinant, we multiply diagonals and subtract products of off-diagonal elements."):
            self.play(Write(step7_calc))
            self.wait(1)
        
        with self.voiceover(text="Simplifying this expression..."):
            self.play(Write(step7_expand))
            self.wait(1)
        
        with self.voiceover(text="...we get a quadratic equation in lambda."):
            self.play(Write(step7_quadratic))
            self.wait(1)
        
        # Step 8: Solve for eigenvalues
        eigenvalues = MathTex(
            "\\lambda = 1 \\text{ or } \\lambda = 3"
        ).next_to(step7_quadratic, DOWN, buff=0.5)
        
        with self.voiceover(text="Solving this quadratic equation, we find our eigenvalues are lambda equals 1 and lambda equals 3."):
            self.play(Write(eigenvalues))
            self.wait(1)
        
        # Step 9: Finding eigenvectors for λ=3
        eigenvector_title = Text("Finding Eigenvectors", font_size=32).to_edge(UP)
        
        step9_lambda1 = MathTex(
            "\\text{For } \\lambda = 3:\\quad (A - 3I)\\vec{v} = \\vec{0}"
        )
        step9_system1 = MathTex(
            "\\begin{bmatrix} 2-3 & 1 \\\\ 1 & 2-3 \\end{bmatrix}"
            "\\begin{bmatrix} v_1 \\\\ v_2 \\end{bmatrix} = "
            "\\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}"
        )
        step9_system1_simplified = MathTex(
            "\\begin{bmatrix} -1 & 1 \\\\ 1 & -1 \\end{bmatrix}"
            "\\begin{bmatrix} v_1 \\\\ v_2 \\end{bmatrix} = "
            "\\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}"
        )
        
        step9_equations1 = MathTex(
            "-v_1 + v_2 &= 0 \\\\",
            "v_1 - v_2 &= 0"
        )
        
        step9_solution1 = MathTex(
            "v_1 = v_2 \\Rightarrow \\vec{v} = c\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix} \\text{ for any } c \\neq 0"
        )
        
        eigenvector1_group = VGroup(step9_lambda1, step9_system1, step9_system1_simplified, step9_equations1, step9_solution1).arrange(DOWN, buff=0.3)
        
        with self.voiceover(text="Now, to find the eigenvector corresponding to lambda equals 3, we substitute this value back into our matrix equation."):
            self.play(
                FadeOut(title),
                FadeOut(step7),
                FadeOut(step7_calc),
                FadeOut(step7_expand),
                FadeOut(step7_quadratic),
                ReplacementTransform(eigenvalues, eigenvector_title)
            )
            self.play(Write(step9_lambda1))
            self.wait(1)
        
        with self.voiceover(text="We get a system of homogeneous linear equations."):
            self.play(Write(step9_system1))
            self.wait(1)
        
        with self.voiceover(text="Simplifying the coefficients..."):
            self.play(ReplacementTransform(step9_system1, step9_system1_simplified))
            self.wait(1)
        
        with self.voiceover(text="This gives us two equations."):
            self.play(Write(step9_equations1))
            self.wait(1)
        
        with self.voiceover(text="Solving this system, we find that v1 equals v2, giving us the eigenvector direction of 1, 1."):
            self.play(Write(step9_solution1))
            self.wait(1)
        
        # Step 10: Finding eigenvectors for λ=1
        step10_lambda2 = MathTex(
            "\\text{For } \\lambda = 1:\\quad (A - 1I)\\vec{v} = \\vec{0}"
        )
        step10_system2 = MathTex(
            "\\begin{bmatrix} 2-1 & 1 \\\\ 1 & 2-1 \\end{bmatrix}"
            "\\begin{bmatrix} v_1 \\\\ v_2 \\end{bmatrix} = "
            "\\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}"
        )
        step10_system2_simplified = MathTex(
            "\\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix}"
            "\\begin{bmatrix} v_1 \\\\ v_2 \\end{bmatrix} = "
            "\\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}"
        )
        
        step10_equations2 = MathTex(
            "v_1 + v_2 &= 0 \\\\",
            "v_1 + v_2 &= 0"
        )
        
        step10_solution2 = MathTex(
            "v_1 = -v_2 \\Rightarrow \\vec{v} = c\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} \\text{ for any } c \\neq 0"
        )
        
        eigenvector2_group = VGroup(step10_lambda2, step10_system2, step10_system2_simplified, step10_equations2, step10_solution2).arrange(DOWN, buff=0.3)
        
        with self.voiceover(text="Similarly, for lambda equals 1, we substitute and solve."):
            self.play(
                FadeOut(eigenvector1_group),
                Write(step10_lambda2)
            )
            self.wait(1)
        
        with self.voiceover(text="Again, we get a homogeneous system."):
            self.play(Write(step10_system2))
            self.wait(1)
        
        with self.voiceover(text="After simplification..."):
            self.play(ReplacementTransform(step10_system2, step10_system2_simplified))
            self.wait(1)
        
        with self.voiceover(text="We get a single independent equation."):
            self.play(Write(step10_equations2))
            self.wait(1)
        
        with self.voiceover(text="Solving this, we find that v1 equals negative v2, giving us the eigenvector direction of 1, negative 1."):
            self.play(Write(step10_solution2))
            self.wait(1)
        
        # Step 11: Verify the eigenvectors
        verify_title = Text("Verifying Our Solutions", font_size=32).to_edge(UP)
        
        verify1 = MathTex(
            "A\\vec{v}_1 &= \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}"
            "\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix} \\\\"
            "&= \\begin{bmatrix} 3 \\\\ 3 \\end{bmatrix} \\\\"
            "&= 3\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix} \\\\"
            "&= \\lambda_1 \\vec{v}_1"
        )
        
        verify2 = MathTex(
            "A\\vec{v}_2 &= \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}"
            "\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} \\\\"
            "&= \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} \\\\"
            "&= 1\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} \\\\"
            "&= \\lambda_2 \\vec{v}_2"
        )
        
        verification_group = VGroup(verify1, verify2).arrange(RIGHT, buff=1)
        
        with self.voiceover(text="Let's verify our solutions by checking that A times v equals lambda times v for each eigenvector."):
            self.play(
                FadeOut(eigenvector2_group),
                FadeOut(eigenvector_title),
                Write(verify_title)
            )
            self.play(Write(verify1))
            self.wait(1)
            self.play(Write(verify2))
            self.wait(1)
        
        # Final summary
        summary = VGroup(
            Text("The eigenvalues of A are λ₁ = 3 and λ₂ = 1", font_size=24),
            Text("With corresponding eigenvectors v₁ = [1, 1] and v₂ = [1, -1]", font_size=24),
            Text("These eigenvalues and eigenvectors completely characterize", font_size=24),
            Text("the behavior of the transformation represented by matrix A", font_size=24)
        ).arrange(DOWN, buff=0.3)
        
        with self.voiceover(text="In summary, we've found that our matrix A has eigenvalues 3 and 1, with corresponding eigenvectors [1,1] and [1,-1]. These eigenvalues and eigenvectors completely characterize the behavior of the transformation represented by our matrix."):
            self.play(
                FadeOut(verification_group),
                FadeOut(verify_title),
                FadeOut(matrix_tex),
                Write(summary)
            )
            self.wait(2)

        # After the verification section, add these new sections:

        # Section: Relationship between eigenvalues and determinant/trace
        relationship_title = Text("Eigenvalues, Determinant & Trace", font_size=32).to_edge(UP)

        trace_def = MathTex(
            "\\text{Trace}(A) = \\sum_{i} a_{ii} = a_{11} + a_{22} + ... + a_{nn}"
        )
        det_def = MathTex(
            "\\text{Determinant}(A) = |A|"
        )

        eigenvalue_properties = VGroup(trace_def, det_def).arrange(DOWN, buff=0.5)

        with self.voiceover(text="Now let's explore the important relationships between eigenvalues and two key matrix properties: the trace and determinant."):
            self.play(
                FadeOut(summary),
                Write(relationship_title),
                Write(eigenvalue_properties)
            )
            self.wait(1)

        # Eigenvalue-trace relationship
        trace_relation = MathTex(
            "\\text{Trace}(A) = \\sum_{i} \\lambda_i"
        )
        trace_example = MathTex(
            "\\text{For our matrix: } \\text{Trace}\\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix} = 2+2 = 4"
        )
        trace_verify = MathTex(
            "\\lambda_1 + \\lambda_2 = 3 + 1 = 4 = \\text{Trace}(A)"
        )

        trace_group = VGroup(trace_relation, trace_example, trace_verify).arrange(DOWN, buff=0.3)

        with self.voiceover(text="The trace of a matrix, which is the sum of its diagonal elements, equals the sum of all eigenvalues. For our matrix, the trace is 4, and indeed, our eigenvalues 3 and 1 sum to 4."):
            self.play(
                FadeOut(eigenvalue_properties),
                Write(trace_group)
            )
            self.wait(1)

        # Eigenvalue-determinant relationship
        det_relation = MathTex(
            "\\text{Determinant}(A) = \\prod_{i} \\lambda_i"
        )
        det_example = MathTex(
            "\\text{For our matrix: } \\text{Det}\\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix} = (2 \\times 2) - (1 \\times 1) = 3"
        )
        det_verify = MathTex(
            "\\lambda_1 \\times \\lambda_2 = 3 \\times 1 = 3 = \\text{Det}(A)"
        )

        det_group = VGroup(det_relation, det_example, det_verify).arrange(DOWN, buff=0.3)

        with self.voiceover(text="Similarly, the determinant of a matrix equals the product of all eigenvalues. Our matrix has determinant 3, which is exactly the product of our eigenvalues 3 and 1."):
            self.play(
                FadeOut(trace_group),
                Write(det_group)
            )
            self.wait(1)

        # Section: Visual examples of different eigenvalue types
        eigentype_title = Text("Geometric Meaning of Eigenvalues", font_size=32).to_edge(UP)

        with self.voiceover(text="Now, let's visualize what different types of eigenvalues mean geometrically. The sign and magnitude of eigenvalues tell us how the transformation affects space."):
            self.play(
                FadeOut(det_group),
                FadeOut(relationship_title),
                Write(eigentype_title)
            )
            self.wait(1)

        # Create a small coordinate system for demonstrations
        small_grid = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_opacity": 0.4,
                "stroke_width": 1,
                "stroke_color": GREY
            }
        )
        small_grid.shift(LEFT * 3)

        # Create a unit square for transformation demonstrations
        unit_square = Square(side_length=1, color=BLUE, fill_opacity=0.2)
        unit_square.move_to(small_grid.c2p(0.5, 0.5, 0))

        # Create a second grid for transformed shapes
        transformed_grid = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_opacity": 0.4,
                "stroke_width": 1,
                "stroke_color": GREY
            }
        )
        transformed_grid.shift(RIGHT * 3)

        # Case 1: Both eigenvalues > 1 (expansion)
        case1_matrix = [[2, 0], [0, 1.5]]
        case1_title = Text("Case 1: λ₁, λ₂ > 1", font_size=24, color=BLUE).next_to(small_grid, UP)
        case1_text = Text("Expansion in all directions", font_size=20).next_to(case1_title, UP)

        transformed_square1 = unit_square.copy()
        transformed_square1.apply_matrix(case1_matrix)
        transformed_square1.move_to(transformed_grid.c2p(0.5, 0.5, 0))

        with self.voiceover(text="When all eigenvalues are greater than 1, the transformation expands space in all directions. Vectors get longer, and areas increase."):
            self.play(
                Create(small_grid),
                Create(transformed_grid),
                Write(case1_title),
                Write(case1_text)
            )
            self.play(Create(unit_square))
            self.play(Create(transformed_square1))
            self.wait(1)

        # Case 2: One eigenvalue > 1, one < 1 (stretch in one direction, compress in another)
        case2_matrix = [[2, 0], [0, 0.5]]
        case2_title = Text("Case 2: λ₁ > 1, 0 < λ₂ < 1", font_size=24, color=GREEN).next_to(small_grid, UP)
        case2_text = Text("Stretch in one direction,\ncompress in another", font_size=20).next_to(case2_title, RIGHT)

        transformed_square2 = unit_square.copy()
        transformed_square2.apply_matrix(case2_matrix)
        transformed_square2.move_to(transformed_grid.c2p(0.5, 0.5, 0))

        with self.voiceover(text="When one eigenvalue is greater than 1 and another is between 0 and 1, the transformation stretches space in one direction while compressing it in another. This creates a directional distortion."):
            self.play(
                FadeOut(transformed_square1),
                FadeOut(case1_title),
                FadeOut(case1_text),
                Write(case2_title),
                Write(case2_text)
            )
            self.play(Create(transformed_square2))
            self.wait(1)

        # Case 3: Negative eigenvalue (reflection + scaling)
        case3_matrix = [[-1.5, 0], [0, 1.5]]
        case3_title = Text("Case 3: λ₁ < 0", font_size=24, color=RED).next_to(small_grid, UP)
        case3_text = Text("Reflection + scaling", font_size=20).next_to(case3_title, UP)

        transformed_square3 = unit_square.copy()
        transformed_square3.apply_matrix(case3_matrix)
        transformed_square3.move_to(transformed_grid.c2p(0.5, 0.5, 0))

        with self.voiceover(text="Negative eigenvalues indicate reflection along with scaling. The space flips across the axis corresponding to this eigenvalue, changing orientation."):
            self.play(
                FadeOut(transformed_square2),
                FadeOut(case2_title),
                FadeOut(case2_text),
                Write(case3_title),
                Write(case3_text)
            )
            self.play(Create(transformed_square3))
            self.wait(1)

        # Case 4: Eigenvalues = 1 (preservation)
        case4_matrix = [[1, 0], [0, 1]]
        case4_title = Text("Case 4: λ₁ = λ₂ = 1", font_size=24, color=YELLOW).next_to(small_grid, UP)
        case4_text = Text("Identity transformation\n(preservation)", font_size=20).next_to(case4_title, RIGHT)

        transformed_square4 = unit_square.copy()
        transformed_square4.apply_matrix(case4_matrix)
        transformed_square4.move_to(transformed_grid.c2p(0.5, 0.5, 0))

        with self.voiceover(text="When eigenvalues equal exactly 1, lengths and areas are preserved in those directions. This is the case with rotations and the identity transformation."):
            self.play(
                FadeOut(transformed_square3),
                FadeOut(case3_title),
                FadeOut(case3_text),
                Write(case4_title),
                Write(case4_text)
            )
            self.play(Create(transformed_square4))
            self.wait(1)

        # Special case: Complex eigenvalues (rotation + scaling)
        # We'll use a 2D rotation matrix combined with scaling
        angle = PI/6  # 30 degrees
        scale = 1.2
        case5_matrix = [
            [scale * np.cos(angle), -scale * np.sin(angle)], 
            [scale * np.sin(angle), scale * np.cos(angle)]
        ]
        case5_title = Text("Special Case: Complex Eigenvalues", font_size=24, color=PURPLE).next_to(small_grid, UP)
        case5_text = Text("Rotation + scaling", font_size=20).next_to(case5_title, UP)

        transformed_square5 = unit_square.copy()
        transformed_square5.apply_matrix(case5_matrix)
        transformed_square5.move_to(transformed_grid.c2p(0.5, 0.5, 0))

        with self.voiceover(text="When eigenvalues are complex, the transformation includes rotation. The real part determines scaling, while the imaginary part controls rotation. This often occurs in dynamic systems exhibiting oscillatory behavior."):
            self.play(
                FadeOut(transformed_square4),
                FadeOut(case4_title),
                FadeOut(case4_text),
                Write(case5_title),
                Write(case5_text)
            )
            self.play(Create(transformed_square5))
            self.wait(1)

        # Final summary about eigenvalue types
        eigenvalue_types_summary = VGroup(
            Text("Eigenvalues > 1: Expansion", font_size=20, color=BLUE),
            Text("Eigenvalues between 0 and 1: Contraction", font_size=20, color=GREEN),
            Text("Negative eigenvalues: Reflection + scaling", font_size=20, color=RED),
            Text("Complex eigenvalues: Rotation + scaling", font_size=20, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT)

        with self.voiceover(text="In summary, eigenvalues tell us how a transformation affects space: values greater than 1 cause expansion, values between 0 and 1 cause contraction, negative values cause reflection, and complex values cause rotation combined with scaling."):
            self.play(
                FadeOut(small_grid),
                FadeOut(transformed_grid),
                FadeOut(unit_square),
                FadeOut(transformed_square5),
                FadeOut(case5_title),
                FadeOut(case5_text),
                Write(eigenvalue_types_summary)
            )
            self.wait(2)

        # Final educational note
        application_title = Text("Significance in Applications", font_size=32).to_edge(UP)
        applications = VGroup(
            Text("System Stability: |λ| < 1 → stable system", font_size=20),
            Text("Principal Component Analysis: λ = variance in direction", font_size=20),
            Text("Quantum Mechanics: λ = observable measurement values", font_size=20),
            Text("Vibrational Analysis: λ = natural frequencies", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        with self.voiceover(text="The values of eigenvalues have profound significance in applications. In system stability analysis, eigenvalues with magnitude less than 1 indicate stable systems. In data science, eigenvalues represent variance along principal components. In quantum mechanics, eigenvalues correspond to observable measurements, and in mechanical engineering, they relate to natural frequencies of vibration."):
            self.play(
                FadeOut(eigenvalue_types_summary),
                FadeOut(eigentype_title),
                Write(application_title),
                Write(applications)
            )
            self.wait(2)

        conclusion = Text("Understanding eigenvalues gives deep insight into\nthe behavior of linear transformations", font_size=28)

        with self.voiceover(text="Understanding eigenvalues and eigenvector gives us deep insight into the behavior of linear transformations, Thanks for watching!"):
            self.play(
                FadeOut(application_title),
                FadeOut(applications),
                Write(conclusion)
            )
            self.wait(2)
if __name__ == "__main__":
    scene = EigenvalueVectorScene()
    scene.render()

