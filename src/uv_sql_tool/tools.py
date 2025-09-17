import json
import os


class Tool:
    def __init__(self, name: str, description: str, input_schema: dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema


def get_sql_config_schema():
    """Get the SQL configuration schema for tools."""
    return {
        "server": {
            "type": "string",
            "description": "SQL Server name (e.g., server.database.windows.net)"
        },
        "database": {
            "type": "string", 
            "description": "Database name"
        },
        "username": {
            "type": "string",
            "description": "Username for authentication"
        },
        "password": {
            "type": "string",
            "description": "Password for authentication"
        },
        "config_file": {
            "type": "string",
            "description": "Path to JSON configuration file"
        },
        "trusted_connection": {
            "type": "boolean",
            "description": "Use Windows authentication (default: false)"
        },
        "encrypt": {
            "type": "boolean", 
            "description": "Use encrypted connection (default: true)"
        }
    }


ALL_SQL_TOOLS = [
    Tool(
        name="create_table",
        description="Creates a new table in the database with configurable SQL Server connection.",
        input_schema={
            "type": "object",
            "properties": {
                "csv_file_path": {
                    "type": "string",
                    "description": "Path to the CSV file containing data for the table."
                },
                "table_name": {
                    "type": "string",
                    "description": "Name of the table to be created."
                },
                **get_sql_config_schema()
            },
            "required": ["csv_file_path", "table_name"]
        }
    ),
    Tool(
        name="create_stored_procedure", 
        description="Generates a stored procedure based on the provided parameters.",
        input_schema={
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Name of the table for which the stored procedure is created."
                },
                "dictionary_path": {
                    "type": "string",
                    "description": "Path to the dictionary file for the stored procedure."
                },
                "reference_sp_path": {
                    "type": "string",
                    "description": "Path to the reference stored procedure."
                },
                **get_sql_config_schema()
            },
            "required": ["table_name", "dictionary_path", "reference_sp_path"]
        }
    )
]

SQL_TOOLS_BY_NAME = {tool.name: tool for tool in ALL_SQL_TOOLS}


def load_mcp_config(config_path="mcp.json"):
    """Load MCP configuration from a JSON file."""
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}