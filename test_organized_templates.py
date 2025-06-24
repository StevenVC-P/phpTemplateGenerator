#!/usr/bin/env python3
"""
Test Organized Template Generation
Demonstrates the new folder-based organization system
"""

import asyncio
import json
import logging
from pathlib import Path
from mcp.orchestrator import TemplateOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_organized_generation():
    """Test the new organized template generation system"""
    print("🗂️ Testing Organized Template Generation")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = TemplateOrchestrator()
    
    print("📋 Running pipeline with organized folder structure...")
    
    # Run the pipeline
    result = await orchestrator.process_request("input/example-request.md")
    
    if result['status'] == 'success':
        print(f"✅ Pipeline completed successfully!")
        print(f"📁 Final output: {result['final_output']}")
        
        # Check the organized structure
        pipeline_id = result['pipeline_id']
        
        # Find the template folder
        template_generations = Path("template_generations")
        if template_generations.exists():
            template_folders = list(template_generations.glob("template_*"))
            if template_folders:
                latest_folder = max(template_folders, key=lambda x: x.stat().st_mtime)
                print(f"\n🗂️ Template Folder Structure:")
                print(f"📁 {latest_folder}")
                
                # Show the organized structure
                show_folder_structure(latest_folder)
                
                # Analyze agent conversations
                analyze_agent_conversations(latest_folder)
                
                return latest_folder
        
        return True
    else:
        print(f"❌ Pipeline failed: {result.get('error', 'Unknown error')}")
        return False

def show_folder_structure(template_folder: Path, indent: str = ""):
    """Show the organized folder structure"""
    subfolders = [
        "specs", "design_variations", "prompts", "templates", 
        "reviews", "refinements", "final", "agent_conversations"
    ]
    
    for subfolder in subfolders:
        subfolder_path = template_folder / subfolder
        if subfolder_path.exists():
            files = list(subfolder_path.glob("*"))
            print(f"   📂 {subfolder}/ ({len(files)} files)")
            
            # Show first few files
            for file in files[:3]:
                print(f"      📄 {file.name}")
            if len(files) > 3:
                print(f"      ... and {len(files) - 3} more files")

def analyze_agent_conversations(template_folder: Path):
    """Analyze the agent conversations and outputs"""
    print(f"\n🤖 Agent Conversation Analysis:")
    
    # Check design variation
    design_var_folder = template_folder / "design_variations"
    if design_var_folder.exists():
        design_files = list(design_var_folder.glob("*.json"))
        if design_files:
            with open(design_files[0], 'r') as f:
                design_data = json.load(f)
            
            print(f"   🎨 Design Variation: {design_data.get('variation_id', 'unknown')}")
            print(f"      • Colors: {design_data.get('colors', {}).get('primary', 'N/A')}")
            print(f"      • Typography: {design_data.get('typography', {}).get('heading', 'N/A')}")
            print(f"      • Layout: {design_data.get('layout', {}).get('name', 'N/A')}")
    
    # Check code review
    reviews_folder = template_folder / "reviews"
    if reviews_folder.exists():
        review_files = list(reviews_folder.glob("*.review.json"))
        if review_files:
            with open(review_files[0], 'r') as f:
                review_data = json.load(f)
            
            print(f"   📊 Code Review:")
            print(f"      • Overall Score: {review_data.get('overall_score', 'N/A')}/10")
            print(f"      • Issues Found: {len(review_data.get('issues', []))}")
            print(f"      • Suggestions: {len(review_data.get('suggestions', []))}")
    
    # Check templates
    templates_folder = template_folder / "templates"
    if templates_folder.exists():
        template_files = list(templates_folder.glob("*.php"))
        print(f"   🏗️ Templates Generated: {len(template_files)}")
        
        # Check for refined versions
        refined_files = [f for f in template_files if 'refined' in f.name]
        if refined_files:
            print(f"      • Refined Versions: {len(refined_files)}")
            print(f"      • Latest: {refined_files[-1].name}")

def compare_with_old_system():
    """Compare the new organized system with the old scattered approach"""
    print(f"\n📊 System Comparison:")
    print(f"=" * 30)
    
    # Count files in old locations
    old_locations = {
        "templates": "templates/",
        "reviews": "reviews/", 
        "specs": "specs/",
        "design_variations": "design_variations/"
    }
    
    old_total = 0
    for name, path in old_locations.items():
        if Path(path).exists():
            count = len(list(Path(path).glob("*")))
            print(f"📁 Old {name}: {count} files")
            old_total += count
    
    # Count files in new organized structure
    template_generations = Path("template_generations")
    new_total = 0
    organized_folders = 0
    
    if template_generations.exists():
        for template_folder in template_generations.glob("template_*"):
            organized_folders += 1
            for subfolder in template_folder.glob("*"):
                if subfolder.is_dir():
                    count = len(list(subfolder.glob("*")))
                    new_total += count
    
    print(f"\n🗂️ New Organized System:")
    print(f"   • Template Generations: {organized_folders}")
    print(f"   • Total Organized Files: {new_total}")
    print(f"   • Old Scattered Files: {old_total}")
    
    if organized_folders > 0:
        print(f"\n✅ Benefits of New System:")
        print(f"   • Each template has its own isolated folder")
        print(f"   • Agent conversations stay together")
        print(f"   • Easy to compare different generations")
        print(f"   • Better variation isolation")
        print(f"   • Cleaner project structure")

async def main():
    """Main test function"""
    print("🗂️ Organized Template Generation Test")
    print("=" * 50)
    
    # Test the organized generation
    result = await test_organized_generation()
    
    if result:
        # Compare systems
        compare_with_old_system()
        
        print("\n" + "=" * 50)
        print("🎯 Organized System Benefits:")
        print("   ✅ Isolated template conversations")
        print("   ✅ Better variation tracking")
        print("   ✅ Cleaner project structure")
        print("   ✅ Easy comparison between generations")
        print("   ✅ Improved agent feedback isolation")
        
        print("\n📝 Folder Structure Created:")
        print("   📁 template_generations/")
        print("      📁 template_YYYYMMDD_HHMMSS/")
        print("         📂 specs/ - Request interpretations")
        print("         📂 design_variations/ - Design specs")
        print("         📂 prompts/ - AI prompts")
        print("         📂 templates/ - Generated templates")
        print("         📂 reviews/ - Agent feedback")
        print("         📂 refinements/ - Iteration history")
        print("         📂 final/ - Packaged output")
        print("         📂 agent_conversations/ - Agent logs")
        
        if isinstance(result, Path):
            print(f"\n🚀 View Latest Template:")
            print(f"   python view_template.py {result}/templates/")
    else:
        print("\n❌ Organized generation test failed")

if __name__ == "__main__":
    asyncio.run(main())
