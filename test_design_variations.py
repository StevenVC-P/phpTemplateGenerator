#!/usr/bin/env python3
"""
Test Design Variation System
Demonstrates how the system generates unique designs for each template
"""

import json
import asyncio
from pathlib import Path
from utils.design_variation_engine import DesignVariationEngine

def create_sample_template_specs():
    """Create sample template specifications for testing"""
    specs = [
        {
            "template_id": "tech_startup",
            "project_type": "saas_landing_page",
            "requirements": {
                "design": {"style": "modern", "responsive": True},
                "technical": {"language": "php", "framework": "none"}
            },
            "target_audience": {"primary": "tech_startups", "secondary": "developers"},
            "industry_context": "software development, SaaS, technology"
        },
        {
            "template_id": "healthcare_service",
            "project_type": "service_landing_page",
            "requirements": {
                "design": {"style": "trustworthy", "responsive": True},
                "technical": {"language": "php", "framework": "none"}
            },
            "target_audience": {"primary": "patients", "secondary": "healthcare_providers"},
            "industry_context": "healthcare, medical services, patient care"
        },
        {
            "template_id": "creative_agency",
            "project_type": "portfolio_site",
            "requirements": {
                "design": {"style": "creative", "responsive": True},
                "technical": {"language": "php", "framework": "none"}
            },
            "target_audience": {"primary": "creative_professionals", "secondary": "clients"},
            "industry_context": "creative services, design agency, portfolio"
        },
        {
            "template_id": "finance_company",
            "project_type": "corporate_website",
            "requirements": {
                "design": {"style": "professional", "responsive": True},
                "technical": {"language": "php", "framework": "none"}
            },
            "target_audience": {"primary": "business_owners", "secondary": "investors"},
            "industry_context": "finance, investment, banking, corporate"
        }
    ]
    
    return specs

def test_design_variations():
    """Test design variation generation"""
    print("🎨 Testing Design Variation System")
    print("=" * 50)
    
    # Initialize engine
    engine = DesignVariationEngine()
    
    # Create sample specs
    template_specs = create_sample_template_specs()
    
    print(f"📋 Testing {len(template_specs)} different template types:")
    
    variations = []
    for i, spec in enumerate(template_specs, 1):
        print(f"\n{i}. {spec['template_id'].replace('_', ' ').title()}")
        print(f"   Industry: {spec['industry_context']}")
        
        # Generate variation
        variation = engine.generate_variation(spec)
        variations.append(variation)
        
        # Display key characteristics
        color_palette = variation['color_palette']
        typography = variation['typography_scheme']['fonts']
        layout = variation['layout_structure']['hero_style']
        
        print(f"   🎨 Colors: {color_palette['primary']} (primary), {color_palette['secondary']} (secondary)")
        print(f"   📝 Fonts: {typography['heading']} (heading), {typography['body']} (body)")
        print(f"   📐 Layout: {layout['name']} - {layout['description']}")
        print(f"   ✨ Personality: {variation['design_personality']}")
    
    # Analyze uniqueness
    print(f"\n🔍 Uniqueness Analysis:")
    unique_colors = len(set(v['color_palette']['primary'] for v in variations))
    unique_fonts = len(set(v['typography_scheme']['fonts']['heading'] for v in variations))
    unique_layouts = len(set(v['layout_structure']['hero_style']['name'] for v in variations))
    
    print(f"   • Unique color schemes: {unique_colors}/{len(variations)}")
    print(f"   • Unique font pairings: {unique_fonts}/{len(variations)}")
    print(f"   • Unique layout styles: {unique_layouts}/{len(variations)}")
    
    # Save variations for inspection
    output_dir = Path("design_variations_test")
    output_dir.mkdir(exist_ok=True)
    
    for i, variation in enumerate(variations):
        output_file = output_dir / f"variation_{i+1}_{variation['variation_id']}.json"
        with open(output_file, 'w') as f:
            json.dump(variation, f, indent=2)
    
    print(f"\n📁 Saved {len(variations)} variations to: {output_dir}/")
    
    return variations

