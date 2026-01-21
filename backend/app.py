"""
Trendsetter AI Resume Helper - Main API
ATS-optimized resume analysis and optimization platform
"""

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pdfplumber
from docx import Document
import io
from typing import Optional, List
from datetime import datetime

# Import our modules
from matcher import match_resume_jd
from ats_checker import ATSChecker
from resume_parser import ResumeParser
from grammar_checker import GrammarChecker
from optimizer import ResumeOptimizer
from database import init_db, get_db, Job, Resume, Keyword, AnalysisHistory

app = FastAPI(title="Trendsetter AI Resume Helper", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Initialize checkers
ats_checker = ATSChecker()
resume_parser = ResumeParser()
grammar_checker = GrammarChecker()
optimizer = ResumeOptimizer()

@app.get("/")
def root():
    return {"message": "Trendsetter AI Resume Helper API ✅", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume file (PDF or DOCX)"""
    try:
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                text = '\n'.join(page.extract_text() or "" for page in pdf.pages)
        elif file.filename.lower().endswith('.docx'):
            doc = Document(io.BytesIO(content))
            text = '\n'.join(para.text for para in doc.paragraphs)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or DOCX")
        
        # Parse resume
        parsed_data = resume_parser.parse(text)
        
        return {
            "filename": file.filename,
            "text": text,
            "parsed": parsed_data,
            "word_count": len(text.split())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/api/analyze-resume")
async def analyze_resume(
    resume_text: str = Form(...),
    filename: Optional[str] = Form(None)
):
    """Full resume analysis: ATS check + grammar + parsing"""
    try:
        # Run all analyses
        ats_result = ats_checker.check_compatibility(resume_text, 'pdf')
        grammar_result = grammar_checker.check(resume_text)
        parsed_data = resume_parser.parse(resume_text)
        
        return {
            "filename": filename or "resume.pdf",
            "ats_analysis": ats_result,
            "grammar_analysis": grammar_result,
            "parsed_data": parsed_data,
            "overall_score": round((ats_result['score'] + grammar_result['readability_score']) / 2, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.post("/api/match-job")
async def match_job(
    resume_text: str = Form(...),
    job_description: str = Form(...),
    job_title: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Match resume against job description"""
    try:
        # Run matching
        match_result = match_resume_jd(resume_text, job_description)
        
        # Run ATS check
        ats_result = ats_checker.check_compatibility(resume_text, 'pdf')
        
        # Run grammar check
        grammar_result = grammar_checker.check(resume_text)
        
        # Generate optimization suggestions
        optimization = optimizer.optimize(
            resume_text,
            match_result.get('missing_keywords', []),
            ats_result.get('issues', []),
            grammar_result.get('issues', [])
        )
        
        # Save to history
        history = AnalysisHistory(
            resume_name=job_title or "Unnamed Resume",
            job_title=job_title or "Unnamed Job",
            score=match_result.get('score', 0),
            ats_score=ats_result.get('score', 0),
            missing_keywords=match_result.get('missing_keywords', []),
            suggestions=optimization.get('priority_fixes', [])
        )
        db.add(history)
        db.commit()
        
        return {
            "match_result": match_result,
            "ats_result": ats_result,
            "grammar_result": grammar_result,
            "optimization": optimization,
            "overall_score": round((match_result['score'] + ats_result['score']) / 2, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching job: {str(e)}")

@app.post("/api/save-job")
async def save_job(
    title: str = Form(...),
    description: str = Form(...),
    role_type: str = Form("Other"),
    company: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Save job description to database"""
    try:
        # Extract keywords from job description
        from matcher import KeywordMatcher
        matcher = KeywordMatcher()
        keywords = list(matcher._extract_keywords(description))
        
        # Save job
        job = Job(
            title=title,
            company=company,
            description=description,
            role_type=role_type,
            keywords=keywords
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Update keyword library
        for keyword in keywords[:20]:  # Top 20 keywords
            existing = db.query(Keyword).filter(
                Keyword.keyword == keyword,
                Keyword.role_type == role_type
            ).first()
            
            if existing:
                existing.frequency += 1
            else:
                new_keyword = Keyword(
                    keyword=keyword,
                    role_type=role_type,
                    frequency=1,
                    importance_score=1.0
                )
                db.add(new_keyword)
        
        db.commit()
        
        return {
            "id": job.id,
            "title": job.title,
            "role_type": job.role_type,
            "keywords_extracted": len(keywords)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving job: {str(e)}")

@app.get("/api/jobs")
async def get_jobs(
    role_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all saved jobs, optionally filtered by role type"""
    try:
        query = db.query(Job)
        
        if role_type and role_type != "All":
            query = query.filter(Job.role_type == role_type)
        
        jobs = query.order_by(Job.created_at.desc()).all()
        
        return {
            "total": len(jobs),
            "jobs": [
                {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "role_type": job.role_type,
                    "keywords": job.keywords[:10] if job.keywords else [],
                    "created_at": job.created_at.isoformat()
                }
                for job in jobs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching jobs: {str(e)}")

@app.get("/api/jobs/{role_type}")
async def get_jobs_by_role(role_type: str, db: Session = Depends(get_db)):
    """Get jobs by specific role type"""
    return await get_jobs(role_type=role_type, db=db)

@app.post("/api/save-resume")
async def save_resume(
    name: str = Form(...),
    profile_type: str = Form("General"),
    content: str = Form(...),
    file_path: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Save resume profile to database"""
    try:
        resume = Resume(
            name=name,
            profile_type=profile_type,
            content=content,
            file_path=file_path
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {
            "id": resume.id,
            "name": resume.name,
            "profile_type": resume.profile_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving resume: {str(e)}")

@app.get("/api/resumes")
async def get_resumes(db: Session = Depends(get_db)):
    """Get all saved resume profiles"""
    try:
        resumes = db.query(Resume).order_by(Resume.created_at.desc()).all()
        
        return {
            "total": len(resumes),
            "resumes": [
                {
                    "id": resume.id,
                    "name": resume.name,
                    "profile_type": resume.profile_type,
                    "created_at": resume.created_at.isoformat()
                }
                for resume in resumes
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resumes: {str(e)}")

@app.get("/api/keyword-library/{role_type}")
async def get_keyword_library(role_type: str, db: Session = Depends(get_db)):
    """Get keyword library for specific role type"""
    try:
        keywords = db.query(Keyword).filter(
            Keyword.role_type == role_type
        ).order_by(Keyword.frequency.desc()).all()
        
        return {
            "role_type": role_type,
            "total": len(keywords),
            "keywords": [
                {
                    "keyword": kw.keyword,
                    "frequency": kw.frequency,
                    "importance_score": kw.importance_score
                }
                for kw in keywords[:100]  # Top 100
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching keywords: {str(e)}")

@app.post("/api/optimize-resume")
async def optimize_resume_endpoint(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """Get optimization suggestions for resume"""
    try:
        # Get match result for missing keywords
        match_result = match_resume_jd(resume_text, job_description)
        
        # Get ATS issues
        ats_result = ats_checker.check_compatibility(resume_text, 'pdf')
        
        # Get grammar issues
        grammar_result = grammar_checker.check(resume_text)
        
        # Generate optimization
        optimization = optimizer.optimize(
            resume_text,
            match_result.get('missing_keywords', []),
            ats_result.get('issues', []),
            grammar_result.get('issues', [])
        )
        
        return optimization
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")

@app.get("/api/analysis-history")
async def get_analysis_history(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get past analysis history"""
    try:
        history = db.query(AnalysisHistory).order_by(
            AnalysisHistory.created_at.desc()
        ).limit(limit).all()
        
        return {
            "total": len(history),
            "history": [
                {
                    "id": h.id,
                    "resume_name": h.resume_name,
                    "job_title": h.job_title,
                    "score": h.score,
                    "ats_score": h.ats_score,
                    "missing_keywords": h.missing_keywords[:5] if h.missing_keywords else [],
                    "created_at": h.created_at.isoformat()
                }
                for h in history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
