import json
from pathlib import Path
from datetime import datetime
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

class PromptDesigner:
    def __init__(self, config: Dict):
        self.config = config

    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        try:
            input_path = Path(input_file)
            template_spec = self.load_spec(input_path)
            prompt_data = self.create_prompt(template_spec)

            # Put prompt in the correct directory
            template_dir = input_path.parent.parent  # Go up from specs/ to template_xxx/
            prompts_dir = template_dir / "prompts"
            prompts_dir.mkdir(exist_ok=True)
            output_file = prompts_dir / f"prompt_{pipeline_id.replace('pipeline_', '')}.json"
            self.save_prompt(prompt_data, output_file)

            return AgentResult(
                agent_id="prompt_designer",
                success=True,
                output_file=str(output_file),
                metadata={"generated_at": prompt_data.get("timestamp")}
            )

        except Exception as e:
            return AgentResult(
                agent_id="prompt_designer",
                success=False,
                error_message=str(e)
            )

    def load_spec(self, path: Path) -> Dict:
        with path.open() as f:
            return json.load(f)

    def create_prompt(self, template_spec: Dict) -> Dict:
        project_type = template_spec.get("project_type", "local_service_page")
        business_name = template_spec.get("business_name", "Professional Service")
        services = template_spec.get("services", ["Professional Services"])
        location = template_spec.get("location", {})
        target_audience = template_spec.get("target_audience", "")
        requirements = template_spec.get("requirements", "")
        design_preferences = template_spec.get("design_preferences", "")
        sections = ", ".join(template_spec.get("sections", []))

        # Extract key requirements as bullet points
        req_lines = [line.strip() for line in requirements.split('\n') if line.strip().startswith('-')]
        requirements_list = "\n".join(req_lines) if req_lines else requirements

        # Extract design preferences as bullet points
        design_lines = [line.strip() for line in design_preferences.split('\n') if line.strip().startswith('-')]
        design_list = "\n".join(design_lines) if design_lines else design_preferences

        system_prompt = "You are an expert PHP developer and modern web designer specializing in creating professional, conversion-focused landing pages."

        user_prompt = f"""
Create a professional PHP landing page template for "{business_name}" - a {project_type.replace('_', ' ')}.

BUSINESS DETAILS:
- Business Name: {business_name}
- Services Offered: {', '.join(services)}
- Location: {location.get('city', 'Local Area')}, {location.get('state', 'State')}
- Primary CTA: {template_spec.get('primary_cta', 'Contact Us')}

TARGET AUDIENCE:
{target_audience}

REQUIREMENTS:
{requirements_list}

DESIGN PREFERENCES:
{design_list}

SECTIONS TO INCLUDE: {sections}

The template should be specifically tailored to this business, using the actual business name, services, and location throughout the content. Create realistic, relevant content that matches the business type and target audience.

Ensure code quality, semantic HTML, and good accessibility practices.
"""

        constraints = [
            "Use the actual business name and services throughout the template",
            "Create location-specific content and references",
            "Use modern PHP practices with proper form handling",
            "Responsive layout using Flexbox or Grid",
            "No external frameworks or dependencies",
            "Minimal JavaScript, focus on CSS for interactions",
            "Include realistic testimonials and content relevant to the business type"
        ]

        return {
            "agent_id": "prompt_designer",
            "status": "complete",
            "timestamp": datetime.now().isoformat(),
            "business_context": {
                "name": business_name,
                "services": services,
                "location": location,
                "project_type": project_type
            },
            "system_prompt": system_prompt.strip(),
            "user_prompt": user_prompt.strip(),
            "constraints": constraints,
            "output_format": "One complete PHP file with business-specific content, embedded CSS, and proper form handling.",
            "examples": []
        }

    def save_prompt(self, prompt_data: Dict, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as f:
            json.dump(prompt_data, f, indent=2)
