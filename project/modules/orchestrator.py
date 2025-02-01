import os
import requests
from datetime import datetime
from config import OUTPUTS_DIR, DEFAULT_PARAMS
from . import pdf_processor, text_processor, image_generator, audio_generator, video_producer, ppt, blog, v
import shutil

class ProcessingPipeline:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.output_dir=f"outputs"
        output_folder = f"outputs"
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)
        
    def run_pipeline(self, languages):
        print("Received runpipe")
        # Extract PDF text
        raw_text = pdf_processor.extract_text_from_pdf(self.pdf_path).replace("**", "").replace("*","")
        if not raw_text:
            return False
        
        # Generate summary and narratives
        summary = text_processor.generate_summary(raw_text).replace("**", "").replace("*","")

        dialogue = text_processor.generate_dialogue(summary,languages[0]).replace("**", "").replace("*","")

        blog_title = text_processor.generate_blog_title(summary).replace("**", "").replace("*","")

        reel_content = text_processor.generate_reel_content(raw_text).replace("**", "").replace("*","")

        image_prompts = text_processor.generate_image_prompt(reel_content)
        
        video_content = text_processor.generate_video_content(raw_text).replace("**", "").replace("*","")

        video_image_prompts = text_processor.generate_image_prompt(video_content)
        print(reel_content)
        # Generate PPT
        ppt_output_path = os.path.join(self.output_dir, "output.pptx")
        ppt.text_to_ppt(summary, template_file="modules/your_template.pptx", output_file=ppt_output_path, theme="professional")

        # Generate StarryAI images from English narrative
        starry_images_reel = []
        for prompt in image_prompts[:2]:
            if url := image_generator.create_starry_image(prompt):
                if img_content := requests.get(url).content:
                    starry_images_reel.append(img_content)

        starry_images_video = []
        for prompt in video_image_prompts[:2]:
            if url := image_generator.create_starry_image(prompt):
                if img_content := requests.get(url).content:
                    starry_images_video.append(img_content)

        print("Starry Sucess")

        audio_generator.process_pdf_to_audio(dialogue,languages[0])
        audio_generator.process_pdf_to_reel(reel_content,languages[0],starry_images_reel)
        audio_generator.process_pdf_to_video(video_content,languages[0],starry_images_video)

        # First process for reel
        # reel_success = audio_generator.process_pdf_to_reel(reel_content, languages[0], starry_images_reel)

        # # Run the second process for video only if the first one was successful
        # if reel_success:
        #     video_success = audio_generator.process_pdf_to_video(video_content, languages[0], starry_images_video)
        #     if video_success:
        #         print("Both processes completed successfully.")
        #     else:
        #         print("Video process failed.")
        # else:
        #     print("Reel process failed.")


        # Generate blog
        blog.generate_blog(title=blog_title, content=summary)
        
        v.func(content=summary)
        
        return self.output_dir