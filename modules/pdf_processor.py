import pdfplumber

def extract_text_from_pdf(pdf_path):
    "Recieved PDF"
    """Extracts text from PDF document"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
            return '\n'.join(full_text)
    except Exception as e:
        print(f"PDF Extraction Error: {e}")
        return None