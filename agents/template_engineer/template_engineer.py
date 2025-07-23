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

    def generate_php_template(self, prompt_data, design_data):
        """Generate dramatically different templates based on design variation"""
        system_context = prompt_data.get("system_prompt", "")
        user_request = prompt_data.get("user_prompt", "")

        # Extract business context from prompt data
        business_context = prompt_data.get("business_context", {})
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        project_type = business_context.get("project_type", "local_service_page")

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
        print(f"   Business: {business_name}")
        print(f"   Services: {services}")
        print(f"   Location: {location.get('city', 'Local')}")
        print(f"   Color Strategy: {color_strategy}")
        print(f"   Hero Style: {hero_style}")
        print(f"   Typography: {typography_pairing}")
        print(f"   Button Style: {button_style}")

        # Generate dramatically different CSS based on design variation
        css = self.generate_variation_css(color_strategy, hero_style, typography_pairing, button_style, unique_elements)

        # Generate completely different HTML structure based on layout with business context
        html_content = self.generate_variation_html(hero_style, layout_structure, component_styles, business_context)

        # Get fonts for this typography pairing
        fonts = self.get_typography_fonts(typography_pairing)

        return f"""<?php
// AI-Generated Template for {business_name}
// Business Type: {project_type}
// Location: {location.get('city', 'Local Area')}, {location.get('state', 'State')}
// Services: {', '.join(services)}
// Design Variation - Color Strategy: {color_strategy}, Hero Style: {hero_style}
// Typography: {typography_pairing}, Button Style: {button_style}
// Unique Elements: {', '.join(unique_elements)}

// Handle form submission
$form_submitted = false;
$form_errors = [];
$success_message = '';

if ($_POST) {{
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $message = trim($_POST['message'] ?? '');

    // Basic validation
    if (empty($name)) {{
        $form_errors[] = 'Name is required';
    }}
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {{
        $form_errors[] = 'Valid email is required';
    }}
    if (empty($message)) {{
        $form_errors[] = 'Message is required';
    }}

    if (empty($form_errors)) {{
        // Process form (save to database, send email, etc.)
        $success_message = 'Thank you for contacting {business_name}! We\\'ll get back to you soon.';
        $form_submitted = true;
    }}
}}
?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{business_name} - Professional {project_type.replace('_', ' ')} in {location.get('city', 'Local Area')}, {location.get('state', 'State')}">
    <title>{business_name} - {project_type.replace('_', ' ').title()}</title>
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

    def generate_variation_css(self, color_strategy, hero_style, typography_pairing, button_style, unique_elements):
        """Generate dramatically different CSS based on design variation"""
        fonts = self.get_typography_fonts(typography_pairing)

        # Color schemes based on strategy
        color_schemes = {
            "complementary_harmony": {
                "primary": "#2563eb", "secondary": "#f59e0b", "accent": "#dc2626",
                "bg": "#ffffff", "text": "#1f2937", "light": "#f8fafc"
            },
            "analogous_palette": {
                "primary": "#059669", "secondary": "#0891b2", "accent": "#7c3aed",
                "bg": "#ffffff", "text": "#1f2937", "light": "#f0fdf4"
            },
            "monochromatic": {
                "primary": "#374151", "secondary": "#6b7280", "accent": "#f59e0b",
                "bg": "#ffffff", "text": "#111827", "light": "#f9fafb"
            },
            "triadic_bold": {
                "primary": "#dc2626", "secondary": "#059669", "accent": "#2563eb",
                "bg": "#ffffff", "text": "#1f2937", "light": "#fef2f2"
            }
        }

        colors = color_schemes.get(color_strategy, color_schemes["complementary_harmony"])

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

        elif hero_style == "split_layout":
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

        elif hero_style == "asymmetric_grid":
            return f"""

        /* Asymmetric Grid Hero */
        .hero {{
            background: linear-gradient(135deg, {colors["bg"]} 0%, {colors["light"]} 100%);
            padding: 4rem 0;
            overflow: hidden;
        }}

        .hero-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr 1.5fr;
            grid-template-rows: auto auto;
            gap: 2rem;
            align-items: center;
            min-height: 70vh;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            color: {colors["primary"]};
            grid-column: 1 / 3;
            font-weight: 800;
            line-height: 1.1;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: {colors["text"]};
            grid-column: 1 / 2;
        }}

        .hero-visual {{
            grid-column: 3 / 4;
            grid-row: 1 / 3;
            background: linear-gradient(45deg, {colors["secondary"]}, {colors["accent"]});
            border-radius: 20px;
            height: 100%;
            min-height: 300px;
        }}"""

        elif hero_style == "diagonal_split":
            return f"""

        /* Diagonal Split Hero */
        .hero {{
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
            position: relative;
            min-height: 100vh;
            display: flex;
            align-items: center;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 60%;
            height: 100%;
            background: {colors["bg"]};
            transform: skewX(-15deg);
            transform-origin: top right;
            z-index: 1;
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
            width: 100%;
        }}

        .hero h1 {{
            font-size: 4rem;
            color: white;
            font-weight: 900;
            line-height: 1.1;
        }}

        .hero p {{
            font-size: 1.25rem;
            color: rgba(255,255,255,0.9);
            margin: 2rem 0;
        }}"""

        elif hero_style == "layered_parallax":
            return f"""

        /* Layered Parallax Hero */
        .hero {{
            position: relative;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
        }}

        .hero-layer {{
            position: absolute;
            width: 100%;
            height: 100%;
        }}

        .hero-layer-1 {{
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><circle cx="200" cy="200" r="100" fill="{colors["accent"]}" opacity="0.1"/><circle cx="800" cy="400" r="150" fill="{colors["light"]}" opacity="0.1"/></svg>');
            animation: float 6s ease-in-out infinite;
        }}

        .hero-layer-2 {{
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><polygon points="100,100 300,50 400,200 200,250" fill="{colors["secondary"]}" opacity="0.05"/></svg>');
            animation: float 8s ease-in-out infinite reverse;
        }}

        .hero-content {{
            position: relative;
            z-index: 3;
            text-align: center;
            color: white;
        }}

        .hero h1 {{
            font-size: 4.5rem;
            font-weight: 300;
            margin-bottom: 2rem;
            text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(2deg); }}
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

        elif button_style == "sharp_edges":
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

    def generate_variation_html(self, hero_style, layout_structure, component_styles, business_context):
        """Generate completely different HTML structures with business-specific content"""

        if hero_style == "split_layout" or hero_style == "split_screen":
            return self.generate_split_layout_html(business_context)
        elif hero_style == "minimal_focus":
            return self.generate_minimal_focus_html(business_context)
        elif hero_style == "overlay_hero":
            return self.generate_overlay_hero_html(business_context)
        elif hero_style == "asymmetric_grid":
            return self.generate_asymmetric_grid_html(business_context)
        elif hero_style == "diagonal_split":
            return self.generate_diagonal_split_html(business_context)
        elif hero_style == "layered_parallax":
            return self.generate_layered_parallax_html(business_context)
        elif hero_style == "card_mosaic":
            return self.generate_card_mosaic_html(business_context)
        elif hero_style == "timeline_flow":
            return self.generate_timeline_flow_html(business_context)
        else:
            return self.generate_classic_centered_html(business_context)

    def generate_split_layout_html(self, business_context):
        """Split layout with image/content side by side"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")

        return f"""    <!-- Split Layout Hero -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1>Welcome to {business_name}</h1>
                    <p>Experience the difference with our professional {services[0].lower()} approach. We combine expertise with innovative solutions for {city} businesses.</p>
                    <a href="#contact" class="btn btn-primary">Start Your Journey</a>
                </div>
                <div class="hero-visual">
                    <div style="background: rgba(255,255,255,0.2); height: 400px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">
                        {business_name}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Grid -->
    <section id="services" class="services" style="padding: 6rem 0; background: white;">
        <div class="container">
            <h2 style="text-align: center; margin-bottom: 3rem; font-size: 2.5rem;">Our Services</h2>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">"""

        # Generate dynamic services for split layout
        colors = ["#2563eb", "#f59e0b", "#059669", "#dc2626", "#7c3aed", "#0891b2"]
        services_html = ""
        for i, service in enumerate(services):
            color = colors[i % len(colors)]
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="padding: 2rem; background: #f8fafc; border-left: 4px solid {color};">
                    <h3 style="color: {color}; margin-bottom: 1rem;">{service}</h3>
                    <p>{description}</p>
                </div>"""

        return services_html + f"""
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" style="background: #1f2937; color: white; padding: 4rem 0; text-align: center;">
        <div class="container">
            <h2 style="color: white; margin-bottom: 2rem;">Contact {business_name}</h2>
            <p style="margin-bottom: 2rem; font-size: 1.25rem;">Ready to get started? Let's discuss how we can help your business succeed.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: transparent; border: 2px solid white; color: white;">Get Quote</a>
        </div>
    </section>"""

    def generate_minimal_focus_html(self, business_context):
        """Minimal, typography-focused layout"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")

        # Generate dynamic services for minimal layout
        services_html = ""
        for i, service in enumerate(services[:3]):  # Limit to 3 for minimal layout
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="margin-bottom: 3rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #2563eb;">{i+1:02d}. {service}</h3>
                    <p style="font-size: 1.125rem; line-height: 1.7; color: #4b5563;">{description}</p>
                </div>"""

        return f"""    <!-- Minimal Header -->
    <header style="background: white; padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 700; font-size: 1.25rem;">{business_name.upper()}</div>
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
            <h1>Excellence in {services[0]}</h1>
            <p>We believe in the power of simplicity. Our approach focuses on what matters most—delivering exceptional {services[0].lower()} results for {city} businesses through thoughtful execution.</p>
            <a href="#contact" class="btn btn-primary">Discover More</a>
        </div>
    </section>

    <!-- Minimal Services -->
    <section id="services" style="padding: 6rem 0; background: #fafafa;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="margin-bottom: 3rem; font-size: 2rem;">Our Services</h2>
            <div style="space-y: 3rem;">
{services_html}
            </div>
        </div>
    </section>

    <!-- Minimal Contact -->
    <section id="contact" style="padding: 6rem 0; background: white;">
        <div class="container" style="max-width: 600px; margin: 0 auto; padding: 0 1rem; text-align: center;">
            <h2 style="margin-bottom: 2rem;">Contact {business_name}</h2>
            <p style="margin-bottom: 3rem; font-size: 1.125rem; color: #6b7280;">Ready to start your project? We'd love to hear from you.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: transparent; border: 2px solid #2563eb; color: #2563eb;">Get Quote</a>
        </div>
    </section>"""

    <!-- Minimal Services -->
    <section id="services" style="padding: 6rem 0; background: #fafafa;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="margin-bottom: 3rem; font-size: 2rem;">Our Services</h2>

            <div style="space-y: 3rem;">"""

        # Generate dynamic services for minimal layout
        services_html = ""
        for i, service in enumerate(services[:3]):  # Limit to 3 for minimal layout
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="margin-bottom: 3rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #2563eb;">{i+1:02d}. {service}</h3>
                    <p style="font-size: 1.125rem; line-height: 1.7; color: #4b5563;">{description}</p>
                </div>"""

        return services_html + f"""
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

    def generate_classic_centered_html(self, business_context):
        """Traditional centered layout with business-specific content"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")
        state = location.get("state", "State")

        return f"""    <!-- Classic Header -->
    <header style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 1.5rem; font-weight: 700;">{business_name}</div>
                <div>
                    <a href="#services" style="color: white; text-decoration: none; margin-left: 2rem;">Services</a>
                    <a href="#about" style="color: white; text-decoration: none; margin-left: 2rem;">About</a>
                    <a href="#contact" style="color: white; text-decoration: none; margin-left: 2rem;">Contact</a>
                </div>
            </nav>
        </div>
    </header>

    <!-- Classic Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h1>Welcome to {business_name}</h1>
            <p>Serving {city}, {state} with professional {services[0].lower()} and exceptional customer service.</p>
            <a href="#contact" class="btn btn-primary">Get Started Today</a>
        </div>
    </section>

    <!-- Classic Services -->
    <section id="services" style="padding: 4rem 0; background: white;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="text-align: center; margin-bottom: 1rem;">Our Services</h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 3rem;">Professional solutions tailored to your needs in {city}, {state}</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 3rem;">"""

        # Generate service cards based on actual services with intelligent descriptions
        services_html = ""
        for i, service in enumerate(services[:3]):  # Limit to 3 services for layout
            # Generate intelligent description based on service name
            description = self.generate_service_description(service, business_name)

            services_html += f"""
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 25px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; transition: transform 0.3s ease;">
                    <h3 style="color: #2563eb; margin-bottom: 1rem;">{service}</h3>
                    <p>{description}</p>
                </div>"""

        return services_html + f"""
            </div>
        </div>
    </section>

    <!-- Classic Contact -->
    <section id="contact" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 4rem 0; text-align: center;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <h2 style="color: white; margin-bottom: 1rem;">Contact {business_name}</h2>
            <p style="margin-bottom: 2rem; opacity: 0.9;">Ready to get started? Contact us today for a free consultation and discover how we can help your business succeed.</p>

            <?php if ($success_message): ?>
                <div style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.5); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
                    <?php echo htmlspecialchars($success_message); ?>
                </div>
            <?php endif; ?>

            <?php if (!empty($form_errors)): ?>
                <div style="background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
                    <?php foreach ($form_errors as $error): ?>
                        <p><?php echo htmlspecialchars($error); ?></p>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>

            <form method="POST" action="" style="max-width: 600px; margin: 0 auto 2rem;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                    <input type="text" name="name" placeholder="Your Name" value="<?php echo htmlspecialchars($_POST['name'] ?? ''); ?>" required style="padding: 1rem; border: none; border-radius: 8px; font-size: 1rem;">
                    <input type="email" name="email" placeholder="Your Email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>" required style="padding: 1rem; border: none; border-radius: 8px; font-size: 1rem;">
                </div>
                <input type="tel" name="phone" placeholder="Your Phone (Optional)" value="<?php echo htmlspecialchars($_POST['phone'] ?? ''); ?>" style="width: 100%; padding: 1rem; border: none; border-radius: 8px; font-size: 1rem; margin-bottom: 1rem;">
                <textarea name="message" placeholder="Tell us about your project..." required style="width: 100%; padding: 1rem; border: none; border-radius: 8px; font-size: 1rem; min-height: 120px; margin-bottom: 1rem; resize: vertical;"><?php echo htmlspecialchars($_POST['message'] ?? ''); ?></textarea>
                <button type="submit" style="background: white; color: #2563eb; padding: 1rem 2rem; border: none; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: all 0.3s;">Send Message</button>
            </form>

            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <a href="tel:555-555-5555" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600;">Call (555) 555-5555</a>
                <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600;">Send Email</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer style="background: #1f2937; color: white; padding: 2rem 0; text-align: center;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <p>&copy; <?php echo date('Y'); ?> {business_name}. Serving {city}, {state}. All rights reserved.</p>
        </div>
    </footer>"""

    def generate_overlay_hero_html(self, business_context):
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
                <div class="service-card">
                    <h3>Consultation</h3>
                    <p>Expert advice and strategic planning to help you make informed decisions for your business growth.</p>
                </div>

                <div class="service-card">
                    <h3>Implementation</h3>
                    <p>Professional execution of solutions with attention to detail and commitment to excellence.</p>
                </div>

                <div class="service-card">
                    <h3>Support</h3>
                    <p>Ongoing assistance and maintenance to ensure your continued success and satisfaction.</p>
                </div>
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

    def generate_service_description(self, service_name, business_name):
        """Generate intelligent service descriptions based on service name and business context"""
        service_lower = service_name.lower()

        # Landscaping and outdoor services
        if any(keyword in service_lower for keyword in ['landscape', 'garden', 'outdoor', 'lawn', 'yard']):
            if 'design' in service_lower:
                return f"Transform your outdoor space with our expert landscape design services. We create beautiful, functional landscapes tailored to your property and lifestyle."
            elif 'maintenance' in service_lower or 'planning' in service_lower:
                return f"Keep your landscape looking its best year-round with our comprehensive maintenance and planning services."
            elif 'installation' in service_lower:
                return f"Professional landscape installation services bringing your outdoor vision to life with quality materials and expert craftsmanship."
            else:
                return f"Professional landscaping services designed to enhance your property's beauty and value."

        # Hardscaping and construction
        elif any(keyword in service_lower for keyword in ['hardscape', 'hardscaping', 'stone', 'patio', 'walkway', 'retaining']):
            return f"Expert hardscaping services including patios, walkways, retaining walls, and stone features that add structure and beauty to your landscape."

        # IT and technology services
        elif any(keyword in service_lower for keyword in ['it', 'tech', 'computer', 'network', 'cloud', 'cyber']):
            if 'consulting' in service_lower:
                return f"Strategic IT consulting services to help your business leverage technology for growth, efficiency, and competitive advantage."
            elif 'network' in service_lower:
                return f"Professional network setup and maintenance services ensuring reliable, secure connectivity for your business operations."
            elif 'cloud' in service_lower:
                return f"Seamless cloud migration services helping you modernize your infrastructure while reducing costs and improving scalability."
            else:
                return f"Comprehensive IT services designed to keep your technology running smoothly and securely."

        # Cleaning and maintenance services
        elif any(keyword in service_lower for keyword in ['clean', 'maintenance', 'seasonal']):
            if 'seasonal' in service_lower:
                return f"Comprehensive seasonal cleanup services to prepare your property for each season and maintain its pristine appearance."
            else:
                return f"Professional cleaning and maintenance services ensuring your space remains spotless and well-maintained."

        # Installation services
        elif 'installation' in service_lower:
            if 'irrigation' in service_lower:
                return f"Expert irrigation system installation and setup ensuring your landscape receives optimal water coverage for healthy growth."
            else:
                return f"Professional installation services with attention to detail and commitment to quality workmanship."

        # Consultation services
        elif any(keyword in service_lower for keyword in ['consult', 'planning', 'assessment']):
            if 'native plant' in service_lower:
                return f"Expert native plant consultation helping you choose sustainable, locally-adapted plants that thrive in your environment."
            else:
                return f"Professional consultation services providing expert guidance and strategic planning for your project success."

        # Design services
        elif 'design' in service_lower:
            return f"Creative design services that bring your vision to life with innovative solutions and attention to aesthetic detail."

        # Development services
        elif 'development' in service_lower:
            return f"Custom development services using the latest technologies and best practices to deliver robust, scalable solutions."

        # Support services
        elif 'support' in service_lower:
            return f"Reliable support services ensuring your continued success with responsive assistance when you need it most."

        # Generic fallback with business context
        else:
            return f"Professional {service_name.lower()} services delivered with expertise, quality, and dedication to your satisfaction."

    def generate_asymmetric_grid_html(self, business_context):
        """Asymmetric grid layout with dynamic positioning"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")
        state = location.get("state", "State")

        # Generate floating service cards
        services_html = ""
        for i, service in enumerate(services):
            offset = (i % 2) * 20 - 10  # Alternate positioning
            rotation = (i - 1) * 2  # Slight rotation
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); transform: translateY({offset}px) rotate({rotation}deg); transition: all 0.3s ease;">
                    <h3 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.5rem;">{service}</h3>
                    <p style="color: #64748b; line-height: 1.6;">{description}</p>
                    <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb;">
                        <a href="#contact" style="color: #3b82f6; text-decoration: none; font-weight: 600;">Learn More →</a>
                    </div>
                </div>"""

        return f"""    <!-- Asymmetric Grid Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1400px; margin: 0 auto; padding: 0 2rem;">
            <div class="hero-grid">
                <h1>{business_name}</h1>
                <p>Professional {services[0].lower()} solutions designed for businesses in {city}, {state}. We combine creativity with technical expertise to deliver exceptional results.</p>
                <div class="hero-visual"></div>
                <div style="grid-column: 2 / 4; display: flex; gap: 1rem; align-items: center;">
                    <a href="#services" class="btn btn-primary" style="padding: 1rem 2rem; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">Explore Services</a>
                    <a href="#contact" class="btn" style="padding: 1rem 2rem; border: 2px solid #3b82f6; color: #3b82f6; text-decoration: none; border-radius: 8px; font-weight: 600;">Get Quote</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Floating Services Cards -->
    <section id="services" style="padding: 8rem 0; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); position: relative;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem; color: #1f2937;">Our Services</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
{services_html}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; padding: 6rem 0; text-align: center;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1.5rem;">Contact {business_name}</h2>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; opacity: 0.9;">Ready to get started? Contact us today to discuss your project needs.</p>
            <a href="tel:555-555-5555" class="btn" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 1.25rem 3rem; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 1.125rem;">Get Started</a>
        </div>
    </section>"""

    def generate_diagonal_split_html(self, business_context):
        """Diagonal split layout with angled sections"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")

        return f"""    <!-- Diagonal Split Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div class="hero-content">
                <div>
                    <h1>{business_name}</h1>
                    <p>Cutting-edge {services[0].lower()} solutions that push boundaries and deliver exceptional results for businesses in {city}.</p>
                    <div style="margin-top: 3rem;">
                        <a href="#contact" class="btn btn-primary" style="background: white; color: #1f2937; padding: 1.25rem 2.5rem; border-radius: 8px; text-decoration: none; font-weight: 700; margin-right: 1rem;">Get Started</a>
                        <a href="#services" style="color: white; text-decoration: none; font-weight: 600; border-bottom: 2px solid white;">View Services →</a>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-end;">
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; backdrop-filter: blur(10px);">
                        <h4 style="color: white; margin-bottom: 0.5rem;">Expert Team</h4>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Professional specialists</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; backdrop-filter: blur(10px);">
                        <h4 style="color: white; margin-bottom: 0.5rem;">Proven Results</h4>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Successful projects delivered</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Angled Services Section -->
    <section style="padding: 6rem 0; background: white; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(45deg, transparent 0%, #f8fafc 50%, transparent 100%); transform: skewY(-3deg); transform-origin: top left;"></div>
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 2;">
            <h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem; color: #1f2937;">Our Services</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 3rem;">"""

        # Generate angled service cards
        services_html = ""
        for i, service in enumerate(services):
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); transform: rotate({(i-1)*1}deg); transition: all 0.3s ease;">
                    <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 12px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">🌿</div>
                    <h3 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.5rem;">{service}</h3>
                    <p style="color: #64748b; line-height: 1.6; margin-bottom: 1.5rem;">{description}</p>
                    <a href="#contact" style="color: #3b82f6; text-decoration: none; font-weight: 600;">Learn More →</a>
                </div>"""

        return f"""    <!-- Diagonal Split Hero -->
    <section class="hero">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div class="hero-content">
                <div>
                    <h1>{business_name}</h1>
                    <p>Professional {services[0].lower()} solutions that deliver exceptional results for businesses in {city}.</p>
                    <div style="margin-top: 3rem;">
                        <a href="#contact" class="btn btn-primary" style="background: white; color: #1f2937; padding: 1.25rem 2.5rem; border-radius: 8px; text-decoration: none; font-weight: 700; margin-right: 1rem;">Get Started</a>
                        <a href="#services" style="color: white; text-decoration: none; font-weight: 600; border-bottom: 2px solid white;">View Services →</a>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-end;">
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; backdrop-filter: blur(10px);">
                        <h4 style="color: white; margin-bottom: 0.5rem;">Expert Team</h4>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Professional specialists</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; backdrop-filter: blur(10px);">
                        <h4 style="color: white; margin-bottom: 0.5rem;">Proven Results</h4>
                        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Successful projects delivered</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Angled Services Section -->
    <section id="services" style="padding: 6rem 0; background: white; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(45deg, transparent 0%, #f8fafc 50%, transparent 100%); transform: skewY(-3deg); transform-origin: top left;"></div>
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 2;">
            <h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem; color: #1f2937;">Our Services</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 3rem;">
{services_html}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; padding: 6rem 0; text-align: center;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1.5rem;">Contact {business_name}</h2>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; opacity: 0.9;">Ready to transform your landscape? Contact us today to discuss your project.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white;">Send Email</a>
        </div>
    </section>"""

    def generate_layered_parallax_html(self, business_context):
        """Layered parallax layout with depth effects"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")

        return f"""    <!-- Layered Parallax Hero -->
    <section class="hero">
        <div class="hero-layer hero-layer-1"></div>
        <div class="hero-layer hero-layer-2"></div>
        <div class="hero-content">
            <h1>{business_name}</h1>
            <p>Experience the future of {services[0].lower()} with our innovative solutions designed for {city} businesses.</p>
            <div style="margin-top: 3rem;">
                <a href="#contact" class="btn btn-primary" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white; padding: 1.25rem 2.5rem; border-radius: 50px; text-decoration: none; font-weight: 600; backdrop-filter: blur(10px);">Start Your Journey</a>
            </div>
        </div>
    </section>

    <!-- Depth Services -->
    <section style="padding: 8rem 0; background: linear-gradient(135deg, #1f2937 0%, #111827 100%); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1200 800\"><defs><pattern id=\"grid\" width=\"40\" height=\"40\" patternUnits=\"userSpaceOnUse\"><path d=\"M 40 0 L 0 0 0 40\" fill=\"none\" stroke=\"rgba(255,255,255,0.05)\" stroke-width=\"1\"/></pattern></defs><rect width=\"100%\" height=\"100%\" fill=\"url(%23grid)\"/></svg>'); opacity: 0.3;"></div>
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 2;">
            <h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem; color: white;">Our Expertise</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 3rem; perspective: 1000px;">"""

        # Generate 3D service cards
        services_html = ""
        for i, service in enumerate(services):
            depth = (i % 3) * 10 + 10  # Varying depth
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="background: rgba(255,255,255,0.1); padding: 3rem; border-radius: 20px; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.2); transform: translateZ({depth}px) rotateY({(i-1)*5}deg); transition: all 0.5s ease;">
                    <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 50%; margin-bottom: 2rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem;">🌿</div>
                    <h3 style="color: white; margin-bottom: 1rem; font-size: 1.5rem;">{service}</h3>
                    <p style="color: rgba(255,255,255,0.8); line-height: 1.6; margin-bottom: 2rem;">{description}</p>
                    <a href="#contact" style="color: #60a5fa; text-decoration: none; font-weight: 600;">Explore →</a>
                </div>"""

        return f"""    <!-- Layered Parallax Hero -->
    <section class="hero">
        <div class="hero-layer hero-layer-1"></div>
        <div class="hero-layer hero-layer-2"></div>
        <div class="hero-content">
            <h1>{business_name}</h1>
            <p>Experience the future of {services[0].lower()} with our innovative solutions designed for {city} businesses.</p>
            <div style="margin-top: 3rem;">
                <a href="#contact" class="btn btn-primary" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white; padding: 1.25rem 2.5rem; border-radius: 50px; text-decoration: none; font-weight: 600; backdrop-filter: blur(10px);">Start Your Journey</a>
            </div>
        </div>
    </section>

    <!-- Depth Services -->
    <section id="services" style="padding: 8rem 0; background: linear-gradient(135deg, #1f2937 0%, #111827 100%); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1200 800\"><defs><pattern id=\"grid\" width=\"40\" height=\"40\" patternUnits=\"userSpaceOnUse\"><path d=\"M 40 0 L 0 0 0 40\" fill=\"none\" stroke=\"rgba(255,255,255,0.05)\" stroke-width=\"1\"/></pattern></defs><rect width=\"100%\" height=\"100%\" fill=\"url(%23grid)\"/></svg>'); opacity: 0.3;"></div>
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 2;">
            <h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem; color: white;">Our Expertise</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 3rem; perspective: 1000px;">
{services_html}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 6rem 0; text-align: center;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1.5rem;">Contact {business_name}</h2>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; opacity: 0.9;">Ready to transform your landscape? Contact us today to discuss your project.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white;">Send Email</a>
        </div>
    </section>"""

    def generate_card_mosaic_html(self, business_context):
        """Interactive card mosaic layout"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")

        # Generate mosaic service cards with different sizes
        services_html = ""
        grid_positions = [
            "grid-column: 7 / 10; grid-row: 1 / 3;",
            "grid-column: 10 / 13; grid-row: 1 / 4;",
            "grid-column: 1 / 4; grid-row: 4 / 7;",
            "grid-column: 4 / 8; grid-row: 4 / 6;",
            "grid-column: 8 / 13; grid-row: 4 / 8;",
            "grid-column: 1 / 6; grid-row: 7 / 9;"
        ]

        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

        for i, service in enumerate(services[:6]):  # Limit to 6 for layout
            position = grid_positions[i % len(grid_positions)]
            color = colors[i % len(colors)]
            description = self.generate_service_description(service, business_name)
            services_html += f"""
                <div style="{position} background: {color}; border-radius: 16px; padding: 2rem; display: flex; flex-direction: column; justify-content: center; color: white; transition: all 0.3s ease; cursor: pointer;">
                    <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">{service}</h3>
                    <p style="opacity: 0.9; font-size: 0.95rem;">{description[:60]}...</p>
                </div>"""

        # Add CTA card
        services_html += f"""
                <div style="grid-column: 6 / 13; grid-row: 6 / 9; background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); border-radius: 16px; padding: 2rem; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; text-align: center;">
                    <h3 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem;">Ready to Start?</h3>
                    <p style="margin-bottom: 2rem; opacity: 0.9;">Let's discuss your project</p>
                    <a href="#contact" style="background: white; color: #ea580c; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: 600;">Get Quote</a>
                </div>"""

        return f"""    <!-- Card Mosaic Hero -->
    <section style="padding: 4rem 0; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); min-height: 100vh; display: flex; align-items: center;">
        <div class="container" style="max-width: 1400px; margin: 0 auto; padding: 0 2rem;">
            <div style="display: grid; grid-template-columns: repeat(12, 1fr); grid-template-rows: repeat(8, 100px); gap: 1rem; height: 80vh;">
                <!-- Main title card -->
                <div style="grid-column: 1 / 7; grid-row: 1 / 4; background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border-radius: 24px; padding: 3rem; display: flex; flex-direction: column; justify-content: center; color: white;">
                    <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.1;">{business_name}</h1>
                    <p style="font-size: 1.25rem; opacity: 0.9;">Professional landscaping solutions for {city} businesses</p>
                </div>

                <!-- Service cards -->
{services_html}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; padding: 6rem 0; text-align: center;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1.5rem;">Contact {business_name}</h2>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; opacity: 0.9;">Ready to transform your landscape? Contact us today to discuss your project.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white;">Send Email</a>
        </div>
    </section>"""

    def generate_timeline_flow_html(self, business_context):
        """Timeline flow layout with story progression"""
        business_name = business_context.get("name", "Professional Service")
        services = business_context.get("services", ["Professional Services"])
        location = business_context.get("location", {})
        city = location.get("city", "Local Area")

        return f"""    <!-- Timeline Flow Hero -->
    <section style="padding: 6rem 0; background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; position: relative;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div style="text-align: center; margin-bottom: 4rem;">
                <h1 style="font-size: 4rem; font-weight: 300; margin-bottom: 1rem;">{business_name}</h1>
                <p style="font-size: 1.5rem; opacity: 0.8;">Your journey to success starts here in {city}</p>
            </div>

            <!-- Timeline -->
            <div style="position: relative; max-width: 800px; margin: 0 auto;">
                <!-- Timeline line -->
                <div style="position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom, #3b82f6, #10b981, #f59e0b); transform: translateX(-50%);"></div>"""

        # Generate timeline steps
        timeline_html = ""
        steps = ["Discovery", "Planning", "Implementation", "Success"]

        for i, (step, service) in enumerate(zip(steps, services + ["Results"])):
            is_left = i % 2 == 0
            margin_side = "margin-right: 50%;" if is_left else "margin-left: 50%;"
            text_align = "text-align: right;" if is_left else "text-align: left;"

            # Use intelligent service descriptions
            if i < len(services):
                description = self.generate_service_description(service, business_name)
                service_text = f"Professional {service.lower()}"
            else:
                description = "Delivered on time with measurable success"
                service_text = "Exceptional Results"

            timeline_html += f"""
                <div style="position: relative; margin-bottom: 4rem;">
                    <div style="{margin_side} {text_align} padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 16px; backdrop-filter: blur(10px);">
                        <div style="position: absolute; top: 50%; {'right: -20px;' if is_left else 'left: -20px;'} width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; transform: translateY(-50%);">{i+1}</div>
                        <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #60a5fa;">{step}</h3>
                        <h4 style="font-size: 1.25rem; margin-bottom: 0.5rem;">{service if i < len(services) else 'Exceptional Results'}</h4>
                        <p style="opacity: 0.8;">{description[:80]}...</p>
                    </div>
                </div>"""

        return f"""    <!-- Timeline Flow Hero -->
    <section style="padding: 6rem 0; background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; position: relative;">
        <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div style="text-align: center; margin-bottom: 4rem;">
                <h1 style="font-size: 4rem; font-weight: 300; margin-bottom: 1rem;">{business_name}</h1>
                <p style="font-size: 1.5rem; opacity: 0.8;">Your journey to success starts here in {city}</p>
            </div>

            <!-- Timeline -->
            <div style="position: relative; max-width: 800px; margin: 0 auto;">
                <!-- Timeline line -->
                <div style="position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom, #3b82f6, #10b981, #f59e0b); transform: translateX(-50%);"></div>
{timeline_html}
            </div>

            <div style="text-align: center; margin-top: 4rem;">
                <a href="#contact" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 1.25rem 3rem; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 1.125rem;">Start Your Journey</a>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 6rem 0; text-align: center;">
        <div class="container" style="max-width: 800px; margin: 0 auto; padding: 0 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1.5rem;">Contact {business_name}</h2>
            <p style="font-size: 1.25rem; margin-bottom: 3rem; opacity: 0.9;">Ready to get started? Contact us today to discuss your project.</p>
            <a href="tel:555-555-5555" class="btn btn-primary" style="margin-right: 1rem;">Call Now</a>
            <a href="mailto:info@{business_name.lower().replace(' ', '')}.com" class="btn" style="background: rgba(255,255,255,0.2); color: white; border: 2px solid white;">Send Email</a>
        </div>
    </section>"""
