#!/usr/bin/env python3
"""
Test the improved template_engineer
"""

import asyncio
import logging
from pathlib import Path
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_improved_template():
    """Test the improved template_engineer"""
    print("🔧 Testing Improved Template Engineer")
    print("=" * 50)
    
    # Use the latest pipeline
    pipeline_id = "pipeline_cf4d4c44"
    
    # Check if files exist
    spec_file = f"template_generations/template_cf4d4c44/specs/template_spec.json"
    design_file = f"template_generations/template_cf4d4c44/design_variations/design_variation_variation_20250624145224.json"
    prompt_file = f"template_generations/template_cf4d4c44/prompts/prompt_cf4d4c44.json"
    
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
        'start_time': '2025-06-24T14:52:00',
        'status': 'running',
        'template_dir': f'template_generations/template_cf4d4c44'
    }
    
    print(f"\n🔧 Testing improved template_engineer...")
    
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
                content = Path(result.output_file).read_text()[:500]
                print(f"   Content preview: {content}...")
                
                # Check for modern features
                modern_features = [
                    "grid-template-columns",
                    "linear-gradient", 
                    "box-shadow",
                    "transform",
                    "@media",
                    "Google Fonts"
                ]
                
                found_features = [f for f in modern_features if f in content]
                print(f"   ✅ Modern CSS features found: {len(found_features)}/6")
                for feature in found_features:
                    print(f"      • {feature}")
                
                if "<?php" in content:
                    print(f"   ✅ Valid PHP file detected")
                else:
                    print(f"   ⚠️ No PHP opening tag found")
            else:
                print(f"   ⚠️ Output file not found")
        else:
            print(f"❌ template_engineer FAILED: {result.message}")
            
    except Exception as e:
        print(f"❌ template_engineer ERROR: {e}")
    
    print(f"\n🎉 Improved template testing completed!")

if __name__ == "__main__":
    asyncio.run(test_improved_template())
