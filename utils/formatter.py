#!/usr/bin/env python3
"""
Formatting Utilities for PHP Template Generator
Handles code formatting, validation, and output processing
"""

import re
import json
import html
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CodeFormatter:
    """Utility class for code formatting and validation"""
    
    def __init__(self):
        self.php_keywords = [
            'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch',
            'class', 'clone', 'const', 'continue', 'declare', 'default', 'die',
            'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor',
            'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit',
            'extends', 'final', 'finally', 'for', 'foreach', 'function', 'global',
            'goto', 'if', 'implements', 'include', 'include_once', 'instanceof',
            'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or',
            'print', 'private', 'protected', 'public', 'require', 'require_once',
            'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset',
            'use', 'var', 'while', 'xor', 'yield'
        ]
    
    def format_php_code(self, code: str, indent_size: int = 4) -> str:
        """Format PHP code with proper indentation"""
        try:
            lines = code.split('\n')
            formatted_lines = []
            indent_level = 0
            in_php = False
            
            for line in lines:
                stripped = line.strip()
                
                # Skip empty lines
                if not stripped:
                    formatted_lines.append('')
                    continue
                
                # Check for PHP opening/closing tags
                if '<?php' in stripped:
                    in_php = True
                    formatted_lines.append(stripped)
                    continue
                elif '?>' in stripped:
                    in_php = False
                    formatted_lines.append(stripped)
                    continue
                
                # Handle HTML content
                if not in_php:
                    formatted_lines.append(self.format_html_line(stripped, indent_level, indent_size))
                    continue
                
                # Handle PHP content
                # Decrease indent for closing braces
                if stripped.startswith('}') or stripped.startswith('?>'):
                    indent_level = max(0, indent_level - 1)
                
                # Apply indentation
                indented_line = ' ' * (indent_level * indent_size) + stripped
                formatted_lines.append(indented_line)
                
                # Increase indent for opening braces
                if stripped.endswith('{') or stripped.endswith('<?php'):
                    indent_level += 1
            
            return '\n'.join(formatted_lines)
            
        except Exception as e:
            logger.error(f"Failed to format PHP code: {e}")
            return code
    
    def format_html_line(self, line: str, base_indent: int, indent_size: int) -> str:
        """Format HTML line with proper indentation"""
        # Simple HTML formatting - can be enhanced
        if line.startswith('</'):
            # Closing tag
            return ' ' * (max(0, base_indent - 1) * indent_size) + line
        elif line.startswith('<') and not line.endswith('/>') and '>' in line:
            # Opening tag
            return ' ' * (base_indent * indent_size) + line
        else:
            # Content or self-closing tag
            return ' ' * (base_indent * indent_size) + line
    
    def format_css_code(self, css: str, indent_size: int = 2) -> str:
        """Format CSS code with proper indentation"""
        try:
            # Remove extra whitespace
            css = re.sub(r'\s+', ' ', css.strip())
            
            # Add line breaks after braces and semicolons
            css = re.sub(r'\{', ' {\n', css)
            css = re.sub(r'\}', '\n}\n', css)
            css = re.sub(r';', ';\n', css)
            
            lines = css.split('\n')
            formatted_lines = []
            indent_level = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                
                # Decrease indent for closing braces
                if stripped == '}':
                    indent_level = max(0, indent_level - 1)
                
                # Apply indentation
                indented_line = ' ' * (indent_level * indent_size) + stripped
                formatted_lines.append(indented_line)
                
                # Increase indent for opening braces
                if stripped.endswith('{'):
                    indent_level += 1
            
            return '\n'.join(formatted_lines)
            
        except Exception as e:
            logger.error(f"Failed to format CSS code: {e}")
            return css
    
    def validate_php_syntax(self, code: str) -> Dict[str, Any]:
        """Basic PHP syntax validation"""
        errors = []
        warnings = []
        
        try:
            # Check for basic syntax issues
            if not code.strip().startswith('<?php'):
                warnings.append("PHP code should start with <?php tag")
            
            # Check for unmatched braces
            open_braces = code.count('{')
            close_braces = code.count('}')
            if open_braces != close_braces:
                errors.append(f"Unmatched braces: {open_braces} opening, {close_braces} closing")
            
            # Check for unmatched parentheses
            open_parens = code.count('(')
            close_parens = code.count(')')
            if open_parens != close_parens:
                errors.append(f"Unmatched parentheses: {open_parens} opening, {close_parens} closing")
            
            # Check for common issues
            if '$_POST' in code and 'htmlspecialchars' not in code:
                warnings.append("Consider using htmlspecialchars() for output sanitization")
            
            if 'mysql_' in code:
                warnings.append("Deprecated mysql_ functions detected, use PDO or mysqli instead")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings
            }
            
        except Exception as e:
            logger.error(f"Failed to validate PHP syntax: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': []
            }
    
    def validate_html_structure(self, html: str) -> Dict[str, Any]:
        """Basic HTML structure validation"""
        errors = []
        warnings = []
        
        try:
            # Check for DOCTYPE
            if '<!DOCTYPE' not in html.upper():
                warnings.append("Missing DOCTYPE declaration")
            
            # Check for required elements
            required_elements = ['<html', '<head', '<body']
            for element in required_elements:
                if element not in html.lower():
                    errors.append(f"Missing required element: {element}")
            
            # Check for meta viewport (responsive design)
            if 'viewport' not in html:
                warnings.append("Missing viewport meta tag for responsive design")
            
            # Check for title tag
            if '<title>' not in html.lower():
                warnings.append("Missing title tag")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings
            }
            
        except Exception as e:
            logger.error(f"Failed to validate HTML structure: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': []
            }
    
    def minify_css(self, css: str) -> str:
        """Minify CSS code"""
        try:
            # Remove comments
            css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
            
            # Remove extra whitespace
            css = re.sub(r'\s+', ' ', css)
            
            # Remove spaces around specific characters
            css = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css)
            
            # Remove trailing semicolons before closing braces
            css = re.sub(r';\s*}', '}', css)
            
            return css.strip()
            
        except Exception as e:
            logger.error(f"Failed to minify CSS: {e}")
            return css
    
    def extract_inline_styles(self, html: str) -> Dict[str, str]:
        """Extract inline CSS from HTML"""
        try:
            # Find style tags
            style_pattern = r'<style[^>]*>(.*?)</style>'
            matches = re.findall(style_pattern, html, re.DOTALL | re.IGNORECASE)
            
            extracted_css = '\n'.join(matches)
            
            # Remove style tags from HTML
            clean_html = re.sub(style_pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
            
            return {
                'html': clean_html,
                'css': extracted_css
            }
            
        except Exception as e:
            logger.error(f"Failed to extract inline styles: {e}")
            return {'html': html, 'css': ''}

class OutputFormatter:
    """Utility class for formatting output and reports"""
    
    def format_review_report(self, review_data: Dict[str, Any]) -> str:
        """Format review data as a readable report"""
        try:
            report = []
            report.append(f"# Code Review Report")
            report.append(f"**Template ID:** {review_data.get('template_id', 'Unknown')}")
            report.append(f"**Review Date:** {review_data.get('review_date', 'Unknown')}")
            report.append(f"**Overall Score:** {review_data.get('overall_score', 'N/A')}/10")
            report.append("")
            
            # Categories
            categories = review_data.get('categories', {})
            for category, details in categories.items():
                report.append(f"## {category.replace('_', ' ').title()}")
                report.append(f"**Score:** {details.get('score', 'N/A')}/10")
                report.append("")
                
                comments = details.get('comments', [])
                if comments:
                    for comment in comments:
                        report.append(f"- {comment}")
                    report.append("")
            
            # Recommendations
            recommendations = review_data.get('recommendations', [])
            if recommendations:
                report.append("## Recommendations")
                for i, rec in enumerate(recommendations, 1):
                    priority = rec.get('priority', 'medium').upper()
                    report.append(f"{i}. **[{priority}]** {rec.get('description', 'No description')}")
                    if rec.get('implementation'):
                        report.append(f"   - Implementation: {rec['implementation']}")
                report.append("")
            
            return '\n'.join(report)
            
        except Exception as e:
            logger.error(f"Failed to format review report: {e}")
            return str(review_data)
    
    def format_execution_summary(self, summary_data: Dict[str, Any]) -> str:
        """Format pipeline execution summary"""
        try:
            report = []
            report.append("# Pipeline Execution Summary")
            report.append(f"**Pipeline ID:** {summary_data.get('pipeline_id', 'Unknown')}")
            report.append(f"**Status:** {summary_data.get('status', 'Unknown')}")
            report.append(f"**Start Time:** {summary_data.get('start_time', 'Unknown')}")
            report.append(f"**End Time:** {summary_data.get('end_time', 'Unknown')}")
            report.append("")
            
            # Agents executed
            agents = summary_data.get('agents_executed', [])
            if agents:
                report.append("## Agents Executed")
                for agent in agents:
                    status = "✅" if agent.get('success') else "❌"
                    report.append(f"- {status} {agent.get('agent_id', 'Unknown')} ({agent.get('execution_time', 0):.2f}s)")
                report.append("")
            
            return '\n'.join(report)
            
        except Exception as e:
            logger.error(f"Failed to format execution summary: {e}")
            return str(summary_data)
    
    def format_json_pretty(self, data: Dict[str, Any], indent: int = 2) -> str:
        """Format JSON data with pretty printing"""
        try:
            return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)
        except Exception as e:
            logger.error(f"Failed to format JSON: {e}")
            return str(data)

# Utility functions
def get_code_formatter() -> CodeFormatter:
    """Get a configured code formatter instance"""
    return CodeFormatter()

def get_output_formatter() -> OutputFormatter:
    """Get a configured output formatter instance"""
    return OutputFormatter()

def format_template_code(code: str, language: str = 'php') -> str:
    """Format template code based on language"""
    formatter = CodeFormatter()
    
    if language.lower() == 'php':
        return formatter.format_php_code(code)
    elif language.lower() == 'css':
        return formatter.format_css_code(code)
    else:
        return code

def validate_template_code(code: str, language: str = 'php') -> Dict[str, Any]:
    """Validate template code based on language"""
    formatter = CodeFormatter()
    
    if language.lower() == 'php':
        return formatter.validate_php_syntax(code)
    elif language.lower() == 'html':
        return formatter.validate_html_structure(code)
    else:
        return {'valid': True, 'errors': [], 'warnings': []}
