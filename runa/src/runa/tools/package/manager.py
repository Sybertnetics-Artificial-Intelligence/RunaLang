#!/usr/bin/env python3
"""
Runa Package Manager

Multi-language package management system supporting all language tiers.
Handles package installation, dependency resolution, and registry operations.
"""

import os
import sys
import json
import hashlib
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error
import toml
import semver
import argparse

from ..cli import RunaCLI
from ...core.config import get_config


@dataclass
class PackageVersion:
    """Represents a package version with semantic versioning."""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None
    
    @classmethod
    def from_string(cls, version_str: str) -> 'PackageVersion':
        """Parse version string into PackageVersion."""
        try:
            parsed = semver.VersionInfo.parse(version_str)
            return cls(
                major=parsed.major,
                minor=parsed.minor, 
                patch=parsed.patch,
                prerelease=parsed.prerelease,
                build=parsed.build
            )
        except ValueError as e:
            raise ValueError(f"Invalid version string '{version_str}': {e}")
    
    def __str__(self) -> str:
        """Convert to standard semver string."""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version
    
    def satisfies(self, constraint: str) -> bool:
        """Check if this version satisfies a constraint."""
        return semver.match(str(self), constraint)


@dataclass
class PackageDependency:
    """Represents a package dependency with version constraints."""
    name: str
    version_constraint: str
    registry: Optional[str] = None
    language: Optional[str] = None  # For cross-language dependencies
    optional: bool = False
    type: str = "runtime"  # runtime, development, build, test
    
    def __post_init__(self):
        """Validate dependency configuration."""
        if self.type not in ["runtime", "development", "build", "test"]:
            raise ValueError(f"Invalid dependency type: {self.type}")


@dataclass
class LanguageTarget:
    """Represents a language compilation target."""
    language: str
    tier: int
    version: Optional[str] = None
    features: List[str] = field(default_factory=list)
    build_options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PackageMetadata:
    """Complete package metadata supporting multi-language packages."""
    name: str
    version: PackageVersion
    description: str
    author: str
    email: str
    license: str
    homepage: Optional[str] = None
    repository: Optional[str] = None
    
    # Multi-language support
    primary_language: str = "runa"
    supported_languages: List[str] = field(default_factory=lambda: ["runa"])
    language_targets: Dict[str, LanguageTarget] = field(default_factory=dict)
    
    # Package structure
    entry_point: Optional[str] = None
    include_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)
    
    # Dependencies
    dependencies: Dict[str, PackageDependency] = field(default_factory=dict)
    
    # Build and deployment
    build_scripts: List[str] = field(default_factory=list)
    test_command: Optional[str] = None
    
    # Registry metadata
    keywords: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    minimum_runa_version: Optional[str] = None
    
    # Publishing metadata
    published_at: Optional[datetime] = None
    checksum: Optional[str] = None
    size_bytes: Optional[int] = None
    
    @classmethod
    def from_toml(cls, toml_path: str) -> 'PackageMetadata':
        """Load package metadata from runa.toml file."""
        with open(toml_path, 'r', encoding='utf-8') as f:
            data = toml.load(f)
        
        package_data = data.get('package', {})
        
        # Parse version
        version = PackageVersion.from_string(package_data.get('version', '0.1.0'))
        
        # Parse dependencies
        dependencies = {}
        deps_data = data.get('dependencies', {})
        for name, dep_config in deps_data.items():
            if isinstance(dep_config, str):
                dependencies[name] = PackageDependency(name=name, version_constraint=dep_config)
            elif isinstance(dep_config, dict):
                dependencies[name] = PackageDependency(
                    name=name,
                    version_constraint=dep_config.get('version', '*'),
                    registry=dep_config.get('registry'),
                    language=dep_config.get('language'),
                    optional=dep_config.get('optional', False),
                    type=dep_config.get('type', 'runtime')
                )
        
        # Parse language targets
        language_targets = {}
        targets_data = data.get('targets', {})
        for lang, target_config in targets_data.items():
            if isinstance(target_config, dict):
                language_targets[lang] = LanguageTarget(
                    language=lang,
                    tier=target_config.get('tier', 1),
                    version=target_config.get('version'),
                    features=target_config.get('features', []),
                    build_options=target_config.get('build_options', {})
                )
        
        return cls(
            name=package_data.get('name', ''),
            version=version,
            description=package_data.get('description', ''),
            author=package_data.get('author', ''),
            email=package_data.get('email', ''),
            license=package_data.get('license', 'MIT'),
            homepage=package_data.get('homepage'),
            repository=package_data.get('repository'),
            primary_language=package_data.get('primary_language', 'runa'),
            supported_languages=package_data.get('supported_languages', ['runa']),
            language_targets=language_targets,
            entry_point=data.get('build', {}).get('entry-point'),
            include_patterns=data.get('build', {}).get('include', []),
            exclude_patterns=data.get('build', {}).get('exclude', []),
            dependencies=dependencies,
            build_scripts=data.get('build', {}).get('build-scripts', []),
            test_command=data.get('build', {}).get('test-command'),
            keywords=package_data.get('keywords', []),
            categories=package_data.get('categories', []),
            minimum_runa_version=data.get('metadata', {}).get('minimum-runa-version')
        )


