import sys
print(sys.executable)
print(sys.path)
from flask import Flask, render_template, request, send_file
import os
import time
from scripts.generate_script import generate_script
from scripts.generate_tts import generate_tts
from scripts.generate_animated_video import generate_animated_video
from waitress import serve
import test_import  # TEMP: Just to test


app = Flask(__name__)
os.makedirs("static", exist_ok=True)

def cleanup_old_files(folder="static", age_limit_sec=600):
    """Delete audio/video files older than `age_limit_sec` seconds."""
    now = time.time()
    for filename in os.listdir(folder):
        if filename.endswith((".mp3", ".mp4")):
            path = os.path.join(folder, filename)
            if os.path.isfile(path) and now - os.path.getmtime(path) > age_limit_sec:
                try:
                    os.remove(path)
                    print(f"🧹 Removed old file: {path}")
                except Exception as e:
                    print(f"❗Error deleting {path}: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()

        if not prompt:
            return render_template("index.html", error="❗ Please enter a math prompt.", video_ready=False)

        print(f"📥 Received prompt: {prompt}")

        sentence = generate_script(prompt).strip()

        if not sentence or "Could not compute" in sentence:
            return render_template("index.html", error=f"❗ {sentence}", video_ready=False)

        # Create unique filenames using timestamp
        timestamp = str(int(time.time()))
        audio_filename = f"audio_{timestamp}.mp3"
        video_filename = f"math_lesson_{timestamp}.mp4"
        audio_path = os.path.join("static", audio_filename)
        video_path = os.path.join("static", video_filename)

        try:
            print("🧹 Cleaning up old files...")
            cleanup_old_files()

            print(f"🔊 Generating audio: {audio_path}")
            generate_tts(sentence, audio_path)

            print(f"🎞 Generating video: {video_path}")
            generate_animated_video(sentence, audio_path, video_path)

        except Exception as e:
            print(f"❗ Error during generation: {e}")
            return render_template("index.html", error=f"❗ Generation error: {e}", video_ready=False)

        print("✅ Successfully generated video!")
        return render_template("index.html", video_ready=True, video_path=video_path, video_filename=video_filename)


    return render_template("index.html", video_ready=False)

@app.route("/video/<path:filename>")
def serve_video(filename):
    video_path = os.path.join("static", filename)
    if os.path.exists(video_path):
        return send_file(video_path, mimetype="video/mp4")
    return "❗ Video not found", 404

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
