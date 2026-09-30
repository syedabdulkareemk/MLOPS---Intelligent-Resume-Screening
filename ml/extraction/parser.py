import re
from typing import Dict, List, Any

class ResumeParser:
    """
    Extracts structured sections from raw resume text using heuristic rules.
    """
    def __init__(self):
        # Academic-style simple heuristic boundary detection
        self.section_patterns = {
            'skills': r'(?i)\b(skills|technical skills|core competencies)\b\s*[:\n]',
            'experience': r'(?i)\b(experience|work history|employment|professional experience)\b\s*[:\n]',
            'education': r'(?i)\b(education|academic background)\b\s*[:\n]'
        }

    def parse(self, text: str) -> Dict[str, str]:
        """
        Parses raw text into distinct sections.
        """
        if not text:
            return {}

        sections = {'skills': '', 'experience': '', 'education': '', 'other': ''}
        
        # A simple linear scan to assign lines to the current active section
        current_section = 'other'
        section_lines = {key: [] for key in sections.keys()}
        
        for line in text.split('\n'):
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Check for section transition
            transitioned = False
            for sec_name, pattern in self.section_patterns.items():
                if re.match(pattern, line_stripped):
                    current_section = sec_name
                    transitioned = True
                    break
            
            if not transitioned:
                section_lines[current_section].append(line_stripped)
                
        for k in sections.keys():
            sections[k] = '\n'.join(section_lines[k])
            
        sections['full_text'] = text
        return sections
