import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from config import FONT_DIR, DEFAULT_PARAMS, STARRY_API_KEY

def create_starry_image(prompt):
    try:
        response = requests.post(
            "https://api.starryai.com/creations/",
            json={
                "model": "detailedIllustration",
                "aspectRatio": "square",
                "prompt": prompt[:750],
                "images": 1,
                "steps": 50
            },
            headers={"X-API-Key": STARRY_API_KEY}
        )
        if response.status_code == 200:
            creation_id = response.json().get('id')
            start_time = time.time()
            while time.time() - start_time < 300:
                status_resp = requests.get(
                    f"https://api.starryai.com/creations/{creation_id}",
                    headers={"X-API-Key": STARRY_API_KEY}
                )
                if status_resp.json().get('status') == 'completed':
                    return status_resp.json()['images'][0]['url']
                time.sleep(10)
        return None
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None

# def generate_text_image(text, output_path, language='english'):
#     "Recieved text_image"
#     """Generates text overlay image with proper font handling"""
#     try:
#         font_size = DEFAULT_PARAMS['font_size']
#         font_path = os.path.join(FONT_DIR, DEFAULT_PARAMS['font_map'][language])
        
#         img = Image.new('RGB', (1920, 1080), color='black')
#         draw = ImageDraw.Draw(img)
        
#         try:
#             font = ImageFont.truetype(font_path, font_size)
#         except:
#             font = ImageFont.load_default()

#         # Text wrapping logic
#         lines = []
#         current_line = []
#         for word in text.split():
#             test_line = ' '.join(current_line + [word])
#             bbox = draw.textbbox((0, 0), test_line, font=font)
#             if bbox[2] < 1800:
#                 current_line.append(word)
#             else:
#                 lines.append(' '.join(current_line))
#                 current_line = [word]
#         lines.append(' '.join(current_line))

#         # Calculate vertical position
#         total_height = len(lines) * (font_size + 10)
#         y = (1080 - total_height) // 2
        
#         # Draw each line
#         for line in lines:
#             bbox = draw.textbbox((0, 0), line, font=font)
#             x = (1920 - bbox[2]) // 2
#             draw.text((x, y), line, font=font, fill="white")
#             y += font_size + 10

#         img.save(output_path, format='PNG', optimize=True)
#         return True
#     except Exception as e:
#         print(f"Text image generation failed: {e}")
#         return False

# def generate_ai_image(prompt):
#     """Generates AI image using StarryAI API"""
#     url = "https://api.starryai.com/creations/"
#     payload = {
#         "model": "detailedIllustration",
#         "aspectRatio": "square",
#         "highResolution": True,
#         "images": 1,
#         "steps": 50,
#         "initialImageMode": "color",
#         "prompt": prompt[:750]
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "X-API-Key": STARRY_API_KEY
#     }
    
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         if response.status_code == 200:
#             creation_id = response.json().get('id')
#             return _poll_for_image(creation_id)
#     except Exception as e:
#         print(f"StarryAI API Error: {e}")
#     return None

# def _poll_for_image(creation_id, timeout=300):
#     """Polls StarryAI API for generated image"""
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         response = requests.get(
#             f"https://api.starryai.com/creations/{creation_id}",
#             headers={"accept": "application/json", "X-API-Key": STARRY_API_KEY}
#         )
#         data = response.json()
#         if data['status'] == 'completed':
#             return [img['url'] for img in data['images'] if img['url']]
#         time.sleep(10)
#     return None