#!/usr/bin/env python3
"""
Test script for the PHP Template Generator Pipeline
Validates the complete multi-agent system functionality
"""

import asyncio
import json
import sys
from pathlib import Path
from mcp.orchestrator import TemplateOrchestrator, PipelineConfig

async def test_pipeline():
    """Test the complete pipeline with sample input"""
    print("🧪 Testing PHP Template Generator Pipeline")
    print("=" * 50)
    
    # Initialize orchestrator
    config = PipelineConfig()
    orchestrator = TemplateOrchestrator(config)
    
    print(f"✅ Loaded {len(orchestrator.agents)} agents:")
    for agent_id, agent_config in orchestrator.agents.items():
        version = agent_config.get('version', '1.0')
        capabilities = len(agent_config.get('capabilities', []))
        print(f"   • {agent_id} v{version} ({capabilities} capabilities)")
    
    print("\n🚀 Running pipeline test...")
    
    # Test with example request
    test_input = "input/example-request.md"
    if not Path(test_input).exists():
        print(f"❌ Test input file not found: {test_input}")
        return False
    
    try:
        # Execute pipeline
        result = await orchestrator.process_request(test_input)
        
        if result['status'] == 'success':
            print("✅ Pipeline executed successfully!")
            
            # Display execution summary
            summary = result['execution_summary']
            print(f"\n📊 Execution Summary:")
            print(f"   • Pipeline ID: {summary['pipeline_id']}")
            print(f"   • Total time: {calculate_total_time(summary):.2f} seconds")
            print(f"   • Agents executed: {len(summary['agents_executed'])}")
            
            print(f"\n📁 Generated files:")
            for agent_exec in summary['agents_executed']:
                if agent_exec['success']:
                    output_file = agent_exec['output_file']
                    if Path(output_file).exists():
                        print(f"   ✅ {output_file}")
                    else:
                        print(f"   ⚠️  {output_file} (not found)")
                else:
                    print(f"   ❌ {agent_exec['agent_id']} failed")
            
            # Validate final output
            final_output = result.get('final_output')
            if final_output and Path(final_output).exists():
                print(f"\n🎉 Final package created: {final_output}")
                return True
            else:
                print(f"\n⚠️  Final output not found: {final_output}")
                return False
                
        else:
            print(f"❌ Pipeline failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def calculate_total_time(summary):
    """Calculate total execution time from summary"""
    agents_executed = summary.get('agents_executed', [])
    return sum(agent.get('execution_time', 0) for agent in agents_executed)

def validate_project_structure():
    """Validate that all required directories exist"""
    print("\n🔍 Validating project structure...")
    
    required_dirs = [
        'input', 'specs', 'prompts', 'templates', 
        'reviews', 'final', 'agents', 'mcp', 'utils'
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not Path(directory).exists():
            missing_dirs.append(directory)
        else:
            print(f"   ✅ {directory}/")
    
    if missing_dirs:
        print(f"   ❌ Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("   ✅ All required directories present")
    return True

def validate_agent_configs():
    """Validate agent configuration files"""
    print("\n🤖 Validating agent configurations...")
    
    agents_dir = Path('agents')
    if not agents_dir.exists():
        print("   ❌ Agents directory not found")
        return False
    
    config_files = list(agents_dir.glob('*.json'))
    if not config_files:
        print("   ❌ No agent configuration files found")
        return False
    
    valid_configs = 0
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Check required fields
            required_fields = ['agent_id', 'name', 'description', 'capabilities']
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"   ⚠️  {config_file.name}: missing {missing_fields}")
            else:
                print(f"   ✅ {config_file.name}")
                valid_configs += 1
                
        except Exception as e:
            print(f"   ❌ {config_file.name}: {e}")
    
    print(f"   📊 {valid_configs}/{len(config_files)} valid configurations")
    return valid_configs == len(config_files)

async def main():
    """Main test function"""
    print("🧠 PHP Template Generator - System Test")
    print("=" * 60)
    
    # Validate project structure
    structure_valid = validate_project_structure()
    
    # Validate agent configurations
    configs_valid = validate_agent_configs()
    
    if not (structure_valid and configs_valid):
        print("\n❌ Pre-flight checks failed. Please fix issues before testing.")
        sys.exit(1)
    
    print("\n✅ Pre-flight checks passed!")
    
    # Run pipeline test
    pipeline_success = await test_pipeline()
    
    print("\n" + "=" * 60)
    if pipeline_success:
        print("🎉 All tests passed! The system is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Replace simulation logic with real AI agent implementations")
        print("   2. Add comprehensive error handling and recovery")
        print("   3. Implement actual template generation logic")
        print("   4. Add performance monitoring and optimization")
        sys.exit(0)
    else:
        print("❌ Tests failed. Please check the logs and fix issues.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
