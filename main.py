# main.py
import sys
from input_processing import parse_input
from prompt_generation import generate_prompt
from code_generation import generate_code
from render import render_animation
from storage import save_record
from config import OUTPUT_DIR
from auto_fix import attempt_fix_code

def main():    
    # Get user input from the command line or other interfaces
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Please enter a math/physics problem description: ")
    
    print("\n🚀 Starting animation generation process...")
    
    question = None
    animation_prompt = None
    manim_code = None
    video_path = None
    error_msg = None

    try:
        # 1. Parse user input
        print("\n📝 Stage 1/5: Parsing user input...")
        question = parse_input(user_input)
        print("✅ Input parsed successfully")
        
        # 2. Call the LLM to generate the derivation process and animation description
        print("\n🤖 Stage 2/5: Generating animation description...")
        animation_prompt = generate_prompt(question)
        print("✅ Animation description generated")
        
        # 3. Call the coding LLM to generate Manim Python code
        print("\n💻 Stage 3/5: Generating Manim code...")
        manim_code = generate_code(animation_prompt)
        print("✅ Manim code generated")
        
        # 4. Render the Manim animation video with auto-fix attempts
        print("\n🎬 Stage 4/5: Rendering animation...")
        video_path, fix_attempts = attempt_fix_code(manim_code, max_attempts=2)
        
    except Exception as e:
        error_msg = f"Error: Animation generation failed due to: {str(e)}"
        print(f"\n❌ {error_msg}")
    
    finally:
        # 5. Save the record to local storage
        print("\n💾 Stage 5/5: Saving records...")
        save_record(
            question=question or user_input,
            animation_prompt=animation_prompt,
            manim_code=manim_code,
            video_path=video_path,
            error=error_msg,
            fix_attempts=fix_attempts if 'fix_attempts' in locals() else 0
        )
        print("✅ Records saved successfully")
        
        if not error_msg:
            print("\n✨ All stages completed successfully!")
        else:
            print(f"\n⚠️ Process completed with errors")


if __name__ == "__main__":
    main()
