"""
ATS Compatibility Checker
Checks for ATS-killer issues and returns compatibility score
"""

import re
from typing import Dict, List

class ATSChecker:
    """Check resume for ATS compatibility issues"""
    
    def __init__(self):
        # ATS-friendly section headers
        self.standard_sections = [
            'summary', 'objective', 'experience', 'work experience', 
            'employment', 'education', 'skills', 'technical skills',
            'certifications', 'projects', 'achievements', 'awards'
        ]
        
    def check_compatibility(self, text: str, file_type: str = 'pdf') -> Dict:
        """
        Check ATS compatibility and return score with issues
        
        Args:
            text: Resume text content
            file_type: File type (pdf, docx)
            
        Returns:
            Dict with score, issues, and suggestions
        """
        issues = []
        score = 100.0
        
        # Check for common ATS-killer patterns
        
        # 1. Check for tables (approximate detection)
        if self._has_table_markers(text):
            issues.append({
                'type': 'tables',
                'severity': 'high',
                'message': 'Tables detected - ATS may not parse correctly',
                'fix': 'Use simple text formatting instead of tables'
            })
            score -= 15
        
        # 2. Check for complex formatting
        if self._has_complex_formatting(text):
            issues.append({
                'type': 'formatting',
                'severity': 'medium',
                'message': 'Complex formatting detected',
                'fix': 'Use simple, clean formatting with standard fonts'
            })
            score -= 10
        
        # 3. Check for non-standard section headers
        non_standard = self._check_section_headers(text)
        if non_standard:
            issues.append({
                'type': 'headers',
                'severity': 'medium',
                'message': f'Non-standard section headers found: {", ".join(non_standard[:3])}',
                'fix': 'Use standard headers like "Work Experience", "Education", "Skills"'
            })
            score -= 10
        
        # 4. Check for special characters and symbols
        if self._has_special_chars(text):
            issues.append({
                'type': 'special_chars',
                'severity': 'low',
                'message': 'Excessive special characters or symbols detected',
                'fix': 'Remove decorative symbols, use simple bullet points'
            })
            score -= 5
        
        # 5. Check for contact information
        if not self._has_contact_info(text):
            issues.append({
                'type': 'contact',
                'severity': 'high',
                'message': 'Contact information not clearly visible',
                'fix': 'Add email and phone number at the top of resume'
            })
            score -= 15
        
        # 6. Check for appropriate length
        word_count = len(text.split())
        if word_count < 200:
            issues.append({
                'type': 'length',
                'severity': 'medium',
                'message': 'Resume appears too short',
                'fix': 'Expand on your experience and achievements'
            })
            score -= 10
        elif word_count > 1500:
            issues.append({
                'type': 'length',
                'severity': 'low',
                'message': 'Resume appears too long',
                'fix': 'Consider reducing to 1-2 pages'
            })
            score -= 5
        
        # 7. Check for quantifiable achievements
        if not self._has_metrics(text):
            issues.append({
                'type': 'metrics',
                'severity': 'medium',
                'message': 'Few or no quantifiable achievements found',
                'fix': 'Add numbers, percentages, and measurable results'
            })
            score -= 10
        
        score = max(0, min(100, score))  # Ensure score is between 0-100
        
        return {
            'score': round(score, 1),
            'issues': issues,
            'total_issues': len(issues),
            'compatibility': self._get_compatibility_rating(score)
        }
    
    def _has_table_markers(self, text: str) -> bool:
        """Check for table-like patterns"""
        lines = text.split('\n')
        # Look for multiple consecutive lines with multiple tabs or excessive spaces
        table_pattern = 0
        for line in lines:
            if '\t\t' in line or '  ' * 5 in line:
                table_pattern += 1
        return table_pattern > 3
    
    def _has_complex_formatting(self, text: str) -> bool:
        """Check for complex formatting patterns"""
        # Check for excessive special formatting characters
        special_count = len(re.findall(r'[│┤├┼─━]', text))
        return special_count > 5
    
    def _check_section_headers(self, text: str) -> List[str]:
        """Check for non-standard section headers"""
        # Extract likely headers (lines with fewer than 5 words, often in caps)
        lines = text.split('\n')
        potential_headers = []
        
        for line in lines:
            line = line.strip()
            words = line.split()
            if 1 <= len(words) <= 4 and len(line) < 50:
                if line.isupper() or line.istitle():
                    header_lower = line.lower()
                    is_standard = any(std in header_lower for std in self.standard_sections)
                    if not is_standard and len(line) > 3:
                        potential_headers.append(line)
        
        return potential_headers[:5]  # Return first 5 non-standard headers
    
    def _has_special_chars(self, text: str) -> bool:
        """Check for excessive special characters"""
        special_chars = len(re.findall(r'[★☆●○■□▪▫◆◇]', text))
        return special_chars > 10
    
    def _has_contact_info(self, text: str) -> bool:
        """Check if contact information is present"""
        # Check for email
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        # Check for phone
        has_phone = bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
        return has_email or has_phone
    
    def _has_metrics(self, text: str) -> bool:
        """Check for quantifiable achievements (numbers, percentages)"""
        # Look for percentages
        percentages = len(re.findall(r'\d+%', text))
        # Look for numbers in context
        numbers = len(re.findall(r'\b\d+\s*(million|billion|thousand|hundred|users|customers|revenue|sales)\b', text, re.IGNORECASE))
        return (percentages + numbers) >= 3
    
    def _get_compatibility_rating(self, score: float) -> str:
        """Get text rating based on score"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        else:
            return 'Poor'
