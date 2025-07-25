#!/usr/bin/env python3
"""
Template Generation Orchestrator - Refactored Version 2.0
Coordinates the execution of multiple agents using standardized interfaces
"""

import asyncio
import json
import logging
import os
import sys
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Type

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import new utilities
from utils.agent_interface import AgentInterface, AgentResult, AgentStatus
from utils.path_manager import PathManager, PipelineContext, PathType
from utils.logging_helper import get_pipeline_logger, PipelineLogAggregator
from utils.pipeline_state_manager import PipelineStateManager, PipelineStatus, AgentStatus as StateAgentStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class TemplateOrchestrator:
    """Refactored orchestrator using new standardized agent interfaces"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.state_manager = PipelineStateManager()
        self.agent_registry: Dict[str, Type[AgentInterface]] = {}
        self.pipeline_definition = self._get_pipeline_definition()
        self._register_agents()
    
    def _get_pipeline_definition(self) -> List[Dict[str, Any]]:
        """Define the standard pipeline with agent configurations"""
        return [
            {
                "agent_id": "request_interpreter",
                "required": True,
                "timeout": 60,
                "retry_count": 2
            },
            {
                "agent_id": "prompt_designer", 
                "required": True,
                "timeout": 60,
                "retry_count": 2
            },
            {
                "agent_id": "design_variation_generator",
                "required": False,
                "timeout": 120,
                "retry_count": 1
            },
            {
                "agent_id": "template_engineer",
                "required": True,
                "timeout": 180,
                "retry_count": 2
            },
            {
                "agent_id": "cta_optimizer",
                "required": True,
                "timeout": 90,
                "retry_count": 1
            },
            {
                "agent_id": "wordpress_theme_assembler",
                "required": True,
                "timeout": 240,
                "retry_count": 2
            },
            {
                "agent_id": "mobile_ux_enhancer",
                "required": False,
                "timeout": 180,
                "retry_count": 1
            },
            {
                "agent_id": "seo_optimizer",
                "required": False,
                "timeout": 120,
                "retry_count": 1
            },
            {
                "agent_id": "component_library",
                "required": False,
                "timeout": 150,
                "retry_count": 1
            },
            {
                "agent_id": "design_critic",
                "required": False,
                "timeout": 90,
                "retry_count": 1
            },
            {
                "agent_id": "visual_inspector",
                "required": False,
                "timeout": 120,
                "retry_count": 1
            },
            {
                "agent_id": "code_reviewer",
                "required": False,
                "timeout": 90,
                "retry_count": 1
            },
            {
                "agent_id": "theme_validator",
                "required": True,
                "timeout": 60,
                "retry_count": 1
            },
            {
                "agent_id": "refinement_orchestrator",
                "required": False,
                "timeout": 600,  # 10 minutes for refinement
                "retry_count": 1
            },
            {
                "agent_id": "packager",
                "required": True,
                "timeout": 120,
                "retry_count": 2
            }
        ]
    
    def _register_agents(self) -> None:
        """Register all available agents"""
        # Import and register agents dynamically
        agent_imports = {
            "request_interpreter": "agents.request_interpreter.request_interpreter.RequestInterpreterAgent",
            "prompt_designer": "agents.prompt_designer.prompt_designer.PromptDesignerAgent", 
            "design_variation_generator": "agents.design_variation_generator.design_variation_generator.DesignVariationGeneratorAgent",
            "template_engineer": "agents.template_engineer.template_engineer.TemplateEngineerAgent",
            "cta_optimizer": "agents.cta_optimizer.cta_optimizer.CTAOptimizerAgent",
            "wordpress_theme_assembler": "agents.wordpress_theme_assembler.wordpress_theme_assembler.WordPressThemeAssemblerAgent",
            "mobile_ux_enhancer": "agents.mobile_ux_enhancer.mobile_ux_enhancer.MobileUXEnhancerAgent",
            "seo_optimizer": "agents.seo_optimizer.seo_optimizer.SEOOptimizerAgent",
            "component_library": "agents.component_library.component_library.ComponentLibraryAgent",
            "design_critic": "agents.design_critic.design_critic.DesignCriticAgent",
            "visual_inspector": "agents.visual_inspector.visual_inspector.VisualInspectorAgent",
            "code_reviewer": "agents.code_reviewer.code_reviewer.CodeReviewerAgent",
            "theme_validator": "agents.theme_validator.theme_validator.ThemeValidator",
            "refinement_orchestrator": "agents.refinement_orchestrator.refinement_orchestrator.RefinementOrchestrator",
            "packager": "agents.packager.packager.PackagerAgent"
        }
        
        for agent_id, import_path in agent_imports.items():
            try:
                module_path, class_name = import_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[class_name])
                agent_class = getattr(module, class_name)
                self.agent_registry[agent_id] = agent_class
                logger.debug(f"Registered agent: {agent_id}")
            except Exception as e:
                logger.warning(f"Could not register agent {agent_id}: {e}")
    
    async def run_pipeline(self, request_file: str, pipeline_id: str = None) -> Dict[str, Any]:
        """Run the complete template generation pipeline"""
        if not pipeline_id:
            pipeline_id = f"pipeline_{uuid.uuid4().hex[:8]}"
        
        logger.info(f"Starting pipeline {pipeline_id}")
        
        # Create pipeline context and path manager
        template_id = f"template_{uuid.uuid4().hex[:8]}"
        context = PipelineContext(
            pipeline_id=pipeline_id,
            template_id=template_id,
            request_file=request_file
        )
        path_manager = PathManager(context)
        
        # Initialize pipeline state
        agent_list = [agent["agent_id"] for agent in self.pipeline_definition]
        pipeline_state = self.state_manager.create_pipeline(
            pipeline_id, request_file, agent_list
        )
        
        # Setup logging
        pipeline_logger = get_pipeline_logger("orchestrator", pipeline_id)
        pipeline_logger.log_agent_start(request_file, {"pipeline_id": pipeline_id})
        
        try:
            # Update pipeline status to running
            self.state_manager.update_pipeline_status(pipeline_id, PipelineStatus.RUNNING)
            
            # Execute pipeline agents
            results = {}
            current_input = request_file
            
            for agent_config in self.pipeline_definition:
                agent_id = agent_config["agent_id"]
                
                # Skip if agent not registered and not required
                if agent_id not in self.agent_registry:
                    if agent_config["required"]:
                        error_msg = f"Required agent {agent_id} not available"
                        pipeline_logger.error(error_msg)
                        raise Exception(error_msg)
                    else:
                        pipeline_logger.warning(f"Optional agent {agent_id} not available, skipping")
                        continue
                
                # Execute agent
                result = await self._execute_agent(
                    agent_id, current_input, context, path_manager, 
                    agent_config, pipeline_logger
                )
                
                results[agent_id] = result
                
                # Update current input for next agent
                if result.success and result.output_path:
                    current_input = result.output_path
                elif agent_config["required"]:
                    error_msg = f"Required agent {agent_id} failed: {result.error_message}"
                    pipeline_logger.error(error_msg)
                    raise Exception(error_msg)
            
            # Mark pipeline as completed
            self.state_manager.update_pipeline_status(pipeline_id, PipelineStatus.COMPLETED)
            
            # Generate final report
            final_report = self._generate_pipeline_report(
                pipeline_id, results, path_manager, pipeline_logger
            )
            
            pipeline_logger.log_agent_end(True, final_report.get("output_path"))
            pipeline_logger.save_structured_log()
            
            logger.info(f"Pipeline {pipeline_id} completed successfully")
            return final_report
            
        except Exception as e:
            # Mark pipeline as failed
            self.state_manager.update_pipeline_status(
                pipeline_id, PipelineStatus.FAILED, str(e)
            )
            
            pipeline_logger.error(f"Pipeline failed: {e}", e)
            pipeline_logger.save_structured_log()
            
            logger.error(f"Pipeline {pipeline_id} failed: {e}")
            raise e
    
    async def _execute_agent(self, agent_id: str, input_path: str, 
                           context: PipelineContext, path_manager: PathManager,
                           agent_config: Dict[str, Any], pipeline_logger) -> AgentResult:
        """Execute a single agent with proper error handling and state management"""
        
        pipeline_logger.info(f"Executing agent: {agent_id}")
        
        # Update agent state to running
        self.state_manager.update_agent_status(
            context.pipeline_id, agent_id, StateAgentStatus.RUNNING,
            input_path=input_path
        )
        
        try:
            # Get agent input path
            agent_input = path_manager.get_input_path(agent_id)
            if not agent_input.exists():
                agent_input = Path(input_path)
            
            # Create agent instance
            agent_class = self.agent_registry[agent_id]
            agent = agent_class(self.config.get(agent_id, {}))
            
            # Execute agent with timeout
            timeout = agent_config.get("timeout", 300)
            
            # Create execution context
            execution_context = {
                "pipeline_id": context.pipeline_id,
                "template_id": context.template_id,
                "request_file": context.request_file,
                "path_manager": path_manager
            }
            
            # Execute with timeout
            result = await asyncio.wait_for(
                agent.run(str(agent_input), execution_context),
                timeout=timeout
            )
            
            # Update agent state based on result
            if result.success:
                self.state_manager.update_agent_status(
                    context.pipeline_id, agent_id, StateAgentStatus.SUCCESS,
                    output_path=result.output_path,
                    metadata=result.metadata
                )
            else:
                self.state_manager.update_agent_status(
                    context.pipeline_id, agent_id, StateAgentStatus.FAILED,
                    error_message=result.error_message
                )
            
            pipeline_logger.info(f"Agent {agent_id} completed: {result.status.value}")
            return result
            
        except asyncio.TimeoutError:
            error_msg = f"Agent {agent_id} timed out after {agent_config.get('timeout', 300)} seconds"
            self.state_manager.update_agent_status(
                context.pipeline_id, agent_id, StateAgentStatus.FAILED,
                error_message=error_msg
            )
            pipeline_logger.error(error_msg)
            return AgentResult(
                agent_id=agent_id,
                status=AgentStatus.FAILED,
                errors=[error_msg]
            )
            
        except Exception as e:
            error_msg = f"Agent {agent_id} execution failed: {str(e)}"
            self.state_manager.update_agent_status(
                context.pipeline_id, agent_id, StateAgentStatus.FAILED,
                error_message=error_msg
            )
            pipeline_logger.error(error_msg, e)
            return AgentResult(
                agent_id=agent_id,
                status=AgentStatus.FAILED,
                errors=[error_msg]
            )

    def _generate_pipeline_report(self, pipeline_id: str, results: Dict[str, AgentResult],
                                path_manager: PathManager, pipeline_logger) -> Dict[str, Any]:
        """Generate comprehensive pipeline execution report"""

        # Get pipeline state
        pipeline_state = self.state_manager.get_pipeline_state(pipeline_id)

        # Calculate success metrics
        successful_agents = [r for r in results.values() if r.success]
        failed_agents = [r for r in results.values() if not r.success]

        # Generate log aggregation
        log_aggregator = PipelineLogAggregator(pipeline_id)
        log_summary = log_aggregator.aggregate_logs()
        health_status = log_aggregator.get_pipeline_health()

        # Find final output
        final_output = None
        if "packager" in results and results["packager"].output_path:
            final_output = results["packager"].output_path
        elif successful_agents:
            # Use last successful agent output
            final_output = successful_agents[-1].output_path

        # Create comprehensive report
        report = {
            "pipeline_id": pipeline_id,
            "status": "completed" if not failed_agents else "partial",
            "execution_summary": {
                "total_agents": len(results),
                "successful_agents": len(successful_agents),
                "failed_agents": len(failed_agents),
                "success_rate": len(successful_agents) / len(results) if results else 0
            },
            "timing": {
                "start_time": pipeline_state.start_time if pipeline_state else None,
                "end_time": pipeline_state.end_time if pipeline_state else None,
                "total_execution_time": sum(r.execution_time for r in results.values())
            },
            "agent_results": {
                agent_id: {
                    "status": result.status.value,
                    "success": result.success,
                    "output_path": result.output_path,
                    "execution_time": result.execution_time,
                    "errors": result.errors,
                    "warnings": result.warnings
                }
                for agent_id, result in results.items()
            },
            "output_path": final_output,
            "log_summary": log_summary,
            "health_status": health_status,
            "recommendations": self._generate_recommendations(results, health_status)
        }

        # Save report
        report_path = path_manager.get_path(PathType.LOGS, "pipeline_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        report["report_path"] = str(report_path)

        pipeline_logger.info(f"Pipeline report generated: {report_path}")
        return report

    def _generate_recommendations(self, results: Dict[str, AgentResult],
                                health_status: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on pipeline results"""
        recommendations = []

        # Check for failed required agents
        failed_agents = [agent_id for agent_id, result in results.items() if not result.success]
        if failed_agents:
            recommendations.append(f"Review and fix failed agents: {', '.join(failed_agents)}")

        # Check health status
        if health_status["status"] == "CRITICAL":
            recommendations.append("Pipeline has critical errors - review logs immediately")
        elif health_status["status"] == "WARNING":
            recommendations.append("Pipeline has warnings - consider reviewing for improvements")

        # Check for missing outputs
        agents_without_output = [
            agent_id for agent_id, result in results.items()
            if result.success and not result.output_path
        ]
        if agents_without_output:
            recommendations.append(f"Agents completed but produced no output: {', '.join(agents_without_output)}")

        # Performance recommendations
        slow_agents = [
            agent_id for agent_id, result in results.items()
            if result.execution_time > 300  # 5 minutes
        ]
        if slow_agents:
            recommendations.append(f"Consider optimizing slow agents: {', '.join(slow_agents)}")

        if not recommendations:
            recommendations.append("Pipeline executed successfully with no issues detected")

        return recommendations

    def get_pipeline_status(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a pipeline"""
        pipeline_state = self.state_manager.get_pipeline_state(pipeline_id)
        if not pipeline_state:
            return None

        return {
            "pipeline_id": pipeline_state.pipeline_id,
            "status": pipeline_state.status.value,
            "start_time": pipeline_state.start_time,
            "end_time": pipeline_state.end_time,
            "agents": {
                agent_id: {
                    "status": agent.status.value,
                    "execution_time": agent.execution_time,
                    "output_path": agent.output_path
                }
                for agent_id, agent in pipeline_state.agents.items()
            }
        }

    def list_pipelines(self) -> Dict[str, Any]:
        """List all pipelines with summary information"""
        return self.state_manager.get_pipeline_summary()

    def cleanup_old_pipelines(self, days_old: int = 7) -> int:
        """Clean up old pipeline states"""
        return self.state_manager.cleanup_old_pipelines(days_old)

# Factory function for backward compatibility
def create_orchestrator(config: Dict[str, Any] = None) -> TemplateOrchestrator:
    """Create a new template orchestrator instance"""
    return TemplateOrchestrator(config)

# Main execution function
async def main():
    """Main execution function for testing"""
    orchestrator = TemplateOrchestrator()

    # Example usage
    request_file = "input/sample_request.md"
    if Path(request_file).exists():
        try:
            result = await orchestrator.run_pipeline(request_file)
            print(f"Pipeline completed successfully!")
            print(f"Final output: {result.get('output_path')}")
        except Exception as e:
            print(f"Pipeline failed: {e}")
    else:
        print(f"Request file not found: {request_file}")

if __name__ == "__main__":
    asyncio.run(main())
