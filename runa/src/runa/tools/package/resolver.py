#!/usr/bin/env python3
"""
Runa Cross-Language Dependency Resolver

Advanced dependency resolution system supporting cross-language dependencies,
version constraints, conflict resolution, and circular dependency detection.
"""

import re
import os
import json
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque, defaultdict
import semver
import networkx as nx

from .manager import PackageVersion, PackageDependency, PackageMetadata, PackageRegistry


class DependencyType(Enum):
    """Types of dependencies in the resolution graph."""
    RUNTIME = "runtime"
    DEVELOPMENT = "development"
    BUILD = "build"
    TEST = "test"
    OPTIONAL = "optional"


class ConflictResolutionStrategy(Enum):
    """Strategies for resolving version conflicts."""
    LATEST = auto()          # Choose latest compatible version
    EARLIEST = auto()        # Choose earliest compatible version
    MANUAL = auto()          # Require manual resolution
    FAIL = auto()            # Fail on any conflict


@dataclass
class DependencyNode:
    """Represents a node in the dependency graph."""
    name: str
    version: PackageVersion
    language: str
    tier: int
    metadata: Optional[PackageMetadata] = None
    
    # Dependency relationships
    dependencies: Dict[str, PackageDependency] = field(default_factory=dict)
    dependents: Set[str] = field(default_factory=set)
    
    # Resolution metadata
    constraint_sources: List[str] = field(default_factory=list)  # Which packages require this
    is_optional: bool = False
    is_dev_only: bool = False
    depth: int = 0  # Distance from root in dependency tree
    
    def __str__(self) -> str:
        return f"{self.name}@{self.version} ({self.language})"
    
    def __hash__(self) -> int:
        return hash((self.name, str(self.version), self.language))


@dataclass
class DependencyConstraint:
    """Represents a version constraint on a dependency."""
    package_name: str
    version_constraint: str
    source_package: str
    language: Optional[str] = None
    dependency_type: DependencyType = DependencyType.RUNTIME
    is_optional: bool = False
    
    def satisfies(self, version: PackageVersion) -> bool:
        """Check if a version satisfies this constraint."""
        return version.satisfies(self.version_constraint)


