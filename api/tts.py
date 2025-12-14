from flask import Flask, request, make_response
from gtts import gTTS
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app) # Izinkan akses dari WebGL mana saja

@app.route('/api/tts', methods=['POST'])
def tts_handler():
    try:
        # 1. Validasi Input JSON
        if not request.is_json:
             return {"error": "Header Content-Type harus application/json"}, 400

        data = request.json
        text = data.get('text', '')

        if not text:
            return {"error": "Text kosong"}, 400

        # 2. Generate Audio ke Memory
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="id")
        tts.write_to_fp(mp3_fp)
        
        # Penting: Kembalikan pointer ke awal file
        mp3_fp.seek(0)
        
        # 3. Buat Response Manual (Lebih Stabil untuk WebGL)
        # Membaca seluruh bytes audio
        audio_bytes = mp3_fp.read()
        
        response = make_response(audio_bytes)
        response.headers.set('Content-Type', 'audio/mpeg')
        response.headers.set('Content-Disposition', 'inline; filename=output.mp3')
        # Header ini membantu browser tahu kapan download selesai
        response.headers.set('Content-Length', str(len(audio_bytes)))
        
        return response

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run()
