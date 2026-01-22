
import re
from typing import Dict

def match_resume_jd(resume_text: str, jd_text: str) -> Dict:
    """Demo matcher - replace with real AI later"""
    
    # Demo keywords from JD
    jd_keywords = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', jd_text)
    resume_keywords = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', resume_text)
    
    # Mock score
    score = min(95, 50 + len(set(resume_keywords) & set(jd_keywords)) * 3)
    
    missing = [kw for kw in jd_keywords[:10] if kw.lower() not in resume_text.lower()]
    
    return {
        "score": score,
        "missing_keywords": missing,
        "found_keywords": list(set(resume_keywords) & set(jd_keywords))[:10],
        "suggestions": [f"Add experience with {kw}" for kw in missing[:5]]
    }
