import asyncio
import sys
import json
from pathlib import Path
from typing import Optional
from mcp.orchestrator import TemplatePipeline, PipelineConfig


def log_agent_step(agent_id: str, input_path: str, output_path: Optional[str]):
    print(f"\n=== 🧠 {agent_id.upper()} ===")
    if Path(input_path).exists():
        print(f"\n📅 INPUT ({input_path}):")
        print(Path(input_path).read_text())
    else:
        print(f"\n📅 INPUT ({input_path}): [File not found]")

    if output_path and Path(output_path).exists():
        print(f"\n📄 OUTPUT ({output_path}):")
        print(Path(output_path).read_text())
    else:
        print(f"\n📄 OUTPUT ({output_path}): [File not found]")


async def manual_run(request_file):
    config = PipelineConfig()
    orchestrator = TemplatePipeline(config)

    print("🛠️  Starting manual test run...")
    pipeline_id = orchestrator.generate_pipeline_id()
    orchestrator.pipeline_state[pipeline_id] = {
        'status': 'started',
        'request_file': request_file,
        'start_time': str(asyncio.get_event_loop().time()),
        'agents_executed': [],
        'current_step': 'initialization'
    }

    for agent_id in orchestrator.pipeline:
        print(f"➔️  {agent_id.replace('_', ' ').title()}...")

        input_path = orchestrator.get_input_path(agent_id, pipeline_id)
        output_path = orchestrator.get_output_path(agent_id, pipeline_id)

        if Path(output_path).exists():
            print(f"⏭️  Skipping {agent_id}, output already exists.")
            continue

        result = await orchestrator.execute_agent(agent_id, input_path, pipeline_id=pipeline_id)
        log_agent_step(agent_id, input_path, getattr(result, 'output_file', None))

        input(f"✅ {agent_id.replace('_', ' ').title()} complete. Press ENTER to continue...\n")

        if not result.success:
            print(f"❌ {agent_id} failed. Stopping pipeline.")
            return

    print("✅ All steps completed.")
    print(json.dumps({agent: orchestrator.pipeline_state[pipeline_id].get(agent) for agent in orchestrator.pipeline}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manual_driver.py input/manual-run.md")
        sys.exit(1)

    asyncio.run(manual_run(sys.argv[1]))
