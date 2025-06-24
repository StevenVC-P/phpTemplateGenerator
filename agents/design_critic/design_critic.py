import re
from pathlib import Path
from typing import Dict
from dataclasses import dataclass
from bs4 import BeautifulSoup

@dataclass
class AgentResult:
    agent_id: str
    success: bool
    output_file: str = ""
    error_message: str = ""
    execution_time: float = 0.0
    metadata: Dict = None

class DesignCritic:
    def __init__(self, config: Dict):
        self.config = config

    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        try:
            input_path = Path(input_file)
            html = input_path.read_text(encoding='utf-8', errors='ignore')
            soup = BeautifulSoup(html, "html.parser")
            template_id = self.extract_template_id(input_path.name)
            output_path = input_path.parent / f"template_{template_id}.design.md"

            report = "\n".join([
                self.generate_summary(soup),
                self.assess_visual_design(soup),
                self.assess_ux(soup),
                self.assess_conversion(soup),
                self.assess_accessibility(soup),
                self.generate_recommendations()
            ])

            output_path.write_text(report.strip())

            return AgentResult(
                agent_id="design_critic",
                success=True,
                output_file=str(output_path),
                metadata={"template_id": template_id}
            )

        except Exception as e:
            return AgentResult(
                agent_id="design_critic",
                success=False,
                error_message=str(e)
            )

    def extract_template_id(self, filename: str) -> str:
        match = re.search(r"template_(\d+)\.php", filename)
        return match.group(1) if match else "000"

    def generate_summary(self, soup) -> str:
        headings = soup.find_all(re.compile(r"h[1-6]"))
        nav = soup.find("nav")
        ctas = soup.find_all("a", string=re.compile(r"(call|contact|get|free|quote)", re.I))
        return f"""\n### Executive Summary
This design appears to follow a {len(headings)}-heading structure. It {'includes' if nav else 'does not include'} a navigation element. {len(ctas)} call-to-action(s) detected.
"""

    def assess_visual_design(self, soup) -> str:
        classes = " ".join([cls for tag in soup.find_all() for cls in tag.get("class", []) if isinstance(cls, str)])
        score = 7 if "hero" in classes or "section" in classes else 5
        return f"""\n### Visual Design Assessment
- Use of semantic sections: {'Yes' if soup.find_all('section') else 'No'}
- Visual balance inferred via layout tags: {'Good' if soup.find('div', class_='grid') else 'Moderate'}
- Typography tags (h1–h6): {len(soup.find_all(re.compile('h[1-6]')))}
**Score:** {score}/10
"""

    def assess_ux(self, soup) -> str:
        nav = soup.find("nav")
        footer = soup.find("footer")
        flow_elements = ['hero', 'services', 'about', 'testimonials', 'contact']
        found = [cls for cls in flow_elements if soup.find(class_=re.compile(cls))]
        return f"""\n### UX Evaluation
- Navigation present: {'Yes' if nav else 'No'}
- Footer present: {'Yes' if footer else 'No'}
- Recognized user flow sections: {', '.join(found) or 'None detected'}
**Score:** {6 + len(found)//2}/10
"""

    def assess_conversion(self, soup) -> str:
        ctas = soup.find_all("a", string=re.compile(r"(call|quote|contact|get)", re.I))
        trust_signals = soup.find_all(string=re.compile(r"(licensed|insured|guarantee|satisfaction)", re.I))
        return f"""\n### Conversion Analysis
- CTAs: {len(ctas)} found
- Trust signals detected: {len(trust_signals)}
**Score:** {min(10, 5 + len(ctas) + len(trust_signals))}/10
"""

    def assess_accessibility(self, soup) -> str:
        aria = soup.find_all(attrs={"aria-label": True})
        alt_texts = soup.find_all("img", alt=True)
        return f"""\n### Accessibility Review
- ARIA labels: {len(aria)}
- Images with alt text: {len(alt_texts)}
**Score:** {7 if len(aria) + len(alt_texts) > 3 else 5}/10
"""

    def generate_recommendations(self) -> str:
        return f"""\n### Recommendations
- Ensure all CTA buttons have descriptive labels
- Improve semantic use of headings for better screen reader navigation
- Consider adding skip-to-content links for accessibility
"""
