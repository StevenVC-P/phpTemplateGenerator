# agents/theme_validator/theme_validator.py

import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.agent_interface import AgentInterface, AgentResult, AgentStatus
from utils.logging_helper import get_pipeline_logger

@dataclass
class ValidationIssue:
    """Represents a validation issue found in the theme"""
    severity: str  # "error", "warning", "info"
    category: str  # "structure", "html", "css", "php", "accessibility", "seo"
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

@dataclass
class ValidationReport:
    """Complete validation report for a WordPress theme"""
    theme_path: str
    overall_score: float
    issues: List[ValidationIssue]
    file_analysis: Dict[str, Any]
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "theme_path": self.theme_path,
            "overall_score": self.overall_score,
            "issues": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "file_path": issue.file_path,
                    "line_number": issue.line_number,
                    "suggestion": issue.suggestion
                }
                for issue in self.issues
            ],
            "file_analysis": self.file_analysis,
            "recommendations": self.recommendations,
            "summary": {
                "total_issues": len(self.issues),
                "errors": len([i for i in self.issues if i.severity == "error"]),
                "warnings": len([i for i in self.issues if i.severity == "warning"]),
                "info": len([i for i in self.issues if i.severity == "info"])
            }
        }

class ThemeValidator(AgentInterface):
    """Validates WordPress themes for quality, structure, and compliance"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.required_files = [
            "style.css",
            "index.php",
            "functions.php"
        ]
        self.recommended_files = [
            "header.php",
            "footer.php",
            "single.php",
            "page.php",
            "404.php"
        ]
    
    async def run(self, input_path: str, context: Dict[str, Any]) -> AgentResult:
        """Validate a WordPress theme directory"""
        self._start_execution()
        
        try:
            theme_path = Path(input_path)
            pipeline_id = context.get('pipeline_id', 'unknown')
            
            # Setup logging
            logger = get_pipeline_logger(self.agent_id, pipeline_id)
            logger.log_agent_start(input_path, context)
            
            if not theme_path.exists():
                error_msg = f"Theme directory not found: {input_path}"
                logger.error(error_msg)
                return self._end_execution(self._create_error_result(error_msg))
            
            # Perform validation
            validation_report = self._validate_theme(theme_path, logger)
            
            # Generate output path
            from utils.path_manager import PathManager, PipelineContext
            path_context = PipelineContext(
                pipeline_id=pipeline_id,
                template_id=context.get('template_id', pipeline_id),
                request_file=context.get('request_file', '')
            )
            path_manager = PathManager(path_context)
            output_path = path_manager.get_output_path(self.agent_id)
            
            # Save validation report
            self.ensure_output_directory(str(output_path))
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(validation_report.to_dict(), f, indent=2)
            
            logger.log_agent_end(True, str(output_path))
            logger.save_structured_log()
            
            # Determine if validation passed
            error_count = len([i for i in validation_report.issues if i.severity == "error"])
            success = error_count == 0
            
            result = self._create_success_result(
                message=f"Theme validation completed - {error_count} errors found",
                output_path=str(output_path),
                quality_score=validation_report.overall_score,
                metadata={
                    "validation_passed": success,
                    "error_count": error_count,
                    "warning_count": len([i for i in validation_report.issues if i.severity == "warning"]),
                    "overall_score": validation_report.overall_score
                }
            )
            
            if not success:
                result.status = AgentStatus.PARTIAL
                result.warnings = [f"Theme has {error_count} validation errors"]
            
            return self._end_execution(result)
            
        except Exception as e:
            return self._end_execution(self._create_error_result(e))
    
    def _validate_theme(self, theme_path: Path, logger) -> ValidationReport:
        """Perform comprehensive theme validation"""
        issues = []
        file_analysis = {}
        
        logger.info("Starting theme validation")
        
        # 1. Validate file structure
        structure_issues = self._validate_file_structure(theme_path)
        issues.extend(structure_issues)
        
        # 2. Validate individual files
        for file_path in theme_path.rglob("*"):
            if file_path.is_file():
                file_issues, analysis = self._validate_file(file_path, theme_path)
                issues.extend(file_issues)
                file_analysis[str(file_path.relative_to(theme_path))] = analysis
        
        # 3. Calculate overall score
        overall_score = self._calculate_overall_score(issues)
        
        # 4. Generate recommendations
        recommendations = self._generate_recommendations(issues)
        
        logger.info(f"Validation completed - Score: {overall_score:.1f}/10")
        
        return ValidationReport(
            theme_path=str(theme_path),
            overall_score=overall_score,
            issues=issues,
            file_analysis=file_analysis,
            recommendations=recommendations
        )
    
    def _validate_file_structure(self, theme_path: Path) -> List[ValidationIssue]:
        """Validate WordPress theme file structure"""
        issues = []
        
        # Check required files
        for required_file in self.required_files:
            file_path = theme_path / required_file
            if not file_path.exists():
                issues.append(ValidationIssue(
                    severity="error",
                    category="structure",
                    message=f"Required file missing: {required_file}",
                    suggestion=f"Create {required_file} file in theme root"
                ))
        
        # Check recommended files
        for recommended_file in self.recommended_files:
            file_path = theme_path / recommended_file
            if not file_path.exists():
                issues.append(ValidationIssue(
                    severity="warning",
                    category="structure",
                    message=f"Recommended file missing: {recommended_file}",
                    suggestion=f"Consider adding {recommended_file} for better theme functionality"
                ))
        
        # Check for style.css header
        style_css = theme_path / "style.css"
        if style_css.exists():
            content = style_css.read_text(encoding='utf-8', errors='ignore')
            if not re.search(r'/\*\s*Theme Name:', content):
                issues.append(ValidationIssue(
                    severity="error",
                    category="structure",
                    message="style.css missing required theme header",
                    file_path="style.css",
                    suggestion="Add theme header comment with Theme Name, Description, etc."
                ))
        
        return issues
    
    def _validate_file(self, file_path: Path, theme_root: Path) -> tuple[List[ValidationIssue], Dict[str, Any]]:
        """Validate individual file"""
        issues = []
        analysis = {"file_type": file_path.suffix, "size": file_path.stat().st_size}
        
        try:
            if file_path.suffix == '.php':
                issues.extend(self._validate_php_file(file_path))
                analysis.update(self._analyze_php_file(file_path))
            elif file_path.suffix == '.css':
                issues.extend(self._validate_css_file(file_path))
                analysis.update(self._analyze_css_file(file_path))
            elif file_path.suffix in ['.html', '.htm']:
                issues.extend(self._validate_html_file(file_path))
                analysis.update(self._analyze_html_file(file_path))
        except Exception as e:
            issues.append(ValidationIssue(
                severity="warning",
                category="structure",
                message=f"Could not validate file: {str(e)}",
                file_path=str(file_path.relative_to(theme_root))
            ))
        
        return issues, analysis
    
    def _validate_php_file(self, file_path: Path) -> List[ValidationIssue]:
        """Validate PHP file"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Check for PHP opening tag
            if not content.strip().startswith('<?php'):
                issues.append(ValidationIssue(
                    severity="warning",
                    category="php",
                    message="PHP file should start with <?php tag",
                    file_path=str(file_path.name)
                ))
            
            # Check for security issues
            dangerous_functions = ['eval', 'exec', 'system', 'shell_exec']
            for func in dangerous_functions:
                if re.search(rf'\b{func}\s*\(', content):
                    issues.append(ValidationIssue(
                        severity="error",
                        category="php",
                        message=f"Potentially dangerous function used: {func}",
                        file_path=str(file_path.name),
                        suggestion=f"Remove or secure usage of {func} function"
                    ))
            
            # Check for WordPress functions
            if file_path.name == 'functions.php':
                if 'wp_enqueue_style' not in content:
                    issues.append(ValidationIssue(
                        severity="warning",
                        category="php",
                        message="functions.php should enqueue styles properly",
                        file_path=str(file_path.name),
                        suggestion="Use wp_enqueue_style() to load CSS files"
                    ))
        
        except UnicodeDecodeError:
            issues.append(ValidationIssue(
                severity="warning",
                category="php",
                message="File encoding issues detected",
                file_path=str(file_path.name)
            ))
        
        return issues
    
    def _validate_css_file(self, file_path: Path) -> List[ValidationIssue]:
        """Validate CSS file"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Check for basic CSS syntax issues
            if content.count('{') != content.count('}'):
                issues.append(ValidationIssue(
                    severity="error",
                    category="css",
                    message="Mismatched CSS braces",
                    file_path=str(file_path.name)
                ))
            
            # Check for responsive design
            if '@media' not in content and file_path.name == 'style.css':
                issues.append(ValidationIssue(
                    severity="warning",
                    category="css",
                    message="No responsive design detected",
                    file_path=str(file_path.name),
                    suggestion="Add media queries for responsive design"
                ))
        
        except UnicodeDecodeError:
            issues.append(ValidationIssue(
                severity="warning",
                category="css",
                message="File encoding issues detected",
                file_path=str(file_path.name)
            ))
        
        return issues
    
    def _validate_html_file(self, file_path: Path) -> List[ValidationIssue]:
        """Validate HTML content"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for basic HTML structure
            if not soup.find('html'):
                issues.append(ValidationIssue(
                    severity="warning",
                    category="html",
                    message="Missing HTML tag",
                    file_path=str(file_path.name)
                ))
            
            # Check for accessibility
            images = soup.find_all('img')
            for img in images:
                if not img.get('alt'):
                    issues.append(ValidationIssue(
                        severity="warning",
                        category="accessibility",
                        message="Image missing alt attribute",
                        file_path=str(file_path.name),
                        suggestion="Add alt attributes to all images"
                    ))
        
        except Exception:
            issues.append(ValidationIssue(
                severity="info",
                category="html",
                message="Could not parse HTML content",
                file_path=str(file_path.name)
            ))
        
        return issues
    
    def _analyze_php_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze PHP file for metrics"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return {
                "lines": len(content.splitlines()),
                "has_wordpress_functions": any(func in content for func in ['wp_', 'get_', 'the_']),
                "has_security_checks": 'defined' in content and 'ABSPATH' in content
            }
        except:
            return {"error": "Could not analyze file"}
    
    def _analyze_css_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze CSS file for metrics"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return {
                "lines": len(content.splitlines()),
                "has_media_queries": '@media' in content,
                "rule_count": content.count('{')
            }
        except:
            return {"error": "Could not analyze file"}
    
    def _analyze_html_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze HTML file for metrics"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            return {
                "lines": len(content.splitlines()),
                "tag_count": len(soup.find_all()),
                "has_semantic_tags": bool(soup.find_all(['header', 'nav', 'main', 'section', 'article', 'footer']))
            }
        except:
            return {"error": "Could not analyze file"}
    
    def _calculate_overall_score(self, issues: List[ValidationIssue]) -> float:
        """Calculate overall quality score (0-10)"""
        base_score = 10.0
        
        for issue in issues:
            if issue.severity == "error":
                base_score -= 2.0
            elif issue.severity == "warning":
                base_score -= 0.5
            elif issue.severity == "info":
                base_score -= 0.1
        
        return max(0.0, min(10.0, base_score))
    
    def _generate_recommendations(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate actionable recommendations based on issues"""
        recommendations = []
        
        error_count = len([i for i in issues if i.severity == "error"])
        warning_count = len([i for i in issues if i.severity == "warning"])
        
        if error_count > 0:
            recommendations.append(f"Fix {error_count} critical errors before deployment")
        
        if warning_count > 5:
            recommendations.append("Consider addressing warnings to improve theme quality")
        
        # Category-specific recommendations
        categories = set(issue.category for issue in issues)
        
        if "accessibility" in categories:
            recommendations.append("Improve accessibility by adding alt text and ARIA labels")
        
        if "css" in categories:
            recommendations.append("Review CSS for responsive design and syntax issues")
        
        if "php" in categories:
            recommendations.append("Review PHP code for security and WordPress best practices")
        
        if not recommendations:
            recommendations.append("Theme validation passed - ready for deployment")
        
        return recommendations
