import os
import pyttsx3  # Offline TTS
from gtts import gTTS  # Online TTS alternative
import PyPDF2  # PDF extraction
from docx import Document  # DOCX extraction
from pydub import AudioSegment  # For audio export (if needed for concatenation)
import argparse

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
        if not text:
            raise ValueError("No text extracted from PDF. It might be scanned—consider adding OCR.")
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
    """Convert text to audio and save as MP3."""
    # Ensure output ends with .mp3
    if not output_file.endswith('.mp3'):
        output_file += '.mp3'
    
    if use_online:
        # Online: gTTS (requires internet, saves directly as MP3)
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
    else:
        # Offline: pyttsx3 (saves to temp WAV, then convert to MP3)
        import tempfile
        engine = pyttsx3.init()
        engine.setProperty('rate', speed)  # Words per minute
        engine.setProperty('volume', 1.0)  # Max volume
        voices = engine.getProperty('voices')
        # Select a voice (e.g., first matching language)
        for voice in voices:
            if lang in voice.languages or 'en' in voice.languages:
                engine.setProperty('voice', voice.id)
                break
        
        # Save to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_file_path = temp_wav.name
        engine.save_to_file(text, temp_file_path)
        engine.runAndWait()
        
        # Convert WAV to MP3 using pydub
        audio = AudioSegment.from_wav(temp_file_path)
        audio.export(output_file, format='mp3')
        
        # Clean up temp WAV
        os.remove(temp_file_path)
        

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