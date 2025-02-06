import os
import subprocess
from pydub import AudioSegment

def create_video(image_dir, audio_path, output_path):
    "recieved crevid"
    """Combines images and audio into video"""
    try:
        images = sorted([img for img in os.listdir(image_dir) if img.endswith(".png")], 
                       key=lambda x: int(x.split('_')[1].split('.')[0]))
        
        if not images:
            raise ValueError("No valid PNG images found")
            
        audio = AudioSegment.from_file(audio_path)
        total_duration = len(audio)
        duration_per_image = total_duration / len(images)
        
        with open("temp_input.txt", "w") as f:
            for img in images:
                f.write(f"file '{os.path.join(image_dir, img)}'\n")
                f.write(f"duration {duration_per_image/1000}\n")
        
        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', 'temp_input.txt', '-i', audio_path,
            '-c:v', 'libx264', '-preset', 'medium',
            '-r', '25', '-pix_fmt', 'yuv420p',
            '-vf', 'fps=25', '-shortest',
            '-c:a', 'aac', '-b:a', '192k',
            output_path
        ], check=True)
        return True
    except Exception as e:
        print(f"Video creation failed: {e}")
        return False
    finally:
        if os.path.exists("temp_input.txt"):
            os.remove("temp_input.txt")