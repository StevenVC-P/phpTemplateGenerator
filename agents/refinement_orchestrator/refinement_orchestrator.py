import json
import shutil
from pathlib import Path
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

class RefinementOrchestrator:
    def __init__(self, config: Dict):
        self.config = config

    async def run(self, input_file: str, pipeline_id: str) -> AgentResult:
        try:
            input_dir = Path(input_file)
            output_dir = Path(f"refinements/template_{pipeline_id}")
            output_dir.mkdir(parents=True, exist_ok=True)

            required_files = [
                "template_001.php",
                "template_001.review.json",
                "template_001.design.md",
                "template_001.visual_analysis.json"
            ]

            missing = [f for f in required_files if not (input_dir / f).exists()]
            if missing:
                raise FileNotFoundError(f"Missing required files: {missing}")

            visual_score = self.extract_score(input_dir / "template_001.visual_analysis.json", "visual_score")
            conversion_score = self.extract_score(input_dir / "template_001.visual_analysis.json", "conversion_score")
            code_score = self.extract_score(input_dir / "template_001.review.json", "overall_score")

            satisfied = self.evaluate_satisfaction(visual_score, conversion_score, code_score)

            # Write report
            result_data = {
                "iteration_summary": {
                    "visual_score": visual_score,
                    "conversion_score": conversion_score,
                    "code_score": code_score,
                    "satisfaction_met": satisfied
                }
            }

            report_path = output_dir / "satisfaction_report.json"
            report_path.write_text(json.dumps(result_data, indent=2))

            # Promote template if satisfied
            if satisfied:
                shutil.copy(input_dir / "template_001.php", output_dir / "index.php")

            return AgentResult(
                agent_id="refinement_orchestrator",
                success=True,
                output_file=str(report_path),
                metadata={"satisfaction_met": satisfied}
            )

        except Exception as e:
            return AgentResult(
                agent_id="refinement_orchestrator",
                success=False,
                error_message=str(e)
            )

    def extract_score(self, json_path: Path, field: str) -> float:
        try:
            with json_path.open() as f:
                data = json.load(f)
            return data.get(field, 0)
        except Exception as e:
            print(f"⚠️ Error reading {json_path}: {e}")
            return 0

    def evaluate_satisfaction(self, visual: float, conversion: float, code: float) -> bool:
        return (
            visual >= 8.0 and
            conversion >= 8.0 and
            code >= 7.5
        )
