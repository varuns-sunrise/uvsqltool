"""MCP server entrypoint for uv_sql_tool (for Copilot Workspace)."""

import sys
import json
import os
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .tools import ALL_SQL_TOOLS, SQL_TOOLS_BY_NAME, load_mcp_config
from .schema_generator import generate_create_table_sql, execute_sql_on_azure, generate_stored_procedure

try:
    from mcp.server import Server
    from mcp.types import TextContent, Tool
except ImportError:
    print("MCP library not installed. Running in standalone mode.", file=sys.stderr)
    Server = None
    Tool = None
    TextContent = None

def create_app():
    class UVSQLToolMCPServer:
        def __init__(self):
            self.logger = logging.getLogger(__name__)
            self.mcp_config = load_mcp_config()
            if Server:
                self.app = Server("uv-sql-tool-mcp-server")
                self._setup_handlers()
            else:
                self.app = None

        def _setup_handlers(self):
            if not self.app:
                return
            import traceback
            @self.app.list_tools()
            async def handle_list_tools() -> list:
                try:
                    return [
                        Tool(
                            name=tool.name,
                            description=tool.description,
                            inputSchema=tool.input_schema
                        )
                        for tool in ALL_SQL_TOOLS
                    ]
                except Exception as e:
                    self.logger.error(f"Exception in handle_list_tools: {e}\n{traceback.format_exc()}")
                    raise

            @self.app.call_tool()
            async def handle_call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> list:
                try:
                    result = await self._execute_tool(name, arguments or {})
                    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
                except Exception as e:
                    self.logger.error(f"Exception in handle_call_tool: {e}\n{traceback.format_exc()}")
                    error_msg = f"Error executing {name}: {str(e)}"
                    return [TextContent(type="text", text=error_msg)]

        async def _execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
            if name not in SQL_TOOLS_BY_NAME:
                raise ValueError(f"Unknown tool: {name}")
            
            # Check if execution should be skipped (from environment variable or config file)
            skip_execution_env = os.getenv("SKIP_EXECUTION", "")
            skip_execution_config = self.mcp_config.get("skip_execution", False)
            skip_execution = (
                skip_execution_env.lower() in ["true", "1", "yes", "on"] or 
                skip_execution_config
            )
            
            # Log configuration for debugging
            self.logger.info(f"SKIP_EXECUTION env var: '{skip_execution_env}'")
            self.logger.info(f"skip_execution from config: {skip_execution_config}")
            self.logger.info(f"Final skip_execution decision: {skip_execution}")
            
            if skip_execution:
                self.logger.info(f"Skipping execution for tool: {name}")
            else:
                self.logger.info(f"Executing tool: {name}")
            
            # Extract SQL config from arguments if provided
            from .config import get_sql_config
            sql_config = None
            if any(key in arguments for key in ['server', 'database', 'username', 'password', 'config_file']):
                sql_config = get_sql_config(
                    config_path=arguments.get('config_file'),
                    server=arguments.get('server'),
                    database=arguments.get('database'),
                    username=arguments.get('username'),
                    password=arguments.get('password'),
                    trusted_connection=arguments.get('trusted_connection', False),
                    encrypt=arguments.get('encrypt', True)
                )
            
            if name == "create_table":
                sql = generate_create_table_sql(arguments["csv_file_path"], arguments["table_name"])
                if skip_execution:
                    # Save SQL to file even when skipping execution
                    # Create generated_sql folder if it doesn't exist
                    sql_folder = Path("generated_sql")
                    sql_folder.mkdir(exist_ok=True)
                    
                    # Use prefixed table name for file naming
                    table_name = arguments["table_name"]
                    prefixed_table_name = f"src{table_name}" if not table_name.startswith("src") else table_name
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    sql_filename = sql_folder / f"{prefixed_table_name}_create_table_{timestamp}.sql"
                    
                    try:
                        with open(sql_filename, 'w', encoding='utf-8') as f:
                            f.write(f"-- Generated SQL for table: {prefixed_table_name}\n")
                            f.write(f"-- Generated at: {datetime.now().isoformat()}\n")
                            f.write(f"-- Source CSV: {arguments['csv_file_path']}\n")
                            f.write(f"-- SKIP_EXECUTION was enabled, SQL not executed\n\n")
                            f.write(sql)
                        return {
                            "message": f"Table '{prefixed_table_name}' creation skipped (skip_execution=True). SQL saved to {sql_filename}.",
                            "sql": sql,
                            "sql_file": str(sql_filename),
                            "skipped": True,
                            "debug": {
                                "skip_execution_env": skip_execution_env,
                                "skip_execution_config": skip_execution_config,
                                "final_skip_execution": skip_execution
                            }
                        }
                    except Exception as e:
                        return {
                            "message": f"Table '{prefixed_table_name}' creation skipped (skip_execution=True). Warning: Could not save SQL file: {str(e)}",
                            "sql": sql,
                            "skipped": True,
                            "error": str(e),
                            "debug": {
                                "skip_execution_env": skip_execution_env,
                                "skip_execution_config": skip_execution_config,
                                "final_skip_execution": skip_execution
                            }
                        }
                execute_sql_on_azure(sql, config=sql_config)
                # Use prefixed table name in success message too
                table_name = arguments["table_name"]
                prefixed_table_name = f"src{table_name}" if not table_name.startswith("src") else table_name
                return {"message": f"Table '{prefixed_table_name}' created successfully."}
            elif name == "create_stored_procedure":
                result = generate_stored_procedure(
                    arguments["table_name"],
                    arguments["dictionary_path"],
                    arguments.get("reference_sp_path")  # Use .get() to handle optional parameter
                )
                if skip_execution:
                    # Save stored procedure to file even when skipping execution
                    # Create generated_sql folder if it doesn't exist
                    sql_folder = Path("generated_sql")
                    sql_folder.mkdir(exist_ok=True)
                    
                    # Use the actual stored procedure name for file naming
                    table_name = arguments["table_name"]
                    prefixed_sp_name = f"stg{table_name}" if not table_name.startswith("stg") else table_name
                    # File name should match the stored procedure name: stgTableName_StoredProcedure.sql
                    sp_filename = sql_folder / f"{prefixed_sp_name}_StoredProcedure.sql"
                    
                    try:
                        with open(sp_filename, 'w', encoding='utf-8') as f:
                            f.write(f"-- Generated stored procedure for table: {arguments['table_name']}\n")
                            f.write(f"-- Stored procedure name: {prefixed_sp_name}_StoredProcedure\n")
                            f.write(f"-- Generated at: {datetime.now().isoformat()}\n")
                            f.write(f"-- Dictionary path: {arguments['dictionary_path']}\n")
                            reference_sp = arguments.get('reference_sp_path')
                            f.write(f"-- Reference SP path: {reference_sp if reference_sp else 'Not provided'}\n")
                            f.write(f"-- SKIP_EXECUTION was enabled, procedure not executed\n\n")
                            f.write(str(result))  # Convert result to string if needed
                        return {
                            "message": f"Stored procedure '{prefixed_sp_name}_StoredProcedure' creation skipped (skip_execution=True). SQL saved to {sp_filename}.",
                            "procedure": result,
                            "sql_file": str(sp_filename),
                            "skipped": True,
                            "debug": {
                                "skip_execution_env": skip_execution_env,
                                "skip_execution_config": skip_execution_config,
                                "final_skip_execution": skip_execution
                            }
                        }
                    except Exception as e:
                        return {
                            "message": f"Stored procedure creation skipped (skip_execution=True). Warning: Could not save SQL file: {str(e)}",
                            "procedure": result,
                            "skipped": True,
                            "error": str(e),
                            "debug": {
                                "skip_execution_env": skip_execution_env,
                                "skip_execution_config": skip_execution_config,
                                "final_skip_execution": skip_execution
                            }
                        }
                return {"message": result}
            else:
                raise ValueError(f"No implementation found for tool: {name}")

        async def run(self):
            import traceback
            if self.app:
                try:
                    from mcp.server.stdio import stdio_server
                    from mcp.server.models import InitializationOptions
                    from mcp.server import NotificationOptions
                    capabilities = self.app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                    initialization_options = InitializationOptions(
                        server_name="uv-sql-tool-mcp-server",
                        server_version="0.1.0",
                        capabilities=capabilities,
                        instructions="uv_sql_tool MCP Server - provides SQL tooling"
                    )
                    async with stdio_server() as (read_stream, write_stream):
                        await self.app.run(
                            read_stream,
                            write_stream,
                            initialization_options
                        )
                except Exception as e:
                    self.logger.error(f"Exception in app.run: {e}\n{traceback.format_exc()}")
                    raise
            else:
                print("MCP server not available.")

    return UVSQLToolMCPServer()

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    try:
        app = create_app()
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()