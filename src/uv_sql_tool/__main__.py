import sys
import asyncio
from uv_sql_tool.server import create_app

def main():
    app = create_app()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()