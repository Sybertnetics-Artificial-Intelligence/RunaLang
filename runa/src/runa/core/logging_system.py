"""
Runa Logging System

Provides comprehensive logging capabilities for the Runa language toolchain.
Supports file logging, console logging, structured logging, and log rotation.
"""

import logging
import logging.handlers
import os
import sys
import json
import traceback
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    Fore = Back = Style = None

from .config import get_config, LogLevel


@dataclass
class LogEntry:
    """Structured log entry."""
    timestamp: datetime
    level: str
    logger_name: str
    message: str
    module: Optional[str] = None
    function: Optional[str] = None
    line_number: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None
    exception_info: Optional[str] = None


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for better readability."""
    
    def __init__(self, fmt=None, datefmt=None, use_colors=True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors and COLORS_AVAILABLE
        
        if self.use_colors:
            self.level_colors = {
                'DEBUG': Fore.CYAN,
                'INFO': Fore.GREEN,
                'WARNING': Fore.YELLOW,
                'ERROR': Fore.RED,
                'CRITICAL': Fore.RED + Back.WHITE,
            }
    
    def format(self, record):
        if self.use_colors and record.levelname in self.level_colors:
            # Save original values
            original_levelname = record.levelname
            original_message = record.getMessage()
            
            # Apply colors
            color = self.level_colors[record.levelname]
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
            
            # Format with colors
            formatted = super().format(record)
            
            # Restore original values
            record.levelname = original_levelname
            record.msg = original_message
            
            return formatted
        else:
            return super().format(record)


class StructuredFormatter(logging.Formatter):
    """JSON structured formatter for machine-readable logs."""
    
    def format(self, record):
        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created),
            level=record.levelname,
            logger_name=record.name,
            message=record.getMessage(),
            module=getattr(record, 'module', None),
            function=getattr(record, 'funcName', None),
            line_number=getattr(record, 'lineno', None),
            extra_data=getattr(record, 'extra_data', None),
            exception_info=self.formatException(record.exc_info) if record.exc_info else None
        )
        
        # Convert to dictionary and then to JSON
        log_dict = asdict(log_entry)
        log_dict['timestamp'] = log_entry.timestamp.isoformat()
        
        return json.dumps(log_dict, ensure_ascii=False)


class RunaLogger:
    """Enhanced logger for Runa with context management."""
    
    def __init__(self, name: str, logger: logging.Logger = None):
        self.name = name
        self.logger = logger or logging.getLogger(name)
        self._context: Dict[str, Any] = {}
    
    def set_context(self, **kwargs):
        """Set logging context that will be included in all log messages."""
        self._context.update(kwargs)
    
    def clear_context(self):
        """Clear the logging context."""
        self._context.clear()
    
    def _log_with_context(self, level: int, message: str, *args, **kwargs):
        """Log message with context information."""
        extra = kwargs.pop('extra', {})
        extra.update({
            'extra_data': {**self._context, **extra.get('extra_data', {})}
        })
        kwargs['extra'] = extra
        
        self.logger.log(level, message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self._log_with_context(logging.DEBUG, message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self._log_with_context(logging.INFO, message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self._log_with_context(logging.WARNING, message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self._log_with_context(logging.ERROR, message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self._log_with_context(logging.CRITICAL, message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback."""
        kwargs['exc_info'] = True
        self.error(message, *args, **kwargs)
    
    def log_compilation_phase(self, phase: str, file_path: str, duration_ms: float):
        """Log compilation phase completion."""
        self.info(f"Compilation phase '{phase}' completed for {file_path} in {duration_ms:.2f}ms",
                 extra={'extra_data': {
                     'phase': phase,
                     'file_path': file_path,
                     'duration_ms': duration_ms,
                     'event_type': 'compilation_phase'
                 }})
    
    def log_semantic_error(self, error_type: str, message: str, line: int, column: int, file_path: str):
        """Log semantic analysis error."""
        self.error(f"Semantic error ({error_type}) at {file_path}:{line}:{column}: {message}",
                  extra={'extra_data': {
                      'error_type': error_type,
                      'line': line,
                      'column': column,
                      'file_path': file_path,
                      'event_type': 'semantic_error'
                  }})
    
    def log_lsp_request(self, method: str, params: Dict[str, Any], duration_ms: float):
        """Log LSP request processing."""
        self.debug(f"LSP request '{method}' processed in {duration_ms:.2f}ms",
                  extra={'extra_data': {
                      'method': method,
                      'params': params,
                      'duration_ms': duration_ms,
                      'event_type': 'lsp_request'
                  }})
    
    def log_package_operation(self, operation: str, package_name: str, version: str, success: bool):
        """Log package manager operation."""
        level = self.info if success else self.error
        status = "succeeded" if success else "failed"
        level(f"Package {operation} for '{package_name}' v{version} {status}",
              extra={'extra_data': {
                  'operation': operation,
                  'package_name': package_name,
                  'version': version,
                  'success': success,
                  'event_type': 'package_operation'
              }})


