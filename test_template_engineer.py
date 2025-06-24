#!/usr/bin/env python3
"""
Test template_engineer specifically
"""

import asyncio
import logging
from pathlib import Path
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_template_engineer():
    """Test template_engineer with existing files"""
    print("🔧 Testing Template Engineer")
    print("=" * 40)
    
    # Use the existing pipeline from test_chain.py
    pipeline_id = "pipeline_e3ae66bf"
    
    # Check if files exist
    spec_file = f"template_generations/template_e3ae66bf/specs/template_spec.json"
    design_file = f"template_generations/template_e3ae66bf/design_variations/design_variation_variation_20250624144112.json"
    prompt_file = f"template_generations/template_e3ae66bf/specs/prompt_pipeline_e3ae66bf.json"
    
    print(f"📋 Checking required files:")
    print(f"   📄 Spec file: {'✅' if Path(spec_file).exists() else '❌'} {spec_file}")
    print(f"   📄 Design file: {'✅' if Path(design_file).exists() else '❌'} {design_file}")
    print(f"   📄 Prompt file: {'✅' if Path(prompt_file).exists() else '❌'} {prompt_file}")
    
    if not all(Path(f).exists() for f in [spec_file, design_file, prompt_file]):
        print("❌ Missing required files")
        return
    
    # Initialize pipeline
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    
    # Set up pipeline state
    pipeline.pipeline_state[pipeline_id] = {
        'request_file': 'input/example-request.md',
        'start_time': '2025-06-24T14:41:00',
        'status': 'running',
        'template_dir': f'template_generations/template_e3ae66bf'
    }
    
    print(f"\n🔧 Testing template_engineer...")
    
    # Get input/output paths
    input_path = pipeline.get_input_path("template_engineer", pipeline_id)
    output_path = pipeline.get_output_path("template_engineer", pipeline_id)
    
    print(f"📥 Input:  {input_path}")
    print(f"📤 Output: {output_path}")
    
    # Check if input exists
    if Path(input_path).exists():
        print(f"✅ Input file exists: {Path(input_path).stat().st_size} bytes")
    else:
        print(f"❌ Input file missing: {input_path}")
        return
    
    try:
        result = await pipeline.run_agent("template_engineer", pipeline_id)
        
        if result.success:
            print(f"✅ template_engineer SUCCESS")
            print(f"   Output: {result.output_file}")
            
            # Check if output file exists
            if result.output_file and Path(result.output_file).exists():
                size = Path(result.output_file).stat().st_size
                print(f"   File size: {size} bytes")
                
                # Show content preview
                content = Path(result.output_file).read_text()[:200]
                print(f"   Content preview: {content}...")
            else:
                print(f"   ⚠️ Output file not found")
        else:
            print(f"❌ template_engineer FAILED: {result.message}")
            
    except Exception as e:
        print(f"❌ template_engineer ERROR: {e}")
    
    print(f"\n🎉 Template engineer testing completed!")

if __name__ == "__main__":
    asyncio.run(test_template_engineer())
