#!/bin/bash
# Simple release script for Face-Recon Security System

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $*"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $*"
}

# Check if version is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.1.0"
    exit 1
fi

VERSION="$1"

# Validate version format
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "Invalid version format: $VERSION"
    log_error "Expected format: X.Y.Z (e.g., 1.1.0)"
    exit 1
fi

log "🚀 Creating release $VERSION for Face-Recon Security System"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    log_error "pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    log_warning "You have uncommitted changes. Please commit or stash them first."
    git status --short
    exit 1
fi

# Update version using the version script
log "📝 Updating version to $VERSION"
python scripts/version.py update "$VERSION"

# Run basic tests
log "🧪 Running basic validation tests"
python -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

try:
    import config
    print('✅ Config module imported successfully')
except Exception as e:
    print(f'❌ Config import failed: {e}')
    sys.exit(1)

print('✅ Basic validation passed')
"

# Check if CHANGELOG.md exists and is updated
if [ -f "CHANGELOG.md" ]; then
    if grep -q "## \[$VERSION\]" CHANGELOG.md; then
        log_success "CHANGELOG.md contains entry for version $VERSION"
    else
        log_warning "CHANGELOG.md doesn't contain entry for version $VERSION"
        log_warning "Please update CHANGELOG.md before releasing"
    fi
else
    log_warning "CHANGELOG.md not found"
fi

# Commit version change
log "📝 Committing version change"
git add pyproject.toml
git commit -m "Bump version to $VERSION"

# Create tag
log "🏷️ Creating git tag v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"

# Instructions for pushing
log_success "Release $VERSION prepared successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Review the changes: git log --oneline -5"
echo "   2. Push the changes: git push origin $(git branch --show-current)"
echo "   3. Push the tag: git push origin v$VERSION"
echo "   4. The GitHub Actions workflow will automatically create the release"
echo ""
echo "🔗 After pushing the tag, check the release at:"
echo "   https://github.com/GizzZmo/Face-Recon/releases/tag/v$VERSION"
echo ""
echo "💡 To manually trigger the release workflow:"
echo "   Go to: https://github.com/GizzZmo/Face-Recon/actions/workflows/release.yml"
echo "   Click 'Run workflow' and specify version v$VERSION"