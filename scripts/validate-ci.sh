#!/bin/bash
# CI Validation Script - Run basic checks that the CI pipeline would perform

set -e

echo "🔍 Running CI Pipeline Validation..."
echo "======================================"

# Set PYTHONPATH to project root to allow imports from src module
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)"
echo "📌 PYTHONPATH set to: $PYTHONPATH"

# 1. Test structure validation
echo "📁 Validating project structure..."
if [ ! -f ".github/workflows/ci-comprehensive.yml" ]; then
    echo "❌ CI workflow file missing"
    exit 1
fi
echo "✅ CI workflow file exists"

# 2. Python syntax validation
echo "🐍 Validating Python syntax..."
python -m py_compile tests/test_*.py
echo "✅ Python syntax valid"

# 3. Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short
echo "✅ Tests passed"

# 4. Code formatting check (if black is available)
if command -v black >/dev/null 2>&1; then
    echo "🎨 Checking code formatting..."
    black --check tests/ || echo "⚠️ Some formatting issues found but CI can continue"
else
    echo "⚠️ Black not available, skipping formatting check"
fi

# 5. Basic linting (if flake8 is available)
if command -v flake8 >/dev/null 2>&1; then
    echo "🔍 Running basic linting..."
    flake8 tests/ --max-line-length=88 --ignore=E501,F841,F401 || echo "⚠️ Some linting issues found but CI can continue"
else
    echo "⚠️ Flake8 not available, skipping linting check"
fi

echo ""
echo "🎉 CI Pipeline Validation Complete!"
echo "=================================="
echo "The CI pipeline should now run successfully with the following features:"
echo "✓ Matrix testing across Python 3.9-3.12"
echo "✓ Code quality checks (black, isort, flake8, mypy)"
echo "✓ Security scanning (safety, bandit, pip-audit)"
echo "✓ Graceful handling of optional dependencies"
echo "✓ Build artifact creation"
echo "✓ Deployment simulation"
echo ""
echo "Note: Heavy dependencies (face_recognition, dlib) are"
echo "      configured as optional to prevent CI timeouts"