@dataclass
class ResolutionResult:
    """Result of dependency resolution."""
    success: bool
    resolved_packages: Dict[str, DependencyNode] = field(default_factory=dict)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    circular_dependencies: List[List[str]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    resolution_time_ms: float = 0.0
    
    def get_install_order(self) -> List[DependencyNode]:
        """Get packages in installation order (topological sort)."""
        if not self.success:
            return []
        
        # Build dependency graph
        graph = nx.DiGraph()
        
        for package in self.resolved_packages.values():
            graph.add_node(package.name, package=package)
            
            for dep_name in package.dependencies:
                if dep_name in self.resolved_packages:
                    graph.add_edge(dep_name, package.name)  # dep -> package
        
        try:
            # Topological sort for installation order
            sorted_names = list(nx.topological_sort(graph))
            return [self.resolved_packages[name] for name in sorted_names]
        except nx.NetworkXError:
            # Fallback: sort by depth
            return sorted(self.resolved_packages.values(), key=lambda p: p.depth)


class CrossLanguageDependencyResolver:
    """Advanced dependency resolver supporting multiple languages and complex constraints."""
    
    def __init__(self, registry: PackageRegistry, 
                 conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.LATEST):
        self.registry = registry
        self.conflict_strategy = conflict_strategy
        
        # Language tier mapping for cross-language compatibility
        self.language_tiers = {
            1: ["javascript", "typescript", "python", "cpp", "java", "csharp", "sql"],
            2: ["rust", "go", "swift", "kotlin", "php", "webassembly"],
            3: ["html", "css", "shell", "hcl", "yaml", "json", "xml"],
            4: ["r", "matlab", "julia", "solidity", "graphql"],
            5: ["lisp", "haskell", "erlang", "elixir", "llvm_ir", "assembly"],
            6: ["objective_c", "visual_basic", "cobol", "ada", "perl", "fortran"]
        }
        
        # Cross-language compatibility matrix
        self.language_compatibility = self._build_compatibility_matrix()
        
        # Cache for package metadata
        self._metadata_cache: Dict[str, PackageMetadata] = {}
    
    def _build_compatibility_matrix(self) -> Dict[Tuple[str, str], float]:
        """Build compatibility matrix between languages."""
        compatibility = {}
        
        # Same language = perfect compatibility
        all_languages = ["runa"] + [lang for tier in self.language_tiers.values() for lang in tier]
        for lang in all_languages:
            compatibility[(lang, lang)] = 1.0
        
        # Runa = universal compatibility (it's the hub language)
        for lang in all_languages:
            if lang != "runa":
                compatibility[("runa", lang)] = 1.0
                compatibility[(lang, "runa")] = 1.0
        
        # Same tier = high compatibility
        for tier, languages in self.language_tiers.items():
            for lang1 in languages:
                for lang2 in languages:
                    if lang1 != lang2:
                        compatibility[(lang1, lang2)] = 0.8
        
        # Adjacent tiers = medium compatibility
        for tier in range(1, 6):
            tier1_langs = self.language_tiers.get(tier, [])
            tier2_langs = self.language_tiers.get(tier + 1, [])
            
            for lang1 in tier1_langs:
                for lang2 in tier2_langs:
                    compatibility[(lang1, lang2)] = 0.6
                    compatibility[(lang2, lang1)] = 0.6
        
        # Everything else = low compatibility
        for lang1 in all_languages:
            for lang2 in all_languages:
                if (lang1, lang2) not in compatibility:
                    compatibility[(lang1, lang2)] = 0.3
        
        return compatibility
    
    def resolve_dependencies(self, root_metadata: PackageMetadata, 
                           include_dev: bool = False, include_optional: bool = False) -> ResolutionResult:
        """
        Resolve all dependencies for a package.
        
        Args:
            root_metadata: The root package metadata
            include_dev: Whether to include development dependencies
            include_optional: Whether to include optional dependencies
            
        Returns:
            ResolutionResult with resolved packages or conflicts
        """
        import time
        start_time = time.time()
        
        result = ResolutionResult()
        
        # Build constraint graph
        constraints = self._collect_constraints(root_metadata, include_dev, include_optional)
        
        # Check for circular dependencies
        circular_deps = self._detect_circular_dependencies(constraints)
        if circular_deps:
            result.circular_dependencies = circular_deps
            result.success = False
            result.resolution_time_ms = (time.time() - start_time) * 1000
            return result
        
        # Resolve version constraints
        resolved_versions = self._resolve_version_constraints(constraints)
        
        if not resolved_versions:
            result.success = False
            result.conflicts.append({
                "type": "unsatisfiable_constraints",
                "message": "No solution found for version constraints"
            })
            result.resolution_time_ms = (time.time() - start_time) * 1000
            return result
        
        # Build dependency nodes
        try:
            resolved_packages = {}
            for package_name, version in resolved_versions.items():
                node = self._create_dependency_node(package_name, version, constraints)
                resolved_packages[package_name] = node
            
            # Validate cross-language compatibility
            compatibility_warnings = self._validate_cross_language_compatibility(resolved_packages)
            result.warnings.extend(compatibility_warnings)
            
            result.resolved_packages = resolved_packages
            result.success = True
            
        except Exception as e:
            result.success = False
            result.conflicts.append({
                "type": "resolution_error",
                "message": str(e)
            })
        
        result.resolution_time_ms = (time.time() - start_time) * 1000
        return result
    
    def _collect_constraints(self, root_metadata: PackageMetadata, 
                           include_dev: bool, include_optional: bool) -> Dict[str, List[DependencyConstraint]]:
        """Collect all dependency constraints recursively."""
        constraints: Dict[str, List[DependencyConstraint]] = defaultdict(list)
        visited: Set[str] = set()
        queue = deque([(root_metadata.name, root_metadata, 0)])
        
        while queue:
            package_name, metadata, depth = queue.popleft()
            
            if package_name in visited:
                continue
            visited.add(package_name)
            
            # Process dependencies
            for dep_name, dependency in metadata.dependencies.items():
                # Skip unwanted dependency types
                if dependency.type == "development" and not include_dev:
                    continue
                if dependency.optional and not include_optional:
                    continue
                
                # Add constraint
                constraint = DependencyConstraint(
                    package_name=dep_name,
                    version_constraint=dependency.version_constraint,
                    source_package=package_name,
                    language=dependency.language,
                    dependency_type=DependencyType(dependency.type),
                    is_optional=dependency.optional
                )
                constraints[dep_name].append(constraint)
                
                # Get dependency metadata for recursive processing
                try:
                    dep_metadata = self._get_package_metadata(dep_name, dependency.version_constraint)
                    if dep_metadata:
                        queue.append((dep_name, dep_metadata, depth + 1))
                except Exception as e:
                    # Log warning but continue
                    pass
        
        return dict(constraints)
    
    def _detect_circular_dependencies(self, constraints: Dict[str, List[DependencyConstraint]]) -> List[List[str]]:
        """Detect circular dependencies in the constraint graph."""
        # Build directed graph
        graph = nx.DiGraph()
        
        for package_name, package_constraints in constraints.items():
            graph.add_node(package_name)
            for constraint in package_constraints:
                graph.add_edge(constraint.source_package, package_name)
        
        # Find strongly connected components with more than one node
        try:
            cycles = []
            for component in nx.strongly_connected_components(graph):
                if len(component) > 1:
                    cycles.append(list(component))
            return cycles
        except Exception:
            return []
    
    def _resolve_version_constraints(self, constraints: Dict[str, List[DependencyConstraint]]) -> Optional[Dict[str, PackageVersion]]:
        """Resolve version constraints using SAT solver approach."""
        resolved = {}
        
        for package_name, package_constraints in constraints.items():
            # Get all available versions
            try:
                available_versions = self.registry.get_package_versions(package_name)
                if not available_versions:
                    continue
                
                # Convert to PackageVersion objects
                version_objects = []
                for v in available_versions:
                    try:
                        version_objects.append(PackageVersion.from_string(v))
                    except ValueError:
                        continue
                
                # Find versions that satisfy all constraints
                satisfying_versions = []
                for version in version_objects:
                    if all(constraint.satisfies(version) for constraint in package_constraints):
                        satisfying_versions.append(version)
                
                if not satisfying_versions:
                    # No version satisfies all constraints
                    return None
                
                # Apply conflict resolution strategy
                if self.conflict_strategy == ConflictResolutionStrategy.LATEST:
                    chosen_version = max(satisfying_versions, key=lambda v: (v.major, v.minor, v.patch))
                elif self.conflict_strategy == ConflictResolutionStrategy.EARLIEST:
                    chosen_version = min(satisfying_versions, key=lambda v: (v.major, v.minor, v.patch))
                else:
                    # Default to latest
                    chosen_version = max(satisfying_versions, key=lambda v: (v.major, v.minor, v.patch))
                
                resolved[package_name] = chosen_version
                
            except Exception as e:
                # Skip packages that can't be resolved
                continue
        
        return resolved
    
    def _create_dependency_node(self, package_name: str, version: PackageVersion, 
                               constraints: Dict[str, List[DependencyConstraint]]) -> DependencyNode:
        """Create a dependency node with full metadata."""
        # Get package metadata
        metadata = self._get_package_metadata(package_name, str(version))
        if not metadata:
            # Create minimal node
            return DependencyNode(
                name=package_name,
                version=version,
                language="unknown",
                tier=6  # Lowest tier for unknown packages
            )
        
        # Determine language tier
        tier = self._get_language_tier(metadata.primary_language)
        
        # Get constraint sources
        constraint_sources = []
        is_optional = False
        is_dev_only = True
        
        if package_name in constraints:
            for constraint in constraints[package_name]:
                constraint_sources.append(constraint.source_package)
                if not constraint.is_optional:
                    is_optional = False
                if constraint.dependency_type != DependencyType.DEVELOPMENT:
                    is_dev_only = False
        
        node = DependencyNode(
            name=package_name,
            version=version,
            language=metadata.primary_language,
            tier=tier,
            metadata=metadata,
            dependencies=metadata.dependencies,
            constraint_sources=constraint_sources,
            is_optional=is_optional,
            is_dev_only=is_dev_only
        )
        
        return node
    
    def _get_package_metadata(self, package_name: str, version_constraint: str) -> Optional[PackageMetadata]:
        """Get package metadata, with caching."""
        cache_key = f"{package_name}@{version_constraint}"
        
        if cache_key in self._metadata_cache:
            return self._metadata_cache[cache_key]
        
        try:
            # Get package info from registry
            package_info = self.registry.get_package_info(package_name)
            
            # Convert to PackageMetadata (simplified for now)
            metadata = PackageMetadata(
                name=package_info["name"],
                version=PackageVersion.from_string(package_info["version"]),
                description=package_info["description"],
                author=package_info["author"],
                email=package_info["email"],
                license=package_info["license"],
                primary_language=package_info.get("primary_language", "runa"),
                supported_languages=package_info.get("supported_languages", ["runa"])
            )
            
            # Parse dependencies
            dependencies = {}
            for dep_name, dep_info in package_info.get("dependencies", {}).items():
                dependencies[dep_name] = PackageDependency(
                    name=dep_name,
                    version_constraint=dep_info["version_constraint"],
                    language=dep_info.get("language"),
                    optional=dep_info.get("optional", False),
                    type=dep_info.get("type", "runtime")
                )
            metadata.dependencies = dependencies
            
            self._metadata_cache[cache_key] = metadata
            return metadata
            
        except Exception:
            return None
    
    def _get_language_tier(self, language: str) -> int:
        """Get the tier number for a language."""
        for tier, languages in self.language_tiers.items():
            if language in languages:
                return tier
        return 1 if language == "runa" else 6  # Runa is tier 1, unknown is tier 6
    
    def _validate_cross_language_compatibility(self, packages: Dict[str, DependencyNode]) -> List[str]:
        """Validate cross-language compatibility and return warnings."""
        warnings = []
        
        # Check for cross-language dependencies
        for package in packages.values():
            for dep_name, dependency in package.dependencies.items():
                if dep_name in packages:
                    dep_package = packages[dep_name]
                    
                    # Check language compatibility
                    compat_key = (package.language, dep_package.language)
                    compatibility = self.language_compatibility.get(compat_key, 0.3)
                    
                    if compatibility < 0.5:
                        warnings.append(
                            f"Low compatibility between {package.name} ({package.language}) "
                            f"and {dep_package.name} ({dep_package.language}): {compatibility:.1%}"
                        )
                    
                    # Check tier compatibility
                    tier_diff = abs(package.tier - dep_package.tier)
                    if tier_diff > 2:
                        warnings.append(
                            f"Large tier difference between {package.name} (tier {package.tier}) "
                            f"and {dep_package.name} (tier {dep_package.tier})"
                        )
        
        return warnings
    
    def find_dependency_conflicts(self, packages: List[PackageMetadata]) -> List[Dict[str, Any]]:
        """Find potential dependency conflicts between packages."""
        conflicts = []
        
        # Collect all constraints
        all_constraints: Dict[str, List[DependencyConstraint]] = defaultdict(list)
        
        for package in packages:
            for dep_name, dependency in package.dependencies.items():
                constraint = DependencyConstraint(
                    package_name=dep_name,
                    version_constraint=dependency.version_constraint,
                    source_package=package.name,
                    language=dependency.language,
                    dependency_type=DependencyType(dependency.type)
                )
                all_constraints[dep_name].append(constraint)
        
        # Check for version conflicts
        for package_name, constraints in all_constraints.items():
            if len(constraints) > 1:
                # Get available versions
                try:
                    available_versions = self.registry.get_package_versions(package_name)
                    version_objects = [PackageVersion.from_string(v) for v in available_versions]
                    
                    # Find versions that satisfy all constraints
                    satisfying_versions = []
                    for version in version_objects:
                        if all(constraint.satisfies(version) for constraint in constraints):
                            satisfying_versions.append(version)
                    
                    if not satisfying_versions:
                        conflicts.append({
                            "type": "version_conflict",
                            "package": package_name,
                            "constraints": [
                                {
                                    "source": c.source_package,
                                    "constraint": c.version_constraint,
                                    "language": c.language
                                }
                                for c in constraints
                            ],
                            "message": f"No version of {package_name} satisfies all constraints"
                        })
                
                except Exception:
                    # Skip packages we can't analyze
                    continue
        
        return conflicts
    
    def suggest_dependency_updates(self, metadata: PackageMetadata) -> List[Dict[str, Any]]:
        """Suggest dependency updates based on available versions."""
        suggestions = []
        
        for dep_name, dependency in metadata.dependencies.items():
            try:
                # Get latest version
                available_versions = self.registry.get_package_versions(dep_name)
                if not available_versions:
                    continue
                
                latest_version = max(
                    [PackageVersion.from_string(v) for v in available_versions],
                    key=lambda v: (v.major, v.minor, v.patch)
                )
                
                # Check if current constraint allows latest
                if not latest_version.satisfies(dependency.version_constraint):
                    suggestions.append({
                        "package": dep_name,
                        "current_constraint": dependency.version_constraint,
                        "latest_version": str(latest_version),
                        "suggested_constraint": f"^{latest_version}",
                        "language": dependency.language,
                        "type": dependency.type
                    })
            
            except Exception:
                continue
        
        return suggestions


class DependencyLockFile:
    """Manages dependency lock files for reproducible builds."""
    
    def __init__(self, lock_file_path: str = "runa.lock"):
        self.lock_file_path = lock_file_path
    
    def save_lock_file(self, result: ResolutionResult, metadata: PackageMetadata):
        """Save resolved dependencies to lock file."""
        if not result.success:
            return
        
        lock_data = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "root_package": {
                "name": metadata.name,
                "version": str(metadata.version),
                "language": metadata.primary_language
            },
            "packages": {},
            "resolution_metadata": {
                "resolution_time_ms": result.resolution_time_ms,
                "conflict_count": len(result.conflicts),
                "warning_count": len(result.warnings)
            }
        }
        
        # Add resolved packages
        for package in result.resolved_packages.values():
            lock_data["packages"][package.name] = {
                "version": str(package.version),
                "language": package.language,
                "tier": package.tier,
                "dependencies": list(package.dependencies.keys()),
                "is_optional": package.is_optional,
                "is_dev_only": package.is_dev_only,
                "depth": package.depth
            }
        
        # Write lock file
        with open(self.lock_file_path, 'w', encoding='utf-8') as f:
            json.dump(lock_data, f, indent=2, sort_keys=True)
    
    def load_lock_file(self) -> Optional[Dict[str, Any]]:
        """Load dependency lock file."""
        if not os.path.exists(self.lock_file_path):
            return None
        
        try:
            with open(self.lock_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def is_lock_file_valid(self, metadata: PackageMetadata) -> bool:
        """Check if lock file is valid for current package metadata."""
        lock_data = self.load_lock_file()
        if not lock_data:
            return False
        
        # Check root package
        root_info = lock_data.get("root_package", {})
        if (root_info.get("name") != metadata.name or 
            root_info.get("version") != str(metadata.version)):
            return False
        
        # Check if all dependencies are present
        locked_packages = set(lock_data.get("packages", {}).keys())
        current_deps = set(metadata.dependencies.keys())
        
        return current_deps.issubset(locked_packages)


def main():
    """CLI entry point for dependency resolver."""
    import argparse
    from .manager import PackageManager
    
    parser = argparse.ArgumentParser(description='Runa Dependency Resolver')
    parser.add_argument('--package-dir', default='.', help='Package directory')
    parser.add_argument('--include-dev', action='store_true', help='Include development dependencies')
    parser.add_argument('--include-optional', action='store_true', help='Include optional dependencies')
    parser.add_argument('--check-conflicts', action='store_true', help='Check for conflicts only')
    parser.add_argument('--suggest-updates', action='store_true', help='Suggest dependency updates')
    parser.add_argument('--output', help='Output file for results')
    
    args = parser.parse_args()
    
    # Load package metadata
    runa_toml = os.path.join(args.package_dir, 'runa.toml')
    if not os.path.exists(runa_toml):
        print("Error: No runa.toml found in package directory")
        return 1
    
    try:
        metadata = PackageMetadata.from_toml(runa_toml)
        
        # Initialize resolver
        package_manager = PackageManager(args.package_dir)
        resolver = CrossLanguageDependencyResolver(package_manager.registry)
        
        if args.check_conflicts:
            # Check for conflicts
            conflicts = resolver.find_dependency_conflicts([metadata])
            
            if conflicts:
                print(f"Found {len(conflicts)} dependency conflicts:")
                for conflict in conflicts:
                    print(f"  - {conflict['message']}")
                return 1
            else:
                print("No dependency conflicts found")
        
        elif args.suggest_updates:
            # Suggest updates
            suggestions = resolver.suggest_dependency_updates(metadata)
            
            if suggestions:
                print(f"Found {len(suggestions)} update suggestions:")
                for suggestion in suggestions:
                    print(f"  - {suggestion['package']}: {suggestion['current_constraint']} -> {suggestion['suggested_constraint']}")
            else:
                print("All dependencies are up to date")
        
        else:
            # Resolve dependencies
            result = resolver.resolve_dependencies(
                metadata, 
                include_dev=args.include_dev,
                include_optional=args.include_optional
            )
            
            if result.success:
                print(f"Successfully resolved {len(result.resolved_packages)} packages")
                
                if result.warnings:
                    print(f"Warnings ({len(result.warnings)}):")
                    for warning in result.warnings:
                        print(f"  - {warning}")
                
                # Show install order
                install_order = result.get_install_order()
                print("\nInstallation order:")
                for i, package in enumerate(install_order, 1):
                    print(f"  {i}. {package}")
                
                # Save lock file
                lock_file = DependencyLockFile(os.path.join(args.package_dir, 'runa.lock'))
                lock_file.save_lock_file(result, metadata)
                print(f"\nLock file saved to {lock_file.lock_file_path}")
                
            else:
                print("Dependency resolution failed")
                
                if result.conflicts:
                    print("Conflicts:")
                    for conflict in result.conflicts:
                        print(f"  - {conflict['message']}")
                
                if result.circular_dependencies:
                    print("Circular dependencies:")
                    for cycle in result.circular_dependencies:
                        print(f"  - {' -> '.join(cycle + [cycle[0]])}")
                
                return 1
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())