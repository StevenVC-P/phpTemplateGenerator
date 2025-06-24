#!/usr/bin/env python3
"""
Debug path generation
"""

from mcp.orchestrator import TemplatePipeline, PipelineConfig

def debug_paths():
    """Debug path generation"""
    print("🔍 Debugging Path Generation")
    print("=" * 40)
    
    # Initialize pipeline
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    pipeline_id = pipeline.generate_pipeline_id()
    
    # Set up request file
    request_file = "input/example-request.md"
    pipeline.pipeline_state[pipeline_id] = {
        'request_file': request_file,
        'start_time': '2025-06-24T14:30:00',
        'status': 'running'
    }
    
    print(f"🆔 Pipeline ID: {pipeline_id}")
    print(f"📄 Request file: {request_file}")
    print(f"📋 Pipeline state: {pipeline.pipeline_state}")
    
    # Test path generation for each agent
    agents = ["request_interpreter", "design_variation_generator", "template_engineer"]
    
    for agent_id in agents:
        print(f"\n🔍 {agent_id}:")
        input_path = pipeline.get_input_path(agent_id, pipeline_id)
        output_path = pipeline.get_output_path(agent_id, pipeline_id)
        
        print(f"   📥 Input:  {input_path} (type: {type(input_path)})")
        print(f"   📤 Output: {output_path} (type: {type(output_path)})")
        
        # Check if input path exists
        from pathlib import Path
        if isinstance(input_path, str) and Path(input_path).exists():
            print(f"   ✅ Input file exists")
        else:
            print(f"   ❌ Input file missing or invalid type")

if __name__ == "__main__":
    debug_paths()
