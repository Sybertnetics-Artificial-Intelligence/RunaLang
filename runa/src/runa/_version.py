"""Version information for Runa Programming Language."""

__version__ = "0.1.0"
__version_info__ = (0, 1, 0)

# Version history and milestones
VERSION_HISTORY = {
    "0.1.0": "Initial development version - Phase 1 Week 1",
}

def get_version() -> str:
    """Get the current version string."""
    return __version__

def get_version_info() -> tuple[int, int, int]:
    """Get the current version as a tuple."""
    return __version_info__ 