#!/usr/bin/env python3
"""
Simple Design Variation Test
Demonstrates the concept of generating different designs
"""

import json
import random
from pathlib import Path

def generate_simple_variation(template_spec):
    """Generate a simple design variation"""
    
    # Color palettes by industry
    color_palettes = {
        "tech": [
            {"primary": "#2563eb", "secondary": "#10b981", "accent": "#7c3aed"},
            {"primary": "#0891b2", "secondary": "#ec4899", "accent": "#f59e0b"},
            {"primary": "#7c3aed", "secondary": "#06b6d4", "accent": "#10b981"}
        ],
        "healthcare": [
            {"primary": "#0891b2", "secondary": "#10b981", "accent": "#6366f1"},
            {"primary": "#059669", "secondary": "#3b82f6", "accent": "#8b5cf6"},
            {"primary": "#06b6d4", "secondary": "#10b981", "accent": "#6366f1"}
        ],
        "creative": [
            {"primary": "#ea580c", "secondary": "#ec4899", "accent": "#8b5cf6"},
            {"primary": "#dc2626", "secondary": "#f59e0b", "accent": "#10b981"},
            {"primary": "#7c2d12", "secondary": "#ea580c", "accent": "#ec4899"}
        ],
        "finance": [
            {"primary": "#1e40af", "secondary": "#059669", "accent": "#374151"},
            {"primary": "#0f172a", "secondary": "#1e293b", "accent": "#475569"},
            {"primary": "#1e293b", "secondary": "#0891b2", "accent": "#10b981"}
        ]
    }
    
    # Typography combinations
    typography_options = [
        {"heading": "Inter", "body": "Inter", "style": "modern"},
        {"heading": "Poppins", "body": "Open Sans", "style": "friendly"},
        {"heading": "Montserrat", "body": "Lato", "style": "bold"},
        {"heading": "Playfair Display", "body": "Source Sans Pro", "style": "elegant"}
    ]
    
    # Layout styles
    layout_styles = [
        {"name": "centered_hero", "description": "Traditional centered layout"},
        {"name": "split_hero", "description": "Text left, visual right"},
        {"name": "minimal_hero", "description": "Typography-focused minimal"},
        {"name": "full_width_hero", "description": "Full-width with overlay"}
    ]
    
    # Button styles
    button_styles = [
        {"name": "rounded", "radius": "8px", "padding": "1rem 2rem"},
        {"name": "pill", "radius": "50px", "padding": "0.875rem 2.5rem"},
        {"name": "sharp", "radius": "4px", "padding": "1.125rem 2.25rem"},
        {"name": "soft", "radius": "12px", "padding": "1rem 2rem"}
    ]

    # Complex components to add variety
    component_sets = [
        {
            "name": "pricing_focus",
            "includes": ["pricing_table", "testimonials", "features"],
            "hero_cta": "View Pricing",
            "sections": ["hero", "features", "pricing", "testimonials", "contact"]
        },
        {
            "name": "feature_showcase",
            "includes": ["feature_grid", "stats", "cta_banner"],
            "hero_cta": "Explore Features",
            "sections": ["hero", "stats", "features", "cta_banner", "contact"]
        },
        {
            "name": "testimonial_heavy",
            "includes": ["testimonials", "case_studies", "team"],
            "hero_cta": "See Success Stories",
            "sections": ["hero", "testimonials", "case_studies", "team", "contact"]
        },
        {
            "name": "conversion_optimized",
            "includes": ["benefits", "social_proof", "urgency"],
            "hero_cta": "Start Free Trial",
            "sections": ["hero", "benefits", "social_proof", "pricing", "contact"]
        }
    ]

    # Visual complexity options
    visual_complexity = [
        {
            "level": "minimal",
            "background": "solid_colors",
            "shadows": "subtle",
            "animations": "basic_hover"
        },
        {
            "level": "moderate",
            "background": "gradients",
            "shadows": "elevated",
            "animations": "smooth_transitions"
        },
        {
            "level": "rich",
            "background": "patterns_gradients",
            "shadows": "layered",
            "animations": "micro_interactions"
        },
        {
            "level": "premium",
            "background": "hero_images",
            "shadows": "dramatic",
            "animations": "scroll_triggered"
        }
    ]
    
    # Detect industry
    industry_context = template_spec.get('industry_context', '').lower()
    industry = "tech"  # default
    
    if any(word in industry_context for word in ['health', 'medical', 'care']):
        industry = "healthcare"
    elif any(word in industry_context for word in ['creative', 'design', 'art']):
        industry = "creative"
    elif any(word in industry_context for word in ['finance', 'bank', 'investment']):
        industry = "finance"
    
    # Select random variations
    colors = random.choice(color_palettes.get(industry, color_palettes["tech"]))
    typography = random.choice(typography_options)
    layout = random.choice(layout_styles)
    buttons = random.choice(button_styles)
    components = random.choice(component_sets)
    complexity = random.choice(visual_complexity)

    return {
        "variation_id": f"var_{random.randint(1000, 9999)}",
        "industry": industry,
        "colors": colors,
        "typography": typography,
        "layout": layout,
        "buttons": buttons,
        "components": components,
        "visual_complexity": complexity,
        "css_variables": {
            "--primary-color": colors["primary"],
            "--secondary-color": colors["secondary"],
            "--accent-color": colors["accent"],
            "--font-heading": typography["heading"],
            "--font-body": typography["body"],
            "--button-radius": buttons["radius"],
            "--button-padding": buttons["padding"]
        }
    }

