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
        target = ", ".join(template_spec.get("target_audience", []))
        requirements = ", ".join(template_spec.get("requirements", []))
        sections = ", ".join(template_spec.get("sections", []))

        system_prompt = "You are an expert PHP developer and modern web designer."

        user_prompt = f"""
Design a clean, responsive PHP landing page for a {project_type.replace('_', ' ')}.
Target Audience: {target}
Requirements: {requirements}
Sections: {sections}
Ensure code quality, semantic HTML, and good accessibility practices.
"""

        constraints = [
            "Use modern PHP practices",
            "Responsive layout using Flexbox or Grid",
            "No frameworks",
            "Minimal JavaScript"
        ]

        return {
            "agent_id": "prompt_designer",
            "status": "complete",
            "timestamp": datetime.now().isoformat(),
            "system_prompt": system_prompt.strip(),
            "user_prompt": user_prompt.strip(),
            "constraints": constraints,
            "output_format": "One complete PHP file with all layout and style embedded or clearly documented.",
            "examples": []
        }

    def save_prompt(self, prompt_data: Dict, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as f:
            json.dump(prompt_data, f, indent=2)
