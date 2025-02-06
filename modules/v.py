from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

output_dir="outputs"
output_file_path = os.path.join(output_dir,"visual.png")

def func(content):
    """
    Generates a word cloud from the given content and saves it as an image file.

    Args:
        content (str): The text content to generate the word cloud from.
        output_file_path (str): The path where the word cloud image will be saved.
    """
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(content)

    # Save the word cloud to an image file
    wordcloud.to_file(output_file_path)

    print(f"Word cloud saved to {output_file_path}")
    
    return None