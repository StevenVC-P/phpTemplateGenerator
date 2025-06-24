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
        print(f"   Color Strategy: {color_strategy}")
        print(f"   Hero Style: {hero_style}")
        print(f"   Typography: {typography_pairing}")
        print(f"   Button Style: {button_style}")

        # Generate dramatically different CSS based on design variation
        css = self.generate_variation_css(color_strategy, hero_style, typography_pairing, button_style, unique_elements)

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

    def generate_variation_html(self, hero_style, layout_structure, component_styles):
        """Generate completely different HTML structures"""

        if hero_style == "split_layout" or hero_style == "split_screen":
            return self.generate_split_layout_html()
        elif hero_style == "minimal_focus":
            return self.generate_minimal_focus_html()
        elif hero_style == "overlay_hero":
            return self.generate_overlay_hero_html()
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
                <div style="padding: 2rem; background: #f8fafc; border-left: 4px solid #2563eb;">
                    <h3 style="color: #2563eb; margin-bottom: 1rem;">Strategy</h3>
                    <p>Comprehensive planning and strategic guidance for sustainable growth.</p>
                </div>

                <div style="padding: 2rem; background: #f8fafc; border-left: 4px solid #f59e0b;">
                    <h3 style="color: #f59e0b; margin-bottom: 1rem;">Execution</h3>
                    <p>Flawless implementation with attention to every detail.</p>
                </div>

                <div style="padding: 2rem; background: #f8fafc; border-left: 4px solid #059669;">
                    <h3 style="color: #059669; margin-bottom: 1rem;">Results</h3>
                    <p>Measurable outcomes that drive your business forward.</p>
                </div>
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
                <div style="margin-bottom: 3rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #2563eb;">01. Consultation</h3>
                    <p style="font-size: 1.125rem; line-height: 1.7; color: #4b5563;">Deep understanding of your needs through comprehensive analysis and strategic planning.</p>
                </div>

                <div style="margin-bottom: 3rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #2563eb;">02. Implementation</h3>
                    <p style="font-size: 1.125rem; line-height: 1.7; color: #4b5563;">Precise execution with continuous monitoring and adjustment for optimal results.</p>
                </div>

                <div style="margin-bottom: 3rem;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: #2563eb;">03. Optimization</h3>
                    <p style="font-size: 1.125rem; line-height: 1.7; color: #4b5563;">Ongoing refinement to ensure sustained success and continuous improvement.</p>
                </div>
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
                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 25px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; transition: transform 0.3s ease;">
                    <h3 style="color: #2563eb; margin-bottom: 1rem;">Consultation</h3>
                    <p>Expert advice and strategic planning to help you make informed decisions for your business growth.</p>
                </div>

                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 25px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; transition: transform 0.3s ease;">
                    <h3 style="color: #2563eb; margin-bottom: 1rem;">Implementation</h3>
                    <p>Professional execution of solutions with attention to detail and commitment to excellence.</p>
                </div>

                <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 25px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; transition: transform 0.3s ease;">
                    <h3 style="color: #2563eb; margin-bottom: 1rem;">Support</h3>
                    <p>Ongoing assistance and maintenance to ensure your continued success and satisfaction.</p>
                </div>
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
