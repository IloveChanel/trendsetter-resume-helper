"""
Grammar and Error Checker
Checks for grammar, spelling, and style issues
"""

import re
from typing import Dict, List

class GrammarChecker:
    """Check grammar, spelling, and writing quality"""
    
    def __init__(self):
        # Common weak phrases to avoid
        self.weak_phrases = [
            'responsible for', 'duties included', 'worked on', 'helped with',
            'participated in', 'assisted with', 'involved in', 'tasked with'
        ]
        
        # Strong action verbs to suggest
        self.action_verbs = [
            'achieved', 'improved', 'increased', 'decreased', 'reduced',
            'developed', 'created', 'built', 'designed', 'implemented',
            'launched', 'led', 'managed', 'optimized', 'streamlined',
            'coordinated', 'executed', 'delivered', 'drove', 'established',
            'generated', 'transformed', 'pioneered', 'spearheaded'
        ]
        
        # Common spelling errors in tech resumes
        self.common_errors = {
            'experiance': 'experience',
            'recieve': 'receive',
            'occured': 'occurred',
            'seperate': 'separate',
            'definately': 'definitely',
            'sucessful': 'successful',
            'managment': 'management',
            'develope': 'develop'
        }
    
    def check(self, text: str) -> Dict:
        """
        Check text for grammar and style issues
        
        Args:
            text: Resume text to check
            
        Returns:
            Dict with issues and suggestions
        """
        issues = []
        
        # Check for weak language
        weak_lang_issues = self._check_weak_language(text)
        issues.extend(weak_lang_issues)
        
        # Check for spelling errors
        spelling_issues = self._check_spelling(text)
        issues.extend(spelling_issues)
        
        # Check for passive voice
        passive_issues = self._check_passive_voice(text)
        issues.extend(passive_issues)
        
        # Check for first person pronouns (should be avoided)
        pronoun_issues = self._check_first_person(text)
        issues.extend(pronoun_issues)
        
        # Check for repetition
        repetition_issues = self._check_repetition(text)
        issues.extend(repetition_issues)
        
        # Calculate readability score
        readability = self._calculate_readability(text)
        
        return {
            'total_issues': len(issues),
            'issues': issues[:20],  # Limit to 20 most important
            'readability_score': readability,
            'action_verb_count': self._count_action_verbs(text),
            'weak_phrase_count': len(weak_lang_issues),
            'suggestions': self._get_general_suggestions(issues)
        }
    
    def _check_weak_language(self, text: str) -> List[Dict]:
        """Check for weak phrases"""
        issues = []
        text_lower = text.lower()
        
        for phrase in self.weak_phrases:
            if phrase in text_lower:
                issues.append({
                    'type': 'weak_language',
                    'severity': 'medium',
                    'phrase': phrase,
                    'message': f'Weak phrase detected: "{phrase}"',
                    'suggestion': f'Replace with strong action verb (e.g., {self._suggest_action_verb()})'
                })
        
        return issues
    
    def _check_spelling(self, text: str) -> List[Dict]:
        """Check for common spelling errors"""
        issues = []
        text_lower = text.lower()
        
        for error, correction in self.common_errors.items():
            if error in text_lower:
                issues.append({
                    'type': 'spelling',
                    'severity': 'high',
                    'error': error,
                    'message': f'Possible spelling error: "{error}"',
                    'suggestion': f'Did you mean "{correction}"?'
                })
        
        return issues
    
    def _check_passive_voice(self, text: str) -> List[Dict]:
        """Check for passive voice (should use active voice)"""
        issues = []
        
        # Common passive voice patterns
        passive_patterns = [
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bhas\s+been\s+\w+ed\b',
            r'\bhave\s+been\s+\w+ed\b',
            r'\bhad\s+been\s+\w+ed\b'
        ]
        
        for pattern in passive_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in list(matches)[:5]:  # Limit to 5 examples
                issues.append({
                    'type': 'passive_voice',
                    'severity': 'low',
                    'phrase': match.group(),
                    'message': f'Passive voice detected: "{match.group()}"',
                    'suggestion': 'Use active voice with strong action verbs'
                })
        
        return issues
    
    def _check_first_person(self, text: str) -> List[Dict]:
        """Check for first person pronouns (should be omitted in resumes)"""
        issues = []
        
        first_person = ['I ', 'my ', 'me ', 'mine ', 'we ', 'our ', 'us ']
        text_with_spaces = ' ' + text + ' '
        
        for pronoun in first_person:
            count = text_with_spaces.lower().count(pronoun)
            if count > 0:
                issues.append({
                    'type': 'first_person',
                    'severity': 'medium',
                    'pronoun': pronoun.strip(),
                    'count': count,
                    'message': f'First person pronoun "{pronoun.strip()}" used {count} time(s)',
                    'suggestion': 'Remove first person pronouns; use direct statements'
                })
        
        return issues
    
    def _check_repetition(self, text: str) -> List[Dict]:
        """Check for repeated words or phrases"""
        issues = []
        
        # Find repeated phrases (3+ words)
        words = text.lower().split()
        
        # Check for repeated action verbs
        action_verb_counts = {}
        for verb in self.action_verbs:
            count = text.lower().count(verb)
            if count > 3:  # Used more than 3 times
                action_verb_counts[verb] = count
        
        if action_verb_counts:
            for verb, count in list(action_verb_counts.items())[:3]:
                issues.append({
                    'type': 'repetition',
                    'severity': 'low',
                    'word': verb,
                    'count': count,
                    'message': f'"{verb}" used {count} times',
                    'suggestion': 'Vary your action verbs for better impact'
                })
        
        return issues
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate simple readability score (0-100)"""
        # Simple heuristic based on sentence and word length
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 50.0
        
        words = text.split()
        total_words = len(words)
        total_sentences = len(sentences)
        
        if total_sentences == 0:
            return 50.0
        
        avg_words_per_sentence = total_words / total_sentences
        
        # Ideal: 15-20 words per sentence
        if 15 <= avg_words_per_sentence <= 20:
            score = 100
        elif 10 <= avg_words_per_sentence < 15:
            score = 90
        elif 20 < avg_words_per_sentence <= 25:
            score = 85
        elif 25 < avg_words_per_sentence <= 30:
            score = 70
        else:
            score = 60
        
        return round(score, 1)
    
    def _count_action_verbs(self, text: str) -> int:
        """Count action verbs in text"""
        text_lower = text.lower()
        count = sum(1 for verb in self.action_verbs if verb in text_lower)
        return count
    
    def _suggest_action_verb(self) -> str:
        """Suggest a random action verb"""
        import random
        return random.choice(self.action_verbs)
    
    def _get_general_suggestions(self, issues: List[Dict]) -> List[str]:
        """Get general writing suggestions"""
        suggestions = []
        
        issue_types = [issue['type'] for issue in issues]
        
        if 'weak_language' in issue_types:
            suggestions.append('Use strong action verbs to start bullet points')
        
        if 'passive_voice' in issue_types:
            suggestions.append('Convert passive voice to active voice for impact')
        
        if 'first_person' in issue_types:
            suggestions.append('Remove first person pronouns (I, my, we, our)')
        
        if len(issues) < 3:
            suggestions.append('Great job! Your resume has strong language')
        
        return suggestions
