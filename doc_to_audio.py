import os
import pyttsx3  # Offline TTS
from gtts import gTTS  # Online TTS alternative
import PyPDF2  # PDF extraction
from docx import Document  # DOCX extraction
from pydub import AudioSegment  # For audio export (if needed for concatenation)
import argparse
import time 

def extract_text_from_file(file_path):
    """Extract text from TXT, PDF, or DOCX files."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif ext == '.pdf':
        text = ''
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # Skip empty pages
                    text += page_text + '\n'
        if not text.strip():  # If no text extracted, use OCR
        print("No text found with standard extraction. Attempting OCR...")
        import pytesseract
        from pdf2image import convert_from_path  # Install if needed: pip install pdf2image
        # Note: pdf2image requires poppler; download from blog.alivate.com.au/poppler-windows and add to PATH
        
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image, lang='eng') + '\n'  # Change lang as needed
    
    if not text.strip():
        raise ValueError("No text extracted from PDF even with OCR.")
    return text
    
    elif ext == '.docx':
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
        if not text:
            raise ValueError("No text extracted from DOCX.")
        return text
    
    else:
        raise ValueError("Unsupported file format. Supported: TXT, PDF, DOCX.")
        

def text_to_audio(text, output_file, use_online=False, lang='en', speed=150):
    """Convert text to audio and save as MP3, handling large texts by chunking."""
    # Ensure output ends with .mp3
    if not output_file.endswith('.mp3'):
        output_file += '.mp3'
    
    # Split text into chunks (by paragraphs)
    chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
    if not chunks:
        raise ValueError("No text chunks to convert.")
    
    full_audio = AudioSegment.empty()  # To concatenate segments
    
    if use_online:
        # Online: gTTS (chunk and concatenate)
        for i, chunk in enumerate(chunks):
            tts = gTTS(text=chunk, lang=lang, slow=False)
            temp_mp3 = f"temp_chunk_{i}.mp3"
            tts.save(temp_mp3)
            segment = AudioSegment.from_mp3(temp_mp3)
            full_audio += segment
            os.remove(temp_mp3)  # Clean up
    else:
        # Offline: pyttsx3 (chunk and concatenate)
        import tempfile
        engine = pyttsx3.init()
        engine.setProperty('rate', speed)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        for voice in voices:
            if lang in voice.languages or 'en' in voice.languages:
                engine.setProperty('voice', voice.id)
                break
        
        for i, chunk in enumerate(chunks):
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_file_path = temp_wav.name
            engine.save_to_file(chunk, temp_file_path)
            engine.runAndWait()
            segment = AudioSegment.from_wav(temp_file_path)
            full_audio += segment
            
            # Clean up with retry
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    os.remove(temp_file_path)
                    break
                except PermissionError:
                    if attempt < max_attempts - 1:
                        time.sleep(0.5)
                    else:
                        print(f"Warning: Could not delete temp file {temp_file_path}.")
        
        engine.stop()
    
    # Export final concatenated audio
    full_audio.export(output_file, format='mp3')       

def main():
    parser = argparse.ArgumentParser(description="Convert documents to audio files.")
    parser.add_argument('input_file', type=str, help="Path to the input document (TXT, PDF, DOCX).")
    parser.add_argument('--output', type=str, default='output.mp3', help="Output audio file name (default: output.mp3).")
    parser.add_argument('--online', action='store_true', help="Use online TTS (gTTS) instead of offline.")
    parser.add_argument('--lang', type=str, default='en', help="Language code (e.g., 'en', 'fr').")
    parser.add_argument('--speed', type=int, default=150, help="Speech speed (words per minute, offline only).")
    
    args = parser.parse_args()
    
    try:
        text = extract_text_from_file(args.input_file)
        text_to_audio(text, args.output, use_online=args.online, lang=args.lang, speed=args.speed)
        print(f"Success! Audio saved as {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()