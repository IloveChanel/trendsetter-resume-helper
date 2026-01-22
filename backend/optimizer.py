"""
Resume Optimizer
Provides actionable suggestions to optimize resumes
"""

from typing import Dict, List
import re

class ResumeOptimizer:
    """Generate optimization suggestions for resumes"""
    
    def __init__(self):
        self.ats_friendly_sections = {
            'about me': 'Summary',
            'profile': 'Summary',
            'career summary': 'Professional Summary',
            'work history': 'Work Experience',
            'employment history': 'Work Experience',
            'professional experience': 'Work Experience',
            'technical skills': 'Skills',
            'core competencies': 'Skills',
            'expertise': 'Skills',
            'academic background': 'Education',
            'qualifications': 'Education'
        }
    
    def optimize(self, text: str, missing_keywords: List[str], 
                 ats_issues: List[Dict], grammar_issues: List[Dict]) -> Dict:
        """
        Generate comprehensive optimization suggestions
        
        Args:
            text: Resume text
            missing_keywords: Keywords missing from resume
            ats_issues: ATS compatibility issues
            grammar_issues: Grammar and style issues
            
        Returns:
            Dict with optimization suggestions
        """
        suggestions = {
            'section_headers': self._optimize_section_headers(text),
            'keyword_placement': self._suggest_keyword_placement(text, missing_keywords),
            'formatting': self._optimize_formatting(ats_issues),
            'content': self._optimize_content(text, missing_keywords),
            'impact_statements': self._create_impact_statements(missing_keywords),
            'priority_fixes': self._prioritize_fixes(ats_issues, grammar_issues, missing_keywords)
        }
        
        return suggestions
    
    def _optimize_section_headers(self, text: str) -> List[Dict]:
        """Suggest ATS-friendly section headers"""
        suggestions = []
        
        # Extract likely headers from text
        lines = text.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            if len(line_stripped) < 50 and len(line_stripped.split()) <= 4:
                line_lower = line_stripped.lower()
                
                # Check if it matches a non-standard header
                for non_standard, standard in self.ats_friendly_sections.items():
                    if non_standard in line_lower and line_lower != standard.lower():
                        suggestions.append({
                            'current': line_stripped,
                            'suggested': standard,
                            'reason': 'ATS-friendly standard section header'
                        })
                        break
        
        return suggestions[:5]  # Top 5 suggestions
    
    def _suggest_keyword_placement(self, text: str, missing_keywords: List[str]) -> List[Dict]:
        """Suggest where and how to add missing keywords"""
        suggestions = []
        
        # Identify sections in resume
        sections = self._identify_sections(text)
        
        for keyword in missing_keywords[:10]:
            placement = []
            
            # Suggest adding to Skills section
            if 'skills' in sections:
                placement.append({
                    'section': 'Skills',
                    'suggestion': f'Add "{keyword}" to your technical skills list',
                    'example': f'• {keyword}'
                })
            
            # Suggest adding to Experience section
            if 'experience' in sections:
                placement.append({
                    'section': 'Work Experience',
                    'suggestion': f'Incorporate "{keyword}" into a bullet point',
                    'example': f'• Utilized {keyword} to [specific achievement]'
                })
            
            # Suggest adding to Summary section
            if 'summary' in sections:
                placement.append({
                    'section': 'Summary',
                    'suggestion': f'Mention "{keyword}" in your professional summary',
                    'example': f'Experienced in {keyword} with proven track record'
                })
            
            if placement:
                suggestions.append({
                    'keyword': keyword,
                    'placements': placement
                })
        
        return suggestions
    
    def _optimize_formatting(self, ats_issues: List[Dict]) -> List[Dict]:
        """Generate formatting optimization suggestions"""
        suggestions = []
        
        for issue in ats_issues[:5]:
            if issue['type'] == 'tables':
                suggestions.append({
                    'issue': 'Tables detected',
                    'fix': 'Convert tables to simple text format with bullet points',
                    'priority': 'high'
                })
            elif issue['type'] == 'headers':
                suggestions.append({
                    'issue': 'Non-standard section headers',
                    'fix': 'Use standard headers: Summary, Work Experience, Education, Skills',
                    'priority': 'high'
                })
            elif issue['type'] == 'special_chars':
                suggestions.append({
                    'issue': 'Special characters detected',
                    'fix': 'Replace decorative symbols with simple bullet points (•)',
                    'priority': 'medium'
                })
        
        return suggestions
    
    def _optimize_content(self, text: str, missing_keywords: List[str]) -> List[Dict]:
        """Generate content optimization suggestions"""
        suggestions = []
        
        # Check for quantifiable achievements
        has_metrics = bool(re.search(r'\d+%|\$\d+|\d+\s*(million|billion|thousand)', text))
        
        if not has_metrics:
            suggestions.append({
                'area': 'Quantifiable Achievements',
                'suggestion': 'Add measurable results and metrics to your bullet points',
                'examples': [
                    'Increased revenue by 25%',
                    'Reduced load time by 40%',
                    'Managed team of 5 developers'
                ]
            })
        
        # Check for action verbs
        action_verbs = ['achieved', 'improved', 'developed', 'led', 'created', 'implemented']
        has_action_verbs = any(verb in text.lower() for verb in action_verbs)
        
        if not has_action_verbs:
            suggestions.append({
                'area': 'Action Verbs',
                'suggestion': 'Start bullet points with strong action verbs',
                'examples': [
                    'Developed',
                    'Implemented',
                    'Led',
                    'Achieved',
                    'Optimized'
                ]
            })
        
        # Suggest adding missing technical skills
        if missing_keywords:
            suggestions.append({
                'area': 'Technical Skills',
                'suggestion': f'Add relevant technical skills from job description',
                'examples': missing_keywords[:5]
            })
        
        return suggestions
    
    def _create_impact_statements(self, missing_keywords: List[str]) -> List[Dict]:
        """Create sample impact statements with missing keywords"""
        statements = []
        
        templates = [
            'Developed {keyword}-based solutions that improved {metric} by {percentage}%',
            'Implemented {keyword} to optimize {area}, resulting in {benefit}',
            'Led team using {keyword} to deliver {outcome} ahead of schedule',
            'Architected scalable {keyword} system supporting {number} users',
            'Utilized {keyword} to reduce {metric} by {percentage}%'
        ]
        
        for keyword in missing_keywords[:5]:
            import random
            template = random.choice(templates)
            
            # Fill in template with examples
            statement = template.replace('{keyword}', keyword)
            statement = statement.replace('{metric}', 'performance')
            statement = statement.replace('{percentage}', '30')
            statement = statement.replace('{area}', 'workflow')
            statement = statement.replace('{benefit}', 'faster deployment cycles')
            statement = statement.replace('{outcome}', 'production release')
            statement = statement.replace('{number}', '10,000+')
            
            statements.append({
                'keyword': keyword,
                'example': statement,
                'tip': 'Customize this example with your actual achievements'
            })
        
        return statements
    
    def _prioritize_fixes(self, ats_issues: List[Dict], grammar_issues: List[Dict], 
                         missing_keywords: List[str]) -> List[Dict]:
        """Prioritize all fixes by importance"""
        priorities = []
        
        # High priority: ATS blockers
        high_severity_ats = [issue for issue in ats_issues if issue.get('severity') == 'high']
        for issue in high_severity_ats[:3]:
            priorities.append({
                'priority': 1,
                'category': 'ATS Compatibility',
                'issue': issue.get('message', ''),
                'fix': issue.get('fix', '')
            })
        
        # High priority: Missing critical keywords
        if len(missing_keywords) > 5:
            priorities.append({
                'priority': 1,
                'category': 'Keywords',
                'issue': f'{len(missing_keywords)} important keywords missing',
                'fix': f'Add key terms: {", ".join(missing_keywords[:5])}'
            })
        
        # Medium priority: Grammar issues
        high_severity_grammar = [issue for issue in grammar_issues if issue.get('severity') == 'high']
        for issue in high_severity_grammar[:2]:
            priorities.append({
                'priority': 2,
                'category': 'Grammar & Style',
                'issue': issue.get('message', ''),
                'fix': issue.get('suggestion', '')
            })
        
        # Medium priority: Other ATS issues
        medium_severity_ats = [issue for issue in ats_issues if issue.get('severity') == 'medium']
        for issue in medium_severity_ats[:2]:
            priorities.append({
                'priority': 2,
                'category': 'ATS Compatibility',
                'issue': issue.get('message', ''),
                'fix': issue.get('fix', '')
            })
        
        return priorities[:10]  # Top 10 priorities
    
    def _identify_sections(self, text: str) -> Dict[str, bool]:
        """Identify which sections exist in resume"""
        text_lower = text.lower()
        
        sections = {
            'summary': any(word in text_lower for word in ['summary', 'objective', 'profile']),
            'experience': any(word in text_lower for word in ['experience', 'employment', 'work history']),
            'education': 'education' in text_lower,
            'skills': any(word in text_lower for word in ['skills', 'technical', 'competencies']),
            'certifications': any(word in text_lower for word in ['certification', 'certificate', 'license'])
        }
        
        return sections
