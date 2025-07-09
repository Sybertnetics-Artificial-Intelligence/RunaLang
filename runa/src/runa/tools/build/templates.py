#!/usr/bin/env python3
"""
Runa Project Templates

Multi-language project templates for each tier with proper structure,
configuration, and best practices for Runa development.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import jinja2

from ..package.manager import PackageMetadata, PackageVersion


@dataclass
class TemplateVariable:
    """A template variable with metadata."""
    name: str
    description: str
    default_value: Any
    required: bool = True
    variable_type: str = "string"  # string, int, bool, list


@dataclass
class ProjectTemplate:
    """Definition of a project template."""
    name: str
    description: str
    language_tier: int
    primary_language: str
    supported_languages: List[str]
    
    # Template configuration
    variables: List[TemplateVariable] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)  # relative_path -> template_content
    directories: List[str] = field(default_factory=list)
    
    # Metadata
    version: str = "1.0.0"
    author: str = "Runa Team"
    license: str = "MIT"
    tags: List[str] = field(default_factory=list)


class ProjectTemplateManager:
    """Manages and creates projects from templates."""
    
    def __init__(self):
        self.templates: Dict[str, ProjectTemplate] = {}
        self.jinja_env = jinja2.Environment(
            loader=jinja2.DictLoader({}),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Initialize built-in templates
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize built-in project templates."""
        
        # Basic Runa Library Template
        self.templates["runa-library"] = self._create_runa_library_template()
        
        # Tier 1 Templates
        self.templates["web-frontend"] = self._create_web_frontend_template()
        self.templates["python-package"] = self._create_python_package_template()
        self.templates["typescript-library"] = self._create_typescript_library_template()
        self.templates["cpp-application"] = self._create_cpp_application_template()
        self.templates["java-application"] = self._create_java_application_template()
        
        # Tier 2 Templates
        self.templates["rust-crate"] = self._create_rust_crate_template()
        self.templates["go-module"] = self._create_go_module_template()
        
        # Tier 3 Templates
        self.templates["web-component"] = self._create_web_component_template()
        self.templates["config-package"] = self._create_config_package_template()
        
        # Multi-language Templates
        self.templates["universal-library"] = self._create_universal_library_template()
        self.templates["cross-platform-app"] = self._create_cross_platform_app_template()
    
    def create_project(self, template_name: str, project_name: str, 
                      project_dir: str, variables: Optional[Dict[str, Any]] = None) -> bool:
        """Create a new project from a template."""
        if template_name not in self.templates:
            print(f"Template '{template_name}' not found")
            return False
        
        template = self.templates[template_name]
        variables = variables or {}
        
        # Validate required variables
        for var in template.variables:
            if var.required and var.name not in variables:
                if var.default_value is not None:
                    variables[var.name] = var.default_value
                else:
                    print(f"Required variable '{var.name}' not provided")
                    return False
        
        # Add standard variables
        variables.update({
            'project_name': project_name,
            'project_name_snake': project_name.lower().replace('-', '_').replace(' ', '_'),
            'project_name_pascal': ''.join(word.capitalize() for word in project_name.replace('-', ' ').replace('_', ' ').split()),
            'current_year': datetime.now().year,
            'current_date': datetime.now().isoformat()[:10],
            'template_name': template_name,
            'template_version': template.version
        })
        
        project_path = Path(project_dir)
        project_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Create directories
            for directory in template.directories:
                dir_path = project_path / self._render_template(directory, variables)
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create files
            for file_path, content in template.files.items():
                rendered_path = self._render_template(file_path, variables)
                rendered_content = self._render_template(content, variables)
                
                full_path = project_path / rendered_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(rendered_content)
            
            print(f"Project '{project_name}' created successfully at {project_path}")
            return True
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False
    
    def _render_template(self, template_str: str, variables: Dict[str, Any]) -> str:
        """Render a template string with variables."""
        template = self.jinja_env.from_string(template_str)
        return template.render(**variables)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates."""
        return [
            {
                "name": name,
                "description": template.description,
                "language_tier": template.language_tier,
                "primary_language": template.primary_language,
                "supported_languages": template.supported_languages,
                "version": template.version,
                "tags": template.tags
            }
            for name, template in self.templates.items()
        ]
    
    def get_template_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a template."""
        if template_name not in self.templates:
            return None
        
        template = self.templates[template_name]
        return {
            "name": template_name,
            "description": template.description,
            "language_tier": template.language_tier,
            "primary_language": template.primary_language,
            "supported_languages": template.supported_languages,
            "version": template.version,
            "author": template.author,
            "license": template.license,
            "tags": template.tags,
            "variables": [
                {
                    "name": var.name,
                    "description": var.description,
                    "default_value": var.default_value,
                    "required": var.required,
                    "type": var.variable_type
                }
                for var in template.variables
            ],
            "file_count": len(template.files),
            "directory_count": len(template.directories)
        }
    
    # Template creation methods
    
    def _create_runa_library_template(self) -> ProjectTemplate:
        """Create basic Runa library template."""
        return ProjectTemplate(
            name="runa-library",
            description="Basic Runa library with standard structure",
            language_tier=1,
            primary_language="runa",
            supported_languages=["runa"],
            variables=[
                TemplateVariable("author_name", "Package author name", "Runa Developer"),
                TemplateVariable("author_email", "Package author email", "developer@example.com"),
                TemplateVariable("description", "Package description", "A Runa library"),
                TemplateVariable("license", "Package license", "MIT"),
                TemplateVariable("version", "Initial version", "0.1.0")
            ],
            directories=[
                "src",
                "tests",
                "examples",
                "docs"
            ],
            files={
                "runa.toml": '''[package]
name = "{{ project_name }}"
version = "{{ version }}"
description = "{{ description }}"
author = "{{ author_name }}"
email = "{{ author_email }}"
license = "{{ license }}"
homepage = "https://github.com/{{ author_name }}/{{ project_name }}"
repository = "https://github.com/{{ author_name }}/{{ project_name }}"
keywords = ["runa", "library"]
categories = ["libraries"]

[dependencies]
# Add your dependencies here

[build]
entry-point = "src/main.runa"
include = ["src/**/*.runa", "README.md", "LICENSE"]
exclude = ["tests/**", "examples/**"]
test-command = "runa test"

[scripts]
test = "runa test tests/ --verbose"
docs = "runa doc generate --output docs/"
''',
                "src/main.runa": '''Note: Main module for {{ project_name }}
Note: {{ description }}

Note: Export your public API here
Export greet

Process called "greet" that takes name as String returns String:
    Return "Hello, " followed by name
''',
                "tests/test_main.runa": '''Note: Tests for {{ project_name }}

Import "src/main" exposing greet

Process called "test_greet":
    Let result be greet with name as "World"
    Display "Testing greet function: " with message result
''',
                "examples/basic_usage.runa": '''Note: Basic usage example for {{ project_name }}

Import "src/main" exposing greet

Process called "main":
    Let greeting be greet with name as "Runa"
    Display greeting
''',
                "README.md": '''# {{ project_name }}

{{ description }}

## Installation

```bash
runa package install {{ project_name }}
```

## Usage

```runa
Import "{{ project_name }}" exposing greet

Process called "main":
    Let message be greet with name as "World"
    Display message
```

## Development

```bash
# Install dependencies
runa package install

# Run tests
runa test

# Build the package
runa build

# Generate documentation
runa doc generate
```

## License

{{ license }}
''',
                "LICENSE": '''MIT License

Copyright (c) {{ current_year }} {{ author_name }}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
                ".gitignore": '''# Runa build outputs
dist/
*.runa.cache
runa.lock

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Dependencies
packages/
node_modules/
'''
            },
            tags=["runa", "library", "basic"]
        )
    
    def _create_web_frontend_template(self) -> ProjectTemplate:
        """Create web frontend template with JavaScript/TypeScript."""
        return ProjectTemplate(
            name="web-frontend",
            description="Web frontend application with Runa -> JavaScript/TypeScript compilation",
            language_tier=1,
            primary_language="runa",
            supported_languages=["runa", "javascript", "typescript", "html", "css"],
            variables=[
                TemplateVariable("use_typescript", "Use TypeScript instead of JavaScript", True, True, "bool"),
                TemplateVariable("include_css_framework", "Include CSS framework", "none", False),
                TemplateVariable("bundle_assets", "Bundle assets for production", True, True, "bool")
            ],
            directories=[
                "src",
                "src/components",
                "src/utils",
                "public",
                "tests",
                "docs"
            ],
            files={
                "runa.toml": '''[package]
name = "{{ project_name }}"
version = "0.1.0"
description = "Web frontend application built with Runa"
author = "{{ author_name }}"
email = "{{ author_email }}"
license = "MIT"
primary_language = "runa"
supported_languages = ["runa", "{% if use_typescript %}typescript{% else %}javascript{% endif %}", "html", "css"]

[targets]
{% if use_typescript %}
typescript = { tier = 1, version = "4.0+", features = ["strict", "es2020"] }
{% else %}
javascript = { tier = 1, version = "es2020+", features = ["modules"] }
{% endif %}
html = { tier = 3, features = ["html5"] }
css = { tier = 3, features = ["css3", "flexbox", "grid"] }

[build]
entry-point = "src/app.runa"
include = ["src/**/*.runa", "public/**", "*.html"]
exclude = ["tests/**", "*.md"]
build-scripts = [
    "runa compile --target {% if use_typescript %}typescript{% else %}javascript{% endif %}",
    {% if bundle_assets %}"runa bundle --target web"{% endif %}
]

[scripts]
dev = "runa build --target development && runa serve"
build = "runa build --target production"
test = "runa test tests/"
serve = "runa serve public/ --port 3000"
''',
                "src/app.runa": '''Note: Main application entry point
Note: Web frontend application built with Runa

Import "components/header" exposing Header
Import "components/main" exposing Main
Import "utils/dom" exposing render

Process called "main":
    Let app be create app
    render with element as app and target as "app"

Process called "create app":
    Return create element with tag as "div" and children as list containing
        Header with title as "{{ project_name }}",
        Main with content as "Welcome to your Runa web application!"
''',
                "src/components/header.runa": '''Note: Header component

Export Header

Process called "Header" that takes title as String returns Element:
    Return create element with:
        tag as "header"
        attributes as dictionary containing "class" as "app-header"
        children as list containing
            create element with tag as "h1" and text as title
''',
                "src/components/main.runa": '''Note: Main content component

Export Main

Process called "Main" that takes content as String returns Element:
    Return create element with:
        tag as "main"
        attributes as dictionary containing "class" as "app-main"
        children as list containing
            create element with tag as "p" and text as content
''',
                "src/utils/dom.runa": '''Note: DOM manipulation utilities

Export render, create element

Process called "render" that takes element as Element and target as String:
    Let container be document get element by id with id as target
    If container is not null:
        Set container inner html to element to html with element as element

Process called "create element" that takes tag as String and attributes as Optional Dictionary and children as Optional List returns Element:
    Note: This would be implemented to create DOM elements
    Return new Element with tag as tag
''',
                "public/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app"></div>
    <script src="dist/app.js"></script>
</body>
</html>
''',
                "public/styles.css": ''':root {
  --primary-color: #007acc;
  --background-color: #f5f5f5;
  --text-color: #333;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
}

.app-header {
  background-color: var(--primary-color);
  color: white;
  padding: 1rem;
  text-align: center;
}

.app-main {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.app-main p {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}
''',
                "tests/test_components.runa": '''Note: Component tests

Import "src/components/header" exposing Header
Import "src/components/main" exposing Main

Process called "test_header":
    Let header be Header with title as "Test Title"
    Note: Add assertions here
    Display "Header component test passed"

Process called "test_main":
    Let main be Main with content as "Test content"
    Note: Add assertions here
    Display "Main component test passed"
'''
            },
            tags=["web", "frontend", "javascript", "typescript", "html", "css"]
        )
    
    def _create_python_package_template(self) -> ProjectTemplate:
        """Create Python package template."""
        return ProjectTemplate(
            name="python-package",
            description="Python package with Runa -> Python compilation",
            language_tier=1,
            primary_language="runa",
            supported_languages=["runa", "python"],
            directories=[
                "src",
                "tests",
                "docs"
            ],
            files={
                "runa.toml": '''[package]
name = "{{ project_name }}"
version = "0.1.0"
description = "Python package built with Runa"
author = "{{ author_name }}"
email = "{{ author_email }}"
license = "MIT"
primary_language = "runa"
supported_languages = ["runa", "python"]

[targets]
python = { tier = 1, version = "3.8+", features = ["type_hints"] }

[build]
entry-point = "src/main.runa"
build-scripts = ["runa compile --target python"]

[scripts]
test = "python -m pytest tests/"
install = "pip install -e ."
''',
                "setup.py": '''from setuptools import setup, find_packages

setup(
    name="{{ project_name_snake }}",
    version="0.1.0",
    description="{{ description }}",
    author="{{ author_name }}",
    author_email="{{ author_email }}",
    packages=find_packages(where="dist/python"),
    package_dir={"": "dist/python"},
    python_requires=">=3.8",
    install_requires=[
        # Add your Python dependencies here
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
''',
                "src/main.runa": '''Note: Main Python module

Export calculate, format result

Process called "calculate" that takes x as Integer and y as Integer returns Integer:
    Return x plus y

Process called "format result" that takes result as Integer returns String:
    Return "Result: " followed by result as String
'''
            },
            tags=["python", "package"]
        )
    
    def _create_universal_library_template(self) -> ProjectTemplate:
        """Create universal library template supporting multiple languages."""
        return ProjectTemplate(
            name="universal-library",
            description="Universal library supporting multiple target languages",
            language_tier=1,
            primary_language="runa",
            supported_languages=["runa", "python", "javascript", "typescript", "java", "cpp"],
            variables=[
                TemplateVariable("target_languages", "Target languages to support", 
                               ["python", "javascript", "java"], True, "list")
            ],
            directories=[
                "src",
                "tests",
                "examples",
                "docs",
                "scripts"
            ],
            files={
                "runa.toml": '''[package]
name = "{{ project_name }}"
version = "0.1.0"
description = "Universal library supporting multiple languages"
author = "{{ author_name }}"
email = "{{ author_email }}"
license = "MIT"
primary_language = "runa"
supported_languages = ["runa"{% for lang in target_languages %}, "{{ lang }}"{% endfor %}]

{% for lang in target_languages %}
[targets.{{ lang }}]
tier = 1
{% if lang == "python" %}
version = "3.8+"
features = ["type_hints"]
{% elif lang == "javascript" %}
version = "es2020+"
features = ["modules"]
{% elif lang == "typescript" %}
version = "4.0+"
features = ["strict"]
{% elif lang == "java" %}
version = "11+"
features = ["generics"]
{% elif lang == "cpp" %}
version = "17+"
features = ["modern_cpp"]
{% endif %}

{% endfor %}

[build]
entry-point = "src/main.runa"
build-scripts = [
    {% for lang in target_languages %}"runa compile --target {{ lang }}"{% if not loop.last %},{% endif %}
    {% endfor %}
]

[scripts]
build-all = "runa build --languages {% for lang in target_languages %}{{ lang }}{% if not loop.last %} {% endif %}{% endfor %}"
test-all = "runa test --all-languages"
''',
                "src/main.runa": '''Note: Universal library main module
Note: This library provides core functionality across multiple languages

Export MathUtils, StringUtils, DataStructures

Module "MathUtils" with:
    Process called "add" that takes a as Number and b as Number returns Number:
        Return a plus b
    
    Process called "multiply" that takes a as Number and b as Number returns Number:
        Return a times b
    
    Process called "power" that takes base as Number and exponent as Integer returns Number:
        Return base to the power of exponent

Module "StringUtils" with:
    Process called "capitalize" that takes text as String returns String:
        If text is empty:
            Return text
        Otherwise:
            Let first char be text substring from 0 to 1 to upper case
            Let rest be text substring from 1
            Return first char followed by rest
    
    Process called "reverse" that takes text as String returns String:
        Let result be ""
        For each char in text:
            Set result to char followed by result
        Return result

Module "DataStructures" with:
    Process called "create stack" returns Stack:
        Return new Stack
    
    Process called "create queue" returns Queue:
        Return new Queue
'''
            },
            tags=["universal", "multi-language", "library"]
        )
    
    # Additional template creation methods for other language tiers...
    
    def _create_typescript_library_template(self) -> ProjectTemplate:
        """Create TypeScript library template."""
        # Implementation similar to above patterns
        pass
    
    def _create_cpp_application_template(self) -> ProjectTemplate:
        """Create C++ application template."""
        # Implementation for C++ projects
        pass
    
    def _create_java_application_template(self) -> ProjectTemplate:
        """Create Java application template."""
        # Implementation for Java projects
        pass
    
    def _create_rust_crate_template(self) -> ProjectTemplate:
        """Create Rust crate template."""
        # Implementation for Rust projects
        pass
    
    def _create_go_module_template(self) -> ProjectTemplate:
        """Create Go module template."""
        # Implementation for Go projects
        pass
    
    def _create_web_component_template(self) -> ProjectTemplate:
        """Create web component template."""
        # Implementation for web components
        pass
    
    def _create_config_package_template(self) -> ProjectTemplate:
        """Create configuration package template."""
        # Implementation for config packages
        pass
    
    def _create_cross_platform_app_template(self) -> ProjectTemplate:
        """Create cross-platform application template."""
        # Implementation for cross-platform apps
        pass


