from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import io
import os
import tempfile
import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import pipeline

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    input_type: str
    content: Optional[str] = None
    format: str
    domain: str = "general"

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def extract_text_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def get_domain_config(domain):
    """Get domain-specific configuration for summarization."""
    configs = {
        "education": {
            "sentences_count": 6,
            "max_length": 250,
            "min_length": 100,
            "style": "academic",
            "keywords": ["learning", "education", "study", "research", "academic"]
        },
        "medical": {
            "sentences_count": 7,
            "max_length": 300,
            "min_length": 150,
            "style": "medical",
            "keywords": ["health", "medical", "clinical", "patient", "treatment"]
        },
        "business": {
            "sentences_count": 5,
            "max_length": 200,
            "min_length": 100,
            "style": "business",
            "keywords": ["business", "market", "company", "strategy", "financial"]
        },
        "technical": {
            "sentences_count": 8,
            "max_length": 350,
            "min_length": 150,
            "style": "technical",
            "keywords": ["technical", "system", "technology", "engineering", "development"]
        },
        "news": {
            "sentences_count": 4,
            "max_length": 150,
            "min_length": 75,
            "style": "news",
            "keywords": ["news", "report", "update", "current", "event"]
        },
        "general": {
            "sentences_count": 5,
            "max_length": 200,
            "min_length": 100,
            "style": "general",
            "keywords": []
        }
    }
    return configs.get(domain, configs["general"])

def format_summary(summary, format_type, domain_config):
    """Format the summary based on the chosen format and domain style."""
    if format_type == "bullet":
        points = summary.split(". ")
        formatted = "\n".join([f"• {point.strip()}" for point in points if point.strip()])
        return f"<div class='domain-{domain_config['style']}'>{formatted}</div>"
    elif format_type == "paragraph":
        return f"<p class='domain-{domain_config['style']}'>{summary}</p>"
    else:  # detailed
        paragraphs = summary.split("\n\n")
        formatted = "\n".join([f"<p class='domain-{domain_config['style']}'>{p.strip()}</p>" 
                             for p in paragraphs if p.strip()])
        return formatted

def summarize_text(text, summary_format, domain="general"):
    """Generate a domain-specific summary of the text."""
    domain_config = get_domain_config(domain)
    
    # Initialize the appropriate summarizer based on format and domain
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    if summary_format == "bullet":
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, sentences_count=domain_config["sentences_count"])
        summary_text = ". ".join([str(sentence) for sentence in summary])
    elif summary_format == "paragraph":
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count=domain_config["sentences_count"])
        summary_text = " ".join([str(sentence) for sentence in summary])
    else:  # detailed
        # Use LSA for detailed summaries as well, but with more sentences
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count=domain_config["sentences_count"] * 2)
        summary_text = " ".join([str(sentence) for sentence in summary])
    
    # Format the summary according to domain and format specifications
    return format_summary(summary_text, summary_format, domain_config)

@app.post("/api/summarize")
async def summarize_content(req: SummarizeRequest):
    if not req.content:
        raise HTTPException(status_code=400, detail="Content is required")
    try:
        if req.input_type == "url":
            text = extract_text_from_url(req.content)
        else:
            text = req.content
        summary = summarize_text(text, req.format, req.domain)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize/file")
async def summarize_file(
    file: UploadFile = File(...), 
    format: str = Form(...),
    domain: str = Form(default="general")
):
    try:
        suffix = os.path.splitext(file.filename)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        if suffix == ".pdf":
            text = extract_text_from_pdf(tmp_path)
        elif suffix == ".docx":
            text = extract_text_from_docx(tmp_path)
        elif suffix in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            text = extract_text_from_image(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        os.unlink(tmp_path)

        summary = summarize_text(text, format, domain)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
