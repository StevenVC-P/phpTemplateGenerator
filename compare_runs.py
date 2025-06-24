#!/usr/bin/env python3
"""
Compare two pipeline runs to demonstrate design variation
"""

import asyncio
import logging
import json
from pathlib import Path
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_pipeline_comparison():
    """Run two pipeline executions and compare results"""
    print("🔄 PIPELINE COMPARISON TEST")
    print("=" * 60)
    print("Running 2 identical requests to demonstrate design variation...")
    
    # Initialize pipeline
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    
    results = []
    
    for run_num in range(1, 3):
        print(f"\n{'='*20} RUN {run_num} {'='*20}")
        
        # Generate new pipeline ID for each run
        pipeline_id = pipeline.generate_pipeline_id()
        
        # Set up request file
        request_file = "input/example-request.md"
        if not Path(request_file).exists():
            print(f"❌ Request file not found: {request_file}")
            return
        
        pipeline.pipeline_state[pipeline_id] = {
            'request_file': request_file,
            'start_time': f'2025-06-24T15:00:0{run_num}',
            'status': 'running'
        }
        
        print(f"🆔 Pipeline ID: {pipeline_id}")
        
        # Run the first 4 agents (core generation pipeline)
        agents_to_run = [
            "request_interpreter",
            "design_variation_generator", 
            "prompt_designer",
            "template_engineer"
        ]
        
        run_results = {
            'pipeline_id': pipeline_id,
            'run_number': run_num,
            'agents': {}
        }
        
        for agent_id in agents_to_run:
            try:
                result = await pipeline.run_agent(agent_id, pipeline_id)
                
                if result.success:
                    print(f"✅ {agent_id}: {Path(result.output_file).name}")
                    
                    # Store result info
                    run_results['agents'][agent_id] = {
                        'success': True,
                        'output_file': result.output_file,
                        'file_size': Path(result.output_file).stat().st_size if Path(result.output_file).exists() else 0
                    }
                    
                    # Extract key design info for comparison
                    if agent_id == "design_variation_generator" and Path(result.output_file).exists():
                        design_data = json.loads(Path(result.output_file).read_text())
                        run_results['design_variation'] = {
                            'color_strategy': design_data.get('color_palette_strategy'),
                            'typography': design_data.get('typography_scheme', {}).get('pairing', {}).get('name'),
                            'layout': design_data.get('layout_structure', {}).get('hero', {}).get('name')
                        }
                    
                else:
                    print(f"❌ {agent_id}: {result.message}")
                    run_results['agents'][agent_id] = {
                        'success': False,
                        'error': result.message
                    }
                    break
                    
            except Exception as e:
                print(f"❌ {agent_id} ERROR: {e}")
                run_results['agents'][agent_id] = {
                    'success': False,
                    'error': str(e)
                }
                break
        
        results.append(run_results)
        print(f"🎉 Run {run_num} completed!")
    
    # Compare results
    print(f"\n{'='*20} COMPARISON ANALYSIS {'='*20}")
    
    if len(results) == 2:
        run1, run2 = results
        
        print(f"📊 DESIGN VARIATIONS COMPARISON:")
        print(f"   Run 1 ID: {run1['pipeline_id']}")
        print(f"   Run 2 ID: {run2['pipeline_id']}")
        
        if 'design_variation' in run1 and 'design_variation' in run2:
            design1 = run1['design_variation']
            design2 = run2['design_variation']
            
            print(f"\n🎨 DESIGN DIFFERENCES:")
            print(f"   Color Strategy:")
            print(f"     Run 1: {design1.get('color_strategy', 'N/A')}")
            print(f"     Run 2: {design2.get('color_strategy', 'N/A')}")
            print(f"     Different: {'✅' if design1.get('color_strategy') != design2.get('color_strategy') else '❌'}")
            
            print(f"   Typography:")
            print(f"     Run 1: {design1.get('typography', 'N/A')}")
            print(f"     Run 2: {design2.get('typography', 'N/A')}")
            print(f"     Different: {'✅' if design1.get('typography') != design2.get('typography') else '❌'}")
            
            print(f"   Layout:")
            print(f"     Run 1: {design1.get('layout', 'N/A')}")
            print(f"     Run 2: {design2.get('layout', 'N/A')}")
            print(f"     Different: {'✅' if design1.get('layout') != design2.get('layout') else '❌'}")
        
        print(f"\n📁 FILE SIZE COMPARISON:")
        for agent_id in ["template_engineer"]:
            if agent_id in run1['agents'] and agent_id in run2['agents']:
                size1 = run1['agents'][agent_id].get('file_size', 0)
                size2 = run2['agents'][agent_id].get('file_size', 0)
                print(f"   {agent_id}:")
                print(f"     Run 1: {size1:,} bytes")
                print(f"     Run 2: {size2:,} bytes")
                print(f"     Difference: {abs(size1 - size2):,} bytes")
        
        # Show template directories
        print(f"\n📂 GENERATED TEMPLATES:")
        print(f"   Run 1: template_generations/template_{run1['pipeline_id'].replace('pipeline_', '')}/")
        print(f"   Run 2: template_generations/template_{run2['pipeline_id'].replace('pipeline_', '')}/")
        
        print(f"\n🎯 VARIATION SUCCESS:")
        variations_different = (
            design1.get('color_strategy') != design2.get('color_strategy') or
            design1.get('typography') != design2.get('typography') or  
            design1.get('layout') != design2.get('layout')
        )
        print(f"   Design variations are different: {'✅ YES' if variations_different else '❌ NO'}")
        
        if variations_different:
            print(f"   🎉 SUCCESS: Design variation engine is working!")
        else:
            print(f"   ⚠️ WARNING: Templates may be too similar")
    
    print(f"\n🎉 Comparison completed!")
    return results

if __name__ == "__main__":
    asyncio.run(run_pipeline_comparison())
