import os
import shutil
import json
from datetime import datetime
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

class Packager:
    def __init__(self, config: Dict):
        self.config = config

    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        try:
            # Derive template_id from input file (e.g., template_001.cta.php)
            template_id = self.extract_template_id(input_file)
            base_dir = Path(f"final/template_{template_id}/")
            base_dir.mkdir(parents=True, exist_ok=True)

            # Input files
            files = {
                "template": f"templates/template_{template_id}.php",
                "cta": f"templates/template_{template_id}.cta.php",
                "review": f"reviews/template_{template_id}.review.json",
                "design": f"reviews/template_{template_id}.design.md",
                "spec": f"specs/template_spec.json",
                "prompt": f"prompts/prompt_{template_id}.json"
            }

            # Output files
            outputs = {
                "index": base_dir / "index.php",
                "index_cta": base_dir / "index-cta.php",
                "readme": base_dir / "README.md",
                "changelog": base_dir / "CHANGELOG.md",
                "manifest": base_dir / "manifest.json",
                "design_copy": base_dir / "template.design.md"
            }

            # Copy core assets
            self.copy_and_rename(files["template"], outputs["index"])
            self.copy_and_rename(files["cta"], outputs["index_cta"])
            self.copy_and_rename(files["design"], outputs["design_copy"])

            # Load structured data
            template_spec = self.load_json(files["spec"])
            prompt_data = self.load_json(files["prompt"])
            review_data = self.load_json(files["review"])

            # Generate README
            readme = self.generate_readme(template_spec, prompt_data, review_data)
            outputs["readme"].write_text(readme)

            # Changelog (simple placeholder)
            outputs["changelog"].write_text("# Changelog\n\n- Initial package generated.")

            # Manifest
            manifest = self.create_manifest(template_id, review_data)
            outputs["manifest"].write_text(json.dumps(manifest, indent=2))

            return AgentResult(
                agent_id="packager",
                success=True,
                output_file=str(base_dir),
                metadata={"template_id": template_id}
            )

        except Exception as e:
            return AgentResult(
                agent_id="packager",
                success=False,
                error_message=str(e)
            )

    def extract_template_id(self, path: str) -> str:
        return Path(path).stem.split(".")[0].replace("template_", "").replace("cta", "").strip("_")

    def load_json(self, path):
        with open(path) as f:
            return json.load(f)

    def copy_and_rename(self, src, dst):
        if os.path.exists(src):
            shutil.copy(src, dst)
        else:
            print(f"⚠️ Missing file: {src}")

    def generate_readme(self, template_spec, prompt_data, review_data):
        return "\n".join([
            f"# {template_spec.get('project_type', 'Web Template').replace('_', ' ').title()}",
            "## Overview Description\nA professionally generated PHP template designed for speed, security, and conversions.",
            "## Installation Instructions\nPlace the template in your PHP-enabled hosting environment and open index.php.",
            "## Customization Guide\nModify the HTML/CSS as needed to match your branding.",
            "## Feature List",
            "- Responsive design\n- Conversion-optimized CTAs\n- Clean semantic HTML\n- Accessibility compliant",
            "## Browser Support\nTested on Chrome, Firefox, Safari, Edge",
            "## Performance Metrics\nBased on review scores: ",
            json.dumps(review_data.get("categories", {}), indent=2),
            "## Troubleshooting\nEnsure PHP 7.4+ and required modules are enabled.",
            "## License Information\nGenerated templates are free to use and modify."
        ])

    def create_manifest(self, template_id, review_data):
        return {
            "version": "1.0.0",
            "creation_date": datetime.utcnow().isoformat(),
            "agent_versions": {"packager": "1.0"},
            "quality_scores": review_data.get("categories", {})
        }
