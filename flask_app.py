from flask import Flask, request, send_file, jsonify
from doc_to_audio import extract_text_from_file, text_to_audio
import os
import uuid

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}"
    file.save(temp_path)
    
    try:
        text = extract_text_from_file(temp_path)
        output_file = "output.mp3"
        use_online = request.form.get('online', 'false').lower() == 'true'
        lang = request.form.get('lang', 'en')
        speed = int(request.form.get('speed', 150))
        
        text_to_audio(text, output_file, use_online=use_online, lang=lang, speed=speed)
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(output_file):
            os.remove(output_file)

@app.route('/')
def index():
    return app.send_static_file('upload.html')

if __name__ == '__main__':
    app.run(debug=True)