class PackageRegistry:
    """Multi-language package registry client."""
    
    def __init__(self, registry_url: str = "https://packages.runa-lang.org", 
                 auth_token: Optional[str] = None):
        self.registry_url = registry_url.rstrip('/')
        self.auth_token = auth_token or os.getenv('RUNA_REGISTRY_TOKEN')
        
        # Language tier configuration
        self.language_tiers = {
            1: ["javascript", "typescript", "python", "cpp", "java", "csharp", "sql"],
            2: ["rust", "go", "swift", "kotlin", "php", "webassembly"],
            3: ["html", "css", "shell", "hcl", "yaml", "json", "xml"],
            4: ["r", "matlab", "julia", "solidity", "graphql"],
            5: ["lisp", "haskell", "erlang", "elixir", "llvm_ir", "assembly"],
            6: ["objective_c", "visual_basic", "cobol", "ada", "perl", "fortran"]
        }
        
        # Reverse mapping for quick tier lookup
        self.language_to_tier = {}
        for tier, languages in self.language_tiers.items():
            for lang in languages:
                self.language_to_tier[lang] = tier
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to registry API."""
        url = f"{self.registry_url}{endpoint}"
        
        headers = {
            'User-Agent': 'runa-package-manager/0.3.0',
            'Accept': 'application/json'
        }
        
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        if method == 'GET':
            try:
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    return json.loads(response.read().decode())
            except urllib.error.HTTPError as e:
                error_data = json.loads(e.read().decode()) if e.code >= 400 else {}
                raise PackageRegistryError(f"Registry request failed: {e.code} {e.reason}", error_data)
        
        elif method == 'POST':
            if files:
                # For file uploads, we'd use a proper multipart library in production
                raise NotImplementedError("File upload not implemented in basic urllib version")
            
            json_data = json.dumps(data).encode() if data else b''
            headers['Content-Type'] = 'application/json'
            
            try:
                request = urllib.request.Request(url, data=json_data, headers=headers, method='POST')
                with urllib.request.urlopen(request) as response:
                    return json.loads(response.read().decode())
            except urllib.error.HTTPError as e:
                error_data = json.loads(e.read().decode()) if e.code >= 400 else {}
                raise PackageRegistryError(f"Registry request failed: {e.code} {e.reason}", error_data)
        
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    
    def search_packages(self, query: str, language: Optional[str] = None, 
                       category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search for packages in the registry."""
        params = {'q': query, 'limit': limit}
        if language:
            params['language'] = language
        if category:
            params['category'] = category
        
        query_string = urllib.parse.urlencode(params)
        endpoint = f"/api/v1/packages/search?{query_string}"
        
        response = self._make_request('GET', endpoint)
        return response.get('packages', [])
    
    def get_package_info(self, package_name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed package information."""
        endpoint = f"/api/v1/packages/{package_name}"
        if version:
            endpoint += f"/{version}"
        
        return self._make_request('GET', endpoint)
    
    def get_package_versions(self, package_name: str) -> List[str]:
        """Get all available versions of a package."""
        endpoint = f"/api/v1/packages/{package_name}/versions"
        response = self._make_request('GET', endpoint)
        return response.get('versions', [])
    
    def publish_package(self, package_path: str, metadata: PackageMetadata) -> Dict[str, Any]:
        """Publish a package to the registry."""
        if not self.auth_token:
            raise PackageRegistryError("Authentication token required for publishing")
        
        # Create package archive
        archive_path = self._create_package_archive(package_path, metadata)
        
        try:
            # Calculate checksum
            with open(archive_path, 'rb') as f:
                content = f.read()
                checksum = hashlib.sha256(content).hexdigest()
                size_bytes = len(content)
            
            # Prepare metadata for upload
            upload_metadata = {
                'name': metadata.name,
                'version': str(metadata.version),
                'description': metadata.description,
                'author': metadata.author,
                'email': metadata.email,
                'license': metadata.license,
                'homepage': metadata.homepage,
                'repository': metadata.repository,
                'primary_language': metadata.primary_language,
                'supported_languages': metadata.supported_languages,
                'language_targets': {
                    lang: {
                        'language': target.language,
                        'tier': target.tier,
                        'version': target.version,
                        'features': target.features,
                        'build_options': target.build_options
                    }
                    for lang, target in metadata.language_targets.items()
                },
                'dependencies': {
                    name: {
                        'version_constraint': dep.version_constraint,
                        'registry': dep.registry,
                        'language': dep.language,
                        'optional': dep.optional,
                        'type': dep.type
                    }
                    for name, dep in metadata.dependencies.items()
                },
                'keywords': metadata.keywords,
                'categories': metadata.categories,
                'minimum_runa_version': metadata.minimum_runa_version,
                'checksum': checksum,
                'size_bytes': size_bytes
            }
            
            # In a real implementation, we'd upload the archive file
            # For now, we'll just send the metadata
            endpoint = "/api/v1/packages/publish"
            return self._make_request('POST', endpoint, upload_metadata)
            
        finally:
            # Clean up temporary archive
            if os.path.exists(archive_path):
                os.unlink(archive_path)
    
    def download_package(self, package_name: str, version: str, target_dir: str) -> str:
        """Download and extract a package."""
        endpoint = f"/api/v1/packages/{package_name}/{version}/download"
        
        # In a real implementation, this would download the actual package archive
        # For now, we'll simulate the process
        package_dir = os.path.join(target_dir, f"{package_name}-{version}")
        os.makedirs(package_dir, exist_ok=True)
        
        # Create a placeholder package structure
        with open(os.path.join(package_dir, 'runa.toml'), 'w') as f:
            f.write(f"""[package]
name = "{package_name}"
version = "{version}"
description = "Downloaded package"
author = "Unknown"
email = "unknown@example.com"
license = "MIT"
""")
        
        return package_dir
    
    def _create_package_archive(self, package_path: str, metadata: PackageMetadata) -> str:
        """Create a package archive for upload."""
        # In a real implementation, this would create a proper archive (tar.gz or zip)
        # For now, we'll create a temporary file with metadata
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        
        archive_metadata = {
            'name': metadata.name,
            'version': str(metadata.version),
            'files': self._get_package_files(package_path, metadata)
        }
        
        json.dump(archive_metadata, temp_file, indent=2)
        temp_file.close()
        
        return temp_file.name
    
    def _get_package_files(self, package_path: str, metadata: PackageMetadata) -> List[str]:
        """Get list of files to include in package."""
        files = []
        package_dir = Path(package_path)
        
        # Include patterns (default to all .runa files)
        include_patterns = metadata.include_patterns or ["**/*.runa", "runa.toml", "README.md", "LICENSE"]
        
        for pattern in include_patterns:
            for file_path in package_dir.glob(pattern):
                if file_path.is_file():
                    rel_path = file_path.relative_to(package_dir)
                    files.append(str(rel_path))
        
        # Apply exclude patterns
        if metadata.exclude_patterns:
            excluded = set()
            for pattern in metadata.exclude_patterns:
                for file_path in package_dir.glob(pattern):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(package_dir)
                        excluded.add(str(rel_path))
            
            files = [f for f in files if f not in excluded]
        
        return sorted(files)


class PackageRegistryError(Exception):
    """Exception raised for package registry operations."""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.details = details or {}


class PackageManager:
    """High-level package manager for multi-language Runa packages."""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root or os.getcwd())
        self.config = get_config()
        
        # Package cache directory
        self.cache_dir = Path.home() / '.runa' / 'packages'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Registry configuration
        default_registry = self.config.get('registry', {}).get('default', 'https://packages.runa-lang.org')
        auth_token = self.config.get('registry', {}).get('token')
        self.registry = PackageRegistry(default_registry, auth_token)
        
        # Installed packages tracking
        self.installed_packages: Dict[str, PackageMetadata] = {}
        self._load_installed_packages()
    
    def _load_installed_packages(self):
        """Load information about installed packages."""
        packages_dir = self.project_root / 'packages'
        if not packages_dir.exists():
            return
        
        for package_dir in packages_dir.iterdir():
            if package_dir.is_dir():
                runa_toml = package_dir / 'runa.toml'
                if runa_toml.exists():
                    try:
                        metadata = PackageMetadata.from_toml(str(runa_toml))
                        self.installed_packages[metadata.name] = metadata
                    except Exception as e:
                        print(f"Warning: Failed to load package {package_dir.name}: {e}")
    
    def search(self, query: str, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for packages."""
        return self.registry.search_packages(query, language)
    
    def install(self, package_name: str, version: Optional[str] = None, 
               language: Optional[str] = None) -> bool:
        """Install a package and its dependencies."""
        try:
            # Get package information
            package_info = self.registry.get_package_info(package_name, version)
            
            if not version:
                # Get latest version
                versions = self.registry.get_package_versions(package_name)
                version = sorted(versions, key=lambda v: PackageVersion.from_string(v), reverse=True)[0]
            
            # Check if already installed
            if package_name in self.installed_packages:
                installed_version = self.installed_packages[package_name].version
                if str(installed_version) == version:
                    print(f"Package {package_name}@{version} is already installed")
                    return True
            
            # Download package
            packages_dir = self.project_root / 'packages'
            packages_dir.mkdir(exist_ok=True)
            
            package_dir = self.registry.download_package(package_name, version, str(packages_dir))
            
            # Load package metadata
            metadata = PackageMetadata.from_toml(os.path.join(package_dir, 'runa.toml'))
            
            # Install dependencies
            for dep_name, dependency in metadata.dependencies.items():
                if dependency.type in ['runtime', 'build']:
                    print(f"Installing dependency: {dep_name}")
                    self.install(dep_name, dependency.version_constraint, dependency.language)
            
            # Update installed packages
            self.installed_packages[package_name] = metadata
            
            print(f"Successfully installed {package_name}@{version}")
            return True
            
        except Exception as e:
            print(f"Failed to install {package_name}: {e}")
            return False
    
    def uninstall(self, package_name: str) -> bool:
        """Uninstall a package."""
        if package_name not in self.installed_packages:
            print(f"Package {package_name} is not installed")
            return False
        
        try:
            # Remove package directory
            packages_dir = self.project_root / 'packages'
            package_dir = packages_dir / package_name
            
            if package_dir.exists():
                shutil.rmtree(package_dir)
            
            # Update installed packages
            del self.installed_packages[package_name]
            
            print(f"Successfully uninstalled {package_name}")
            return True
            
        except Exception as e:
            print(f"Failed to uninstall {package_name}: {e}")
            return False
    
    def list_installed(self) -> List[PackageMetadata]:
        """List all installed packages."""
        return list(self.installed_packages.values())
    
    def publish(self, package_path: Optional[str] = None) -> bool:
        """Publish a package to the registry."""
        package_path = package_path or str(self.project_root)
        runa_toml = os.path.join(package_path, 'runa.toml')
        
        if not os.path.exists(runa_toml):
            print("Error: No runa.toml found in package directory")
            return False
        
        try:
            metadata = PackageMetadata.from_toml(runa_toml)
            result = self.registry.publish_package(package_path, metadata)
            
            print(f"Successfully published {metadata.name}@{metadata.version}")
            print(f"Package URL: {result.get('url', 'N/A')}")
            return True
            
        except Exception as e:
            print(f"Failed to publish package: {e}")
            return False


def main():
    """CLI entry point for the package manager."""
    parser = argparse.ArgumentParser(
        prog='runa-package',
        description='Runa Multi-Language Package Manager'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for packages')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--language', help='Filter by language')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install a package')
    install_parser.add_argument('package', help='Package name')
    install_parser.add_argument('--version', help='Specific version to install')
    install_parser.add_argument('--language', help='Target language')
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall a package')
    uninstall_parser.add_argument('package', help='Package name')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List installed packages')
    
    # Publish command
    publish_parser = subparsers.add_parser('publish', help='Publish a package')
    publish_parser.add_argument('--path', help='Package directory path')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show package information')
    info_parser.add_argument('package', help='Package name')
    info_parser.add_argument('--version', help='Specific version')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize package manager
    package_manager = PackageManager()
    
    try:
        if args.command == 'search':
            results = package_manager.search(args.query, args.language)
            if results:
                print(f"Found {len(results)} packages:")
                for pkg in results:
                    print(f"  {pkg['name']} ({pkg['version']}) - {pkg['description']}")
            else:
                print("No packages found")
        
        elif args.command == 'install':
            success = package_manager.install(args.package, args.version, args.language)
            return 0 if success else 1
        
        elif args.command == 'uninstall':
            success = package_manager.uninstall(args.package)
            return 0 if success else 1
        
        elif args.command == 'list':
            packages = package_manager.list_installed()
            if packages:
                print("Installed packages:")
                for pkg in packages:
                    langs = ', '.join(pkg.supported_languages)
                    print(f"  {pkg.name} ({pkg.version}) - {langs}")
            else:
                print("No packages installed")
        
        elif args.command == 'publish':
            success = package_manager.publish(args.path)
            return 0 if success else 1
        
        elif args.command == 'info':
            info = package_manager.registry.get_package_info(args.package, args.version)
            print(f"Package: {info['name']}")
            print(f"Version: {info['version']}")
            print(f"Description: {info['description']}")
            print(f"Author: {info['author']}")
            print(f"Languages: {', '.join(info['supported_languages'])}")
            if info.get('dependencies'):
                print("Dependencies:")
                for dep_name, dep_info in info['dependencies'].items():
                    print(f"  {dep_name} ({dep_info['version_constraint']})")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())