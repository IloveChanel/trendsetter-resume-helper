"""
Resume Parser
Extract structured data from resumes
"""

import re
from typing import Dict, List, Optional
from datetime import datetime

class ResumeParser:
    """Parse resume and extract structured information"""
    
    def __init__(self):
        self.section_keywords = {
            'contact': ['email', 'phone', 'address', 'linkedin', 'github'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'experience': ['experience', 'employment', 'work history', 'professional experience'],
            'education': ['education', 'academic', 'university', 'college', 'degree'],
            'skills': ['skills', 'technical skills', 'technologies', 'competencies'],
            'certifications': ['certifications', 'certificates', 'licenses'],
            'projects': ['projects', 'portfolio'],
            'achievements': ['achievements', 'awards', 'honors', 'accomplishments']
        }
    
    def parse(self, text: str) -> Dict:
        """
        Parse resume and extract structured data
        
        Args:
            text: Resume text content
            
        Returns:
            Dict with structured resume data
        """
        sections = self._identify_sections(text)
        
        return {
            'contact_info': self._extract_contact_info(text),
            'work_experience': self._extract_experience(sections.get('experience', '')),
            'education': self._extract_education(sections.get('education', '')),
            'skills': self._extract_skills(sections.get('skills', '')),
            'certifications': self._extract_certifications(sections.get('certifications', '')),
            'sections': sections,
            'metrics': self._extract_metrics(text),
            'action_verbs': self._count_action_verbs(text)
        }
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract different sections of resume"""
        sections = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for i, line in enumerate(lines):
            line_lower = line.strip().lower()
            
            # Check if this line is a section header
            matched_section = None
            for section_name, keywords in self.section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Verify it looks like a header (short line, possibly in caps)
                    if len(line.split()) <= 5 and len(line.strip()) < 50:
                        matched_section = section_name
                        break
            
            if matched_section:
                # Save previous section
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                
                current_section = matched_section
                section_content = []
            elif current_section:
                section_content.append(line)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        # Extract first 10 lines for contact info
        first_lines = '\n'.join(text.split('\n')[:10])
        
        contact = {}
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', first_lines)
        if email_match:
            contact['email'] = email_match.group()
        
        # Phone
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', first_lines)
        if phone_match:
            contact['phone'] = phone_match.group()
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', first_lines, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        # GitHub
        github_match = re.search(r'github\.com/[\w-]+', first_lines, re.IGNORECASE)
        if github_match:
            contact['github'] = github_match.group()
        
        return contact
    
    def _extract_experience(self, experience_text: str) -> List[Dict]:
        """Extract work experience entries"""
        if not experience_text:
            return []
        
        experiences = []
        # Split by common date patterns or multiple newlines
        entries = re.split(r'\n\s*\n', experience_text)
        
        for entry in entries:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
            
            exp_dict = {}
            
            # Try to extract dates
            date_patterns = [
                r'(\d{4})\s*[-–]\s*(\d{4}|Present|Current)',
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
            ]
            
            dates_found = []
            for pattern in date_patterns:
                dates = re.findall(pattern, entry, re.IGNORECASE)
                if dates:
                    dates_found.extend(dates)
            
            if dates_found:
                exp_dict['dates'] = str(dates_found[0])
            
            # Extract first line as likely job title/company
            first_line = entry.strip().split('\n')[0]
            exp_dict['title'] = first_line
            
            # Extract bullet points or responsibilities
            bullets = re.findall(r'[•\-\*]\s*(.+)', entry)
            if bullets:
                exp_dict['responsibilities'] = bullets
            
            experiences.append(exp_dict)
        
        return experiences[:10]  # Limit to 10 most recent
    
    def _extract_education(self, education_text: str) -> List[Dict]:
        """Extract education entries"""
        if not education_text:
            return []
        
        education = []
        entries = re.split(r'\n\s*\n', education_text)
        
        # Common degree keywords
        degree_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.a.', 'm.a.', 'mba', 'associate']
        
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
            
            edu_dict = {}
            entry_lower = entry.lower()
            
            # Check for degree
            for keyword in degree_keywords:
                if keyword in entry_lower:
                    edu_dict['degree'] = keyword
                    break
            
            # Extract year
            years = re.findall(r'\b(19|20)\d{2}\b', entry)
            if years:
                edu_dict['year'] = years[-1]  # Most recent year
            
            # First line often contains institution
            first_line = entry.strip().split('\n')[0]
            edu_dict['institution'] = first_line
            
            education.append(edu_dict)
        
        return education
    
    def _extract_skills(self, skills_text: str) -> List[str]:
        """Extract skills list"""
        if not skills_text:
            return []
        
        # Remove bullet points and split by common separators
        skills_text = re.sub(r'[•\-\*]', '', skills_text)
        skills = re.split(r'[,;\n]+', skills_text)
        
        # Clean and filter
        skills = [s.strip() for s in skills if s.strip() and len(s.strip()) > 2]
        
        return skills[:50]  # Limit to 50 skills
    
    def _extract_certifications(self, cert_text: str) -> List[str]:
        """Extract certifications"""
        if not cert_text:
            return []
        
        certs = []
        lines = cert_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 200:
                # Remove bullet points
                line = re.sub(r'^[•\-\*]\s*', '', line)
                certs.append(line)
        
        return certs
    
    def _extract_metrics(self, text: str) -> Dict:
        """Extract quantifiable metrics from resume"""
        metrics = {
            'percentages': [],
            'numbers': [],
            'currencies': []
        }
        
        # Find percentages
        percentages = re.findall(r'\d+\.?\d*\s*%', text)
        metrics['percentages'] = list(set(percentages))
        
        # Find large numbers with context
        number_patterns = re.findall(
            r'\b\d+\.?\d*\s*(million|billion|thousand|K|M|B|users|customers|sales|revenue)\b',
            text,
            re.IGNORECASE
        )
        metrics['numbers'] = list(set(number_patterns))
        
        # Find currency amounts
        currencies = re.findall(r'\$\d+[,\d]*(?:\.\d{2})?[KMB]?', text)
        metrics['currencies'] = list(set(currencies))
        
        return metrics
    
    def _count_action_verbs(self, text: str) -> int:
        """Count action verbs (indicates strong resume)"""
        action_verbs = [
            'achieved', 'improved', 'trained', 'managed', 'created', 'developed',
            'built', 'led', 'implemented', 'increased', 'decreased', 'reduced',
            'launched', 'established', 'designed', 'analyzed', 'optimized',
            'coordinated', 'executed', 'generated', 'delivered', 'drove'
        ]
        
        text_lower = text.lower()
        count = sum(text_lower.count(verb) for verb in action_verbs)
        
        return count
