
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from docx import Document
from matcher import match_resume_jd
import io

app = FastAPI(title="Trendsetter AI Resume Helper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Trendsetter AI Resume Helper API ✅"}

@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.lower().endswith('.pdf'):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text = '\n'.join(page.extract_text() or "" for page in pdf.pages)
    else:  # DOCX
        doc = Document(io.BytesIO(content))
        text = '\n'.join(para.text for para in doc.paragraphs)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return {"resume": {"text": text, "lines": lines[:50]}}  # First 50 lines

@app.post("/api/match-jd")
async def match_jd(resume_text: str = Form(...), jd_text: str = Form(...)):
    result = match_resume_jd(resume_text, jd_text)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
