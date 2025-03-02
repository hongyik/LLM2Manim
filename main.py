# main.py
import sys
from input_processing import parse_input
from prompt_generation import generate_prompt
from code_generation import generate_code
from render import render_animation
from storage import save_record
from config import OUTPUT_DIR

def main():    
    # Get user input from the command line or other interfaces
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Please enter a math/physics problem description: ")
    
    # try:
        # 1. Parse user input
        question = parse_input(user_input)
        
        # 2. Call the LLM to generate the derivation process and animation description
        animation_prompt = generate_prompt(question)
        
        # 3. Call the coding LLM to generate Manim Python code
        manim_code = generate_code(animation_prompt)
        
        # 4. Render the Manim animation video
        video_path = render_animation(manim_code, output_dir=OUTPUT_DIR)
        
        # 5. Save the record to local storage
        save_record(question, manim_code, video_path)
    
    # except Exception as e:
    #   print(f"Error: Animation generation failed due to: {e}")


if __name__ == "__main__":
    main()

