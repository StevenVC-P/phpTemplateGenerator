# utils/pipeline_state_manager.py

import json
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import fcntl
import os

class PipelineStatus(Enum):
    """Pipeline execution status"""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentStatus(Enum):
    """Agent execution status within a pipeline"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class AgentState:
    """State information for an agent within a pipeline"""
    agent_id: str
    status: AgentStatus
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class PipelineState:
    """Complete state information for a pipeline"""
    pipeline_id: str
    status: PipelineStatus
    request_file: str
    start_time: str
    end_time: Optional[str] = None
    agents: Dict[str, AgentState] = None
    error_traceback: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.agents is None:
            self.agents = {}
        if self.metadata is None:
            self.metadata = {}

class PipelineStateManager:
    """Thread-safe manager for pipeline state persistence and querying"""
    
    def __init__(self, state_file: str = "pipeline_state.json"):
        self.state_file = Path(state_file)
        self.lock = threading.RLock()
        self._ensure_state_file()
    
    def _ensure_state_file(self) -> None:
        """Ensure state file exists with proper structure"""
        if not self.state_file.exists():
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump({"pipelines": {}, "metadata": {"created": datetime.now().isoformat()}}, f)
    
    def _load_state(self) -> Dict[str, Any]:
        """Load state from file with file locking"""
        with self.lock:
            try:
                with open(self.state_file, 'r') as f:
                    # Use file locking for concurrent access
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        data = json.load(f)
                        # Migrate old format if needed
                        if "pipelines" not in data:
                            data = {"pipelines": data, "metadata": {"migrated": datetime.now().isoformat()}}
                        return data
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except (FileNotFoundError, json.JSONDecodeError):
                return {"pipelines": {}, "metadata": {"created": datetime.now().isoformat()}}
    
    def _save_state(self, data: Dict[str, Any]) -> None:
        """Save state to file with file locking"""
        with self.lock:
            # Create backup
            backup_file = self.state_file.with_suffix('.json.backup')
            if self.state_file.exists():
                self.state_file.replace(backup_file)
            
            try:
                with open(self.state_file, 'w') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        json.dump(data, f, indent=2)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except Exception as e:
                # Restore backup on failure
                if backup_file.exists():
                    backup_file.replace(self.state_file)
                raise e
    
    def create_pipeline(self, pipeline_id: str, request_file: str, 
                       agent_list: List[str] = None) -> PipelineState:
        """Create a new pipeline state"""
        pipeline_state = PipelineState(
            pipeline_id=pipeline_id,
            status=PipelineStatus.QUEUED,
            request_file=request_file,
            start_time=datetime.now().isoformat()
        )
        
        # Initialize agent states
        if agent_list:
            for agent_id in agent_list:
                pipeline_state.agents[agent_id] = AgentState(
                    agent_id=agent_id,
                    status=AgentStatus.PENDING
                )
        
        # Save to state file
        data = self._load_state()
        data["pipelines"][pipeline_id] = asdict(pipeline_state)
        self._save_state(data)
        
        return pipeline_state
    
    def update_pipeline_status(self, pipeline_id: str, status: PipelineStatus, 
                              error_traceback: str = None) -> None:
        """Update pipeline status"""
        data = self._load_state()
        
        if pipeline_id not in data["pipelines"]:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        data["pipelines"][pipeline_id]["status"] = status.value
        
        if status in [PipelineStatus.COMPLETED, PipelineStatus.FAILED, PipelineStatus.CANCELLED]:
            data["pipelines"][pipeline_id]["end_time"] = datetime.now().isoformat()
        
        if error_traceback:
            data["pipelines"][pipeline_id]["error_traceback"] = error_traceback
        
        self._save_state(data)
    
    def update_agent_status(self, pipeline_id: str, agent_id: str, 
                           status: AgentStatus, **kwargs) -> None:
        """Update agent status within a pipeline"""
        data = self._load_state()
        
        if pipeline_id not in data["pipelines"]:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        # Initialize agent if not exists
        if agent_id not in data["pipelines"][pipeline_id]["agents"]:
            data["pipelines"][pipeline_id]["agents"][agent_id] = asdict(AgentState(
                agent_id=agent_id,
                status=status
            ))
        
        agent_data = data["pipelines"][pipeline_id]["agents"][agent_id]
        agent_data["status"] = status.value
        
        # Update timestamps
        if status == AgentStatus.RUNNING and not agent_data.get("start_time"):
            agent_data["start_time"] = datetime.now().isoformat()
        elif status in [AgentStatus.SUCCESS, AgentStatus.FAILED, AgentStatus.SKIPPED]:
            agent_data["end_time"] = datetime.now().isoformat()
            
            # Calculate execution time
            if agent_data.get("start_time"):
                start = datetime.fromisoformat(agent_data["start_time"])
                end = datetime.now()
                agent_data["execution_time"] = (end - start).total_seconds()
        
        # Update other fields
        for key, value in kwargs.items():
            if key in ["input_path", "output_path", "error_message", "metadata"]:
                agent_data[key] = value
        
        self._save_state(data)
    
    def get_pipeline_state(self, pipeline_id: str) -> Optional[PipelineState]:
        """Get current state of a pipeline"""
        data = self._load_state()
        pipeline_data = data["pipelines"].get(pipeline_id)
        
        if not pipeline_data:
            return None
        
        # Convert agent data back to AgentState objects
        agents = {}
        for agent_id, agent_data in pipeline_data.get("agents", {}).items():
            agents[agent_id] = AgentState(
                agent_id=agent_data["agent_id"],
                status=AgentStatus(agent_data["status"]),
                start_time=agent_data.get("start_time"),
                end_time=agent_data.get("end_time"),
                input_path=agent_data.get("input_path"),
                output_path=agent_data.get("output_path"),
                error_message=agent_data.get("error_message"),
                execution_time=agent_data.get("execution_time", 0.0),
                metadata=agent_data.get("metadata", {})
            )
        
        return PipelineState(
            pipeline_id=pipeline_data["pipeline_id"],
            status=PipelineStatus(pipeline_data["status"]),
            request_file=pipeline_data["request_file"],
            start_time=pipeline_data["start_time"],
            end_time=pipeline_data.get("end_time"),
            agents=agents,
            error_traceback=pipeline_data.get("error_traceback"),
            metadata=pipeline_data.get("metadata", {})
        )
    
    def get_running_pipelines(self) -> List[str]:
        """Get list of currently running pipeline IDs"""
        data = self._load_state()
        return [
            pipeline_id for pipeline_id, pipeline_data in data["pipelines"].items()
            if pipeline_data["status"] == PipelineStatus.RUNNING.value
        ]
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Get summary of all pipelines"""
        data = self._load_state()
        
        summary = {
            "total_pipelines": len(data["pipelines"]),
            "by_status": {},
            "recent_pipelines": [],
            "problematic_pipelines": []
        }
        
        # Count by status
        for status in PipelineStatus:
            summary["by_status"][status.value] = 0
        
        # Analyze pipelines
        pipeline_list = []
        for pipeline_id, pipeline_data in data["pipelines"].items():
            status = pipeline_data["status"]
            summary["by_status"][status] += 1
            
            pipeline_list.append({
                "pipeline_id": pipeline_id,
                "status": status,
                "start_time": pipeline_data["start_time"],
                "end_time": pipeline_data.get("end_time"),
                "request_file": pipeline_data["request_file"]
            })
            
            # Track problematic pipelines
            if status == PipelineStatus.FAILED.value:
                summary["problematic_pipelines"].append(pipeline_id)
        
        # Sort by start time and get recent ones
        pipeline_list.sort(key=lambda x: x["start_time"], reverse=True)
        summary["recent_pipelines"] = pipeline_list[:10]
        
        return summary
    
    def cleanup_old_pipelines(self, days_old: int = 7) -> int:
        """Clean up pipeline states older than specified days"""
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        data = self._load_state()
        
        pipelines_to_remove = []
        for pipeline_id, pipeline_data in data["pipelines"].items():
            try:
                start_time = datetime.fromisoformat(pipeline_data["start_time"])
                if start_time.timestamp() < cutoff_date:
                    # Only remove completed or failed pipelines
                    if pipeline_data["status"] in [PipelineStatus.COMPLETED.value, PipelineStatus.FAILED.value]:
                        pipelines_to_remove.append(pipeline_id)
            except (ValueError, KeyError):
                # Remove malformed entries
                pipelines_to_remove.append(pipeline_id)
        
        # Remove old pipelines
        for pipeline_id in pipelines_to_remove:
            del data["pipelines"][pipeline_id]
        
        if pipelines_to_remove:
            self._save_state(data)
        
        return len(pipelines_to_remove)
