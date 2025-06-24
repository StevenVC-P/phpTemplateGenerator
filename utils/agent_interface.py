#!/usr/bin/env python3
"""
Agent Interface Specification
Defines the standard interface for all template generation agents
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Standard agent configuration structure"""
    agent_id: str
    name: str
    version: str
    description: str
    capabilities: List[str]
    input_format: Dict[str, Any]
    output_format: Dict[str, Any]
    
    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> 'AgentConfig':
        """Load agent configuration from JSON file"""
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        return cls(
            agent_id=data['agent_id'],
            name=data['name'],
            version=data['version'],
            description=data['description'],
            capabilities=data['capabilities'],
            input_format=data['input_format'],
            output_format=data['output_format']
        )

@dataclass
class AgentInput:
    """Standard input structure for agents"""
    file_path: str
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    pipeline_context: Optional[Dict[str, Any]] = None

@dataclass
class AgentOutput:
    """Standard output structure for agents"""
    success: bool
    output_file: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    quality_score: Optional[float] = None
    execution_time: Optional[float] = None

class BaseAgent(ABC):
    """Abstract base class for all template generation agents"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"agent.{config.agent_id}")
    
    @abstractmethod
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """Execute the agent's main functionality"""
        pass
    
    def validate_input(self, input_data: AgentInput) -> bool:
        """Validate input data against agent requirements"""
        try:
            # Check if input file exists
            if input_data.file_path and not Path(input_data.file_path).exists():
                self.logger.error(f"Input file not found: {input_data.file_path}")
                return False
            
            # Validate input format
            input_format = self.config.input_format
            if input_format.get('type') == 'json' and input_data.content:
                try:
                    json.loads(input_data.content)
                except json.JSONDecodeError:
                    self.logger.error("Invalid JSON input")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Input validation failed: {e}")
            return False
    
    def create_output_file(self, content: str, template_id: str) -> str:
        """Create output file based on agent configuration"""
        output_format = self.config.output_format
        file_name = output_format.get('file_name', f"{self.config.agent_id}_output.txt")
        
        # Replace template ID placeholder
        file_name = file_name.replace('{id}', template_id)
        
        # Determine output directory
        output_dir = self.get_output_directory()
        output_path = Path(output_dir) / file_name
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Created output file: {output_path}")
        return str(output_path)
    
    def get_output_directory(self) -> str:
        """Get output directory for this agent type"""
        directory_mapping = {
            'request_interpreter': 'specs',
            'prompt_designer': 'prompts',
            'template_engineer': 'templates',
            'code_reviewer': 'reviews',
            'design_critic': 'reviews',
            'cta_optimizer': 'templates',
            'packager': 'final'
        }
        
        return directory_mapping.get(self.config.agent_id, 'output')
    
    def calculate_quality_score(self, output_data: Any) -> float:
        """Calculate quality score for the output (to be overridden by subclasses)"""
        return 8.0  # Default score

class RequestInterpreterAgent(BaseAgent):
    """Agent for interpreting user requests into structured specifications"""
    
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """Execute request interpretation"""
        try:
            if not self.validate_input(input_data):
                return AgentOutput(
                    success=False,
                    error_message="Input validation failed"
                )
            
            # Read input content
            with open(input_data.file_path, 'r') as f:
                request_content = f.read()
            
            # Process request (placeholder implementation)
            spec_data = self.parse_request(request_content)
            
            # Generate template ID
            template_id = f"template_{len(spec_data.get('requirements', {}))}"
            
            # Create output file
            output_content = json.dumps(spec_data, indent=2)
            output_file = self.create_output_file(output_content, template_id)
            
            return AgentOutput(
                success=True,
                output_file=output_file,
                content=output_content,
                quality_score=self.calculate_quality_score(spec_data),
                metadata={'template_id': template_id}
            )
            
        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
            return AgentOutput(
                success=False,
                error_message=str(e)
            )
    
    def parse_request(self, content: str) -> Dict[str, Any]:
        """Parse request content into structured specification"""
        # Placeholder implementation - would use NLP in real version
        return {
            "template_id": "template_001",
            "project_type": "saas_landing_page",
            "requirements": {
                "design": {"style": "modern", "responsive": True},
                "technical": {"language": "php", "framework": "none"}
            },
            "target_audience": {"primary": "small_businesses"},
            "created_at": "2025-06-23T14:33:00Z",
            "status": "parsed"
        }

class AgentFactory:
    """Factory for creating agent instances"""
    
    _agent_classes = {
        'request_interpreter': RequestInterpreterAgent,
        # Add other agent classes as they're implemented
    }
    
    @classmethod
    def create_agent(cls, config: AgentConfig) -> BaseAgent:
        """Create agent instance based on configuration"""
        agent_class = cls._agent_classes.get(config.agent_id)
        
        if not agent_class:
            raise ValueError(f"Unknown agent type: {config.agent_id}")
        
        return agent_class(config)
    
    @classmethod
    def register_agent(cls, agent_id: str, agent_class: type):
        """Register a new agent class"""
        cls._agent_classes[agent_id] = agent_class

# Utility functions
def load_agent_config(config_path: Union[str, Path]) -> AgentConfig:
    """Load agent configuration from file"""
    return AgentConfig.from_file(config_path)

def validate_agent_configs(agents_dir: Union[str, Path]) -> List[str]:
    """Validate all agent configurations in directory"""
    agents_path = Path(agents_dir)
    invalid_configs = []
    
    for config_file in agents_path.glob("*.json"):
        try:
            config = load_agent_config(config_file)
            logger.info(f"Valid config: {config.agent_id}")
        except Exception as e:
            logger.error(f"Invalid config {config_file}: {e}")
            invalid_configs.append(str(config_file))
    
    return invalid_configs
