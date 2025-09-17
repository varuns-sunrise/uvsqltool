"""MCP server entrypoint for uv_sql_tool (for Copilot Workspace)."""

import sys
import json
import asyncio
import logging
from typing import Any, Dict, Optional

from .tools import ALL_SQL_TOOLS, SQL_TOOLS_BY_NAME
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
                execute_sql_on_azure(sql, config=sql_config)
                return {"message": f"Table '{arguments['table_name']}' created successfully."}
            elif name == "create_stored_procedure":
                result = generate_stored_procedure(
                    arguments["table_name"],
                    arguments["dictionary_path"],
                    arguments["reference_sp_path"]
                )
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