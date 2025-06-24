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

    def generate_variation(self, template_spec: Dict) -> Dict:
        industry = template_spec.get("project_type", "local_services")
        config = self.config  # from .json passed into constructor

        # Color palette
        industry_colors = config["variation_strategies"]["color_generation"]["industry_influences"].get(industry, ["blues", "greens"])
        color_palette = self.random_choice(config["variation_strategies"]["color_generation"]["methods"])

        # Layout
        hero_layout = self.random_choice(config["variation_strategies"]["layout_variations"]["hero_styles"])
        section_order = self.random_choice(config["variation_strategies"]["layout_variations"]["section_arrangements"])
        grid_system = self.random_choice(config["variation_strategies"]["layout_variations"]["grid_systems"])

        # Typography
        typography = self.random_choice(config["variation_strategies"]["typography_variations"]["font_pairings"])
        font_scale = self.random_choice(config["variation_strategies"]["typography_variations"]["size_scales"])

        # Components
        button_style = self.random_choice(config["variation_strategies"]["component_variations"]["button_styles"])
        card_style = self.random_choice(config["variation_strategies"]["component_variations"]["card_styles"])

        # Unique elements
        background_pattern = self.random_choice(config["unique_elements_library"]["background_patterns"])
        decoration = self.random_choice(config["unique_elements_library"]["decorative_elements"])
        interaction = self.random_choice(config["unique_elements_library"]["interaction_styles"])

        return {
            "variation_id": self.generate_variation_id(),
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
            "unique_elements": [background_pattern, decoration]
        }
