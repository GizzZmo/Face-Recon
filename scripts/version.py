#!/usr/bin/env python3
"""
Version management script for Face-Recon Security System
"""

import os
import re
import sys
import subprocess
from datetime import datetime


def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = "pyproject.toml"
    if not os.path.exists(pyproject_path):
        raise FileNotFoundError("pyproject.toml not found")
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
    
    raise ValueError("Version not found in pyproject.toml")


def update_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = "pyproject.toml"
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    # Update version
    new_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    with open(pyproject_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated version to {new_version} in pyproject.toml")


def validate_version(version):
    """Validate semantic version format"""
    pattern = r'^(\d+)\.(\d+)\.(\d+)$'
    if not re.match(pattern, version):
        raise ValueError(f"Invalid version format: {version}. Expected X.Y.Z")
    return True


def create_tag(version):
    """Create git tag for the version"""
    tag_name = f"v{version}"
    
    # Check if tag already exists
    try:
        result = subprocess.run(
            ["git", "tag", "-l", tag_name],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            print(f"❌ Tag {tag_name} already exists")
            return False
    except subprocess.CalledProcessError:
        print("⚠️ Could not check existing tags")
    
    # Create tag
    try:
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"],
            check=True
        )
        print(f"✅ Created tag {tag_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create tag: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/version.py current          - Show current version")
        print("  python scripts/version.py update X.Y.Z     - Update to specific version")
        print("  python scripts/version.py tag              - Create git tag for current version")
        print("  python scripts/version.py release X.Y.Z    - Update version and create tag")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "current":
            version = get_current_version()
            print(f"Current version: {version}")
        
        elif command == "update":
            if len(sys.argv) < 3:
                print("❌ Please specify version: python scripts/version.py update X.Y.Z")
                sys.exit(1)
            
            new_version = sys.argv[2]
            validate_version(new_version)
            update_version(new_version)
        
        elif command == "tag":
            version = get_current_version()
            if create_tag(version):
                print(f"✅ Use 'git push origin v{version}' to push the tag")
        
        elif command == "release":
            if len(sys.argv) < 3:
                print("❌ Please specify version: python scripts/version.py release X.Y.Z")
                sys.exit(1)
            
            new_version = sys.argv[2]
            validate_version(new_version)
            
            print(f"🚀 Creating release {new_version}")
            update_version(new_version)
            
            if create_tag(new_version):
                print(f"✅ Release {new_version} ready!")
                print(f"📋 Next steps:")
                print(f"   1. git add pyproject.toml")
                print(f"   2. git commit -m 'Bump version to {new_version}'")
                print(f"   3. git push origin v{new_version}")
                print(f"   4. The release workflow will automatically create the GitHub release")
        
        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()