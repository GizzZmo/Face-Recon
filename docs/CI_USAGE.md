# CI Pipeline Usage Guide

This document explains how to use and maintain the Face-Recon CI/CD pipeline.

## Overview

The CI pipeline is designed to be robust and efficient, with graceful handling of heavy dependencies that can cause timeouts in cloud environments.

## Pipeline Structure

### Workflows
- **Primary**: `.github/workflows/ci-comprehensive.yml` - Main CI/CD pipeline
- **Legacy**: `.github/workflows/ci.yml` - Deprecated, kept for reference

### Key Features
- **Matrix Testing**: Python 3.8-3.12 across multiple OS (Ubuntu, Windows, macOS)
- **Code Quality**: Black, isort, flake8, mypy, safety, bandit
- **Testing**: Pytest with coverage reporting
- **Building**: Source distribution creation
- **Security**: Dependency and code security scanning
- **Deployment**: Automated deployment simulation

## Dependency Strategy

### Core Dependencies (Always Installed)
- `numpy` - Essential for numerical operations
- `Flask` - Required for web functionality
- `pytest` family - Testing framework

### Optional Dependencies (Skipped in CI)
- `opencv-python` - Heavy computer vision library
- `face_recognition` - Depends on dlib (very heavy compilation)
- `dlib` - C++ compilation required (causes timeouts)

### Files
- `requirements.txt` - Full production dependencies
- `requirements-ci.txt` - Lightweight CI dependencies

## Running Locally

### Full Installation
```bash
pip install -r requirements.txt
```

### CI-style Installation
```bash
pip install -r requirements-ci.txt
```

### Validate CI Pipeline
```bash
./scripts/validate-ci.sh
```

## CI Behavior

### What Passes
- Core Python functionality
- Essential dependency imports (numpy, Flask)
- Code formatting and linting
- Security scans
- Build artifact creation

### What's Gracefully Handled
- Missing OpenCV (skipped tests, warnings)
- Missing face_recognition (skipped tests, warnings)
- Network timeouts during dependency installation
- Platform-specific dependency issues

## Customizing the Pipeline

### Adding New Dependencies
1. Add to `requirements.txt` for production
2. If lightweight, add to CI workflow directly
3. If heavy, add graceful fallback in tests

### Example Test Pattern
```python
def test_optional_dependency():
    try:
        import heavy_library
        # Test functionality
        assert heavy_library.version
    except ImportError:
        pytest.skip("Heavy library not available - expected in CI")
```

### Modifying CI Steps
The CI workflow is modular:
1. **Code Quality** - Linting and formatting
2. **Testing** - Multi-platform test execution  
3. **Building** - Package creation
4. **Security** - Vulnerability scanning
5. **Deployment** - Production deployment simulation

## Troubleshooting

### Common Issues

#### "Module not found" errors
- Expected for heavy dependencies in CI
- Tests should use graceful fallbacks
- Check test output for warnings vs failures

#### Timeout during pip install
- Heavy dependencies causing issues
- Use `|| echo "..."` for non-critical installs
- Consider using `--timeout` flag

#### Formatting failures
```bash
black .
isort .
```

#### Linting failures
```bash
flake8 . --max-line-length=88
```

### CI Debug Tips
1. Check GitHub Actions logs for specific failure points
2. Run validation script locally: `./scripts/validate-ci.sh`
3. Test with minimal dependencies first
4. Use matrix strategy to isolate platform issues

## Performance Optimizations

### Caching
- Pip dependencies cached by Python version
- Cache keys include requirements.txt hash
- Separate caches for different OS

### Parallel Execution
- Matrix jobs run in parallel
- Independent job failure doesn't stop others
- Fail-fast disabled for comprehensive testing

### Resource Efficiency
- Lightweight dependencies in CI
- Heavy compilation avoided
- Timeout protection on installs

## Monitoring

### Success Metrics
- All jobs complete without critical failures
- Tests pass with acceptable skip rate
- Build artifacts generated successfully
- Security scans complete

### Expected Warnings
- "OpenCV not available" - Normal in CI
- "Some dependencies not available" - Expected
- Minor linting issues - Acceptable

### Failure Indicators
- Core import failures (config, numpy, Flask)
- Test failures (not skips)
- Security vulnerabilities found
- Build artifact creation fails

## Contributing

When adding new features:
1. Ensure tests handle missing dependencies gracefully
2. Update both requirements files appropriately
3. Test locally with validation script
4. Consider CI performance impact

## Support

For CI pipeline issues:
1. Run `./scripts/validate-ci.sh` locally
2. Check GitHub Actions logs
3. Review this documentation
4. Create issue with specific error details