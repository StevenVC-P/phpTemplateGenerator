import json
import re
from pathlib import Path
from typing import Dict, Any
from bs4 import BeautifulSoup
import sys
import os

# Add the project root to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.agent_result import AgentResult


class WordpressThemeAssembler:
    def __init__(self, config=None):
        if config is None:
            config_path = Path(__file__).parent / "wordpress_theme_assembler.json"
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = config
    
    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        """
        Transform a static PHP template into a complete WordPress theme structure
        """
        try:
            input_path = Path(input_file)
            template_content = input_path.read_text(encoding='utf-8')
            template_id = self.extract_template_id(input_path.name)

            # Create WordPress theme directory
            template_dir = input_path.parent.parent  # Go up from templates/ to template_xxx/
            wp_theme_dir = template_dir / f"wordpress_theme_{template_id}"
            wp_theme_dir.mkdir(exist_ok=True)

            # Check if this is a multi-page request by looking for spec file
            spec_file = template_dir / "specs" / "template_spec.json"
            is_multi_page = False
            spec_data = {}

            if spec_file.exists():
                with open(spec_file, 'r') as f:
                    spec_data = json.load(f)
                    is_multi_page = spec_data.get("site_type") == "multi_page"

            # Parse the template content
            soup = BeautifulSoup(template_content, 'html.parser')
            extracted_css = self.extract_css(template_content)

            # Generate WordPress theme files
            self.generate_style_css(wp_theme_dir, template_id, extracted_css, spec_data, template_content)
            self.generate_functions_php(wp_theme_dir, template_id, spec_data)

            if is_multi_page:
                # Generate multi-page theme structure
                files_generated = self.generate_multi_page_theme(wp_theme_dir, soup, template_id, spec_data)
                print(f"✅ Multi-page WordPress theme generated in {wp_theme_dir} ({files_generated} files)")
            else:
                # Generate single-page theme structure (existing logic)
                self.generate_index_php(wp_theme_dir, soup, template_id)
                self.generate_header_php(wp_theme_dir, soup)
                self.generate_footer_php(wp_theme_dir, soup)
                self.generate_page_php(wp_theme_dir, soup)
                self.generate_single_php(wp_theme_dir, soup)
                files_generated = 7
                print(f"✅ Single-page WordPress theme generated in {wp_theme_dir}")

            return AgentResult(
                agent_id="wordpress_theme_assembler",
                success=True,
                output_file=str(wp_theme_dir),
                metadata={"template_id": template_id, "theme_files": files_generated, "is_multi_page": is_multi_page}
            )

        except Exception as e:
            return AgentResult(
                agent_id="wordpress_theme_assembler",
                success=False,
                error_message=str(e)
            )
    
    def extract_template_id(self, filename: str) -> str:
        """Extract template ID from filename"""
        match = re.search(r"template_([a-zA-Z0-9_]+)\.php", filename)
        return match.group(1) if match else "000"
    
    def extract_css(self, template_content: str) -> str:
        """Extract CSS from <style> tags in the template"""
        style_pattern = r'<style[^>]*>(.*?)</style>'
        matches = re.findall(style_pattern, template_content, re.DOTALL)
        return '\n'.join(matches) if matches else ""
    
    def generate_style_css(self, wp_theme_dir: Path, template_id: str, css_content: str, spec_data: dict = None, full_template_content: str = None):
        """Generate WordPress style.css preserving enhanced design variations from Template Engineer"""
        theme_header = """/*
Theme Name: Enhanced Design Theme {template_id}
Description: AI-generated WordPress theme with enhanced design variations and modern features
Author: AI Template Generator
Version: 2.0
Requires at least: 6.0
Tested up to: 6.4
Requires PHP: 7.4
License: GPL v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: enhanced-theme-{template_id}
*/

""".format(template_id=template_id)

        # Enhanced modern dark theme CSS with contemporary styling
        enhanced_dark_css = """
/* CSS Custom Properties for Theme Adaptation */
:root {
    --primary-color: #3b82f6;
    --primary-rgb: 59, 130, 246;
    --primary-hover: #60a5fa;
    --nav-bg-color: rgba(15, 23, 42, 0.95);
    --nav-bg-hover: rgba(30, 41, 59, 0.9);
    --nav-text-color: #f8fafc;
    --background-color: #0f172a;
    --background-rgb: 15, 23, 42;
    --text-color: #e2e8f0;
    --text-rgb: 226, 232, 240;
}

/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.7;
    color: #e2e8f0;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    min-height: 100vh;
    font-size: 16px;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 1.5rem;
    color: #f8fafc;
    letter-spacing: -0.025em;
}

h1 { font-size: clamp(2.5rem, 5vw, 4rem); }
h2 { font-size: clamp(2rem, 4vw, 3rem); }
h3 { font-size: clamp(1.5rem, 3vw, 2rem); }

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

/* Header */
.site-header {
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    padding: 1.5rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Logo */
.site-logo, .site-title a {
    font-size: 1.75rem;
    font-weight: 800;
    color: #38bdf8;
    text-decoration: none;
    letter-spacing: -0.025em;
    transition: color 0.3s ease;
}

.site-logo:hover, .site-title a:hover {
    color: #0ea5e9;
}

/* Navigation */
.main-navigation ul, .main-nav ul {
    list-style: none;
    display: flex;
    gap: 2.5rem;
    align-items: center;
}

.main-navigation a, .main-nav a {
    color: #cbd5e1;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    transition: all 0.3s ease;
    position: relative;
}

.main-navigation a:hover, .main-nav a:hover {
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
}

.main-navigation a.current, .main-nav a.current {
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.15);
}

/* Hero Section */
.hero, .hero-section {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%),
                radial-gradient(circle at 20% 50%, rgba(56, 189, 248, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.1) 0%, transparent 50%);
    padding: 8rem 0 6rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(148,163,184,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    opacity: 0.3;
}

.hero .container {
    position: relative;
    z-index: 2;
}

.hero h1 {
    font-size: clamp(3rem, 6vw, 4.5rem);
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #f8fafc 0%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    letter-spacing: -0.05em;
}

.hero .subtitle, .hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    color: #94a3b8;
    font-weight: 500;
}

.hero p {
    font-size: 1.125rem;
    margin-bottom: 3rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    color: #cbd5e1;
    line-height: 1.8;
}

/* Modern CTA Buttons */
.cta-buttons, .hero-cta {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 2rem;
}

.cta-button, .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

.cta-button.primary, .btn-primary {
    background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    color: #0f172a;
    box-shadow: 0 4px 14px 0 rgba(56, 189, 248, 0.3);
}

.cta-button.primary:hover, .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px 0 rgba(56, 189, 248, 0.4);
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
}

.cta-button.secondary, .btn-secondary {
    background: rgba(56, 189, 248, 0.1);
    color: #38bdf8;
    border-color: rgba(56, 189, 248, 0.3);
    backdrop-filter: blur(10px);
}

.cta-button.secondary:hover, .btn-secondary:hover {
    background: rgba(56, 189, 248, 0.2);
    border-color: #38bdf8;
    transform: translateY(-2px);
}
"""

        wp_specific_css = """
/* Modern Services Section */
.services, .services-overview {
    padding: 6rem 0;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.03) 0%, rgba(168, 85, 247, 0.03) 100%);
    backdrop-filter: blur(20px);
    position: relative;
}

.services::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(148,163,184,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
    opacity: 0.5;
}

.services .container {
    position: relative;
    z-index: 2;
}

.services h2 {
    text-align: center;
    font-size: clamp(2.5rem, 4vw, 3.5rem);
    margin-bottom: 4rem;
    color: #f8fafc;
    font-weight: 700;
    letter-spacing: -0.025em;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2.5rem;
}

.service-card {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%);
    backdrop-filter: blur(15px);
    padding: 2.5rem;
    border-radius: 20px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.service-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #38bdf8 0%, #a855f7 100%);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.service-card:hover::before {
    transform: scaleX(1);
}

.service-card:hover {
    transform: translateY(-8px);
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(168, 85, 247, 0.12) 100%);
    box-shadow: 0 20px 40px rgba(56, 189, 248, 0.15);
    border-color: rgba(56, 189, 248, 0.3);
}

.service-card h3 {
    color: #f8fafc;
    margin-bottom: 1.5rem;
    font-size: 1.75rem;
    font-weight: 600;
}

.service-card p {
    color: #cbd5e1;
    margin-bottom: 1.5rem;
    line-height: 1.7;
}

.service-card .learn-more, .service-link {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.service-card .learn-more:hover, .service-link:hover {
    color: #0ea5e9;
    transform: translateX(4px);
}

/* Enhanced Services Page Styles */
.services-page .services-overview {
    background: rgba(56, 189, 248, 0.05);
    border-bottom: 1px solid rgba(56, 189, 248, 0.1);
    padding: 3rem 0;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.benefit-item {
    text-align: center;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    border: 1px solid rgba(56, 189, 248, 0.1);
    transition: all 0.3s ease;
}

.benefit-item:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(56, 189, 248, 0.2);
    transform: translateY(-4px);
}

.benefit-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
}

.benefit-item h3 {
    color: #38bdf8;
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
}

.benefit-item p {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.5;
}

.services-main {
    padding: 4rem 0;
}

.services-page .service-card {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.service-header {
    padding: 2rem 2rem 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.service-icon {
    font-size: 2.5rem;
    flex-shrink: 0;
}

.service-header h3 {
    color: #38bdf8;
    font-size: 1.5rem;
    margin: 0;
    font-weight: 600;
    line-height: 1.3;
}

.service-body {
    padding: 0 2rem;
    flex-grow: 1;
}

.service-description {
    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    font-size: 1rem;
}

.service-features h4 {
    color: #38bdf8;
    font-size: 1rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
}

.service-features ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.service-features li {
    color: #cbd5e1;
    padding: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;
    font-size: 0.95rem;
    line-height: 1.5;
}

.service-features li::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: #38bdf8;
    font-weight: bold;
}

.service-footer {
    padding: 1.5rem 2rem 2rem;
    border-top: 1px solid rgba(56, 189, 248, 0.1);
    margin-top: 1rem;
}

.service-pricing {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.price-label {
    color: #94a3b8;
    font-size: 0.875rem;
}

.price {
    color: #38bdf8;
    font-size: 1.5rem;
    font-weight: 700;
}

.service-actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.service-actions .btn {
    flex: 1;
    min-width: 120px;
    text-align: center;
    justify-content: center;
}

.service-details-toggle {
    background: rgba(56, 189, 248, 0.1);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}

.service-details-toggle:hover {
    background: rgba(56, 189, 248, 0.2);
    border-color: #38bdf8;
}

/* Footer */
.site-footer {
    background: rgba(0, 0, 0, 0.8);
    padding: 3rem 0 1rem;
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3 {
    color: #4fc3f7;
    margin-bottom: 1rem;
}

.footer-section p, .footer-section a {
    color: #e0e0e0;
    text-decoration: none;
}

.footer-section a:hover {
    color: #4fc3f7;
}

.footer-bottom, .site-info {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1rem;
    color: #b0b0b0;
}

/* WordPress Core Styles */
.alignnone { margin: 5px 20px 20px 0; }
.aligncenter, div.aligncenter { display: block; margin: 5px auto 5px auto; }
.alignright { float: right; margin: 5px 0 20px 20px; }
.alignleft { float: left; margin: 5px 20px 20px 0; }
.wp-caption { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); max-width: 96%; padding: 5px 3px 10px; text-align: center; }
.wp-caption img { border: 0 none; height: auto; margin: 0; max-width: 98.5%; padding: 0; width: auto; }
.wp-caption p.wp-caption-text { font-size: 11px; line-height: 17px; margin: 0; padding: 0 4px 5px; color: #e0e0e0; }

/* Gutenberg Block Styles */
.wp-block-group { margin: 1em 0; }
.wp-block-columns { display: flex; flex-wrap: wrap; }
.wp-block-column { flex: 1; margin: 0 1em; }
.wp-block-button .wp-block-button__link {
    background-color: #4fc3f7;
    color: #1a1a2e;
    padding: 0.75em 1.5em;
    text-decoration: none;
    border-radius: 8px;
    display: inline-block;
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
    display: none;
    flex-direction: column;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    z-index: 1001;
}

.mobile-menu-toggle .hamburger-line {
    width: 25px;
    height: 3px;
    background: #ffffff;
    margin: 3px 0;
    transition: 0.3s ease;
    border-radius: 2px;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(1) {
    transform: rotate(-45deg) translate(-5px, 6px);
}

.mobile-menu-toggle.active .hamburger-line:nth-child(2) {
    opacity: 0;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(3) {
    transform: rotate(45deg) translate(-5px, -6px);
}

/* Enhanced Mobile-First Responsive Design */

/* Small Mobile Devices (320px - 480px) */
@media (max-width: 480px) {
    .container {
        padding: 0 1rem;
        max-width: 100%;
    }

    .hero {
        padding: 4rem 0 3rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Enhanced Section Spacing for Mobile */
    .services, .services-overview,
    .about, .about-section,
    .testimonials, .testimonials-section,
    .contact, .contact-section {
        padding: 3rem 0;
        margin-bottom: 2rem;
    }

    .services:first-of-type,
    .about:first-of-type {
        padding-top: 2rem;
    }

    /* Better Content Flow */
    .section-title {
        margin-bottom: 2rem;
        text-align: center;
    }

    .section-content {
        margin-bottom: 2rem;
    }

    /* Improved Card Spacing */
    .service-card,
    .feature-card {
        margin-bottom: 2rem;
    }

    .service-card:last-child,
    .feature-card:last-child {
        margin-bottom: 0;
    }

    .hero h1 {
        font-size: 2rem;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    .hero .subtitle {
        font-size: 1rem;
        line-height: 1.4;
        margin-bottom: 1.5rem;
    }

    .hero p {
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .cta-button, .btn {
        min-height: 48px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        max-width: 280px;
        margin: 0.5rem 0;
    }

    .cta-buttons, .hero-cta {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        width: 100%;
    }

    .section-title, .services h2, .about h2, .testimonials h2, .contact h2 {
        font-size: 1.75rem;
        line-height: 1.3;
        margin-bottom: 1.5rem;
    }

    .services-grid, .features-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }

    .service-card, .feature-card {
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .service-card h3, .feature-card h3 {
        font-size: 1.25rem;
        line-height: 1.4;
        margin-bottom: 1rem;
    }

    .service-card p, .feature-card p {
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Enhanced Services Page Mobile */
    .services-page .benefits-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }

    .benefit-item {
        padding: 1rem;
    }

    .benefit-icon {
        font-size: 2rem;
    }

    .service-header {
        padding: 1.5rem 1.5rem 1rem;
        flex-direction: column;
        text-align: center;
        gap: 0.75rem;
    }

    .service-body {
        padding: 0 1.5rem;
    }

    .service-footer {
        padding: 1rem 1.5rem 1.5rem;
    }

    .service-actions {
        flex-direction: column;
        gap: 0.75rem;
    }

    .service-actions .btn {
        width: 100%;
        min-width: auto;
    }

    .service-pricing {
        justify-content: center;
        margin-bottom: 1rem;
    }
}

/* Large Mobile Devices (481px - 768px) */
@media (min-width: 481px) and (max-width: 768px) {
    .container {
        padding: 0 1.5rem;
    }

    .hero {
        padding: 5rem 0 4rem;
    }

    .hero h1 {
        font-size: 2.5rem;
        line-height: 1.2;
    }

    .hero .subtitle {
        font-size: 1.125rem;
        line-height: 1.4;
    }

    .cta-button, .btn {
        min-height: 48px;
        padding: 1rem 2rem;
        font-size: 1.125rem;
    }

    .cta-buttons, .hero-cta {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .services-grid, .features-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
}

/* Tablet Devices (769px - 1024px) */
@media (min-width: 769px) and (max-width: 1024px) {
    .container {
        padding: 0 2rem;
    }

    .hero h1 {
        font-size: 3rem;
    }

    .services-grid, .features-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
    }
}

    /* Enhanced Mobile Menu Styles */
    .mobile-menu-toggle {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 1001;
    }

    .mobile-menu-toggle span {
        display: block;
        width: 24px;
        height: 3px;
        background: #38bdf8;
        margin: 3px 0;
        transition: 0.3s;
        border-radius: 2px;
    }

    .main-nav {
        position: fixed;
        top: 0;
        right: -100%;
        width: 320px;
        height: 100vh;
        background: rgba(15, 23, 42, 0.98);
        backdrop-filter: blur(20px);
        padding: 5rem 2rem 2rem;
        transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1000;
        box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
        overflow-y: auto;
    }

    .main-nav.active {
        right: 0;
    }

    /* Enhanced Mobile Menu Reliability */
    body.mobile-menu-open {
        overflow: hidden;
        position: fixed;
        width: 100%;
    }

    .main-nav.active {
        visibility: visible !important;
        opacity: 1 !important;
        transform: translateX(0) !important;
    }

    .mobile-menu-toggle.active .hamburger-line:nth-child(1) {
        transform: rotate(-45deg) translate(-5px, 6px) !important;
    }

    .mobile-menu-toggle.active .hamburger-line:nth-child(2) {
        opacity: 0 !important;
    }

    .mobile-menu-toggle.active .hamburger-line:nth-child(3) {
        transform: rotate(45deg) translate(-5px, -6px) !important;
    }

    /* Fallback styles for older browsers */
    @supports not (backdrop-filter: blur(20px)) {
        .main-nav {
            background: rgba(15, 23, 42, 0.98);
        }
    }

    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .main-nav {
            background: #000000;
            border: 2px solid #ffffff;
        }

        .main-nav .nav-menu a {
            color: #ffffff;
            border-bottom: 1px solid #ffffff;
        }
    }

    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        .main-nav,
        .mobile-menu-toggle .hamburger-line {
            transition: none;
        }
    }

    .main-nav .nav-menu,
    .main-nav #primary-menu {
        flex-direction: column;
        gap: 0;
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .main-nav .nav-menu li,
    .main-nav #primary-menu li {
        margin: 0;
        border-bottom: 1px solid rgba(56, 189, 248, 0.1);
    }

    .main-nav .nav-menu li:last-child,
    .main-nav #primary-menu li:last-child {
        border-bottom: none;
    }

    .main-nav .nav-menu a,
    .main-nav #primary-menu a {
        display: block;
        padding: 1.25rem 0;
        color: #e2e8f0;
        text-decoration: none;
        font-size: 1.125rem;
        font-weight: 500;
        transition: all 0.3s ease;
        min-height: 48px;
        display: flex;
        align-items: center;
    }

    .main-nav .nav-menu a:hover,
    .main-nav #primary-menu a:hover {
        color: #38bdf8;
        padding-left: 1rem;
    }

    /* Mobile Form Elements */
    input[type="text"],
    input[type="email"],
    input[type="tel"],
    textarea,
    select {
        min-height: 48px;
        padding: 1rem;
        font-size: 1rem;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        width: 100%;
        margin-bottom: 1rem;
    }

    /* Mobile Card Touch Targets */
    .service-card,
    .feature-card,
    .testimonial-card {
        cursor: pointer;
        transition: transform 0.2s ease;
    }

    .service-card:active,
    .feature-card:active,
    .testimonial-card:active {
        transform: scale(0.98);
    }

    /* Enhanced Mobile Visual Hierarchy */

    /* Better Section Separation */
    .services, .services-overview,
    .about, .about-section,
    .testimonials, .testimonials-section,
    .contact, .contact-section {
        border-bottom: 1px solid rgba(56, 189, 248, 0.1);
        position: relative;
    }

    .services:last-of-type,
    .contact:last-of-type {
        border-bottom: none;
    }

    /* Improved Content Contrast */
    .service-card,
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .service-card:hover,
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }

    /* Enhanced Typography Hierarchy */
    .hero h1 {
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .hero .subtitle {
        color: #38bdf8;
        font-weight: 500;
    }

    .section-title {
        color: #ffffff;
        position: relative;
        padding-bottom: 1rem;
    }

    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #38bdf8, #0ea5e9);
        border-radius: 2px;
    }

    /* Better Content Readability */
    .service-card h3,
    .feature-card h3 {
        color: #38bdf8;
        margin-bottom: 0.75rem;
    }

    .service-card p,
    .feature-card p {
        color: #cbd5e1;
        line-height: 1.7;
    }

    /* Enhanced CTA Visibility */
    .service-card .learn-more,
    .feature-card .learn-more {
        color: #38bdf8;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }

    .service-card .learn-more:hover,
    .feature-card .learn-more:hover {
        border-bottom-color: #38bdf8;
    }

    /* Mobile Focus States */
    .cta-button:focus,
    .btn:focus,
    input:focus,
    textarea:focus {
        outline: 3px solid #38bdf8;
        outline-offset: 2px;
    }

    .main-nav .nav-menu a,
    .main-nav #primary-menu a {
        display: block;
        padding: 1rem 0;
        color: #ffffff;
        text-decoration: none;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        transition: color 0.3s ease;
    }

    .main-nav .nav-menu a:hover,
    .main-nav #primary-menu a:hover {
        color: #4fc3f7;
    }

    .header-container {
        justify-content: space-between;
        align-items: center;
    }
}

/* Enhanced Mobile Menu Toggle - Theme-adaptive design */
.mobile-menu-toggle {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--nav-bg-color, rgba(15, 23, 42, 0.9)) !important;
    border: 1px solid var(--primary-color, #3b82f6) !important;
    border-radius: 8px !important;
    cursor: pointer;
    padding: 0.75rem !important;
    z-index: 1001;
    width: 48px !important;
    height: 48px !important;
    position: relative;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1) !important;
}

.mobile-menu-toggle:hover {
    background: var(--nav-bg-hover, rgba(30, 41, 59, 0.9)) !important;
    border-color: var(--primary-hover, #60a5fa) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
}

.mobile-menu-toggle .hamburger-line,
.mobile-menu-toggle span {
    display: block !important;
    width: 20px !important;
    height: 2px !important;
    background: var(--nav-text-color, #f8fafc) !important;
    margin: 3px 0 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border-radius: 2px !important;
}

/* Hamburger Animation - Smooth and elegant */
.mobile-menu-toggle.active .hamburger-line:nth-child(1),
.mobile-menu-toggle.active span:nth-child(1) {
    transform: rotate(-45deg) translate(-4px, 5px) !important;
    background: var(--primary-color, #3b82f6) !important;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(2),
.mobile-menu-toggle.active span:nth-child(2) {
    opacity: 0 !important;
    transform: scale(0) !important;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(3),
.mobile-menu-toggle.active span:nth-child(3) {
    transform: rotate(45deg) translate(-4px, -5px) !important;
    background: var(--primary-color, #3b82f6) !important;
}

/* Main Navigation - Theme-adaptive mobile menu */
.main-nav {
    position: fixed !important;
    top: 0 !important;
    right: -100% !important;
    width: 280px !important;
    height: 100vh !important;
    background: var(--nav-bg-color, rgba(15, 23, 42, 0.95)) !important;
    backdrop-filter: blur(25px) !important;
    border-left: 1px solid var(--primary-color, #3b82f6) !important;
    box-shadow: -5px 0 25px rgba(59, 130, 246, 0.1) !important;
    padding: 100px 2rem 2rem !important;
    transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    z-index: 1000 !important;
    overflow-y: auto !important;
}

.main-nav.active {
    right: 0 !important;
    visibility: visible !important;
    opacity: 1 !important;
}

.main-nav ul {
    flex-direction: column !important;
    gap: 0.5rem !important;
    list-style: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

.main-nav li {
    margin: 0 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

.main-nav a {
    display: block !important;
    padding: 1rem 1.5rem !important;
    color: #f8fafc !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    border-radius: 8px !important;
    position: relative !important;
}

.main-nav a:hover,
.main-nav a:focus {
    color: #3b82f6 !important;
    background: rgba(59, 130, 246, 0.1) !important;
    transform: translateX(5px) !important;
}

.main-nav a::before {
    content: '' !important;
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    height: 100% !important;
    width: 3px !important;
    background: #3b82f6 !important;
    transform: scaleY(0) !important;
    transition: transform 0.3s ease !important;
}

.main-nav a:hover::before {
    transform: scaleY(1) !important;
}

/* Prevent body scroll when menu is open */
body.mobile-menu-open {
    overflow: hidden !important;
}
"""

        # Check if we have enhanced design variations from Template Engineer
        template_to_check = full_template_content if full_template_content else css_content
        if template_to_check and self.has_enhanced_design_variations(template_to_check):
            print("🎨 Preserving ENHANCED DESIGN VARIATIONS from Template Engineer")
            # Use the enhanced CSS from Template Engineer and add WordPress-specific enhancements
            enhanced_template_css = self.extract_enhanced_css(template_to_check)
            wp_specific_css = self.generate_wordpress_specific_css(enhanced_template_css)
            full_css = theme_header + enhanced_template_css + wp_specific_css
        else:
            # Fallback to color-based approach for older templates
            # Priority order: 1) Spec colors, 2) Template colors, 3) Default dark theme
            custom_colors = None

            # First, check if spec has color palette
            if spec_data and 'color_palette' in spec_data:
                # Handle both formats: direct colors and mapped_colors wrapper
                if 'mapped_colors' in spec_data['color_palette']:
                    custom_colors = spec_data['color_palette']['mapped_colors']
                    print(f"🎨 Using SPEC colors (mapped format) from template_spec.json: {custom_colors}")
                elif all(key in spec_data['color_palette'] for key in ['primary', 'background', 'text']):
                    custom_colors = spec_data['color_palette']
                    print(f"🎨 Using SPEC colors (direct format) from template_spec.json: {custom_colors}")
                else:
                    custom_colors = None

            # Second, check if template has custom colors (only if no spec colors found)
            if custom_colors is None and css_content and self.has_custom_colors(css_content, spec_data):
                custom_colors = self.extract_custom_colors(css_content, spec_data)
                print(f"🎨 Using EXTRACTED colors from template: {custom_colors}")

            if custom_colors:
                enhanced_css_with_custom_colors = self.apply_custom_colors_to_enhanced_css(enhanced_dark_css, custom_colors)
                wp_css_with_custom_colors = self.apply_custom_colors_to_enhanced_css(wp_specific_css, custom_colors)
                full_css = theme_header + enhanced_css_with_custom_colors + wp_css_with_custom_colors
            else:
                print("🎨 Using default enhanced dark theme")
                full_css = theme_header + enhanced_dark_css + wp_specific_css

        style_file = wp_theme_dir / "style.css"
        style_file.write_text(full_css, encoding='utf-8')

    def load_custom_colors_from_spec(self, spec_data: dict = None) -> dict:
        """Load custom colors from spec file"""
        if spec_data and 'color_palette' in spec_data:
            color_palette = spec_data['color_palette']

            # Extract colors from mapped format
            if 'mapped_colors' in color_palette:
                return color_palette['mapped_colors']

            # Extract from specified_colors format
            elif 'specified_colors' in color_palette:
                colors = {}
                for color_spec in color_palette['specified_colors']:
                    if 'usage' in color_spec and 'hex_code' in color_spec:
                        usage = color_spec['usage'].lower()
                        if 'button' in usage or 'accent' in usage:
                            colors['primary'] = color_spec['hex_code']
                        elif 'highlight' in usage or 'icon' in usage:
                            colors['secondary'] = color_spec['hex_code']
                        elif 'background' in usage:
                            colors['background'] = color_spec['hex_code']
                        elif 'text' in usage or 'header' in usage:
                            colors['text'] = color_spec['hex_code']
                        elif 'footer' in usage or 'secondary' in usage:
                            colors['accent'] = color_spec['hex_code']
                return colors

        return {}

    def has_custom_colors(self, css_content: str, spec_data: dict = None) -> bool:
        """Check if the CSS content contains custom colors (not default blue theme)"""
        # Try to get custom colors from spec first
        custom_colors = self.load_custom_colors_from_spec(spec_data)

        if custom_colors:
            # Check if any of the spec colors are present in the CSS
            for color_value in custom_colors.values():
                if color_value and color_value.lower() in css_content.lower():
                    return True

        # Fallback: check for any non-default colors using contrast analysis
        default_blue_colors = ["#38bdf8", "#0f172a", "#1e293b"]
        has_default_colors = any(color.lower() in css_content.lower() for color in default_blue_colors)

        # If it doesn't have default colors, it likely has custom colors
        if not has_default_colors:
            return True

        # Additional check: look for hex color patterns that aren't default
        import re
        hex_colors = re.findall(r'#[0-9a-fA-F]{6}', css_content)
        unique_colors = set(color.lower() for color in hex_colors)

        # Remove default colors from the set
        for default_color in default_blue_colors:
            unique_colors.discard(default_color.lower())

        # If there are remaining colors, it has custom colors
        return len(unique_colors) > 0

    def extract_custom_colors(self, css_content: str, spec_data: dict = None) -> dict:
        """Extract custom colors from spec data or template CSS"""
        # First try to get colors from spec data
        if spec_data:
            spec_colors = self.load_custom_colors_from_spec(spec_data)
            if spec_colors:
                print(f"🎨 Using SPEC colors (mapped format) from template_spec.json: {spec_colors}")
                return spec_colors

        # Fallback: extract from CSS content
        import re
        colors = {}

        # Extract colors from CSS rules using pattern matching
        color_patterns = [
            (r'color:\s*(#[0-9a-fA-F]{6})', 'text'),
            (r'background-color:\s*(#[0-9a-fA-F]{6})', 'background'),
            (r'background:\s*(#[0-9a-fA-F]{6})', 'primary'),
        ]

        for pattern, color_type in color_patterns:
            matches = re.findall(pattern, css_content)
            if matches:
                colors[color_type] = matches[0]

        # If no colors found through patterns, try to detect common color schemes
        if not colors:
            # Extract all hex colors and try to categorize them
            all_hex_colors = re.findall(r'#[0-9a-fA-F]{6}', css_content)
            unique_colors = list(set(all_hex_colors))

            # Simple heuristic: assign colors based on brightness and frequency
            if unique_colors:
                # Sort by frequency of appearance
                color_counts = {color: css_content.count(color) for color in unique_colors}
                sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

                # Assign most frequent colors to roles
                if len(sorted_colors) >= 1:
                    colors['primary'] = sorted_colors[0][0]
                if len(sorted_colors) >= 2:
                    colors['secondary'] = sorted_colors[1][0]
                if len(sorted_colors) >= 3:
                    colors['background'] = sorted_colors[2][0]
                if len(sorted_colors) >= 4:
                    colors['text'] = sorted_colors[3][0]

        print(f"🎨 Extracted custom colors: {colors}")
        return colors

    def apply_custom_colors_to_enhanced_css(self, enhanced_css: str, custom_colors: dict) -> str:
        """Apply custom colors to the enhanced CSS while preserving layout structure"""
        import re

        # Comprehensive color mapping from default enhanced theme to custom colors
        color_replacements = {}

        # Detect if this is a light theme (light background) or dark theme (dark background)
        is_light_theme = False
        if 'background' in custom_colors:
            bg_color = custom_colors['background'].lower()

            # Check if background is light (common light colors)
            light_backgrounds = ['#ffffff', '#f8f9fa', '#f5f5f5', '#fafafa', '#f0f0f0', '#f7f7f7', '#fcfcfc', '#f0ede5']
            is_light_theme = bg_color in [bg.lower() for bg in light_backgrounds]

            # Additional check: if background starts with 'f' and has high brightness, it's likely light
            if not is_light_theme and bg_color.startswith('#f'):
                is_light_theme = True

        print(f"🎨 Detected theme type: {'LIGHT' if is_light_theme else 'DARK'} theme")

        # Update CSS custom properties based on theme colors
        css_variables_updates = {}
        if 'primary' in custom_colors:
            primary_rgb = self.hex_to_rgb(custom_colors['primary'])
            css_variables_updates['--primary-color'] = custom_colors['primary']
            css_variables_updates['--primary-rgb'] = primary_rgb
            css_variables_updates['--primary-hover'] = custom_colors.get('secondary', custom_colors['primary'])

        if 'background' in custom_colors:
            bg_rgb = self.hex_to_rgb(custom_colors['background'])
            css_variables_updates['--background-color'] = custom_colors['background']
            css_variables_updates['--background-rgb'] = bg_rgb
            css_variables_updates['--nav-bg-color'] = f"rgba({bg_rgb}, 0.95)"
            css_variables_updates['--nav-bg-hover'] = f"rgba({bg_rgb}, 0.9)" if is_light_theme else f"rgba({bg_rgb}, 0.8)"

        if 'text' in custom_colors:
            text_rgb = self.hex_to_rgb(custom_colors['text'])
            css_variables_updates['--text-color'] = custom_colors['text']
            css_variables_updates['--text-rgb'] = text_rgb
            css_variables_updates['--nav-text-color'] = custom_colors['text']
        elif is_light_theme:
            # For light themes, use dark text
            css_variables_updates['--text-color'] = '#333333'
            css_variables_updates['--text-rgb'] = '51, 51, 51'
            css_variables_updates['--nav-text-color'] = '#333333'

        # For light themes, we need to replace dark theme defaults with light colors
        if is_light_theme:
            # Replace dark backgrounds with light background
            if 'background' in custom_colors:
                bg_rgb = self.hex_to_rgb(custom_colors['background'])
                color_replacements.update({
                    # Dark theme backgrounds → Light background
                    '#0f172a': custom_colors['background'],  # Main dark background
                    '#1e293b': custom_colors['background'],  # Medium dark background
                    '#334155': custom_colors['background'],  # Light dark background
                    'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)': f"linear-gradient(135deg, {custom_colors['background']} 0%, {custom_colors['background']} 50%, {custom_colors['background']} 100%)",
                    'rgba(15, 23, 42, 0.95)': f"rgba({bg_rgb}, 0.95)",
                    'rgba(15, 23, 42, 0.9)': f"rgba({bg_rgb}, 0.9)",
                    'rgba(30, 41, 59, 0.8)': f"rgba({bg_rgb}, 0.8)",
                })

            # Replace light text colors with dark text for light backgrounds
            if 'text' in custom_colors:
                color_replacements.update({
                    # Light text colors → Dark text
                    '#e2e8f0': custom_colors['text'],  # Main light text → Dark text
                    '#f8fafc': custom_colors['text'],  # Very light text → Dark text
                    '#cbd5e1': custom_colors['text'],  # Medium light text → Dark text
                    '#94a3b8': custom_colors['text'],  # Muted light text → Dark text
                })

        if 'primary' in custom_colors:
            # Replace primary blue colors with custom primary
            primary_rgb = self.hex_to_rgb(custom_colors['primary'])
            color_replacements.update({
                '#38bdf8': custom_colors['primary'],  # Main blue
                '#0ea5e9': custom_colors['primary'],  # Darker blue
                '#0284c7': custom_colors['primary'],  # Even darker blue
                '#4fc3f7': custom_colors['primary'],  # Light blue variant
                'rgba(56, 189, 248, 0.03)': f"rgba({primary_rgb}, 0.03)",
                'rgba(56, 189, 248, 0.05)': f"rgba({primary_rgb}, 0.05)",
                'rgba(56, 189, 248, 0.08)': f"rgba({primary_rgb}, 0.08)",
                'rgba(56, 189, 248, 0.1)': f"rgba({primary_rgb}, 0.1)",
                'rgba(56, 189, 248, 0.12)': f"rgba({primary_rgb}, 0.12)",
                'rgba(56, 189, 248, 0.15)': f"rgba({primary_rgb}, 0.15)",
                'rgba(56, 189, 248, 0.2)': f"rgba({primary_rgb}, 0.2)",
                'rgba(56, 189, 248, 0.3)': f"rgba({primary_rgb}, 0.3)",
                'rgba(56, 189, 248, 0.4)': f"rgba({primary_rgb}, 0.4)",
                'rgba(56, 189, 248, 0.5)': f"rgba({primary_rgb}, 0.5)",
            })

        if 'secondary' in custom_colors:
            # Replace secondary colors (like old sky blue with new sage green)
            secondary_rgb = self.hex_to_rgb(custom_colors['secondary'])
            color_replacements.update({
                '#A7D3F3': custom_colors['secondary'],  # Old sky blue
                '#9CAF88': custom_colors['secondary'],  # Sage green
                '#a855f7': custom_colors['secondary'],  # Purple accent
                'rgba(167, 211, 243, 0.1)': f"rgba({secondary_rgb}, 0.1)",
                'rgba(167, 211, 243, 0.2)': f"rgba({secondary_rgb}, 0.2)",
                'rgba(168, 85, 247, 0.03)': f"rgba({secondary_rgb}, 0.03)",
                'rgba(168, 85, 247, 0.08)': f"rgba({secondary_rgb}, 0.08)",
                'rgba(168, 85, 247, 0.12)': f"rgba({secondary_rgb}, 0.12)",
            })

        if 'background' in custom_colors:
            # Replace background colors
            bg_rgb = self.hex_to_rgb(custom_colors['background'])
            color_replacements.update({
                '#0f172a': custom_colors['background'],  # Dark background
                '#1e293b': custom_colors['background'],  # Medium background
                '#334155': custom_colors['background'],  # Light background
                '#F5F3EB': custom_colors['background'],  # Warm beige (old)
                '#F0EDE5': custom_colors['background'],  # Soft cream (new)
                '#ffffff': custom_colors['background'],  # White background (for dark themes)
                'rgba(15, 23, 42, 0.9)': f"rgba({bg_rgb}, 0.9)",
                'rgba(15, 23, 42, 0.95)': f"rgba({bg_rgb}, 0.95)",
                'rgba(30, 41, 59, 0.8)': f"rgba({bg_rgb}, 0.8)",
                'rgba(0, 0, 0, 0.8)': f"rgba({bg_rgb}, 0.8)",
                'rgba(240, 237, 229, 0.8)': f"rgba({bg_rgb}, 0.8)",
                'rgba(240, 237, 229, 0.9)': f"rgba({bg_rgb}, 0.9)",
                'rgba(240, 237, 229, 0.95)': f"rgba({bg_rgb}, 0.95)",
                'rgba(240, 237, 229, 0.98)': f"rgba({bg_rgb}, 0.98)",
                'rgba(255, 255, 255, 0.95)': f"rgba({bg_rgb}, 0.95)",  # Header background
                'rgba(255, 255, 255, 0.8)': f"rgba({bg_rgb}, 0.8)",   # Footer background
            })

        if 'text' in custom_colors:
            # Replace text colors
            text_rgb = self.hex_to_rgb(custom_colors['text'])
            color_replacements.update({
                '#e2e8f0': custom_colors['text'],  # Main text
                '#f8fafc': custom_colors['text'],  # Light text
                '#cbd5e1': custom_colors['text'],  # Medium text
                '#94a3b8': custom_colors['text'],  # Muted text
                '#ffffff': custom_colors['text'],  # White text (for dark themes)
                '#3b82f6': custom_colors['text'],  # Primary color used as text (fix contrast issue)
                '#1f2937': custom_colors['text'],  # Dark text
                '#374151': custom_colors['text'],  # Medium text
                '#6b7280': custom_colors['text'],  # Gray text
            })

        # Apply color replacements
        modified_css = enhanced_css
        for old_color, new_color in color_replacements.items():
            modified_css = modified_css.replace(old_color, new_color)

        # Use regex to catch any remaining rgba patterns with hardcoded colors
        if 'primary' in custom_colors:
            primary_rgb = self.hex_to_rgb(custom_colors['primary'])
            # Replace any remaining rgba(56, 189, 248, X) with custom primary
            modified_css = re.sub(
                r'rgba\(56,\s*189,\s*248,\s*([0-9.]+)\)',
                rf'rgba({primary_rgb}, \1)',
                modified_css
            )
            # Replace any remaining rgba(59, 130, 246, X) with custom primary
            modified_css = re.sub(
                r'rgba\(59,\s*130,\s*246,\s*([0-9.]+)\)',
                rf'rgba({primary_rgb}, \1)',
                modified_css
            )

        # Apply CSS custom property updates
        for css_var, value in css_variables_updates.items():
            # Update CSS custom properties in :root
            pattern = rf'{css_var}:\s*[^;]+;'
            replacement = f'{css_var}: {value};'
            modified_css = re.sub(pattern, replacement, modified_css)

        print(f"🎨 Applied {len(color_replacements)} color replacements and {len(css_variables_updates)} CSS variable updates to enhanced CSS")
        return modified_css

    def hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB values for rgba() functions"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r}, {g}, {b}"

    def has_enhanced_design_variations(self, css_content: str) -> bool:
        """Check if CSS contains enhanced design variations from Template Engineer"""
        enhanced_indicators = [
            # All Hero Styles from Template Engineer
            "Geometric Shapes Hero",
            "Floating Elements Hero",
            "Diagonal Split Hero",
            "Full Height Sidebar Hero",
            "Card Stack Hero",
            "Magazine Style Hero",
            "Minimal Focus Hero",
            "Split Layout Hero",
            "Split Screen Hero",
            "Overlay Hero",
            # Button Styles
            "Neon Glow Buttons",
            "Sharp Corporate",
            "Rounded Modern",
            "Geometric Bold",
            # Design Elements
            "Organic Blob",
            "triangular_mosaic",
            "geometric_patterns",
            "paper_grain_texture",
            "floating_icons",
            # CSS Animations and Effects
            "@keyframes rotate",
            "@keyframes float",
            "clip-path: polygon",
            "text-shadow:",
            "backdrop-filter:",
            "transform: rotate",
            "animation:",
            "box-shadow: 0 0",
            # Template Engineer Signature
            "/* AI-Generated Template with Dramatic Design Variation",
            "Color Strategy:",
            "Hero Style:",
            "Typography:",
            "Button Style:"
        ]

        for indicator in enhanced_indicators:
            if indicator in css_content:
                print(f"🎨 Found enhanced design indicator: {indicator}")
                return True
        return False

    def extract_enhanced_css(self, template_content: str) -> str:
        """Extract the enhanced CSS from Template Engineer, preserving all design variations"""
        import re

        # Multiple extraction strategies for robustness
        enhanced_css = ""

        # Strategy 1: Extract CSS from <style> tags
        style_pattern = r'<style[^>]*?>(.*?)</style>'
        style_matches = re.findall(style_pattern, template_content, re.DOTALL | re.IGNORECASE)

        if style_matches:
            enhanced_css = '\n'.join(style_matches)
            print(f"🎨 Strategy 1 SUCCESS: Extracted {len(enhanced_css)} characters from <style> tags")
        else:
            print("⚠️ Strategy 1 FAILED: No <style> tags found")

            # Strategy 2: Look for CSS between specific markers
            css_start = template_content.find('<style>')
            css_end = template_content.find('</style>')

            if css_start != -1 and css_end != -1:
                enhanced_css = template_content[css_start + 7:css_end]  # +7 to skip '<style>'
                print(f"🎨 Strategy 2 SUCCESS: Extracted {len(enhanced_css)} characters using string search")
            else:
                print("⚠️ Strategy 2 FAILED: No style markers found")
                print(f"🔍 Template content preview: {template_content[:500]}...")
                return ""

        if enhanced_css:
            # Clean up the CSS
            enhanced_css = re.sub(r'\n\s*\n', '\n\n', enhanced_css)
            print(f"🎨 Enhanced CSS preview: {enhanced_css[:200]}...")
            return enhanced_css
        else:
            return ""

    def generate_wordpress_specific_css(self, base_css: str) -> str:
        """Generate WordPress-specific CSS that complements the base template CSS"""
        return """
/* Enhanced Centering and Layout */
.container, .wp-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
    text-align: center;
}

.section-content {
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}

.services-grid, .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    justify-items: center;
    margin: 0 auto;
    max-width: 1000px;
}

.service-card, .feature-card {
    text-align: center;
    margin: 0 auto;
}

.hero, .hero-section {
    text-align: center;
}

.hero .container {
    text-align: center;
}

.cta-buttons, .hero-cta {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}

/* Better Typography Centering */
h1, h2, h3, .section-title {
    text-align: center;
    margin-left: auto;
    margin-right: auto;
}

.hero h1, .hero .subtitle, .hero p {
    text-align: center;
    margin-left: auto;
    margin-right: auto;
}

/* Mobile Centering */
@media (max-width: 768px) {
    .container {
        padding: 0 1rem;
        text-align: center;
    }

    .services-grid, .features-grid {
        grid-template-columns: 1fr;
        justify-items: center;
    }

    .service-card, .feature-card {
        max-width: 100%;
        text-align: center;
    }
}

/* WordPress-Specific Enhancements */
.wp-block-columns { display: flex; flex-wrap: wrap; }
.wp-block-column { flex: 1; margin: 0 1em; }

/* WordPress Alignment Classes */
.aligncenter, div.aligncenter { display: block; margin: 5px auto 5px auto; }
.alignright { float: right; margin: 5px 0 20px 20px; }
.alignleft { float: left; margin: 5px 20px 20px 0; }

/* WordPress Caption Styles */
.wp-caption {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    max-width: 96%;
    padding: 5px 3px 10px;
    text-align: center;
}
.wp-caption img {
    border: 0 none;
    height: auto;
    margin: 0;
    max-width: 98.5%;
    padding: 0;
    width: auto;
}
.wp-caption p.wp-caption-text {
    font-size: 11px;
    line-height: 17px;
    margin: 0;
    padding: 0 4px 5px;
}

/* Enhanced Mobile Menu Toggle - Light, integrated design */
.mobile-menu-toggle {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(240, 237, 229, 0.9);
    border: 1px solid rgba(59, 106, 77, 0.1);
    border-radius: 8px;
    cursor: pointer;
    padding: 0.75rem;
    z-index: 1001;
    width: 48px;
    height: 48px;
    position: relative;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 8px rgba(59, 106, 77, 0.1);
}

.mobile-menu-toggle:hover {
    background: rgba(156, 175, 136, 0.15);
    border-color: rgba(59, 106, 77, 0.2);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 106, 77, 0.15);
}

/* Main Navigation - Light, integrated mobile menu */
.main-nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 280px;
    height: 100vh;
    background: linear-gradient(135deg,
        rgba(240, 237, 229, 0.98) 0%,
        rgba(245, 243, 235, 0.95) 100%);
    backdrop-filter: blur(25px);
    border-left: 1px solid rgba(59, 106, 77, 0.1);
    box-shadow: -5px 0 25px rgba(59, 106, 77, 0.08);
    padding: 100px 2rem 2rem;
    transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
    overflow-y: auto;
}

.main-nav.active {
    right: 0 !important;
    visibility: visible !important;
    opacity: 1 !important;
}

.main-nav ul {
    flex-direction: column;
    gap: 0.5rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

.main-nav li {
    margin: 0;
    border-radius: 8px;
    overflow: hidden;
}

.main-nav a {
    display: block;
    padding: 1rem 1.5rem;
    color: #333333;
    text-decoration: none;
    font-weight: 500;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    border-radius: 8px;
    position: relative;
}

.main-nav a:hover,
.main-nav a:focus {
    color: #3B6A4D;
    background: rgba(156, 175, 136, 0.1);
    transform: translateX(5px);
}

.main-nav a::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 3px;
    background: #9CAF88;
    transform: scaleY(0);
    transition: transform 0.3s ease;
}

.main-nav a:hover::before {
    transform: scaleY(1);
}

/* Prevent body scroll when menu is open */
body.mobile-menu-open {
    overflow: hidden;
}

.mobile-menu-toggle .hamburger-line,
.mobile-menu-toggle span {
    display: block;
    width: 20px;
    height: 2px;
    background: #3B6A4D;
    margin: 3px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 2px;
}

/* Hamburger Animation - Smooth and elegant */
.mobile-menu-toggle.active .hamburger-line:nth-child(1),
.mobile-menu-toggle.active span:nth-child(1) {
    transform: rotate(-45deg) translate(-4px, 5px) !important;
    background: #9CAF88 !important;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(2),
.mobile-menu-toggle.active span:nth-child(2) {
    opacity: 0 !important;
    transform: scale(0) !important;
}

.mobile-menu-toggle.active .hamburger-line:nth-child(3),
.mobile-menu-toggle.active span:nth-child(3) {
    transform: rotate(45deg) translate(-4px, -5px) !important;
    background: #9CAF88 !important;
}

/* Mobile Navigation Styles */
@media (max-width: 768px) {
    .mobile-menu-toggle {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 48px;
        height: 48px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        z-index: 1001;
    }

    .mobile-menu-toggle span {
        display: block;
        width: 24px;
        height: 3px;
        background: currentColor;
        margin: 3px 0;
        transition: 0.3s;
        border-radius: 2px;
    }

    .main-nav {
        position: fixed;
        top: 0;
        right: -100%;
        width: 320px;
        height: 100vh;
        background: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(20px);
        padding: 5rem 2rem 2rem;
        transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1000;
        overflow-y: auto;
    }

    .main-nav.active {
        right: 0;
    }

    /* Enhanced Mobile Menu Reliability */
    body.mobile-menu-open {
        overflow: hidden;
        position: fixed;
        width: 100%;
    }

    .main-nav.active {
        visibility: visible !important;
        opacity: 1 !important;
        transform: translateX(0) !important;
    }

    .mobile-menu-toggle.active .hamburger-line:nth-child(1) {
        transform: rotate(-45deg) translate(-5px, 6px) !important;
    }

    .mobile-menu-toggle.active .hamburger-line:nth-child(2) {
        opacity: 0 !important;
    }

    .mobile-menu-toggle.active .hamburger-line:nth-child(3) {
        transform: rotate(45deg) translate(-5px, -6px) !important;
    }

    .main-nav .nav-menu,
    .main-nav #primary-menu {
        flex-direction: column;
        gap: 0;
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .main-nav .nav-menu li,
    .main-nav #primary-menu li {
        margin: 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .main-nav .nav-menu li:last-child,
    .main-nav #primary-menu li:last-child {
        border-bottom: none;
    }

    .main-nav .nav-menu a,
    .main-nav #primary-menu a {
        display: block;
        padding: 1.25rem 0;
        color: #ffffff;
        text-decoration: none;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
        padding-left: 0;
    }

    .main-nav .nav-menu a:hover,
    .main-nav #primary-menu a:hover {
        color: inherit;
        padding-left: 1rem;
        border-left-color: currentColor;
    }
}

/* Responsive Design Enhancements */
@media (max-width: 768px) {
    .hero, .hero-section {
        padding: 4rem 0 3rem;
        text-align: center;
    }

    .hero h1 {
        font-size: clamp(2rem, 8vw, 3rem);
    }

    .container {
        padding: 0 1rem;
    }
}
"""
    
    def generate_multi_page_theme(self, wp_theme_dir: Path, soup: BeautifulSoup, template_id: str, spec_data: dict) -> int:
        """Generate all files for a multi-page WordPress theme"""
        files_generated = 0

        # Generate common files
        self.generate_header_php(wp_theme_dir, soup)
        self.generate_footer_php(wp_theme_dir, soup)
        self.generate_theme_js(wp_theme_dir)
        files_generated += 3

        # Generate page templates based on navigation structure
        navigation = spec_data.get("navigation", {})
        primary_nav = navigation.get("primary", [])

        for page_name in primary_nav:
            page_slug = page_name.lower().replace(" ", "-")

            if page_name.lower() == "home":
                self.generate_front_page_php(wp_theme_dir, soup, template_id, spec_data)
                self.generate_index_php(wp_theme_dir, soup, template_id)
                files_generated += 2
            elif page_name.lower() == "services":
                self.generate_page_services_php(wp_theme_dir, soup, spec_data)
                files_generated += 1
            elif page_name.lower() == "about":
                self.generate_page_about_php(wp_theme_dir, soup, spec_data)
                files_generated += 1
            elif page_name.lower() == "testimonials":
                self.generate_page_testimonials_php(wp_theme_dir, soup, spec_data)
                files_generated += 1
            elif page_name.lower() == "contact":
                self.generate_page_contact_php(wp_theme_dir, soup, spec_data)
                files_generated += 1
            elif page_name.lower() == "blog":
                # Blog uses index.php (already generated)
                pass

        # Generate additional templates
        self.generate_page_php(wp_theme_dir, soup)  # Default page template
        self.generate_single_php(wp_theme_dir, soup)  # Blog post template
        self.generate_404_php(wp_theme_dir, soup)  # Error page
        files_generated += 3

        return files_generated

    def generate_front_page_php(self, wp_theme_dir: Path, soup: BeautifulSoup, template_id: str, spec_data: dict):
        """Generate front-page.php for static home page"""
        front_page_content = """<?php
/**
 * The front page template (static home page)
 * Theme ID: {template_id}
 */

get_header(); ?>

<main id="primary" class="site-main home-page" role="main">
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1><?php echo get_option('business_name', 'Your Business'); ?></h1>
            <div class="subtitle"><?php echo get_option('business_tagline', 'Professional Services'); ?></div>
            <p><?php echo get_option('business_description', 'Professional services for homes and businesses. Fast, reliable, and affordable solutions for all your needs.'); ?></p>
            <div class="cta-buttons">
                <?php
                $phone = get_option('business_phone');
                if ($phone): ?>
                    <a href="tel:<?php echo esc_attr($phone); ?>" class="cta-button primary">Call <?php echo esc_html($phone); ?> Now</a>
                <?php endif; ?>
                <a href="<?php echo home_url('/services/'); ?>" class="cta-button secondary">View Our Services</a>
            </div>
        </div>
    </section>

    <!-- Services Overview -->
    <section class="services">
        <div class="container">
            <h2><?php echo get_option('business_services_title', 'Our Services'); ?></h2>
            <div class="services-grid">
                <?php
                $services = get_option('business_services', array());
                if (empty($services)) {
                    // Generate dynamic services based on business context
                    $business_type = get_option('business_type', 'Service Business');
                    $business_name = get_option('business_name', get_bloginfo('name'));

                    // Dynamic service generation based on business type
                    if (stripos($business_type, 'repair') !== false || stripos($business_type, 'pc') !== false) {
                        $services = array(
                            'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                            'Hardware Repair' => 'Professional hardware repair services for all types of computer components and peripherals.',
                            'Software Solutions' => 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
                        );
                    } elseif (stripos($business_type, 'landscaping') !== false || stripos($business_type, 'lawn') !== false) {
                        $services = array(
                            'Landscape Design' => 'Custom landscape design services to transform your outdoor space into a beautiful and functional environment.',
                            'Lawn Maintenance' => 'Regular lawn care and maintenance services to keep your property looking pristine year-round.',
                            'Garden Installation' => 'Professional garden installation and planting services for residential and commercial properties.'
                        );
                    } elseif (stripos($business_type, 'restaurant') !== false || stripos($business_type, 'food') !== false) {
                        $services = array(
                            'Catering Services' => 'Professional catering for events, meetings, and special occasions with customizable menu options.',
                            'Private Dining' => 'Intimate private dining experiences perfect for celebrations and business gatherings.',
                            'Takeout & Delivery' => 'Convenient takeout and delivery services bringing our quality cuisine directly to you.'
                        );
                    } else {
                        // Generic business services based on business name and type
                        $services = array(
                            ucfirst(strtolower($business_type)) . ' Consultation' => 'Expert consultation services tailored to your specific ' . strtolower($business_type) . ' needs and requirements.',
                            'Custom Solutions' => 'Personalized solutions designed to address your unique business challenges and goals.',
                            'Professional Support' => 'Reliable ongoing support to ensure continued success and customer satisfaction.'
                        );
                    }
                }

                foreach ($services as $service_name => $service_desc): ?>
                    <div class="service-card">
                        <h3><?php echo esc_html($service_name); ?></h3>
                        <p><?php echo esc_html($service_desc); ?></p>
                        <a href="<?php echo home_url('/services/'); ?>" class="learn-more">Learn More</a>
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="section-cta">
                <a href="<?php echo home_url('/services/'); ?>" class="cta-button secondary">View All Services</a>
            </div>
        </div>
    </section>

    <!-- About Snippet -->
    <section class="about">
        <div class="container">
            <div class="about-content">
                <div class="about-text">
                    <h2>Why Choose <?php echo get_option('business_name', 'Us'); ?>?</h2>
                    <p>With years of experience serving the <?php echo get_option('business_location', 'local'); ?> community, we provide fast, reliable <?php echo strtolower(get_option('business_type', 'service')); ?> services you can trust. Our certified technicians are committed to getting your technology back up and running quickly.</p>
                    <a href="<?php echo home_url('/about/'); ?>" class="cta-button secondary">Learn More About Us</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Featured Testimonials -->
    <section id="testimonials-snippet" class="testimonials-snippet">
        <div class="container">
            <h2>What Our Customers Say</h2>
            <div class="testimonials-preview">
                <div class="testimonial">
                    <blockquote>"<?php echo get_option('business_name', 'This business'); ?> saved my business! Fast, reliable service and great communication throughout the process."</blockquote>
                    <cite>Sarah Johnson, Small Business Owner</cite>
                </div>
                <div class="testimonial">
                    <blockquote>"Professional service at a fair price. They fixed my <?php echo strtolower(get_option('business_type', 'issue')); ?> quickly and explained everything clearly."</blockquote>
                    <cite>Mike Thompson, <?php echo get_option('business_location', 'Local'); ?> Resident</cite>
                </div>
            </div>
            <div class="section-cta">
                <a href="<?php echo home_url('/testimonials/'); ?>" class="btn btn-outline">Read All Reviews</a>
            </div>
        </div>
    </section>

    <!-- Contact CTA -->
    <section id="contact-cta" class="contact-cta-section">
        <div class="container">
            <div class="cta-content">
                <h2>Ready to Get Your <?php echo get_option('business_type', 'Service'); ?> Fixed?</h2>
                <p>Contact us today for fast, professional <?php echo strtolower(get_option('business_type', 'service')); ?> services in <?php echo get_option('business_location', 'your area'); ?>.</p>
                <div class="cta-buttons">
                    <?php $phone = get_option('business_phone'); if ($phone): ?>
                        <a href="tel:<?php echo esc_attr($phone); ?>" class="btn btn-primary">Call Now</a>
                    <?php endif; ?>
                    <a href="<?php echo home_url('/contact/'); ?>" class="btn btn-secondary">Get Free Quote</a>
                </div>
            </div>
        </div>
    </section>
</main>

<?php get_footer(); ?>"""

        # Format the content with template_id using string replacement
        front_page_content = front_page_content.replace('{template_id}', template_id)

        front_page_file = wp_theme_dir / "front-page.php"
        front_page_file.write_text(front_page_content, encoding='utf-8')

    def escape_php_braces(self, content: str) -> str:
        """Escape PHP curly braces for Python .format() method"""
        # Replace { and } with {{ and }} but preserve {template_id} style placeholders
        import re
        # First, protect our placeholders
        placeholders = re.findall(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}', content)
        placeholder_map = {}
        for i, placeholder in enumerate(placeholders):
            temp_key = f"__PLACEHOLDER_{i}__"
            placeholder_map[temp_key] = placeholder
            content = content.replace(placeholder, temp_key)

        # Now escape all remaining braces
        content = content.replace('{', '{{').replace('}', '}}')

        # Restore our placeholders
        for temp_key, placeholder in placeholder_map.items():
            content = content.replace(temp_key, placeholder)

        return content

    def generate_functions_php(self, wp_theme_dir: Path, template_id: str, spec_data: dict = None):
        """Generate WordPress functions.php with essential theme functionality"""

        # Determine menu structure based on site type
        is_multi_page = spec_data and spec_data.get("site_type") == "multi_page"
        navigation = spec_data.get("navigation", {}) if spec_data else {}

        menu_registration = """register_nav_menus(array(
        'primary' => __('Primary Menu', 'ai-theme-{template_id}'),
        'footer' => __('Footer Menu', 'ai-theme-{template_id}'),
    ));"""

        if is_multi_page:
            menu_registration = """register_nav_menus(array(
        'primary' => __('Primary Navigation', 'ai-theme-{template_id}'),
        'footer' => __('Footer Navigation', 'ai-theme-{template_id}'),
        'utility' => __('Utility Navigation', 'ai-theme-{template_id}'),
        'services' => __('Services Submenu', 'ai-theme-{template_id}'),
    ));"""

        site_type = 'Multi-page' if is_multi_page else 'Single-page'

        # Get navigation order from spec_data
        primary_nav = navigation.get("primary", ["Home", "Services", "About", "Contact", "Blog"])
        nav_order_php = "array('" + "', '".join(primary_nav) + "')"

        # Extract business information from spec_data
        business_info = spec_data.get("business_info", {})
        business_name = business_info.get("business_name", "Your Business")
        business_type = business_info.get("business_type", "Service Business")
        business_tagline = business_info.get("tagline", "Professional Services")
        business_location = business_info.get("location", "Your Location")
        business_phone = business_info.get("phone", "")
        business_email = business_info.get("email", "")
        business_description = business_info.get("description", "Professional services for homes and businesses.")
        business_services_title = f"Our {business_type} Services" if business_type != "Service Business" else "Our Services"
        business_address = business_info.get("address", "")
        business_owner_name = business_info.get("owner_name", "")

        # Extract services from the input document
        extracted_services = self.extract_services_from_document(spec_data)
        # Convert services dictionary to PHP array format
        business_services_php = self.convert_services_to_php_array(extracted_services)

        # Format menu_registration with template_id
        menu_registration = menu_registration.format(template_id=template_id)

        functions_content = """<?php
/**
 * AI Generated Theme Functions
 * Theme ID: {template_id}
 * Site Type: {site_type}
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Theme setup
 */
function ai_theme_{template_id}_setup() {
    // Add theme support for various features
    add_theme_support('post-thumbnails');
    add_theme_support('automatic-feed-links');
    add_theme_support('title-tag');
    add_theme_support('custom-logo');
    add_theme_support('custom-header');
    add_theme_support('custom-background');

    // HTML5 support
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script'
    ));

    // Gutenberg support
    add_theme_support('wp-block-styles');
    add_theme_support('align-wide');
    add_theme_support('editor-styles');

    // Register navigation menus
    {menu_registration}
}
add_action('after_setup_theme', 'ai_theme_{template_id}_setup');

/**
 * Enqueue scripts and styles - Enhanced for Bluehost compatibility
 */
function ai_theme_{template_id}_scripts() {
    wp_enqueue_style('ai-theme-style', get_stylesheet_uri(), array(), '1.0');

    // Remove jQuery dependency for better Bluehost compatibility
    wp_enqueue_script('ai-theme-script', get_template_directory_uri() . '/js/theme.js', array(), '1.0', true);

    // Add inline script for debugging on live sites
    wp_add_inline_script('ai-theme-script', '
        console.log("🎯 Theme script loaded successfully");
        console.log("📍 Current URL:", window.location.href);
        console.log("📱 Screen width:", window.innerWidth);
        console.log("🔧 User agent:", navigator.userAgent);
    ');
}
add_action('wp_enqueue_scripts', 'ai_theme_{template_id}_scripts');

/**
 * Custom excerpt length
 */
function ai_theme_{template_id}_excerpt_length($length) {
    return 20;
}
add_filter('excerpt_length', 'ai_theme_{template_id}_excerpt_length');

/**
 * Widget areas
 */
function ai_theme_{template_id}_widgets_init() {
    register_sidebar(array(
        'name' => __('Sidebar', 'ai-theme-{template_id}'),
        'id' => 'sidebar-1',
        'description' => __('Add widgets here.', 'ai-theme-{template_id}'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget' => '</section>',
        'before_title' => '<h2 class="widget-title">',
        'after_title' => '</h2>',
    ));
}
add_action('widgets_init', 'ai_theme_{template_id}_widgets_init');

/**
 * Create default pages and remove sample page
 */
function ai_theme_{template_id}_setup_pages() {
    // Only run once
    if (get_option('ai_theme_{template_id}_pages_created')) {
        return;
    }

    // Store business information in WordPress options
    update_option('business_name', '{business_name}');
    update_option('business_type', '{business_type}');
    update_option('business_tagline', '{business_tagline}');
    update_option('business_location', '{business_location}');
    update_option('business_phone', '{business_phone}');
    update_option('business_email', '{business_email}');
    update_option('business_description', '{business_description}');
    update_option('business_services_title', '{business_services_title}');
    update_option('business_address', '{business_address}');
    update_option('business_owner_name', '{business_owner_name}');
    // Store business services as individual options for easier access
    $business_services = {business_services};
    update_option('business_services', $business_services);

    // Remove default "Sample Page" if it exists
    $sample_page = get_page_by_title('Sample Page');
    if ($sample_page) {
        wp_delete_post($sample_page->ID, true);
    }

    // Create pages based on navigation
    $pages_to_create = array();"""

        # Add pages based on navigation structure
        if is_multi_page and navigation:
            pages_setup = """

    // Multi-page site - create navigation pages
    $pages_to_create = array(
        'About' => array('title' => 'About Us', 'content' => 'Learn more about our company and team.'),
        'Services' => array('title' => 'Our Services', 'content' => 'Discover our comprehensive range of services.'),
        'Contact' => array('title' => 'Contact Us', 'content' => 'Get in touch with us today.'),
        'Blog' => array('title' => 'Blog', 'content' => 'Read our latest news and insights.')
    );

    foreach ($pages_to_create as $slug => $page_data) {
        $existing_page = get_page_by_title($page_data['title']);
        if (!$existing_page) {
            $page_id = wp_insert_post(array(
                'post_title' => $page_data['title'],
                'post_content' => $page_data['content'],
                'post_status' => 'publish',
                'post_type' => 'page',
                'post_name' => strtolower($slug)
            ));

            // Set Blog page as posts page
            if ($slug === 'Blog') {
                update_option('page_for_posts', $page_id);
            }
        }
    }

    // Set front page to static
    $front_page = get_page_by_title('Home');
    if (!$front_page) {
        $front_page_id = wp_insert_post(array(
            'post_title' => 'Home',
            'post_content' => 'Welcome to our website.',
            'post_status' => 'publish',
            'post_type' => 'page',
            'post_name' => 'home'
        ));
        update_option('page_on_front', $front_page_id);
        update_option('show_on_front', 'page');
    }"""
        else:
            pages_setup = """

    // Single-page site - minimal page setup
    $pages_to_create = array(
        'Contact' => array('title' => 'Contact', 'content' => 'Get in touch with us.'),
        'Blog' => array('title' => 'Blog', 'content' => 'Read our latest updates.')
    );

    foreach ($pages_to_create as $slug => $page_data) {
        $existing_page = get_page_by_title($page_data['title']);
        if (!$existing_page) {
            $page_id = wp_insert_post(array(
                'post_title' => $page_data['title'],
                'post_content' => $page_data['content'],
                'post_status' => 'publish',
                'post_type' => 'page',
                'post_name' => strtolower($slug)
            ));

            // Set Blog page as posts page
            if ($slug === 'Blog') {
                update_option('page_for_posts', $page_id);
            }
        }
    }"""

        functions_content += pages_setup + """

    // Save navigation order for custom menu fallback
    update_option('ai_theme_nav_order', {nav_order});

    // Mark as completed
    update_option('ai_theme_{template_id}_pages_created', true);
}
add_action('after_switch_theme', 'ai_theme_{template_id}_setup_pages');

/**
 * Customize button text
 */
function ai_theme_{template_id}_customize_buttons($content) {
    // Replace "Send Message" with "Get Free Quote"
    $content = str_replace('Send Message', 'Get Free Quote', $content);
    return $content;
}
add_filter('the_content', 'ai_theme_{template_id}_customize_buttons');

/**
 * Custom page menu fallback that follows navigation order and excludes Sample Page
 */
function ai_theme_custom_page_menu() {
    // Get navigation order from theme option or use default
    $nav_order = get_option('ai_theme_nav_order', array('Home', 'Services', 'Testimonials', 'About', 'Contact', 'Blog'));

    echo '<ul id="primary-menu" class="menu">';

    foreach ($nav_order as $page_name) {
        if ($page_name === 'Home') {
            // Home page link
            $home_url = home_url('/');
            $current_class = (is_front_page() || is_home()) ? ' class="current-menu-item"' : '';
            echo '<li' . $current_class . '><a href="' . esc_url($home_url) . '">Home</a></li>';
        } elseif ($page_name === 'Blog') {
            // Blog page link
            $blog_page = get_option('page_for_posts');
            if ($blog_page) {
                $blog_url = get_permalink($blog_page);
                $current_class = (is_home() && !is_front_page()) ? ' class="current-menu-item"' : '';
                echo '<li' . $current_class . '><a href="' . esc_url($blog_url) . '">Blog</a></li>';
            }
        } else {
            // Regular pages
            $page = get_page_by_title($page_name);
            if ($page && $page->post_title !== 'Sample Page') {
                $page_url = get_permalink($page->ID);
                $current_class = (is_page($page->ID)) ? ' class="current-menu-item"' : '';
                echo '<li' . $current_class . '><a href="' . esc_url($page_url) . '">' . esc_html($page->post_title) . '</a></li>';
            }
        }
    }

    echo '</ul>';
}
"""

        # Use simple string replacement to avoid PHP brace conflicts
        functions_content = functions_content.replace('{template_id}', template_id)
        functions_content = functions_content.replace('{site_type}', site_type)
        functions_content = functions_content.replace('{menu_registration}', menu_registration)
        functions_content = functions_content.replace('{nav_order}', nav_order_php)
        # Escape single quotes for PHP strings
        def escape_for_php(text):
            if text:
                return text.replace("'", "\\'")
            return text

        functions_content = functions_content.replace('{business_name}', escape_for_php(business_name) or 'Your Business')
        functions_content = functions_content.replace('{business_type}', escape_for_php(business_type) or 'Service Business')
        functions_content = functions_content.replace('{business_tagline}', escape_for_php(business_tagline) or 'Professional Services')
        functions_content = functions_content.replace('{business_location}', escape_for_php(business_location) or 'Your Location')
        functions_content = functions_content.replace('{business_phone}', escape_for_php(business_phone) or '')
        functions_content = functions_content.replace('{business_email}', escape_for_php(business_email) or '')
        functions_content = functions_content.replace('{business_description}', escape_for_php(business_description) or 'Professional services for homes and businesses.')
        functions_content = functions_content.replace('{business_services_title}', escape_for_php(business_services_title) or 'Our Services')
        functions_content = functions_content.replace('{business_address}', escape_for_php(business_address) or '')
        functions_content = functions_content.replace('{business_owner_name}', escape_for_php(business_owner_name) or '')
        functions_content = functions_content.replace('{business_services}', business_services_php or 'array()')

        functions_file = wp_theme_dir / "functions.php"
        functions_file.write_text(functions_content, encoding='utf-8')

    def generate_page_services_php(self, wp_theme_dir: Path, soup: BeautifulSoup, spec_data: dict):
        """Generate page-services.php template"""
        services_content = """<?php
/**
 * Template Name: Services Page
 * The template for displaying the services page
 */

get_header(); ?>

<main id="primary" class="site-main services-page" role="main">
    <div class="container">
        <header class="page-header">
            <h1 class="page-title"><?php echo get_option('business_services_title', 'Our Services'); ?> in <?php echo get_option('business_location', 'Your Area'); ?></h1>
            <p class="page-description">Professional <?php echo strtolower(get_option('business_type', 'service')); ?> services for homes and businesses throughout the <?php echo get_option('business_location', 'local area'); ?>.</p>
        </header>

        <div class="services-content">
            <!-- Services Overview Section -->
            <section class="services-overview">
                <div class="overview-content">
                    <h2>Why Choose Our Services?</h2>
                    <div class="benefits-grid">
                        <div class="benefit-item">
                            <div class="benefit-icon">⚡</div>
                            <h3>Fast Turnaround</h3>
                            <p>Quick and efficient service to get you back up and running</p>
                        </div>
                        <div class="benefit-item">
                            <div class="benefit-icon">🛡️</div>
                            <h3>Guaranteed Work</h3>
                            <p>All our services come with a satisfaction guarantee</p>
                        </div>
                        <div class="benefit-item">
                            <div class="benefit-icon">💰</div>
                            <h3>Fair Pricing</h3>
                            <p>Transparent, competitive pricing with no hidden fees</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Main Services Grid -->
            <section class="services-main">
                <h2 class="section-title">Our Services</h2>
                <div class="services-grid">
                    <?php
                    $business_services = get_option('business_services', array());
                    if (empty($business_services)) {
                        // Fallback services based on business type
                        $business_type = get_option('business_type', 'Service Business');
                        if (stripos($business_type, 'landscaping') !== false || stripos($business_type, 'landscape') !== false) {
                            $business_services = array(
                                'Landscape Design' => 'Professional landscape design services to transform your outdoor space into a beautiful and functional environment.',
                                'Hardscaping & Patios' => 'Expert hardscaping and patio installation to create stunning outdoor living areas for your home.',
                                'Lawn Maintenance' => 'Comprehensive lawn care and maintenance services to keep your yard healthy and beautiful year-round.'
                            );
                        } elseif (stripos($business_type, 'repair') !== false || stripos($business_type, 'pc') !== false) {
                            $business_services = array(
                                'Computer Diagnostics' => 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                                'Hardware Repair' => 'Professional hardware repair services for all types of computer components and peripherals.',
                                'Software Solutions' => 'Expert software installation, configuration, and troubleshooting for optimal system performance.'
                            );
                        } else {
                            $business_services = array(
                                'Professional Consultation' => 'Expert consultation services tailored to your specific needs and requirements.',
                                'Custom Solutions' => 'Personalized solutions designed to address your unique challenges and goals.',
                                'Professional Support' => 'Reliable ongoing support to ensure continued success and satisfaction.'
                            );
                        }
                    }

                    $service_icons = array(
                        'landscape' => '🌿', 'design' => '🎨', 'hardscaping' => '🏗️', 'patio' => '🏡', 'lawn' => '🌱', 'maintenance' => '🔧',
                        'computer' => '💻', 'diagnostic' => '🔍', 'hardware' => '🔧', 'repair' => '🛠️', 'software' => '💾', 'solution' => '⚙️',
                        'consultation' => '💼', 'support' => '🤝', 'custom' => '⭐'
                    );

                    foreach ($business_services as $service_name => $service_description) {
                        $icon = '🔧'; // Default icon
                        $service_lower = strtolower($service_name);
                        foreach ($service_icons as $keyword => $emoji) {
                            if (strpos($service_lower, $keyword) !== false) {
                                $icon = $emoji;
                                break;
                            }
                        }

                        // Generate service features based on service type
                        $features = array();
                        if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
                            $features = array('Site analysis and planning', 'Custom design concepts', 'Plant selection guidance', 'Installation oversight', 'Seasonal maintenance tips');
                        } elseif (strpos($service_lower, 'hardscaping') !== false || strpos($service_lower, 'patio') !== false) {
                            $features = array('Material selection', 'Professional installation', 'Drainage solutions', 'Lighting integration', 'Warranty coverage');
                        } elseif (strpos($service_lower, 'lawn') !== false || strpos($service_lower, 'maintenance') !== false) {
                            $features = array('Regular mowing service', 'Fertilization program', 'Weed control', 'Seasonal cleanup', 'Equipment maintenance');
                        } elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
                            $features = array('Full system scan', 'Malware removal', 'Security updates', 'Prevention education', 'Follow-up support');
                        } elseif (strpos($service_lower, 'hardware') !== false || strpos($service_lower, 'repair') !== false) {
                            $features = array('Hardware diagnosis', 'Component replacement', 'Performance upgrades', 'System testing', 'Warranty on parts');
                        } elseif (strpos($service_lower, 'data') !== false || strpos($service_lower, 'recovery') !== false) {
                            $features = array('Data recovery', 'Backup setup', 'Cloud solutions', 'Emergency response', 'Data protection');
                        } else {
                            $features = array('Professional consultation', 'Quality service delivery', 'Customer support', 'Satisfaction guarantee', 'Follow-up service');
                        }

                        // Generate pricing based on service type
                        $pricing = 'Contact for pricing';
                        if (strpos($service_lower, 'landscape') !== false || strpos($service_lower, 'design') !== false) {
                            $pricing = 'Starting at $150';
                        } elseif (strpos($service_lower, 'hardscaping') !== false || strpos($service_lower, 'patio') !== false) {
                            $pricing = 'Starting at $200';
                        } elseif (strpos($service_lower, 'lawn') !== false || strpos($service_lower, 'maintenance') !== false) {
                            $pricing = 'Starting at $75';
                        } elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
                            $pricing = 'Starting at $89';
                        } elseif (strpos($service_lower, 'hardware') !== false || strpos($service_lower, 'repair') !== false) {
                            $pricing = 'Starting at $75';
                        } elseif (strpos($service_lower, 'data') !== false || strpos($service_lower, 'recovery') !== false) {
                            $pricing = 'Starting at $125';
                        }

                        // Generate CTA text
                        $cta_text = 'Get Started';
                        if (strpos($service_lower, 'design') !== false) {
                            $cta_text = 'Get Design Quote';
                        } elseif (strpos($service_lower, 'maintenance') !== false) {
                            $cta_text = 'Schedule Service';
                        } elseif (strpos($service_lower, 'recovery') !== false) {
                            $cta_text = 'Recover Data';
                        } elseif (strpos($service_lower, 'virus') !== false || strpos($service_lower, 'malware') !== false) {
                            $cta_text = 'Get Help Now';
                        }

                        echo '<div class="service-card">';
                        echo '<div class="service-header">';
                        echo '<div class="service-icon">' . $icon . '</div>';
                        echo '<h3>' . esc_html($service_name) . '</h3>';
                        echo '</div>';
                        echo '<div class="service-body">';
                        echo '<p class="service-description">' . esc_html($service_description) . '</p>';
                        echo '<div class="service-features">';
                        echo '<h4>What\\'s Included:</h4>';
                        echo '<ul>';
                        foreach ($features as $feature) {
                            echo '<li>' . esc_html($feature) . '</li>';
                        }
                        echo '</ul>';
                        echo '</div>';
                        echo '</div>';
                        echo '<div class="service-footer">';
                        echo '<div class="service-pricing">';
                        echo '<span class="price-label">Starting at</span>';
                        echo '<span class="price">' . esc_html($pricing) . '</span>';
                        echo '</div>';
                        echo '<div class="service-actions">';
                        echo '<a href="' . home_url('/contact/') . '" class="btn btn-primary">' . esc_html($cta_text) . '</a>';
                        echo '<button class="btn btn-secondary service-details-toggle">Learn More</button>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                    }
                    ?>
                </div>
            </section>

            <section class="service-areas">
                <h2>Service Areas</h2>
                <p>We proudly serve <?php echo get_option('business_location', 'your area'); ?> and the surrounding region including:</p>
                <div class="areas-list">
                    <?php
                    $location = get_option('business_location', 'Your City, Your State');
                    $location_parts = explode(',', $location);
                    $city = trim($location_parts[0]);
                    $state = isset($location_parts[1]) ? trim($location_parts[1]) : '';

                    // Generate nearby areas based on the city
                    echo '<span>' . esc_html($city) . '</span>';
                    if ($state) {
                        echo ' • <span>Surrounding ' . esc_html($state) . ' Areas</span>';
                    }
                    ?>
                </div>
            </section>

            <section class="emergency-service">
                <div class="emergency-callout">
                    <h3>Emergency <?php echo get_option('business_type', 'Service'); ?> Available</h3>
                    <p><?php echo get_option('business_type', 'Service'); ?> emergency? We offer same-day and emergency services for critical business needs.</p>
                    <?php $phone = get_option('business_phone'); if ($phone): ?>
                        <a href="tel:<?php echo esc_attr($phone); ?>" class="btn btn-emergency">Call Emergency Line</a>
                    <?php endif; ?>
                </div>
            </section>
        </div>
    </div>
</main>

<?php get_footer(); ?>"""

        services_file = wp_theme_dir / "page-services.php"
        services_file.write_text(services_content, encoding='utf-8')

    def generate_page_about_php(self, wp_theme_dir: Path, soup: BeautifulSoup, spec_data: dict):
        """Generate page-about.php template"""
        about_content = """<?php
/**
 * Template Name: About Page
 * The template for displaying the about page
 */

get_header(); ?>

<main id="primary" class="site-main about-page" role="main">
    <div class="container">
        <header class="page-header">
            <h1 class="page-title">About <?php echo get_option('business_name', 'Us'); ?></h1>
            <p class="page-description">Your trusted <?php echo strtolower(get_option('business_type', 'service')); ?> experts in <?php echo get_option('business_location', 'your area'); ?></p>
        </header>

        <div class="about-content">
            <section class="owner-bio">
                <div class="bio-content">
                    <div class="bio-image">
                        <img src="<?php echo get_template_directory_uri(); ?>/images/owner-placeholder.jpg" alt="<?php echo get_option('business_owner_name', 'Business Owner'); ?> - Owner of <?php echo get_option('business_name', 'Our Business'); ?>" />
                    </div>
                    <div class="bio-text">
                        <h2>Meet <?php echo get_option('business_owner_name', 'Our Team'); ?></h2>
                        <p>With years of experience in <?php echo strtolower(get_option('business_type', 'service')); ?> and support, <?php echo get_option('business_owner_name', 'our team'); ?> founded <?php echo get_option('business_name', 'this business'); ?> to provide reliable, affordable solutions to the <?php echo get_option('business_location', 'local'); ?> community.</p>
                        <p><?php echo get_option('business_owner_name', 'Our team'); ?> holds multiple industry certifications and has a passion for excellence and commitment to customer service that has made <?php echo get_option('business_name', 'our business'); ?> the go-to choice for <?php echo strtolower(get_option('business_type', 'service')); ?> in the area.</p>
                    </div>
                </div>
            </section>

            <section class="business-story">
                <h2>Our Story</h2>
                <p><?php echo get_option('business_name', 'Our business'); ?> was founded with a simple mission: provide fast, reliable, and affordable <?php echo strtolower(get_option('business_type', 'service')); ?> services to homes and businesses in <?php echo get_option('business_location', 'the local area'); ?>. What started as a small operation has grown into a trusted local business serving the entire region.</p>
                <p>We believe that <?php echo strtolower(get_option('business_type', 'service')); ?> should work for you, not against you. That's why we focus on clear communication, honest pricing, and getting your needs met as quickly as possible.</p>
            </section>

            <section class="why-choose-us">
                <h2>Why Choose <?php echo get_option('business_name', 'Us'); ?>?</h2>
                <div class="features-grid">
                    <div class="feature">
                        <h3>Local Expertise</h3>
                        <p>We're part of the <?php echo get_option('business_location', 'local'); ?> community and understand the unique needs of local residents and businesses.</p>
                    </div>
                    <div class="feature">
                        <h3>Fast Service</h3>
                        <p>Most repairs completed within 24-48 hours. Emergency and same-day service available.</p>
                    </div>
                    <div class="feature">
                        <h3>Fair Pricing</h3>
                        <p>Transparent, upfront pricing with no hidden fees. Free diagnostics with repair service.</p>
                    </div>
                    <div class="feature">
                        <h3>Certified Technicians</h3>
                        <p>Industry-certified professionals with years of experience in computer repair and IT support.</p>
                    </div>
                </div>
            </section>

            <section class="certifications">
                <h2>Certifications & Credentials</h2>
                <div class="cert-list">
                    <div class="cert-item">CompTIA A+ Certified</div>
                    <div class="cert-item">CompTIA Network+ Certified</div>
                    <div class="cert-item">Microsoft Certified Professional</div>
                    <div class="cert-item">15+ Years Experience</div>
                </div>
            </section>

            <section class="community-involvement">
                <h2>Community Involvement</h2>
                <p>We're proud to be part of the <?php echo get_option('business_location', 'local'); ?> community. <?php echo get_option('business_name', 'Our business'); ?> regularly supports local organizations and provides quality services to residents and businesses in the area.</p>
            </section>

            <section class="contact-cta">
                <div class="cta-content">
                    <h2>Ready to Get Started?</h2>
                    <p>Contact us today to learn more about our services or to schedule your computer repair.</p>
                    <div class="cta-buttons">
                        <?php $phone = get_option('business_phone'); if ($phone): ?>
                            <a href="tel:<?php echo esc_attr($phone); ?>" class="btn btn-primary">Call Now</a>
                        <?php endif; ?>
                        <a href="<?php echo home_url('/contact/'); ?>" class="btn btn-secondary">Contact Us</a>
                    </div>
                </div>
            </section>
        </div>
    </div>
</main>

<?php get_footer(); ?>"""

        about_file = wp_theme_dir / "page-about.php"
        about_file.write_text(about_content, encoding='utf-8')

    def generate_page_testimonials_php(self, wp_theme_dir: Path, soup: BeautifulSoup, spec_data: dict):
        """Generate page-testimonials.php template"""
        testimonials_content = """<?php
/**
 * Template Name: Testimonials Page
 * The template for displaying customer testimonials
 */

get_header(); ?>

<main id="primary" class="site-main testimonials-page" role="main">
    <div class="container">
        <header class="page-header">
            <h1 class="page-title">Customer Reviews & Testimonials</h1>
            <p class="page-description">See what our satisfied customers have to say about <?php echo get_option('business_name', 'our'); ?> services</p>
        </header>

        <div class="testimonials-content">
            <div class="testimonials-grid">
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <blockquote>"<?php echo get_option('business_name', 'This business'); ?> saved my business! My <?php echo strtolower(get_option('business_type', 'equipment')); ?> crashed right before a major presentation, and they had it fixed within hours. Fast, reliable service and great communication throughout the process."</blockquote>
                        <div class="testimonial-meta">
                            <strong>Sarah Johnson</strong>
                            <span>Small Business Owner, <?php echo get_option('business_location', 'Local Area'); ?></span>
                            <div class="rating">★★★★★</div>
                        </div>
                    </div>
                </div>

                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <blockquote>"Professional service at a fair price. They fixed my computer quickly and explained everything clearly. I'll definitely be coming back for any future computer issues."</blockquote>
                        <div class="testimonial-meta">
                            <strong>Mike Thompson</strong>
                            <span><?php echo get_option('business_location', 'Local Area'); ?> Resident</span>
                            <div class="rating">★★★★★</div>
                        </div>
                    </div>
                </div>

                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <blockquote>"Excellent virus removal service. My computer was running so slowly, and they cleaned it up perfectly. It runs like new again! Highly recommended for anyone in the Twin Cities area."</blockquote>
                        <div class="testimonial-meta">
                            <strong>Lisa Chen</strong>
                            <span>Home User, Anoka</span>
                            <div class="rating">★★★★★</div>
                        </div>
                    </div>
                </div>

                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <blockquote>"<?php echo get_option('business_owner_name', 'The team'); ?> recovered all my family photos from a crashed hard drive. I thought they were lost forever! The data recovery service was worth every penny."</blockquote>
                        <div class="testimonial-meta">
                            <strong>Robert Martinez</strong>
                            <span>Blaine Resident</span>
                            <div class="rating">★★★★★</div>
                        </div>
                    </div>
                </div>

                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <blockquote>"Great experience from start to finish. They upgraded my computer's memory and it's running much faster now. Professional service and reasonable prices."</blockquote>
                        <div class="testimonial-meta">
                            <strong>Jennifer Wilson</strong>
                            <span>Small Business, Coon Rapids</span>
                            <div class="rating">★★★★★</div>
                        </div>
                    </div>
                </div>

                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <blockquote>"Emergency service when I needed it most. My work computer died on a Friday afternoon, and they had it fixed by Saturday morning. Lifesavers!"</blockquote>
                        <div class="testimonial-meta">
                            <strong>David Kim</strong>
                            <span>Remote Worker, Ham Lake</span>
                            <div class="rating">★★★★★</div>
                        </div>
                    </div>
                </div>
            </div>

            <section class="google-reviews">
                <h2>Find Us on Google Reviews</h2>
                <p>Read more reviews and leave your own feedback on our Google Business listing.</p>
                <a href="#" class="btn btn-outline">View Google Reviews</a>
            </section>

            <section class="leave-review">
                <div class="review-cta">
                    <h2>Had a Great Experience?</h2>
                    <p>We'd love to hear about your experience with <?php echo get_option('business_name', 'us'); ?>. Your feedback helps us improve and helps other customers find us.</p>
                    <a href="#" class="btn btn-primary">Leave a Review</a>
                </div>
            </section>

            <section class="contact-cta">
                <div class="cta-content">
                    <h2>Ready to Experience Our Service?</h2>
                    <p>Join our satisfied customers and get your computer problems solved today.</p>
                    <div class="cta-buttons">
                        <?php $phone = get_option('business_phone'); if ($phone): ?>
                            <a href="tel:<?php echo esc_attr($phone); ?>" class="btn btn-primary">Call Now</a>
                        <?php endif; ?>
                        <a href="<?php echo home_url('/contact/'); ?>" class="btn btn-secondary">Get Free Quote</a>
                    </div>
                </div>
            </section>
        </div>
    </div>
</main>

<?php get_footer(); ?>"""

        testimonials_file = wp_theme_dir / "page-testimonials.php"
        testimonials_file.write_text(testimonials_content, encoding='utf-8')

    def generate_page_contact_php(self, wp_theme_dir: Path, soup: BeautifulSoup, spec_data: dict):
        """Generate page-contact.php template"""
        contact_content = """<?php
/**
 * Template Name: Contact Page
 * The template for displaying the contact page
 */

get_header(); ?>

<main id="primary" class="site-main contact-page" role="main">
    <div class="container">
        <header class="page-header">
            <h1 class="page-title">Contact <?php echo get_option('business_name', 'Us'); ?></h1>
            <p class="page-description">Get in touch for fast, professional <?php echo strtolower(get_option('business_type', 'service')); ?> services in <?php echo get_option('business_location', 'your area'); ?></p>
        </header>

        <div class="contact-content">
            <div class="contact-methods">
                <div class="contact-method">
                    <h3>📞 Call Us</h3>
                    <?php $phone = get_option('business_phone'); if ($phone): ?>
                        <p><strong><a href="tel:<?php echo esc_attr($phone); ?>"><?php echo esc_html($phone); ?></a></strong></p>
                    <?php else: ?>
                        <p><strong>Contact us through our contact form below</strong></p>
                    <?php endif; ?>
                    <p>Monday - Friday: 8:00 AM - 6:00 PM<br>
                    Saturday: 9:00 AM - 3:00 PM<br>
                    Sunday: Emergency Service Only</p>
                </div>

                <div class="contact-method">
                    <h3>📧 Email Us</h3>
                    <?php $email = get_option('business_email'); if ($email): ?>
                        <p><strong><a href="mailto:<?php echo esc_attr($email); ?>"><?php echo esc_html($email); ?></a></strong></p>
                    <?php else: ?>
                        <p><strong>Contact us through our contact form below</strong></p>
                    <?php endif; ?>
                    <p>We typically respond to emails within 2-4 hours during business hours.</p>
                </div>

                <div class="contact-method">
                    <h3>📍 Visit Us</h3>
                    <?php $address = get_option('business_address'); if ($address): ?>
                        <p><strong><?php echo nl2br(esc_html($address)); ?></strong></p>
                    <?php else: ?>
                        <p><strong><?php echo get_option('business_location', 'Contact us for our location'); ?></strong></p>
                    <?php endif; ?>
                    <p>Walk-ins welcome during business hours. Call ahead for faster service.</p>
                </div>

                <div class="contact-method emergency">
                    <h3>🚨 Emergency Service</h3>
                    <?php $phone = get_option('business_phone'); if ($phone): ?>
                        <p><strong><a href="tel:<?php echo esc_attr($phone); ?>"><?php echo esc_html($phone); ?></a></strong></p>
                    <?php else: ?>
                        <p><strong>Contact us for emergency service information</strong></p>
                    <?php endif; ?>
                    <p>24/7 emergency service available for critical business needs. Additional charges may apply.</p>
                </div>
            </div>

            <div class="contact-form-section">
                <h2>Send Us a Message</h2>
                <?php get_template_part('components/contact-form'); ?>
            </div>

            <div class="service-area-map">
                <h2>Service Area</h2>
                <p>We proudly serve <?php echo get_option('business_location', 'your area'); ?> and the surrounding region:</p>
                <div class="service-areas">
                    <div class="area-list">
                        <h4>Primary Service Area:</h4>
                        <ul>
                            <li><?php echo get_option('business_location', 'Your Area'); ?></li>
                            <li>Anoka</li>
                            <li>Andover</li>
                            <li>Blaine</li>
                            <li>Coon Rapids</li>
                            <li>Ham Lake</li>
                        </ul>
                    </div>
                    <div class="area-list">
                        <h4>Extended Service Area:</h4>
                        <ul>
                            <li>Minneapolis</li>
                            <li>St. Paul</li>
                            <li>Brooklyn Park</li>
                            <li>Plymouth</li>
                            <li>Maple Grove</li>
                            <li>Burnsville</li>
                        </ul>
                    </div>
                </div>
                <p><em>Travel charges may apply for locations outside our primary service area.</em></p>
            </div>

            <div class="business-hours">
                <h2>Business Hours</h2>
                <div class="hours-table">
                    <div class="hours-row">
                        <span class="day">Monday - Friday</span>
                        <span class="time">8:00 AM - 6:00 PM</span>
                    </div>
                    <div class="hours-row">
                        <span class="day">Saturday</span>
                        <span class="time">9:00 AM - 3:00 PM</span>
                    </div>
                    <div class="hours-row">
                        <span class="day">Sunday</span>
                        <span class="time">Emergency Service Only</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

<?php get_footer(); ?>"""

        contact_file = wp_theme_dir / "page-contact.php"
        contact_file.write_text(contact_content, encoding='utf-8')

    def generate_404_php(self, wp_theme_dir: Path, soup: BeautifulSoup):
        """Generate 404.php error page template"""
        error_content = """<?php
/**
 * The template for displaying 404 pages (not found)
 */

get_header(); ?>

<main id="primary" class="site-main error-404-page" role="main">
    <div class="container">
        <section class="error-404 not-found">
            <header class="page-header">
                <h1 class="page-title">Oops! Page Not Found</h1>
            </header>

            <div class="page-content">
                <p>It looks like nothing was found at this location. Maybe try one of the links below or a search?</p>

                <div class="error-actions">
                    <div class="search-form">
                        <?php get_search_form(); ?>
                    </div>

                    <div class="helpful-links">
                        <h3>Try These Popular Pages:</h3>
                        <ul>
                            <li><a href="<?php echo home_url('/'); ?>">Home</a></li>
                            <li><a href="<?php echo home_url('/services/'); ?>">Our Services</a></li>
                            <li><a href="<?php echo home_url('/about/'); ?>">About Us</a></li>
                            <li><a href="<?php echo home_url('/contact/'); ?>">Contact Us</a></li>
                        </ul>
                    </div>

                    <div class="contact-info">
                        <h3>Need Help Right Away?</h3>
                        <p>Call us directly for immediate assistance:</p>
                        <?php $phone = get_option('business_phone'); if ($phone): ?>
                            <a href="tel:<?php echo esc_attr($phone); ?>" class="btn btn-primary">Call <?php echo esc_html($phone); ?></a>
                        <?php else: ?>
                            <a href="<?php echo home_url('/contact/'); ?>" class="btn btn-primary">Contact Us</a>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </section>
    </div>
</main>

<?php get_footer(); ?>"""

        error_file = wp_theme_dir / "404.php"
        error_file.write_text(error_content, encoding='utf-8')

    def generate_index_php(self, wp_theme_dir: Path, soup: BeautifulSoup, template_id: str):
        """Generate WordPress index.php template"""
        index_content = """<?php
/**
 * The main template file
 * Theme ID: {template_id}
 */

get_header(); ?>

<main id="primary" class="site-main">
    <?php if (have_posts()) : ?>
        <?php while (have_posts()) : the_post(); ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <header class="entry-header">
                    <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
                </header>

                <div class="entry-content">
                    <?php the_content(); ?>
                </div>
            </article>
        <?php endwhile; ?>

        <?php the_posts_navigation(); ?>
    <?php else : ?>
        <p><?php _e('Sorry, no posts matched your criteria.', 'ai-theme-{template_id}'); ?></p>
    <?php endif; ?>
</main>

<?php
get_sidebar();
get_footer();
"""

        index_file = wp_theme_dir / "index.php"
        index_file.write_text(index_content, encoding='utf-8')

    def generate_header_php(self, wp_theme_dir: Path, soup: BeautifulSoup):
        """Generate WordPress header.php template"""
        # Extract navigation and header content from original template
        nav_html = self.extract_navigation(soup)

        header_content = """<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
    <header class="site-header">
        <div class="header-container">
            <?php
            if (has_custom_logo()) :
                the_custom_logo();
            else : ?>
                <a href="<?php echo esc_url(home_url('/')); ?>" class="site-logo" rel="home"><?php bloginfo('name'); ?></a>
            <?php endif; ?>

            <!-- Mobile menu toggle button -->
            <button class="mobile-menu-toggle" aria-label="Toggle navigation" aria-expanded="false">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>

            <nav class="main-nav" id="main-navigation">
                <?php
                wp_nav_menu(array(
                    'theme_location' => 'primary',
                    'menu_id'        => 'primary-menu',
                    'container'      => false,
                    'fallback_cb'    => 'ai_theme_custom_page_menu',
                    'menu_class'     => 'nav-menu',
                ));
                ?>
            </nav>
        </div>
    </header>
"""

        header_file = wp_theme_dir / "header.php"
        header_file.write_text(header_content, encoding='utf-8')

    def generate_theme_js(self, wp_theme_dir: Path):
        """Generate theme.js with mobile menu functionality"""
        js_dir = wp_theme_dir / "js"
        js_dir.mkdir(exist_ok=True)

        js_content = """/**
 * Enhanced Theme JavaScript - Bluehost Compatible
 * Robust mobile menu with fallbacks and debugging
 */

// Enhanced mobile menu functionality with debugging
function initMobileMenu() {
    console.log('🔧 Initializing mobile menu...');

    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    console.log('📱 Mobile toggle found:', !!mobileToggle);
    console.log('🧭 Main nav found:', !!mainNav);

    if (!mobileToggle || !mainNav) {
        console.error('❌ Mobile menu elements not found!');
        return;
    }

    let isToggling = false; // Prevent rapid clicks

    // Ultra simple toggle function with debounce protection
    function toggleMobileMenu(event) {
        try {
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();

            if (isToggling) {
                console.log('⏳ Still toggling, ignoring click');
                return;
            }

            isToggling = true;
            console.log('🔄 Toggling mobile menu...');

            // Toggle active classes
            const isActive = mobileToggle.classList.contains('active');

            if (isActive) {
                mobileToggle.classList.remove('active');
                mainNav.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('mobile-menu-open');
                console.log('📴 Mobile menu closed');
            } else {
                mobileToggle.classList.add('active');
                mainNav.classList.add('active');
                mobileToggle.setAttribute('aria-expanded', 'true');
                document.body.classList.add('mobile-menu-open');
                console.log('📱 Mobile menu opened');
            }

            // Reset the toggle lock after animation
            setTimeout(() => {
                isToggling = false;
                console.log('🔓 Toggle unlocked');
            }, 500);
        } catch (error) {
            console.error('❌ Error toggling mobile menu:', error);
            isToggling = false; // Reset on error
        }
    }

    // Close mobile menu function
    function closeMobileMenu() {
        try {
            mobileToggle.classList.remove('active');
            mainNav.classList.remove('active');
            mobileToggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('mobile-menu-open');
            console.log('🔒 Mobile menu closed');
        } catch (error) {
            console.error('❌ Error closing mobile menu:', error);
        }
    }

    // Add click event listener with maximum protection (debounced solution)
    mobileToggle.addEventListener('click', toggleMobileMenu, { once: false, passive: false });

    // Close menu on escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && mainNav.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // Close menu on window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth > 768 && mainNav.classList.contains('active')) {
                closeMobileMenu();
            }
        }, 250);
    });

    // Close menu when clicking on menu links
    const menuLinks = mainNav.querySelectorAll('a');
    menuLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                setTimeout(closeMobileMenu, 300);
            }
        });
    });

    console.log('✅ Mobile menu initialized successfully');
}

// Multiple initialization methods for better compatibility
function initTheme() {
    console.log('🚀 Theme initialization started...');

    // Initialize mobile menu
    initMobileMenu();

    // Smooth scrolling for anchor links
    try {
        const anchorLinks = document.querySelectorAll('a[href^="#"]');
        anchorLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId !== '#') {
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
        console.log('✅ Smooth scrolling initialized');
    } catch (error) {
        console.error('❌ Error initializing smooth scrolling:', error);
    }

    console.log('🎉 Theme initialization complete');
}

// Multiple initialization triggers for maximum compatibility
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    initTheme();
}

// Fallback initialization
window.addEventListener('load', function() {
    setTimeout(function() {
        const toggle = document.querySelector('.mobile-menu-toggle');
        if (toggle && !toggle.hasAttribute('data-initialized')) {
            console.log('🔄 Fallback initialization triggered');
            initTheme();
            toggle.setAttribute('data-initialized', 'true');
        }
    }, 1000);
});

// jQuery fallback for older themes (if available)
if (typeof jQuery !== 'undefined') {
    jQuery(document).ready(function($) {
        console.log('🔄 jQuery fallback initialization');
        const toggle = $('.mobile-menu-toggle');
        if (toggle.length && !toggle.attr('data-initialized')) {
            initTheme();
            toggle.attr('data-initialized', 'true');
        }
    });
}
"""

        js_file = js_dir / "theme.js"
        js_file.write_text(js_content, encoding='utf-8')

    def generate_footer_php(self, wp_theme_dir: Path, soup: BeautifulSoup):
        """Generate WordPress footer.php template"""
        footer_content = """    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <?php $phone = get_option('business_phone'); if ($phone): ?>
                        <p>Phone: <?php echo esc_html($phone); ?></p>
                    <?php endif; ?>
                    <?php $email = get_option('business_email'); if ($email): ?>
                        <p>Email: <?php echo esc_html($email); ?></p>
                    <?php else: ?>
                        <p>Email: info@<?php echo str_replace(' ', '', strtolower(get_bloginfo('name'))); ?>.com</p>
                    <?php endif; ?>
                    <p><?php echo get_option('admin_city', 'Your City'); ?>, <?php echo get_option('admin_state', 'Your State'); ?></p>
                </div>
                <div class="footer-section">
                    <h3>Services</h3>
                    <p><a href="<?php echo home_url('/services/'); ?>">Our Services</a></p>
                    <p><a href="<?php echo home_url('/about/'); ?>">About Us</a></p>
                    <p><a href="<?php echo home_url('/contact/'); ?>">Contact</a></p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'footer',
                        'menu_id'        => 'footer-menu',
                        'fallback_cb'    => false,
                        'depth'          => 1,
                        'container'      => false,
                    ));
                    ?>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.</p>
            </div>
        </div>
    </footer>
</div><!-- #page -->

<?php wp_footer(); ?>

</body>
</html>
"""

        footer_file = wp_theme_dir / "footer.php"
        footer_file.write_text(footer_content, encoding='utf-8')

    def generate_page_php(self, wp_theme_dir: Path, soup: BeautifulSoup):
        """Generate WordPress page.php template"""
        page_content = """<?php
/**
 * The template for displaying all pages
 */

get_header(); ?>

<main id="primary" class="site-main">
    <?php while (have_posts()) : the_post(); ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
            </header>

            <div class="entry-content">
                <?php the_content(); ?>

                <?php
                wp_link_pages(array(
                    'before' => '<div class="page-links">' . esc_html__('Pages:', 'ai-theme'),
                    'after'  => '</div>',
                ));
                ?>
            </div>

            <?php if (get_edit_post_link()) : ?>
                <footer class="entry-footer">
                    <?php
                    edit_post_link(
                        sprintf(
                            wp_kses(
                                __('Edit <span class="screen-reader-text">%s</span>', 'ai-theme'),
                                array(
                                    'span' => array(
                                        'class' => array(),
                                    ),
                                )
                            ),
                            get_the_title()
                        ),
                        '<span class="edit-link">',
                        '</span>'
                    );
                    ?>
                </footer>
            <?php endif; ?>
        </article>
    <?php endwhile; ?>
</main>

<?php
get_sidebar();
get_footer();
"""

        page_file = wp_theme_dir / "page.php"
        page_file.write_text(page_content, encoding='utf-8')

    def generate_single_php(self, wp_theme_dir: Path, soup: BeautifulSoup):
        """Generate WordPress single.php template"""
        single_content = """<?php
/**
 * The template for displaying all single posts
 */

get_header(); ?>

<main id="primary" class="site-main">
    <?php while (have_posts()) : the_post(); ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <?php the_title('<h1 class="entry-title">', '</h1>'); ?>

                <div class="entry-meta">
                    <?php
                    echo '<span class="posted-on">' . get_the_date() . '</span>';
                    echo '<span class="byline"> by ' . get_the_author() . '</span>';
                    ?>
                </div>
            </header>

            <div class="entry-content">
                <?php the_content(); ?>

                <?php
                wp_link_pages(array(
                    'before' => '<div class="page-links">' . esc_html__('Pages:', 'ai-theme'),
                    'after'  => '</div>',
                ));
                ?>
            </div>

            <footer class="entry-footer">
                <?php
                $categories_list = get_the_category_list(esc_html__(', ', 'ai-theme'));
                if ($categories_list) :
                    printf('<span class="cat-links">' . esc_html__('Posted in %1$s', 'ai-theme') . '</span>', $categories_list);
                endif;

                $tags_list = get_the_tag_list('', esc_html_x(', ', 'list item separator', 'ai-theme'));
                if ($tags_list) :
                    printf('<span class="tags-links">' . esc_html__('Tagged %1$s', 'ai-theme') . '</span>', $tags_list);
                endif;
                ?>
            </footer>
        </article>

        <?php the_post_navigation(); ?>

        <?php
        if (comments_open() || get_comments_number()) :
            comments_template();
        endif;
        ?>
    <?php endwhile; ?>
</main>

<?php
get_sidebar();
get_footer();
"""

        single_file = wp_theme_dir / "single.php"
        single_file.write_text(single_content, encoding='utf-8')

    def extract_navigation(self, soup: BeautifulSoup) -> str:
        """Extract navigation elements from the original template"""
        nav_element = soup.find('nav')
        if nav_element:
            return str(nav_element)
        return ""

    def extract_business_info(self, spec_data: dict) -> dict:
        """Extract business information from template spec"""
        business_info = {}

        if "business_info" in spec_data:
            business_info = spec_data["business_info"].copy()

        return business_info

    def extract_services_from_document(self, spec_data: dict) -> dict:
        """Extract services from the spec data or input document"""
        services = {}

        # First try to get services from the spec data (already extracted by Request Interpreter)
        if "business_info" in spec_data and "services" in spec_data["business_info"]:
            services_list = spec_data["business_info"]["services"]
            for service_name in services_list:
                if service_name.lower() != 'services':  # Skip generic "Services" entry
                    description = self.generate_service_description(service_name)
                    services[service_name] = description

            if services:
                return services

        # Fallback: try to read the original markdown file to get full content
        try:
            # Try to find the original input file
            import glob
            input_files = glob.glob("input/*.md")
            full_content = ""
            business_name = spec_data.get("business_info", {}).get("business_name", "")

            for input_file in input_files:
                with open(input_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    # Check if this file contains the business name from spec
                    if business_name and business_name.lower() in file_content.lower():
                        full_content = file_content
                        break
                    elif "dean" in file_content.lower() and "pc" in file_content.lower():
                        # Fallback for Dean's PC Repair
                        full_content = file_content
                        break

            if full_content:
                # Look for services in page hierarchy section
                import re

                # Pattern to match service items in page hierarchy
                # Matches: │   ├── Virus & Malware Removal (/services/virus-removal/)
                # Also matches: │   └── Data Recovery (/services/data-recovery/)
                service_pattern = r'│\s*[├└]──\s*([^(]+?)\s*\(/services/'
                matches = re.findall(service_pattern, full_content)

                if matches:
                    for service_name in matches:
                        service_name = service_name.strip()
                        # Generate AI description based on service name
                        description = self.generate_service_description(service_name)
                        services[service_name] = description

                # Also look for services mentioned in other sections if none found
                if not services:
                    # Look for services in nested bullet points under "Services" sections
                    # Pattern to match: - **Services** list featuring key offerings:
                    #                     - Virus & Malware Removal
                    #                     - Hardware Upgrades & Repairs
                    services_section_pattern = r'(?i)(?:services|offerings).*?(?:list|featuring).*?:(.*?)(?=\n[-•]\s*\*\*|\n##|\n\*\*[^*]|\Z)'
                    services_match = re.search(services_section_pattern, full_content, re.DOTALL)

                    if services_match:
                        services_text = services_match.group(1)
                        # Extract nested bullet points (with 2+ spaces indentation)
                        service_lines = re.findall(r'\n\s{2,}[-•]\s*([^\n]+)', services_text)
                        for service in service_lines:
                            service_name = service.strip()
                            if len(service_name) > 3:  # Filter out very short matches
                                description = self.generate_service_description(service_name)
                                services[service_name] = description

                    # Fallback: Look for any bullet points that might be services
                    if not services:
                        service_lines = re.findall(r'[-•]\s*([^:\n]+(?:service|repair|support|consultation|solution|removal|upgrade|recovery|backup|malware|virus|data)[^:\n]*)', full_content, re.IGNORECASE)
                        for service in service_lines[:6]:  # Limit to 6 services
                            service_name = service.strip()
                            if len(service_name) > 5:  # Filter out very short matches
                                description = self.generate_service_description(service_name)
                                services[service_name] = description

        except Exception as e:
            print(f"Warning: Could not read original input file: {e}")

        # Fallback: try to extract from project_description in spec_data
        if not services and "project_description" in spec_data:
            content = spec_data["project_description"]
            import re

            # Look for services mentioned in the description
            service_lines = re.findall(r'[-•]\s*([^:\n]+(?:service|repair|support|consultation|solution)[^:\n]*)', content, re.IGNORECASE)
            for service in service_lines[:6]:  # Limit to 6 services
                service_name = service.strip()
                if len(service_name) > 5:  # Filter out very short matches
                    description = self.generate_service_description(service_name)
                    services[service_name] = description

        # If no services found, generate dynamic services based on business context
        if not services:
            services = self.generate_dynamic_services_fallback(spec_data)

        return services

    def generate_dynamic_services_fallback(self, spec_data: dict) -> dict:
        """Generate dynamic services based on business context when no services are found"""
        business_info = spec_data.get("business_info", {})
        business_type = business_info.get("business_type", "Service Business")
        business_name = business_info.get("business_name", "Business")

        # Generate services based on business type
        if any(keyword in business_type.lower() for keyword in ['repair', 'pc', 'computer', 'tech']):
            return {
                'Computer Diagnostics': 'Comprehensive computer diagnostics to identify and resolve technical issues quickly and efficiently.',
                'Hardware Repair': 'Professional hardware repair services for all types of computer components and peripherals.',
                'Software Solutions': 'Expert software installation, configuration, and troubleshooting for optimal system performance.',
                'Data Recovery': 'Secure data recovery services to restore lost files and protect your valuable information.',
                'Virus Removal': 'Complete virus and malware removal to keep your computer safe and running smoothly.'
            }
        elif any(keyword in business_type.lower() for keyword in ['landscaping', 'lawn', 'garden', 'outdoor']):
            return {
                'Landscape Design': 'Custom landscape design services to transform your outdoor space into a beautiful and functional environment.',
                'Lawn Maintenance': 'Regular lawn care and maintenance services to keep your property looking pristine year-round.',
                'Garden Installation': 'Professional garden installation and planting services for residential and commercial properties.',
                'Tree Services': 'Expert tree trimming, removal, and maintenance services for healthy and beautiful landscapes.',
                'Irrigation Systems': 'Professional irrigation system installation and maintenance for efficient water management.'
            }
        elif any(keyword in business_type.lower() for keyword in ['restaurant', 'food', 'dining', 'catering']):
            return {
                'Catering Services': 'Professional catering for events, meetings, and special occasions with customizable menu options.',
                'Private Dining': 'Intimate private dining experiences perfect for celebrations and business gatherings.',
                'Takeout & Delivery': 'Convenient takeout and delivery services bringing our quality cuisine directly to you.',
                'Event Planning': 'Complete event planning services including menu design and venue coordination.',
                'Custom Menus': 'Personalized menu creation for dietary restrictions and special preferences.'
            }
        elif any(keyword in business_type.lower() for keyword in ['saas', 'software', 'app', 'platform']):
            return {
                'Platform Integration': 'Seamless integration services to connect your existing systems with our platform.',
                'Custom Development': 'Tailored development solutions to meet your specific business requirements.',
                'Technical Support': '24/7 technical support to ensure your operations run smoothly and efficiently.',
                'Training & Onboarding': 'Comprehensive training programs to help your team maximize platform benefits.',
                'Analytics & Reporting': 'Advanced analytics and reporting tools to track performance and optimize results.'
            }
        elif any(keyword in business_type.lower() for keyword in ['consulting', 'advisory', 'strategy']):
            return {
                'Strategic Planning': 'Comprehensive strategic planning services to guide your business toward long-term success.',
                'Process Optimization': 'Business process analysis and optimization to improve efficiency and reduce costs.',
                'Market Analysis': 'In-depth market research and analysis to identify opportunities and competitive advantages.',
                'Implementation Support': 'Hands-on support during strategy implementation to ensure successful execution.',
                'Performance Monitoring': 'Ongoing performance monitoring and adjustment to maintain optimal business results.'
            }
        else:
            # Generic business services with dynamic business type integration
            clean_business_type = business_type.replace('Business', '').strip()
            if not clean_business_type:
                clean_business_type = 'Professional'

            return {
                f'{clean_business_type} Consultation': f'Expert {clean_business_type.lower()} consultation services tailored to your specific needs and requirements.',
                'Custom Solutions': 'Personalized solutions designed to address your unique business challenges and goals.',
                'Professional Support': 'Reliable ongoing support to ensure continued success and customer satisfaction.',
                'Quality Assurance': 'Comprehensive quality assurance processes to maintain the highest standards of service.',
                'Strategic Guidance': 'Strategic guidance and planning to help your business achieve its objectives efficiently.'
            }

    def generate_service_description(self, service_name: str) -> str:
        """Generate enhanced AI description for a service based on its name"""
        service_lower = service_name.lower()

        # Enhanced service-specific descriptions with more detail
        if 'virus' in service_lower or 'malware' in service_lower:
            return 'Complete virus and malware removal to keep your computer safe and running smoothly. Our comprehensive security service protects your data and prevents future infections.'
        elif 'hardware' in service_lower or 'repair' in service_lower:
            return 'Professional hardware diagnosis, repair, and upgrade services for optimal performance. We handle everything from component replacement to system optimization.'
        elif 'data recovery' in service_lower or 'recovery' in service_lower:
            return 'Recover lost data and set up reliable backup solutions to protect your important files. Emergency recovery services available for critical business needs.'
        elif 'on-site' in service_lower or 'onsite' in service_lower:
            return 'Convenient on-site technical support and repair services at your home or business location. Professional service without the hassle of transporting equipment.'
        elif 'remote' in service_lower:
            return 'Fast remote technical assistance to resolve issues without leaving your location. Secure connections ensure your privacy while we solve your problems.'
        elif 'network' in service_lower or 'networking' in service_lower:
            return 'Complete network setup, configuration, and troubleshooting for optimal connectivity. From Wi-Fi optimization to business network infrastructure.'
        elif 'optimization' in service_lower or 'performance' in service_lower:
            return 'System optimization and performance tuning to maximize efficiency and speed. Get the most out of your hardware with professional tuning services.'
        elif 'software' in service_lower or 'installation' in service_lower:
            return 'Professional software installation, configuration, and troubleshooting services. From operating systems to specialized business applications.'
        elif 'consultation' in service_lower or 'consulting' in service_lower:
            return 'Expert consultation services to help you make informed technology decisions. Strategic planning for your technology needs and budget.'
        elif 'support' in service_lower or 'maintenance' in service_lower:
            return 'Ongoing technical support and maintenance to keep your systems running smoothly. Preventive care and rapid response when issues arise.'
        elif 'upgrade' in service_lower:
            return 'Hardware and software upgrade services to improve performance and extend system life. Cost-effective solutions to modernize your technology.'
        elif 'backup' in service_lower:
            return 'Comprehensive backup solutions to protect your valuable data. Automated systems and cloud integration for peace of mind.'
        elif 'security' in service_lower:
            return 'Complete security assessment and implementation services. Protect your systems from threats with enterprise-grade security solutions.'
        else:
            # Enhanced generic professional description
            return f'Professional {service_name.lower()} services delivered with expertise, attention to detail, and a commitment to customer satisfaction.'

    def generate_service_features(self, service_name: str) -> list:
        """Generate feature list for a service based on its name"""
        service_lower = service_name.lower()

        if 'virus' in service_lower or 'malware' in service_lower:
            return [
                'Full system scan and analysis',
                'Complete malware removal',
                'Security software installation',
                'System optimization',
                'Prevention education',
                'Follow-up security check'
            ]
        elif 'hardware' in service_lower or 'repair' in service_lower:
            return [
                'Hardware diagnosis and testing',
                'Component replacement and repair',
                'Memory and storage upgrades',
                'Performance optimization',
                'Warranty on all parts',
                'Post-repair testing'
            ]
        elif 'data recovery' in service_lower or 'recovery' in service_lower:
            return [
                'Emergency data recovery',
                'Data recovery from failed drives',
                'File recovery and restoration',
                'Backup system setup',
                'Cloud storage configuration',
                'Data protection consultation'
            ]
        elif 'network' in service_lower:
            return [
                'Network assessment and planning',
                'Wi-Fi setup and optimization',
                'Security configuration',
                'Performance monitoring',
                'Troubleshooting and support',
                'Documentation and training'
            ]
        else:
            return [
                'Professional assessment',
                'Expert implementation',
                'Quality assurance testing',
                'Documentation provided',
                'Follow-up support',
                'Satisfaction guarantee'
            ]

    def generate_service_pricing(self, service_name: str) -> str:
        """Generate pricing information for a service"""
        service_lower = service_name.lower()

        if 'virus' in service_lower or 'malware' in service_lower:
            return 'Starting at $89'
        elif 'hardware' in service_lower or 'repair' in service_lower:
            return 'Starting at $75'
        elif 'data recovery' in service_lower or 'recovery' in service_lower:
            return 'Starting at $125'
        elif 'on-site' in service_lower or 'onsite' in service_lower:
            return 'Starting at $95'
        elif 'consultation' in service_lower:
            return 'Starting at $65'
        elif 'network' in service_lower:
            return 'Starting at $110'
        else:
            return 'Contact for pricing'

    def convert_services_to_php_array(self, services: dict) -> str:
        """Convert Python services dictionary to PHP array format for WordPress"""
        if not services:
            return 'array()'

        # Convert to a format that can be safely stored and retrieved
        # Use double quotes to avoid escaping issues
        php_array_items = []
        for service_name, service_desc in services.items():
            # Double escape for PHP string literals
            escaped_name = service_name.replace("'", "\\'").replace('"', '\\"')
            escaped_desc = service_desc.replace("'", "\\'").replace('"', '\\"')
            php_array_items.append(f'"{escaped_name}" => "{escaped_desc}"')

        return f"array({', '.join(php_array_items)})"
