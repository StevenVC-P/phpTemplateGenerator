import json
import random
from pathlib import Path
from datetime import datetime
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

class DesignVariationGenerator:
    def __init__(self, config: Dict):
        self.config = config

    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        try:
            input_path = Path(input_file)
            # Put design variation in the correct directory
            template_dir = input_path.parent.parent  # Go up from specs/ to template_xxx/
            design_variations_dir = template_dir / "design_variations"
            design_variations_dir.mkdir(exist_ok=True)
            output_file = design_variations_dir / f"design_variation_{self.generate_variation_id()}.json"

            template_spec = json.loads(input_path.read_text())
            variation = self.generate_variation(template_spec)

            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(json.dumps(variation, indent=2))

            return AgentResult(
                agent_id="design_variation_generator",
                success=True,
                output_file=str(output_file),
                metadata={"variation_id": variation.get("variation_id")}
            )

        except Exception as e:
            return AgentResult(
                agent_id="design_variation_generator",
                success=False,
                error_message=str(e)
            )

    def generate_variation_id(self) -> str:
        return f"variation_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def random_choice(self, options):
        return random.choice(options) if options else None

    def get_business_appropriate_hero(self, industry, hero_options):
        """Select hero style based on business type"""
        # Business-specific hero preferences
        business_hero_preferences = {
            "landscaping": ["image_background_hero", "nature_focused_hero", "outdoor_showcase"],
            "pc repair": ["tech_focused_hero", "problem_solution_hero", "service_oriented"],
            "restaurant": ["food_showcase_hero", "ambiance_hero", "menu_highlight"],
            "real estate": ["property_showcase_hero", "professional_hero", "trust_building"],
            "construction": ["project_showcase_hero", "before_after_hero", "capability_hero"],
            "automotive": ["vehicle_showcase_hero", "service_bay_hero", "expertise_hero"],
            "beauty & wellness": ["transformation_hero", "relaxation_hero", "service_showcase"],
            "photography": ["portfolio_hero", "artistic_hero", "creative_showcase"],
            "marketing": ["results_hero", "creative_hero", "growth_focused"],
            "financial services": ["trust_hero", "security_hero", "growth_hero"],
            "education": ["learning_hero", "achievement_hero", "knowledge_hero"],
            "travel & hospitality": ["destination_hero", "experience_hero", "adventure_hero"],
            "pet services": ["pet_friendly_hero", "care_focused_hero", "happy_pets"],
            "fitness": ["transformation_hero", "energy_hero", "results_hero"],
            "cleaning services": ["before_after_hero", "fresh_clean_hero", "trust_hero"],
            "consulting": ["expertise_hero", "results_hero", "professional_hero"],
            "legal services": ["authority_hero", "trust_hero", "expertise_hero"]
        }

        # Get preferred styles for this business type
        preferred_styles = business_hero_preferences.get(industry, [])

        # If we have business-specific preferences, use them; otherwise use random
        if preferred_styles:
            # Try to find matching hero styles from available options
            matching_styles = [style for style in hero_options if any(pref in style.get("name", "") for pref in preferred_styles)]
            if matching_styles:
                return self.random_choice(matching_styles)

        # Fallback to random choice
        return self.random_choice(hero_options)

    def get_business_appropriate_typography(self, industry, typography_options):
        """Select typography based on business type"""
        # Business-specific typography preferences
        business_typography_preferences = {
            "landscaping": ["natural", "organic", "earthy", "friendly"],
            "pc repair": ["modern", "tech", "clean", "professional"],
            "restaurant": ["elegant", "warm", "inviting", "classic"],
            "real estate": ["professional", "trustworthy", "sophisticated", "clean"],
            "construction": ["bold", "strong", "industrial", "reliable"],
            "automotive": ["bold", "modern", "technical", "strong"],
            "beauty & wellness": ["elegant", "soft", "luxurious", "calming"],
            "photography": ["artistic", "creative", "elegant", "modern"],
            "marketing": ["dynamic", "creative", "bold", "modern"],
            "financial services": ["professional", "trustworthy", "conservative", "clean"],
            "education": ["friendly", "approachable", "clear", "professional"],
            "travel & hospitality": ["inviting", "adventurous", "elegant", "warm"],
            "pet services": ["friendly", "playful", "warm", "approachable"],
            "fitness": ["bold", "energetic", "strong", "motivational"],
            "cleaning services": ["clean", "fresh", "trustworthy", "professional"],
            "consulting": ["professional", "sophisticated", "trustworthy", "modern"],
            "legal services": ["authoritative", "professional", "traditional", "trustworthy"]
        }

        # Get preferred typography styles for this business type
        preferred_styles = business_typography_preferences.get(industry, [])

        # If we have business-specific preferences, use them; otherwise use random
        if preferred_styles:
            # Try to find matching typography from available options
            matching_typography = [typo for typo in typography_options if any(pref in typo.get("style", "").lower() for pref in preferred_styles)]
            if matching_typography:
                return self.random_choice(matching_typography)

        # Fallback to random choice
        return self.random_choice(typography_options)

    def get_theme_appropriate_color_strategy(self, visual_theme, color_methods):
        """Select color strategy based on visual theme"""
        theme_name = visual_theme["name"]

        theme_color_preferences = {
            "minimalist_clean": ["monochromatic_variation", "analogous_palette", "cool_palette"],
            "bold_expressive": ["complementary_harmony", "triadic_scheme", "vibrant_bold", "high_contrast"],
            "organic_natural": ["analogous_palette", "earth_tones", "warm_palette"],
            "tech_modern": ["cool_palette", "monochromatic_variation", "split_complementary"],
            "artistic_creative": ["triadic_scheme", "tetradic_scheme", "vibrant_bold"],
            "professional_corporate": ["monochromatic_variation", "analogous_palette", "cool_palette"]
        }

        preferred_colors = theme_color_preferences.get(theme_name, color_methods)
        available_colors = [method for method in preferred_colors if method in color_methods]

        return self.random_choice(available_colors) if available_colors else self.random_choice(color_methods)

    def get_theme_appropriate_hero(self, visual_theme, industry, hero_styles):
        """Select hero style based on visual theme and industry"""
        theme_name = visual_theme["name"]

        theme_hero_preferences = {
            "minimalist_clean": ["minimal_focus", "classic_centered"],
            "bold_expressive": ["overlay_hero", "geometric_shapes", "floating_elements"],
            "organic_natural": ["split_screen", "card_stack", "magazine_style"],
            "tech_modern": ["diagonal_split", "full_height_sidebar", "geometric_shapes"],
            "artistic_creative": ["floating_elements", "magazine_style", "geometric_shapes"],
            "professional_corporate": ["classic_centered", "split_screen", "full_height_sidebar"]
        }

        preferred_heroes = theme_hero_preferences.get(theme_name, [])
        available_heroes = [hero for hero in hero_styles if hero["name"] in preferred_heroes]

        if available_heroes:
            return self.random_choice(available_heroes)
        else:
            # Fall back to business-appropriate hero
            return self.get_business_appropriate_hero(industry, hero_styles)

    def get_theme_appropriate_grid(self, visual_theme, grid_systems):
        """Select grid system based on visual theme"""
        theme_name = visual_theme["name"]

        theme_grid_preferences = {
            "minimalist_clean": ["three_column_equal", "two_column_sidebar", "asymmetric_grid"],
            "bold_expressive": ["magazine_layout", "diagonal_grid", "pinterest_masonry"],
            "organic_natural": ["pinterest_masonry", "circular_arrangement", "asymmetric_grid"],
            "tech_modern": ["four_column_masonry", "hexagonal_grid", "timeline_vertical"],
            "artistic_creative": ["magazine_layout", "asymmetric_grid", "circular_arrangement"],
            "professional_corporate": ["three_column_equal", "four_column_masonry", "accordion_sections"]
        }

        preferred_grids = theme_grid_preferences.get(theme_name, grid_systems)
        available_grids = [grid for grid in preferred_grids if grid in grid_systems]

        return self.random_choice(available_grids) if available_grids else self.random_choice(grid_systems)

    def get_theme_appropriate_typography(self, visual_theme, industry, font_pairings):
        """Select typography based on visual theme and industry"""
        theme_name = visual_theme["name"]

        theme_typography_preferences = {
            "minimalist_clean": ["modern_professional", "minimal_geometric"],
            "bold_expressive": ["bold_statement", "artistic_creative"],
            "organic_natural": ["friendly_approachable", "warm_humanist"],
            "tech_modern": ["tech_futuristic", "modern_professional", "minimal_geometric"],
            "artistic_creative": ["artistic_creative", "playful_modern"],
            "professional_corporate": ["elegant_contrast", "classic_traditional", "modern_professional"]
        }

        preferred_typography = theme_typography_preferences.get(theme_name, [])
        available_typography = [font for font in font_pairings if font["name"] in preferred_typography]

        if available_typography:
            return self.random_choice(available_typography)
        else:
            # Fall back to business-appropriate typography
            return self.get_business_appropriate_typography(industry, font_pairings)

    def get_theme_appropriate_button(self, visual_theme, button_styles):
        """Select button style based on visual theme"""
        theme_name = visual_theme["name"]

        theme_button_preferences = {
            "minimalist_clean": ["rounded_modern", "sharp_corporate"],
            "bold_expressive": ["geometric_bold", "neon_glow"],
            "organic_natural": ["soft_friendly", "organic_blob"],
            "tech_modern": ["sharp_corporate", "neon_glow"],
            "artistic_creative": ["organic_blob", "vintage_classic"],
            "professional_corporate": ["rounded_modern", "sharp_corporate", "vintage_classic"]
        }

        preferred_buttons = theme_button_preferences.get(theme_name, [])
        available_buttons = [btn for btn in button_styles if btn["name"] in preferred_buttons]

        return self.random_choice(available_buttons) if available_buttons else self.random_choice(button_styles)

    def get_theme_appropriate_card(self, visual_theme, card_styles):
        """Select card style based on visual theme"""
        theme_name = visual_theme["name"]

        theme_card_preferences = {
            "minimalist_clean": ["outlined_minimal", "elevated_modern"],
            "bold_expressive": ["geometric_sharp", "neon_border"],
            "organic_natural": ["soft_organic", "paper_torn"],
            "tech_modern": ["floating_glass", "geometric_sharp"],
            "artistic_creative": ["paper_torn", "floating_glass"],
            "professional_corporate": ["elevated_modern", "outlined_minimal"]
        }

        preferred_cards = theme_card_preferences.get(theme_name, [])
        available_cards = [card for card in card_styles if card["name"] in preferred_cards]

        return self.random_choice(available_cards) if available_cards else self.random_choice(card_styles)

    def generate_variation(self, template_spec: Dict) -> Dict:
        # Get business type from business_info for industry-specific design choices
        business_info = template_spec.get("business_info", {})
        business_type = business_info.get("business_type", "Service Business")

        # Map business type to industry key (lowercase for consistency)
        industry = business_type.lower()

        # Check for custom color palette first
        color_palette_info = template_spec.get("color_palette", {})
        has_custom_colors = color_palette_info.get("has_custom_palette", False)

        config = self.config  # from .json passed into constructor

        # Select a visual theme first - this will influence all other choices
        visual_theme = self.random_choice(config["variation_strategies"]["visual_themes"])
        print(f"🎨 Selected Visual Theme: {visual_theme['name']} - {visual_theme['description']}")

        if has_custom_colors:
            print(f"🎨 Using CUSTOM color palette specified in request for {business_type} business")
            specified_colors = color_palette_info.get("specified_colors", [])
            for color in specified_colors:
                print(f"   🎨 Custom Color: {color['name']} = {color['hex']} ({color['description']})")
        else:
            # Color palette - use business-specific colors
            industry_colors = config["variation_strategies"]["color_generation"]["industry_influences"].get(industry, ["blues", "greens"])
            print(f"🎨 Generating design for {business_type} business with {industry} color palette: {industry_colors}")

        # Choose color strategy based on visual theme
        color_palette = self.get_theme_appropriate_color_strategy(visual_theme, config["variation_strategies"]["color_generation"]["methods"])

        # Layout - theme and business-appropriate choices
        hero_layout = self.get_theme_appropriate_hero(visual_theme, industry, config["variation_strategies"]["layout_variations"]["hero_styles"])
        section_order = self.random_choice(config["variation_strategies"]["layout_variations"]["section_arrangements"])
        grid_system = self.get_theme_appropriate_grid(visual_theme, config["variation_strategies"]["layout_variations"]["grid_systems"])

        # Typography - theme-appropriate choices
        typography = self.get_theme_appropriate_typography(visual_theme, industry, config["variation_strategies"]["typography_variations"]["font_pairings"])
        font_scale = self.random_choice(config["variation_strategies"]["typography_variations"]["size_scales"])

        # Components - theme-appropriate styles
        button_style = self.get_theme_appropriate_button(visual_theme, config["variation_strategies"]["component_variations"]["button_styles"])
        card_style = self.get_theme_appropriate_card(visual_theme, config["variation_strategies"]["component_variations"]["card_styles"])

        # Unique elements - multiple for more variation
        background_pattern = self.random_choice(config["unique_elements_library"]["background_patterns"])
        decoration = self.random_choice(config["unique_elements_library"]["decorative_elements"])
        interaction = self.random_choice(config["unique_elements_library"]["interaction_styles"])
        layout_modifier = self.random_choice(config["unique_elements_library"]["layout_modifiers"])

        # Add some randomness - sometimes pick completely different elements
        if random.random() < 0.3:  # 30% chance for creative deviation
            print("🎲 Adding creative deviation to design choices")
            hero_layout = self.random_choice(config["variation_strategies"]["layout_variations"]["hero_styles"])
            button_style = self.random_choice(config["variation_strategies"]["component_variations"]["button_styles"])

        return {
            "variation_id": self.generate_variation_id(),
            "visual_theme": visual_theme,
            "color_palette_strategy": color_palette,
            "typography_scheme": {
                "pairing": typography,
                "scale": font_scale
            },
            "layout_structure": {
                "hero": hero_layout,
                "section_order": section_order,
                "grid": grid_system,
                "modifier": layout_modifier
            },
            "component_styles": {
                "button": button_style,
                "card": card_style
            },
            "animation_preferences": [interaction],
            "unique_elements": [background_pattern, decoration],
            "creative_deviation": random.random() < 0.3
        }
