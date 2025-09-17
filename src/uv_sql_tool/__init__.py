"""
UV SQL Tool - Package initialization.
Provides main entry points and exports for MCP server and CLI usage.
"""

__version__ = "0.1.0"
__author__ = "Varun Shah"
__email__ = "varun.shah@sunrise.co"

# Export main components for CLI and MCP server
from .cli import main as cli_main
from .server import create_app
from .config import SQLServerConfig, get_sql_config, create_sample_config

__all__ = ["cli_main", "create_app", "SQLServerConfig", "get_sql_config", "create_sample_config", "__version__"]