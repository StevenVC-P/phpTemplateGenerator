#!/usr/bin/env python3
"""
Test Active Agents System
Tests the new orchestrator with active agent structure
"""

import asyncio
import logging
from pathlib import Path
from mcp.orchestrator import TemplatePipeline, PipelineConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_active_agents():
    """Test the new active agents system"""
    print("🤖 Testing Active Agents System")
    print("=" * 50)
    
    # Initialize pipeline with new structure
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    
    print(f"📋 Loaded {len(pipeline.agents)} agents:")
    for agent_id, agent_info in pipeline.agents.items():
        status = "Active" if agent_info.get('is_active') else "Legacy"
        print(f"   • {agent_id} ({status})")
    
    print("\n🚀 Running pipeline with active agents...")
    
    # Test with example request
    request_file = "input/example-request.md"
    if not Path(request_file).exists():
        print(f"❌ Request file not found: {request_file}")
        return False
    
    try:
        await pipeline.run_pipeline(request_file)
        print("✅ Active agents pipeline completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return False

def test_agent_loading():
    """Test agent loading from new directory structure"""
    print("\n🔍 Testing Agent Loading")
    print("-" * 30)
    
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    
    agents_dir = Path(config.agents_dir)
    print(f"📁 Agents directory: {agents_dir}")
    
    if not agents_dir.exists():
        print("❌ Agents directory not found")
        return False
    
    # Check each agent directory
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir():
            agent_id = agent_dir.name
            py_file = agent_dir / f"{agent_id}.py"
            json_file = agent_dir / f"{agent_id}.json"
            
            print(f"\n📂 {agent_id}/")
            print(f"   • Python file: {'✅' if py_file.exists() else '❌'} {py_file.name}")
            print(f"   • Config file: {'✅' if json_file.exists() else '❌'} {json_file.name}")
            
            if agent_id in pipeline.agents:
                agent_info = pipeline.agents[agent_id]
                print(f"   • Loaded: ✅ ({'Active' if agent_info.get('is_active') else 'Legacy'})")
                print(f"   • Class: {agent_info.get('class', 'N/A')}")
            else:
                print(f"   • Loaded: ❌ Not found in pipeline.agents")
    
    return True

def check_agent_structure():
    """Check if agents follow the expected structure"""
    print("\n🏗️ Checking Agent Structure")
    print("-" * 30)
    
    agents_dir = Path("agents")
    expected_agents = [
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
    
    for agent_id in expected_agents:
        agent_dir = agents_dir / agent_id
        py_file = agent_dir / f"{agent_id}.py"
        json_file = agent_dir / f"{agent_id}.json"
        
        status = "✅" if agent_dir.exists() and py_file.exists() and json_file.exists() else "❌"
        print(f"   {status} {agent_id}")
        
        if agent_dir.exists():
            if not py_file.exists():
                print(f"      ⚠️ Missing: {py_file.name}")
            if not json_file.exists():
                print(f"      ⚠️ Missing: {json_file.name}")

async def test_single_agent():
    """Test running a single agent"""
    print("\n🎯 Testing Single Agent Execution")
    print("-" * 30)
    
    config = PipelineConfig()
    pipeline = TemplatePipeline(config)
    
    # Test design_variation_generator as it should be fully implemented
    agent_id = "design_variation_generator"
    
    if agent_id not in pipeline.agents:
        print(f"❌ Agent {agent_id} not found")
        return False
    
    try:
        print(f"🚀 Testing {agent_id}...")
        result = await pipeline.run_agent(agent_id, "test_pipeline")
        
        if result.success:
            print(f"✅ {agent_id} executed successfully")
            print(f"   Output: {result.output_file}")
            return True
        else:
            print(f"❌ {agent_id} failed: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing {agent_id}: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Active Agents System Test Suite")
    print("=" * 50)
    
    # Test 1: Agent loading
    print("\n1️⃣ Testing agent loading...")
    if not test_agent_loading():
        print("❌ Agent loading test failed")
        return
    
    # Test 2: Agent structure
    print("\n2️⃣ Checking agent structure...")
    check_agent_structure()
    
    # Test 3: Single agent execution
    print("\n3️⃣ Testing single agent execution...")
    if not await test_single_agent():
        print("❌ Single agent test failed")
        return
    
    # Test 4: Full pipeline
    print("\n4️⃣ Testing full pipeline...")
    if await test_active_agents():
        print("\n🎉 All tests passed! Active agents system is working.")
    else:
        print("\n❌ Pipeline test failed")

if __name__ == "__main__":
    asyncio.run(main())
