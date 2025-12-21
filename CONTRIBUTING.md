# Contributing to Face-Recon

Thank you for your interest in contributing to Face-Recon! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

Be respectful and constructive in all interactions. We're building an inclusive community focused on improving security technology for everyone.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Face-Recon.git
   cd Face-Recon
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/GizzZmo/Face-Recon.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher (3.10 or 3.11 recommended)
- Git for version control
- Virtual environment tool (venv or conda)

### Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-ci.txt
   ```

3. **Verify installation**:
   ```bash
   python -m pytest tests/
   ```

## Coding Standards

We maintain high code quality standards. Please follow these guidelines:

### Python Style Guide

- **PEP 8**: Follow Python's official style guide
- **Line Length**: Maximum 88 characters (Black default)
- **Imports**: Group imports (stdlib, third-party, local)
- **Type Hints**: Add type hints to all function signatures
- **Docstrings**: Use Google-style docstrings for all public functions

### Code Quality Tools

Before submitting, run these tools:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check for style issues
flake8 .

# Run type checker
mypy src/

# Run tests
pytest tests/ -v
```

### Example Function

```python
"""Module for user authentication."""

from typing import Optional


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with username and password.

    Args:
        username: User's username
        password: User's password

    Returns:
        User data dictionary if authenticated, None otherwise

    Example:
        >>> user = authenticate_user("john_doe", "secret123")
        >>> if user:
        ...     print(f"Welcome {user['name']}")
    """
    # Implementation here
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Include docstrings for complex tests

Example:

```python
def test_face_encoding_extraction():
    """Test that face encodings are correctly extracted from images."""
    # Arrange
    test_image = "data/test_faces/john_doe.jpg"
    
    # Act
    encodings = extract_face_encodings(test_image)
    
    # Assert
    assert len(encodings) > 0
    assert len(encodings[0]) == 128  # Face encoding dimension
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Run all quality checks**:
   ```bash
   black .
   isort .
   flake8 .
   pytest tests/
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: brief description
   
   - Detailed point 1
   - Detailed point 2
   - Fixes #issue_number"
   ```

5. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Submitting the PR

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to any related issues
   - Screenshots for UI changes
   - Test results

3. **Respond to feedback** promptly and make requested changes

### PR Requirements

- ✅ All tests must pass
- ✅ Code coverage should not decrease
- ✅ No linting errors
- ✅ Documentation updated if needed
- ✅ CHANGELOG.md updated for significant changes

## Reporting Issues

### Bug Reports

Include:

- **Clear title** summarizing the issue
- **Description** of the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment** (OS, Python version, package versions)
- **Error messages** and stack traces
- **Screenshots** if applicable

### Feature Requests

Include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: What other approaches were considered?
- **Additional context**: Any relevant information

## Development Workflow

### Typical Workflow

1. Check [Issues](https://github.com/GizzZmo/Face-Recon/issues) for tasks
2. Comment on issue to indicate you're working on it
3. Create feature branch from `main`
4. Make changes following coding standards
5. Write/update tests
6. Run quality checks locally
7. Commit changes with clear messages
8. Push to your fork
9. Open Pull Request
10. Address review feedback
11. Celebrate when merged! 🎉

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates

Examples:
- `feature/voice-authentication`
- `fix/database-connection-leak`
- `docs/api-endpoints`
- `refactor/error-handling`

## Questions?

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the [README](README.md) and [docs/](docs/) folder

## Recognition

Contributors are recognized in:
- Git commit history
- Pull request acknowledgments
- Project documentation

Thank you for contributing to Face-Recon! 🚀
