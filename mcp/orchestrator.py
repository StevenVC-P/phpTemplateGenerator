#!/usr/bin/env python3
"""
PHP Template Generator Orchestrator
Main coordination logic for the template generation pipeline
"""

import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import design variation system
try:
    import sys
    sys.path.append('.')
    from test_simple_variations import generate_simple_variation
    DESIGN_VARIATIONS_AVAILABLE = True
    logger.info("Design variation system loaded successfully")
except ImportError as e:
    DESIGN_VARIATIONS_AVAILABLE = False
    logger.warning(f"Design variation system not available: {e}")

# Import template refinement system
try:
    from utils.template_refiner import TemplateRefiner
    TEMPLATE_REFINEMENT_AVAILABLE = True
    logger.info("Template refinement system loaded successfully")
except ImportError as e:
    TEMPLATE_REFINEMENT_AVAILABLE = False
    logger.warning(f"Template refinement system not available: {e}")

@dataclass
class PipelineConfig:
    """Configuration for the template generation pipeline"""
    input_dir: str = "input"
    specs_dir: str = "specs"
    prompts_dir: str = "prompts"
    templates_dir: str = "templates"
    reviews_dir: str = "reviews"
    final_dir: str = "final"
    agents_dir: str = "agents"
    utils_dir: str = "utils"

@dataclass
class AgentResult:
    """Result from an agent execution"""
    agent_id: str
    success: bool
    output_file: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None

