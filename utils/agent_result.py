from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class AgentResult:
    agent_id: str
    success: bool
    output_file: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
