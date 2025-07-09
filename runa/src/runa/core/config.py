"""
Runa Configuration Management System

Provides centralized configuration management for the Runa language toolchain.
Supports environment variables, configuration files, and runtime settings.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""
    pass


class LogLevel(Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class CompilerConfig:
    """Compiler configuration settings."""
    target_language: str = "python"
    optimize_code: bool = True
    debug_symbols: bool = False
    strict_types: bool = True
    allow_unsafe_operations: bool = False
    max_errors: int = 50
    max_warnings: int = 100
    target_python_version: str = "3.9"


@dataclass
class LSPConfig:
    """Language Server Protocol configuration."""
    enabled: bool = True
    port: int = 8080
    host: str = "localhost"
    max_clients: int = 10
    completion_enabled: bool = True
    hover_enabled: bool = True
    diagnostics_enabled: bool = True
    formatting_enabled: bool = True
    signature_help_enabled: bool = True


@dataclass
class IDEConfig:
    """IDE integration configuration."""
    vscode_extension_enabled: bool = True
    intellij_plugin_enabled: bool = True
    syntax_highlighting: bool = True
    auto_completion: bool = True
    error_squiggles: bool = True
    code_folding: bool = True
    bracket_matching: bool = True


@dataclass
class PackageConfig:
    """Package manager configuration."""
    registry_url: str = "https://packages.runa-lang.org"
    cache_directory: str = "~/.runa/cache"
    install_directory: str = "~/.runa/packages"
    auto_update: bool = False
    verify_signatures: bool = True
    timeout_seconds: int = 30


@dataclass
class RuntimeConfig:
    """Runtime configuration settings."""
    garbage_collection: bool = True
    memory_limit_mb: int = 1024
    stack_size_mb: int = 8
    max_recursion_depth: int = 1000
    async_enabled: bool = True
    concurrency_limit: int = 100


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: LogLevel = LogLevel.INFO
    log_to_file: bool = False
    log_file: str = "runa.log"
    log_to_console: bool = True
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    max_file_size_mb: int = 10
    backup_count: int = 5
    colored_output: bool = True


@dataclass
class RunaConfig:
    """Main Runa configuration containing all subsystem configs."""
    compiler: CompilerConfig = None
    lsp: LSPConfig = None
    ide: IDEConfig = None
    package: PackageConfig = None
    runtime: RuntimeConfig = None
    logging: LoggingConfig = None
    
    def __post_init__(self):
        """Initialize sub-configs if not provided."""
        if self.compiler is None:
            self.compiler = CompilerConfig()
        if self.lsp is None:
            self.lsp = LSPConfig()
        if self.ide is None:
            self.ide = IDEConfig()
        if self.package is None:
            self.package = PackageConfig()
        if self.runtime is None:
            self.runtime = RuntimeConfig()
        if self.logging is None:
            self.logging = LoggingConfig()


class ConfigManager:
    """Manages Runa configuration from multiple sources."""
    
    def __init__(self):
        self.config = RunaConfig()
        self._config_paths = [
            "runa.json",
            "runa.yaml", 
            "runa.yml",
            os.path.expanduser("~/.runa/config.json"),
            os.path.expanduser("~/.runa/config.yaml"),
            "/etc/runa/config.json"
        ]
    
    def load_config(self, config_path: Optional[str] = None) -> RunaConfig:
        """Load configuration from files and environment variables."""
        # Start with defaults
        self.config = RunaConfig()
        
        # Load from configuration files
        if config_path:
            self._load_config_file(config_path)
        else:
            self._load_default_config_files()
        
        # Override with environment variables
        self._load_environment_variables()
        
        # Validate configuration
        self._validate_config()
        
        return self.config
    
    def _load_default_config_files(self):
        """Load configuration from default file locations."""
        for path in self._config_paths:
            if os.path.exists(path):
                try:
                    self._load_config_file(path)
                    break  # Use first found config file
                except Exception as e:
                    print(f"Warning: Failed to load config from {path}: {e}")
    
    def _load_config_file(self, path: str):
        """Load configuration from a specific file."""
        path = os.path.expanduser(path)
        
        if not os.path.exists(path):
            raise ConfigError(f"Configuration file not found: {path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.endswith(('.yaml', '.yml')):
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            self._merge_config_data(config_data)
            
        except Exception as e:
            raise ConfigError(f"Failed to load configuration from {path}: {e}")
    
    def _merge_config_data(self, config_data: Dict[str, Any]):
        """Merge configuration data into current config."""
        if not isinstance(config_data, dict):
            return
        
        # Merge compiler config
        if 'compiler' in config_data:
            self._merge_section(self.config.compiler, config_data['compiler'])
        
        # Merge LSP config
        if 'lsp' in config_data:
            self._merge_section(self.config.lsp, config_data['lsp'])
        
        # Merge IDE config
        if 'ide' in config_data:
            self._merge_section(self.config.ide, config_data['ide'])
        
        # Merge package config
        if 'package' in config_data:
            self._merge_section(self.config.package, config_data['package'])
        
        # Merge runtime config
        if 'runtime' in config_data:
            self._merge_section(self.config.runtime, config_data['runtime'])
        
        # Merge logging config
        if 'logging' in config_data:
            logging_data = config_data['logging']
            # Handle LogLevel enum
            if 'level' in logging_data:
                if isinstance(logging_data['level'], str):
                    logging_data['level'] = LogLevel(logging_data['level'].upper())
            self._merge_section(self.config.logging, logging_data)
    
    def _merge_section(self, config_section: Any, data: Dict[str, Any]):
        """Merge data into a configuration section."""
        for key, value in data.items():
            if hasattr(config_section, key):
                setattr(config_section, key, value)
    
    def _load_environment_variables(self):
        """Load configuration from environment variables."""
        env_mappings = {
            # Compiler settings
            'RUNA_TARGET_LANGUAGE': ('compiler', 'target_language'),
            'RUNA_OPTIMIZE': ('compiler', 'optimize_code', bool),
            'RUNA_DEBUG_SYMBOLS': ('compiler', 'debug_symbols', bool),
            'RUNA_STRICT_TYPES': ('compiler', 'strict_types', bool),
            
            # LSP settings
            'RUNA_LSP_PORT': ('lsp', 'port', int),
            'RUNA_LSP_HOST': ('lsp', 'host'),
            'RUNA_LSP_ENABLED': ('lsp', 'enabled', bool),
            
            # Package settings
            'RUNA_REGISTRY_URL': ('package', 'registry_url'),
            'RUNA_CACHE_DIR': ('package', 'cache_directory'),
            'RUNA_INSTALL_DIR': ('package', 'install_directory'),
            
            # Runtime settings
            'RUNA_MEMORY_LIMIT': ('runtime', 'memory_limit_mb', int),
            'RUNA_STACK_SIZE': ('runtime', 'stack_size_mb', int),
            
            # Logging settings
            'RUNA_LOG_LEVEL': ('logging', 'level', lambda x: LogLevel(x.upper())),
            'RUNA_LOG_FILE': ('logging', 'log_file'),
            'RUNA_LOG_TO_CONSOLE': ('logging', 'log_to_console', bool),
        }
        
        for env_var, config_info in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                section_name, attr_name = config_info[:2]
                converter = config_info[2] if len(config_info) > 2 else str
                
                try:
                    if converter == bool:
                        converted_value = value.lower() in ('true', '1', 'yes', 'on')
                    elif converter == int:
                        converted_value = int(value)
                    elif callable(converter):
                        converted_value = converter(value)
                    else:
                        converted_value = value
                    
                    section = getattr(self.config, section_name)
                    setattr(section, attr_name, converted_value)
                    
                except (ValueError, TypeError) as e:
                    print(f"Warning: Invalid value for {env_var}: {value} ({e})")
    
    def _validate_config(self):
        """Validate the loaded configuration."""
        errors = []
        
        # Validate compiler config
        if self.config.compiler.max_errors < 1:
            errors.append("Compiler max_errors must be at least 1")
        
        if self.config.compiler.target_language not in ['python', 'javascript', 'cpp']:
            errors.append(f"Unsupported target language: {self.config.compiler.target_language}")
        
        # Validate LSP config
        if not (1 <= self.config.lsp.port <= 65535):
            errors.append("LSP port must be between 1 and 65535")
        
        if self.config.lsp.max_clients < 1:
            errors.append("LSP max_clients must be at least 1")
        
        # Validate runtime config
        if self.config.runtime.memory_limit_mb < 64:
            errors.append("Runtime memory_limit_mb must be at least 64MB")
        
        if self.config.runtime.stack_size_mb < 1:
            errors.append("Runtime stack_size_mb must be at least 1MB")
        
        # Validate logging config
        if self.config.logging.max_file_size_mb < 1:
            errors.append("Logging max_file_size_mb must be at least 1MB")
        
        if errors:
            raise ConfigError(f"Configuration validation failed: {'; '.join(errors)}")
    
    def save_config(self, path: str, format: str = 'json'):
        """Save current configuration to file."""
        path = os.path.expanduser(path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Convert config to dictionary
        config_dict = {
            'compiler': asdict(self.config.compiler),
            'lsp': asdict(self.config.lsp),
            'ide': asdict(self.config.ide),
            'package': asdict(self.config.package),
            'runtime': asdict(self.config.runtime),
            'logging': {
                **asdict(self.config.logging),
                'level': self.config.logging.level.value
            }
        }
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                if format.lower() in ['yaml', 'yml']:
                    yaml.dump(config_dict, f, indent=2, default_flow_style=False)
                else:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            raise ConfigError(f"Failed to save configuration to {path}: {e}")
    
    def get_config(self) -> RunaConfig:
        """Get the current configuration."""
        return self.config
    
    def update_config(self, **kwargs):
        """Update configuration programmatically."""
        for section_name, section_data in kwargs.items():
            if hasattr(self.config, section_name):
                section = getattr(self.config, section_name)
                for key, value in section_data.items():
                    if hasattr(section, key):
                        setattr(section, key, value)


# Global configuration manager instance
config_manager = ConfigManager()


def get_config() -> RunaConfig:
    """Get the global Runa configuration."""
    return config_manager.get_config()


def load_config(config_path: Optional[str] = None) -> RunaConfig:
    """Load configuration from file or defaults."""
    return config_manager.load_config(config_path)


def save_config(path: str, format: str = 'json'):
    """Save current configuration to file."""
    config_manager.save_config(path, format)


def update_config(**kwargs):
    """Update configuration programmatically."""
    config_manager.update_config(**kwargs)