import os

# HTML template for the blog with enhanced CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Post</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.8;
            margin: 0;
            padding: 0;
            background-color: #fafafa;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}
        h1 {{
            font-size: 2.8em;
            margin-bottom: 20px;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.2;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        p {{
            font-size: 1.2em;
            color: #555;
            margin-bottom: 20px;
        }}
        .content {{
            font-size: 1.1em;
            color: #444;
        }}
        .content p {{
            margin-bottom: 1.5em;
        }}
        .content p:first-of-type {{
            font-size: 1.3em;
            color: #2c3e50;
            line-height: 1.6;
        }}
        .author {{
            font-style: italic;
            color: #777;
            margin-top: 30px;
            border-top: 1px solid #eee;
            padding-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="content">
            {content}
        </div>
        <div class="author">Written by AI Blog Generator</div>
    </div>
</body>
</html>
"""

def generate_blog(title, content, output_dir="outputs", image_url=""):
    """
    Generates a blog post and saves it as an HTML file.
    
    Args:
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        output_dir (str): The directory to save the blog HTML file.
        image_url (str): The URL of the image to include in the blog post.
    """
    # Render the blog post using the template
    blog_html = HTML_TEMPLATE.format(
        title=title,
        content=content,
    )
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the blog post as an HTML file
    blog_file_path = os.path.join(output_dir, "blog.html")
    with open(blog_file_path, "w", encoding="utf-8") as file:
        file.write(blog_html)
    
    print(f"Blog generated and saved to {blog_file_path}")
    return blog_file_path