def test_variations():
    """Test generating multiple variations"""
    print("🎨 Simple Design Variation Test")
    print("=" * 50)
    
    # Test specs
    test_specs = [
        {"template_id": "tech_startup", "industry_context": "software development, SaaS, technology"},
        {"template_id": "healthcare_clinic", "industry_context": "healthcare, medical services, patient care"},
        {"template_id": "creative_agency", "industry_context": "creative services, design agency, portfolio"},
        {"template_id": "finance_firm", "industry_context": "finance, investment, banking, corporate"}
    ]
    
    variations = []
    
    for spec in test_specs:
        print(f"\n📋 {spec['template_id'].replace('_', ' ').title()}")
        
        # Generate 3 variations for each spec
        for i in range(3):
            variation = generate_simple_variation(spec)
            variations.append(variation)
            
            print(f"   Variation {i+1}:")
            print(f"   🎨 Colors: {variation['colors']['primary']} | {variation['colors']['secondary']}")
            print(f"   📝 Fonts: {variation['typography']['heading']} + {variation['typography']['body']}")
            print(f"   📐 Layout: {variation['layout']['name']}")
            print(f"   🔘 Buttons: {variation['buttons']['name']} style")
    
    # Save variations
    output_dir = Path("simple_variations_test")
    output_dir.mkdir(exist_ok=True)
    
    for i, variation in enumerate(variations):
        output_file = output_dir / f"variation_{i+1}.json"
        with open(output_file, 'w') as f:
            json.dump(variation, f, indent=2)
    
    print(f"\n📁 Saved {len(variations)} variations to: {output_dir}/")
    
    # Analyze uniqueness
    unique_colors = len(set(v['colors']['primary'] for v in variations))
    unique_fonts = len(set(v['typography']['heading'] for v in variations))
    unique_layouts = len(set(v['layout']['name'] for v in variations))
    
    print(f"\n🔍 Uniqueness Analysis:")
    print(f"   • Unique color schemes: {unique_colors}/{len(variations)}")
    print(f"   • Unique font combinations: {unique_fonts}/{len(variations)}")
    print(f"   • Unique layout styles: {unique_layouts}/{len(variations)}")
    
    return variations

