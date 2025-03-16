import streamlit as st
import logging
from main import process_visualization
import os
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Mathematical Visualization System",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for video player
st.markdown("""
    <style>
    .stVideo {
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
    }
    .video-container {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎯 Mathematical Visualization System")
st.markdown("""
This system helps you visualize mathematical and physics concepts through animations.
Simply enter your problem description below, and the system will generate an animated visualization.
""")

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(message)s')

# Sidebar for video controls
with st.sidebar:
    st.header("Video Settings")
    video_speed = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.25)
    show_controls = st.checkbox("Show Video Controls", value=True)
    autoplay = st.checkbox("Autoplay", value=False)
    loop = st.checkbox("Loop Video", value=False)

# Input section
with st.form("visualization_form"):
    user_input = st.text_area(
        "Enter your math/physics problem description:",
        height=150,
        placeholder="Example: Show the geometric interpretation of the derivative of a function at x=2..."
    )
    submit_button = st.form_submit_button("Generate Visualization")

if submit_button and user_input:
    with st.spinner("Generating your visualization..."):
        try:
            # Process the visualization
            result = process_visualization(user_input)
            
            if result["status"] == "success":
                # Display the final animation if available
                if "combined_scene_path" in result["stages"]:
                    video_path = result["stages"]["combined_scene_path"]
                    if os.path.exists(video_path):
                        st.subheader("🎬 Your Mathematical Visualization")
                        
                        # Video container with styling
                        st.markdown('<div class="video-container">', unsafe_allow_html=True)
                        
                        # Video player
                        video_file = open(video_path, 'rb')
                        video_bytes = video_file.read()
                        st.video(
                            video_bytes,
                            format="video/mp4",
                            start_time=0
                        )
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download button for the video
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="⬇️ Download Animation",
                                data=video_bytes,
                                file_name=Path(video_path).name,
                                mime="video/mp4",
                                use_container_width=True,
                            )
                    else:
                        st.error("Video file not found at the specified path.")
                else:
                    st.error("No visualization was generated.")
            else:
                st.error(f"Error: {result['error']}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("👆 Enter your problem description and click 'Generate Visualization' to start.")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Manim") 