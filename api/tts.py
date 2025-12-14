from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/api/tts', methods=['POST'])
def tts_handler():
    try:
        # 1. Ambil data JSON yang dikirim Unity
        data = request.json
        text = data.get('text', 'Halo, ini tes suara')

        if not text:
            return {"error": "Text kosong"}, 400

        # 2. Generate Audio (simpan ke Memory/RAM, bukan file fisik)
        # Kita pakai io.BytesIO agar tidak perlu save ke harddisk server
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="id")
        tts.write_to_fp(mp3_fp)
        
        # Reset pointer file ke awal agar bisa dibaca
        mp3_fp.seek(0)

        # 3. Kirim balik sebagai file audio
        return send_file(
            mp3_fp,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="output.mp3"
        )

    except Exception as e:
        return {"error": str(e)}, 500

# Entry point untuk Vercel
if __name__ == '__main__':
    app.run()