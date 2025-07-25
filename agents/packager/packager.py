import os
import shutil
import json
import zipfile
import re
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
            # Check if we're in organized template structure
            if "template_generations" in input_file:
                return await self.run_organized_structure(input_file, pipeline_id)
            else:
                return await self.run_legacy_structure(input_file, pipeline_id)

        except Exception as e:
            return AgentResult(
                agent_id="packager",
                success=False,
                error_message=str(e)
            )

    async def run_organized_structure(self, input_file: str, pipeline_id: str) -> AgentResult:
        """Handle packaging for organized template structure with WordPress themes"""
        try:
            # Extract template_id from pipeline_id
            template_id = pipeline_id.replace('pipeline_', '')

            # Find the template directory
            template_dir = Path(input_file).parent

            # Look for WordPress theme directory
            wp_theme_dirs = list(template_dir.glob("*wordpress_theme*")) + \
                           list(template_dir.glob("*component_enhanced_theme*")) + \
                           list(template_dir.glob("*seo_enhanced_theme*"))

            if not wp_theme_dirs:
                # Fallback to legacy packaging
                return await self.run_legacy_structure(input_file, pipeline_id)

            # Use the most enhanced theme directory available
            wp_theme_dir = wp_theme_dirs[-1]  # Last one should be most enhanced

            # Load spec file to get business info for naming
            spec_file = template_dir / "specs" / "template_spec.json"
            business_name = "wordpress-theme"
            theme_type = "business"

            if spec_file.exists():
                spec_data = self.load_json(spec_file)
                business_name = self.extract_business_name(spec_data)
                theme_type = spec_data.get("project_type", "business").replace("_", "-")

            # Create distinct theme name
            theme_name = self.generate_theme_name(business_name, theme_type, template_id)

            # Create output directory
            output_dir = Path("wordpress_theme_packages")
            output_dir.mkdir(exist_ok=True)

            # Create zip file
            zip_path = output_dir / f"{theme_name}.zip"
            self.create_wordpress_theme_zip(wp_theme_dir, zip_path, theme_name)

            # Also create legacy package for compatibility
            await self.create_legacy_package(template_dir, template_id)

            print(f"✅ WordPress theme package created: {zip_path}")

            return AgentResult(
                agent_id="packager",
                success=True,
                output_file=str(zip_path),
                metadata={
                    "template_id": template_id,
                    "theme_name": theme_name,
                    "business_name": business_name,
                    "package_type": "wordpress_theme_zip"
                }
            )

        except Exception as e:
            return AgentResult(
                agent_id="packager",
                success=False,
                error_message=str(e)
            )

    async def run_legacy_structure(self, input_file: str, pipeline_id: str) -> AgentResult:
        """Handle legacy packaging structure"""
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

    def extract_business_name(self, spec_data: dict) -> str:
        """Extract business name from spec data for theme naming"""
        # Try different fields that might contain business name
        business_name = (
            spec_data.get("business_name", "") or
            spec_data.get("company_name", "") or
            spec_data.get("site_name", "") or
            spec_data.get("title", "") or
            ""
        )

        # If not found in direct fields, try to extract from project_description
        if not business_name:
            description = spec_data.get("project_description", "")
            # Look for patterns like "**Business Name**" or "Business Name"
            import re
            patterns = [
                r'\*\*([^*]+)\*\*',  # **Business Name**
                r'for\s+([A-Z][^,\.]+)',  # "for Business Name"
                r'website\s+for\s+([A-Z][^,\.]+)',  # "website for Business Name"
                r'([A-Z][^,\.]+)\s*,\s*a\s+',  # "Business Name, a local"
            ]

            for pattern in patterns:
                match = re.search(pattern, description)
                if match:
                    business_name = match.group(1).strip()
                    break

        # Clean up the name for file naming
        if business_name:
            business_name = re.sub(r'[^\w\s-]', '', business_name.lower())
            business_name = re.sub(r'\s+', '-', business_name.strip())
            business_name = re.sub(r'-+', '-', business_name)

        return business_name or "business"

    def generate_theme_name(self, business_name: str, theme_type: str, template_id: str) -> str:
        """Generate a distinct theme name"""
        # Create timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")

        # Combine elements for distinct name
        theme_name = f"{business_name}-{theme_type}-theme-{template_id}-{timestamp}"

        # Ensure it's a valid filename
        theme_name = re.sub(r'[^\w\s-]', '', theme_name)
        theme_name = re.sub(r'\s+', '-', theme_name)
        theme_name = re.sub(r'-+', '-', theme_name)

        return theme_name

    def create_wordpress_theme_zip(self, theme_dir: Path, zip_path: Path, theme_name: str):
        """Create a zip file of the WordPress theme"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from the theme directory
            for file_path in theme_dir.rglob('*'):
                if file_path.is_file():
                    # Create archive path with theme name as root folder
                    archive_path = theme_name / file_path.relative_to(theme_dir)
                    zipf.write(file_path, archive_path)

        print(f"📦 Created WordPress theme zip: {zip_path}")

    async def create_legacy_package(self, template_dir: Path, template_id: str):
        """Create legacy package structure for compatibility"""
        try:
            base_dir = template_dir / "final"
            base_dir.mkdir(exist_ok=True)

            # Copy key files if they exist
            files_to_copy = [
                ("templates/template_{}.php".format(template_id), "index.php"),
                ("templates/template_{}.cta.php".format(template_id), "index-cta.php"),
                ("specs/template_spec.json", "template_spec.json"),
                ("reviews/template_{}.design.md".format(template_id), "design_review.md")
            ]

            for src_rel, dst_name in files_to_copy:
                src_path = template_dir / src_rel
                dst_path = base_dir / dst_name
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)

            # Create simple README
            readme_path = base_dir / "README.md"
            readme_content = f"""# Template Package {template_id}

This package contains the generated template files and WordPress theme.

## Contents
- WordPress theme zip file in `../wordpress_theme_packages/`
- Original template files
- Design reviews and specifications

## Installation
Extract the WordPress theme zip file and upload to your WordPress installation.
"""
            readme_path.write_text(readme_content)

        except Exception as e:
            print(f"⚠️ Could not create legacy package: {e}")

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
