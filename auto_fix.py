from openai import OpenAI
import logging
from config import GPT4_API_KEY, Free_Web, OUTPUT_DIR
from render import render_animation
import traceback

def generate_fix(code: str, error_msg: str) -> str:
    """
    Call GPT API directly to fix Manim code errors.
    
    Args:
        code (str): The code that needs fixing
        error_msg (str): The error message to address
    
    Returns:
        str: The fixed code
    """
    try:
        client = OpenAI(api_key=GPT4_API_KEY, base_url=Free_Web)
        
        system_prompt = """You are an expert Manim developer. Your task is to fix errors in Manim code while preserving its original functionality.
        Provide ONLY the corrected code without any explanations or markdown formatting."""
        
        fix_prompt = f"""
        The following Manim script has an error:

        {code}

        Error: {error_msg}

        Please correct this script while keeping its original intent.
        Ensure it is fully functional with correct imports and syntax.
        Return the corrected code.
        """

        print("🤖 Consulting GPT for code fix...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": fix_prompt}
            ],
            temperature=0  # Set to 0 for more consistent outputs
        )
        
        fixed_code = response.choices[0].message.content
        return fixed_code

    except Exception as e:
        logging.error(f"Failed to call GPT for code fix: {e}")
        raise RuntimeError(f"Failed to generate fix: {str(e)}")

def attempt_fix_code(manim_code: str, max_attempts: int = 3) -> tuple[str, int]:
    """
    Attempts to render Manim code and fix any errors that occur.
    
    Args:
        manim_code (str): The Manim code to render
        max_attempts (int): Maximum number of fix attempts
    
    Returns:
        tuple: (video_path, attempts_made)
            - video_path: Path to the rendered video if successful
            - attempts_made: Number of fix attempts made
    """
    attempts = 0
    current_code = manim_code
    last_error = None

    while attempts < max_attempts:
        try:
            # Try to render the current code
            print(f"\n🎬 Rendering attempt {attempts + 1}/{max_attempts}...")
            video_path = render_animation(current_code, output_dir=OUTPUT_DIR)
            print(f"✅ Animation rendered successfully: {video_path}")
            return video_path, attempts  # Success!
            
        except Exception as render_error:
            attempts += 1
            render_error = traceback.format_exc()
            last_error = str(render_error)
            print(f"\n⚠️ Render attempt {attempts} failed: {last_error}")
            
            if attempts < max_attempts:
                try:
                    print(f"🔧 Attempting to fix code...")
                    current_code = generate_fix(current_code, last_error)
                    print("✅ Fixed code generated, retrying render...")
                except Exception as fix_error:
                    print(f"❌ Fix attempt {attempts} failed: {str(fix_error)}")
            else:
                print(f"❌ Maximum attempts ({max_attempts}) reached")
                raise RuntimeError(f"Failed to render after {attempts} attempts. Final error: {last_error}")

    # This should never be reached due to the raise above, but including for completeness
    raise RuntimeError(f"Failed to render after {attempts} attempts. Final error: {last_error}") 