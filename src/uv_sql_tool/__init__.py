"""UV SQL Tool - A tool for migrating legacy data into Dynamics Finance & Operations."""

__version__ = "0.1.0"
__author__ = "Varun Shah"
__email__ = "varun.shah@sunrise.co"

# Export main components
from .cli import main as cli_main
from .server import create_app
from .config import SQLServerConfig, get_sql_config, create_sample_config

__all__ = ["cli_main", "create_app", "SQLServerConfig", "get_sql_config", "create_sample_config", "__version__"]