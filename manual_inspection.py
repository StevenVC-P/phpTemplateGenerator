#!/usr/bin/env python3
"""
Manual Active Agents Inspection
Step-by-step execution with detailed inspection of each agent
"""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure detailed logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ManualInspector:
    def __init__(self):
        self.config = PipelineConfig()
        self.pipeline = TemplatePipeline(self.config)
        self.pipeline_id = None
        self.results = {}
        
    def print_separator(self, title: str, char: str = "="):
        print(f"\n{char * 60}")
        print(f"🔍 {title}")
        print(f"{char * 60}")
    
    def print_step(self, step: int, title: str):
        print(f"\n{'=' * 20} STEP {step}: {title} {'=' * 20}")
    
    def inspect_agent_config(self, agent_id: str):
        """Inspect agent configuration"""
        if agent_id in self.pipeline.agents:
            agent_info = self.pipeline.agents[agent_id]
            print(f"📋 Agent Configuration for {agent_id}:")
            print(f"   • Class: {agent_info.get('class', 'N/A')}")
            print(f"   • Active: {agent_info.get('is_active', False)}")
            print(f"   • Config keys: {list(agent_info.get('config', {}).keys())}")
            
            # Show some config details
            config = agent_info.get('config', {})
            if 'capabilities' in config:
                print(f"   • Capabilities: {config['capabilities'][:3]}..." if len(config['capabilities']) > 3 else f"   • Capabilities: {config['capabilities']}")
            if 'input_format' in config:
                print(f"   • Input format: {config['input_format']}")
            if 'output_format' in config:
                print(f"   • Output format: {config['output_format']}")
        else:
            print(f"❌ Agent {agent_id} not found in pipeline.agents")
    
    def inspect_file_system(self, description: str):
        """Inspect current file system state"""
        print(f"\n📁 File System State: {description}")
        
        # Check key directories
        dirs_to_check = [
            "input", "specs", "prompts", "templates", 
            "reviews", "design_variations", "final", "template_generations"
        ]
        
        for dir_name in dirs_to_check:
            dir_path = Path(dir_name)
            if dir_path.exists():
                files = list(dir_path.glob("*"))
                print(f"   📂 {dir_name}/: {len(files)} files")
                # Show recent files
                for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:2]:
                    print(f"      📄 {file.name}")
            else:
                print(f"   📂 {dir_name}/: (not found)")
    
    def inspect_agent_output(self, agent_id: str, result):
        """Inspect agent execution result"""
        print(f"\n📊 Agent {agent_id} Result:")
        print(f"   • Success: {result.success}")
        print(f"   • Output file: {result.output_file}")
        print(f"   • Message: {result.message}")
        
        # Try to inspect output file if it exists
        if result.output_file and Path(result.output_file).exists():
            output_path = Path(result.output_file)
            print(f"   • File size: {output_path.stat().st_size} bytes")
            print(f"   • File type: {output_path.suffix}")
            
            # Show content preview for small files
            if output_path.suffix in ['.json', '.md'] and output_path.stat().st_size < 2000:
                try:
                    content = output_path.read_text()
                    if output_path.suffix == '.json':
                        data = json.loads(content)
                        print(f"   • JSON keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    print(f"   • Content preview: {content[:200]}...")
                except Exception as e:
                    print(f"   • Content preview failed: {e}")
        else:
            print(f"   • Output file not found or not specified")
    
    async def run_single_agent(self, agent_id: str, step_num: int):
        """Run a single agent with detailed inspection"""
        self.print_step(step_num, f"Running {agent_id}")
        
        # Pre-execution inspection
        print(f"\n🔍 Pre-execution inspection:")
        self.inspect_agent_config(agent_id)
        
        # Get input/output paths
        input_path = self.pipeline.get_input_path(agent_id, self.pipeline_id)
        output_path = self.pipeline.get_output_path(agent_id, self.pipeline_id)
        
        print(f"\n📥 Input path: {input_path}")
        print(f"📤 Output path: {output_path}")
        
        # Check if input exists
        if input_path and Path(input_path).exists():
            print(f"✅ Input file exists: {Path(input_path).stat().st_size} bytes")
        else:
            print(f"❌ Input file missing: {input_path}")
        
        # Execute agent
        print(f"\n🚀 Executing {agent_id}...")
        try:
            result = await self.pipeline.run_agent(agent_id, self.pipeline_id)
            self.results[agent_id] = result
            
            # Post-execution inspection
            print(f"\n🔍 Post-execution inspection:")
            self.inspect_agent_output(agent_id, result)
            
            return result
            
        except Exception as e:
            print(f"❌ Agent execution failed: {e}")
            return None
    
    def wait_for_user(self, message: str = "Press Enter to continue..."):
        """Wait for user input"""
        print(f"\n⏸️  {message}")
        input()
    
    async def manual_pipeline_run(self):
        """Run the pipeline manually with inspection at each step"""
        self.print_separator("MANUAL ACTIVE AGENTS PIPELINE INSPECTION")
        
        # Initialize
        print(f"📋 Loaded {len(self.pipeline.agents)} active agents")
        for agent_id in self.pipeline.agents:
            print(f"   • {agent_id}")
        
        # Generate pipeline ID
        self.pipeline_id = self.pipeline.generate_pipeline_id()
        print(f"\n🆔 Pipeline ID: {self.pipeline_id}")
        
        # Set up request file
        request_file = "input/example-request.md"
        if not Path(request_file).exists():
            print(f"❌ Request file not found: {request_file}")
            return
        
        self.pipeline.pipeline_state[self.pipeline_id] = {
            'request_file': request_file,
            'start_time': datetime.now().isoformat(),
            'status': 'running'
        }
        
        print(f"📄 Request file: {request_file}")
        
        # Initial file system state
        self.inspect_file_system("Initial state")
        
        self.wait_for_user("Ready to start pipeline? Press Enter...")
        
        # Run each agent in the pipeline
        pipeline_agents = [
            "request_interpreter",
            "design_variation_generator", 
            "prompt_designer",
            "template_engineer",
            "cta_optimizer",
            "code_reviewer",
            "design_critic",
            "visual_inspector",
            "refinement_orchestrator",
            "packager"
        ]
        
        for i, agent_id in enumerate(pipeline_agents, 1):
            if agent_id in self.pipeline.agents:
                result = await self.run_single_agent(agent_id, i)
                
                # File system state after each agent
                self.inspect_file_system(f"After {agent_id}")
                
                if not result or not result.success:
                    print(f"\n❌ Pipeline halted at {agent_id}")
                    self.wait_for_user("Agent failed. Continue anyway?")
                else:
                    print(f"\n✅ {agent_id} completed successfully")
                
                if i < len(pipeline_agents):
                    self.wait_for_user(f"Continue to next agent ({pipeline_agents[i] if i < len(pipeline_agents) else 'done'})?")
            else:
                print(f"\n⚠️ Skipping {agent_id} - not loaded")
        
        # Final summary
        self.print_separator("PIPELINE EXECUTION SUMMARY")
        
        successful_agents = [aid for aid, result in self.results.items() if result and result.success]
        failed_agents = [aid for aid, result in self.results.items() if not result or not result.success]
        
        print(f"✅ Successful agents ({len(successful_agents)}):")
        for agent_id in successful_agents:
            result = self.results[agent_id]
            print(f"   • {agent_id}: {result.output_file}")
        
        if failed_agents:
            print(f"\n❌ Failed agents ({len(failed_agents)}):")
            for agent_id in failed_agents:
                result = self.results.get(agent_id)
                error = result.message if result else "No result"
                print(f"   • {agent_id}: {error}")
        
        # Final file system state
        self.inspect_file_system("Final state")
        
        print(f"\n🎉 Manual inspection completed!")
        print(f"📊 Success rate: {len(successful_agents)}/{len(self.results)} agents")

async def main():
    """Main inspection function"""
    inspector = ManualInspector()
    await inspector.manual_pipeline_run()

if __name__ == "__main__":
    asyncio.run(main())
