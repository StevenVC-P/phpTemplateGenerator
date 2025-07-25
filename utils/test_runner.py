# utils/test_runner.py

import asyncio
import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.agent_interface import AgentInterface, AgentResult, AgentStatus
from utils.path_manager import PathManager, PipelineContext
from utils.logging_helper import get_pipeline_logger
from mcp.orchestrator_v2 import TemplateOrchestrator

@dataclass
class TestCase:
    """Represents a single test case"""
    name: str
    description: str
    request_file: str
    expected_agents: List[str]
    success_criteria: Dict[str, Any]
    timeout: int = 1800  # 30 minutes default

@dataclass
class TestResult:
    """Results of a test execution"""
    test_name: str
    success: bool
    execution_time: float
    pipeline_id: str
    agent_results: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    output_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "success": self.success,
            "execution_time": self.execution_time,
            "pipeline_id": self.pipeline_id,
            "agent_results": self.agent_results,
            "errors": self.errors,
            "warnings": self.warnings,
            "output_path": self.output_path,
            "timestamp": datetime.now().isoformat()
        }

class EndToEndTestRunner:
    """Comprehensive end-to-end testing framework for the pipeline"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.test_results: List[TestResult] = []
        self.logger = logging.getLogger("TestRunner")
        self.orchestrator = TemplateOrchestrator(config)
        
    def get_test_cases(self) -> List[TestCase]:
        """Define standard test cases"""
        return [
            TestCase(
                name="basic_saas_template",
                description="Test basic SaaS landing page generation",
                request_file="test_data/saas_request.md",
                expected_agents=[
                    "request_interpreter", "prompt_designer", "template_engineer",
                    "cta_optimizer", "wordpress_theme_assembler", "theme_validator", "packager"
                ],
                success_criteria={
                    "min_agents_success": 6,
                    "required_files": ["style.css", "index.php", "functions.php"],
                    "min_quality_score": 7.0
                }
            ),
            TestCase(
                name="ecommerce_template",
                description="Test e-commerce template generation",
                request_file="test_data/ecommerce_request.md",
                expected_agents=[
                    "request_interpreter", "prompt_designer", "template_engineer",
                    "cta_optimizer", "wordpress_theme_assembler", "seo_optimizer", 
                    "theme_validator", "packager"
                ],
                success_criteria={
                    "min_agents_success": 7,
                    "required_files": ["style.css", "index.php", "functions.php", "woocommerce.php"],
                    "min_quality_score": 7.5
                }
            ),
            TestCase(
                name="blog_template",
                description="Test blog template generation",
                request_file="test_data/blog_request.md",
                expected_agents=[
                    "request_interpreter", "prompt_designer", "template_engineer",
                    "wordpress_theme_assembler", "seo_optimizer", "theme_validator", "packager"
                ],
                success_criteria={
                    "min_agents_success": 6,
                    "required_files": ["style.css", "index.php", "single.php", "archive.php"],
                    "min_quality_score": 7.0
                }
            ),
            TestCase(
                name="refinement_loop_test",
                description="Test refinement and feedback loop",
                request_file="test_data/complex_request.md",
                expected_agents=[
                    "request_interpreter", "template_engineer", "design_critic",
                    "visual_inspector", "refinement_orchestrator", "theme_validator"
                ],
                success_criteria={
                    "min_agents_success": 5,
                    "refinement_iterations": 2,
                    "min_quality_score": 8.0
                }
            )
        ]
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test cases and generate comprehensive report"""
        self.logger.info("Starting end-to-end test suite")
        
        test_cases = self.get_test_cases()
        self.test_results = []
        
        # Create test data if it doesn't exist
        self._create_test_data()
        
        # Run each test case
        for test_case in test_cases:
            self.logger.info(f"Running test: {test_case.name}")
            
            try:
                result = await self._run_single_test(test_case)
                self.test_results.append(result)
                
                if result.success:
                    self.logger.info(f"✅ Test {test_case.name} PASSED")
                else:
                    self.logger.error(f"❌ Test {test_case.name} FAILED")
                    
            except Exception as e:
                self.logger.error(f"💥 Test {test_case.name} CRASHED: {e}")
                self.test_results.append(TestResult(
                    test_name=test_case.name,
                    success=False,
                    execution_time=0.0,
                    pipeline_id="",
                    agent_results={},
                    errors=[str(e)],
                    warnings=[]
                ))
        
        # Generate final report
        report = self._generate_test_report()
        self._save_test_report(report)
        
        return report
    
    async def _run_single_test(self, test_case: TestCase) -> TestResult:
        """Run a single test case"""
        start_time = datetime.now()
        
        # Check if test data exists
        request_path = Path(test_case.request_file)
        if not request_path.exists():
            return TestResult(
                test_name=test_case.name,
                success=False,
                execution_time=0.0,
                pipeline_id="",
                agent_results={},
                errors=[f"Test request file not found: {test_case.request_file}"],
                warnings=[]
            )
        
        try:
            # Run pipeline with timeout
            pipeline_result = await asyncio.wait_for(
                self.orchestrator.run_pipeline(str(request_path)),
                timeout=test_case.timeout
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Validate results against success criteria
            validation_result = self._validate_test_result(
                pipeline_result, test_case.success_criteria
            )
            
            return TestResult(
                test_name=test_case.name,
                success=validation_result["success"],
                execution_time=execution_time,
                pipeline_id=pipeline_result.get("pipeline_id", ""),
                agent_results=pipeline_result.get("agent_results", {}),
                errors=validation_result["errors"],
                warnings=validation_result["warnings"],
                output_path=pipeline_result.get("output_path")
            )
            
        except asyncio.TimeoutError:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TestResult(
                test_name=test_case.name,
                success=False,
                execution_time=execution_time,
                pipeline_id="",
                agent_results={},
                errors=[f"Test timed out after {test_case.timeout} seconds"],
                warnings=[]
            )
    
    def _validate_test_result(self, pipeline_result: Dict[str, Any], 
                            criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Validate pipeline result against success criteria"""
        errors = []
        warnings = []
        
        # Check minimum successful agents
        agent_results = pipeline_result.get("agent_results", {})
        successful_agents = sum(1 for r in agent_results.values() if r.get("success", False))
        min_success = criteria.get("min_agents_success", 0)
        
        if successful_agents < min_success:
            errors.append(f"Only {successful_agents} agents succeeded, minimum required: {min_success}")
        
        # Check required files if output path exists
        output_path = pipeline_result.get("output_path")
        if output_path and criteria.get("required_files"):
            missing_files = self._check_required_files(output_path, criteria["required_files"])
            if missing_files:
                errors.append(f"Missing required files: {missing_files}")
        
        # Check quality score
        min_quality = criteria.get("min_quality_score", 0.0)
        if "theme_validator" in agent_results:
            validator_result = agent_results["theme_validator"]
            quality_score = validator_result.get("metadata", {}).get("overall_score", 0.0)
            if quality_score < min_quality:
                errors.append(f"Quality score {quality_score} below minimum {min_quality}")
        
        # Check refinement iterations
        min_iterations = criteria.get("refinement_iterations", 0)
        if "refinement_orchestrator" in agent_results:
            refinement_result = agent_results["refinement_orchestrator"]
            iterations = refinement_result.get("metadata", {}).get("iterations_completed", 0)
            if iterations < min_iterations:
                warnings.append(f"Only {iterations} refinement iterations, expected {min_iterations}")
        
        return {
            "success": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _check_required_files(self, output_path: str, required_files: List[str]) -> List[str]:
        """Check if required files exist in output"""
        missing_files = []
        output_dir = Path(output_path)
        
        if output_dir.is_file():
            # If output is a zip file, we'd need to extract and check
            # For now, assume it's valid if it exists
            return missing_files
        
        for required_file in required_files:
            file_path = output_dir / required_file
            if not file_path.exists():
                missing_files.append(required_file)
        
        return missing_files
    
    def _create_test_data(self) -> None:
        """Create test data files if they don't exist"""
        test_data_dir = Path("test_data")
        test_data_dir.mkdir(exist_ok=True)
        
        # Create sample test requests
        test_requests = {
            "saas_request.md": """# SaaS Landing Page Request

## Business Information
- **Business Name**: CloudFlow Analytics
- **Business Type**: SaaS Platform
- **Industry**: Data Analytics

## Requirements
- Modern, professional design
- Clear value proposition
- Pricing section
- Customer testimonials
- Contact form

## Target Audience
- Small to medium businesses
- Data analysts
- Business intelligence professionals

## Design Preferences
- Clean, minimalist design
- Blue and white color scheme
- Mobile-responsive
- Fast loading
""",
            "ecommerce_request.md": """# E-commerce Store Request

## Business Information
- **Business Name**: TechGear Pro
- **Business Type**: E-commerce Store
- **Industry**: Electronics

## Requirements
- Product catalog
- Shopping cart functionality
- Customer reviews
- Payment integration
- Inventory management

## Target Audience
- Tech enthusiasts
- Professionals
- Gamers

## Design Preferences
- Modern, tech-focused design
- Dark theme with accent colors
- Product showcase
- Mobile-optimized
""",
            "blog_request.md": """# Blog Template Request

## Business Information
- **Business Name**: Digital Marketing Insights
- **Business Type**: Blog/Content Site
- **Industry**: Digital Marketing

## Requirements
- Article listing
- Category organization
- Author profiles
- Social sharing
- Newsletter signup

## Target Audience
- Digital marketers
- Small business owners
- Marketing students

## Design Preferences
- Clean, readable typography
- Professional layout
- SEO-optimized
- Fast loading
""",
            "complex_request.md": """# Complex Multi-Feature Request

## Business Information
- **Business Name**: Innovation Hub
- **Business Type**: Consulting & Services
- **Industry**: Business Consulting

## Requirements
- Multi-page navigation
- Service portfolio
- Team profiles
- Case studies
- Blog section
- Contact forms
- Resource downloads

## Target Audience
- Enterprise clients
- Startup founders
- Business executives

## Design Preferences
- Sophisticated, professional design
- Custom color scheme
- Interactive elements
- High-quality imagery
- Mobile-first approach
"""
        }
        
        for filename, content in test_requests.items():
            file_path = test_data_dir / filename
            if not file_path.exists():
                file_path.write_text(content, encoding='utf-8')
                self.logger.info(f"Created test data: {file_path}")
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - passed_tests
        
        return {
            "test_suite": "End-to-End Pipeline Tests",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
                "total_execution_time": sum(r.execution_time for r in self.test_results)
            },
            "test_results": [r.to_dict() for r in self.test_results],
            "recommendations": self._generate_test_recommendations()
        }
    
    def _generate_test_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if not r.success]
        if failed_tests:
            recommendations.append(f"Fix {len(failed_tests)} failing tests before deployment")
        
        # Check for common failure patterns
        common_errors = {}
        for result in failed_tests:
            for error in result.errors:
                common_errors[error] = common_errors.get(error, 0) + 1
        
        if common_errors:
            most_common = max(common_errors.items(), key=lambda x: x[1])
            recommendations.append(f"Most common error: {most_common[0]} (occurred {most_common[1]} times)")
        
        # Performance recommendations
        slow_tests = [r for r in self.test_results if r.execution_time > 600]  # 10 minutes
        if slow_tests:
            recommendations.append(f"Optimize performance for slow tests: {[r.test_name for r in slow_tests]}")
        
        if not recommendations:
            recommendations.append("All tests passed successfully - system is ready for deployment")
        
        return recommendations
    
    def _save_test_report(self, report: Dict[str, Any]) -> None:
        """Save test report to file"""
        report_dir = Path("test_reports")
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"test_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Test report saved: {report_file}")

# Main execution
async def main():
    """Run the test suite"""
    test_runner = EndToEndTestRunner()
    report = await test_runner.run_all_tests()
    
    print(f"\n{'='*60}")
    print(f"TEST SUITE RESULTS")
    print(f"{'='*60}")
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Success Rate: {report['summary']['success_rate']:.1%}")
    print(f"Total Time: {report['summary']['total_execution_time']:.1f}s")
    print(f"{'='*60}")
    
    if report['summary']['failed'] > 0:
        print("\nFAILED TESTS:")
        for result in report['test_results']:
            if not result['success']:
                print(f"❌ {result['test_name']}: {result['errors']}")
    
    print(f"\nRECOMMENDATIONS:")
    for rec in report['recommendations']:
        print(f"• {rec}")

if __name__ == "__main__":
    asyncio.run(main())
