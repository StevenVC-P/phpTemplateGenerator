#!/usr/bin/env python3
"""
Test the fixes for active agents
"""

import asyncio
import logging
from pathlib import Path
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_agent_fixes():
    """Test the fixed agents"""
    print("🔧 Testing Agent Fixes")
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
        'start_time': '2025-06-24T14:30:00',
        'status': 'running'
    }
    
    print(f"🆔 Pipeline ID: {pipeline_id}")
    print(f"📄 Request file: {request_file}")
    
    # Test agents that should now work
    agents_to_test = [
        "request_interpreter",
        "template_engineer", 
        "visual_inspector"
    ]
    
    for agent_id in agents_to_test:
        print(f"\n🧪 Testing {agent_id}...")
        
        if agent_id not in pipeline.agents:
            print(f"❌ Agent {agent_id} not loaded")
            continue
        
        try:
            result = await pipeline.run_agent(agent_id, pipeline_id)
            
            if result.success:
                print(f"✅ {agent_id} SUCCESS")
                print(f"   Output: {result.output_file}")
                
                # Check if output file exists
                if result.output_file and Path(result.output_file).exists():
                    size = Path(result.output_file).stat().st_size
                    print(f"   File size: {size} bytes")
                else:
                    print(f"   ⚠️ Output file not found")
            else:
                print(f"❌ {agent_id} FAILED: {result.message}")
                
        except Exception as e:
            print(f"❌ {agent_id} ERROR: {e}")
    
    print(f"\n🎉 Fix testing completed!")

if __name__ == "__main__":
    asyncio.run(test_agent_fixes())
