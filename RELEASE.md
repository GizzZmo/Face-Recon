# Release Guide

This document explains how to create releases for the Face-Recon Security System.

## Quick Release

Use the automated release script:

```bash
# Make sure you're on main branch with clean working directory
git checkout main
git pull origin main

# Create and prepare release (replace 1.2.0 with desired version)
./scripts/release.sh 1.2.0

# Push changes and tag
git push origin main
git push origin v1.2.0
```

The GitHub Actions workflow will automatically create the release with:
- Comprehensive release notes
- Source code artifacts
- Documentation packages
- Changelog integration

## Manual Release Process

### 1. Prepare Release

```bash
# Update version in pyproject.toml
python scripts/version.py update 1.2.0

# Update CHANGELOG.md with new version section
# Add your changes under ## [1.2.0] - YYYY-MM-DD

# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 1.2.0"
```

### 2. Create Release

**Option A: Automatic (Recommended)**
```bash
# Create and push tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

**Option B: Manual Trigger**
1. Go to [GitHub Actions](https://github.com/GizzZmo/Face-Recon/actions/workflows/release.yml)
2. Click "Run workflow"
3. Enter version (e.g., v1.2.0)
4. Set prerelease flag if needed
5. Click "Run workflow"

### 3. Verify Release

Check the [releases page](https://github.com/GizzZmo/Face-Recon/releases) to ensure:
- Release notes are complete
- Artifacts are uploaded
- Version links work correctly

## Version Management

### Version Script Usage

```bash
# Check current version
python scripts/version.py current

# Update version
python scripts/version.py update 1.2.0

# Create tag for current version
python scripts/version.py tag

# Full release process
python scripts/version.py release 1.2.0
```

### Version Format

Follow [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (X.Y.0): New features, backwards compatible  
- **Patch** (X.Y.Z): Bug fixes, backwards compatible

## Release Workflow Features

The automated release workflow includes:

### 🚀 **Automated Release Creation**
- Validates version format
- Extracts changelog for the version
- Creates comprehensive release notes
- Generates source and documentation artifacts
- Uploads artifacts to GitHub release

### 📝 **Release Notes Generation**
- Project overview and key features
- Technical excellence highlights
- Multi-platform support details
- Quick start instructions
- System requirements
- Links and resources
- Support information

### 📦 **Artifacts**
- **Source Package**: Complete source code with dependencies
- **Documentation Package**: All documentation files
- **Checksums**: Integrity verification for all artifacts

### 🔐 **Security**
- Version validation
- Tag verification
- Artifact integrity checks
- Secure artifact upload

## Changelog Management

### Format
Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.2.0] - 2025-MM-DD

### Added
- New feature descriptions

### Changed
- Modified feature descriptions

### Fixed
- Bug fix descriptions

### Security
- Security fix descriptions
```

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

## Troubleshooting

### Common Issues

**Tag already exists**
```bash
# Delete local tag
git tag -d v1.2.0

# Delete remote tag (if needed)
git push origin :refs/tags/v1.2.0

# Create new tag
git tag -a v1.2.0 -m "Release v1.2.0"
```

**Workflow fails**
1. Check [Actions tab](https://github.com/GizzZmo/Face-Recon/actions) for error details
2. Verify all required files exist
3. Ensure version format is correct (vX.Y.Z)
4. Check CHANGELOG.md format

**Missing artifacts**
- Ensure workflow completed successfully
- Check if source files exist in repository
- Verify artifact upload permissions

### Getting Help

- 📖 [GitHub Actions Documentation](https://docs.github.com/en/actions)
- 🐛 [Report Issues](https://github.com/GizzZmo/Face-Recon/issues)
- 💡 [Discussions](https://github.com/GizzZmo/Face-Recon/discussions)

## Best Practices

1. **Test Before Release**: Run tests locally before creating release
2. **Update Documentation**: Ensure README and docs are current
3. **Review Changes**: Double-check changelog for accuracy
4. **Semantic Versioning**: Follow version numbering conventions
5. **Clean History**: Squash commits if needed before release
6. **Verify Links**: Check that all documentation links work

---

For questions about the release process, create an issue or discussion on GitHub.