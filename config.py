# config.py
# LLM API keys and options
GPT4_API_KEY = "sk-TmeRzxqaqBwUEfz2FHi3S73k9siM6gsBBrPDc0JXkcZb8xH9"  # "Your OpenAI API key"
CLAUDE_API_KEY = "Claude API key"
USE_CLAUDE = False  # Toggle whether to use Claude; otherwise, GPT-4 will be used.
Free_Web = "https://api.chatanywhere.tech/v1"

# Manim configuration
MANIM_CLI_PATH = "C:\\Users\\kehon\\AppData\\Roaming\\Python\\Python312\\Scripts\\manim.exe"  # Path to the Manim executable
MANIM_RENDER_QUALITY = "l"  # Rendering quality options: low (l), medium (m), high (h), etc.


# Output directory
OUTPUT_DIR = "./outputs"
def prompt_template(content):
    # Prompt template for prompt generation
    system_p= (
        "You are a mathematical and physics visualization assistant, highly skilled in converting "
        "complex mathematical and physics concepts into structured animations using Manim. "
        "Your task is to generate a detailed step-by-step animation description that can be directly used "
        "to create Manim animations for educational videos. "
        
        "For broad concepts, follow this structured format:\n"
        "1️⃣ **Definition** - Briefly introduce the concept.\n"
        "2️⃣ **Formula** - Display key formulas related to the topic.\n"
        "3️⃣ **Derivation** - Show the step-by-step derivation of the formula with animated sequences.\n"
        "4️⃣ **Example** - Provide a real-world example or application, animated step by step.\n"
        "5️⃣ **Conclusion** - Summarize the key takeaways and reinforce learning."

        "For specific problem-solving requests, adapt accordingly, ensuring a structured breakdown "
        "of problem setup, solution steps, and results."

        "🔹 **Always Include the Following in Your Response:**\n"
        "- **2D Animations**: Describe how each mathematical/physics element should be visually represented.\n"
        "- **Formula Derivations**: Specify how formulas should appear, transform, and be highlighted.\n"
        "- **Voiceover Scripts**: Provide narration text using `Manim_voiceover` (e.g., `from manim_voiceover import VoiceoverScene`).\n"
        "- **Manim Packages**: List required Manim and Python packages (e.g., `Manim`, `Manim_voiceover`, `numpy`).\n"

        "🔹 **Animation Details Should Include:**\n"
        "- **Object Appearances & Movements**: How elements appear, move, and transform.\n"
        "- **Highlighting & Colors**: Specify color coding and highlighting effects.\n"
        "- **Annotations & Labels**: Text descriptions, vector arrows, or graphical explanations.\n"
        "- **Scene Transitions**: Describe smooth transitions between steps to maintain viewer engagement.\n"

        "Your output should be **highly detailed and optimized** for direct use with an AI code generator for Manim animations."
    )
    user_p = (
        f"I am creating a Manim animation based on the following topic or problem:\n\n"
        f"🔹 **User Query:** {content}\n\n"
        "📌 **Your task:**\n"
        "- Detect the nature of the query (broad concept or specific problem) and adapt your response accordingly.\n"
        "- Provide a structured breakdown **if the query is conceptual** (Definition → Formula → Derivation → Example → Conclusion).\n"
        "- Generate detailed animation descriptions that specify **how each part should be visualized**.\n"
        "- Include **step-by-step formula derivation animations**.\n"
        "- Write a **voiceover script** using `Manim_voiceover` to narrate each step.\n"
        "- Specify necessary Manim and Python packages required for implementation.\n"
        "- Ensure that every animation description is **clear enough for direct Manim code generation**.\n"
        
        "🎬 **Example of an effective animation description:**\n"
        "- 'First, a coordinate axis fades in. Then, a projectile trajectory is drawn as a dashed curve, labeled with its equations...'\n"
        "- 'The velocity vector is shown as an arrow, dynamically changing as the projectile moves...'\n"
        "- 'The equation transforms term by term, with each transformation animated sequentially...'\n"

        "🔹 **Generate the most detailed and structured response possible, ensuring AI-assisted code generation is seamless.**"
    )
    return system_p,user_p
def prompt_template_code(animation_prompt):
    system_prompt = (
        "You are an experienced Python developer and a Manim expert. "
        "Your task is to generate high-quality Manim animation code based on a given description. "
        "The output must be a **fully functional** Python script that follows best practices for Manim scripting.\n\n"
        
        "🔹 **Code Structure:**\n"
        "1. The code must define a Manim `Scene` class called `GenScene` (subclassing `Scene` or `VoiceoverScene` if needed).\n"
        "2. All animations must be implemented in the `construct(self)` method.\n"
        "3. Use appropriate Manim objects:\n"
        "   - `Text()` for text elements\n"
        "   - `MathTex()` for mathematical formulas\n"
        "   - `Table()` for structured data\n"
        "4. Include all necessary imports (`manim`, `numpy`, etc.).\n"
        "5. Follow Manim best practices for animations and timing.\n\n"
        
        "🔹 **Error Prevention Guidelines:**\n"
        "- Ensure all objects added to `self.play()` are valid Manim objects (e.g., `Text()`, `Circle()`, `MathTex()`).\n"
        "- Avoid using unsupported data types inside Manim objects (e.g., strings inside `VGroup()`, strings inside 'Table()').\n"
        "- Include debugging messages (e.g., `print()` statements) to track progress if needed.\n"
        "- Use `self.wait(1)` at the end of animations to ensure smooth transitions.\n"
        
        "🔹 **Example:**\n"
        "```python\n"
        "from manim import *\n"
        "from manim_voiceover import VoiceoverScene\n"
        "from manim_voiceover.services.gtts import GTTSService\n"
        "\n"
        "class GenScene(VoiceoverScene):\n"
        "    def construct(self):\n"
        "        # Set up voiceover service\n"
        "        self.set_speech_service(GTTSService())\n"
        "        \n"
        "        # Create and animate title\n"
        "        title = Text('Logic Gates', font_size=48)\n"
        "        with self.voiceover(text='Let\\'s learn about logic gates.') as tracker:\n"
        "            self.play(Write(title))\n"
        "        self.wait(1)\n"
        "        self.play(title.animate.to_edge(UP))\n"
        "        \n"
        "        # Create and animate truth table\n"
        "        table_data = [\n"
        "            ['A', 'B', 'A ∧ B'],\n"
        "            ['0', '0', '0'],\n"
        "            ['0', '1', '0'],\n"
        "            ['1', '0', '0'],\n"
        "            ['1', '1', '1']\n"
        "        ]\n"
        "        table = Table(\n"
        "            table_data,\n"
        "            include_outer_lines=True,\n"
        "            line_config={'stroke_width': 1}\n"
        "        )\n"
        "        \n"
        "        with self.voiceover(text='Here is the truth table for AND gate.') as tracker:\n"
        "            self.play(Create(table))\n"
        "        self.wait(1)\n"
        "```"
    )

    user_prompt = (
        f"Generate Manim code for the following animation description:\n\n{animation_prompt}\n\n"
        "Requirements:\n"
        "- Create a `GenScene` class with complete animation implementation\n"
        "- Include all necessary imports and setup\n"
        "- Use appropriate Manim objects and animations\n"
        "- Add smooth transitions and proper timing\n"
        "- Ensure proper voiceover integration if needed\n"
        "- Include clear comments for code readability\n"
        "- Test the code to ensure it runs without errors"
    )
    
    return system_prompt, user_prompt