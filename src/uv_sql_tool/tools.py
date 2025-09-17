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
        description="Creates a new table in the database by analyzing a pipe-delimited text file. Automatically detects column names and data types from the file content. Table names are automatically prefixed with 'src'.",
        input_schema={
            "type": "object",
            "properties": {
                "csv_file_path": {
                    "type": "string",
                    "description": "Path to the pipe-delimited text file containing data for the table. The first row should contain column headers."
                },
                "table_name": {
                    "type": "string",
                    "description": "Name of the table to be created (will be automatically prefixed with 'src'). The table structure will be generated based on the file content."
                },
                **get_sql_config_schema()
            },
            "required": ["csv_file_path", "table_name"]
        }
    ),
    Tool(
        name="create_stored_procedure", 
        description="Generates a stored procedure that creates a staging table and maps columns from a source table using a dictionary/mapping file. The procedure reads Spanish column names from the source table and maps them to English column names in the staging table. Stored procedure names are automatically prefixed with 'stg'. Reference stored procedure path is optional.",
        input_schema={
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Name of the table for which the stored procedure is created (procedure will be automatically prefixed with 'stg')."
                },
                "dictionary_path": {
                    "type": "string",
                    "description": "Path to the CSV or pipe-delimited dictionary/mapping file containing column mappings. Expected columns: 'SGE Column Name' (Spanish), 'English Column Name', and 'Field type'."
                },
                "reference_sp_path": {
                    "type": "string",
                    "description": "Optional path to the reference stored procedure for template reference."
                },
                **get_sql_config_schema()
            },
            "required": ["table_name", "dictionary_path"]
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