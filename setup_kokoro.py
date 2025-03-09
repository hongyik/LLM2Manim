import os
import requests

# Define file URLs
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin"

# Define file paths
MODEL_PATH = "kokoro-v0_19.onnx"
VOICES_PATH = "voices.bin"

def download_file(url, filepath):
    """Download a file if it doesn't already exist."""
    if not os.path.exists(filepath):
        print(f"Downloading {filepath}...")
        response = requests.get(url, stream=True)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"✅ Downloaded: {filepath}")
    else:
        print(f"✔️ {filepath} already exists, skipping download.")

# Run downloads
download_file(MODEL_URL, MODEL_PATH)
download_file(VOICES_URL, VOICES_PATH)
