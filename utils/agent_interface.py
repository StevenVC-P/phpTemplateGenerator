# utils/agent_interface.py

import json
import logging
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from enum import Enum

class AgentStatus(Enum):
    """Standardized agent execution status"""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"

@dataclass
class AgentResult:
    """Unified result object for all agents"""
    agent_id: str
    status: AgentStatus
    message: str = ""
    output_path: Optional[str] = None
    errors: List[str] = None
    warnings: List[str] = None
    metadata: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    quality_score: Optional[float] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}

    @property
    def success(self) -> bool:
        """Backward compatibility property"""
        return self.status == AgentStatus.SUCCESS

    @property
    def error_message(self) -> str:
        """Backward compatibility property"""
        return "; ".join(self.errors) if self.errors else ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "message": self.message,
            "output_path": self.output_path,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "execution_time": self.execution_time,
            "quality_score": self.quality_score,
            "timestamp": datetime.now().isoformat()
        }

class AgentInterface(ABC):
    """Base interface that all agents must implement"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agent_id = self.__class__.__name__.lower().replace('agent', '')
        self.logger = self._setup_logger()
        self.start_time = None

    def _setup_logger(self) -> logging.Logger:
        """Setup agent-specific logger"""
        logger = logging.getLogger(f"agent.{self.agent_id}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.agent_id} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    @abstractmethod
    async def run(self, input_path: str, context: Dict[str, Any]) -> AgentResult:
        """
        Main execution method that all agents must implement

        Args:
            input_path: Path to input file or directory
            context: Pipeline context including pipeline_id, paths, etc.

        Returns:
            AgentResult: Standardized result with status and metadata
        """
        pass

    def _start_execution(self) -> None:
        """Mark start of execution for timing"""
        self.start_time = datetime.now()
        self.logger.info(f"Starting {self.agent_id} execution")

    def _end_execution(self, result: AgentResult) -> AgentResult:
        """Mark end of execution and calculate timing"""
        if self.start_time:
            result.execution_time = (datetime.now() - self.start_time).total_seconds()
        self.logger.info(f"Completed {self.agent_id} execution in {result.execution_time:.2f}s")
        return result

    def _create_success_result(self, message: str = "Completed successfully",
                             output_path: str = None, **kwargs) -> AgentResult:
        """Helper to create success result"""
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.SUCCESS,
            message=message,
            output_path=output_path,
            **kwargs
        )

    def _create_error_result(self, error: Union[str, Exception],
                           message: str = "Execution failed") -> AgentResult:
        """Helper to create error result"""
        error_str = str(error)
        if isinstance(error, Exception):
            self.logger.error(f"Exception in {self.agent_id}: {error_str}")
            self.logger.debug(traceback.format_exc())
        else:
            self.logger.error(f"Error in {self.agent_id}: {error_str}")

        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.FAILED,
            message=message,
            errors=[error_str]
        )

    def validate_input(self, input_path: str) -> bool:
        """Validate that input file/directory exists"""
        path = Path(input_path)
        if not path.exists():
            self.logger.error(f"Input path not found: {input_path}")
            return False
        return True

    def ensure_output_directory(self, output_path: str) -> bool:
        """Ensure output directory exists"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create output directory: {e}")
            return False

# Backward compatibility classes for existing agents
@dataclass
class AgentConfig:
    """Legacy agent configuration structure for backward compatibility"""
    agent_id: str
    name: str = ""
    version: str = "1.0"
    description: str = ""
    capabilities: List[str] = None
    input_format: Dict[str, Any] = None
    output_format: Dict[str, Any] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.input_format is None:
            self.input_format = {}
        if self.output_format is None:
            self.output_format = {}

# Legacy compatibility - will be removed in future versions
AgentOutput = AgentResult
            
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
