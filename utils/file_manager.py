#!/usr/bin/env python3
"""
File Management Utilities for PHP Template Generator
Handles file I/O, formatting, and directory operations
"""

import os
import json
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """Utility class for file and directory operations"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            "input", "specs", "prompts", "templates", 
            "reviews", "final", "agents", "mcp", "utils"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(exist_ok=True)
            logger.debug(f"Ensured directory exists: {dir_path}")
    
    def read_file(self, file_path: Union[str, Path]) -> str:
        """Read text content from a file"""
        try:
            full_path = self.base_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            raise
    
    def write_file(self, file_path: Union[str, Path], content: str, create_dirs: bool = True) -> bool:
        """Write text content to a file"""
        try:
            full_path = self.base_path / file_path
            
            if create_dirs:
                full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Successfully wrote file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return False
    
    def read_json(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Read and parse JSON file"""
        try:
            content = self.read_file(file_path)
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to read JSON file {file_path}: {e}")
            raise
    
    def write_json(self, file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> bool:
        """Write data to JSON file"""
        try:
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            return self.write_file(file_path, content)
        except Exception as e:
            logger.error(f"Failed to write JSON file {file_path}: {e}")
            return False
    
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Copy a file from source to destination"""
        try:
            source_path = self.base_path / source
            dest_path = self.base_path / destination
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            
            logger.info(f"Copied file: {source} -> {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to copy file {source} -> {destination}: {e}")
            return False
    
    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Move a file from source to destination"""
        try:
            source_path = self.base_path / source
            dest_path = self.base_path / destination
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
            
            logger.info(f"Moved file: {source} -> {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to move file {source} -> {destination}: {e}")
            return False
    
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """Delete a file"""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            else:
                logger.warning(f"File not found for deletion: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False
    
    def list_files(self, directory: Union[str, Path], pattern: str = "*", recursive: bool = False) -> List[Path]:
        """List files in a directory"""
        try:
            dir_path = self.base_path / directory
            if not dir_path.exists():
                return []
            
            if recursive:
                return list(dir_path.rglob(pattern))
            else:
                return list(dir_path.glob(pattern))
                
        except Exception as e:
            logger.error(f"Failed to list files in {directory}: {e}")
            return []
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get file information"""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return {}
            
            stat = full_path.stat()
            
            return {
                'path': str(file_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'is_file': full_path.is_file(),
                'is_directory': full_path.is_dir(),
                'extension': full_path.suffix,
                'name': full_path.name,
                'stem': full_path.stem
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info for {file_path}: {e}")
            return {}
    
    def calculate_file_hash(self, file_path: Union[str, Path], algorithm: str = 'md5') -> Optional[str]:
        """Calculate file hash"""
        try:
            full_path = self.base_path / file_path
            hash_obj = hashlib.new(algorithm)
            
            with open(full_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return None
    
    def create_backup(self, file_path: Union[str, Path]) -> Optional[str]:
        """Create a backup of a file"""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{full_path.stem}_{timestamp}{full_path.suffix}"
            backup_path = full_path.parent / "backups" / backup_name
            
            backup_path.parent.mkdir(exist_ok=True)
            shutil.copy2(full_path, backup_path)
            
            logger.info(f"Created backup: {backup_path}")
            return str(backup_path.relative_to(self.base_path))
            
        except Exception as e:
            logger.error(f"Failed to create backup for {file_path}: {e}")
            return None
    
    def cleanup_temp_files(self, max_age_hours: int = 24):
        """Clean up temporary files older than specified hours"""
        try:
            temp_patterns = ["*.tmp", "*.temp", "*~", ".#*"]
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            
            deleted_count = 0
            for pattern in temp_patterns:
                for file_path in self.list_files(".", pattern, recursive=True):
                    full_path = self.base_path / file_path
                    if full_path.stat().st_mtime < cutoff_time:
                        full_path.unlink()
                        deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} temporary files")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup temp files: {e}")
            return 0

class TemplateFileManager(FileManager):
    """Specialized file manager for template operations"""
    
    def save_template_spec(self, spec_data: Dict[str, Any], template_id: str) -> bool:
        """Save template specification"""
        file_path = f"specs/{template_id}_spec.json"
        return self.write_json(file_path, spec_data)
    
    def load_template_spec(self, template_id: str) -> Dict[str, Any]:
        """Load template specification"""
        file_path = f"specs/{template_id}_spec.json"
        return self.read_json(file_path)
    
    def save_template_prompt(self, prompt_data: Dict[str, Any], prompt_id: str) -> bool:
        """Save template generation prompt"""
        file_path = f"prompts/{prompt_id}.json"
        return self.write_json(file_path, prompt_data)
    
    def save_template_code(self, code_content: str, template_id: str, variant: str = "") -> bool:
        """Save template PHP code"""
        suffix = f".{variant}" if variant else ""
        file_path = f"templates/{template_id}{suffix}.php"
        return self.write_file(file_path, code_content)
    
    def save_review_data(self, review_data: Dict[str, Any], template_id: str, review_type: str) -> bool:
        """Save review data"""
        if review_type == "design":
            file_path = f"reviews/{template_id}.design.md"
            # Convert review data to markdown format
            content = self.format_design_review(review_data)
            return self.write_file(file_path, content)
        else:
            file_path = f"reviews/{template_id}.{review_type}.json"
            return self.write_json(file_path, review_data)
    
    def format_design_review(self, review_data: Dict[str, Any]) -> str:
        """Format design review data as markdown"""
        # This is a simplified formatter - expand as needed
        content = f"# Design Review: {review_data.get('template_id', 'Unknown')}\n\n"
        content += f"**Overall Score:** {review_data.get('overall_score', 'N/A')}/10\n\n"
        
        for category, details in review_data.get('categories', {}).items():
            content += f"## {category.replace('_', ' ').title()}\n"
            content += f"**Score:** {details.get('score', 'N/A')}/10\n\n"
            
            for comment in details.get('comments', []):
                content += f"- {comment}\n"
            content += "\n"
        
        return content
    
    def package_final_template(self, template_id: str) -> bool:
        """Package final template with all assets"""
        try:
            final_dir = Path(f"final/{template_id}")
            final_dir.mkdir(exist_ok=True)
            
            # Copy main template
            template_files = self.list_files("templates", f"{template_id}*.php")
            for template_file in template_files:
                dest_name = "index.php" if template_file.name == f"{template_id}.php" else template_file.name
                self.copy_file(template_file, final_dir / dest_name)
            
            # Copy documentation
            readme_path = f"final/{template_id}/README.md"
            if not Path(self.base_path / readme_path).exists():
                # Generate basic README if not exists
                readme_content = f"# Template {template_id}\n\nGenerated template package.\n"
                self.write_file(readme_path, readme_content)
            
            logger.info(f"Packaged final template: {template_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to package template {template_id}: {e}")
            return False

# Utility functions
def get_file_manager(base_path: str = ".") -> TemplateFileManager:
    """Get a configured template file manager instance"""
    return TemplateFileManager(base_path)

def ensure_project_structure(base_path: str = "."):
    """Ensure the complete project structure exists"""
    fm = FileManager(base_path)
    fm.ensure_directories()
    logger.info("Project structure verified")
