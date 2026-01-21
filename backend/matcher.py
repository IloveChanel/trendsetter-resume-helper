"""
Advanced Keyword Matcher with TF-IDF and NLP
Matches resumes against job descriptions with intelligent keyword extraction
"""

import re
from typing import List, Dict, Set
from collections import Counter
import math

class KeywordMatcher:
    """Advanced keyword matching with TF-IDF and synonym matching"""
    
    def __init__(self):
        # Common keyword synonyms
        self.synonyms = {
            'javascript': ['js', 'javascript', 'ecmascript'],
            'react': ['react', 'reactjs', 'react.js'],
            'node': ['node', 'nodejs', 'node.js'],
            'python': ['python', 'py'],
            'typescript': ['typescript', 'ts'],
            'database': ['database', 'db', 'sql', 'nosql'],
            'api': ['api', 'rest', 'restful', 'graphql'],
            'frontend': ['frontend', 'front-end', 'front end'],
            'backend': ['backend', 'back-end', 'back end'],
            'fullstack': ['fullstack', 'full-stack', 'full stack'],
        }
        
        # Technical skills patterns
        self.tech_patterns = [
            r'\b(?:React|Angular|Vue|JavaScript|TypeScript|Python|Java|C\+\+|C#|Ruby|Go|Rust|Swift|Kotlin)\b',
            r'\b(?:Node\.?js|Django|Flask|Spring|Express|FastAPI|Rails)\b',
            r'\b(?:SQL|PostgreSQL|MySQL|MongoDB|Redis|Cassandra|DynamoDB)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|CI/CD)\b',
            r'\b(?:Git|GitHub|GitLab|Jira|Agile|Scrum)\b',
        ]
    
    def match_resume_jd(self, resume_text: str, jd_text: str) -> Dict:
        """
        Match resume against job description
        
        Args:
            resume_text: Resume content
            jd_text: Job description content
            
        Returns:
            Dict with match score, keywords, and suggestions
        """
        # Extract keywords from both
        jd_keywords = self._extract_keywords(jd_text)
        resume_keywords = self._extract_keywords(resume_text)
        
        # Calculate TF-IDF scores
        jd_tfidf = self._calculate_tfidf(jd_text, jd_keywords)
        resume_tfidf = self._calculate_tfidf(resume_text, resume_keywords)
        
        # Find matches (including synonyms)
        matches = self._find_matches(resume_keywords, jd_keywords, resume_text.lower(), jd_text.lower())
        
        # Find missing critical keywords
        missing = self._find_missing_keywords(jd_keywords, resume_keywords, resume_text.lower())
        
        # Calculate match score
        score = self._calculate_match_score(matches, jd_keywords, jd_tfidf)
        
        # Calculate keyword density
        density = self._calculate_keyword_density(resume_text, matches)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(missing, jd_text)
        
        return {
            "score": round(score, 1),
            "match_percentage": round(score, 1),
            "found_keywords": sorted(list(matches))[:20],
            "missing_keywords": sorted(missing)[:15],
            "keyword_density": density,
            "total_jd_keywords": len(jd_keywords),
            "matched_keywords": len(matches),
            "suggestions": suggestions[:10]
        }
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text"""
        keywords = set()
        
        # Extract technical terms (capitalized words, tech stack)
        for pattern in self.tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.update([m.lower() for m in matches])
        
        # Extract multi-word technical terms
        multiword_patterns = [
            r'\b(?:machine learning|artificial intelligence|data science|web development)\b',
            r'\b(?:software engineer|full stack|front end|back end|devops)\b',
            r'\b(?:agile methodology|test driven|continuous integration|version control)\b',
        ]
        
        for pattern in multiword_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.update([m.lower() for m in matches])
        
        # Extract important nouns and technologies (simple heuristic)
        # Words that are: 3+ chars, start with capital or all caps, appear multiple times
        words = re.findall(r'\b[A-Z][a-z]{2,}|[A-Z]{2,}\b', text)
        word_counts = Counter([w.lower() for w in words])
        
        for word, count in word_counts.items():
            if count >= 2 and len(word) >= 3:  # Appears at least twice
                keywords.add(word)
        
        # Remove common words
        common_words = {'the', 'and', 'for', 'with', 'you', 'this', 'that', 'will', 'have', 'are', 'from'}
        keywords = {kw for kw in keywords if kw not in common_words}
        
        return keywords
    
    def _calculate_tfidf(self, text: str, keywords: Set[str]) -> Dict[str, float]:
        """Calculate TF-IDF scores for keywords"""
        text_lower = text.lower()
        words = text_lower.split()
        total_words = len(words)
        
        tfidf = {}
        for keyword in keywords:
            # Term frequency
            tf = text_lower.count(keyword.lower()) / total_words if total_words > 0 else 0
            
            # Inverse document frequency (simplified - assuming single document)
            # Higher weight for keywords that appear 2-5 times (not too rare, not too common)
            count = text_lower.count(keyword.lower())
            if count >= 2 and count <= 5:
                idf = 2.0
            elif count == 1:
                idf = 1.5
            else:
                idf = 1.0
            
            tfidf[keyword] = tf * idf
        
        return tfidf
    
    def _find_matches(self, resume_kw: Set[str], jd_kw: Set[str], 
                     resume_text: str, jd_text: str) -> Set[str]:
        """Find matching keywords including synonyms"""
        matches = set()
        
        # Direct matches
        direct_matches = resume_kw & jd_kw
        matches.update(direct_matches)
        
        # Synonym matches
        for jd_keyword in jd_kw:
            if jd_keyword in matches:
                continue
            
            # Check if JD keyword exists in resume (case insensitive)
            if jd_keyword in resume_text:
                matches.add(jd_keyword)
                continue
            
            # Check synonyms
            for key, synonyms in self.synonyms.items():
                if jd_keyword in synonyms:
                    # Check if any synonym appears in resume
                    for synonym in synonyms:
                        if synonym in resume_text:
                            matches.add(jd_keyword)
                            break
        
        return matches
    
    def _find_missing_keywords(self, jd_kw: Set[str], resume_kw: Set[str], 
                               resume_text: str) -> List[str]:
        """Find important missing keywords"""
        missing = []
        
        for keyword in jd_kw:
            # Check if keyword or its synonyms are in resume
            found = keyword in resume_text
            
            if not found:
                # Check synonyms
                for key, synonyms in self.synonyms.items():
                    if keyword in synonyms:
                        found = any(syn in resume_text for syn in synonyms)
                        break
            
            if not found:
                missing.append(keyword)
        
        return missing
    
    def _calculate_match_score(self, matches: Set[str], jd_keywords: Set[str], 
                               jd_tfidf: Dict[str, float]) -> float:
        """Calculate overall match score"""
        if not jd_keywords:
            return 0.0
        
        # Base score: percentage of JD keywords found
        base_score = (len(matches) / len(jd_keywords)) * 100
        
        # Weighted score: consider TF-IDF importance
        matched_weight = sum(jd_tfidf.get(kw, 1.0) for kw in matches)
        total_weight = sum(jd_tfidf.values())
        
        weighted_score = (matched_weight / total_weight) * 100 if total_weight > 0 else 0
        
        # Combine base and weighted (70% base, 30% weighted)
        final_score = (base_score * 0.7) + (weighted_score * 0.3)
        
        return min(100, final_score)
    
    def _calculate_keyword_density(self, text: str, keywords: Set[str]) -> Dict[str, float]:
        """Calculate keyword density"""
        text_lower = text.lower()
        total_words = len(text_lower.split())
        
        density = {}
        for keyword in list(keywords)[:10]:  # Top 10 keywords
            count = text_lower.count(keyword)
            density[keyword] = round((count / total_words) * 100, 2) if total_words > 0 else 0
        
        return density
    
    def _generate_suggestions(self, missing_keywords: List[str], jd_text: str) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []
        
        for keyword in missing_keywords[:10]:
            # Find context in JD
            keyword_lower = keyword.lower()
            jd_lower = jd_text.lower()
            
            if keyword_lower in jd_lower:
                # Find sentence containing keyword
                sentences = re.split(r'[.!?]', jd_text)
                for sentence in sentences:
                    if keyword_lower in sentence.lower():
                        suggestions.append({
                            'keyword': keyword,
                            'suggestion': f'Add "{keyword}" to your skills or experience section',
                            'context': sentence.strip()[:100]
                        })
                        break
            else:
                suggestions.append({
                    'keyword': keyword,
                    'suggestion': f'Consider adding "{keyword}" to your resume',
                    'context': ''
                })
        
        return suggestions

# Singleton instance
_matcher = KeywordMatcher()

def match_resume_jd(resume_text: str, jd_text: str) -> Dict:
    """Wrapper function for backward compatibility"""
    return _matcher.match_resume_jd(resume_text, jd_text)
