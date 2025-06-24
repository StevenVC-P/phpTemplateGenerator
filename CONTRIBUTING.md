# Contributing to PHP Template Generator

Thank you for your interest in contributing to the PHP Template Generator! This document provides guidelines and information for contributors.

## 🎯 Project Vision

We're building an advanced multi-agent system that generates high-quality, unique PHP templates with real feedback loops and iterative improvement. Our goal is to demonstrate the power of AI agent orchestration while creating practical, production-ready templates.

## 🚀 Quick Start for Contributors

### 1. Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/AITemplateDevelopment.git
cd AITemplateDevelopment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
python test_organized_templates.py
```

### 2. Understanding the Architecture

#### Core Components
- **🤖 Agents**: Specialized AI components in `agents/` directory
- **🎭 Orchestrator**: Pipeline management in `mcp/orchestrator.py`
- **🛠️ Utils**: Helper functions in `utils/` directory
- **🗂️ Template Generations**: Organized outputs in `template_generations/`

#### Key Features to Understand
- **Design Variation Engine**: Creates unique designs every time
- **Feedback Loop**: Agents provide real feedback and templates improve automatically
- **Organized Conversations**: Each template generation has its own isolated folder
- **Real Agent Analysis**: Comprehensive code and design reviews with actionable insights

## 🤝 How to Contribute

### 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear Description**: What happened vs. what you expected
2. **Reproduction Steps**: Detailed steps to reproduce the issue
3. **Environment Info**: Python version, OS, dependencies
4. **Error Messages**: Full error logs and stack traces
5. **Template Context**: Which template generation or agent was involved

**Template for Bug Reports:**
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Run `python test_organized_templates.py`
2. Navigate to generated template
3. Observe issue

## Expected Behavior
What should have happened

## Actual Behavior
What actually happened

## Environment
- Python version: 3.x.x
- OS: Windows/macOS/Linux
- Template generation: template_YYYYMMDD_HHMMSS

## Error Logs
```
Paste error messages here
```
```

### ✨ Feature Requests

We welcome feature suggestions! Please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered
4. **Impact**: Who would benefit from this feature?

### 🔧 Code Contributions

#### Types of Contributions Welcome

1. **🤖 New Agents**: Specialized agents for specific tasks
2. **🎨 Design Enhancements**: Improved variation algorithms
3. **🔄 Feedback Improvements**: Better agent analysis and suggestions
4. **🧪 Testing**: Additional test coverage and scenarios
5. **📚 Documentation**: Guides, examples, and API documentation
6. **🐛 Bug Fixes**: Issue resolution and stability improvements

#### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow existing code patterns
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run existing tests
   python test_organized_templates.py
   python test_feedback_loop.py
   python test_design_variations.py
   
   # Test your specific changes
   python your_test_file.py
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new agent for X functionality"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Include test results

## 🤖 Adding New Agents

### Agent Structure

All agents should follow this pattern:

```python
# agents/your_agent.py
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class YourAgent:
    """Agent description and purpose"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agent_id = "your_agent"
    
    def process(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Main processing method"""
        try:
            # Load input
            with open(input_file, 'r') as f:
                input_data = json.load(f)
            
            # Process data
            result = self.your_processing_logic(input_data)
            
            # Save output
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            return {
                "success": True,
                "message": "Processing completed successfully",
                "output_file": output_file
            }
            
        except Exception as e:
            logger.error(f"Agent processing failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def your_processing_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement your agent's core logic here"""
        # Your implementation
        return processed_data
```

### Agent Configuration

Create a configuration file in `agents/your_agent.json`:

```json
{
  "agent_id": "your_agent",
  "name": "Your Agent Name",
  "version": "1.0",
  "description": "What your agent does",
  "capabilities": [
    "capability_1",
    "capability_2"
  ],
  "input_format": "json",
  "output_format": "json",
  "dependencies": [],
  "quality_thresholds": {
    "accuracy": 8.0,
    "completeness": 9.0
  }
}
```

### Integration with Orchestrator

Add your agent to the pipeline in `mcp/orchestrator.py`:

1. Import your agent
2. Add to agent execution sequence
3. Configure input/output handling
4. Add to organized folder structure

## 🎨 Design Variation Contributions

### Adding New Design Elements

Contribute to `utils/design_variation_engine.py`:

1. **Color Palettes**: Industry-specific color schemes
2. **Typography**: Font combinations and hierarchies
3. **Layouts**: New layout patterns and structures
4. **Components**: Reusable design components

### Example Contribution

```python
# Add to design_variation_engine.py
INDUSTRY_PALETTES = {
    "your_industry": {
        "primary": "#your_color",
        "secondary": "#your_color",
        "accent": "#your_color",
        "background": "#your_color",
        "text": "#your_color"
    }
}

TYPOGRAPHY_COMBINATIONS = {
    "your_combination": {
        "heading": "Your Heading Font",
        "body": "Your Body Font",
        "accent": "Your Accent Font"
    }
}
```

## 🧪 Testing Guidelines

### Test Categories

1. **Unit Tests**: Individual agent functionality
2. **Integration Tests**: Agent pipeline interactions
3. **End-to-End Tests**: Complete template generation
4. **Visual Tests**: Template appearance and quality

### Writing Tests

```python
# tests/test_your_feature.py
import unittest
from your_module import YourClass

class TestYourFeature(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = {...}
    
    def test_your_functionality(self):
        """Test specific functionality"""
        result = YourClass().your_method(self.test_data)
        self.assertTrue(result['success'])
        self.assertIn('expected_key', result)
    
    def tearDown(self):
        """Clean up after tests"""
        # Cleanup code
```

## 📚 Documentation Standards

### Code Documentation

- **Docstrings**: All classes and methods should have clear docstrings
- **Type Hints**: Use type hints for better code clarity
- **Comments**: Explain complex logic and business rules
- **Examples**: Include usage examples in docstrings

### README Updates

When adding features, update:
- Feature list in README.md
- Quick start instructions
- Project structure documentation
- Roadmap status

## 🔍 Code Review Process

### What We Look For

1. **Code Quality**: Clean, readable, maintainable code
2. **Testing**: Adequate test coverage for new features
3. **Documentation**: Clear documentation and examples
4. **Performance**: Efficient algorithms and resource usage
5. **Security**: Secure coding practices
6. **Compatibility**: Works with existing system

### Review Criteria

- ✅ Follows existing code patterns
- ✅ Includes appropriate tests
- ✅ Updates documentation
- ✅ Handles errors gracefully
- ✅ Maintains backward compatibility
- ✅ Improves overall system quality

## 🎉 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- CHANGELOG.md feature credits
- GitHub contributor graphs
- Project documentation

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Code Review**: For implementation guidance

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing to the PHP Template Generator! Together, we're building the future of AI-powered template generation.** 🚀
