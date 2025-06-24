#!/usr/bin/env python3
"""
Test the agent chain with fixed paths
"""

import asyncio
import logging
from pathlib import Path
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_agent_chain():
    """Test the first few agents in sequence"""
    print("🔗 Testing Agent Chain")
    print("=" * 40)
    
    # Initialize pipeline
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    pipeline_id = pipeline.generate_pipeline_id()
    
    # Set up request file
    request_file = "input/example-request.md"
    if not Path(request_file).exists():
        print(f"❌ Request file not found: {request_file}")
        return
    
    pipeline.pipeline_state[pipeline_id] = {
        'request_file': request_file,
        'start_time': '2025-06-24T14:40:00',
        'status': 'running'
    }
    
    print(f"🆔 Pipeline ID: {pipeline_id}")
    print(f"📄 Request file: {request_file}")
    
    # Test agents in sequence
    agents_to_test = [
        "request_interpreter",
        "design_variation_generator",
        "prompt_designer"
    ]
    
    for i, agent_id in enumerate(agents_to_test, 1):
        print(f"\n{'='*20} STEP {i}: {agent_id} {'='*20}")
        
        if agent_id not in pipeline.agents:
            print(f"❌ Agent {agent_id} not loaded")
            continue
        
        # Show input/output paths
        input_path = pipeline.get_input_path(agent_id, pipeline_id)
        output_path = pipeline.get_output_path(agent_id, pipeline_id)
        
        print(f"📥 Input:  {input_path}")
        print(f"📤 Output: {output_path}")
        
        # Check if input exists
        if input_path and Path(input_path).exists():
            print(f"✅ Input file exists: {Path(input_path).stat().st_size} bytes")
        else:
            print(f"❌ Input file missing: {input_path}")
        
        try:
            result = await pipeline.run_agent(agent_id, pipeline_id)
            
            if result.success:
                print(f"✅ {agent_id} SUCCESS")
                print(f"   Output: {result.output_file}")
                
                # Check if output file exists
                if result.output_file and Path(result.output_file).exists():
                    size = Path(result.output_file).stat().st_size
                    print(f"   File size: {size} bytes")
                    
                    # Show content preview for JSON files
                    if result.output_file.endswith('.json'):
                        try:
                            import json
                            content = json.loads(Path(result.output_file).read_text())
                            print(f"   JSON keys: {list(content.keys())[:5]}...")
                        except:
                            pass
                else:
                    print(f"   ⚠️ Output file not found")
            else:
                print(f"❌ {agent_id} FAILED: {result.message}")
                print("   🛑 Stopping chain test")
                break
                
        except Exception as e:
            print(f"❌ {agent_id} ERROR: {e}")
            print("   🛑 Stopping chain test")
            break
    
    print(f"\n🎉 Chain testing completed!")

if __name__ == "__main__":
    asyncio.run(test_agent_chain())
