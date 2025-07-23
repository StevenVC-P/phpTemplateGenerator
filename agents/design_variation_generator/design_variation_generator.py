import json
import random
import time
import hashlib
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
        # Track recent combinations to avoid repetition
        self.recent_combinations = []
        self.max_recent_combinations = 10
        # Ensure true randomness by seeding with current time and process info
        seed = int(time.time() * 1000000) % 2**32
        random.seed(seed)
        print(f"🎲 Design variation generator seeded with: {seed}")

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
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # Add microseconds and random component for uniqueness
        microseconds = datetime.now().microsecond
        random_component = random.randint(1000, 9999)
        return f"variation_{timestamp}_{microseconds}_{random_component}"

    def random_choice(self, options):
        return random.choice(options) if options else None

    def weighted_hero_choice(self, hero_styles):
        """Select hero style with weighted preference for complex layouts and avoiding recent choices"""
        if not hero_styles:
            return None

        # Get recently used hero styles
        recent_hero_names = [combo.get("hero", "") for combo in self.recent_combinations]

        # Create weights favoring complex layouts and penalizing recent choices
        weights = []
        for style in hero_styles:
            complexity = style.get("complexity", "simple")
            base_weight = 3 if complexity == "high" else (2 if complexity == "medium" else 1)

            # Reduce weight if recently used
            if style["name"] in recent_hero_names:
                base_weight = max(1, base_weight // 3)  # Significantly reduce but don't eliminate

            weights.append(base_weight)

        return random.choices(hero_styles, weights=weights, k=1)[0]

    def generate_variation(self, template_spec: Dict) -> Dict:
        # Re-seed for each variation to ensure uniqueness
        current_seed = int(time.time() * 1000000 + random.randint(0, 10000)) % 2**32
        random.seed(current_seed)

        industry = template_spec.get("project_type", "local_services")
        business_name = template_spec.get("business_name", "Business")
        config = self.config  # from .json passed into constructor

        print(f"🎨 Generating variation for {business_name} (seed: {current_seed})")

        # Color palette - add more randomness
        industry_colors = config["variation_strategies"]["color_generation"]["industry_influences"].get(industry, ["blues", "greens"])
        color_methods = config["variation_strategies"]["color_generation"]["methods"]
        # Shuffle the methods to avoid patterns
        random.shuffle(color_methods)
        color_palette = color_methods[0]

        # Layout - use weighted selection for hero styles
        hero_styles = config["variation_strategies"]["layout_variations"]["hero_styles"]
        hero_layout = self.weighted_hero_choice(hero_styles)

        section_arrangements = config["variation_strategies"]["layout_variations"]["section_arrangements"]
        random.shuffle(section_arrangements)
        section_order = section_arrangements[0]

        grid_systems = config["variation_strategies"]["layout_variations"]["grid_systems"]
        random.shuffle(grid_systems)
        grid_system = grid_systems[0]

        # Typography - ensure variety
        font_pairings = config["variation_strategies"]["typography_variations"]["font_pairings"]
        random.shuffle(font_pairings)
        typography = font_pairings[0]

        font_scales = config["variation_strategies"]["typography_variations"]["size_scales"]
        random.shuffle(font_scales)
        font_scale = font_scales[0]

        # Components - randomize order
        button_styles = config["variation_strategies"]["component_variations"]["button_styles"]
        random.shuffle(button_styles)
        button_style = button_styles[0]

        card_styles = config["variation_strategies"]["component_variations"]["card_styles"]
        random.shuffle(card_styles)
        card_style = card_styles[0]

        # Unique elements - select multiple for more variety
        background_patterns = config["unique_elements_library"]["background_patterns"]
        decorative_elements = config["unique_elements_library"]["decorative_elements"]
        interaction_styles = config["unique_elements_library"]["interaction_styles"]
        layout_effects = config["unique_elements_library"].get("layout_effects", [])

        # Select 2-3 unique elements for more complexity
        num_elements = random.randint(2, 4)
        all_elements = background_patterns + decorative_elements + layout_effects
        random.shuffle(all_elements)
        unique_elements = all_elements[:num_elements]

        # Select interaction style
        random.shuffle(interaction_styles)
        interaction = interaction_styles[0]

        print(f"   Selected: {hero_layout['name']} hero, {color_palette} colors, {typography['name']} typography")

        variation_data = {
            "variation_id": self.generate_variation_id(),
            "generation_seed": current_seed,
            "business_context": business_name,
            "color_palette_strategy": color_palette,
            "typography_scheme": {
                "pairing": typography,
                "scale": font_scale
            },
            "layout_structure": {
                "hero": hero_layout,
                "section_order": section_order,
                "grid": grid_system
            },
            "component_styles": {
                "button": button_style,
                "card": card_style
            },
            "animation_preferences": [interaction],
            "unique_elements": unique_elements,
            "complexity_score": self.calculate_complexity_score(hero_layout, unique_elements, interaction)
        }

        print(f"   Complexity Score: {variation_data['complexity_score']}/10")

        # Track this combination to avoid repetition
        combination_key = {
            "hero": hero_layout["name"],
            "colors": color_palette,
            "typography": typography["name"]
        }
        self.recent_combinations.append(combination_key)

        # Keep only recent combinations
        if len(self.recent_combinations) > self.max_recent_combinations:
            self.recent_combinations.pop(0)

        return variation_data

    def calculate_complexity_score(self, hero_layout, unique_elements, interaction):
        """Calculate visual complexity score (1-10)"""
        score = 1

        # Hero complexity
        complexity = hero_layout.get("complexity", "simple")
        if complexity == "high":
            score += 4
        elif complexity == "medium":
            score += 2

        # Unique elements add complexity
        score += len(unique_elements)

        # Advanced interactions add complexity
        advanced_interactions = ["magnetic_hover_effects", "morphing_transitions", "parallax_scrolling", "liquid_animations"]
        if interaction in advanced_interactions:
            score += 2

        return min(score, 10)
