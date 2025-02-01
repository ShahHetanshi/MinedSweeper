from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, top_p=0.85)

def generate_content(text, template, **kwargs):
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": text, **kwargs})

def generate_summary(raw_text):
    summary = generate_content(raw_text, 
            "Generate a comprehensive summary in English focusing on key concepts:\n{text}")
    return (summary)

def generate_narrative(summary, language):
    """Generates language-specific narrative"""
    narrative_prompt = PromptTemplate.from_template(
        "Convert to {language} narrative for podcast:\n{summary}"
    )
    return (narrative_prompt | llm | StrOutputParser()).invoke({
        "summary": summary, 
        "language": language.capitalize()
    })

def generate_dialogue(summary,LANGUAGE):
        dialogue = generate_content(summary,
        "Create a natural {language} dialogue between Rahul (male) and Priya (female).\n"
        "Format strictly as:\nRahul: [emphasized text]\nPriya: [text?]\n...\n"
        "Use asterisks for emphasis and ? for questions. Keep sentences short.\n"
        "Focus on key concepts from:\n{text}. Use the summary as the source of discussion. Add some natural pauses and sounds like a normal human",
        language=LANGUAGE.capitalize())
        return (dialogue)


def generate_image_prompt(summary):
    image_prompt=generate_content(summary,
        "Generate 3 visual metaphors (40 words max) for key concepts in this text:\n{text}").split('\n')

    return (image_prompt)

def generate_blog_title(summary):
    blog_title=generate_content(summary,
        "Give me 1 and only 1 appropriate title for the blog which has the above content:\n{text}")

    return (blog_title)

def generate_reel_content(raw_text):
    reel_content=generate_content(raw_text,
        "Give me consise funny and interesting explaination in paragraph form of the following such that we can present it for atleast 30 second:\n{text}")

    return (reel_content)

def generate_video_content(raw_text):
    video_content=generate_content(raw_text,
        "Give me funny and interesting explaination of the following such that we can present it for atleast 2 minutes:\n{text}")

    return (video_content)