def create_sample_template_with_variation(variation):
    """Create a sample template using the variation"""
    colors = variation['colors']
    typography = variation['typography']
    layout = variation['layout']
    buttons = variation['buttons']
    
    # Generate CSS based on variation
    css = f"""
/* Design Variation: {variation['variation_id']} */
/* Industry: {variation['industry']} */
/* Style: {typography['style']}, {layout['name']} */

:root {{
    --primary-color: {colors['primary']};
    --secondary-color: {colors['secondary']};
    --accent-color: {colors['accent']};
    --font-heading: '{typography['heading']}', sans-serif;
    --font-body: '{typography['body']}', sans-serif;
    --button-radius: {buttons['radius']};
    --button-padding: {buttons['padding']};
}}

body {{
    font-family: var(--font-body);
    color: #1f2937;
}}

.hero {{
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    padding: 120px 0 80px;
    text-align: {'center' if layout['name'] == 'centered_hero' else 'left'};
}}

.hero h1 {{
    font-family: var(--font-heading);
    font-size: {'4rem' if layout['name'] == 'full_width_hero' else '3.5rem'};
    font-weight: {'300' if typography['style'] == 'elegant' else '700'};
    margin-bottom: 1rem;
}}

.cta-button {{
    background: var(--accent-color);
    color: white;
    padding: var(--button-padding);
    border-radius: var(--button-radius);
    text-decoration: none;
    font-weight: 600;
    display: inline-block;
    transition: all 0.3s ease;
}}

.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}}

.feature-card {{
    background: white;
    padding: 2rem;
    border-radius: {'20px' if buttons['name'] == 'soft' else '12px'};
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: {'2px solid #e5e7eb' if buttons['name'] == 'sharp' else 'none'};
}}
"""
    
    return css

def demonstrate_integration():
    """Demonstrate how this integrates with the pipeline"""
    print("\n🔗 Pipeline Integration Demonstration")
    print("=" * 50)
    
    # Simulate pipeline steps
    print("1. 📝 Request Interpreter → Template Spec")
    template_spec = {
        "template_id": "demo_template",
        "project_type": "saas_landing_page",
        "industry_context": "technology, software, SaaS",
        "requirements": {"design": {"style": "modern"}}
    }
    
    print("2. 🎨 Design Variation Generator → Unique Design")
    variation = generate_simple_variation(template_spec)
    
    print("3. 🏗️ Template Engineer → CSS with Variation")
    css = create_sample_template_with_variation(variation)
    
    print(f"\n✨ Generated Design:")
    print(f"   • Colors: {variation['colors']['primary']} (primary)")
    print(f"   • Typography: {variation['typography']['heading']} + {variation['typography']['body']}")
    print(f"   • Layout: {variation['layout']['description']}")
    print(f"   • Button Style: {variation['buttons']['name']}")
    
    # Save demonstration files
    output_dir = Path("integration_demo")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "template_spec.json", 'w') as f:
        json.dump(template_spec, f, indent=2)
    
    with open(output_dir / "design_variation.json", 'w') as f:
        json.dump(variation, f, indent=2)
    
    with open(output_dir / "generated_styles.css", 'w') as f:
        f.write(css)
    
    print(f"\n📁 Demo files saved to: {output_dir}/")

if __name__ == "__main__":
    # Test basic variations
    variations = test_variations()
    
    # Demonstrate integration
    demonstrate_integration()
    
    print("\n" + "=" * 50)
    print("🎯 Design Variation System Benefits:")
    print("   ✅ Industry-specific color palettes")
    print("   ✅ Typography variety (4 different styles)")
    print("   ✅ Layout structure options (4 layouts)")
    print("   ✅ Component style variations")
    print("   ✅ Automatic CSS variable generation")
    print("   ✅ Easy pipeline integration")
    
    print("\n📝 Next Steps:")
    print("   1. Integrate into orchestrator pipeline")
    print("   2. Update template_engineer to use variations")
    print("   3. Test with real template generation")
    print("   4. Add more variation options")
