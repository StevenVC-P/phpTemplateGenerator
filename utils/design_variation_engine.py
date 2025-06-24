#!/usr/bin/env python3
"""
Design Variation Engine
Generates unique design variations for each template to ensure visual diversity
"""

import json
import random
import colorsys
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DesignVariationEngine:
    """Engine for generating unique design variations"""
    
    def __init__(self, config_path: str = "agents/design_variation_generator.json"):
        self.config = self.load_config(config_path)
        self.used_combinations = set()  # Track used combinations to avoid duplicates
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load design variation configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if file not found"""
        return {
            "variation_strategies": {
                "color_generation": {
                    "methods": ["complementary_harmony", "triadic_scheme"],
                    "industry_influences": {
                        "tech": ["#2563eb", "#10b981", "#7c3aed"],
                        "finance": ["#1e40af", "#059669", "#374151"],
                        "healthcare": ["#0891b2", "#10b981", "#6366f1"],
                        "creative": ["#ea580c", "#ec4899", "#8b5cf6"],
                        "corporate": ["#1e293b", "#0f172a", "#475569"],
                        "default": ["#2563eb", "#10b981", "#f59e0b"]
                    }
                },
                "typography_variations": {
                    "font_pairings": [
                        {
                            "name": "modern_professional",
                            "heading": "Inter",
                            "body": "Inter",
                            "accent": "JetBrains Mono",
                            "personality": "clean, modern, tech-forward"
                        }
                    ],
                    "size_scales": [
                        {
                            "name": "conservative",
                            "h1": "2.5rem",
                            "h2": "2rem",
                            "h3": "1.5rem",
                            "body": "1rem"
                        }
                    ]
                },
                "layout_variations": {
                    "hero_styles": [
                        {
                            "name": "classic_centered",
                            "structure": "centered_content_with_background",
                            "cta_placement": "below_text",
                            "visual_weight": "balanced",
                            "description": "Traditional centered hero with symmetrical layout"
                        }
                    ],
                    "section_arrangements": ["hero_features_pricing_contact"],
                    "grid_systems": ["three_column_equal"]
                },
                "component_variations": {
                    "button_styles": [
                        {
                            "name": "rounded_modern",
                            "border_radius": "8px",
                            "padding": "1rem 2rem",
                            "shadow": "0 4px 15px rgba(0,0,0,0.1)"
                        }
                    ],
                    "card_styles": [
                        {
                            "name": "elevated_modern",
                            "border_radius": "12px",
                            "shadow": "0 4px 6px rgba(0,0,0,0.1)",
                            "border": "none"
                        }
                    ]
                }
            },
            "unique_elements_library": {
                "background_patterns": ["subtle_geometric_grid"],
                "decorative_elements": ["floating_icons"],
                "interaction_styles": ["hover_lift_animations"]
            }
        }
    
    def generate_variation(self, template_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a unique design variation based on template specification"""
        logger.info("Generating design variation")
        
        try:
            # Extract context from template spec
            project_type = template_spec.get('project_type', 'saas_landing_page')
            target_audience = template_spec.get('target_audience', {})
            industry = self.detect_industry(template_spec)
            
            # Generate variation components
            color_palette = self.generate_color_palette(industry)
            typography = self.select_typography_scheme(project_type)
            layout = self.select_layout_structure(project_type)
            components = self.generate_component_styles()
            unique_elements = self.select_unique_elements()
            
            # Create variation specification
            variation = {
                "variation_id": self.generate_variation_id(),
                "timestamp": datetime.now().isoformat(),
                "industry_context": industry,
                "color_palette": color_palette,
                "typography_scheme": typography,
                "layout_structure": layout,
                "component_styles": components,
                "unique_elements": unique_elements,
                "css_variables": self.generate_css_variables(color_palette, typography),
                "design_personality": self.determine_personality(color_palette, typography, layout)
            }
            
            # Track this combination to avoid duplicates
            combination_key = self.create_combination_key(variation)
            self.used_combinations.add(combination_key)
            
            logger.info(f"Generated variation: {variation['variation_id']}")
            return variation
            
        except Exception as e:
            logger.error(f"Failed to generate variation: {e}")
            return self.get_fallback_variation()
    
    def detect_industry(self, template_spec: Dict[str, Any]) -> str:
        """Detect industry from template specification"""
        project_type = template_spec.get('project_type', '').lower()
        requirements = str(template_spec.get('requirements', {})).lower()
        
        if any(word in requirements for word in ['tech', 'software', 'saas', 'app']):
            return 'tech'
        elif any(word in requirements for word in ['finance', 'bank', 'investment']):
            return 'finance'
        elif any(word in requirements for word in ['health', 'medical', 'care']):
            return 'healthcare'
        elif any(word in requirements for word in ['creative', 'design', 'art']):
            return 'creative'
        else:
            return 'corporate'
    
    def generate_color_palette(self, industry: str) -> Dict[str, str]:
        """Generate a harmonious color palette based on industry"""
        try:
            strategies = self.config["variation_strategies"]["color_generation"]
            industry_colors = strategies["industry_influences"].get(industry, strategies["industry_influences"]["default"])

            # Select base color from industry palette
            base_color = random.choice(industry_colors)

            # Validate base color format
            if not base_color.startswith('#') or len(base_color) != 7:
                base_color = "#2563eb"  # Fallback to safe color

            # Generate complementary colors
            method = random.choice(strategies["methods"])

            if method == "complementary_harmony":
                palette = self.generate_complementary_palette(base_color)
            elif method == "triadic_scheme":
                palette = self.generate_triadic_palette(base_color)
            elif method == "analogous_palette":
                palette = self.generate_analogous_palette(base_color)
            else:
                palette = self.generate_monochromatic_palette(base_color)

            return palette
        except Exception as e:
            logger.error(f"Color palette generation failed: {e}")
            # Return safe fallback palette
            return {
                "primary": "#2563eb",
                "secondary": "#10b981",
                "accent": "#f59e0b",
                "neutral_light": "#f8fafc",
                "neutral_dark": "#1e293b",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            }
    
    def generate_complementary_palette(self, base_color: str) -> Dict[str, str]:
        """Generate complementary color palette"""
        # Convert hex to HSV
        h, s, v = self.hex_to_hsv(base_color)
        
        # Generate complementary color (180 degrees opposite)
        comp_h = (h + 0.5) % 1.0
        
        return {
            "primary": base_color,
            "secondary": self.hsv_to_hex(comp_h, s * 0.8, v * 0.9),
            "accent": self.hsv_to_hex((h + 0.15) % 1.0, s * 0.6, v * 1.1),
            "neutral_light": "#f8fafc",
            "neutral_dark": "#1e293b",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
    
    def generate_triadic_palette(self, base_color: str) -> Dict[str, str]:
        """Generate triadic color palette"""
        h, s, v = self.hex_to_hsv(base_color)
        
        return {
            "primary": base_color,
            "secondary": self.hsv_to_hex((h + 0.33) % 1.0, s * 0.8, v * 0.9),
            "accent": self.hsv_to_hex((h + 0.66) % 1.0, s * 0.7, v * 0.95),
            "neutral_light": "#f8fafc",
            "neutral_dark": "#1e293b",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
    
    def generate_analogous_palette(self, base_color: str) -> Dict[str, str]:
        """Generate analogous color palette"""
        h, s, v = self.hex_to_hsv(base_color)
        
        return {
            "primary": base_color,
            "secondary": self.hsv_to_hex((h + 0.08) % 1.0, s * 0.9, v * 0.95),
            "accent": self.hsv_to_hex((h - 0.08) % 1.0, s * 0.7, v * 1.05),
            "neutral_light": "#f8fafc",
            "neutral_dark": "#1e293b",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
    
    def generate_monochromatic_palette(self, base_color: str) -> Dict[str, str]:
        """Generate monochromatic color palette"""
        h, s, v = self.hex_to_hsv(base_color)
        
        return {
            "primary": base_color,
            "secondary": self.hsv_to_hex(h, s * 0.6, v * 0.8),
            "accent": self.hsv_to_hex(h, s * 0.4, v * 1.2),
            "neutral_light": "#f8fafc",
            "neutral_dark": "#1e293b",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
    
    def hex_to_hsv(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to HSV"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        return colorsys.rgb_to_hsv(r, g, b)
    
    def hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """Convert HSV to hex color"""
        # Clamp values
        s = max(0, min(1, s))
        v = max(0, min(1, v))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def select_typography_scheme(self, project_type: str) -> Dict[str, Any]:
        """Select typography scheme based on project type"""
        typography_variations = self.config["variation_strategies"]["typography_variations"]
        font_pairings = typography_variations["font_pairings"]
        size_scales = typography_variations["size_scales"]
        
        # Select random pairing and scale
        pairing = random.choice(font_pairings)
        scale = random.choice(size_scales)
        
        return {
            "fonts": pairing,
            "scale": scale,
            "google_fonts_url": self.generate_google_fonts_url(pairing)
        }
    
    def generate_google_fonts_url(self, pairing: Dict[str, str]) -> str:
        """Generate Google Fonts URL for font pairing"""
        fonts = []
        for font_type in ['heading', 'body', 'accent']:
            font_name = pairing.get(font_type, 'Inter')
            if font_name and font_name not in [f.split(':')[0] for f in fonts]:
                fonts.append(f"{font_name.replace(' ', '+')}:wght@300;400;500;600;700")
        
        return f"https://fonts.googleapis.com/css2?{'+'.join([f'family={font}' for font in fonts])}&display=swap"
    
    def select_layout_structure(self, project_type: str) -> Dict[str, Any]:
        """Select layout structure variation"""
        layout_variations = self.config["variation_strategies"]["layout_variations"]
        
        return {
            "hero_style": random.choice(layout_variations["hero_styles"]),
            "section_arrangement": random.choice(layout_variations["section_arrangements"]),
            "grid_system": random.choice(layout_variations["grid_systems"])
        }
    
    def generate_component_styles(self) -> Dict[str, Any]:
        """Generate component style variations"""
        component_variations = self.config["variation_strategies"]["component_variations"]
        
        return {
            "buttons": random.choice(component_variations["button_styles"]),
            "cards": random.choice(component_variations["card_styles"])
        }
    
    def select_unique_elements(self) -> Dict[str, Any]:
        """Select unique design elements"""
        unique_library = self.config["unique_elements_library"]
        
        return {
            "background_pattern": random.choice(unique_library["background_patterns"]),
            "decorative_element": random.choice(unique_library["decorative_elements"]),
            "interaction_style": random.choice(unique_library["interaction_styles"])
        }
    
    def generate_css_variables(self, color_palette: Dict[str, str], typography: Dict[str, Any]) -> Dict[str, str]:
        """Generate CSS custom properties for the variation"""
        fonts = typography["fonts"]
        scale = typography["scale"]
        
        return {
            "--primary-color": color_palette["primary"],
            "--secondary-color": color_palette["secondary"],
            "--accent-color": color_palette["accent"],
            "--neutral-light": color_palette["neutral_light"],
            "--neutral-dark": color_palette["neutral_dark"],
            "--font-heading": fonts["heading"],
            "--font-body": fonts["body"],
            "--font-accent": fonts.get("accent", fonts["body"]),
            "--text-xl": scale["h1"],
            "--text-lg": scale["h2"],
            "--text-md": scale["h3"],
            "--text-base": scale["body"]
        }
    
    def determine_personality(self, color_palette: Dict[str, str], typography: Dict[str, Any], layout: Dict[str, Any]) -> str:
        """Determine the design personality based on choices"""
        personalities = []
        
        # Color-based personality
        primary_hue = self.hex_to_hsv(color_palette["primary"])[0]
        if 0.5 <= primary_hue <= 0.7:  # Blue range
            personalities.append("professional")
        elif 0.7 <= primary_hue <= 0.9:  # Purple range
            personalities.append("creative")
        elif 0.0 <= primary_hue <= 0.1 or 0.9 <= primary_hue <= 1.0:  # Red range
            personalities.append("energetic")
        
        # Typography-based personality
        font_personality = typography["fonts"].get("personality", "modern")
        personalities.append(font_personality.split(",")[0].strip())
        
        return ", ".join(personalities)
    
    def create_combination_key(self, variation: Dict[str, Any]) -> str:
        """Create a key to track used combinations"""
        return f"{variation['color_palette']['primary']}_{variation['typography_scheme']['fonts']['heading']}_{variation['layout_structure']['hero_style']['name']}"
    
    def generate_variation_id(self) -> str:
        """Generate unique variation ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"var_{timestamp}_{random.randint(100, 999)}"
    
    def get_fallback_variation(self) -> Dict[str, Any]:
        """Get fallback variation if generation fails"""
        return {
            "variation_id": "fallback_001",
            "timestamp": datetime.now().isoformat(),
            "industry_context": "tech",
            "color_palette": {
                "primary": "#2563eb",
                "secondary": "#10b981",
                "accent": "#f59e0b",
                "neutral_light": "#f8fafc",
                "neutral_dark": "#1e293b",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            },
            "typography_scheme": {
                "fonts": {"heading": "Inter", "body": "Inter", "accent": "Inter"},
                "scale": {"h1": "3rem", "h2": "2rem", "h3": "1.5rem", "body": "1rem"},
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
            },
            "layout_structure": {
                "hero_style": {
                    "name": "classic_centered",
                    "structure": "centered_content_with_background",
                    "cta_placement": "below_text",
                    "visual_weight": "balanced",
                    "description": "Traditional centered hero with symmetrical layout"
                },
                "section_arrangement": "hero_features_pricing_contact",
                "grid_system": "three_column_equal"
            },
            "component_styles": {
                "buttons": {
                    "name": "rounded_modern",
                    "border_radius": "8px",
                    "padding": "1rem 2rem",
                    "shadow": "0 4px 15px rgba(0,0,0,0.1)"
                },
                "cards": {
                    "name": "elevated_modern",
                    "border_radius": "12px",
                    "shadow": "0 4px 6px rgba(0,0,0,0.1)",
                    "border": "none"
                }
            },
            "unique_elements": {
                "background_pattern": "subtle_geometric_grid",
                "decorative_element": "floating_icons",
                "interaction_style": "hover_lift_animations"
            },
            "css_variables": {
                "--primary-color": "#2563eb",
                "--secondary-color": "#10b981",
                "--accent-color": "#f59e0b",
                "--neutral-light": "#f8fafc",
                "--neutral-dark": "#1e293b",
                "--font-heading": "Inter",
                "--font-body": "Inter",
                "--font-accent": "Inter",
                "--text-xl": "3rem",
                "--text-lg": "2rem",
                "--text-md": "1.5rem",
                "--text-base": "1rem"
            },
            "design_personality": "professional, modern"
        }

# Utility functions
def generate_design_variation(template_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to generate design variation"""
    engine = DesignVariationEngine()
    return engine.generate_variation(template_spec)