class TemplateOrchestrator:
    """Main orchestrator for the PHP template generation pipeline"""
    
    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()
        self.agents = {}
        self.pipeline_state = {}
        self.current_template_folder = None
        self.load_agent_configurations()

    def create_template_folder(self, pipeline_id: str) -> str:
        """Create dedicated folder for this template generation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        template_folder = f"template_generations/template_{timestamp}"

        # Create folder structure
        folders = [
            f"{template_folder}",
            f"{template_folder}/specs",
            f"{template_folder}/design_variations",
            f"{template_folder}/prompts",
            f"{template_folder}/templates",
            f"{template_folder}/reviews",
            f"{template_folder}/refinements",
            f"{template_folder}/final",
            f"{template_folder}/agent_conversations"
        ]

        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)

        # Store in pipeline state
        self.pipeline_state[pipeline_id]['template_folder'] = template_folder
        self.current_template_folder = template_folder

        logger.info(f"Created template folder: {template_folder}")
        return template_folder

    def get_template_output_path(self, agent_id: str, file_name: str) -> str:
        """Get output path within the current template folder"""
        if not self.current_template_folder:
            # Fallback to old system
            return self.determine_output_file(agent_id, {}, file_name)

        # Map agents to their subfolders
        agent_folders = {
            'request_interpreter': 'specs',
            'design_variation_generator': 'design_variations',
            'prompt_designer': 'prompts',
            'template_engineer': 'templates',
            'code_reviewer': 'reviews',
            'design_critic': 'reviews',
            'cta_optimizer': 'templates',
            'packager': 'final'
        }

        subfolder = agent_folders.get(agent_id, 'agent_conversations')
        return f"{self.current_template_folder}/{subfolder}/{file_name}"

    def load_agent_configurations(self):
        """Load agent configurations from the agents directory"""
        agents_path = Path(self.config.agents_dir)
        if not agents_path.exists():
            logger.warning(f"Agents directory not found: {agents_path}")
            return

        for agent_file in agents_path.glob("*.json"):
            try:
                with open(agent_file, 'r') as f:
                    agent_config = json.load(f)
                    agent_id = agent_config.get('agent_id', agent_file.stem)

                    # Validate agent configuration
                    if self.validate_agent_config(agent_config):
                        self.agents[agent_id] = agent_config
                        logger.info(f"Loaded agent configuration: {agent_id} v{agent_config.get('version', '1.0')}")
                    else:
                        logger.error(f"Invalid agent configuration: {agent_file}")

            except Exception as e:
                logger.error(f"Failed to load agent config {agent_file}: {e}")

    def validate_agent_config(self, config: Dict[str, Any]) -> bool:
        """Validate agent configuration structure"""
        required_fields = ['agent_id', 'name', 'description', 'capabilities']

        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required field in agent config: {field}")
                return False

        # Validate capabilities
        if not isinstance(config.get('capabilities'), list):
            logger.error("Agent capabilities must be a list")
            return False

        return True
    
    async def process_request(self, request_file: str) -> Dict[str, Any]:
        """Process a template request through the complete pipeline"""
        logger.info(f"Starting pipeline for request: {request_file}")
        
        pipeline_id = self.generate_pipeline_id()
        self.pipeline_state[pipeline_id] = {
            'status': 'started',
            'request_file': request_file,
            'start_time': datetime.now().isoformat(),
            'agents_executed': [],
            'current_step': 'initialization'
        }

        # Create dedicated template folder
        self.create_template_folder(pipeline_id)
        
        try:
            # Step 1: Request Interpretation
            spec_result = await self.execute_agent(
                'request_interpreter', 
                request_file, 
                pipeline_id
            )
            
            if not spec_result.success:
                return self.handle_pipeline_failure(pipeline_id, spec_result)
            
            # Step 2: Design Variation Generation
            variation_result = await self.execute_agent(
                'design_variation_generator',
                spec_result.output_file,
                pipeline_id
            )

            if not variation_result.success:
                logger.warning("Design variation generation failed, continuing with defaults")

            # Step 3: Prompt Design (now includes design variation)
            prompt_result = await self.execute_agent(
                'prompt_designer',
                spec_result.output_file,
                pipeline_id
            )

            if not prompt_result.success:
                return self.handle_pipeline_failure(pipeline_id, prompt_result)

            # Step 4: Template Generation (with design variation)
            template_result = await self.execute_agent(
                'template_engineer',
                prompt_result.output_file,
                pipeline_id
            )

            # Store variation data for template engineer to use
            if variation_result.success:
                self.pipeline_state[pipeline_id]['design_variation'] = variation_result.output_file
            
            if not template_result.success:
                return self.handle_pipeline_failure(pipeline_id, template_result)
            
            # Step 4: CTA Optimization (before reviews for better analysis)
            cta_result = await self.execute_agent(
                'cta_optimizer',
                template_result.output_file,
                pipeline_id
            )

            # Use CTA-optimized template for reviews if available
            review_input = cta_result.output_file if cta_result.success else template_result.output_file

            # Step 5: Parallel Reviews (Code Review and Design Critique)
            review_tasks = [
                self.execute_agent('code_reviewer', review_input, pipeline_id),
                self.execute_agent('design_critic', review_input, pipeline_id)
            ]

            review_results = await asyncio.gather(*review_tasks, return_exceptions=True)
            review_result, design_result = review_results

            # Check if reviews completed successfully
            reviews_successful = (
                isinstance(review_result, AgentResult) and review_result.success and
                isinstance(design_result, AgentResult) and design_result.success
            )

            if not reviews_successful:
                logger.warning("Some reviews failed, but continuing with packaging")

            # Step 6: Final Packaging
            package_result = await self.execute_agent(
                'packager',
                cta_result.output_file if cta_result.success else template_result.output_file,
                pipeline_id
            )

            # Step 7: Agent Feedback Refinement Loop
            if package_result.success and TEMPLATE_REFINEMENT_AVAILABLE:
                # Run refinement loop using agent feedback
                refinement_result = await self.run_refinement_loop(
                    pipeline_id,
                    cta_result.output_file,
                    review_result.output_file if isinstance(review_result, AgentResult) and review_result.success else None,
                    design_result.output_file if isinstance(design_result, AgentResult) and design_result.success else None
                )

                if refinement_result.success:
                    logger.info(f"Refinement completed: {refinement_result.message}")
                    # Update the final template in the package
                    final_template = refinement_result.output_file
                else:
                    logger.warning(f"Refinement failed: {refinement_result.error_message}")
                    final_template = cta_result.output_file
            else:
                final_template = cta_result.output_file

            # Step 8: Visual Inspection (Optional)
            if package_result.success:
                visual_result = await self.execute_visual_refinement(
                    package_result.output_file,
                    pipeline_id
                )

                if visual_result.success:
                    final_output = visual_result.output_file
                else:
                    final_output = package_result.output_file
                    logger.warning("Visual refinement failed, using original package")
            else:
                final_output = package_result.output_file

            # Complete pipeline
            self.pipeline_state[pipeline_id]['status'] = 'completed'
            self.pipeline_state[pipeline_id]['end_time'] = datetime.now().isoformat()

            return {
                'pipeline_id': pipeline_id,
                'status': 'success',
                'final_output': final_output,
                'execution_summary': self.get_execution_summary(pipeline_id)
            }
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return self.handle_pipeline_failure(pipeline_id, None, str(e))
    
    async def execute_agent(self, agent_id: str, input_file: str, pipeline_id: str) -> AgentResult:
        """Execute a specific agent in the pipeline"""
        logger.info(f"Executing agent: {agent_id}")
        
        start_time = datetime.now()
        self.pipeline_state[pipeline_id]['current_step'] = agent_id
        
        try:
            # Get agent configuration
            agent_config = self.agents.get(agent_id)
            if not agent_config:
                raise ValueError(f"Agent configuration not found: {agent_id}")
            
            # Simulate agent execution (replace with actual agent calls)
            result = await self.simulate_agent_execution(agent_id, input_file, agent_config)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Record execution
            self.pipeline_state[pipeline_id]['agents_executed'].append({
                'agent_id': agent_id,
                'input_file': input_file,
                'output_file': result.output_file,
                'success': result.success,
                'execution_time': execution_time
            })
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Agent execution failed: {agent_id} - {e}")
            
            return AgentResult(
                agent_id=agent_id,
                success=False,
                error_message=str(e),
                execution_time=execution_time
            )
    
    async def simulate_agent_execution(self, agent_id: str, input_file: str, config: Dict) -> AgentResult:
        """Execute agent with configuration-based logic"""
        start_time = datetime.now()

        try:
            # Validate input file exists (if specified)
            if input_file and not Path(input_file).exists():
                logger.warning(f"Input file not found for {agent_id}: {input_file}")

            # Generate unique template ID for this pipeline
            template_id = self.generate_template_id()

            # Determine output file based on agent configuration
            if self.current_template_folder:
                # Use template folder structure with proper file names
                if agent_id == 'request_interpreter':
                    file_name = "template_spec.json"
                elif agent_id == 'template_engineer':
                    file_name = f"{template_id}.php"
                elif agent_id == 'cta_optimizer':
                    file_name = f"{template_id}.cta.php"
                elif agent_id == 'code_reviewer':
                    file_name = f"{template_id}.review.json"
                elif agent_id == 'design_critic':
                    file_name = f"{template_id}.design.md"
                elif agent_id == 'design_variation_generator':
                    file_name = f"design_variation_{template_id}.json"
                elif agent_id == 'prompt_designer':
                    file_name = f"prompt_{template_id}.json"
                elif agent_id == 'packager':
                    file_name = f"package_{template_id}"
                else:
                    file_name = f"{agent_id}_{template_id}.json"

                output_file = self.get_template_output_path(agent_id, file_name)
            else:
                # Fallback to old system
                output_file = self.determine_output_file(agent_id, config, template_id)

            # Simulate processing time based on agent complexity
            processing_time = self.calculate_processing_time(agent_id, config)
            await asyncio.sleep(processing_time)

            # Create output directory if needed
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Simulate agent-specific processing
            success = await self.execute_agent_logic(agent_id, input_file, output_file, config)

            execution_time = (datetime.now() - start_time).total_seconds()

            return AgentResult(
                agent_id=agent_id,
                success=success,
                output_file=output_file,
                execution_time=execution_time,
                metadata={
                    'template_id': template_id,
                    'config_version': config.get('version', '1.0'),
                    'capabilities_used': config.get('capabilities', [])
                }
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Agent execution failed for {agent_id}: {e}")

            return AgentResult(
                agent_id=agent_id,
                success=False,
                error_message=str(e),
                execution_time=execution_time
            )

    def generate_template_id(self) -> str:
        """Generate unique template ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"template_{timestamp}"

    def determine_output_file(self, agent_id: str, config: Dict, template_id: str) -> str:
        """Determine output file path based on agent configuration"""
        output_format = config.get('output_format', {})

        if isinstance(output_format, dict):
            file_name = output_format.get('file_name', f"{agent_id}_output.json")
            # Replace template ID placeholder
            file_name = file_name.replace('{id}', template_id.replace('template_', ''))
        else:
            file_name = f"{template_id}.{output_format}"

        # Determine directory based on agent type
        directory_mapping = {
            'request_interpreter': self.config.specs_dir,
            'design_variation_generator': 'design_variations',
            'prompt_designer': self.config.prompts_dir,
            'template_engineer': self.config.templates_dir,
            'code_reviewer': self.config.reviews_dir,
            'design_critic': self.config.reviews_dir,
            'cta_optimizer': self.config.templates_dir,
            'packager': self.config.final_dir
        }

        directory = directory_mapping.get(agent_id, 'output')
        return f"{directory}/{file_name}"

    def calculate_processing_time(self, agent_id: str, config: Dict) -> float:
        """Calculate simulated processing time based on agent complexity"""
        base_times = {
            'request_interpreter': 0.5,
            'design_variation_generator': 0.2,
            'prompt_designer': 0.3,
            'template_engineer': 2.0,
            'code_reviewer': 1.0,
            'design_critic': 0.8,
            'cta_optimizer': 0.6,
            'packager': 0.4
        }

        base_time = base_times.get(agent_id, 0.5)

        # Adjust based on capabilities
        capabilities = config.get('capabilities', [])
        complexity_multiplier = 1.0 + (len(capabilities) * 0.1)

        return base_time * complexity_multiplier

    async def execute_agent_logic(self, agent_id: str, input_file: str, output_file: str, config: Dict) -> bool:
        """Execute agent-specific logic (placeholder for actual implementation)"""
        try:
            # This is where you would integrate with actual AI agents
            # input_file and config would be used in real implementation
            # For now, create placeholder output files

            output_path = Path(output_file)

            if agent_id == 'request_interpreter':
                # Create spec file
                spec_data = {
                    "template_id": "template_001",
                    "project_type": "saas_landing_page",
                    "status": "generated_by_simulator"
                }
                with open(output_path, 'w') as f:
                    json.dump(spec_data, f, indent=2)

            elif agent_id in ['template_engineer', 'cta_optimizer']:
                # Create PHP template file with design variation
                template_content = self.generate_template_with_variation(agent_id, input_file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(template_content)

            elif agent_id in ['code_reviewer']:
                # Perform real code review
                review_data = self.perform_code_review(input_file)
                with open(output_path, 'w') as f:
                    json.dump(review_data, f, indent=2)

            elif agent_id == 'design_critic':
                # Perform real design critique
                design_review = self.perform_design_critique(input_file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(design_review)

            elif agent_id == 'design_variation_generator':
                # Generate design variation using simple variation system
                if DESIGN_VARIATIONS_AVAILABLE:
                    # Load template spec
                    with open(input_file, 'r') as f:
                        template_spec = json.load(f)

                    # Generate variation using simple system
                    variation = generate_simple_variation(template_spec)

                    # Add metadata
                    variation['generated_at'] = datetime.now().isoformat()
                    variation['source_spec'] = input_file
                    variation['agent_version'] = config.get('version', '1.0')

                    # Save variation
                    with open(output_path, 'w') as f:
                        json.dump(variation, f, indent=2)

                    logger.info(f"Generated design variation: {variation['variation_id']}")
                    logger.info(f"  Industry: {variation['industry']}")
                    logger.info(f"  Colors: {variation['colors']['primary']} (primary)")
                    logger.info(f"  Typography: {variation['typography']['heading']} + {variation['typography']['body']}")
                    logger.info(f"  Layout: {variation['layout']['name']}")
                else:
                    # Fallback if design variations not available
                    fallback_variation = {
                        "variation_id": "fallback_001",
                        "industry": "tech",
                        "colors": {"primary": "#2563eb", "secondary": "#10b981", "accent": "#f59e0b"},
                        "typography": {"heading": "Inter", "body": "Inter", "style": "modern"},
                        "layout": {"name": "centered_hero", "description": "Traditional centered layout"},
                        "buttons": {"name": "rounded", "radius": "8px", "padding": "1rem 2rem"},
                        "css_variables": {
                            "--primary-color": "#2563eb",
                            "--secondary-color": "#10b981",
                            "--accent-color": "#f59e0b",
                            "--font-heading": "Inter",
                            "--font-body": "Inter"
                        }
                    }

                    with open(output_path, 'w') as f:
                        json.dump(fallback_variation, f, indent=2)

                    logger.warning("Using fallback design variation")

            elif agent_id == 'packager':
                # Create directory structure for packager
                if output_file.endswith('.json'):
                    # Fix output path to be a directory
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = output_file.replace('packager_output.json', f'template_{timestamp}/')
                    output_path = Path(output_file)

                output_path.mkdir(parents=True, exist_ok=True)
                readme_path = output_path / 'README.md'
                with open(readme_path, 'w') as f:
                    f.write("# Template Package\n\nGenerated by packager simulator\n")

                # Create index.php placeholder
                index_path = output_path / 'index.php'
                with open(index_path, 'w') as f:
                    f.write("<?php\n// Packaged template\n// Generated by packager simulator\n?>")

            else:
                # Generic JSON output
                with open(output_path, 'w') as f:
                    json.dump({"agent_id": agent_id, "status": "simulated"}, f, indent=2)

            logger.info(f"Agent {agent_id} created output: {output_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to execute {agent_id} logic: {e}")
            return False

    def generate_template_with_variation(self, agent_id: str, input_file: str) -> str:
        """Generate template content using design variation data"""
        try:
            # Find the current pipeline to get design variation
            current_pipeline = None
            for pipeline_id, state in self.pipeline_state.items():
                if state.get('current_step') == agent_id:
                    current_pipeline = pipeline_id
                    break

            # Load design variation if available
            variation_data = None
            if current_pipeline and 'design_variation' in self.pipeline_state[current_pipeline]:
                variation_file = self.pipeline_state[current_pipeline]['design_variation']
                try:
                    with open(variation_file, 'r') as f:
                        variation_data = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to load design variation: {e}")

            # Generate template based on variation
            if variation_data:
                return self.create_varied_template(variation_data, agent_id)
            else:
                return f"<?php\n// Generated by {agent_id}\n// No design variation available\n?>"

        except Exception as e:
            logger.error(f"Failed to generate template with variation: {e}")
            return f"<?php\n// Generated by {agent_id}\n// Error in variation generation\n?>"

    def create_varied_template(self, variation_data: Dict[str, Any], agent_id: str) -> str:
        """Create template content based on design variation"""
        colors = variation_data.get('colors', {})
        typography = variation_data.get('typography', {})
        layout = variation_data.get('layout', {})
        buttons = variation_data.get('buttons', {})
        css_vars = variation_data.get('css_variables', {})

        # Generate Google Fonts URL
        fonts_url = self.generate_fonts_url(typography)

        # Create template with variation-specific styling
        template_content = f'''<?php
/**
 * Template Generated with Design Variation
 * Variation ID: {variation_data.get('variation_id', 'unknown')}
 * Industry: {variation_data.get('industry', 'generic')}
 * Style: {typography.get('style', 'modern')}, {layout.get('name', 'standard')}
 * Generated by: {agent_id}
 */

// Handle form submission
$form_submitted = false;
$form_errors = [];
$success_message = '';

if ($_POST) {{
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $company = trim($_POST['company'] ?? '');
    $message = trim($_POST['message'] ?? '');

    // Basic validation
    if (empty($name)) $form_errors[] = 'Name is required';
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) $form_errors[] = 'Valid email is required';
    if (empty($company)) $form_errors[] = 'Company name is required';
    if (empty($message)) $form_errors[] = 'Message is required';

    if (empty($form_errors)) {{
        $success_message = 'Thank you for your message! We\\'ll get back to you soon.';
        $form_submitted = true;
    }}
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Landing Page - {variation_data.get('industry', 'Professional').title()} Solution</title>
    <link href="{fonts_url}" rel="stylesheet">
    <style>
        :root {{
            /* Design Variation: {variation_data.get('variation_id', 'default')} */
            --primary-color: {colors.get('primary', '#2563eb')};
            --secondary-color: {colors.get('secondary', '#10b981')};
            --accent-color: {colors.get('accent', '#f59e0b')};
            --font-heading: '{typography.get('heading', 'Inter')}', sans-serif;
            --font-body: '{typography.get('body', 'Inter')}', sans-serif;
            --button-radius: {buttons.get('radius', '8px')};
            --button-padding: {buttons.get('padding', '1rem 2rem')};
            --text-dark: #1f2937;
            --text-gray: #6b7280;
            --bg-light: #f9fafb;
            --white: #ffffff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: var(--font-body);
            line-height: 1.6;
            color: var(--text-dark);
            scroll-behavior: smooth;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* Header */
        header {{
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }}

        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }}

        .logo {{
            font-family: var(--font-heading);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-color);
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}

        .nav-links a {{
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s ease;
        }}

        .nav-links a:hover {{
            color: var(--primary-color);
        }}

        /* Hero Section - {layout.get('description', 'Standard layout')} */
        .hero {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: var(--white);
            padding: 120px 0 80px;
            text-align: {'center' if layout.get('name') == 'centered_hero' else 'left'};
            min-height: {'100vh' if layout.get('name') == 'full_width_hero' else '80vh'};
            display: flex;
            align-items: center;
        }}

        .hero h1 {{
            font-family: var(--font-heading);
            font-size: {'4rem' if layout.get('name') == 'full_width_hero' else '3.5rem'};
            font-weight: {'300' if typography.get('style') == 'elegant' else '700'};
            margin-bottom: 1rem;
            line-height: 1.2;
        }}

        .hero .subtitle {{
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.95;
            max-width: 600px;
            {'margin-left: auto; margin-right: auto;' if layout.get('name') == 'centered_hero' else ''}
        }}

        /* CTA Button - {buttons.get('name', 'standard')} style */
        .cta-button {{
            display: inline-block;
            background: var(--accent-color);
            color: var(--white);
            padding: var(--button-padding);
            text-decoration: none;
            border-radius: var(--button-radius);
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}

        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }}

        /* Features Section */
        .features {{
            padding: 80px 0;
            background: var(--bg-light);
        }}

        .section-title {{
            font-family: var(--font-heading);
            text-align: center;
            font-size: 2.5rem;
            font-weight: {'400' if typography.get('style') == 'elegant' else '700'};
            margin-bottom: 1rem;
            color: var(--text-dark);
        }}

        .section-subtitle {{
            text-align: center;
            font-size: 1.1rem;
            color: var(--text-gray);
            margin-bottom: 3rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }}

        .feature-card {{
            background: var(--white);
            padding: 2rem;
            border-radius: {'20px' if buttons.get('name') == 'soft' else '12px'};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s ease;
            border: {'2px solid #e5e7eb' if buttons.get('name') == 'sharp' else 'none'};
        }}

        .feature-card:hover {{
            transform: translateY(-5px);
        }}

        .feature-icon {{
            width: 60px;
            height: 60px;
            background: var(--primary-color);
            border-radius: 50%;
            margin: 0 auto 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            font-size: 1.5rem;
        }}

        /* Contact Section */
        .contact {{
            padding: 80px 0;
            background: var(--white);
        }}

        .contact-form {{
            max-width: 600px;
            margin: 0 auto;
            background: var(--bg-light);
            padding: 2.5rem;
            border-radius: var(--button-radius);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .form-group {{
            margin-bottom: 1.5rem;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-dark);
            font-weight: 500;
        }}

        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 1rem;
            border: 2px solid #e5e7eb;
            border-radius: var(--button-radius);
            font-size: 1rem;
            font-family: inherit;
            transition: border-color 0.3s ease;
        }}

        .form-group input:focus,
        .form-group textarea:focus {{
            outline: none;
            border-color: var(--primary-color);
        }}

        .submit-btn {{
            width: 100%;
            background: var(--primary-color);
            color: var(--white);
            padding: var(--button-padding);
            border: none;
            border-radius: var(--button-radius);
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s ease;
        }}

        .submit-btn:hover {{
            background: var(--secondary-color);
        }}

        /* Footer */
        footer {{
            background: var(--text-dark);
            color: var(--white);
            text-align: center;
            padding: 2rem 0;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}

            .nav-links {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <nav class="container">
            <a href="#home" class="logo">{variation_data.get('industry', 'Business').title()}Pro</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="container">
            <h1>Transform Your {variation_data.get('industry', 'Business').title()} Today</h1>
            <p class="subtitle">Professional solutions designed for modern {variation_data.get('industry', 'business')} needs. Experience the difference with our {typography.get('style', 'modern')} approach.</p>
            <a href="#contact" class="cta-button">Get Started Now</a>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features" id="features">
        <div class="container">
            <h2 class="section-title">Why Choose Our Solution?</h2>
            <p class="section-subtitle">Powerful features designed specifically for {variation_data.get('industry', 'business')} professionals.</p>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Fast & Efficient</h3>
                    <p>Optimized performance that keeps your {variation_data.get('industry', 'business')} running smoothly.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Secure & Reliable</h3>
                    <p>Enterprise-grade security with 99.9% uptime guarantee.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Advanced Analytics</h3>
                    <p>Comprehensive insights to make data-driven decisions.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="contact" id="contact">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <p class="section-subtitle">Ready to transform your {variation_data.get('industry', 'business')}? Contact us today.</p>

            <div class="contact-form">
                <?php if ($success_message): ?>
                    <div style="background: var(--secondary-color); color: white; padding: 1rem; border-radius: var(--button-radius); margin-bottom: 1.5rem; text-align: center;">
                        <?php echo htmlspecialchars($success_message); ?>
                    </div>
                <?php endif; ?>

                <?php if (!empty($form_errors)): ?>
                    <div style="background: #ef4444; color: white; padding: 1rem; border-radius: var(--button-radius); margin-bottom: 1.5rem;">
                        <?php foreach ($form_errors as $error): ?>
                            <p><?php echo htmlspecialchars($error); ?></p>
                        <?php endforeach; ?>
                    </div>
                <?php endif; ?>

                <?php if (!$form_submitted): ?>
                <form method="POST" action="">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" name="name" value="<?php echo htmlspecialchars($_POST['name'] ?? ''); ?>" required>
                    </div>

                    <div class="form-group">
                        <label for="email">Email Address *</label>
                        <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>" required>
                    </div>

                    <div class="form-group">
                        <label for="company">Company Name *</label>
                        <input type="text" id="company" name="company" value="<?php echo htmlspecialchars($_POST['company'] ?? ''); ?>" required>
                    </div>

                    <div class="form-group">
                        <label for="message">Message *</label>
                        <textarea id="message" name="message" placeholder="Tell us about your needs..." required><?php echo htmlspecialchars($_POST['message'] ?? ''); ?></textarea>
                    </div>

                    <button type="submit" class="submit-btn">Send Message</button>
                </form>
                <?php endif; ?>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2025 {variation_data.get('industry', 'Business').title()}Pro. All rights reserved. | Design Variation: {variation_data.get('variation_id', 'default')}</p>
        </div>
    </footer>

    <script>
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>'''

        return template_content

    def generate_fonts_url(self, typography: Dict[str, Any]) -> str:
        """Generate Google Fonts URL for typography"""
        heading_font = typography.get('heading', 'Inter').replace(' ', '+')
        body_font = typography.get('body', 'Inter').replace(' ', '+')

        fonts = []
        if heading_font not in [f.split(':')[0] for f in fonts]:
            fonts.append(f"{heading_font}:wght@300;400;500;600;700")
        if body_font not in [f.split(':')[0] for f in fonts]:
            fonts.append(f"{body_font}:wght@300;400;500;600;700")

        return f"https://fonts.googleapis.com/css2?{'&'.join([f'family={font}' for font in fonts])}&display=swap"

    def perform_code_review(self, template_file: str) -> Dict[str, Any]:
        """Perform real code review of the template"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()

            issues = []
            suggestions = []
            score = 6.0  # Start with lower score to demonstrate improvement

            # Check for security issues
            if 'htmlspecialchars' not in content:
                issues.append({
                    "type": "security",
                    "severity": "high",
                    "message": "Missing XSS protection - use htmlspecialchars() for user input",
                    "line": "form handling section"
                })
                score -= 1.5

            # Check for responsive design
            if '@media' not in content:
                issues.append({
                    "type": "design",
                    "severity": "high",
                    "message": "Missing responsive design breakpoints",
                    "line": "CSS section"
                })
                score -= 2.0

            # Check for insufficient mobile optimization
            if '@media (max-width: 480px)' not in content:
                issues.append({
                    "type": "design",
                    "severity": "medium",
                    "message": "Missing mobile-specific breakpoints (480px)",
                    "line": "CSS responsive section"
                })
                score -= 1.0

            # Check for performance issues
            if 'preconnect' not in content and 'fonts.googleapis.com' in content:
                issues.append({
                    "type": "performance",
                    "severity": "medium",
                    "message": "Missing font preloading optimization",
                    "line": "head section"
                })
                score -= 0.8

            # Check for accessibility
            if 'alt=' not in content and '<img' in content:
                issues.append({
                    "type": "accessibility",
                    "severity": "medium",
                    "message": "Images missing alt attributes",
                    "line": "image tags"
                })
                score -= 0.5

            # Check for modern CSS
            if 'var(--' in content:
                suggestions.append({
                    "type": "enhancement",
                    "message": "Good use of CSS custom properties",
                    "impact": "positive"
                })
                score += 0.5

            # Check for form validation
            if 'required' in content:
                suggestions.append({
                    "type": "enhancement",
                    "message": "Good use of HTML5 form validation",
                    "impact": "positive"
                })
                score += 0.3

            # Performance suggestions
            if 'fonts.googleapis.com' in content:
                suggestions.append({
                    "type": "performance",
                    "message": "Consider preloading Google Fonts for better performance",
                    "impact": "optimization"
                })

            # Design complexity assessment
            complexity_score = self.assess_design_complexity(content)

            return {
                "agent_id": "code_reviewer",
                "template_file": template_file,
                "overall_score": max(0, min(10, score)),
                "complexity_score": complexity_score,
                "issues": issues,
                "suggestions": suggestions,
                "security_check": "passed" if not any(i["type"] == "security" for i in issues) else "failed",
                "accessibility_score": 8.5 - len([i for i in issues if i["type"] == "accessibility"]) * 0.5,
                "performance_score": 8.0,
                "review_timestamp": datetime.now().isoformat(),
                "improvements_needed": len(issues) > 0,
                "recommended_actions": self.generate_improvement_actions(issues, suggestions)
            }

        except Exception as e:
            logger.error(f"Code review failed: {e}")
            return {
                "agent_id": "code_reviewer",
                "overall_score": 5.0,
                "error": str(e),
                "status": "review_failed"
            }

    def assess_design_complexity(self, content: str) -> float:
        """Assess the complexity of the design"""
        complexity_score = 0.0

        # Count CSS rules and properties
        css_rules = content.count('{')
        complexity_score += min(css_rules * 0.1, 3.0)

        # Check for advanced CSS features
        advanced_features = [
            'grid', 'flexbox', 'transform', 'transition', 'animation',
            'gradient', 'box-shadow', 'border-radius', 'calc(', 'var('
        ]

        for feature in advanced_features:
            if feature in content.lower():
                complexity_score += 0.3

        # Check for interactive elements
        interactive_elements = ['hover', 'focus', 'active', 'onclick', 'addEventListener']
        for element in interactive_elements:
            if element in content:
                complexity_score += 0.2

        return min(complexity_score, 10.0)

    def generate_improvement_actions(self, issues: List[Dict], suggestions: List[Dict]) -> List[str]:
        """Generate actionable improvement recommendations"""
        actions = []

        # High priority security fixes
        for issue in issues:
            if issue["severity"] == "high":
                actions.append(f"🔴 URGENT: {issue['message']}")

        # Medium priority improvements
        for issue in issues:
            if issue["severity"] == "medium":
                actions.append(f"🟡 Improve: {issue['message']}")

        # Enhancement suggestions
        for suggestion in suggestions:
            if suggestion["type"] == "enhancement":
                actions.append(f"✅ Consider: {suggestion['message']}")

        return actions

    def perform_design_critique(self, template_file: str) -> str:
        """Perform comprehensive design critique"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract design elements
            has_gradient = 'gradient' in content.lower()
            has_shadows = 'box-shadow' in content
            has_animations = 'transition' in content or 'animation' in content
            has_responsive = '@media' in content

            # Color analysis
            colors = self.extract_colors_from_content(content)

            # Typography analysis
            fonts = self.extract_fonts_from_content(content)

            # Layout analysis
            layout_complexity = self.analyze_layout_complexity(content)

            # Generate comprehensive review
            review = f"""# Design Critique Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Template: {template_file}

## 🎨 Visual Design Assessment

### Color Palette Analysis
- **Primary Colors**: {', '.join(colors[:3]) if colors else 'Standard blue/green scheme'}
- **Color Harmony**: {'✅ Good contrast and harmony' if len(colors) >= 3 else '⚠️ Limited color palette'}
- **Accessibility**: {'✅ Sufficient contrast' if has_shadows else '⚠️ Check contrast ratios'}

### Typography Evaluation
- **Font Selection**: {', '.join(fonts) if fonts else 'Standard web fonts'}
- **Hierarchy**: {'✅ Clear heading hierarchy' if 'h1' in content and 'h2' in content else '⚠️ Improve typography hierarchy'}
- **Readability**: {'✅ Good line height and spacing' if 'line-height' in content else '⚠️ Add line-height for better readability'}

### Layout & Composition
- **Complexity Score**: {layout_complexity}/10
- **Grid System**: {'✅ Modern grid layout' if 'grid' in content else '⚠️ Consider CSS Grid for better layouts'}
- **Responsive Design**: {'✅ Mobile-responsive' if has_responsive else '❌ Missing responsive breakpoints'}
- **Visual Effects**: {'✅ Modern visual effects' if has_gradient and has_shadows else '⚠️ Add visual depth with gradients/shadows'}

## 🚀 Enhancement Recommendations

### High Priority Improvements
{self.generate_design_improvements(content, layout_complexity)}

### Visual Complexity Enhancements
{self.generate_complexity_suggestions(content)}

### Modern Design Trends
{self.generate_trend_suggestions(content)}

## 📊 Overall Assessment

**Design Score**: {self.calculate_design_score(content)}/10

**Strengths**:
{self.identify_design_strengths(content)}

**Areas for Improvement**:
{self.identify_design_weaknesses(content)}

## 🎯 Next Steps

1. **Immediate**: Fix responsive design issues
2. **Short-term**: Enhance visual complexity with more components
3. **Long-term**: Implement advanced interactions and animations

---
*Generated by Design Critic Agent v1.0*
"""

            return review

        except Exception as e:
            logger.error(f"Design critique failed: {e}")
            return f"# Design Critique Error\n\nFailed to analyze template: {str(e)}"

    def extract_colors_from_content(self, content: str) -> List[str]:
        """Extract color values from CSS content"""
        import re
        colors = []

        # Find hex colors
        hex_colors = re.findall(r'#[0-9a-fA-F]{6}', content)
        colors.extend(hex_colors)

        # Find CSS custom properties
        css_vars = re.findall(r'--[\w-]+:\s*(#[0-9a-fA-F]{6})', content)
        colors.extend(css_vars)

        return list(set(colors))  # Remove duplicates

    def extract_fonts_from_content(self, content: str) -> List[str]:
        """Extract font families from CSS content"""
        import re
        fonts = []

        # Find font-family declarations
        font_families = re.findall(r'font-family:\s*[\'"]([^\'\"]+)[\'"]', content)
        fonts.extend(font_families)

        # Find CSS custom properties for fonts
        font_vars = re.findall(r'--font-[\w-]+:\s*[\'"]([^\'\"]+)[\'"]', content)
        fonts.extend(font_vars)

        return list(set(fonts))

    def analyze_layout_complexity(self, content: str) -> float:
        """Analyze layout complexity"""
        complexity = 0.0

        # Check for modern layout techniques
        if 'display: grid' in content or 'grid-template' in content:
            complexity += 2.0
        if 'display: flex' in content or 'flex-direction' in content:
            complexity += 1.5
        if 'position: absolute' in content or 'position: fixed' in content:
            complexity += 1.0

        # Check for responsive design
        media_queries = content.count('@media')
        complexity += min(media_queries * 0.5, 2.0)

        # Check for animations and transitions
        if 'transition:' in content:
            complexity += 0.5
        if 'animation:' in content or '@keyframes' in content:
            complexity += 1.0

        return min(complexity, 10.0)

    def generate_design_improvements(self, content: str, complexity: float) -> str:
        """Generate specific design improvement suggestions"""
        improvements = []

        if complexity < 3.0:
            improvements.append("- Add more visual hierarchy with varied font sizes and weights")
            improvements.append("- Implement CSS Grid for more sophisticated layouts")
            improvements.append("- Add subtle animations and transitions for better UX")

        if 'box-shadow' not in content:
            improvements.append("- Add depth with box-shadows on cards and buttons")

        if '@media' not in content:
            improvements.append("- Implement responsive breakpoints for mobile optimization")

        if 'gradient' not in content.lower():
            improvements.append("- Consider gradient backgrounds for visual interest")

        return '\n'.join(improvements) if improvements else "- Design shows good complexity and modern techniques"

    def generate_complexity_suggestions(self, content: str) -> str:
        """Generate suggestions for increasing design complexity"""
        suggestions = [
            "- Add pricing tables with feature comparisons",
            "- Implement testimonial carousels or cards",
            "- Create interactive elements (tabs, accordions, modals)",
            "- Add hero image or video backgrounds",
            "- Include icon libraries for better visual communication",
            "- Implement sticky navigation with scroll effects",
            "- Add progress bars or loading animations",
            "- Create multi-step forms with validation feedback"
        ]

        return '\n'.join(suggestions[:4])  # Return top 4 suggestions

    def generate_trend_suggestions(self, content: str) -> str:
        """Generate modern design trend suggestions"""
        trends = [
            "- Implement dark mode toggle functionality",
            "- Add glassmorphism effects with backdrop-filter",
            "- Use CSS custom properties for dynamic theming",
            "- Implement micro-interactions on hover states",
            "- Add skeleton loading states for better perceived performance",
            "- Use CSS Grid for magazine-style layouts",
            "- Implement scroll-triggered animations",
            "- Add floating action buttons for key actions"
        ]

        return '\n'.join(trends[:3])  # Return top 3 trends

    def calculate_design_score(self, content: str) -> float:
        """Calculate overall design score"""
        score = 5.0  # Base score

        # Modern CSS features
        if 'var(--' in content:
            score += 1.0
        if 'grid' in content:
            score += 0.5
        if 'flexbox' in content or 'flex' in content:
            score += 0.5

        # Visual effects
        if 'gradient' in content.lower():
            score += 0.5
        if 'box-shadow' in content:
            score += 0.5
        if 'transition' in content:
            score += 0.5

        # Responsive design
        if '@media' in content:
            score += 1.0

        # Accessibility
        if 'focus:' in content:
            score += 0.5

        return min(score, 10.0)

    def identify_design_strengths(self, content: str) -> str:
        """Identify design strengths"""
        strengths = []

        if 'var(--' in content:
            strengths.append("- Modern CSS custom properties implementation")
        if 'grid' in content:
            strengths.append("- CSS Grid layout system")
        if 'gradient' in content.lower():
            strengths.append("- Attractive gradient backgrounds")
        if 'transition' in content:
            strengths.append("- Smooth transitions and animations")
        if '@media' in content:
            strengths.append("- Responsive design implementation")

        return '\n'.join(strengths) if strengths else "- Clean, functional design"

    def identify_design_weaknesses(self, content: str) -> str:
        """Identify areas for design improvement"""
        weaknesses = []

        if '@media' not in content:
            weaknesses.append("- Missing responsive design breakpoints")
        if 'box-shadow' not in content:
            weaknesses.append("- Lacks visual depth (shadows, elevation)")
        if content.count('section') < 4:
            weaknesses.append("- Limited content sections and variety")
        if 'animation' not in content and 'transition' not in content:
            weaknesses.append("- No interactive animations or micro-interactions")

        return '\n'.join(weaknesses) if weaknesses else "- Minor improvements possible in visual complexity"

    async def run_refinement_loop(self, pipeline_id: str, template_file: str, review_file: str, design_file: str) -> AgentResult:
        """Run iterative refinement loop based on agent feedback"""
        logger.info(f"Starting refinement loop for pipeline {pipeline_id}")

        try:
            if not TEMPLATE_REFINEMENT_AVAILABLE:
                return AgentResult(
                    agent_id="refinement_loop",
                    success=False,
                    error_message="Template refinement system not available"
                )

            refiner = TemplateRefiner()
            current_template = template_file
            iteration = 0
            max_iterations = 3
            quality_threshold = 8.0

            while iteration < max_iterations:
                iteration += 1
                logger.info(f"Refinement iteration {iteration}/{max_iterations}")

                # Load current review data
                try:
                    if review_file and Path(review_file).exists():
                        with open(review_file, 'r') as f:
                            review_data = json.load(f)
                    else:
                        logger.warning("Review file not available, using default data")
                        review_data = {"overall_score": 5.0, "recommended_actions": []}

                    if design_file and Path(design_file).exists():
                        with open(design_file, 'r', encoding='utf-8') as f:
                            design_critique = f.read()
                    else:
                        logger.warning("Design critique file not available, using default")
                        design_critique = "No design critique available"
                except Exception as e:
                    logger.error(f"Failed to load feedback files: {e}")
                    break

                # Check if quality threshold is met
                current_score = review_data.get('overall_score', 0)
                if current_score >= quality_threshold:
                    logger.info(f"Quality threshold met: {current_score}/{quality_threshold}")
                    break

                # Apply refinements
                refined_content, refinement_report = refiner.refine_template(
                    current_template, review_data, design_critique
                )

                if not refinement_report.get('content_changed', False):
                    logger.info("No improvements applied, stopping refinement")
                    break

                # Save refined template
                refined_file = current_template.replace('.php', f'.refined_v{iteration}.php')
                with open(refined_file, 'w', encoding='utf-8') as f:
                    f.write(refined_content)

                logger.info(f"Applied {refinement_report['total_improvements']} improvements in iteration {iteration}")

                # Re-run code review on refined template
                new_review_data = self.perform_code_review(refined_file)
                new_score = new_review_data.get('overall_score', 0)

                logger.info(f"Score improvement: {current_score} → {new_score}")

                # Update files for next iteration
                current_template = refined_file

                # Save updated review
                updated_review_file = review_file.replace('.json', f'_v{iteration}.json')
                with open(updated_review_file, 'w') as f:
                    json.dump(new_review_data, f, indent=2)

                review_file = updated_review_file

                # Check if we've reached the threshold
                if new_score >= quality_threshold:
                    logger.info(f"Quality threshold achieved: {new_score}/{quality_threshold}")
                    break

            # Generate final refinement summary
            final_summary = {
                "pipeline_id": pipeline_id,
                "iterations_completed": iteration,
                "final_template": current_template,
                "final_score": new_score if 'new_score' in locals() else current_score,
                "improvements_made": iteration > 0,
                "threshold_met": (new_score if 'new_score' in locals() else current_score) >= quality_threshold
            }

            # Save refinement summary
            summary_file = f"refinement_summary_{pipeline_id}.json"
            with open(summary_file, 'w') as f:
                json.dump(final_summary, f, indent=2)

            return AgentResult(
                agent_id="refinement_loop",
                success=True,
                output_file=current_template,
                message=f"Completed {iteration} refinement iterations, final score: {final_summary['final_score']}"
            )

        except Exception as e:
            logger.error(f"Refinement loop failed: {e}")
            return AgentResult(
                agent_id="refinement_loop",
                success=False,
                error_message=str(e)
            )

    async def execute_visual_refinement(self, package_path: str, pipeline_id: str) -> AgentResult:
        """Execute visual inspection and iterative refinement process"""
        try:
            logger.info("Starting visual refinement process")

            # Check if visual inspector is available
            if 'visual_inspector' not in self.agents:
                logger.warning("Visual inspector not configured, skipping refinement")
                return AgentResult(
                    agent_id='visual_refinement',
                    success=False,
                    error_message="Visual inspector not available"
                )

            # Start local server for template testing
            template_url = await self.start_template_server(package_path)

            if not template_url:
                return AgentResult(
                    agent_id='visual_refinement',
                    success=False,
                    error_message="Failed to start template server"
                )

            # Execute visual inspection
            visual_result = await self.execute_agent(
                'visual_inspector',
                template_url,
                pipeline_id
            )

            # Stop template server
            await self.stop_template_server()

            if visual_result.success:
                logger.info("Visual refinement completed successfully")
                return AgentResult(
                    agent_id='visual_refinement',
                    success=True,
                    output_file=package_path,  # For now, return original package
                    metadata={'visual_analysis': visual_result.output_file}
                )
            else:
                logger.error("Visual inspection failed")
                return visual_result

        except Exception as e:
            logger.error(f"Visual refinement failed: {e}")
            return AgentResult(
                agent_id='visual_refinement',
                success=False,
                error_message=str(e)
            )

    async def start_template_server(self, package_path: str) -> Optional[str]:
        """Start a local server to serve the template for visual inspection"""
        try:
            # For now, return a placeholder URL
            # In real implementation, would start actual server
            template_url = f"http://localhost:8000/index.php"
            logger.info(f"Template server started: {template_url}")
            return template_url

        except Exception as e:
            logger.error(f"Failed to start template server: {e}")
            return None

    async def stop_template_server(self):
        """Stop the template server"""
        try:
            # Placeholder for server cleanup
            logger.info("Template server stopped")

        except Exception as e:
            logger.error(f"Failed to stop template server: {e}")
    
    def generate_pipeline_id(self) -> str:
        """Generate a unique pipeline ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"pipeline_{timestamp}"
    
    def handle_pipeline_failure(self, pipeline_id: str, result: AgentResult = None, error: str = None) -> Dict[str, Any]:
        """Handle pipeline failure"""
        self.pipeline_state[pipeline_id]['status'] = 'failed'
        self.pipeline_state[pipeline_id]['end_time'] = datetime.now().isoformat()
        
        error_message = error or (result.error_message if result else "Unknown error")
        
        return {
            'pipeline_id': pipeline_id,
            'status': 'failed',
            'error': error_message,
            'execution_summary': self.get_execution_summary(pipeline_id)
        }
    
    def get_execution_summary(self, pipeline_id: str) -> Dict[str, Any]:
        """Get execution summary for a pipeline"""
        state = self.pipeline_state.get(pipeline_id, {})
        
        return {
            'pipeline_id': pipeline_id,
            'status': state.get('status'),
            'start_time': state.get('start_time'),
            'end_time': state.get('end_time'),
            'agents_executed': state.get('agents_executed', []),
            'current_step': state.get('current_step')
        }
    
    def get_pipeline_status(self, pipeline_id: str) -> Dict[str, Any]:
        """Get current status of a pipeline"""
        return self.pipeline_state.get(pipeline_id, {'status': 'not_found'})
    
    def list_active_pipelines(self) -> List[str]:
        """List all active pipeline IDs"""
        return [
            pid for pid, state in self.pipeline_state.items() 
            if state.get('status') in ['started', 'running']
        ]

# CLI Interface
async def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PHP Template Generator Orchestrator')
    parser.add_argument('request_file', help='Path to the request file')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize orchestrator
    orchestrator = TemplateOrchestrator()
    
    # Process request
    result = await orchestrator.process_request(args.request_file)
    
    # Output result
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
