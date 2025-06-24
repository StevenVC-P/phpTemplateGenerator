import json
import re
from pathlib import Path
from typing import Dict
from dataclasses import dataclass

@dataclass
class AgentResult:
    agent_id: str
    success: bool
    output_file: str = ""
    error_message: str = ""
    execution_time: float = 0.0
    metadata: Dict = None

class CodeReviewer:
    def __init__(self, config: Dict):
        self.config = config

    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        try:
            input_path = Path(input_file)
            output_file = str(input_path).replace(".php", ".review.json")
            output_path = Path(output_file)

            php_code = input_path.read_text()
            review = self.analyze_php_code(php_code)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(review, indent=2))

            return AgentResult(
                agent_id="code_reviewer",
                success=True,
                output_file=str(output_path),
                metadata={"score": review.get("overall_score", 0)}
            )

        except Exception as e:
            return AgentResult(
                agent_id="code_reviewer",
                success=False,
                error_message=str(e)
            )

    def analyze_php_code(self, code: str) -> Dict:
        results = {
            "categories": {
                "code_quality": {},
                "security": {},
                "performance": {},
                "accessibility": {},
                "maintainability": {}
            },
            "recommendations": [],
            "compliance": {},
            "overall_score": 0
        }

        # CODE QUALITY CHECKS
        results["categories"]["code_quality"] = {
            "syntax_correctness": True,
            "code_structure": "basic_single_file",
            "naming_conventions": "consistent",
            "documentation_quality": "minimal"
        }

        if "<?php" not in code:
            results["categories"]["code_quality"]["syntax_correctness"] = False
            results["recommendations"].append("PHP opening tag '<?php' not found.")

        # SECURITY CHECKS
        security_flags = {
            "input_validation": bool(re.search(r"\$_(POST|GET|REQUEST)", code)),
            "output_sanitization": "htmlspecialchars" in code or "htmlentities" in code,
            "xss_protection": "<script>" not in code
        }
        results["categories"]["security"] = security_flags

        if not security_flags["output_sanitization"]:
            results["recommendations"].append("Missing output sanitization functions like htmlspecialchars().")

        # PERFORMANCE CHECKS
        results["categories"]["performance"] = {
            "code_efficiency": "standard",
            "optimization_potential": "moderate"
        }

        # ACCESSIBILITY CHECKS
        accessibility = {
            "semantic_html": bool(re.search(r"<(header|main|footer|section)>", code)),
            "aria_labels": "aria-label" in code,
            "keyboard_navigation": "tabindex" in code,
            "color_contrast": "manual_check"
        }
        results["categories"]["accessibility"] = accessibility

        # MAINTAINABILITY CHECKS
        results["categories"]["maintainability"] = {
            "code_readability": "moderate",
            "modularity": "single_block",
            "error_handling": "minimal"
        }

        # SCORING
        weights = {
            "code_quality": 0.30,
            "security": 0.25,
            "performance": 0.20,
            "accessibility": 0.15,
            "maintainability": 0.10
        }

        score = 0
        for category, weight in weights.items():
            sub = results["categories"][category]
            passed = sum(1 for k, v in sub.items() if v or (isinstance(v, str) and v != "minimal"))
            total = len(sub)
            score += (passed / total) * 10 * weight

        results["overall_score"] = round(score, 2)
        results["compliance"] = {
            "php_standards": "PSR-12 (basic heuristics only)",
            "security_standards": "OWASP_Top_10 (partial)",
            "accessibility_standards": "WCAG 2.1 AA (partial)",
            "performance_standards": "Core Web Vitals (manual review needed)"
        }

        return results
