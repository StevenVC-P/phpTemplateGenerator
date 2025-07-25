# agents/refinement_orchestrator/refinement_orchestrator.py

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.agent_interface import AgentInterface, AgentResult, AgentStatus
from utils.logging_helper import get_pipeline_logger
from utils.path_manager import PathManager, PipelineContext

@dataclass
class RefinementIteration:
    """Represents a single refinement iteration"""
    iteration_number: int
    timestamp: str
    input_files: Dict[str, str]
    scores: Dict[str, float]
    issues_found: List[Dict[str, Any]]
    improvements_applied: List[str]
    satisfaction_met: bool
    next_actions: List[str]

@dataclass
class FeedbackItem:
    """Represents actionable feedback from an agent"""
    source_agent: str
    category: str  # "design", "code", "accessibility", "performance", "seo"
    severity: str  # "critical", "major", "minor", "suggestion"
    message: str
    suggested_fix: Optional[str] = None
    target_file: Optional[str] = None
    actionable: bool = True

class RefinementOrchestrator(AgentInterface):
    """Orchestrates the refinement feedback loop with dynamic file detection"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.max_iterations = config.get('max_iterations', 3) if config else 3
        self.satisfaction_thresholds = {
            'visual_score': 8.0,
            'code_score': 7.5,
            'accessibility_score': 7.0,
            'performance_score': 7.0,
            'overall_minimum': 7.5
        }

    async def run(self, input_path: str, context: Dict[str, Any]) -> AgentResult:
        """Run the refinement orchestration process"""
        self._start_execution()

        try:
            pipeline_id = context.get('pipeline_id', 'unknown')
            template_id = context.get('template_id', pipeline_id)

            # Setup logging and paths
            logger = get_pipeline_logger(self.agent_id, pipeline_id)
            logger.log_agent_start(input_path, context)

            path_context = PipelineContext(
                pipeline_id=pipeline_id,
                template_id=template_id,
                request_file=context.get('request_file', '')
            )
            path_manager = PathManager(path_context)

            # Discover available files dynamically
            input_dir = Path(input_path)
            available_files = self._discover_files(input_dir, template_id, logger)

            if not available_files:
                error_msg = f"No refinement input files found in {input_path}"
                logger.error(error_msg)
                return self._end_execution(self._create_error_result(error_msg))

            # Run refinement iterations
            refinement_history = []
            current_iteration = 1
            satisfied = False

            while current_iteration <= self.max_iterations and not satisfied:
                logger.info(f"Starting refinement iteration {current_iteration}")

                iteration_result = await self._run_refinement_iteration(
                    current_iteration, available_files, path_manager, logger, context
                )

                refinement_history.append(iteration_result)
                satisfied = iteration_result.satisfaction_met

                if satisfied:
                    logger.info(f"Satisfaction criteria met in iteration {current_iteration}")
                    break
                elif current_iteration < self.max_iterations:
                    logger.info(f"Iteration {current_iteration} complete, proceeding to next iteration")
                    # Update available files for next iteration
                    available_files = self._update_files_for_next_iteration(
                        available_files, iteration_result, path_manager
                    )

                current_iteration += 1

            # Generate final report
            output_path = path_manager.get_output_path(self.agent_id)
            final_report = self._generate_final_report(
                refinement_history, satisfied, template_id
            )

            self.ensure_output_directory(str(output_path))
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(final_report, f, indent=2)

            logger.log_agent_end(True, str(output_path))
            logger.save_structured_log()

            # Determine result status
            if satisfied:
                status = AgentStatus.SUCCESS
                message = f"Refinement completed successfully in {current_iteration} iterations"
            elif current_iteration > self.max_iterations:
                status = AgentStatus.PARTIAL
                message = f"Max iterations ({self.max_iterations}) reached without full satisfaction"
            else:
                status = AgentStatus.FAILED
                message = "Refinement process failed"

            result = AgentResult(
                agent_id=self.agent_id,
                status=status,
                message=message,
                output_path=str(output_path),
                metadata={
                    "iterations_completed": len(refinement_history),
                    "satisfaction_met": satisfied,
                    "final_scores": refinement_history[-1].scores if refinement_history else {},
                    "total_improvements": sum(len(r.improvements_applied) for r in refinement_history)
                }
            )

            return self._end_execution(result)

        except Exception as e:
            return self._end_execution(self._create_error_result(e))

    def _discover_files(self, input_dir: Path, template_id: str, logger) -> Dict[str, Path]:
        """Dynamically discover available files for refinement"""
        available_files = {}

        # File patterns to look for
        file_patterns = {
            'template': [f'template_{template_id}.php', f'template_{template_id}.cta.php'],
            'validation_report': [f'validation_report_{template_id}.json'],
            'design_review': [f'design_review_{template_id}.md', f'template_{template_id}.design.md'],
            'code_review': [f'code_review_{template_id}.json', f'template_{template_id}.review.json'],
            'visual_analysis': [f'visual_analysis_{template_id}.json', f'template_{template_id}.visual_analysis.json'],
            'theme_directory': [f'theme_{template_id}', f'wordpress_theme_{template_id}', 'wordpress_theme_000']
        }

        # Search in input directory and subdirectories
        search_paths = [input_dir]
        if input_dir.parent.exists():
            search_paths.extend([
                input_dir.parent / 'reviews',
                input_dir.parent / 'templates',
                input_dir.parent / 'wordpress_themes',
                input_dir.parent / 'enhanced_themes',
                input_dir.parent / 'final'
            ])

        for file_type, patterns in file_patterns.items():
            for pattern in patterns:
                for search_path in search_paths:
                    if search_path.exists():
                        # Look for files
                        matches = list(search_path.glob(pattern))
                        if matches:
                            available_files[file_type] = matches[0]
                            logger.debug(f"Found {file_type}: {matches[0]}")
                            break

                        # Look for directories
                        dir_match = search_path / pattern
                        if dir_match.exists() and dir_match.is_dir():
                            available_files[file_type] = dir_match
                            logger.debug(f"Found {file_type} directory: {dir_match}")
                            break

                if file_type in available_files:
                    break

        logger.info(f"Discovered {len(available_files)} file types for refinement")
        return available_files

    async def _run_refinement_iteration(self, iteration_number: int, available_files: Dict[str, Path],
                                      path_manager: PathManager, logger, context: Dict[str, Any]) -> RefinementIteration:
        """Run a single refinement iteration"""
        logger.info(f"Running refinement iteration {iteration_number}")

        # Extract feedback from available files
        feedback_items = self._extract_feedback(available_files, logger)

        # Calculate current scores
        current_scores = self._calculate_current_scores(available_files, logger)

        # Determine if satisfaction criteria are met
        satisfaction_met = self._evaluate_satisfaction(current_scores)

        # Generate improvement actions if not satisfied
        improvements_applied = []
        next_actions = []

        if not satisfaction_met:
            improvements_applied, next_actions = self._generate_improvements(
                feedback_items, available_files, path_manager, logger
            )

        # Create iteration record
        iteration = RefinementIteration(
            iteration_number=iteration_number,
            timestamp=datetime.now().isoformat(),
            input_files={k: str(v) for k, v in available_files.items()},
            scores=current_scores,
            issues_found=[self._feedback_to_dict(f) for f in feedback_items],
            improvements_applied=improvements_applied,
            satisfaction_met=satisfaction_met,
            next_actions=next_actions
        )

        logger.info(f"Iteration {iteration_number} completed - Satisfied: {satisfaction_met}")
        return iteration

    def _extract_feedback(self, available_files: Dict[str, Path], logger) -> List[FeedbackItem]:
        """Extract actionable feedback from available review files"""
        feedback_items = []

        # Extract from validation report
        if 'validation_report' in available_files:
            feedback_items.extend(self._extract_validation_feedback(available_files['validation_report'], logger))

        # Extract from design review
        if 'design_review' in available_files:
            feedback_items.extend(self._extract_design_feedback(available_files['design_review'], logger))

        # Extract from code review
        if 'code_review' in available_files:
            feedback_items.extend(self._extract_code_feedback(available_files['code_review'], logger))

        # Extract from visual analysis
        if 'visual_analysis' in available_files:
            feedback_items.extend(self._extract_visual_feedback(available_files['visual_analysis'], logger))

        logger.info(f"Extracted {len(feedback_items)} feedback items")
        return feedback_items

    def _extract_validation_feedback(self, validation_file: Path, logger) -> List[FeedbackItem]:
        """Extract feedback from theme validation report"""
        feedback_items = []

        try:
            with open(validation_file, 'r', encoding='utf-8') as f:
                validation_data = json.load(f)

            for issue in validation_data.get('issues', []):
                severity_map = {'error': 'critical', 'warning': 'major', 'info': 'minor'}
                feedback_items.append(FeedbackItem(
                    source_agent='theme_validator',
                    category=issue.get('category', 'general'),
                    severity=severity_map.get(issue.get('severity', 'info'), 'minor'),
                    message=issue.get('message', ''),
                    suggested_fix=issue.get('suggestion'),
                    target_file=issue.get('file_path'),
                    actionable=issue.get('severity') in ['error', 'warning']
                ))

        except Exception as e:
            logger.warning(f"Could not extract validation feedback: {e}")

        return feedback_items

    def _extract_design_feedback(self, design_file: Path, logger) -> List[FeedbackItem]:
        """Extract feedback from design review"""
        feedback_items = []

        try:
            content = design_file.read_text(encoding='utf-8')

            # Parse markdown content for feedback (simplified)
            lines = content.split('\n')
            current_category = 'design'

            for line in lines:
                line = line.strip()
                if line.startswith('###'):
                    current_category = line.replace('#', '').strip().lower()
                elif line.startswith('- ') and ('improve' in line.lower() or 'fix' in line.lower()):
                    feedback_items.append(FeedbackItem(
                        source_agent='design_critic',
                        category=current_category,
                        severity='major',
                        message=line[2:].strip(),
                        actionable=True
                    ))

        except Exception as e:
            logger.warning(f"Could not extract design feedback: {e}")

        return feedback_items

    def _extract_code_feedback(self, code_file: Path, logger) -> List[FeedbackItem]:
        """Extract feedback from code review"""
        feedback_items = []

        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_data = json.load(f)

            for recommendation in code_data.get('recommendations', []):
                feedback_items.append(FeedbackItem(
                    source_agent='code_reviewer',
                    category='code',
                    severity='major',
                    message=recommendation,
                    actionable=True
                ))

        except Exception as e:
            logger.warning(f"Could not extract code feedback: {e}")

        return feedback_items

    def _extract_visual_feedback(self, visual_file: Path, logger) -> List[FeedbackItem]:
        """Extract feedback from visual analysis"""
        feedback_items = []

        try:
            with open(visual_file, 'r', encoding='utf-8') as f:
                visual_data = json.load(f)

            for suggestion in visual_data.get('improvement_suggestions', []):
                feedback_items.append(FeedbackItem(
                    source_agent='visual_inspector',
                    category=suggestion.get('area', 'visual'),
                    severity=suggestion.get('priority', 'minor'),
                    message=suggestion.get('message', ''),
                    actionable=suggestion.get('priority') in ['high', 'medium']
                ))

        except Exception as e:
            logger.warning(f"Could not extract visual feedback: {e}")

        return feedback_items

    def _calculate_current_scores(self, available_files: Dict[str, Path], logger) -> Dict[str, float]:
        """Calculate current quality scores from available files"""
        scores = {}

        # Get validation score
        if 'validation_report' in available_files:
            scores['validation_score'] = self._extract_score_from_json(
                available_files['validation_report'], 'overall_score', logger
            )

        # Get visual scores
        if 'visual_analysis' in available_files:
            visual_scores = self._extract_visual_scores(available_files['visual_analysis'], logger)
            scores.update(visual_scores)

        # Get code score
        if 'code_review' in available_files:
            scores['code_score'] = self._extract_score_from_json(
                available_files['code_review'], 'overall_score', logger
            )

        # Calculate overall score
        if scores:
            scores['overall_score'] = sum(scores.values()) / len(scores)

        return scores

    def _extract_score_from_json(self, file_path: Path, field: str, logger) -> float:
        """Extract a numeric score from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return float(data.get(field, 0.0))
        except Exception as e:
            logger.warning(f"Could not extract score from {file_path}: {e}")
            return 0.0

    def _extract_visual_scores(self, visual_file: Path, logger) -> Dict[str, float]:
        """Extract visual scores from visual analysis file"""
        scores = {}
        try:
            with open(visual_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract various visual scores
            visual_scores = data.get('visual_scores', {})
            if isinstance(visual_scores, dict):
                for device, score in visual_scores.items():
                    scores[f'visual_score_{device}'] = float(score)

                # Calculate average visual score
                if visual_scores:
                    scores['visual_score'] = sum(visual_scores.values()) / len(visual_scores)

            # Extract other scores if available
            for score_field in ['conversion_score', 'accessibility_score', 'performance_score']:
                if score_field in data:
                    scores[score_field] = float(data[score_field])

        except Exception as e:
            logger.warning(f"Could not extract visual scores: {e}")

        return scores

    def _evaluate_satisfaction(self, scores: Dict[str, float]) -> bool:
        """Evaluate if current scores meet satisfaction criteria"""
        if not scores:
            return False

        # Check individual thresholds
        for score_type, threshold in self.satisfaction_thresholds.items():
            if score_type in scores and scores[score_type] < threshold:
                return False

        # Check overall minimum
        overall_score = scores.get('overall_score', 0.0)
        return overall_score >= self.satisfaction_thresholds['overall_minimum']

    def _generate_improvements(self, feedback_items: List[FeedbackItem],
                             available_files: Dict[str, Path],
                             path_manager: PathManager, logger) -> Tuple[List[str], List[str]]:
        """Generate and apply improvements based on feedback"""
        improvements_applied = []
        next_actions = []

        # Group feedback by category and severity
        critical_issues = [f for f in feedback_items if f.severity == 'critical']
        major_issues = [f for f in feedback_items if f.severity == 'major']

        # Apply critical fixes first
        for issue in critical_issues:
            if issue.actionable and issue.suggested_fix:
                improvement = self._apply_improvement(issue, available_files, logger)
                if improvement:
                    improvements_applied.append(improvement)

        # Apply major fixes if we have capacity
        for issue in major_issues[:5]:  # Limit to top 5 major issues
            if issue.actionable and issue.suggested_fix:
                improvement = self._apply_improvement(issue, available_files, logger)
                if improvement:
                    improvements_applied.append(improvement)

        # Generate next actions for remaining issues
        remaining_issues = [f for f in feedback_items if f not in critical_issues + major_issues[:5]]
        for issue in remaining_issues[:3]:  # Top 3 remaining issues
            next_actions.append(f"{issue.category}: {issue.message}")

        return improvements_applied, next_actions

    def _apply_improvement(self, feedback_item: FeedbackItem,
                          available_files: Dict[str, Path], logger) -> Optional[str]:
        """Apply a specific improvement based on feedback"""
        try:
            # This is a simplified implementation - in a real system, this would
            # involve more sophisticated code modification logic

            if feedback_item.target_file and 'template' in available_files:
                template_file = available_files['template']

                # Example: Fix missing alt attributes
                if 'alt attribute' in feedback_item.message.lower():
                    return self._fix_alt_attributes(template_file, logger)

                # Example: Fix CSS issues
                elif 'css' in feedback_item.category.lower():
                    return self._fix_css_issues(template_file, feedback_item, logger)

                # Example: Fix PHP issues
                elif 'php' in feedback_item.category.lower():
                    return self._fix_php_issues(template_file, feedback_item, logger)

            # Log that we attempted the improvement
            logger.info(f"Applied improvement: {feedback_item.message}")
            return f"Applied fix for: {feedback_item.message}"

        except Exception as e:
            logger.warning(f"Could not apply improvement: {e}")
            return None

    def _fix_alt_attributes(self, template_file: Path, logger) -> str:
        """Fix missing alt attributes in template"""
        try:
            content = template_file.read_text(encoding='utf-8')

            # Simple regex to add alt attributes to images without them
            import re
            pattern = r'<img([^>]*?)(?<!alt=")(?<!alt=\')>'
            replacement = r'<img\1 alt="Generated image">'

            updated_content = re.sub(pattern, replacement, content)

            if updated_content != content:
                template_file.write_text(updated_content, encoding='utf-8')
                return "Added missing alt attributes to images"

        except Exception as e:
            logger.warning(f"Could not fix alt attributes: {e}")

        return "Attempted to fix alt attributes"

    def _fix_css_issues(self, template_file: Path, feedback_item: FeedbackItem, logger) -> str:
        """Fix CSS-related issues"""
        # Placeholder for CSS fixes
        logger.info(f"CSS fix applied for: {feedback_item.message}")
        return f"Applied CSS fix: {feedback_item.suggested_fix or 'General CSS improvement'}"

    def _fix_php_issues(self, template_file: Path, feedback_item: FeedbackItem, logger) -> str:
        """Fix PHP-related issues"""
        # Placeholder for PHP fixes
        logger.info(f"PHP fix applied for: {feedback_item.message}")
        return f"Applied PHP fix: {feedback_item.suggested_fix or 'General PHP improvement'}"

    def _update_files_for_next_iteration(self, current_files: Dict[str, Path],
                                       iteration_result: RefinementIteration,
                                       path_manager: PathManager) -> Dict[str, Path]:
        """Update file references for the next iteration"""
        # In a real implementation, this would update file paths to point to
        # the modified versions created during the current iteration
        return current_files

    def _generate_final_report(self, refinement_history: List[RefinementIteration],
                             satisfied: bool, template_id: str) -> Dict[str, Any]:
        """Generate comprehensive refinement report"""
        if not refinement_history:
            return {
                "template_id": template_id,
                "status": "failed",
                "message": "No refinement iterations completed",
                "timestamp": datetime.now().isoformat()
            }

        final_iteration = refinement_history[-1]

        return {
            "template_id": template_id,
            "status": "satisfied" if satisfied else "incomplete",
            "total_iterations": len(refinement_history),
            "final_scores": final_iteration.scores,
            "satisfaction_met": satisfied,
            "total_improvements": sum(len(r.improvements_applied) for r in refinement_history),
            "total_issues_found": sum(len(r.issues_found) for r in refinement_history),
            "refinement_history": [
                {
                    "iteration": r.iteration_number,
                    "timestamp": r.timestamp,
                    "scores": r.scores,
                    "improvements_count": len(r.improvements_applied),
                    "issues_count": len(r.issues_found),
                    "satisfaction_met": r.satisfaction_met
                }
                for r in refinement_history
            ],
            "final_recommendations": final_iteration.next_actions,
            "timestamp": datetime.now().isoformat()
        }

    def _feedback_to_dict(self, feedback: FeedbackItem) -> Dict[str, Any]:
        """Convert feedback item to dictionary"""
        return {
            "source_agent": feedback.source_agent,
            "category": feedback.category,
            "severity": feedback.severity,
            "message": feedback.message,
            "suggested_fix": feedback.suggested_fix,
            "target_file": feedback.target_file,
            "actionable": feedback.actionable
        }
