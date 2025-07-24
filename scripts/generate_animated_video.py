from moviepy.editor import ImageSequenceClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os
import shutil
import platform

def generate_animated_video(text, audio_path, output_video_path="static/math_lesson.mp4"):
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    frames = []

    try:
        print("🔊 Loading audio...")
        audio = AudioFileClip(audio_path)
        duration = max(audio.duration, 1)
        print(f"⏳ Audio duration: {duration:.2f} seconds")

        words = text.split()

        try:
            if platform.system() == "Windows":
                font_path = "arial.ttf"
            else:
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

            font = ImageFont.truetype(font_path, 120)  # ✅ Bigger text
        except:
            font = ImageFont.load_default()

        for i in range(1, len(words) + 1):
            img = Image.new("RGB", (1280, 720), color="grey")  # White background
            draw = ImageDraw.Draw(img)
            current_text = " ".join(words[:i])
            current_text = current_text.replace("+", "+").replace("=", "=")

            bbox = draw.textbbox((0, 0), current_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((1280 - text_width) // 2, (720 - text_height) // 2)

            draw.text(position, current_text, fill="black", font=font)  # Black large text

            frame_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
            img.save(frame_path)
            frames.append(frame_path)

        fps = max(1, len(frames) / duration)
        print(f"📸 Total frames: {len(frames)}, FPS: {fps:.2f}")

        if not output_video_path.endswith(".mp4"):
            output_video_path += ".mp4"

        print(f"🎞️ Writing video to: {output_video_path}")

        clip = ImageSequenceClip(frames, fps=fps).set_audio(audio)
        clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
        clip.close()
        audio.close()

        print(f"✅ Video generation complete! 📁 Saved to: {os.path.abspath(output_video_path)}")

    except Exception as e:
        raise RuntimeError(f"❗ Error generating video: {e}")

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
