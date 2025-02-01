import os
import re
import time
import random
import requests
import pdfplumber
from PIL import Image, ImageDraw, ImageFont
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from moviepy.editor import *
import traceback
import datetime
import srt


# Configuration
# LANGUAGE = "english"  # Options: english, hindi, gujarati
SECTIONS_PER_IMAGE = 3
FONT_SIZE = 60
STARRY_API_KEY = "BlodgkIBFkqlY4k964rVFcuGomVzRg"
ELEVENLABS_API_KEY = "sk_ce9b7af7ab805a731e45b085c6f1c2ecb3919d9ddb903880"
os.environ['GOOGLE_API_KEY'] = "AIzaSyCWTJKkX5G7WB0Ooq5m0UzX-YRtiMjxvPo"
os.environ["IMAGEMAGICK_BINARY"] = r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

# ElevenLabs Configuration with multiple voices
ELEVENLABS_VOICES = {
    'male': [
        'TxGEqnHWrfWFTfGW9XjX',  # Deep male
        'AZnzlk1XvdvUeBnXmlld'   # Middle-aged male
    ],
    'female': [
        'EXAVITQu4vr4xnSDxMaL',  # Soft female
        '21m00Tcm4TlvDq8ikWAM',  # Energetic female
        'MF3mGyEYCl7XYWbV9V6O'   # Mature female
    ]
}


def generate_text_image(text, output_path, language='english'):
    try:
        img = Image.new('RGB', (1920, 1080), color='black')
        draw = ImageDraw.Draw(img)
        try:
            font_path = {
                'gujarati': 'NotoSansGujarati-Regular.ttf',
                'hindi': 'NotoSansHindi-Regular.ttf',
                'english': 'arial.ttf'
            }[language]
            font = ImageFont.truetype(font_path, FONT_SIZE)
        except (IOError, KeyError):
            font = ImageFont.load_default()
            print("Using default font")

        words = text.split()
        lines, current_line = [], []
        for word in words:
            if draw.textlength(' '.join(current_line + [word]), font=font) < 1800:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))

        y = (1080 - (len(lines) * (FONT_SIZE + 10))) // 2
        for line in lines:
            text_width = draw.textlength(line, font=font)
            draw.text(((1920 - text_width) // 2, y), line, font=font, fill="white")
            y += FONT_SIZE + 10

        img.save(output_path)
        return True
    except Exception as e:
        print(f"Text image error: {e}")
        return False

def add_ssml_effects(text, gender):
    """Enhance text with SSML tags for natural speech patterns"""
    # Add emphasis to words wrapped in asterisks
    # Add emphasis to words wrapped in asterisks (e.g., "*important*" → "<emphasis level='strong'>important</emphasis>")
    text = re.sub(r'\*(.*?)\*', r'<emphasis level="strong">\1</emphasis>', text)

    # Add pauses after punctuation
    text = re.sub(r'([,])(\s|$)', r'\1<break time="300ms"/>\2', text)  # Short pause for commas
    text = re.sub(r'([.!?])(\s|$)', r'\1<break time="800ms"/>\2', text)  # Longer pause for sentence-ending punctuation

    
    # Voice characteristics based on gender
    if gender == 'male':
        prosody = '<prosody pitch="low" rate="medium" volume="loud">'
    else:
        prosody = '<prosody pitch="medium" rate="medium" volume="soft">'
    
    return f'<speak>{prosody}{text}</prosody></speak>'

def generate_elevenlabs_audio(text, voice_id, output_path, gender):
    try:
        ssml_text = add_ssml_effects(text, gender)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": ssml_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.65,
                "similarity_boost": 0.75,
                "style": 0.4 if 'female' in voice_id else 0.2,
                "use_speaker_boost": True
            }
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        print(f"ElevenLabs API Error: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"Audio generation failed: {e}")
        return False

def generate_transcript(subtitles, output_folder):
    subs = []
    for idx, (start, end, text) in enumerate(subtitles, 1):
        subs.append(srt.Subtitle(
            index=idx,
            start=datetime.timedelta(seconds=start),
            end=datetime.timedelta(seconds=end),
            content=text
        ))
    
    transcript_path = os.path.join(output_folder, "transcript.srt")
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subs))
    return transcript_path

def process_pdf_to_audio(dialogue,LANGUAGE):
    try:
        # Audio Generation
        output_folder="outputs"
        selected_voices = {
            'male': random.choice(ELEVENLABS_VOICES['male']),
            'female': random.choice(ELEVENLABS_VOICES['female'])
        }

        audio_files = []
        subtitles = []
        start_time = 0

        for line in dialogue.split('\n'):
            line = line.strip()
            if not line or ':' not in line:
                continue

            speaker, text = line.split(':', 1)
            speaker = speaker.strip()
            text = text.strip()

            gender = 'male' if 'Rahul' in speaker else 'female'
            voice_id = selected_voices[gender]
            audio_path = os.path.join(output_folder, f"audio_{100+len(audio_files)}.mp3")
            
            if generate_elevenlabs_audio(text, voice_id, audio_path, gender):
                duration = AudioFileClip(audio_path).duration
                end_time = start_time + duration
                subtitles.append((start_time, end_time, text))
                audio_files.append(audio_path)
                start_time = end_time

        # Generate transcript
        generate_transcript(subtitles, output_folder)

        # Create final audio file
        audio = concatenate_audioclips([AudioFileClip(f) for f in audio_files])
        final_audio_path = os.path.join(output_folder, "final_audio.mp3")
        audio.write_audiofile(final_audio_path)

        for f in audio_files:
            os.remove(f)

        return True

    except Exception as e:
        print(f"Processing failed: {e}")
        traceback.print_exc()
        return False