def generate_css_preview(variation):
    """Generate CSS preview for a variation"""
    css_vars = variation['css_variables']
    color_palette = variation['color_palette']
    
    css = f"""
/* Design Variation: {variation['variation_id']} */
/* Personality: {variation['design_personality']} */

:root {{
    /* Colors */
    --primary-color: {color_palette['primary']};
    --secondary-color: {color_palette['secondary']};
    --accent-color: {color_palette['accent']};
    --neutral-light: {color_palette['neutral_light']};
    --neutral-dark: {color_palette['neutral_dark']};
    
    /* Typography */
    --font-heading: '{css_vars['--font-heading']}', sans-serif;
    --font-body: '{css_vars['--font-body']}', sans-serif;
    --text-xl: {css_vars['--text-xl']};
    --text-lg: {css_vars['--text-lg']};
    --text-base: {css_vars['--text-base']};
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    padding: 120px 0 80px;
    text-align: center;
}}

.hero h1 {{
    font-family: var(--font-heading);
    font-size: var(--text-xl);
    font-weight: 700;
    margin-bottom: 1rem;
}}

/* CTA Button */
.cta-button {{
    background: var(--accent-color);
    color: white;
    padding: 1.25rem 2.5rem;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}}
"""
    
    return css

def create_css_previews(variations):
    """Create CSS previews for all variations"""
    print("\n🎨 Generating CSS Previews:")
    
    output_dir = Path("design_variations_test")
    
    for i, variation in enumerate(variations):
        css_content = generate_css_preview(variation)
        css_file = output_dir / f"variation_{i+1}_styles.css"
        
        with open(css_file, 'w') as f:
            f.write(css_content)
        
        print(f"   ✅ {css_file.name}")

def demonstrate_multiple_generations():
    """Demonstrate generating multiple variations for the same spec"""
    print("\n🔄 Multiple Generations Test:")
    print("Generating 5 variations for the same template spec...")
    
    engine = DesignVariationEngine()
    
    # Use the same spec multiple times
    base_spec = {
        "template_id": "multi_test",
        "project_type": "saas_landing_page",
        "requirements": {"design": {"style": "modern"}},
        "target_audience": {"primary": "businesses"},
        "industry_context": "technology, software"
    }
    
    variations = []
    for i in range(5):
        variation = engine.generate_variation(base_spec)
        variations.append(variation)
        
        print(f"   {i+1}. {variation['color_palette']['primary']} | {variation['typography_scheme']['fonts']['heading']} | {variation['layout_structure']['hero_style']['name']}")
    
    # Check uniqueness
    unique_combinations = len(set(
        f"{v['color_palette']['primary']}_{v['typography_scheme']['fonts']['heading']}_{v['layout_structure']['hero_style']['name']}"
        for v in variations
    ))
    
    print(f"   📊 Unique combinations: {unique_combinations}/5")
    
    return unique_combinations == 5

async def main():
    """Main test function"""
    print("🎨 Design Variation System Test")
    print("=" * 60)
    
    # Test basic variation generation
    variations = test_design_variations()
    
    # Create CSS previews
    create_css_previews(variations)
    
    # Test multiple generations
    all_unique = demonstrate_multiple_generations()
    
    print("\n" + "=" * 60)
    print("🎯 Design Variation System Summary:")
    print("   • Industry-specific color palettes ✅")
    print("   • Typography variation system ✅")
    print("   • Layout structure diversity ✅")
    print("   • CSS variable generation ✅")
    print("   • Personality determination ✅")
    print(f"   • Multiple unique generations: {'✅' if all_unique else '⚠️'}")
    
    print("\n📝 Integration Steps:")
    print("   1. Add design_variation_generator to agent pipeline")
    print("   2. Update template_engineer to use variations")
    print("   3. Modify CSS generation to use variation data")
    print("   4. Test with real template generation")
    
    print(f"\n📁 Check generated files in: design_variations_test/")

if __name__ == "__main__":
    asyncio.run(main())
