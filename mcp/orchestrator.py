import json
import os
import asyncio
import logging
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Orchestrator")

# --- Data Classes ---

@dataclass
class PipelineConfig:
    input_dir: str = "input"
    specs_dir: str = "specs"
    prompts_dir: str = "prompts"
    templates_dir: str = "templates"
    reviews_dir: str = "reviews"
    final_dir: str = "final"
    agents_dir: str = "agents"
    utils_dir: str = "utils"
    state_file: str = "pipeline_state.json"

@dataclass
class AgentResult:
    agent_id: str
    success: bool
    output_file: Optional[str] = None
    message: Optional[str] = None

# --- Orchestrator ---

class TemplatePipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.agents: Dict[str, Any] = {}
        self.pipeline_state: Dict[str, Any] = {}
        self.pipeline = [
            "request_interpreter",
            "prompt_designer",
            "design_variation_generator",
            "template_engineer",
            "cta_optimizer",
            "design_critic",
            "visual_inspector",
            "code_reviewer",
            "refinement_orchestrator",
            "packager"
        ]
        self.max_refinement_iterations = 5
        self.load_previous_state()
        self.load_agents()

    def load_previous_state(self):
        state_path = Path(self.config.state_file)
        if state_path.exists():
            self.pipeline_state = json.loads(state_path.read_text())
        else:
            self.pipeline_state = {}

    def save_state(self):
        Path(self.config.state_file).write_text(json.dumps(self.pipeline_state, indent=2))

    def load_agents(self):
        agents_root = Path(self.config.agents_dir)
        for folder in agents_root.iterdir():
            if folder.is_dir():
                agent_id = folder.name
                py_file = folder / f"{agent_id}.py"
                json_file = folder / f"{agent_id}.json"
                if py_file.exists():
                    try:
                        spec = importlib.util.spec_from_file_location(agent_id, py_file)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Look for agent class (capitalized version of agent_id)
                        class_name = ''.join(word.capitalize() for word in agent_id.split('_'))
                        agent_class = getattr(module, class_name, None)

                        if agent_class and hasattr(agent_class, 'run'):
                            config = json.loads(json_file.read_text()) if json_file.exists() else {}
                            self.agents[agent_id] = {
                                "class": agent_class,
                                "config": config,
                                "is_active": True
                            }
                            logger.info(f"✅ Loaded active agent: {agent_id}")
                        else:
                            logger.warning(f"⚠️ Agent class {class_name} not found or missing 'run' method in {agent_id}")
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to load {agent_id}: {e}")

    async def run_agent(self, agent_id: str, pipeline_id: str = None) -> AgentResult:
        if agent_id not in self.agents:
            return AgentResult(agent_id, False, message="Agent not found")

        try:
            logger.info(f"🚀 Running agent: {agent_id}")

            # Get input and output paths
            input_path = self.get_input_path(agent_id, pipeline_id or "default")
            output_path = self.get_output_path(agent_id, pipeline_id or "default")

            # Create agent instance and run
            agent_config = self.agents[agent_id]['config']
            logger.info(f"🔧 Creating {agent_id} instance with config keys: {list(agent_config.keys())}")
            agent_instance = self.agents[agent_id]['class'](agent_config)
            logger.info(f"🔧 {agent_id} instance created successfully")

            # Run the agent with proper parameters
            if hasattr(agent_instance, 'run') and callable(agent_instance.run):
                # Debug: check method signature
                is_async = asyncio.iscoroutinefunction(agent_instance.run)
                logger.info(f"🔍 {agent_id}.run - async: {is_async}, input: '{input_path}' ({type(input_path)})")

                if is_async:
                    result = await agent_instance.run(input_path, pipeline_id or "default")
                else:
                    result = await asyncio.to_thread(agent_instance.run, input_path, pipeline_id or "default")
            else:
                raise Exception(f"Agent {agent_id} does not have a callable 'run' method")

            # Handle result
            if hasattr(result, 'success') and result.success:
                self.pipeline_state[agent_id] = {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "output_file": getattr(result, 'output_file', output_path)
                }
                self.save_state()
                return AgentResult(agent_id, True, output_file=getattr(result, 'output_file', output_path), message="Completed")
            else:
                error_msg = getattr(result, 'error_message', 'Unknown error')
                raise Exception(error_msg)

        except Exception as e:
            logger.error(f"❌ Error in {agent_id}: {e}")
            self.pipeline_state[agent_id] = {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "message": str(e)
            }
            self.save_state()
            return AgentResult(agent_id, False, message=str(e))

    async def run_pipeline(self, request_file: str = None):
        logger.info("🔁 Starting pipeline execution...")

        # Generate pipeline ID
        pipeline_id = self.generate_pipeline_id()
        logger.info(f"📋 Pipeline ID: {pipeline_id}")

        # Initialize pipeline-specific state
        self.pipeline_state[pipeline_id] = {
            'request_file': request_file,
            'start_time': datetime.now().isoformat(),
            'status': 'running',
            'agents': {}
        }

        for agent_id in self.pipeline:
            # Check pipeline-specific agent state, not global
            agent_state = self.pipeline_state[pipeline_id]['agents'].get(agent_id, {})
            if agent_state.get("status") == "success":
                logger.info(f"⏩ Skipping {agent_id} (already completed in this pipeline)")
                continue

            result = await self.run_agent(agent_id, pipeline_id)

            # Store agent result in pipeline-specific state
            self.pipeline_state[pipeline_id]['agents'][agent_id] = {
                'status': 'success' if result.success else 'failed',
                'output_file': result.output_file,
                'message': result.message,
                'timestamp': datetime.now().isoformat()
            }

            if not result.success:
                logger.error(f"🛑 Pipeline halted at {agent_id}")
                break

            if agent_id == "refinement_orchestrator":
                count = agent_state.get("iteration_count", 1)
                if count > self.max_refinement_iterations:
                    logger.warning("⚠️ Max refinement iterations reached — exiting.")
                    break

        # Mark pipeline as completed
        if pipeline_id in self.pipeline_state:
            self.pipeline_state[pipeline_id]['status'] = 'completed'
            self.pipeline_state[pipeline_id]['end_time'] = datetime.now().isoformat()
            self.save_state()

        logger.info(f"✅ Pipeline {pipeline_id} completed")

    def generate_pipeline_id(self) -> str:
        from uuid import uuid4
        return f"pipeline_{uuid4().hex[:8]}"
    
    def get_input_path(self, agent_id: str, pipeline_id: str) -> str:
        # For organized template structure, use pipeline-specific paths
        if pipeline_id in self.pipeline_state and 'request_file' in self.pipeline_state[pipeline_id]:
            # Get the template directory for this pipeline
            template_dir = self.pipeline_state[pipeline_id].get('template_dir')
            if not template_dir:
                # Generate template directory name from pipeline_id
                template_dir = f"template_generations/template_{pipeline_id.replace('pipeline_', '')}"
                self.pipeline_state[pipeline_id]['template_dir'] = template_dir

            # Use organized template structure
            if agent_id == "request_interpreter":
                return self.pipeline_state[pipeline_id]['request_file']
            elif agent_id in ["prompt_designer", "design_variation_generator"]:
                # These agents need the spec file from request_interpreter
                return f"{template_dir}/specs/template_spec.json"
            elif agent_id == "template_engineer":
                return f"{template_dir}/prompts/prompt_{pipeline_id.replace('pipeline_', '')}.json"
            elif agent_id == "cta_optimizer":
                return f"{template_dir}/templates/template_{pipeline_id.replace('pipeline_', '')}.php"
            elif agent_id in ["design_critic", "code_reviewer", "visual_inspector"]:
                return f"{template_dir}/templates/template_{pipeline_id.replace('pipeline_', '')}.cta.php"
            elif agent_id == "refinement_orchestrator":
                return f"{template_dir}/reviews/"
            elif agent_id == "packager":
                return f"{template_dir}/final/"
            else:
                return ""
        else:
            # Fallback to legacy paths for testing
            if agent_id == "request_interpreter":
                return "input/example-request.md"
            elif agent_id in ["prompt_designer", "design_variation_generator"]:
                return f"{self.config.specs_dir}/template_spec.json"
            elif agent_id == "template_engineer":
                return f"{self.config.prompts_dir}/prompt_001.json"
            elif agent_id == "cta_optimizer":
                return f"{self.config.templates_dir}/template_001.php"
            elif agent_id in ["design_critic", "code_reviewer", "visual_inspector"]:
                return f"{self.config.templates_dir}/template_001.cta.php"
            elif agent_id == "refinement_orchestrator":
                return f"{self.config.reviews_dir}/"
            elif agent_id == "packager":
                return f"{self.config.final_dir}/"
            else:
                return ""

    def get_output_path(self, agent_id: str, pipeline_id: str) -> str:
        # For organized template structure, use pipeline-specific paths
        if pipeline_id in self.pipeline_state and 'request_file' in self.pipeline_state[pipeline_id]:
            # Get the template directory for this pipeline
            template_dir = self.pipeline_state[pipeline_id].get('template_dir')
            if not template_dir:
                # Generate template directory name from pipeline_id
                template_dir = f"template_generations/template_{pipeline_id.replace('pipeline_', '')}"
                self.pipeline_state[pipeline_id]['template_dir'] = template_dir

            # Use consistent naming within the template directory
            template_id = pipeline_id.replace('pipeline_', '')

            if agent_id == "request_interpreter":
                return f"{template_dir}/specs/template_spec.json"
            elif agent_id == "prompt_designer":
                return f"{template_dir}/prompts/prompt_{template_id}.json"
            elif agent_id == "design_variation_generator":
                return f"{template_dir}/design_variations/design_variation_{template_id}.json"
            elif agent_id == "template_engineer":
                return f"{template_dir}/templates/template_{template_id}.php"
            elif agent_id == "cta_optimizer":
                return f"{template_dir}/templates/template_{template_id}.cta.php"
            elif agent_id == "design_critic":
                return f"{template_dir}/reviews/template_{template_id}.design.md"
            elif agent_id == "code_reviewer":
                return f"{template_dir}/reviews/template_{template_id}.review.json"
            elif agent_id == "visual_inspector":
                return f"{template_dir}/agent_conversations/visual_inspector_{template_id}.json"
            elif agent_id == "refinement_orchestrator":
                return f"{template_dir}/refinements/refinement_{template_id}.json"
            elif agent_id == "packager":
                return f"{template_dir}/final/package_{template_id}"
            else:
                return ""
        else:
            # Fallback to legacy paths for testing
            if agent_id == "request_interpreter":
                return f"{self.config.specs_dir}/template_spec.json"
            elif agent_id == "prompt_designer":
                return f"{self.config.prompts_dir}/prompt_001.json"
            elif agent_id == "design_variation_generator":
                return f"design_variations/design_variation_001.json"
            elif agent_id == "template_engineer":
                return f"{self.config.templates_dir}/template_001.php"
            elif agent_id == "cta_optimizer":
                return f"{self.config.templates_dir}/template_001.cta.php"
            elif agent_id == "design_critic":
                return f"{self.config.reviews_dir}/template_001.design.md"
            elif agent_id == "code_reviewer":
                return f"{self.config.reviews_dir}/template_001.review.json"
            elif agent_id == "visual_inspector":
                return f"output/template_001.visual_analysis.json"
            elif agent_id == "refinement_orchestrator":
                return f"{self.config.final_dir}/refinement_001.json"
            elif agent_id == "packager":
                return f"{self.config.final_dir}/package_001"
            else:
                return ""
# --- Entry Point ---

def main(request_file: str = "input/example-request.md"):
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    asyncio.run(pipeline.run_pipeline(request_file))

if __name__ == "__main__":
    import sys
    request_file = sys.argv[1] if len(sys.argv) > 1 else "input/example-request.md"
    main(request_file)
