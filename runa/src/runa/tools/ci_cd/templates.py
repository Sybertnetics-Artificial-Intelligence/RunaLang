#!/usr/bin/env python3
"""
Runa CI/CD Template Generator

Generates CI/CD pipeline configurations for various platforms with
multi-language support, automated testing, and deployment strategies.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime

from ..package.manager import PackageMetadata


class CIPlatform(Enum):
    """Supported CI/CD platforms."""
    GITHUB_ACTIONS = "github_actions"
    GITLAB_CI = "gitlab_ci"
    JENKINS = "jenkins"
    AZURE_PIPELINES = "azure_pipelines"
    CIRCLECI = "circleci"
    TRAVIS_CI = "travis_ci"
    BITBUCKET_PIPELINES = "bitbucket_pipelines"


class DeploymentTarget(Enum):
    """Deployment targets."""
    NPM = "npm"
    PYPI = "pypi"
    MAVEN_CENTRAL = "maven_central"
    NUGET = "nuget"
    CRATES_IO = "crates_io"
    DOCKER_HUB = "docker_hub"
    GITHUB_RELEASES = "github_releases"
    RUNA_REGISTRY = "runa_registry"
    STATIC_SITE = "static_site"
    CLOUD_FUNCTIONS = "cloud_functions"


@dataclass
class CIConfiguration:
    """Configuration for CI/CD pipeline generation."""
    platform: CIPlatform
    project_name: str
    
    # Build configuration
    target_languages: List[str] = field(default_factory=list)
    build_matrix: bool = True  # Test on multiple OS/versions
    parallel_builds: bool = True
    
    # Testing configuration
    run_unit_tests: bool = True
    run_integration_tests: bool = True
    run_cross_language_tests: bool = True
    test_coverage: bool = True
    coverage_threshold: float = 80.0
    
    # Quality checks
    code_formatting: bool = True
    linting: bool = True
    security_scanning: bool = True
    dependency_scanning: bool = True
    
    # Deployment configuration
    deployment_targets: List[DeploymentTarget] = field(default_factory=list)
    auto_deploy_on_tag: bool = True
    staging_deployment: bool = True
    
    # Notifications
    slack_notifications: bool = False
    email_notifications: bool = False
    
    # Advanced features
    caching: bool = True
    artifacts_retention_days: int = 30
    timeout_minutes: int = 60


class CITemplateGenerator:
    """Generates CI/CD pipeline templates for different platforms."""
    
    def __init__(self):
        self.language_tools = self._initialize_language_tools()
        self.platform_generators = {
            CIPlatform.GITHUB_ACTIONS: self._generate_github_actions,
            CIPlatform.GITLAB_CI: self._generate_gitlab_ci,
            CIPlatform.JENKINS: self._generate_jenkins,
            CIPlatform.AZURE_PIPELINES: self._generate_azure_pipelines,
            CIPlatform.CIRCLECI: self._generate_circleci
        }
    
    def _initialize_language_tools(self) -> Dict[str, Dict[str, Any]]:
        """Initialize language-specific tool configurations."""
        return {
            "runa": {
                "test_command": "runa test",
                "build_command": "runa build",
                "lint_command": "runa lint",
                "package_command": "runa package publish",
                "dependencies": []
            },
            "python": {
                "versions": ["3.8", "3.9", "3.10", "3.11"],
                "test_command": "python -m pytest",
                "build_command": "python -m build",
                "lint_command": "flake8",
                "format_command": "black",
                "package_command": "twine upload dist/*",
                "dependencies": ["pytest", "black", "flake8", "build", "twine"]
            },
            "javascript": {
                "versions": ["16", "18", "20"],
                "test_command": "npm test",
                "build_command": "npm run build",
                "lint_command": "npm run lint",
                "format_command": "npm run format",
                "package_command": "npm publish",
                "dependencies": ["jest", "eslint", "prettier"]
            },
            "typescript": {
                "versions": ["16", "18", "20"],
                "test_command": "npm test",
                "build_command": "npm run build",
                "lint_command": "npm run lint",
                "format_command": "npm run format",
                "package_command": "npm publish",
                "dependencies": ["typescript", "jest", "@types/jest", "eslint", "prettier"]
            },
            "java": {
                "versions": ["11", "17", "21"],
                "test_command": "mvn test",
                "build_command": "mvn compile",
                "lint_command": "mvn checkstyle:check",
                "package_command": "mvn deploy",
                "dependencies": []
            },
            "cpp": {
                "compilers": ["gcc", "clang"],
                "test_command": "make test",
                "build_command": "make",
                "lint_command": "cppcheck",
                "dependencies": ["cmake", "cppcheck"]
            },
            "rust": {
                "versions": ["stable", "beta"],
                "test_command": "cargo test",
                "build_command": "cargo build",
                "lint_command": "cargo clippy",
                "format_command": "cargo fmt",
                "package_command": "cargo publish",
                "dependencies": []
            },
            "go": {
                "versions": ["1.19", "1.20", "1.21"],
                "test_command": "go test ./...",
                "build_command": "go build",
                "lint_command": "golangci-lint run",
                "format_command": "go fmt",
                "dependencies": ["golangci-lint"]
            }
        }
    
    def generate_ci_pipeline(self, config: CIConfiguration, 
                           metadata: Optional[PackageMetadata] = None) -> Dict[str, str]:
        """Generate CI/CD pipeline for specified platform."""
        if config.platform not in self.platform_generators:
            raise ValueError(f"Unsupported CI platform: {config.platform}")
        
        generator = self.platform_generators[config.platform]
        return generator(config, metadata)
    
    def _generate_github_actions(self, config: CIConfiguration, 
                                metadata: Optional[PackageMetadata] = None) -> Dict[str, str]:
        """Generate GitHub Actions workflow."""
        workflows = {}
        
        # Main CI workflow
        workflows[".github/workflows/ci.yml"] = self._create_github_ci_workflow(config, metadata)
        
        # Release workflow
        if config.deployment_targets:
            workflows[".github/workflows/release.yml"] = self._create_github_release_workflow(config, metadata)
        
        # Security workflow
        if config.security_scanning:
            workflows[".github/workflows/security.yml"] = self._create_github_security_workflow(config)
        
        return workflows
    
    def _create_github_ci_workflow(self, config: CIConfiguration, 
                                  metadata: Optional[PackageMetadata] = None) -> str:
        """Create GitHub Actions CI workflow."""
        workflow = {
            "name": "CI",
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main"]}
            },
            "jobs": {}
        }
        
        # Add language-specific jobs
        for language in config.target_languages:
            if language in self.language_tools:
                job_name = f"test-{language.replace('_', '-')}"
                workflow["jobs"][job_name] = self._create_language_job(language, config)
        
        # Add cross-language test job
        if config.run_cross_language_tests and len(config.target_languages) > 1:
            workflow["jobs"]["cross-language-tests"] = self._create_cross_language_job(config)
        
        # Add deployment job
        if config.deployment_targets:
            workflow["jobs"]["deploy"] = self._create_deployment_job(config)
        
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False)
    
    def _create_language_job(self, language: str, config: CIConfiguration) -> Dict[str, Any]:
        """Create job configuration for a specific language."""
        tools = self.language_tools[language]
        
        job = {
            "runs-on": "ubuntu-latest" if not config.build_matrix else "${{ matrix.os }}",
            "strategy": {
                "matrix": self._get_build_matrix(language, config)
            } if config.build_matrix else None,
            "steps": [
                {
                    "name": "Checkout code",
                    "uses": "actions/checkout@v4"
                }
            ]
        }
        
        # Language-specific setup
        if language == "python":
            job["steps"].extend([
                {
                    "name": "Setup Python",
                    "uses": "actions/setup-python@v4",
                    "with": {
                        "python-version": "${{ matrix.python-version }}" if config.build_matrix else "3.11"
                    }
                },
                {
                    "name": "Install dependencies",
                    "run": "pip install -r requirements.txt" if Path("requirements.txt").exists() else "pip install ."
                }
            ])
        elif language in ["javascript", "typescript"]:
            job["steps"].extend([
                {
                    "name": "Setup Node.js",
                    "uses": "actions/setup-node@v4",
                    "with": {
                        "node-version": "${{ matrix.node-version }}" if config.build_matrix else "18"
                    }
                },
                {
                    "name": "Install dependencies",
                    "run": "npm ci"
                }
            ])
        elif language == "java":
            job["steps"].extend([
                {
                    "name": "Setup Java",
                    "uses": "actions/setup-java@v3",
                    "with": {
                        "java-version": "${{ matrix.java-version }}" if config.build_matrix else "17",
                        "distribution": "temurin"
                    }
                }
            ])
        elif language == "rust":
            job["steps"].extend([
                {
                    "name": "Setup Rust",
                    "uses": "actions-rs/toolchain@v1",
                    "with": {
                        "toolchain": "${{ matrix.rust-version }}" if config.build_matrix else "stable",
                        "components": "rustfmt, clippy"
                    }
                }
            ])
        elif language == "go":
            job["steps"].extend([
                {
                    "name": "Setup Go",
                    "uses": "actions/setup-go@v4",
                    "with": {
                        "go-version": "${{ matrix.go-version }}" if config.build_matrix else "1.21"
                    }
                }
            ])
        
        # Install Runa
        job["steps"].append({
            "name": "Install Runa",
            "run": "pip install runa-lang"
        })
        
        # Caching
        if config.caching:
            job["steps"].append(self._get_cache_step(language))
        
        # Code formatting
        if config.code_formatting and "format_command" in tools:
            job["steps"].append({
                "name": "Check code formatting",
                "run": tools["format_command"]
            })
        
        # Linting
        if config.linting and "lint_command" in tools:
            job["steps"].append({
                "name": "Run linter",
                "run": tools["lint_command"]
            })
        
        # Build
        job["steps"].append({
            "name": f"Build {language}",
            "run": tools.get("build_command", f"runa build --target {language}")
        })
        
        # Tests
        if config.run_unit_tests:
            job["steps"].append({
                "name": "Run unit tests",
                "run": tools.get("test_command", "runa test --type unit")
            })
        
        if config.run_integration_tests:
            job["steps"].append({
                "name": "Run integration tests",
                "run": tools.get("test_command", "runa test --type integration")
            })
        
        # Coverage
        if config.test_coverage:
            job["steps"].extend([
                {
                    "name": "Generate coverage report",
                    "run": self._get_coverage_command(language)
                },
                {
                    "name": "Upload coverage",
                    "uses": "codecov/codecov-action@v3",
                    "with": {
                        "file": self._get_coverage_file(language)
                    }
                }
            ])
        
        # Remove None values
        return {k: v for k, v in job.items() if v is not None}
    
    def _get_build_matrix(self, language: str, config: CIConfiguration) -> Dict[str, Any]:
        """Get build matrix for language."""
        tools = self.language_tools.get(language, {})
        matrix = {"os": ["ubuntu-latest", "windows-latest", "macos-latest"]}
        
        if language == "python" and "versions" in tools:
            matrix["python-version"] = tools["versions"]
        elif language in ["javascript", "typescript"] and "versions" in tools:
            matrix["node-version"] = tools["versions"]
        elif language == "java" and "versions" in tools:
            matrix["java-version"] = tools["versions"]
        elif language == "rust" and "versions" in tools:
            matrix["rust-version"] = tools["versions"]
        elif language == "go" and "versions" in tools:
            matrix["go-version"] = tools["versions"]
        
        return matrix
    
    def _get_cache_step(self, language: str) -> Dict[str, Any]:
        """Get cache configuration for language."""
        cache_configs = {
            "python": {
                "name": "Cache Python dependencies",
                "uses": "actions/cache@v3",
                "with": {
                    "path": "~/.cache/pip",
                    "key": "${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}"
                }
            },
            "javascript": {
                "name": "Cache Node.js dependencies",
                "uses": "actions/cache@v3",
                "with": {
                    "path": "~/.npm",
                    "key": "${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}"
                }
            },
            "typescript": {
                "name": "Cache Node.js dependencies", 
                "uses": "actions/cache@v3",
                "with": {
                    "path": "~/.npm",
                    "key": "${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}"
                }
            },
            "rust": {
                "name": "Cache Rust dependencies",
                "uses": "actions/cache@v3",
                "with": {
                    "path": "target",
                    "key": "${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}"
                }
            },
            "go": {
                "name": "Cache Go dependencies",
                "uses": "actions/cache@v3",
                "with": {
                    "path": "~/go/pkg/mod",
                    "key": "${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}"
                }
            }
        }
        
        return cache_configs.get(language, {
            "name": f"Cache {language} dependencies",
            "uses": "actions/cache@v3",
            "with": {
                "path": f".{language}_cache",
                "key": f"${{{{ runner.os }}}}-{language}-${{{{ hashFiles('**/*') }}}}"
            }
        })
    
    def _get_coverage_command(self, language: str) -> str:
        """Get coverage command for language."""
        commands = {
            "python": "python -m pytest --cov --cov-report=xml",
            "javascript": "npm run test:coverage",
            "typescript": "npm run test:coverage",
            "rust": "cargo tarpaulin --out xml",
            "go": "go test -coverprofile=coverage.out ./..."
        }
        return commands.get(language, "runa test --coverage")
    
    def _get_coverage_file(self, language: str) -> str:
        """Get coverage file path for language."""
        files = {
            "python": "./coverage.xml",
            "javascript": "./coverage/lcov.info",
            "typescript": "./coverage/lcov.info",
            "rust": "./cobertura.xml",
            "go": "./coverage.out"
        }
        return files.get(language, "./coverage.xml")
    
    def _create_cross_language_job(self, config: CIConfiguration) -> Dict[str, Any]:
        """Create cross-language testing job."""
        return {
            "runs-on": "ubuntu-latest",
            "needs": [f"test-{lang.replace('_', '-')}" for lang in config.target_languages],
            "steps": [
                {
                    "name": "Checkout code",
                    "uses": "actions/checkout@v4"
                },
                {
                    "name": "Setup multi-language environment",
                    "run": self._get_multilangiage_setup_script(config.target_languages)
                },
                {
                    "name": "Install Runa",
                    "run": "pip install runa-lang"
                },
                {
                    "name": "Run cross-language tests",
                    "run": "runa test --type cross_language --languages " + " ".join(config.target_languages)
                },
                {
                    "name": "Verify translation accuracy",
                    "run": "runa test --type verification --all-languages"
                }
            ]
        }
    
    def _get_multilangiage_setup_script(self, languages: List[str]) -> str:
        """Generate setup script for multiple languages."""
        setup_commands = []
        
        if "python" in languages:
            setup_commands.append("python -m pip install --upgrade pip")
        
        if any(lang in languages for lang in ["javascript", "typescript"]):
            setup_commands.append("npm install -g npm@latest")
        
        if "java" in languages:
            setup_commands.append("sudo apt-get update && sudo apt-get install -y openjdk-17-jdk")
        
        if "rust" in languages:
            setup_commands.append("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
        
        if "go" in languages:
            setup_commands.append("wget -q -O - https://go.dev/dl/go1.21.0.linux-amd64.tar.gz | sudo tar -C /usr/local -xzf -")
        
        return " && ".join(setup_commands)
    
    def _create_deployment_job(self, config: CIConfiguration) -> Dict[str, Any]:
        """Create deployment job."""
        return {
            "runs-on": "ubuntu-latest",
            "needs": [f"test-{lang.replace('_', '-')}" for lang in config.target_languages],
            "if": "github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')",
            "steps": [
                {
                    "name": "Checkout code",
                    "uses": "actions/checkout@v4"
                },
                {
                    "name": "Setup deployment environment",
                    "run": "pip install runa-lang"
                },
                {
                    "name": "Build all targets",
                    "run": "runa build --target production --languages " + " ".join(config.target_languages)
                }
            ] + [
                self._get_deployment_step(target) for target in config.deployment_targets
            ]
        }
    
    def _get_deployment_step(self, target: DeploymentTarget) -> Dict[str, Any]:
        """Get deployment step for specific target."""
        steps = {
            DeploymentTarget.RUNA_REGISTRY: {
                "name": "Publish to Runa Registry",
                "run": "runa package publish",
                "env": {
                    "RUNA_REGISTRY_TOKEN": "${{ secrets.RUNA_REGISTRY_TOKEN }}"
                }
            },
            DeploymentTarget.NPM: {
                "name": "Publish to NPM",
                "run": "npm publish",
                "env": {
                    "NPM_TOKEN": "${{ secrets.NPM_TOKEN }}"
                }
            },
            DeploymentTarget.PYPI: {
                "name": "Publish to PyPI",
                "run": "twine upload dist/*",
                "env": {
                    "TWINE_USERNAME": "__token__",
                    "TWINE_PASSWORD": "${{ secrets.PYPI_TOKEN }}"
                }
            },
            DeploymentTarget.GITHUB_RELEASES: {
                "name": "Create GitHub Release",
                "uses": "softprops/action-gh-release@v1",
                "with": {
                    "files": "dist/*",
                    "generate_release_notes": True
                }
            }
        }
        
        return steps.get(target, {
            "name": f"Deploy to {target.value}",
            "run": f"echo 'Deploying to {target.value}'"
        })
    
    def _create_github_release_workflow(self, config: CIConfiguration,
                                      metadata: Optional[PackageMetadata] = None) -> str:
        """Create GitHub Actions release workflow."""
        workflow = {
            "name": "Release",
            "on": {
                "push": {
                    "tags": ["v*"]
                }
            },
            "jobs": {
                "release": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v4"
                        },
                        {
                            "name": "Setup release environment",
                            "run": "pip install runa-lang"
                        },
                        {
                            "name": "Build release artifacts",
                            "run": "runa build --target release --optimize aggressive"
                        },
                        {
                            "name": "Run release tests",
                            "run": "runa test --type verification"
                        },
                        {
                            "name": "Package release",
                            "run": "runa package build --release"
                        }
                    ] + [
                        self._get_deployment_step(target) for target in config.deployment_targets
                    ]
                }
            }
        }
        
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False)
    
    def _create_github_security_workflow(self, config: CIConfiguration) -> str:
        """Create GitHub Actions security workflow."""
        workflow = {
            "name": "Security",
            "on": {
                "push": {"branches": ["main"]},
                "pull_request": {"branches": ["main"]},
                "schedule": [{"cron": "0 6 * * 1"}]  # Weekly
            },
            "jobs": {
                "security": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v4"
                        },
                        {
                            "name": "Run Trivy vulnerability scanner",
                            "uses": "aquasecurity/trivy-action@master",
                            "with": {
                                "scan-type": "fs",
                                "scan-ref": "."
                            }
                        },
                        {
                            "name": "Run dependency audit",
                            "run": "runa audit --dependencies"
                        },
                        {
                            "name": "Run security linting",
                            "run": "runa lint --security-rules"
                        }
                    ]
                }
            }
        }
        
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False)
    
    def _generate_gitlab_ci(self, config: CIConfiguration,
                           metadata: Optional[PackageMetadata] = None) -> Dict[str, str]:
        """Generate GitLab CI configuration."""
        gitlab_ci = {
            "stages": ["test", "build", "deploy"],
            "variables": {
                "PIP_CACHE_DIR": "$CI_PROJECT_DIR/.cache/pip"
            },
            "cache": {
                "paths": [".cache/pip"]
            }
        }
        
        # Add language-specific jobs
        for language in config.target_languages:
            job_name = f"test-{language}"
            gitlab_ci[job_name] = {
                "stage": "test",
                "image": self._get_gitlab_image(language),
                "script": self._get_gitlab_test_script(language, config),
                "artifacts": {
                    "reports": {
                        "junit": f"test-results-{language}.xml",
                        "coverage_report": {
                            "coverage_format": "cobertura",
                            "path": f"coverage-{language}.xml"
                        }
                    },
                    "expire_in": f"{config.artifacts_retention_days} days"
                }
            }
        
        return {".gitlab-ci.yml": yaml.dump(gitlab_ci, default_flow_style=False)}
    
    def _get_gitlab_image(self, language: str) -> str:
        """Get GitLab CI image for language."""
        images = {
            "python": "python:3.11",
            "javascript": "node:18",
            "typescript": "node:18",
            "java": "openjdk:17",
            "rust": "rust:latest",
            "go": "golang:1.21"
        }
        return images.get(language, "ubuntu:latest")
    
    def _get_gitlab_test_script(self, language: str, config: CIConfiguration) -> List[str]:
        """Get GitLab CI test script for language."""
        tools = self.language_tools.get(language, {})
        script = ["pip install runa-lang"]
        
        if language == "python":
            script.extend([
                "pip install -r requirements.txt",
                "python -m pytest --junitxml=test-results-python.xml --cov --cov-report=xml:coverage-python.xml"
            ])
        elif language in ["javascript", "typescript"]:
            script.extend([
                "npm ci",
                "npm test -- --coverage --ci --reporters=junit,default --outputFile=test-results-js.xml"
            ])
        
        script.append(f"runa build --target {language}")
        
        if config.run_cross_language_tests:
            script.append("runa test --type cross_language")
        
        return script
    
    def _generate_jenkins(self, config: CIConfiguration,
                         metadata: Optional[PackageMetadata] = None) -> Dict[str, str]:
        """Generate Jenkins pipeline configuration."""
        pipeline = {
            "pipeline": {
                "agent": "any",
                "stages": []
            }
        }
        
        # Test stage
        test_steps = []
        for language in config.target_languages:
            test_steps.append({
                "sh": f"runa test --language {language}"
            })
        
        pipeline["pipeline"]["stages"].append({
            "stage": "Test",
            "steps": test_steps
        })
        
        # Build stage
        pipeline["pipeline"]["stages"].append({
            "stage": "Build", 
            "steps": [
                {"sh": f"runa build --languages {' '.join(config.target_languages)}"}
            ]
        })
        
        if config.deployment_targets:
            pipeline["pipeline"]["stages"].append({
                "stage": "Deploy",
                "when": {"tag": "*"},
                "steps": [
                    {"sh": "runa package publish"}
                ]
            })
        
        return {"Jenkinsfile": json.dumps(pipeline, indent=2)}
    
    def _generate_azure_pipelines(self, config: CIConfiguration,
                                 metadata: Optional[PackageMetadata] = None) -> Dict[str, str]:
        """Generate Azure Pipelines configuration."""
        pipeline = {
            "trigger": ["main"],
            "pr": ["main"],
            "pool": {
                "vmImage": "ubuntu-latest"
            },
            "stages": []
        }
        
        # Test stage
        test_jobs = []
        for language in config.target_languages:
            test_jobs.append({
                "job": f"Test_{language}",
                "displayName": f"Test {language}",
                "steps": [
                    {
                        "task": "UsePythonVersion@0",
                        "inputs": {"versionSpec": "3.11"}
                    },
                    {
                        "script": "pip install runa-lang",
                        "displayName": "Install Runa"
                    },
                    {
                        "script": f"runa build --target {language}",
                        "displayName": f"Build {language}"
                    },
                    {
                        "script": f"runa test --language {language}",
                        "displayName": f"Test {language}"
                    }
                ]
            })
        
        pipeline["stages"].append({
            "stage": "Test",
            "jobs": test_jobs
        })
        
        return {"azure-pipelines.yml": yaml.dump(pipeline, default_flow_style=False)}
    
    def _generate_circleci(self, config: CIConfiguration,
                          metadata: Optional[PackageMetadata] = None) -> Dict[str, str]:
        """Generate CircleCI configuration."""
        circle_config = {
            "version": 2.1,
            "workflows": {
                "test-and-deploy": {
                    "jobs": []
                }
            },
            "jobs": {}
        }
        
        # Add language jobs
        for language in config.target_languages:
            job_name = f"test-{language}"
            circle_config["jobs"][job_name] = {
                "docker": [{"image": self._get_circleci_image(language)}],
                "steps": [
                    "checkout",
                    {"run": "pip install runa-lang"},
                    {"run": f"runa build --target {language}"},
                    {"run": f"runa test --language {language}"}
                ]
            }
            circle_config["workflows"]["test-and-deploy"]["jobs"].append(job_name)
        
        return {".circleci/config.yml": yaml.dump(circle_config, default_flow_style=False)}
    
    def _get_circleci_image(self, language: str) -> str:
        """Get CircleCI image for language."""
        images = {
            "python": "circleci/python:3.11",
            "javascript": "circleci/node:18",
            "typescript": "circleci/node:18",
            "java": "circleci/openjdk:17"
        }
        return images.get(language, "circleci/python:3.11")


def main():
    """CLI entry point for CI/CD template generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runa CI/CD Template Generator')
    parser.add_argument('platform', choices=['github', 'gitlab', 'jenkins', 'azure', 'circleci'],
                       help='CI/CD platform')
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--languages', nargs='*', default=['runa'], 
                       help='Target languages')
    parser.add_argument('--deploy-targets', nargs='*', 
                       choices=['npm', 'pypi', 'maven', 'nuget', 'crates', 'docker', 'github', 'runa'],
                       help='Deployment targets')
    parser.add_argument('--no-matrix', action='store_true', help='Disable build matrix')
    parser.add_argument('--no-coverage', action='store_true', help='Disable coverage')
    parser.add_argument('--no-security', action='store_true', help='Disable security scanning')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    
    args = parser.parse_args()
    
    # Map platform names
    platform_map = {
        'github': CIPlatform.GITHUB_ACTIONS,
        'gitlab': CIPlatform.GITLAB_CI,
        'jenkins': CIPlatform.JENKINS,
        'azure': CIPlatform.AZURE_PIPELINES,
        'circleci': CIPlatform.CIRCLECI
    }
    
    # Map deployment targets
    deploy_map = {
        'npm': DeploymentTarget.NPM,
        'pypi': DeploymentTarget.PYPI,
        'maven': DeploymentTarget.MAVEN_CENTRAL,
        'nuget': DeploymentTarget.NUGET,
        'crates': DeploymentTarget.CRATES_IO,
        'docker': DeploymentTarget.DOCKER_HUB,
        'github': DeploymentTarget.GITHUB_RELEASES,
        'runa': DeploymentTarget.RUNA_REGISTRY
    }
    
    config = CIConfiguration(
        platform=platform_map[args.platform],
        project_name=args.project,
        target_languages=args.languages,
        build_matrix=not args.no_matrix,
        test_coverage=not args.no_coverage,
        security_scanning=not args.no_security,
        deployment_targets=[deploy_map[t] for t in (args.deploy_targets or [])]
    )
    
    generator = CITemplateGenerator()
    templates = generator.generate_ci_pipeline(config)
    
    output_dir = Path(args.output_dir)
    
    print(f"Generating {args.platform.upper()} CI/CD templates...")
    
    for file_path, content in templates.items():
        full_path = output_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {full_path}")
    
    print(f"\nCI/CD templates generated successfully!")
    print(f"Platform: {args.platform.upper()}")
    print(f"Languages: {', '.join(args.languages)}")
    if args.deploy_targets:
        print(f"Deployment targets: {', '.join(args.deploy_targets)}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())