def process_pdf_to_reel(dialogue,LANGUAGE,starry_images):
    try:
        # Audio Generation
        print(dialogue)
        output_folder="outputs"
        selected_voices = {
            'female': random.choice(ELEVENLABS_VOICES['female'])
        }

        audio_files = []
        subtitles = []
        start_time = 0

        for line in dialogue.split('\n'):
            line = line.strip()
            if not line or ':' not in line:
                continue

            speaker, text = line.split(':', 1)
            speaker = speaker.strip()
            text = text.strip()

            gender = 'female'
            voice_id = selected_voices[gender]
            audio_path = os.path.join(output_folder, f"audio_{500+len(audio_files)}.mp3")
            
            if generate_elevenlabs_audio(text, voice_id, audio_path, gender):
                duration = AudioFileClip(audio_path).duration
                end_time = start_time + duration
                subtitles.append((start_time, end_time, text))
                audio_files.append(audio_path)
                start_time = end_time

        # Generate transcript
        generate_transcript(subtitles, output_folder)

        # Create final audio file
        audio = concatenate_audioclips([AudioFileClip(f) for f in audio_files])
        final_audio_path = os.path.join(output_folder, "final_reel_audio.mp3")
        audio.write_audiofile(final_audio_path)
        # Video Assembly
        clips = []
        total_audio_duration = sum(AudioFileClip(f).duration for f in audio_files)
        current_video_duration = 0

        for idx, (start, end, text) in enumerate(subtitles):
            # Text Image
            img_path = os.path.join(output_folder, f"text_{idx}.png")
            if generate_text_image(text, img_path, LANGUAGE):
                clip_duration = end - start
                clips.append(ImageClip(img_path).set_duration(clip_duration))
                current_video_duration += clip_duration

                # Add AI image after specified number of sections
                if (idx + 1) % SECTIONS_PER_IMAGE == 0 and starry_images:
                    ai_duration = min(5, total_audio_duration - current_video_duration)
                    if ai_duration > 0:
                        ai_path = os.path.join(output_folder, f"ai_{len(clips)}.png")
                        with open(ai_path, 'wb') as f:
                            f.write(starry_images.pop(0))
                        clips.append(ImageClip(ai_path).set_duration(ai_duration))
                        current_video_duration += ai_duration

        # Final video composition
        video = concatenate_videoclips(clips)
        audio = concatenate_audioclips([AudioFileClip(f) for f in audio_files])
        
        # Sync audio and video
        final_video = video.set_audio(audio)
        if final_video.duration > audio.duration:
            final_video = final_video.subclip(0, audio.duration)

        final_video.write_videofile(
            os.path.join(output_folder, "reel_output.mp4"),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='ultrafast'
        )

        # Cleanup
        for f in audio_files:
            os.remove(f)

        return True

    except Exception as e:
        print(f"Processing failed: {e}")
        traceback.print_exc()
        return False

def process_pdf_to_video(dialogue,LANGUAGE,starry_images):
    try:
        # Audio Generation
        output_folder="outputs"
        selected_voices = {
            'male': random.choice(ELEVENLABS_VOICES['male']),
        }

        audio_files = []
        subtitles = []
        start_time = 0

        for line in dialogue.split('\n'):
            line = line.strip()
            if not line or ':' not in line:
                continue

            speaker, text = line.split(':', 1)
            speaker = speaker.strip()
            text = text.strip()

            gender = 'male'
            voice_id = selected_voices[gender]
            audio_path = os.path.join(output_folder, f"audio_{1000+len(audio_files)}.mp3")
            
            if generate_elevenlabs_audio(text, voice_id, audio_path, gender):
                duration = AudioFileClip(audio_path).duration
                end_time = start_time + duration
                subtitles.append((start_time, end_time, text))
                audio_files.append(audio_path)
                start_time = end_time

        # Generate transcript
        generate_transcript(subtitles, output_folder)

        # Create final audio file
        audio = concatenate_audioclips([AudioFileClip(f) for f in audio_files])
        final_audio_path = os.path.join(output_folder, "final_video_audio.mp3")
        audio.write_audiofile(final_audio_path)
        # Video Assembly
        clips = []
        total_audio_duration = sum(AudioFileClip(f).duration for f in audio_files)
        current_video_duration = 0

        for idx, (start, end, text) in enumerate(subtitles):
            # Text Image
            img_path = os.path.join(output_folder, f"text_{idx}.png")
            if generate_text_image(text, img_path, LANGUAGE):
                clip_duration = end - start
                clips.append(ImageClip(img_path).set_duration(clip_duration))
                current_video_duration += clip_duration

                # Add AI image after specified number of sections
                if (idx + 1) % SECTIONS_PER_IMAGE == 0 and starry_images:
                    ai_duration = min(5, total_audio_duration - current_video_duration)
                    if ai_duration > 0:
                        ai_path = os.path.join(output_folder, f"ai_{len(clips)}.png")
                        with open(ai_path, 'wb') as f:
                            f.write(starry_images.pop(0))
                        clips.append(ImageClip(ai_path).set_duration(ai_duration))
                        current_video_duration += ai_duration

        # Final video composition
        video = concatenate_videoclips(clips)
        audio = concatenate_audioclips([AudioFileClip(f) for f in audio_files])
        
        # Sync audio and video
        final_video = video.set_audio(audio)
        if final_video.duration > audio.duration:
            final_video = final_video.subclip(0, audio.duration)

        final_video.write_videofile(
            os.path.join(output_folder, "video_output.mp4"),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            preset='ultrafast'
        )

        # Cleanup
        for f in audio_files:
            os.remove(f)

        return True

    except Exception as e:
        print(f"Processing failed: {e}")
        traceback.print_exc()
        return False