class LoggingSystem:
    """Central logging system for Runa."""
    
    def __init__(self):
        self.loggers: Dict[str, RunaLogger] = {}
        self.configured = False
    
    def configure(self, config=None):
        """Configure the logging system."""
        if config is None:
            config = get_config().logging
        
        # Clear existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Set root logging level
        level = getattr(logging, config.level.value)
        root_logger.setLevel(level)
        
        # Configure console logging
        if config.log_to_console:
            self._setup_console_logging(config)
        
        # Configure file logging
        if config.log_to_file:
            self._setup_file_logging(config)
        
        self.configured = True
    
    def _setup_console_logging(self, config):
        """Set up console logging handler."""
        console_handler = logging.StreamHandler(sys.stdout)
        
        if config.colored_output:
            formatter = ColoredFormatter(
                fmt=config.format_string,
                use_colors=True
            )
        else:
            formatter = logging.Formatter(config.format_string)
        
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
    
    def _setup_file_logging(self, config):
        """Set up file logging with rotation."""
        log_file = os.path.expanduser(config.log_file)
        log_dir = os.path.dirname(log_file)
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=config.max_file_size_mb * 1024 * 1024,
            backupCount=config.backup_count
        )
        
        # Use structured formatter for file logging
        formatter = StructuredFormatter()
        file_handler.setFormatter(formatter)
        
        logging.getLogger().addHandler(file_handler)
    
    def get_logger(self, name: str) -> RunaLogger:
        """Get or create a logger with the given name."""
        if not self.configured:
            self.configure()
        
        if name not in self.loggers:
            logger = logging.getLogger(name)
            self.loggers[name] = RunaLogger(name, logger)
        
        return self.loggers[name]
    
    def set_global_context(self, **kwargs):
        """Set context for all loggers."""
        for logger in self.loggers.values():
            logger.set_context(**kwargs)
    
    def clear_global_context(self):
        """Clear context for all loggers."""
        for logger in self.loggers.values():
            logger.clear_context()
    
    def flush_logs(self):
        """Flush all log handlers."""
        for handler in logging.getLogger().handlers:
            handler.flush()
    
    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """Log performance metrics."""
        perf_logger = self.get_logger('runa.performance')
        perf_logger.info("Performance metrics collected",
                        extra={'extra_data': {
                            'metrics': metrics,
                            'event_type': 'performance_metrics'
                        }})
    
    def log_system_info(self):
        """Log system information at startup."""
        import platform
        import sys
        
        system_logger = self.get_logger('runa.system')
        system_info = {
            'platform': platform.platform(),
            'python_version': sys.version,
            'architecture': platform.architecture(),
            'processor': platform.processor(),
            'hostname': platform.node(),
        }
        
        system_logger.info("Runa system started",
                          extra={'extra_data': {
                              'system_info': system_info,
                              'event_type': 'system_startup'
                          }})


# Global logging system instance
logging_system = LoggingSystem()


def get_logger(name: str) -> RunaLogger:
    """Get a logger for the given name."""
    return logging_system.get_logger(name)


def configure_logging(config=None):
    """Configure the global logging system."""
    logging_system.configure(config)


def set_global_context(**kwargs):
    """Set global logging context."""
    logging_system.set_global_context(**kwargs)


def clear_global_context():
    """Clear global logging context."""
    logging_system.clear_global_context()


def flush_logs():
    """Flush all log handlers."""
    logging_system.flush_logs()


# Convenience function for common loggers
def get_compiler_logger() -> RunaLogger:
    """Get logger for compiler operations."""
    return get_logger('runa.compiler')


def get_lsp_logger() -> RunaLogger:
    """Get logger for LSP operations."""
    return get_logger('runa.lsp')


def get_package_logger() -> RunaLogger:
    """Get logger for package manager operations."""
    return get_logger('runa.package')


def get_runtime_logger() -> RunaLogger:
    """Get logger for runtime operations."""
    return get_logger('runa.runtime')


# Error handling utilities
def log_unhandled_exception(exc_type, exc_value, exc_traceback):
    """Log unhandled exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_logger = get_logger('runa.error')
    error_logger.critical(
        f"Unhandled exception: {exc_type.__name__}: {exc_value}",
        extra={'extra_data': {
            'exception_type': exc_type.__name__,
            'exception_value': str(exc_value),
            'traceback': ''.join(traceback.format_tb(exc_traceback)),
            'event_type': 'unhandled_exception'
        }}
    )


def setup_exception_logging():
    """Set up logging for unhandled exceptions."""
    sys.excepthook = log_unhandled_exception


# Context managers
class LoggingContext:
    """Context manager for temporary logging context."""
    
    def __init__(self, logger: RunaLogger, **kwargs):
        self.logger = logger
        self.context = kwargs
        self.old_context = {}
    
    def __enter__(self):
        # Save current context
        self.old_context = self.logger._context.copy()
        # Set new context
        self.logger.set_context(**self.context)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore old context
        self.logger._context = self.old_context


def with_logging_context(logger: RunaLogger, **kwargs):
    """Create a logging context manager."""
    return LoggingContext(logger, **kwargs)