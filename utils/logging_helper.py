# utils/logging_helper.py

import logging
import json
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

class LogLevel(Enum):
    """Standardized log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    level: str
    agent_id: str
    pipeline_id: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)

class PipelineLogger:
    """Enhanced logger for pipeline operations with structured logging"""
    
    def __init__(self, agent_id: str, pipeline_id: str, log_dir: Path = None):
        self.agent_id = agent_id
        self.pipeline_id = pipeline_id
        self.log_dir = log_dir or Path("pipeline_output") / f"pipeline_{pipeline_id}" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup file and console loggers
        self.logger = self._setup_logger()
        self.log_entries: List[LogEntry] = []
    
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logger with file and console handlers"""
        logger_name = f"pipeline.{self.pipeline_id}.{self.agent_id}"
        logger = logging.getLogger(logger_name)
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        logger.setLevel(logging.DEBUG)
        
        # File handler for agent-specific logs
        agent_log_file = self.log_dir / f"{self.agent_id}.log"
        file_handler = logging.FileHandler(agent_log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for immediate feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            f'%(asctime)s - {self.agent_id} - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _log_entry(self, level: LogLevel, message: str, 
                   metadata: Dict[str, Any] = None, error: Exception = None) -> None:
        """Create and store a structured log entry"""
        error_details = None
        if error:
            error_details = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "traceback": traceback.format_exc()
            }
        
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level.value,
            agent_id=self.agent_id,
            pipeline_id=self.pipeline_id,
            message=message,
            metadata=metadata,
            error_details=error_details
        )
        
        self.log_entries.append(entry)
        
        # Also log to standard logger
        log_method = getattr(self.logger, level.value.lower())
        log_method(message)
        
        if error:
            self.logger.debug(f"Error details: {error_details}")
    
    def debug(self, message: str, metadata: Dict[str, Any] = None) -> None:
        """Log debug message"""
        self._log_entry(LogLevel.DEBUG, message, metadata)
    
    def info(self, message: str, metadata: Dict[str, Any] = None) -> None:
        """Log info message"""
        self._log_entry(LogLevel.INFO, message, metadata)
    
    def warning(self, message: str, metadata: Dict[str, Any] = None) -> None:
        """Log warning message"""
        self._log_entry(LogLevel.WARNING, message, metadata)
    
    def error(self, message: str, error: Exception = None, 
              metadata: Dict[str, Any] = None) -> None:
        """Log error message with optional exception details"""
        self._log_entry(LogLevel.ERROR, message, metadata, error)
    
    def critical(self, message: str, error: Exception = None, 
                 metadata: Dict[str, Any] = None) -> None:
        """Log critical message with optional exception details"""
        self._log_entry(LogLevel.CRITICAL, message, metadata, error)
    
    def log_agent_start(self, input_path: str, context: Dict[str, Any] = None) -> None:
        """Log agent execution start"""
        self.info(f"Starting {self.agent_id} execution", {
            "input_path": input_path,
            "context": context or {}
        })
    
    def log_agent_end(self, success: bool, output_path: str = None, 
                      execution_time: float = None) -> None:
        """Log agent execution end"""
        status = "SUCCESS" if success else "FAILED"
        self.info(f"Completed {self.agent_id} execution - {status}", {
            "success": success,
            "output_path": output_path,
            "execution_time": execution_time
        })
    
    def log_file_operation(self, operation: str, file_path: str, 
                          success: bool = True, error: Exception = None) -> None:
        """Log file operations"""
        message = f"File {operation}: {file_path}"
        if success:
            self.debug(message)
        else:
            self.error(f"Failed {message}", error)
    
    def log_validation_result(self, validation_type: str, passed: bool, 
                             details: Dict[str, Any] = None) -> None:
        """Log validation results"""
        status = "PASSED" if passed else "FAILED"
        self.info(f"Validation {validation_type}: {status}", details)
    
    def save_structured_log(self) -> Path:
        """Save structured log entries to JSON file"""
        log_file = self.log_dir / f"{self.agent_id}_structured.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump([entry.to_dict() for entry in self.log_entries], f, indent=2)
        
        return log_file
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors and warnings"""
        errors = [entry for entry in self.log_entries if entry.level == LogLevel.ERROR.value]
        warnings = [entry for entry in self.log_entries if entry.level == LogLevel.WARNING.value]
        
        return {
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": [{"message": e.message, "timestamp": e.timestamp} for e in errors],
            "warnings": [{"message": w.message, "timestamp": w.timestamp} for w in warnings]
        }

class PipelineLogAggregator:
    """Aggregates logs from multiple agents in a pipeline"""
    
    def __init__(self, pipeline_id: str, log_dir: Path = None):
        self.pipeline_id = pipeline_id
        self.log_dir = log_dir or Path("pipeline_output") / f"pipeline_{pipeline_id}" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def aggregate_logs(self) -> Dict[str, Any]:
        """Aggregate all agent logs for the pipeline"""
        aggregated = {
            "pipeline_id": self.pipeline_id,
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "summary": {
                "total_errors": 0,
                "total_warnings": 0,
                "agents_with_errors": [],
                "agents_with_warnings": []
            }
        }
        
        # Process each agent's structured log
        for log_file in self.log_dir.glob("*_structured.json"):
            agent_id = log_file.stem.replace("_structured", "")
            
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    agent_logs = json.load(f)
                
                # Analyze agent logs
                errors = [log for log in agent_logs if log["level"] == "ERROR"]
                warnings = [log for log in agent_logs if log["level"] == "WARNING"]
                
                aggregated["agents"][agent_id] = {
                    "total_entries": len(agent_logs),
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "last_entry": agent_logs[-1] if agent_logs else None
                }
                
                # Update summary
                aggregated["summary"]["total_errors"] += len(errors)
                aggregated["summary"]["total_warnings"] += len(warnings)
                
                if errors:
                    aggregated["summary"]["agents_with_errors"].append(agent_id)
                if warnings:
                    aggregated["summary"]["agents_with_warnings"].append(agent_id)
                    
            except Exception as e:
                aggregated["agents"][agent_id] = {
                    "error": f"Failed to process log file: {str(e)}"
                }
        
        # Save aggregated log
        aggregated_file = self.log_dir / "pipeline_summary.json"
        with open(aggregated_file, 'w', encoding='utf-8') as f:
            json.dump(aggregated, f, indent=2)
        
        return aggregated
    
    def get_pipeline_health(self) -> Dict[str, Any]:
        """Get overall pipeline health status"""
        summary = self.aggregate_logs()
        
        total_errors = summary["summary"]["total_errors"]
        total_warnings = summary["summary"]["total_warnings"]
        
        if total_errors > 0:
            health_status = "CRITICAL"
        elif total_warnings > 5:
            health_status = "WARNING"
        elif total_warnings > 0:
            health_status = "CAUTION"
        else:
            health_status = "HEALTHY"
        
        return {
            "status": health_status,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "problematic_agents": summary["summary"]["agents_with_errors"],
            "timestamp": datetime.now().isoformat()
        }

def get_pipeline_logger(agent_id: str, pipeline_id: str, log_dir: Path = None) -> PipelineLogger:
    """Factory function to get a pipeline logger"""
    return PipelineLogger(agent_id, pipeline_id, log_dir)
