# agents/template_engineer/template_engineer.py
import json
from pathlib import Path

class TemplateEngineer:
    def __init__(self, config=None):
        self.config = config or {}

    def load_json(self, path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"❌ Failed to load {path}: {e}")
            return None

    def load_business_info_from_spec(self):
        """Load business info from the template spec file"""
        try:
            # Try to find the most recent template spec file
            import glob
            import json
            from pathlib import Path

            # Look for spec files in template_generations
            spec_files = glob.glob("template_generations/template_*/specs/template_spec.json")
            if spec_files:
                # Get the most recent one
                latest_spec = max(spec_files, key=lambda x: Path(x).stat().st_mtime)
                with open(latest_spec, 'r') as f:
                    spec_data = json.load(f)
                    return spec_data.get("business_info", {})
        except Exception as e:
            print(f"⚠️ Could not load business info from spec: {e}")

        return {}

    def get_dynamic_services(self) -> dict:
        """Get dynamic services based on business context"""
        # Try to load business info from spec file
        business_info = self.load_business_info_from_spec()
        business_type = business_info.get("business_type", "Service Business")

        # First try to get services from the spec file
        services_list = business_info.get("services", [])
        if services_list:
            services_dict = {}
            for service_name in services_list:
                services_dict[service_name] = self.generate_service_description(service_name)
            return services_dict

        # Generate services based on business type
        if any(keyword in business_type.lower() for keyword in ['landscaping', 'landscape', 'lawn', 'garden']):
            return {
                'Landscape Design': 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                'Hardscaping & Patios': 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                'Lawn Maintenance': 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
            }
        elif any(keyword in business_type.lower() for keyword in ['repair', 'pc', 'computer', 'tech']):
            return {
                'Computer Diagnostics': 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                'Hardware Repair': 'Professional hardware repair services for all types of computer components and peripherals.',
                'Software Solutions': 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
            }
        elif any(keyword in business_type.lower() for keyword in ['landscaping', 'lawn', 'garden', 'outdoor']):
            return {
                'Landscape Design': 'Custom landscape design services to transform your outdoor space into a beautiful environment.',
                'Lawn Maintenance': 'Regular lawn care and maintenance services to keep your property looking pristine year-round.',
                'Garden Installation': 'Professional garden installation and planting services for residential and commercial properties.'
            }
        elif any(keyword in business_type.lower() for keyword in ['restaurant', 'food', 'dining', 'catering']):
            return {
                'Catering Services': 'Professional catering for events and special occasions with customizable menu options.',
                'Private Dining': 'Intimate private dining experiences perfect for celebrations and business gatherings.',
                'Takeout & Delivery': 'Convenient takeout and delivery services bringing quality cuisine directly to you.'
            }
        elif any(keyword in business_type.lower() for keyword in ['saas', 'software', 'app', 'platform']):
            return {
                'Platform Integration': 'Seamless integration services to connect your existing systems with our platform.',
                'Custom Development': 'Tailored development solutions to meet your specific business requirements.',
                'Technical Support': '24/7 technical support to ensure your operations run smoothly and efficiently.'
            }
        else:
            # Generic business services
            clean_business_type = business_type.replace('Business', '').strip()
            if not clean_business_type:
                clean_business_type = 'Professional'

            return {
                f'{clean_business_type} Consultation': f'Expert {clean_business_type.lower()} consultation services tailored to your specific needs.',
                'Custom Solutions': 'Personalized solutions designed to address your unique business challenges and goals.',
                'Professional Support': 'Reliable ongoing support to ensure continued success and customer satisfaction.'
            }

    def load_custom_colors_from_spec(self):
        """Load custom color palette from the template spec file"""
        try:
            # Try to find the most recent template spec file
            import glob
            import json
            from pathlib import Path

            # Look for spec files in template_generations
            spec_files = glob.glob("template_generations/template_*/specs/template_spec.json")
            if spec_files:
                # Get the most recent one
                latest_spec = max(spec_files, key=lambda x: Path(x).stat().st_mtime)
                with open(latest_spec, 'r') as f:
                    spec_data = json.load(f)
                    return spec_data.get("color_palette", {})
        except Exception as e:
            print(f"⚠️ Could not load custom colors from spec: {e}")

        return {}

    def generate_service_description(self, service_name: str) -> str:
        """Generate appropriate description for a service based on its name"""
        service_lower = service_name.lower()

        if 'landscape' in service_lower or 'design' in service_lower:
            return "Professional landscape design services to transform your outdoor space into a beautiful and functional environment."
        elif 'hardscape' in service_lower or 'patio' in service_lower:
            return "Expert hardscaping and patio installation to create stunning outdoor living areas for your home."
        elif 'lawn' in service_lower or 'maintenance' in service_lower:
            return "Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round."
        elif 'tree' in service_lower or 'plant' in service_lower:
            return "Professional tree and plant care services including pruning, planting, and health assessments."
        elif 'irrigation' in service_lower or 'water' in service_lower:
            return "Expert irrigation system installation and maintenance for efficient landscape watering."
        elif 'computer' in service_lower or 'diagnostic' in service_lower:
            return "Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently."
        elif 'hardware' in service_lower or 'repair' in service_lower:
            return "Professional hardware repair services for all types of computer components and peripherals."
        elif 'software' in service_lower or 'solution' in service_lower:
            return "Expert software installation, configuration, and troubleshooting for optimal system performance."
        else:
            return "Professional service tailored to meet your specific needs with quality results and customer satisfaction."

    def generate_php_template(self, prompt_data, design_data):
        """Generate dramatically different templates based on design variation"""
        system_context = prompt_data.get("system_prompt", "")
        user_request = prompt_data.get("user_prompt", "")

        # Extract business context for industry-specific design
        # Try to get business info from prompt data first, then from spec file
        business_info = prompt_data.get("business_info", {})
        if not business_info:
            # Load business info from spec file
            business_info = self.load_business_info_from_spec()

        business_type = business_info.get("business_type", "Service Business")
        business_name = business_info.get("business_name", "Your Business")

        # Extract design variation details
        color_strategy = design_data.get("color_palette_strategy", "monochromatic")
        layout_structure = design_data.get("layout_structure", {})
        typography_scheme = design_data.get("typography_scheme", {})
        component_styles = design_data.get("component_styles", {})
        unique_elements = design_data.get("unique_elements", [])

        # Get specific design elements
        hero_style = layout_structure.get("hero", {}).get("name", "classic_centered")
        typography_pairing = typography_scheme.get("pairing", {}).get("name", "elegant_contrast")
        button_style = component_styles.get("button", {}).get("name", "rounded_modern")

        print(f"🎨 Generating template with:")
        print(f"   Business Type: {business_type}")
        print(f"   Color Strategy: {color_strategy}")
        print(f"   Hero Style: {hero_style}")
        print(f"   Typography: {typography_pairing}")
        print(f"   Button Style: {button_style}")

        # Generate dramatically different CSS based on design variation and business context
        css = self.generate_variation_css(color_strategy, hero_style, typography_pairing, button_style, unique_elements, business_type)

        # Generate completely different HTML structure based on layout
        html_content = self.generate_variation_html(hero_style, layout_structure, component_styles)

        # Get fonts for this typography pairing
        fonts = self.get_typography_fonts(typography_pairing)

        return f"""<?php
// AI-Generated Template with Dramatic Design Variation
// Color Strategy: {color_strategy}
// Hero Style: {hero_style}
// Typography: {typography_pairing}
// Button Style: {button_style}
// Unique Elements: {', '.join(unique_elements)}
?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Professional service page with unique design variation">
    <title>Professional Service Page - {hero_style.replace('_', ' ').title()}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{fonts['google_fonts_url']}" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body class="{color_strategy.replace('_', '-')} {hero_style.replace('_', '-')} {typography_pairing.replace('_', '-')}">
{html_content}
</body>
</html>
"""

    def get_typography_fonts(self, typography_pairing):
        """Get Google Fonts for different typography pairings"""
        font_combinations = {
            "elegant_contrast": {
                "heading": "Playfair Display",
                "body": "Source Sans Pro",
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+Pro:wght@400;500&display=swap"
            },
            "bold_statement": {
                "heading": "Montserrat",
                "body": "Lato",
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Lato:wght@400;500&display=swap"
            },
            "modern_minimal": {
                "heading": "Inter",
                "body": "Inter",
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
            },
            "creative_display": {
                "heading": "Oswald",
                "body": "Open Sans",
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Open+Sans:wght@400;500&display=swap"
            },
            "classic_serif": {
                "heading": "Merriweather",
                "body": "Lato",
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Lato:wght@400;500&display=swap"
            }
        }
        return font_combinations.get(typography_pairing, font_combinations["elegant_contrast"])

    def get_business_colors(self, business_type, color_strategy, custom_colors=None):
        """Get business-appropriate colors based on industry and color strategy"""

        # If custom colors are provided, use them first
        if custom_colors and custom_colors.get("has_custom_palette"):
            print(f"🎨 Using CUSTOM colors from specification")
            mapped_colors = custom_colors.get("mapped_colors", {})
            specified_colors = custom_colors.get("specified_colors", [])

            # Build color scheme from custom colors with intelligent fallbacks
            custom_color_scheme = {}

            # Use mapped colors if available
            if mapped_colors:
                custom_color_scheme = {
                    "primary": mapped_colors.get("primary"),
                    "secondary": mapped_colors.get("secondary"),
                    "accent": mapped_colors.get("accent"),
                    "bg": mapped_colors.get("background"),
                    "text": mapped_colors.get("text"),
                    "light": mapped_colors.get("background")
                }

            # If we have specific colors, assign them intelligently based on their descriptions
            if specified_colors:
                for color in specified_colors:
                    desc_lower = color["description"].lower()

                    # Assign based on description keywords
                    if any(keyword in desc_lower for keyword in ["button", "accent", "callout"]) and not custom_color_scheme.get("primary"):
                        custom_color_scheme["primary"] = color["hex"]
                    elif any(keyword in desc_lower for keyword in ["highlight", "icon", "hover"]) and not custom_color_scheme.get("secondary"):
                        custom_color_scheme["secondary"] = color["hex"]
                    elif any(keyword in desc_lower for keyword in ["background", "main background"]) and not custom_color_scheme.get("bg"):
                        custom_color_scheme["bg"] = color["hex"]
                        custom_color_scheme["light"] = color["hex"]
                    elif any(keyword in desc_lower for keyword in ["text", "header", "important text"]) and not custom_color_scheme.get("text"):
                        custom_color_scheme["text"] = color["hex"]
                    elif any(keyword in desc_lower for keyword in ["footer", "secondary element"]) and not custom_color_scheme.get("accent"):
                        custom_color_scheme["accent"] = color["hex"]

            # Fill in any missing colors with defaults from the Northern Roots palette
            custom_color_scheme["primary"] = custom_color_scheme.get("primary") or "#3B6A4D"  # Evergreen
            custom_color_scheme["secondary"] = custom_color_scheme.get("secondary") or "#A7D3F3"  # Sky Blue
            custom_color_scheme["accent"] = custom_color_scheme.get("accent") or "#A68C6D"  # Earth Brown
            custom_color_scheme["bg"] = custom_color_scheme.get("bg") or "#F5F3EB"  # Warm Beige
            custom_color_scheme["text"] = custom_color_scheme.get("text") or "#333333"  # Charcoal Gray
            custom_color_scheme["light"] = custom_color_scheme.get("light") or custom_color_scheme["bg"]

            print(f"   🎨 Custom Primary: {custom_color_scheme['primary']}")
            print(f"   🎨 Custom Secondary: {custom_color_scheme['secondary']}")
            print(f"   🎨 Custom Background: {custom_color_scheme['bg']}")
            print(f"   🎨 Custom Text: {custom_color_scheme['text']}")
            print(f"   🎨 Custom Accent: {custom_color_scheme['accent']}")

            return custom_color_scheme

        # Business-specific color palettes (fallback)
        business_color_palettes = {
            "landscaping": {
                "primary": "#22c55e", "secondary": "#16a34a", "accent": "#84cc16",
                "bg": "#ffffff", "text": "#1f2937", "light": "#f0fdf4"
            },
            "pc repair": {
                "primary": "#3b82f6", "secondary": "#1d4ed8", "accent": "#06b6d4",
                "bg": "#ffffff", "text": "#1f2937", "light": "#eff6ff"
            },
            "restaurant": {
                "primary": "#dc2626", "secondary": "#b91c1c", "accent": "#f59e0b",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fef2f2"
            },
            "real estate": {
                "primary": "#1e40af", "secondary": "#1e3a8a", "accent": "#d97706",
                "bg": "#ffffff", "text": "#1f2937", "light": "#eff6ff"
            },
            "construction": {
                "primary": "#ea580c", "secondary": "#c2410c", "accent": "#eab308",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fff7ed"
            },
            "automotive": {
                "primary": "#dc2626", "secondary": "#991b1b", "accent": "#6b7280",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fef2f2"
            },
            "beauty & wellness": {
                "primary": "#ec4899", "secondary": "#db2777", "accent": "#a855f7",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fdf2f8"
            },
            "photography": {
                "primary": "#7c3aed", "secondary": "#6d28d9", "accent": "#06b6d4",
                "bg": "#ffffff", "text": "#1f2937", "light": "#f5f3ff"
            },
            "marketing": {
                "primary": "#f59e0b", "secondary": "#d97706", "accent": "#dc2626",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fffbeb"
            },
            "financial services": {
                "primary": "#1e40af", "secondary": "#1e3a8a", "accent": "#059669",
                "bg": "#ffffff", "text": "#1f2937", "light": "#eff6ff"
            },
            "education": {
                "primary": "#2563eb", "secondary": "#1d4ed8", "accent": "#16a34a",
                "bg": "#ffffff", "text": "#1f2937", "light": "#eff6ff"
            },
            "travel & hospitality": {
                "primary": "#0891b2", "secondary": "#0e7490", "accent": "#f59e0b",
                "bg": "#ffffff", "text": "#1f2937", "light": "#ecfeff"
            },
            "pet services": {
                "primary": "#16a34a", "secondary": "#15803d", "accent": "#f59e0b",
                "bg": "#ffffff", "text": "#1f2937", "light": "#f0fdf4"
            },
            "fitness": {
                "primary": "#dc2626", "secondary": "#b91c1c", "accent": "#ea580c",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fef2f2"
            },
            "cleaning services": {
                "primary": "#0891b2", "secondary": "#0e7490", "accent": "#22c55e",
                "bg": "#ffffff", "text": "#1f2937", "light": "#ecfeff"
            },
            "consulting": {
                "primary": "#1e40af", "secondary": "#1e3a8a", "accent": "#7c3aed",
                "bg": "#ffffff", "text": "#1f2937", "light": "#eff6ff"
            },
            "legal services": {
                "primary": "#1f2937", "secondary": "#374151", "accent": "#1e40af",
                "bg": "#ffffff", "text": "#1f2937", "light": "#f9fafb"
            }
        }

        # Get business-specific colors or fallback to default
        business_colors = business_color_palettes.get(business_type.lower())

        if business_colors:
            print(f"🎨 Using BUSINESS-SPECIFIC colors for {business_type}")
        else:
            print(f"⚠️ No specific colors found for '{business_type}', using DEFAULT color scheme")
            business_colors = {
                "primary": "#2563eb", "secondary": "#1d4ed8", "accent": "#f59e0b",
                "bg": "#ffffff", "text": "#1f2937", "light": "#eff6ff"
            }

        return business_colors

    def generate_variation_css(self, color_strategy, hero_style, typography_pairing, button_style, unique_elements, business_type="Service Business"):
        """Generate dramatically different CSS based on design variation and business context"""
        fonts = self.get_typography_fonts(typography_pairing)

        # Get business-appropriate colors (prioritize custom colors if available)
        custom_colors = self.load_custom_colors_from_spec()
        colors = self.get_business_colors(business_type, color_strategy, custom_colors)

        # Base CSS with dramatic variations
        base_css = f"""        /* Reset and Typography Variation: {typography_pairing} */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: '{fonts["body"]}', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: {colors["text"]};
            background-color: {colors["bg"]};
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: '{fonts["heading"]}', serif;
            font-weight: 600;
            line-height: 1.2;
            margin-bottom: 1rem;
        }}"""

        # Add hero-specific styles
        hero_css = self.get_hero_css(hero_style, colors, fonts)

        # Add button-specific styles
        button_css = self.get_button_css(button_style, colors)

        # Add unique element styles
        unique_css = self.get_unique_element_css(unique_elements, colors)

        return base_css + hero_css + button_css + unique_css

    def get_hero_css(self, hero_style, colors, fonts):
        """Generate dramatically different hero styles"""
        if hero_style == "classic_centered":
            return f"""

        /* Classic Centered Hero */
        .hero {{
            background: linear-gradient(135deg, {colors["light"]} 0%, #e2e8f0 100%);
            padding: 6rem 0;
            text-align: center;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            color: {colors["text"]};
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: #64748b;
            max-width: 600px;
            margin: 0 auto 2rem;
        }}"""

        elif hero_style == "minimal_focus":
            return f"""

        /* Minimal Focus Hero */
        .hero {{
            background: {colors["bg"]};
            padding: 8rem 0 4rem;
            text-align: left;
            border-bottom: 3px solid {colors["primary"]};
        }}

        .hero h1 {{
            font-size: 4rem;
            color: {colors["primary"]};
            margin-bottom: 2rem;
            font-weight: 300;
            letter-spacing: -0.02em;
        }}

        .hero p {{
            font-size: 1.5rem;
            color: {colors["text"]};
            max-width: 500px;
            margin-bottom: 3rem;
            font-weight: 300;
        }}"""

        elif hero_style == "split_layout" or hero_style == "split_screen":
            return f"""

        /* Split Layout Hero */
        .hero {{
            background: linear-gradient(45deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
        }}

        .hero-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }}

        .hero h1 {{
            font-size: 3rem;
            color: white;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }}

        .hero p {{
            font-size: 1.125rem;
            color: rgba(255,255,255,0.9);
            margin-bottom: 2rem;
        }}"""

        elif hero_style == "geometric_shapes":
            return f"""

        /* Geometric Shapes Hero */
        .hero {{
            background: {colors["bg"]};
            padding: 8rem 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background:
                polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%),
                linear-gradient(45deg, {colors["primary"]}22 0%, {colors["secondary"]}22 100%);
            animation: rotate 20s linear infinite;
            z-index: 1;
        }}

        .hero .container {{
            position: relative;
            z-index: 2;
        }}

        .hero h1 {{
            font-size: 4rem;
            color: {colors["text"]};
            margin-bottom: 2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}"""

        elif hero_style == "floating_elements":
            return f"""

        /* Floating Elements Hero */
        .hero {{
            background: linear-gradient(135deg, {colors["bg"]} 0%, {colors["light"]} 100%);
            padding: 10rem 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 20%;
            left: 10%;
            width: 100px;
            height: 100px;
            background: {colors["primary"]};
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
            opacity: 0.3;
        }}

        .hero::after {{
            content: '';
            position: absolute;
            top: 60%;
            right: 15%;
            width: 150px;
            height: 150px;
            background: {colors["secondary"]};
            clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            animation: float 8s ease-in-out infinite reverse;
            opacity: 0.2;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            color: {colors["text"]};
            margin-bottom: 2rem;
            font-weight: 400;
            position: relative;
            z-index: 2;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}"""

        elif hero_style == "diagonal_split":
            return f"""

        /* Diagonal Split Hero */
        .hero {{
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["primary"]} 60%, {colors["bg"]} 60%, {colors["bg"]} 100%);
            padding: 8rem 0;
            position: relative;
        }}

        .hero-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }}

        .hero-text {{
            color: white;
            z-index: 2;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            color: white;
            margin-bottom: 2rem;
            font-weight: 700;
            line-height: 1.1;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: rgba(255,255,255,0.9);
            margin-bottom: 2rem;
        }}"""

        elif hero_style == "full_height_sidebar":
            return f"""

        /* Full Height Sidebar Hero */
        .hero {{
            background: {colors["bg"]};
            min-height: 100vh;
            display: flex;
            align-items: stretch;
            padding: 0;
        }}

        .hero-sidebar {{
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
            width: 40%;
            padding: 4rem 3rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: white;
        }}

        .hero-content {{
            width: 60%;
            padding: 4rem 3rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .hero h1 {{
            font-size: 3rem;
            color: white;
            margin-bottom: 2rem;
            font-weight: 700;
        }}

        .hero p {{
            font-size: 1.125rem;
            color: rgba(255,255,255,0.9);
            margin-bottom: 2rem;
        }}"""

        elif hero_style == "card_stack":
            return f"""

        /* Card Stack Hero */
        .hero {{
            background: linear-gradient(135deg, {colors["light"]} 0%, {colors["bg"]} 100%);
            padding: 8rem 0;
            text-align: center;
            position: relative;
        }}

        .hero-cards {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 3rem;
        }}

        .hero-card {{
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transform: rotate(-2deg);
            max-width: 300px;
        }}

        .hero-card:nth-child(2) {{
            transform: rotate(1deg) translateY(-1rem);
            z-index: 2;
        }}

        .hero-card:nth-child(3) {{
            transform: rotate(-1deg) translateY(0.5rem);
        }}

        .hero h1 {{
            font-size: 3.5rem;
            color: {colors["text"]};
            margin-bottom: 2rem;
            font-weight: 700;
        }}"""

        elif hero_style == "magazine_style":
            return f"""

        /* Magazine Style Hero */
        .hero {{
            background: {colors["bg"]};
            padding: 4rem 0;
            position: relative;
        }}

        .hero-layout {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 3rem;
            align-items: start;
        }}

        .hero-main {{
            border-left: 4px solid {colors["primary"]};
            padding-left: 2rem;
        }}

        .hero-sidebar {{
            background: {colors["light"]};
            padding: 2rem;
            border-radius: 8px;
        }}

        .hero h1 {{
            font-size: 4rem;
            color: {colors["text"]};
            margin-bottom: 1rem;
            font-weight: 900;
            line-height: 0.9;
        }}

        .hero .subtitle {{
            font-size: 1.5rem;
            color: {colors["primary"]};
            margin-bottom: 2rem;
            font-weight: 600;
        }}"""

        else:  # default
            return f"""

        /* Default Hero */
        .hero {{
            background: {colors["primary"]};
            color: white;
            padding: 4rem 0;
            text-align: center;
        }}

        .hero h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}"""

    def get_button_css(self, button_style, colors):
        """Generate different button styles"""
        if button_style == "rounded_modern":
            return f"""

        /* Rounded Modern Buttons */
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.125rem;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, {colors["secondary"]} 0%, {colors["accent"]} 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        }}"""

        elif button_style == "sharp_edges" or button_style == "sharp_corporate":
            return f"""

        /* Sharp Edge Buttons */
        .btn {{
            display: inline-block;
            padding: 1.25rem 3rem;
            border-radius: 0;
            text-decoration: none;
            font-weight: 700;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            transition: all 0.2s ease;
            border: 3px solid {colors["primary"]};
            cursor: pointer;
        }}

        .btn-primary {{
            background: {colors["primary"]};
            color: white;
        }}

        .btn-primary:hover {{
            background: transparent;
            color: {colors["primary"]};
        }}"""

        elif button_style == "geometric_bold":
            return f"""

        /* Geometric Bold Buttons */
        .btn {{
            display: inline-block;
            padding: 1.25rem 3rem;
            border-radius: 0;
            text-decoration: none;
            font-weight: 900;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            transition: all 0.2s ease;
            border: none;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}

        .btn-primary {{
            background: {colors["primary"]};
            color: white;
            box-shadow: 4px 4px 0px rgba(0,0,0,0.2);
        }}

        .btn-primary:hover {{
            transform: translate(-2px, -2px);
            box-shadow: 6px 6px 0px rgba(0,0,0,0.3);
        }}"""

        elif button_style == "organic_blob":
            return f"""

        /* Organic Blob Buttons */
        .btn {{
            display: inline-block;
            padding: 1rem 2.5rem;
            border-radius: 30px 10px 25px 15px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.125rem;
            transition: all 0.4s ease;
            border: none;
            cursor: pointer;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
            color: white;
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }}

        .btn-primary:hover {{
            border-radius: 15px 25px 10px 30px;
            transform: scale(1.05);
        }}"""

        elif button_style == "neon_glow":
            return f"""

        /* Neon Glow Buttons */
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            border: 2px solid {colors["primary"]};
            cursor: pointer;
            background: transparent;
        }}

        .btn-primary {{
            color: {colors["primary"]};
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
        }}

        .btn-primary:hover {{
            background: {colors["primary"]};
            color: white;
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.8);
        }}"""

        else:  # default
            return f"""

        /* Default Buttons */
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }}

        .btn-primary {{
            background: {colors["primary"]};
            color: white;
        }}"""

    def get_unique_element_css(self, unique_elements, colors):
        """Add unique visual elements"""
        css = ""

        for element in unique_elements:
            if element == "geometric_shapes":
                css += f"""

        /* Geometric Shapes */
        .hero::before {{
            content: '';
            position: absolute;
            top: 20%;
            right: 10%;
            width: 200px;
            height: 200px;
            background: linear-gradient(45deg, {colors["secondary"]}, {colors["accent"]});
            border-radius: 50%;
            opacity: 0.1;
            z-index: 1;
        }}"""

            elif element == "diagonal_sections":
                css += f"""

        /* Diagonal Sections */
        .services {{
            position: relative;
            transform: skewY(-2deg);
            margin: 4rem 0;
        }}

        .services .container {{
            transform: skewY(2deg);
        }}"""

        return css

    def generate_variation_html(self, hero_style, layout_structure, component_styles):
        """Generate completely different HTML structures"""

        if hero_style == "split_layout" or hero_style == "split_screen":
            return self.generate_split_layout_html()
        elif hero_style == "minimal_focus":
            return self.generate_minimal_focus_html()
        elif hero_style == "overlay_hero":
            return self.generate_overlay_hero_html()
        elif hero_style == "geometric_shapes":
            return self.generate_geometric_shapes_html()
        elif hero_style == "floating_elements":
            return self.generate_floating_elements_html()
        elif hero_style == "diagonal_split":
            return self.generate_diagonal_split_html()
        elif hero_style == "full_height_sidebar":
            return self.generate_full_height_sidebar_html()
        elif hero_style == "card_stack":
            return self.generate_card_stack_html()
        elif hero_style == "magazine_style":
            return self.generate_magazine_style_html()
        else:
            return self.generate_classic_centered_html()

    def generate_split_layout_html(self):
        """Split layout with image/content side by side"""
        return """    <!-- Split Layout Hero -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1>Transform Your Business Today</h1>
                    <p>Experience the difference with our innovative approach to service delivery. We combine expertise with cutting-edge solutions.</p>
                    <a href="#contact" class="btn btn-primary">Start Your Journey</a>
                </div>
                <div class="hero-visual">
                    <div style="background: rgba(255,255,255,0.2); height: 400px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">
                        Visual Element
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Grid -->
    <section class="services" style="padding: 6rem 0; background: white;">
        <div class="container">
            <h2 style="text-align: center; margin-bottom: 3rem; font-size: 2.5rem;">Our Expertise</h2>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
                <?php
                $services = get_option('business_services', array());
                if (empty($services)) {
                    // Dynamic fallback based on business type
                    $business_type = get_option('business_type', 'Service Business');
                    if (stripos($business_type, 'landscaping') !== false || stripos($business_type, 'landscape') !== false) {
                        $services = array(
                            'Landscape Design' => 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                            'Hardscaping & Patios' => 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                            'Lawn Maintenance' => 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
                        );
                    } elseif (stripos($business_type, 'repair') !== false || stripos($business_type, 'pc') !== false) {
                        $services = array(
                            'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                            'Hardware Repair' => 'Professional hardware repair services for all types of computer components and peripherals.',
                            'Software Solutions' => 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
                        );
                    } else {
                        $services = array(
                            'Professional Consultation' => 'Expert consultation services tailored to your specific needs and requirements.',
                            'Custom Solutions' => 'Personalized solutions designed to address your unique challenges and goals.',
                            'Professional Support' => 'Reliable ongoing support to ensure continued success and satisfaction.'
                        );
                    }
                }
                $colors = ['#2563eb', '#f59e0b', '#059669', '#8b5cf6', '#ef4444', '#06b6d4'];
                $i = 0;
                foreach ($services as $service_name => $service_desc):
                    $color = $colors[$i % count($colors)];
                ?>
                <div style="padding: 2rem; background: #f8fafc; border-left: 4px solid <?php echo $color; ?>;">
                    <h3 style="color: <?php echo $color; ?>; margin-bottom: 1rem;"><?php echo esc_html($service_name); ?></h3>
                    <p><?php echo esc_html($service_desc); ?></p>
                </div>
                <?php $i++; endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" style="background: #1f2937; color: white; padding: 4rem 0; text-align: center;">
        <div class="container">
            <h2 style="color: white; margin-bottom: 2rem;">Ready to Begin?</h2>
            <p style="margin-bottom: 2rem; font-size: 1.25rem;">Let's discuss how we can help transform your business.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@business.com" class="btn" style="background: transparent; border: 2px solid white; color: white;">Get Quote</a>
        </div>
    </section>"""

    def generate_minimal_focus_html(self):
        """Minimal, typography-focused layout"""
        return """    <!-- Minimal Header -->
    <header style="background: white; padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 700; font-size: 1.25rem;">BUSINESS</div>
                <div>
                    <a href="#services" style="color: #374151; text-decoration: none; margin-left: 2rem;">Services</a>
                    <a href="#contact" style="color: #374151; text-decoration: none; margin-left: 2rem;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Minimal Hero -->
    <section class="hero">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 1rem;">
            <h1>Excellence in Every Detail</h1>
            <p>We believe in the power of simplicity. Our approach focuses on what matters most—delivering exceptional results through thoughtful execution.</p>
            <a href="#contact" class="btn btn-primary">Discover More</a>
        </div>
    </section>

    <!-- Minimal Services -->
    <section id="services" style="padding: 6rem 0; background: #fafafa;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="margin-bottom: 3rem; font-size: 2rem;">What We Do</h2>

            <div style="space-y: 3rem;">
                <?php
                $services = get_option('business_services', array());
                if (empty($services)) {
                    // Dynamic fallback based on business type
                    $business_type = get_option('business_type', 'Service Business');
                    if (stripos($business_type, 'landscaping') !== false || stripos($business_type, 'landscape') !== false) {
                        $services = array(
                            'Landscape Design' => 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                            'Hardscaping & Patios' => 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                            'Lawn Maintenance' => 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
                        );
                    } elseif (stripos($business_type, 'repair') !== false || stripos($business_type, 'pc') !== false) {
                        $services = array(
                            'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                            'Hardware Repair' => 'Professional hardware repair services for all types of computer components and peripherals.',
                            'Software Solutions' => 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
                        );
                    } else {
                        $services = array(
                            'Professional Consultation' => 'Expert consultation services tailored to your specific needs and requirements.',
                            'Custom Solutions' => 'Personalized solutions designed to address your unique challenges and goals.',
                            'Professional Support' => 'Reliable ongoing support to ensure continued success and satisfaction.'
                        );
                    }
                }
                $i = 1;
                foreach ($services as $service_name => $service_desc):
                ?>
                <div style="margin-bottom: 3rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #2563eb;"><?php echo sprintf('%02d. %s', $i, esc_html($service_name)); ?></h3>
                    <p style="font-size: 1.125rem; line-height: 1.7; color: #4b5563;"><?php echo esc_html($service_desc); ?></p>
                </div>
                <?php $i++; endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Minimal Contact -->
    <section id="contact" style="padding: 6rem 0; background: white;">
        <div class="container" style="max-width: 600px; margin: 0 auto; padding: 0 1rem; text-align: center;">
            <h2 style="margin-bottom: 2rem;">Let's Talk</h2>
            <p style="margin-bottom: 3rem; font-size: 1.125rem; color: #6b7280;">Ready to start your project? We'd love to hear from you.</p>
            <a href="mailto:hello@business.com" class="btn btn-primary">Send Message</a>
        </div>
    </section>"""

    def generate_classic_centered_html(self):
        """Traditional centered layout"""
        return """    <!-- Classic Header -->
    <header style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">Your Business</div>
                <div>
                    <a href="#services" style="color: white; text-decoration: none; margin-left: 2rem;">Services</a>
                    <a href="#contact" style="color: white; text-decoration: none; margin-left: 2rem;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Classic Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h1>Professional Service Solutions</h1>
            <p>We provide exceptional service to help your business grow and succeed in today's competitive market.</p>
            <a href="#contact" class="btn btn-primary">Get Started Today</a>
        </div>
    </section>

    <!-- Classic Services -->
    <section id="services" style="padding: 4rem 0; background: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem;">Our Services</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 3rem;">Comprehensive solutions tailored to your needs</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 3rem;">
                <?php
                $services = get_option('business_services', array());
                if (empty($services)) {
                    // Dynamic fallback based on business type
                    $business_type = get_option('business_type', 'Service Business');
                    if (stripos($business_type, 'landscaping') !== false || stripos($business_type, 'landscape') !== false) {
                        $services = array(
                            'Landscape Design' => 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                            'Hardscaping & Patios' => 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                            'Lawn Maintenance' => 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
                        );
                    } elseif (stripos($business_type, 'repair') !== false || stripos($business_type, 'pc') !== false) {
                        $services = array(
                            'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                            'Hardware Repair' => 'Professional hardware repair services for all types of computer components and peripherals.',
                            'Software Solutions' => 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
                        );
                    } else {
                        $services = array(
                            'Professional Consultation' => 'Expert consultation services tailored to your specific needs and requirements.',
                            'Custom Solutions' => 'Personalized solutions designed to address your unique challenges and goals.',
                            'Professional Support' => 'Reliable ongoing support to ensure continued success and satisfaction.'
                        );
                    }
                }
                foreach ($services as $service_name => $service_desc):
                ?>
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 25px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; transition: transform 0.3s ease;">
                    <h3 style="color: #2563eb; margin-bottom: 1rem;"><?php echo esc_html($service_name); ?></h3>
                    <p><?php echo esc_html($service_desc); ?></p>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Classic Contact -->
    <section id="contact" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 4rem 0; text-align: center;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="color: white; margin-bottom: 1rem;">Ready to Get Started?</h2>
            <p style="margin-bottom: 2rem; opacity: 0.9;">Contact us today for a free consultation and discover how we can help your business succeed.</p>
            <a href="tel:555-555-5555" class="btn" style="background: white; color: #2563eb; margin-right: 1rem; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600;">Call (555) 555-5555</a>
            <a href="mailto:info@yourbusiness.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600;">Send Email</a>
        </div>
    </section>

    <!-- Footer -->
    <footer style="background: #1f2937; color: white; padding: 2rem 0; text-align: center;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <p>&copy; <?php echo date('Y'); ?> Your Business. All rights reserved.</p>
        </div>
    </footer>"""

    def generate_overlay_hero_html(self):
        """Full-screen background with overlay text"""
        return """    <!-- Overlay Hero -->
    <section class="hero" style="
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.4)),
                    url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1200 800\"><rect fill=\"%23667eea\" width=\"1200\" height=\"800\"/><polygon fill=\"%23764ba2\" points=\"0,800 1200,600 1200,800\"/></svg>');
        background-size: cover;
        background-position: center;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white;
        position: relative;
    ">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 1rem; z-index: 2;">
            <h1 style="font-size: 4rem; font-weight: 700; margin-bottom: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                Elevate Your Business
            </h1>
            <p style="font-size: 1.5rem; margin-bottom: 3rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); opacity: 0.95;">
                Transform your vision into reality with our comprehensive suite of professional services designed for modern businesses.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="#contact" class="btn btn-primary" style="
                    background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
                    color: white;
                    padding: 1.25rem 3rem;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 1.125rem;
                    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
                    transition: all 0.3s ease;
                ">Get Started Now</a>
                <a href="#services" class="btn" style="
                    background: rgba(255,255,255,0.2);
                    color: white;
                    border: 2px solid white;
                    padding: 1.25rem 3rem;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 1.125rem;
                    backdrop-filter: blur(10px);
                    transition: all 0.3s ease;
                ">Learn More</a>
            </div>
        </div>

        <!-- Floating elements -->
        <div style="position: absolute; top: 20%; left: 10%; width: 100px; height: 100px; background: rgba(255,255,255,0.1); border-radius: 50%; animation: float 6s ease-in-out infinite;"></div>
        <div style="position: absolute; bottom: 30%; right: 15%; width: 150px; height: 150px; background: rgba(245, 158, 11, 0.2); border-radius: 30%; animation: float 8s ease-in-out infinite reverse;"></div>
    </section>

    <!-- Services with Cards -->
    <section id="services" style="padding: 6rem 0; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem; font-size: 3rem; color: #1f2937;">Our Services</h2>
            <p style="text-align: center; color: #6b7280; margin-bottom: 4rem; font-size: 1.25rem;">Comprehensive solutions for every business need</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 3rem;">
                <div style="
                    background: white;
                    padding: 3rem 2rem;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                    text-align: center;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    border-top: 5px solid #667eea;
                ">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; margin: 0 auto 2rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold;">01</div>
                    <h3 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.5rem;">Strategic Planning</h3>
                    <p style="color: #6b7280; line-height: 1.6;">Comprehensive business analysis and strategic roadmap development for sustainable growth.</p>
                </div>

                <div style="
                    background: white;
                    padding: 3rem 2rem;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                    text-align: center;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    border-top: 5px solid #f59e0b;
                ">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #f59e0b, #ea580c); border-radius: 50%; margin: 0 auto 2rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold;">02</div>
                    <h3 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.5rem;">Implementation</h3>
                    <p style="color: #6b7280; line-height: 1.6;">Expert execution of strategies with precision, quality control, and measurable outcomes.</p>
                </div>

                <div style="
                    background: white;
                    padding: 3rem 2rem;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                    text-align: center;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    border-top: 5px solid #10b981;
                ">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; margin: 0 auto 2rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold;">03</div>
                    <h3 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.5rem;">Optimization</h3>
                    <p style="color: #6b7280; line-height: 1.6;">Continuous improvement and optimization to maximize efficiency and return on investment.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact with Gradient -->
    <section id="contact" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 6rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle fill=\"rgba(255,255,255,0.05)\" cx=\"50\" cy=\"50\" r=\"40\"/></svg>'); opacity: 0.1;"></div>

        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 1rem; position: relative; z-index: 2;">
            <h2 style="color: white; margin-bottom: 1rem; font-size: 3rem;">Ready to Transform?</h2>
            <p style="margin-bottom: 3rem; font-size: 1.25rem; opacity: 0.9;">Join hundreds of businesses that have already transformed their operations with our expertise.</p>

            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 3rem;">
                <a href="tel:555-555-5555" class="btn" style="
                    background: white;
                    color: #667eea;
                    padding: 1.25rem 3rem;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 1.125rem;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                ">Call (555) 555-5555</a>
                <a href="mailto:info@business.com" class="btn" style="
                    background: rgba(255,255,255,0.2);
                    color: white;
                    border: 2px solid white;
                    padding: 1.25rem 3rem;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 1.125rem;
                    backdrop-filter: blur(10px);
                    transition: all 0.3s ease;
                ">Send Email</a>
            </div>

            <p style="opacity: 0.8; font-size: 0.9rem;">Free consultation • No commitment • Quick response</p>
        </div>
    </section>

    <!-- Footer -->
    <footer style="background: #1f2937; color: white; padding: 3rem 0; text-align: center;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <p>&copy; <?php echo date('Y'); ?> Your Business. All rights reserved.</p>
        </div>
    </footer>

    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
    </style>"""

    def generate_modern_css(self, colors, typography, layout):
        """Generate modern, professional CSS"""
        typography_pairing = typography.get("pairing", {})
        heading_font = typography_pairing.get("heading", "Inter")
        body_font = typography_pairing.get("body", "Inter")

        # Generate color palette from design data
        primary_color = "#2563eb"  # Default blue
        accent_color = "#f59e0b"   # Default orange
        text_color = "#1f2937"     # Dark gray
        bg_color = "#ffffff"       # White

        return f"""        /* Reset and Base Styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: '{body_font}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: {text_color};
            background-color: {bg_color};
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: '{heading_font}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 600;
            line-height: 1.2;
            margin-bottom: 1rem;
        }}

        h1 {{ font-size: 3rem; font-weight: 700; }}
        h2 {{ font-size: 2.25rem; }}
        h3 {{ font-size: 1.875rem; }}
        p {{ margin-bottom: 1rem; font-size: 1.125rem; }}

        /* Layout */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, {primary_color} 0%, #1d4ed8 100%);
            color: white;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
        }}

        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 4rem 0;
            text-align: center;
        }}

        .hero h1 {{
            color: {text_color};
            margin-bottom: 1.5rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: #64748b;
            max-width: 600px;
            margin: 0 auto 2rem;
        }}

        /* Buttons */
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.125rem;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, {accent_color} 0%, #ea580c 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        }}

        /* Services Section */
        .services {{
            padding: 4rem 0;
            background: white;
        }}

        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }}

        .service-card {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e2e8f0;
        }}

        .service-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 35px rgba(0,0,0,0.12);
        }}

        .service-card h3 {{
            color: {primary_color};
            margin-bottom: 1rem;
        }}

        /* Contact Section */
        .contact {{
            background: linear-gradient(135deg, {primary_color} 0%, #1d4ed8 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }}

        .contact h2 {{
            color: white;
            margin-bottom: 1rem;
        }}

        .contact p {{
            margin-bottom: 2rem;
            opacity: 0.9;
        }}

        /* Footer */
        .footer {{
            background: #1f2937;
            color: white;
            padding: 2rem 0;
            text-align: center;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            h1 {{ font-size: 2.25rem; }}
            h2 {{ font-size: 1.875rem; }}
            .hero {{ padding: 2rem 0; }}
            .services {{ padding: 2rem 0; }}
            .contact {{ padding: 2rem 0; }}
            .services-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
        }}"""

    def generate_structured_html(self, hero_style, typography_pairing):
        """Generate structured, professional HTML content"""
        return """    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">Your Business</div>
                <div class="nav-links">
                    <a href="#services" style="color: white; text-decoration: none; margin-left: 2rem;">Services</a>
                    <a href="#contact" style="color: white; text-decoration: none; margin-left: 2rem;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>Professional Service Solutions</h1>
            <p>We provide exceptional service to help your business grow and succeed in today's competitive market.</p>
            <a href="#contact" class="btn btn-primary">Get Started Today</a>
        </div>
    </section>

    <!-- Services Section -->
    <section class="services" id="services">
        <div class="container">
            <h2 style="text-align: center; margin-bottom: 1rem;">Our Services</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 3rem;">Comprehensive solutions tailored to your needs</p>

            <div class="services-grid">
                <?php
                $services = get_option('business_services', array());
                if (empty($services)) {
                    // Dynamic fallback based on business type
                    $business_type = get_option('business_type', 'Service Business');
                    if (stripos($business_type, 'landscaping') !== false || stripos($business_type, 'landscape') !== false) {
                        $services = array(
                            'Landscape Design' => 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                            'Hardscaping & Patios' => 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                            'Lawn Maintenance' => 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
                        );
                    } elseif (stripos($business_type, 'repair') !== false || stripos($business_type, 'pc') !== false) {
                        $services = array(
                            'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                            'Hardware Repair' => 'Professional hardware repair services for all types of computer components and peripherals.',
                            'Software Solutions' => 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
                        );
                    } else {
                        $services = array(
                            'Professional Consultation' => 'Expert consultation services tailored to your specific needs and requirements.',
                            'Custom Solutions' => 'Personalized solutions designed to address your unique challenges and goals.',
                            'Professional Support' => 'Reliable ongoing support to ensure continued success and satisfaction.'
                        );
                    }
                }
                foreach ($services as $service_name => $service_desc):
                ?>
                <div class="service-card">
                    <h3><?php echo esc_html($service_name); ?></h3>
                    <p><?php echo esc_html($service_desc); ?></p>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="contact" id="contact">
        <div class="container">
            <h2>Ready to Get Started?</h2>
            <p>Contact us today for a free consultation and discover how we can help your business succeed.</p>
            <a href="tel:555-555-5555" class="btn" style="background: white; color: #2563eb; margin-right: 1rem;">Call (555) 555-5555</a>
            <a href="mailto:info@yourbusiness.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white;">Send Email</a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; <?php echo date('Y'); ?> Your Business. All rights reserved.</p>
        </div>
    </footer>"""

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
            # For template_engineer, input_file should be the prompt file
            prompt_path = Path(input_file)

            # Look for design variation file in the same template directory
            template_dir = prompt_path.parent.parent
            design_files = list(template_dir.glob("design_variations/design_variation_*.json"))

            if not design_files:
                return AgentResult(
                    agent_id="template_engineer",
                    success=False,
                    error_message="No design variation file found"
                )

            design_path = design_files[0]  # Use the first design variation

            # Generate output path
            template_id = pipeline_id.replace('pipeline_', '')
            output_path = template_dir / f"templates/template_{template_id}.php"

            # Load data
            prompt_data = self.load_json(prompt_path)
            design_data = self.load_json(design_path)

            if not prompt_data or not design_data:
                return AgentResult(
                    agent_id="template_engineer",
                    success=False,
                    error_message="Failed to load prompt or design data"
                )

            # Generate PHP template
            php_code = self.generate_php_template(prompt_data, design_data)

            # Write output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(php_code, encoding='utf-8')

            print(f"✅ PHP template written to {output_path}")

            return AgentResult(
                agent_id="template_engineer",
                success=True,
                output_file=str(output_path),
                metadata={"template_id": template_id}
            )

        except Exception as e:
            return AgentResult(
                agent_id="template_engineer",
                success=False,
                error_message=str(e)
            )

    def run_legacy(self, prompt_path, design_path, output_path) -> bool:
        """Legacy method for backward compatibility"""
        prompt_data = self.load_json(prompt_path)
        design_data = self.load_json(design_path)

        if not prompt_data or not design_data:
            return False

        php_code = self.generate_php_template(prompt_data, design_data)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(php_code)

        print(f"✅ PHP template written to {output_path}")
        return True

    def generate_geometric_shapes_html(self):
        """Geometric shapes hero with animated elements"""
        return """    <!-- Geometric Shapes Header -->
    <header style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 1rem 0; position: relative; z-index: 10;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">GEOMETRIC</div>
                <div>
                    <a href="#services" style="color: white; text-decoration: none; margin-left: 2rem; text-transform: uppercase; letter-spacing: 0.1em;">Services</a>
                    <a href="#contact" style="color: white; text-decoration: none; margin-left: 2rem; text-transform: uppercase; letter-spacing: 0.1em;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Geometric Shapes Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h1>BOLD DESIGN SOLUTIONS</h1>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; max-width: 600px; margin-left: auto; margin-right: auto;">Experience the power of geometric precision combined with innovative thinking.</p>
            <a href="#contact" class="btn btn-primary">START PROJECT</a>
        </div>
    </section>

    <!-- Angular Services -->
    <section id="services" style="padding: 6rem 0; background: white; position: relative;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem; font-size: 3rem; text-transform: uppercase; letter-spacing: 0.1em;">SERVICES</h2>
            <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #3b82f6, #8b5cf6); margin: 0 auto 4rem;"></div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 3rem;">
                <div style="background: #f8fafc; padding: 3rem 2rem; position: relative; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-size: 1.5rem; text-transform: uppercase;">STRATEGY</h3>
                    <p style="color: #64748b;">Bold strategic planning with geometric precision and innovative approaches.</p>
                </div>
                <div style="background: #f1f5f9; padding: 3rem 2rem; position: relative; clip-path: polygon(5% 0, 100% 0, 95% 100%, 0% 100%);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-size: 1.5rem; text-transform: uppercase;">DESIGN</h3>
                    <p style="color: #64748b;">Cutting-edge design solutions that break conventional boundaries.</p>
                </div>
                <div style="background: #f8fafc; padding: 3rem 2rem; position: relative; clip-path: polygon(0 0, 95% 0, 100% 100%, 5% 100%);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-size: 1.5rem; text-transform: uppercase;">EXECUTION</h3>
                    <p style="color: #64748b;">Flawless implementation with attention to every geometric detail.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="padding: 6rem 0; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; text-align: center;">
            <h2 style="margin-bottom: 1rem; font-size: 3rem; text-transform: uppercase; letter-spacing: 0.1em;">CONNECT</h2>
            <p style="margin-bottom: 3rem; font-size: 1.25rem;">Ready to create something extraordinary?</p>
            <a href="mailto:contact@example.com" class="btn btn-primary">CONTACT US</a>
        </div>
    </section>"""

    def generate_floating_elements_html(self):
        """Floating elements hero with organic feel"""
        return """    <!-- Floating Elements Header -->
    <header style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); color: #1e293b; padding: 1rem 0; position: fixed; top: 0; width: 100%; z-index: 100; box-shadow: 0 2px 20px rgba(0,0,0,0.1);">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 1.5rem; font-weight: 400; font-style: italic;">Floating</div>
                <div>
                    <a href="#services" style="color: #1e293b; text-decoration: none; margin-left: 2rem; font-weight: 300;">Services</a>
                    <a href="#contact" style="color: #1e293b; text-decoration: none; margin-left: 2rem; font-weight: 300;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Floating Elements Hero -->
    <section class="hero" style="margin-top: 80px;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h1>Creative Solutions That Float Above The Rest</h1>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; max-width: 600px; margin-left: auto; margin-right: auto; font-weight: 300;">Discover the beauty of organic design combined with modern functionality.</p>
            <a href="#contact" class="btn btn-primary">Explore Possibilities</a>
        </div>
    </section>

    <!-- Organic Services -->
    <section id="services" style="padding: 6rem 0; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem; font-size: 2.5rem; font-weight: 400;">Our Services</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 4rem; font-size: 1.125rem;">Flowing solutions that adapt to your needs</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: rotate(-1deg);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-weight: 500;">Creative Consulting</h3>
                    <p style="color: #64748b; line-height: 1.7;">Innovative approaches that flow naturally from your vision to reality.</p>
                </div>
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: rotate(1deg);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-weight: 500;">Organic Design</h3>
                    <p style="color: #64748b; line-height: 1.7;">Designs that breathe and adapt, creating harmonious user experiences.</p>
                </div>
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: rotate(-0.5deg);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-weight: 500;">Fluid Implementation</h3>
                    <p style="color: #64748b; line-height: 1.7;">Seamless execution that flows smoothly from concept to completion.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="padding: 6rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; text-align: center;">
            <h2 style="margin-bottom: 1rem; font-size: 2.5rem; font-weight: 400;">Let's Create Together</h2>
            <p style="margin-bottom: 3rem; font-size: 1.125rem; opacity: 0.9;">Ready to bring your vision to life?</p>
            <a href="mailto:contact@example.com" class="btn btn-primary">Get In Touch</a>
        </div>
    </section>"""

    def generate_diagonal_split_html(self):
        """Diagonal split layout with dynamic composition"""
        return """    <!-- Diagonal Split Header -->
    <header style="background: #1e293b; color: white; padding: 1rem 0; position: relative; z-index: 10;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">DIAGONAL</div>
                <div>
                    <a href="#services" style="color: white; text-decoration: none; margin-left: 2rem;">Services</a>
                    <a href="#contact" style="color: white; text-decoration: none; margin-left: 2rem;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Diagonal Split Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div class="hero-content">
                <div class="hero-text">
                    <h1>Dynamic Solutions</h1>
                    <p>Breaking conventional boundaries with innovative diagonal thinking and creative problem-solving approaches.</p>
                    <a href="#contact" class="btn btn-primary">Explore Solutions</a>
                </div>
                <div style="display: flex; align-items: center; justify-content: center;">
                    <div style="width: 300px; height: 300px; background: rgba(255,255,255,0.1); transform: rotate(45deg); border: 3px solid rgba(255,255,255,0.3);"></div>
                </div>
            </div>
        </div>
    </section>

    <!-- Dynamic Services -->
    <section id="services" style="padding: 6rem 0; background: white; position: relative;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, transparent 0%, transparent 45%, #f8fafc 45%, #f8fafc 55%, transparent 55%, transparent 100%); z-index: 1;"></div>
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; position: relative; z-index: 2;">
            <h2 style="text-align: center; margin-bottom: 1rem; font-size: 2.5rem;">Our Services</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 4rem;">Dynamic solutions for modern challenges</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 3rem;">
                <div style="background: white; padding: 2.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transform: skew(-5deg); margin: 1rem 0;">
                    <div style="transform: skew(5deg);">
                        <h3 style="color: #1e293b; margin-bottom: 1rem;">Strategic Planning</h3>
                        <p style="color: #64748b;">Dynamic strategies that adapt to changing market conditions.</p>
                    </div>
                </div>
                <div style="background: white; padding: 2.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transform: skew(5deg); margin: 1rem 0;">
                    <div style="transform: skew(-5deg);">
                        <h3 style="color: #1e293b; margin-bottom: 1rem;">Creative Design</h3>
                        <p style="color: #64748b;">Innovative designs that break traditional boundaries.</p>
                    </div>
                </div>
                <div style="background: white; padding: 2.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); transform: skew(-5deg); margin: 1rem 0;">
                    <div style="transform: skew(5deg);">
                        <h3 style="color: #1e293b; margin-bottom: 1rem;">Implementation</h3>
                        <p style="color: #64748b;">Seamless execution with dynamic project management.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="padding: 6rem 0; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; position: relative;">
        <div style="position: absolute; top: 0; right: 0; width: 0; height: 0; border-style: solid; border-width: 0 0 100px 100px; border-color: transparent transparent rgba(255,255,255,0.1) transparent;"></div>
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; text-align: center; position: relative; z-index: 2;">
            <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Ready to Break Boundaries?</h2>
            <p style="margin-bottom: 3rem; font-size: 1.125rem;">Let's create something extraordinary together.</p>
            <a href="mailto:contact@example.com" class="btn btn-primary">Contact Us</a>
        </div>
    </section>"""

    def generate_full_height_sidebar_html(self):
        """Full height sidebar layout"""
        return """    <!-- Full Height Sidebar Hero -->
    <section class="hero">
        <div class="hero-sidebar">
            <h1>Professional Excellence</h1>
            <p>Delivering exceptional results through innovative solutions and dedicated service.</p>
            <a href="#contact" class="btn btn-primary">Get Started</a>
        </div>
        <div class="hero-content">
            <h2 style="color: #333333; font-size: 2.5rem; margin-bottom: 2rem;">Why Choose Us?</h2>
            <div style="display: grid; gap: 2rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.5rem;">1</div>
                    <div>
                        <h3 style="color: #333333; margin-bottom: 0.5rem;">Expert Team</h3>
                        <p style="color: #64748b;">Highly skilled professionals with years of experience.</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #10b981, #3b82f6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.5rem;">2</div>
                    <div>
                        <h3 style="color: #333333; margin-bottom: 0.5rem;">Quality Results</h3>
                        <p style="color: #64748b;">Consistent delivery of high-quality outcomes.</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #f59e0b, #ef4444); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.5rem;">3</div>
                    <div>
                        <h3 style="color: #333333; margin-bottom: 0.5rem;">Customer Focus</h3>
                        <p style="color: #64748b;">Your satisfaction is our top priority.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" style="padding: 6rem 0; background: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem; font-size: 2.5rem;">Our Services</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 4rem;">Comprehensive solutions for your needs</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div style="background: #f8fafc; padding: 2.5rem; border-radius: 12px; text-align: center; border-left: 4px solid #3b82f6;">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Consulting</h3>
                    <p style="color: #64748b;">Strategic guidance to help you achieve your goals.</p>
                </div>
                <div style="background: #f8fafc; padding: 2.5rem; border-radius: 12px; text-align: center; border-left: 4px solid #10b981;">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Implementation</h3>
                    <p style="color: #64748b;">Expert execution of your vision and requirements.</p>
                </div>
                <div style="background: #f8fafc; padding: 2.5rem; border-radius: 12px; text-align: center; border-left: 4px solid #f59e0b;">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Support</h3>
                    <p style="color: #64748b;">Ongoing assistance to ensure your continued success.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="padding: 6rem 0; background: #f8fafc;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; text-align: center;">
            <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Ready to Get Started?</h2>
            <p style="color: #64748b; margin-bottom: 3rem;">Contact us today to discuss your project.</p>
            <a href="mailto:contact@example.com" class="btn btn-primary">Contact Us</a>
        </div>
    </section>"""

    def generate_card_stack_html(self):
        """Card stack layout with overlapping elements"""
        return """    <!-- Card Stack Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h1>Innovative Card Design</h1>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; max-width: 600px; margin-left: auto; margin-right: auto;">Experience our unique approach to presenting information through dynamic card layouts.</p>

            <div class="hero-cards">
                <div class="hero-card">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Strategy</h3>
                    <p style="color: #64748b;">Comprehensive planning and strategic thinking.</p>
                </div>
                <div class="hero-card">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Design</h3>
                    <p style="color: #64748b;">Creative solutions that stand out from the crowd.</p>
                </div>
                <div class="hero-card">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Results</h3>
                    <p style="color: #64748b;">Measurable outcomes that drive success.</p>
                </div>
            </div>

            <div style="margin-top: 3rem;">
                <a href="#contact" class="btn btn-primary">Explore Our Work</a>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" style="padding: 6rem 0; background: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem; font-size: 2.5rem;">Our Approach</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 4rem;">Layered solutions for complex challenges</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: rotate(-1deg);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Discovery</h3>
                    <p style="color: #64748b;">Understanding your unique needs and challenges.</p>
                </div>
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: rotate(1deg);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Development</h3>
                    <p style="color: #64748b;">Creating tailored solutions that fit perfectly.</p>
                </div>
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: rotate(-0.5deg);">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">Delivery</h3>
                    <p style="color: #64748b;">Implementing solutions with precision and care.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="padding: 6rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem; text-align: center;">
            <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Let's Build Something Amazing</h2>
            <p style="margin-bottom: 3rem; font-size: 1.125rem; opacity: 0.9;">Ready to see what we can create together?</p>
            <a href="mailto:contact@example.com" class="btn btn-primary">Start Your Project</a>
        </div>
    </section>"""

    def generate_magazine_style_html(self):
        """Magazine-style layout with editorial design"""
        return """    <!-- Magazine Style Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div class="hero-layout">
                <div class="hero-main">
                    <h1>EDITORIAL EXCELLENCE</h1>
                    <div class="subtitle">Where Content Meets Design</div>
                    <p style="font-size: 1.125rem; color: #64748b; margin-bottom: 2rem; line-height: 1.8;">Discover the perfect blend of compelling content and sophisticated design. Our magazine-style approach brings editorial quality to every project.</p>
                    <a href="#contact" class="btn btn-primary">Read More</a>
                </div>
                <div class="hero-sidebar">
                    <h3 style="color: #1e293b; margin-bottom: 1rem; font-size: 1.25rem;">Featured Story</h3>
                    <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1rem;">How we transformed a simple idea into a compelling narrative that resonates with audiences.</p>
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 1rem; margin-top: 1rem;">
                        <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">This Issue</div>
                        <div style="font-weight: 600; color: #1e293b;">Design Innovation</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Editorial Services -->
    <section id="services" style="padding: 6rem 0; background: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 4rem; align-items: start;">
                <div>
                    <h2 style="font-size: 2.5rem; margin-bottom: 1rem; line-height: 1.1;">Our Editorial Services</h2>
                    <p style="color: #64748b; font-size: 1.125rem; line-height: 1.7;">Professional content creation with magazine-quality design and layout.</p>
                </div>
                <div style="display: grid; gap: 3rem;">
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: start;">
                        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="color: #1e293b; margin-bottom: 0.5rem; font-size: 1.25rem;">01</h3>
                            <div style="font-weight: 600; color: #3b82f6;">Content Strategy</div>
                        </div>
                        <div>
                            <p style="color: #64748b; line-height: 1.7;">Developing compelling narratives that engage your audience and drive meaningful connections.</p>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: start;">
                        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="color: #1e293b; margin-bottom: 0.5rem; font-size: 1.25rem;">02</h3>
                            <div style="font-weight: 600; color: #10b981;">Editorial Design</div>
                        </div>
                        <div>
                            <p style="color: #64748b; line-height: 1.7;">Creating visually stunning layouts that enhance readability and user experience.</p>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: start;">
                        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px;">
                            <h3 style="color: #1e293b; margin-bottom: 0.5rem; font-size: 1.25rem;">03</h3>
                            <div style="font-weight: 600; color: #f59e0b;">Publication</div>
                        </div>
                        <div>
                            <p style="color: #64748b; line-height: 1.7;">Delivering polished, professional content ready for publication across all platforms.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="padding: 6rem 0; background: #1e293b; color: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div style="text-align: center; max-width: 600px; margin: 0 auto;">
                <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Start Your Story</h2>
                <p style="margin-bottom: 3rem; font-size: 1.125rem; opacity: 0.9;">Every great publication begins with a conversation. Let's discuss your editorial needs.</p>
                <a href="mailto:contact@example.com" class="btn btn-primary">Contact Our Editorial Team</a>
            </div>
        </div>
    </section>"""
