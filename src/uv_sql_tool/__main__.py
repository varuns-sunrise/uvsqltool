"""
Entrypoint for running the UV SQL Tool MCP server.

This script initializes and starts the MCP server using asyncio.
"""

import sys
import asyncio
from uv_sql_tool.server import create_app


def main():
    # Create the MCP server app
    app = create_app()
    try:
        # Run the server event loop
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()