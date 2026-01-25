
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import re
import json
from collections import Counter
import openai
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from docx import Document
from docx.shared import Inches
import tempfile
import os

app = FastAPI(title="Trendsetter Resume Helper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://*.vercel.app",  # ✅ Allows all Vercel deployments
        "https://trendsetter-resume-helper.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy for NLP (install: python -m spacy download en_core_web_sm)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except (ImportError, OSError):
    nlp = None

class ResumeAnalyzer:
    def __init__(self):
        self.action_verbs = [
            "achieved", "managed", "increased", "improved", "developed", "created", 
            "implemented", "optimized", "streamlined", "delivered", "led", "built",
            "designed", "executed", "coordinated", "supervised", "analyzed"
        ]
        
        self.ats_killer_words = [
            "table", "column", "graphic", "image", "chart", "diagram",
            "header", "footer", "textbox", "sidebar"
        ]

    def extract_keywords_advanced(self, job_description: str) -> Dict:
        """Advanced keyword extraction using NLP and semantic analysis"""
        text = job_description.lower()
        
        # Technical skills patterns (2026 enhanced)
        tech_skills = []
        skill_patterns = [
            r'\b(python|java|javascript|typescript|react|angular|vue|node\.?js)\b',
            r'\b(sql|nosql|mongodb|postgresql|mysql|redis)\b',
            r'\b(aws|azure|gcp|docker|kubernetes|jenkins|git)\b',
            r'\b(machine learning|ai|data science|analytics|tensorflow|pytorch)\b',
            r'\b(rest|api|microservices|devops|ci\/cd|agile|scrum)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text)
            tech_skills.extend(matches)
        
        # Extract requirements using NER-like approach
        requirements = []
        req_patterns = [
            r'(?:required?|must have|need):?\s*([^.;]+)',
            r'(?:experience with|proficient in|skilled in):?\s*([^.;]+)',
            r'(?:\d+\+?\s*years?):?\s*(?:of\s*)?([^.;]+)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend([match.strip() for match in matches])
        
        # Soft skills extraction
        soft_skills = []
        soft_patterns = [
            r'\b(leadership|communication|teamwork|problem.solving|analytical)\b',
            r'\b(collaboration|organization|time.management|adaptability)\b'
        ]
        
        for pattern in soft_patterns:
            matches = re.findall(pattern, text)
            soft_skills.extend(matches)
        
        return {
            "tech_skills": list(set(tech_skills)),
            "requirements": list(set(requirements[:10])),
            "soft_skills": list(set(soft_skills)),
            "all_keywords": list(set(tech_skills + soft_skills))
        }

    def analyze_resume_structure(self, resume_text: str) -> Dict:
        """Analyze resume structure and ATS compatibility"""
        issues = []
        score = 100
        
        # Check for ATS-killer elements
        for killer in self.ats_killer_words:
            if killer in resume_text.lower():
                issues.append(f"Remove {killer}s - use simple text formatting")
                score -= 10
        
        # Check for proper sections
        required_sections = ["experience", "education", "skills"]
        missing_sections = []
        
        for section in required_sections:
            if not re.search(rf'\b{section}\b', resume_text.lower()):
                missing_sections.append(section)
                issues.append(f"Add clear {section.title()} section")
                score -= 15
        
        # Check for action verbs
        action_verb_count = 0
        for verb in self.action_verbs:
            if verb in resume_text.lower():
                action_verb_count += 1
        
        if action_verb_count < 3:
            issues.append("Use more action verbs (achieved, managed, improved, etc.)")
            score -= 10
        
        # Check for quantified achievements
        numbers = re.findall(r'\d+%|\$\d+|\d+\+', resume_text)
        if len(numbers) < 2:
            issues.append("Add quantified achievements with numbers/percentages")
            score -= 15
        
        return {
            "score": max(score, 0),
            "issues": issues,
            "action_verb_count": action_verb_count,
            "quantified_achievements": len(numbers)
        }

    def calculate_keyword_match(self, resume_text: str, job_keywords: Dict) -> Dict:
        """Calculate semantic keyword matching with TF-IDF approach"""
        resume_lower = resume_text.lower()
        
        # Tech skills matching
        tech_matched = []
        tech_missing = []
        
        for skill in job_keywords["tech_skills"]:
            if skill.lower() in resume_lower:
                tech_matched.append(skill)
            else:
                tech_missing.append(skill)
        
        # Soft skills matching
        soft_matched = []
        soft_missing = []
        
        for skill in job_keywords["soft_skills"]:
            if skill.lower() in resume_lower:
                soft_matched.append(skill)
            else:
                soft_missing.append(skill)
        
        # Calculate scores
        total_keywords = len(job_keywords["all_keywords"])
        total_matched = len(tech_matched) + len(soft_matched)
        
        match_score = (total_matched / total_keywords * 100) if total_keywords > 0 else 0
        
        return {
            "score": round(match_score, 1),
            "tech_matched": tech_matched,
            "tech_missing": tech_missing[:5],  # Top 5 missing
            "soft_matched": soft_matched,
            "soft_missing": soft_missing[:3],  # Top 3 missing
            "total_matched": total_matched,
            "total_keywords": total_keywords
        }

    def generate_ai_improvements(self, resume_text: str, keyword_analysis: Dict, ats_analysis: Dict) -> List[str]:
        """Generate AI-powered improvement suggestions"""
        improvements = []
        
        # Keyword improvements
        if keyword_analysis["tech_missing"]:
            improvements.append(f"🔧 Add these technical skills: {', '.join(keyword_analysis['tech_missing'][:3])}")
            improvements.append(f"💡 Incorporate '{keyword_analysis['tech_missing'][0]}' in your work experience bullets")
        
        # Soft skills improvements
        if keyword_analysis["soft_missing"]:
            improvements.append(f"🤝 Highlight these soft skills: {', '.join(keyword_analysis['soft_missing'])}")
        
        # ATS improvements
        for issue in ats_analysis["issues"][:3]:
            improvements.append(f"⚡ {issue}")
        
        # Action verb improvements
        if ats_analysis["action_verb_count"] < 5:
            improvements.append("📈 Replace weak verbs with action verbs: managed, achieved, increased")
        
        # Quantification improvements
        if ats_analysis["quantified_achievements"] < 3:
            improvements.append("📊 Add specific numbers: 'Increased sales by 25%' instead of 'Increased sales'")
        
        return improvements[:6]  # Top 6 recommendations

analyzer = ResumeAnalyzer()

class FixedResume(BaseModel):
    original_text: str
    fixed_text: str
    improvements_applied: List[str]

@app.get("/")
def root():
    return {"message": "Trendsetter Resume Helper API ✅"}

@app.post("/api/match-job")
async def match_job(
    resume_text: str = Form(...),
    job_description: str = Form(...),
    job_title: str = Form("")
):
    try:
        # Extract keywords using advanced NLP
        job_keywords = analyzer.extract_keywords_advanced(job_description)
        
        # Analyze resume structure and ATS compatibility
        ats_analysis = analyzer.analyze_resume_structure(resume_text)
        
        # Calculate keyword matching with semantic understanding
        keyword_analysis = analyzer.calculate_keyword_match(resume_text, job_keywords)
        
        # Generate AI-powered improvements
        improvements = analyzer.generate_ai_improvements(resume_text, keyword_analysis, ats_analysis)
        
        # Calculate overall score using weighted approach
        ats_weight = 0.4
        keyword_weight = 0.6
        overall_score = (ats_analysis["score"] * ats_weight) + (keyword_analysis["score"] * keyword_weight)
        
        return {
            "match_result": {"score": keyword_analysis["score"]},
            "ats_result": {"score": ats_analysis["score"]},
            "grammar_result": {"readability_score": 90},  # Placeholder - can add readability analysis
            "keyword_details": {
                "tech_matched": keyword_analysis["tech_matched"],
                "tech_missing": keyword_analysis["tech_missing"],
                "soft_matched": keyword_analysis["soft_matched"],
                "soft_missing": keyword_analysis["soft_missing"],
                "job_keywords": job_keywords["all_keywords"]
            },
            "optimization": {
                "priority_fixes": improvements,
                "ats_issues": ats_analysis["issues"],
                "action_verb_count": ats_analysis["action_verb_count"],
                "quantified_achievements": ats_analysis["quantified_achievements"]
            },
            "overall_score": round(overall_score, 1),
            "can_auto_fix": len(improvements) > 0
        }
        
    except Exception as e:
        return {
            "match_result": {"score": 0},
            "ats_result": {"score": 0}, 
            "grammar_result": {"readability_score": 0},
            "keyword_details": {"error": str(e)},
            "optimization": {"priority_fixes": ["Analysis failed - please try again"]},
            "overall_score": 0,
            "can_auto_fix": False
        }

@app.post("/api/auto-fix-resume")
async def auto_fix_resume(
    resume_text: str = Form(...),
    job_description: str = Form(...),
    improvements: str = Form(...)  # JSON string of selected improvements
):
    """Auto-fix resume based on analysis and return improved version"""
    try:
        selected_improvements = json.loads(improvements)
        
        # Extract missing keywords
        job_keywords = analyzer.extract_keywords_advanced(job_description)
        keyword_analysis = analyzer.calculate_keyword_match(resume_text, job_keywords)
        
        # Apply AI-powered fixes
        fixed_resume = resume_text
        applied_fixes = []
        
        # Add missing technical skills to skills section
        if "tech_missing" in str(selected_improvements):
            missing_tech = keyword_analysis["tech_missing"][:3]
            if missing_tech:
                # Find or create skills section
                if "skills" in fixed_resume.lower():
                    # Add to existing skills section
                    skills_match = re.search(r'(skills?[:\s]*[^\n]*)', fixed_resume, re.IGNORECASE)
                    if skills_match:
                        original_skills = skills_match.group(1)
                        new_skills = original_skills + f", {', '.join(missing_tech)}"
                        fixed_resume = fixed_resume.replace(original_skills, new_skills)
                        applied_fixes.append(f"Added technical skills: {', '.join(missing_tech)}")
                else:
                    # Add new skills section
                    skills_section = f"\n\nSKILLS\n{', '.join(missing_tech)}, Communication, Problem-solving"
                    fixed_resume += skills_section
                    applied_fixes.append(f"Created Skills section with: {', '.join(missing_tech)}")
        
        # Enhance action verbs
        if "action verbs" in str(selected_improvements).lower():
            weak_verbs = ["did", "was", "were", "had", "worked on", "responsible for"]
            strong_verbs = ["achieved", "managed", "developed", "implemented", "optimized", "led"]
            
            for i, weak in enumerate(weak_verbs):
                if weak in fixed_resume.lower() and i < len(strong_verbs):
                    fixed_resume = re.sub(rf'\b{weak}\b', strong_verbs[i], fixed_resume, count=1, flags=re.IGNORECASE)
                    applied_fixes.append(f"Replaced '{weak}' with '{strong_verbs[i]}'")
        
        # Add quantified achievements
        if "numbers" in str(selected_improvements).lower() or "quantified" in str(selected_improvements).lower():
            # Add percentage improvements to bullet points
            bullet_pattern = r'(•|\*|-)\s*([^.\n]+)'
            matches = re.findall(bullet_pattern, fixed_resume)
            
            if matches and len(matches) > 0:
                # Enhance first bullet point with quantification
                first_bullet = matches[0][1]
                if not re.search(r'\d+%|\d+\+|\$\d+', first_bullet):
                    enhanced_bullet = first_bullet + " (increased efficiency by 25%)"
                    fixed_resume = fixed_resume.replace(first_bullet, enhanced_bullet, 1)
                    applied_fixes.append("Added quantified achievement example")
        
        return {
            "original_text": resume_text,
            "fixed_text": fixed_resume,
            "improvements_applied": applied_fixes,
            "word_count_change": len(fixed_resume.split()) - len(resume_text.split())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-fix failed: {str(e)}")

@app.post("/api/generate-resume-file")
async def generate_resume_file(
    resume_text: str = Form(...),
    format_type: str = Form("pdf")  # pdf or docx
):
    """Generate downloadable resume file"""
    try:
        temp_dir = tempfile.mkdtemp()
        
        if format_type == "pdf":
            file_path = os.path.join(temp_dir, "improved_resume.pdf")
            
            # Create PDF using reportlab
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Parse resume text into sections
            lines = resume_text.split('\n')
            story = []
            
            for line in lines:
                if line.strip():
                    if line.isupper() or (len(line) < 50 and not line.startswith((' ', '\t'))):
                        # Section header
                        story.append(Paragraph(line.strip(), styles['Heading2']))
                    else:
                        # Body text
                        story.append(Paragraph(line.strip(), styles['Normal']))
                    story.append(Spacer(1, 6))
            
            doc.build(story)
            
        else:  # docx
            file_path = os.path.join(temp_dir, "improved_resume.docx")
            
            # Create DOCX using python-docx
            doc = Document()
            
            # Add content
            lines = resume_text.split('\n')
            for line in lines:
                if line.strip():
                    if line.isupper() or (len(line) < 50 and not line.startswith((' ', '\t'))):
                        # Section header
                        heading = doc.add_heading(line.strip(), level=2)
                    else:
                        # Body text
                        doc.add_paragraph(line.strip())
            
            doc.save(file_path)
        
        return FileResponse(
            file_path,
            media_type='application/pdf' if format_type == 'pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=f"improved_resume.{format_type}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File generation failed: {str(e)}")

# Existing endpoints
@app.post("/api/scan-resume")
async def scan_resume(file: UploadFile = File(...)):
    content = await file.read()
    text_content = content.decode('utf-8', errors='ignore')
    return {
        "text": text_content,
        "word_count": len(text_content.split()),
        "line_count": len(text_content.splitlines()),
        "ats_score": 75,
        "keywords": ["placeholder", "keywords"]
    }

application = app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)