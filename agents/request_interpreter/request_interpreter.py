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

    def extract_business_name(self, markdown_text):
        """Extract business name from various patterns in the markdown"""
        # Look for specific business name patterns first
        patterns = [
            r"for\s+([A-Z][A-Za-z\s&]+?),\s+a\s+",  # "for TechFlow Solutions, a local"
            r"for\s+([A-Z][A-Za-z\s&]+?)\s+(?:business|company|service|shop|store|agency|firm)",
            r"(?:business|company|service|shop|store|agency|firm):\s*([A-Z][A-Za-z\s&]+)",
            r"([A-Z][A-Za-z\s&]+?)\s+(?:business|company|service|shop|store|agency|firm)",
            r"# ([A-Z][A-Za-z\s&]+?)(?:\s+(?:Template|Request|Landing|Page))",
        ]

        for pattern in patterns:
            match = re.search(pattern, markdown_text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Filter out generic terms, short matches, and text that looks like descriptions
                excluded_terms = ['local', 'professional', 'modern', 'clean', 'business', 'service',
                                'a local', 'the local', 'project description', 'create a', 'template']
                if (len(name) > 3 and len(name) < 50 and  # Reasonable length for business name
                    name.lower() not in excluded_terms and
                    not any(excluded in name.lower() for excluded in excluded_terms) and
                    not name.startswith('Create') and not name.startswith('Project')):
                    return name

        # Try to extract from project description
        project_desc = self.extract_section(markdown_text, "Project Description")
        if project_desc:
            # Look for specific business types first
            business_types = {
                'it consulting': 'IT Consulting Services',
                'hvac': 'HVAC Services',
                'plumbing': 'Plumbing Services',
                'electrical': 'Electrical Services',
                'landscaping': 'Landscaping Services',
                'cleaning': 'Cleaning Services',
                'restaurant': 'Restaurant',
                'dental': 'Dental Practice',
                'law': 'Law Firm',
                'accounting': 'Accounting Services',
                'consulting': 'Consulting Services'
            }

            for keyword, business_name in business_types.items():
                if keyword in project_desc.lower():
                    return business_name

        # Default fallback
        return "Professional Service"

    def extract_services(self, markdown_text):
        """Extract services from the markdown content"""
        services = []

        # Look for services section with multiple possible headers
        services_section = self.extract_section(markdown_text, "Services Offered")
        if not services_section:
            services_section = self.extract_section(markdown_text, "Services")
        if not services_section:
            services_section = self.extract_section(markdown_text, "Our Services")
        if not services_section:
            services_section = self.extract_section(markdown_text, "Sections Needed")

        if services_section:
            # Extract bullet points or list items, but filter out generic section names
            lines = services_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    service = line[1:].strip()
                    # Filter out generic section names and keep actual services
                    generic_sections = ['hero section', 'services overview', 'about', 'testimonials',
                                      'contact', 'footer', 'hero', 'contact information', 'social proof']
                    if (service and len(service) > 3 and
                        not any(generic in service.lower() for generic in generic_sections)):
                        services.append(service)

        # If no specific services found, try to infer from project description and requirements
        if not services:
            project_desc = self.extract_section(markdown_text, "Project Description")
            requirements = self.extract_section(markdown_text, "Requirements")
            combined_text = f"{project_desc} {requirements}".lower()

            # Map keywords to services
            service_keywords = {
                'consultation': 'Professional Consultation',
                'consulting': 'Business Consulting',
                'repair': 'Repair Services',
                'maintenance': 'Maintenance Services',
                'installation': 'Installation Services',
                'design': 'Design Services',
                'development': 'Development Services',
                'marketing': 'Marketing Services',
                'seo': 'SEO Services',
                'web': 'Web Services',
                'support': 'Customer Support',
                'training': 'Training Services',
                'analysis': 'Analysis Services'
            }

            for keyword, service_name in service_keywords.items():
                if keyword in combined_text:
                    services.append(service_name)

            # If still no services, provide generic ones based on business type
            if not services:
                if 'saas' in combined_text or 'software' in combined_text:
                    services = ['Software Solutions', 'Technical Support', 'Implementation Services']
                elif 'local' in combined_text:
                    services = ['Professional Services', 'Local Support', 'Consultation']
                else:
                    services = ['Professional Services', 'Consultation', 'Support']

        return services[:3]  # Limit to 3 services for better layout

    def extract_location(self, markdown_text):
        """Extract location information from markdown"""
        # Look for location patterns with more comprehensive matching
        location_patterns = [
            r"serving\s+(?:the\s+)?([A-Z][a-z\s]+?)\s+(?:area|region|metro)(?:\s+in\s+([A-Z][a-z]+))?",
            r"(?:in|serving|located in|based in)\s+([A-Z][a-z\s]+?),\s*([A-Z][a-z]+)",
            r"([A-Z][a-z\s]+?),\s*([A-Z][A-Z])\s+(?:area|region|metro)",
            r"([A-Z][a-z]+)\s+(?:area|region|metro)",
            r"([A-Z][a-z]+),\s*([A-Z][a-z]+)",
        ]

        for pattern in location_patterns:
            match = re.search(pattern, markdown_text, re.IGNORECASE)
            if match:
                if match.lastindex >= 2:  # Has both city and state
                    city = match.group(1).strip()
                    state = match.group(2).strip()
                    return {
                        "city": city,
                        "state": state,
                        "region": f"{city} Area"
                    }
                else:  # Only has one location component
                    location = match.group(1).strip()
                    # Handle special cases
                    if "twin cities" in location.lower():
                        return {
                            "city": "Twin Cities",
                            "state": "Minnesota",
                            "region": "Twin Cities Metro"
                        }
                    else:
                        return {
                            "city": location,
                            "state": "State",
                            "region": f"{location} Area"
                        }

        # Default location
        return {
            "city": "Local Area",
            "state": "State",
            "region": "Regional"
        }

    def determine_project_type(self, markdown_text):
        """Determine project type from content"""
        text_lower = markdown_text.lower()

        if any(term in text_lower for term in ['saas', 'software', 'app', 'platform', 'subscription']):
            return "saas_landing_page"
        elif any(term in text_lower for term in ['ecommerce', 'shop', 'store', 'product', 'buy', 'sell']):
            return "ecommerce_page"
        elif any(term in text_lower for term in ['portfolio', 'showcase', 'work', 'projects', 'gallery']):
            return "portfolio_site"
        elif any(term in text_lower for term in ['corporate', 'enterprise', 'company', 'organization']):
            return "corporate_website"
        else:
            return "local_service_page"

    def parse_request_markdown(self, markdown_text):
        # Debug: check what we received
        print(f"🔍 parse_request_markdown called with:")
        print(f"   markdown_text: {type(markdown_text)} - {str(markdown_text)[:100]}...")

        required_sections = self.config.get("input_format", {}).get("required_sections", [])
        optional_sections = self.config.get("input_format", {}).get("optional_sections", [])

        # Extract dynamic content from the markdown
        business_name = self.extract_business_name(markdown_text)
        services = self.extract_services(markdown_text)
        location = self.extract_location(markdown_text)
        project_type = self.determine_project_type(markdown_text)

        print(f"🔍 Extracted dynamic content:")
        print(f"   Business Name: {business_name}")
        print(f"   Services: {services}")
        print(f"   Location: {location}")
        print(f"   Project Type: {project_type}")

        spec = {
            "template_id": "template_001",
            "project_type": project_type,
            "status": "parsed_from_request",
            "business_name": business_name,
            "services": services,
            "location": location,
            "responsive": True,
            "framework": "none",
            "audience": ["local_customers"],
            "sections": ["hero", "services", "about", "testimonials", "contact"],
            "layout_style": "single_page",
            "primary_cta": "Get Started" if project_type == "saas_landing_page" else "Contact Us",
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
