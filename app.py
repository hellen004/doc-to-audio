import streamlit as st
from doc_to_audio import extract_text_from_file, text_to_audio  # Import from your main script
import os

st.title("Document to Audio Converter")

# File uploader
uploaded_file = st.file_uploader("Upload a document (TXT, PDF, DOCX)", type=['txt', 'pdf', 'docx'])

# Options
use_online = st.checkbox("Use online TTS (better quality, requires internet)", value=False)
lang = st.text_input("Language code (e.g., 'en')", value='en')
speed = st.slider("Speech speed (offline only)", min_value=100, max_value=200, value=150)

if uploaded_file:
    # Save uploaded file temporarily
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    if st.button("Convert to Audio"):
        try:
            text = extract_text_from_file(temp_path)
            output_file = "output.mp3"
            text_to_audio(text, output_file, use_online=use_online, lang=lang, speed=speed)
            
            # Provide download link
            with open(output_file, 'rb') as audio_file:
                st.download_button("Download Audio", data=audio_file, file_name=output_file)
            st.success("Conversion complete!")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.remove(temp_path)  # Clean up
            if os.path.exists(output_file):
                os.remove(output_file)  # Optional: Clean up after download