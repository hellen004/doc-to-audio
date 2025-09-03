# Document-to-Audio Converter

A simple Python command-line tool that converts documents (TXT, PDF, DOCX) into MP3 audio files using text-to-speech (TTS). Supports offline (pyttsx3) and online (gTTS) modes.

## Features
- Extracts text from TXT, PDF, and DOCX files.
- Converts text to speech with customizable speed and language.
- Saves output as MP3.
- Handles basic errors like unsupported formats or empty text.

## Requirements
- Python 3.10+ (download from python.org).
- FFmpeg (for MP3 export): Download from ffmpeg.org and add to PATH.
- Libraries: Install via pip (see installation below).

## Installation
1. Clone the repository:
git clone https://github.com/your-username/doc-to-audio.git
cd doc-to-audio

2. Install dependencies:
pip install pyttsx3 gtts PyPDF2 python-docx pydub

3. Install FFmpeg:
- Windows: Download build, extract, add `bin` to PATH (search "edit environment variables").
- macOS: `brew install ffmpeg` (install Homebrew first).
- Linux: `sudo apt install ffmpeg`.

## Usage
Run the script with:
python doc_to_audio.py <input_file> [options]

- `<input_file>`: Path to your document (e.g., `C:\path\to\file.pdf`).
- Options:
  - `--output <file.mp3>`: Custom output name (default: output.mp3).
  - `--online`: Use online TTS (gTTS, requires internet, better quality).
  - `--lang <code>`: Language (default: en).
  - `--speed <int>`: Speech speed (offline only, default: 150).

Example:
python doc_to_audio.py C:\Users\PC\Downloads\example.pdf --output my_audio.mp3 --online --speed 180


## Notes
- For scanned PDFs (images, no selectable text), text extraction may fail. Add OCR (e.g., pytesseract) manually.
- Offline TTS uses system voices; quality varies by OS.
- Tested on Windows; should work on macOS/Linux with minor tweaks.

## License
MIT License (feel free to use and modify).