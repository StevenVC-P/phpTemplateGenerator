#!/usr/bin/env python3
"""
Template Refinement Engine
Automatically applies agent feedback to improve templates iteratively
"""

import json
import re
import logging
from typing import Dict, List, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class TemplateRefiner:
    """Applies agent feedback to iteratively improve templates"""
    
    def __init__(self):
        self.max_iterations = 5
        self.quality_threshold = 8.0
        self.improvement_patterns = self.load_improvement_patterns()
    
    def load_improvement_patterns(self) -> Dict[str, Any]:
        """Load patterns for applying common improvements"""
        return {
            "security": {
                "xss_protection": {
                    "pattern": r"(\$_POST\[['\"]\w+['\"]\])",
                    "replacement": r"htmlspecialchars(\1)",
                    "description": "Add XSS protection to form inputs"
                },
                "csrf_token": {
                    "pattern": r"(<form[^>]*>)",
                    "replacement": r'\1\n    <input type="hidden" name="csrf_token" value="<?php echo $_SESSION[\'csrf_token\']; ?>">',
                    "description": "Add CSRF protection to forms"
                }
            },
            "responsive": {
                "mobile_breakpoints": {
                    "pattern": r"(@media \(max-width: 768px\) \{[^}]*\})",
                    "replacement": self.generate_enhanced_mobile_css,
                    "description": "Enhance mobile responsive design"
                },
                "tablet_breakpoints": {
                    "pattern": r"(\/\* Responsive Design \*\/)",
                    "replacement": r'\1\n        @media (max-width: 1024px) {\n            .hero h1 { font-size: 3rem; }\n            .container { padding: 0 15px; }\n        }',
                    "description": "Add tablet breakpoints"
                }
            },
            "accessibility": {
                "focus_states": {
                    "pattern": r"(\.[\w-]+:hover \{[^}]*\})",
                    "replacement": r'\1\n        \1:focus {\n            outline: 2px solid var(--primary-color);\n            outline-offset: 2px;\n        }',
                    "description": "Add focus states for accessibility"
                },
                "alt_attributes": {
                    "pattern": r"(<img[^>]*)(>)",
                    "replacement": r'\1 alt="Professional service image"\2',
                    "description": "Add alt attributes to images"
                }
            },
            "performance": {
                "font_preload": {
                    "pattern": r"(<link href=\"https://fonts\.googleapis\.com[^>]*>)",
                    "replacement": r'<link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    \1',
                    "description": "Add font preloading for performance"
                },
                "image_optimization": {
                    "pattern": r"(<img[^>]*)(>)",
                    "replacement": r'\1 loading="lazy"\2',
                    "description": "Add lazy loading to images"
                }
            },
            "visual_complexity": {
                "box_shadows": {
                    "pattern": r"(\.feature-card \{[^}]*)(border-radius: [^;]*;)",
                    "replacement": r'\1\2\n            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);\n            transition: transform 0.3s ease, box-shadow 0.3s ease;',
                    "description": "Add depth with enhanced shadows"
                },
                "hover_animations": {
                    "pattern": r"(\.feature-card:hover \{[^}]*)(transform: translateY\([^)]*\);)",
                    "replacement": r'\1\2\n            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);',
                    "description": "Enhance hover animations"
                }
            }
        }
    
    def refine_template(self, template_file: str, review_data: Dict[str, Any], design_critique: str) -> Tuple[str, Dict[str, Any]]:
        """Apply refinements based on agent feedback"""
        logger.info(f"Refining template: {template_file}")
        
        try:
            # Read current template
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Track applied improvements
            improvements_applied = []
            original_content = content
            
            # Apply security improvements
            content, security_improvements = self.apply_security_improvements(content, review_data)
            improvements_applied.extend(security_improvements)
            
            # Apply responsive design improvements
            content, responsive_improvements = self.apply_responsive_improvements(content, review_data)
            improvements_applied.extend(responsive_improvements)
            
            # Apply accessibility improvements
            content, accessibility_improvements = self.apply_accessibility_improvements(content, review_data)
            improvements_applied.extend(accessibility_improvements)
            
            # Apply performance improvements
            content, performance_improvements = self.apply_performance_improvements(content, review_data)
            improvements_applied.extend(performance_improvements)
            
            # Apply visual complexity improvements
            content, visual_improvements = self.apply_visual_improvements(content, design_critique)
            improvements_applied.extend(visual_improvements)
            
            # Generate refinement report
            refinement_report = {
                "template_file": template_file,
                "improvements_applied": improvements_applied,
                "total_improvements": len(improvements_applied),
                "content_changed": content != original_content,
                "estimated_score_improvement": len(improvements_applied) * 0.3,
                "refinement_timestamp": self.get_timestamp()
            }
            
            logger.info(f"Applied {len(improvements_applied)} improvements to template")
            
            return content, refinement_report
            
        except Exception as e:
            logger.error(f"Template refinement failed: {e}")
            return content, {"error": str(e), "improvements_applied": []}
    
    def apply_security_improvements(self, content: str, review_data: Dict[str, Any]) -> Tuple[str, List[Dict]]:
        """Apply security-related improvements"""
        improvements = []
        
        # Check if XSS protection is needed
        if any("XSS" in action or "htmlspecialchars" in action for action in review_data.get("recommended_actions", [])):
            pattern = self.improvement_patterns["security"]["xss_protection"]
            if re.search(pattern["pattern"], content):
                content = re.sub(pattern["pattern"], pattern["replacement"], content)
                improvements.append({
                    "type": "security",
                    "description": pattern["description"],
                    "priority": "high"
                })
        
        # Add CSRF protection if forms exist
        if "<form" in content and "csrf_token" not in content:
            pattern = self.improvement_patterns["security"]["csrf_token"]
            content = re.sub(pattern["pattern"], pattern["replacement"], content)
            improvements.append({
                "type": "security", 
                "description": pattern["description"],
                "priority": "high"
            })
        
        return content, improvements
    
    def apply_responsive_improvements(self, content: str, review_data: Dict[str, Any]) -> Tuple[str, List[Dict]]:
        """Apply responsive design improvements"""
        improvements = []
        
        # Add mobile breakpoints if missing
        if "@media" not in content or "responsive" in str(review_data.get("recommended_actions", [])).lower():
            # Add enhanced mobile CSS
            mobile_css = """
        
        /* Enhanced Mobile Responsive Design */
        @media (max-width: 480px) {
            .container {
                padding: 0 10px;
            }
            
            .hero {
                padding: 80px 0 60px;
            }
            
            .hero h1 {
                font-size: 2rem;
                line-height: 1.3;
            }
            
            .hero .subtitle {
                font-size: 1rem;
            }
            
            .cta-button {
                padding: 1rem 1.5rem;
                font-size: 1rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .feature-card {
                padding: 1.5rem;
            }
            
            .section-title {
                font-size: 2rem;
            }
        }
        
        @media (max-width: 1024px) {
            .hero h1 {
                font-size: 3rem;
            }
            
            .container {
                padding: 0 15px;
            }
            
            .features-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }"""
            
            # Insert before closing </style> tag
            content = content.replace("</style>", mobile_css + "\n    </style>")
            improvements.append({
                "type": "responsive",
                "description": "Added comprehensive mobile and tablet breakpoints",
                "priority": "medium"
            })
        
        return content, improvements
    
    def apply_accessibility_improvements(self, content: str, review_data: Dict[str, Any]) -> Tuple[str, List[Dict]]:
        """Apply accessibility improvements"""
        improvements = []
        
        # Add focus states
        if ":focus" not in content:
            focus_css = """
        
        /* Enhanced Accessibility */
        .cta-button:focus,
        .submit-btn:focus,
        input:focus,
        textarea:focus {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
        }
        
        .nav-links a:focus {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
            border-radius: 4px;
        }"""
            
            content = content.replace("</style>", focus_css + "\n    </style>")
            improvements.append({
                "type": "accessibility",
                "description": "Added focus states for keyboard navigation",
                "priority": "medium"
            })
        
        return content, improvements
    
    def apply_performance_improvements(self, content: str, review_data: Dict[str, Any]) -> Tuple[str, List[Dict]]:
        """Apply performance improvements"""
        improvements = []
        
        # Add font preloading
        if "fonts.googleapis.com" in content and "preconnect" not in content:
            pattern = r'(<link href="https://fonts\.googleapis\.com[^>]*>)'
            replacement = '''<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    \\1'''
            content = re.sub(pattern, replacement, content)
            improvements.append({
                "type": "performance",
                "description": "Added font preloading for better performance",
                "priority": "low"
            })
        
        return content, improvements
    
    def apply_visual_improvements(self, content: str, design_critique: str) -> Tuple[str, List[Dict]]:
        """Apply visual complexity improvements based on design critique"""
        improvements = []
        
        # Add enhanced shadows if complexity is low
        if "complexity" in design_critique.lower() and "shadow" in design_critique.lower():
            enhanced_shadows = """
        
        /* Enhanced Visual Depth */
        .feature-card {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15), 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        .contact-form {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        header {
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }"""
            
            content = content.replace("</style>", enhanced_shadows + "\n    </style>")
            improvements.append({
                "type": "visual",
                "description": "Enhanced visual depth with layered shadows",
                "priority": "low"
            })
        
        return content, improvements
    
    def generate_enhanced_mobile_css(self, match):
        """Generate enhanced mobile CSS"""
        return """@media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .nav-links {
                display: none;
            }
            
            .container {
                padding: 0 15px;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
        }"""
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Utility functions
def refine_template_with_feedback(template_file: str, review_file: str, design_file: str) -> Dict[str, Any]:
    """Convenience function to refine template with feedback"""
    refiner = TemplateRefiner()
    
    # Load review data
    with open(review_file, 'r') as f:
        review_data = json.load(f)
    
    # Load design critique
    with open(design_file, 'r') as f:
        design_critique = f.read()
    
    # Apply refinements
    refined_content, report = refiner.refine_template(template_file, review_data, design_critique)
    
    # Save refined template
    refined_file = template_file.replace('.php', '.refined.php')
    with open(refined_file, 'w', encoding='utf-8') as f:
        f.write(refined_content)
    
    report['refined_file'] = refined_file
    return report
