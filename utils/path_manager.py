# utils/path_manager.py

import os
import re
from pathlib import Path
from typing import Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum

class PathType(Enum):
    """Types of paths in the pipeline"""
    INPUT = "inputs"
    INTERMEDIATE = "intermediate" 
    OUTPUT = "outputs"
    LOGS = "logs"
    SPECS = "specs"
    PROMPTS = "prompts"
    TEMPLATES = "templates"
    REVIEWS = "reviews"
    DESIGN_VARIATIONS = "design_variations"
    WORDPRESS_THEMES = "wordpress_themes"
    ENHANCED_THEMES = "enhanced_themes"
    FINAL = "final"

@dataclass
class PipelineContext:
    """Context information for a pipeline execution"""
    pipeline_id: str
    template_id: str
    request_file: str
    base_dir: str = "pipeline_output"
    
    @property
    def pipeline_dir(self) -> Path:
        """Get the main pipeline directory"""
        return Path(self.base_dir) / f"pipeline_{self.pipeline_id}"

class PathManager:
    """Centralized path management for consistent file organization"""
    
    def __init__(self, context: PipelineContext):
        self.context = context
        self._ensure_base_structure()
    
    def _ensure_base_structure(self) -> None:
        """Create the base directory structure for the pipeline"""
        base_dir = self.context.pipeline_dir
        
        # Create main pipeline directory
        base_dir.mkdir(parents=True, exist_ok=True)
        
        # Create standard subdirectories
        for path_type in PathType:
            (base_dir / path_type.value).mkdir(exist_ok=True)
    
    def get_path(self, path_type: PathType, filename: str = None, 
                 agent_id: str = None, create_dirs: bool = True) -> Path:
        """
        Get a standardized path for the given type and context
        
        Args:
            path_type: Type of path to generate
            filename: Optional filename to append
            agent_id: Optional agent ID for agent-specific paths
            create_dirs: Whether to create directories if they don't exist
            
        Returns:
            Path object for the requested location
        """
        base_path = self.context.pipeline_dir / path_type.value
        
        # Add agent-specific subdirectory if provided
        if agent_id:
            base_path = base_path / agent_id
        
        # Create directories if requested
        if create_dirs:
            base_path.mkdir(parents=True, exist_ok=True)
        
        # Add filename if provided
        if filename:
            # Replace template placeholders in filename
            filename = self._resolve_filename_template(filename)
            base_path = base_path / filename
        
        return base_path
    
    def _resolve_filename_template(self, filename: str) -> str:
        """Resolve template placeholders in filenames"""
        replacements = {
            '{pipeline_id}': self.context.pipeline_id,
            '{template_id}': self.context.template_id,
            '{id}': self.context.template_id,  # Legacy compatibility
        }
        
        for placeholder, value in replacements.items():
            filename = filename.replace(placeholder, value)
        
        return filename
    
    def get_input_path(self, agent_id: str) -> Path:
        """Get the input path for a specific agent based on pipeline flow"""
        agent_input_mapping = {
            'request_interpreter': self.context.request_file,
            'prompt_designer': self.get_path(PathType.SPECS, f"template_spec_{self.context.template_id}.json"),
            'design_variation_generator': self.get_path(PathType.SPECS, f"template_spec_{self.context.template_id}.json"),
            'template_engineer': self.get_path(PathType.PROMPTS, f"prompt_{self.context.template_id}.json"),
            'cta_optimizer': self.get_path(PathType.TEMPLATES, f"template_{self.context.template_id}.php"),
            'wordpress_theme_assembler': self.get_path(PathType.TEMPLATES, f"template_{self.context.template_id}.cta.php"),
            'mobile_ux_enhancer': self.get_path(PathType.WORDPRESS_THEMES, f"theme_{self.context.template_id}"),
            'seo_optimizer': self.get_path(PathType.ENHANCED_THEMES, f"mobile_enhanced_{self.context.template_id}"),
            'component_library': self.get_path(PathType.ENHANCED_THEMES, f"seo_enhanced_{self.context.template_id}"),
            'design_critic': self.get_path(PathType.ENHANCED_THEMES, f"component_enhanced_{self.context.template_id}"),
            'visual_inspector': self.get_path(PathType.ENHANCED_THEMES, f"component_enhanced_{self.context.template_id}"),
            'code_reviewer': self.get_path(PathType.TEMPLATES, f"template_{self.context.template_id}.cta.php"),
            'refinement_orchestrator': self.get_path(PathType.REVIEWS),
            'theme_validator': self.get_path(PathType.FINAL, f"theme_{self.context.template_id}"),
            'packager': self.get_path(PathType.FINAL, f"validated_theme_{self.context.template_id}")
        }
        
        input_path = agent_input_mapping.get(agent_id)
        if isinstance(input_path, str):
            return Path(input_path)
        return input_path or self.get_path(PathType.INPUT)
    
    def get_output_path(self, agent_id: str, filename: str = None) -> Path:
        """Get the output path for a specific agent"""
        if not filename:
            filename = self._get_default_output_filename(agent_id)
        
        agent_output_mapping = {
            'request_interpreter': self.get_path(PathType.SPECS, filename),
            'prompt_designer': self.get_path(PathType.PROMPTS, filename),
            'design_variation_generator': self.get_path(PathType.DESIGN_VARIATIONS, filename),
            'template_engineer': self.get_path(PathType.TEMPLATES, filename),
            'cta_optimizer': self.get_path(PathType.TEMPLATES, filename),
            'wordpress_theme_assembler': self.get_path(PathType.WORDPRESS_THEMES, filename),
            'mobile_ux_enhancer': self.get_path(PathType.ENHANCED_THEMES, filename),
            'seo_optimizer': self.get_path(PathType.ENHANCED_THEMES, filename),
            'component_library': self.get_path(PathType.ENHANCED_THEMES, filename),
            'design_critic': self.get_path(PathType.REVIEWS, filename),
            'visual_inspector': self.get_path(PathType.REVIEWS, filename),
            'code_reviewer': self.get_path(PathType.REVIEWS, filename),
            'refinement_orchestrator': self.get_path(PathType.INTERMEDIATE, filename),
            'theme_validator': self.get_path(PathType.REVIEWS, filename),
            'packager': self.get_path(PathType.FINAL, filename)
        }
        
        return agent_output_mapping.get(agent_id, self.get_path(PathType.OUTPUT, filename))
    
    def _get_default_output_filename(self, agent_id: str) -> str:
        """Get default output filename for an agent"""
        default_filenames = {
            'request_interpreter': f"template_spec_{self.context.template_id}.json",
            'prompt_designer': f"prompt_{self.context.template_id}.json",
            'design_variation_generator': f"design_variation_{self.context.template_id}.json",
            'template_engineer': f"template_{self.context.template_id}.php",
            'cta_optimizer': f"template_{self.context.template_id}.cta.php",
            'wordpress_theme_assembler': f"theme_{self.context.template_id}",
            'mobile_ux_enhancer': f"mobile_enhanced_{self.context.template_id}",
            'seo_optimizer': f"seo_enhanced_{self.context.template_id}",
            'component_library': f"component_enhanced_{self.context.template_id}",
            'design_critic': f"design_review_{self.context.template_id}.md",
            'visual_inspector': f"visual_analysis_{self.context.template_id}.json",
            'code_reviewer': f"code_review_{self.context.template_id}.json",
            'refinement_orchestrator': f"refinement_{self.context.template_id}.json",
            'theme_validator': f"validation_report_{self.context.template_id}.json",
            'packager': f"final_package_{self.context.template_id}.zip"
        }
        
        return default_filenames.get(agent_id, f"{agent_id}_output_{self.context.template_id}")
    
    def get_log_path(self, agent_id: str) -> Path:
        """Get log file path for an agent"""
        return self.get_path(PathType.LOGS, f"{agent_id}_{self.context.template_id}.log")
    
    def cleanup_pipeline(self) -> None:
        """Clean up pipeline directory (use with caution)"""
        import shutil
        if self.context.pipeline_dir.exists():
            shutil.rmtree(self.context.pipeline_dir)
    
    @staticmethod
    def extract_template_id(filename: str) -> Optional[str]:
        """Extract template ID from filename using common patterns"""
        patterns = [
            r'template_([a-zA-Z0-9_]+)',
            r'pipeline_([a-zA-Z0-9_]+)',
            r'theme_([a-zA-Z0-9_]+)',
            r'([a-zA-Z0-9_]{8,})'  # Generic ID pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def create_context_from_pipeline_id(pipeline_id: str, request_file: str = None) -> 'PipelineContext':
        """Create a pipeline context from a pipeline ID"""
        # Extract template ID from pipeline ID
        template_id = pipeline_id.replace('pipeline_', '') if pipeline_id.startswith('pipeline_') else pipeline_id
        
        return PipelineContext(
            pipeline_id=pipeline_id,
            template_id=template_id,
            request_file=request_file or "input/default_request.md"
        )
