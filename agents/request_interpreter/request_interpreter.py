# agents/request_interpreter/request_interpreter.py
import json
import re
from pathlib import Path

class RequestInterpreter:
    def __init__(self, config=None):
        if isinstance(config, dict):
            # Config passed as dict (from orchestrator)
            self.config = config
        elif isinstance(config, (str, Path)):
            # Config passed as file path
            self.config_path = Path(config)
            self.config = json.loads(self.config_path.read_text())
        else:
            # Default: load from file
            self.config_path = Path(__file__).parent / "request_interpreter.json"
            self.config = json.loads(self.config_path.read_text())

    def extract_section(self, markdown, header):
        pattern = rf"## {re.escape(header)}\n(.+?)(?=\n## |\Z)"
        match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def parse_request_markdown(self, markdown_text):
        # Debug: check what we received
        print(f"🔍 parse_request_markdown called with:")
        print(f"   markdown_text: {type(markdown_text)} - {str(markdown_text)[:100]}...")

        required_sections = self.config.get("input_format", {}).get("required_sections", [])
        optional_sections = self.config.get("input_format", {}).get("optional_sections", [])

        spec = {
            "template_id": "template_001",
            "project_type": "local_service_page",
            "status": "parsed_from_request",
            "location": {
                "city": "Ramsey",
                "state": "Minnesota",
                "region": "Twin Cities Metro"
            },
            "responsive": True,
            "framework": "none",
            "audience": ["local_customers"],
            "sections": ["hero", "services", "about", "testimonials", "contact"],
            "layout_style": "single_page",
            "primary_cta": "Call Now",
            "technical_notes": {
                "language": "PHP",
                "css": "manual_or_flexbox",
                "js": "minimal"
            }
        }

        for section in required_sections + optional_sections:
            content = self.extract_section(markdown_text, section.replace("_", " ").title())
            if content:
                spec[section] = content

        return spec

    def validate_spec(self, spec):
        required_fields = self.config.get("validation_rules", {}).get("required_fields", [])
        missing = [field for field in required_fields if field not in spec]
        if missing:
            print(f"⚠️  Warning: Missing required fields in spec: {', '.join(missing)}")

    async def run(self, input_file: str, pipeline_id: str):
        """Standard agent interface for orchestrator"""
        from dataclasses import dataclass
        from typing import Dict
        from datetime import datetime

        @dataclass
        class AgentResult:
            agent_id: str
            success: bool
            output_file: str = ""
            error_message: str = ""
            execution_time: float = 0.0
            metadata: Dict = None

        try:
            # Debug: print what we received
            print(f"🔍 request_interpreter.run called with:")
            print(f"   input_file: {input_file} (type: {type(input_file)})")
            print(f"   pipeline_id: {pipeline_id} (type: {type(pipeline_id)})")

            # Convert input_file to Path object
            input_path = Path(input_file)

            # Generate output path using pipeline_id for consistency
            template_id = pipeline_id.replace('pipeline_', '')
            output_path = Path(f"template_generations/template_{template_id}/specs/template_spec.json")

            # Check if input file exists
            if not input_path.exists():
                return AgentResult(
                    agent_id="request_interpreter",
                    success=False,
                    error_message=f"Input file not found: {input_path}"
                )

            # Read and process the markdown file
            markdown = input_path.read_text(encoding='utf-8')
            structured = self.parse_request_markdown(markdown)
            self.validate_spec(structured)

            # Create output directory and write spec file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(structured, indent=2), encoding='utf-8')

            print(f"✅ Spec written to {output_path}")

            return AgentResult(
                agent_id="request_interpreter",
                success=True,
                output_file=str(output_path),
                metadata={"template_id": structured.get("template_id")}
            )

        except Exception as e:
            return AgentResult(
                agent_id="request_interpreter",
                success=False,
                error_message=str(e)
            )

    def run_old(self, input_path: str, output_path: str) -> bool:
        """Legacy method for backward compatibility"""
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            print(f"❌ Input file not found: {input_path}")
            return False

        markdown = input_path.read_text()
        structured = self.parse_request_markdown(markdown)
        self.validate_spec(structured)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(structured, indent=2))

        print(f"✅ Spec written to {output_path}")
        return True
