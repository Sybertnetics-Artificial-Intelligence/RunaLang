"""
Runa Language Toolchain Registration

This module provides the complete Runa language toolchain for the
hub-and-spoke translation system. Since Runa is the central hub language,
it has special handling in the pipeline.
"""

from .runa_parser import RunaParser, RUNA_LANGUAGE_INFO
from .runa_generator import RunaGenerator

# Create instances
runa_parser = RunaParser()
runa_generator = RunaGenerator()

def register_runa_toolchain():
    """Register the Runa toolchain with the global pipeline."""
    from ...core.pipeline import get_pipeline
    from ...core.base_components import register_language_info
    
    # Register language info
    register_language_info(RUNA_LANGUAGE_INFO)
    
    # Register with pipeline (special handling for Runa as the hub)
    pipeline = get_pipeline()
    pipeline.register_runa_toolchain(runa_parser, runa_generator)
    
    return {
        "parser": runa_parser,
        "generator": runa_generator,
        "language_info": RUNA_LANGUAGE_INFO
    }

# Auto-register when module is imported
_toolchain = register_runa_toolchain()

# Export public interface
__all__ = [
    "RunaParser",
    "RunaGenerator", 
    "runa_parser",
    "runa_generator",
    "RUNA_LANGUAGE_INFO",
    "register_runa_toolchain"
]