def main():
    """CLI entry point for project templates."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runa Project Template Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List templates
    list_parser = subparsers.add_parser('list', help='List available templates')
    list_parser.add_argument('--tier', type=int, help='Filter by language tier')
    list_parser.add_argument('--language', help='Filter by language')
    
    # Show template info
    info_parser = subparsers.add_parser('info', help='Show template information')
    info_parser.add_argument('template', help='Template name')
    
    # Create project
    create_parser = subparsers.add_parser('create', help='Create new project from template')
    create_parser.add_argument('template', help='Template name')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('--dir', default='.', help='Project directory')
    create_parser.add_argument('--var', action='append', help='Template variables (key=value)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    manager = ProjectTemplateManager()
    
    if args.command == 'list':
        templates = manager.list_templates()
        
        # Apply filters
        if args.tier:
            templates = [t for t in templates if t['language_tier'] == args.tier]
        if args.language:
            templates = [t for t in templates if args.language in t['supported_languages']]
        
        if templates:
            print(f"Available templates ({len(templates)}):")
            for template in templates:
                languages = ', '.join(template['supported_languages'][:3])
                if len(template['supported_languages']) > 3:
                    languages += f" (+{len(template['supported_languages'])-3} more)"
                
                print(f"  {template['name']} (Tier {template['language_tier']})")
                print(f"    {template['description']}")
                print(f"    Languages: {languages}")
                print()
        else:
            print("No templates found matching criteria")
    
    elif args.command == 'info':
        info = manager.get_template_info(args.template)
        if info:
            print(f"Template: {info['name']}")
            print(f"Description: {info['description']}")
            print(f"Language Tier: {info['language_tier']}")
            print(f"Primary Language: {info['primary_language']}")
            print(f"Supported Languages: {', '.join(info['supported_languages'])}")
            print(f"Version: {info['version']}")
            print(f"Author: {info['author']}")
            print(f"License: {info['license']}")
            print(f"Files: {info['file_count']}")
            print(f"Directories: {info['directory_count']}")
            
            if info['variables']:
                print("\nTemplate Variables:")
                for var in info['variables']:
                    required = "required" if var['required'] else "optional"
                    default = f" (default: {var['default_value']})" if var['default_value'] is not None else ""
                    print(f"  {var['name']} ({var['type']}, {required}){default}")
                    print(f"    {var['description']}")
        else:
            print(f"Template '{args.template}' not found")
            return 1
    
    elif args.command == 'create':
        # Parse variables
        variables = {}
        if args.var:
            for var_str in args.var:
                if '=' in var_str:
                    key, value = var_str.split('=', 1)
                    # Try to parse as JSON for complex types
                    try:
                        variables[key] = json.loads(value)
                    except json.JSONDecodeError:
                        variables[key] = value
        
        project_dir = os.path.join(args.dir, args.name)
        success = manager.create_project(args.template, args.name, project_dir, variables)
        
        if success:
            print(f"\nNext steps:")
            print(f"  cd {project_dir}")
            print(f"  runa package install")
            print(f"  runa build")
            return 0
        else:
            return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())