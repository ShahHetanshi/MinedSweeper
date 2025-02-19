# MinedSweeper
```markdown
# ResearchReach: AI-Powered Research Simplifier 🎧📄✨  
*Transform academic papers into podcasts, videos, and visuals with one click.*

---

## 📌 Project Overview  
**ResearchReach** leverages generative AI to **automatically convert complex research papers** into engaging, layperson-friendly multimedia formats (audio, video, graphics). Designed for educators, journalists, and curious minds, it bridges the gap between academia and the public.  

![Demo Workflow](https://via.placeholder.com/800x400.png?text=Upload+Paper+->+Generate+->+Share!) *(Replace with a GIF/video demo)*  

---

## 🚀 Key Features  
- **AI Summarization**: Gemini + LangChain condense papers into plain-language summaries.  
- **Natural Audio**: ElevenLabs TTS with SSML tags for expressive, non-robotic narration.  
- **AI Visuals**: StarryAI generates context-aware images for key concepts.  
- **Auto-Video Synthesis**: Combine audio, images, and text into MP4 videos (MoviePy/FFmpeg).  
- **Drag-and-Drop Interface**: Zero training needed. Upload a PDF, get a podcast/video in minutes!  

---

## ⚙️ Installation  

### Prerequisites  
- Python 3.8+  
- API keys: [Google Gemini](https://ai.google.dev/), [ElevenLabs](https://elevenlabs.io/), [StarryAI](https://starryai.com/)  

### Steps  
1. Clone the repo:  
   ```bash  
   git clone https://github.com/SiddhDoshi1/MinedSweeper.git 
   cd ResearchReach  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
3. Create a `.env` file and add your API keys:  
   ```  
   GEMINI_API_KEY=your_key_here  
   ELEVENLABS_API_KEY=your_key_here  
   STARRYAI_API_KEY=your_key_here  
   ```  

---

## 🎬 Usage  
1. **Upload a PDF**: Drag-and-drop your research paper into the `/input` folder.  
2. **Choose the desired output**
3. **Get outputs**:  
   - Audio
   - Video
   - PPT
   - Blog
   - Graphics
   - Visualization

---

## 🛠️ Tech Stack  
- **Summarization**: Google Gemini + LangChain  
- **Text-to-Speech**: ElevenLabs API (SSML-enhanced)  
- **Image Generation**: StarryAI  
- **Video Editing**: MoviePy, PyDub
- **Interface**: ReactJS,css,html
- **PPT Generation**: pptx
- **Graphics**: wordcloud

---

**Requirements**
 
pdfplumber==0.10.0
pillow==10.3.0
langchain-google-genai==0.1.4
langchain==0.2.1
moviepy==1.0.3
requests==2.32.3
srt==3.5.3
elevenlabs==0.2.21
python-pptx
wordcloud 

---

## 🔍 Limitations & Future Work  
- **Single-paper processing** (batch support planned).  

---

Made with ❤️ by MinedSweeper. **Democratizing knowledge, one paper at a time.**  
```
