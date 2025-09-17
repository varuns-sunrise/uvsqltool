# UV SQL Tool - MCP Server

A powerful Model Context Protocol (MCP) server for migrating legacy data into Microsoft Dynamics Finance & Operations (F&O).

## Dependencies & Prerequisites

- **UV Python Package Manager**  
  Install UV for MCP tool management:
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  uv --version
  ```
- **ODBC Driver 17 for SQL Server**  
  _Required only if you plan to execute SQL on a real database. If `SKIP_EXECUTION=True`, you do not need the ODBC driver installed._  
  [ODBC Driver Download](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- **SQL Server Access**  
  You need a reachable SQL Server instance and valid credentials.
- **Windows 10/11** (recommended)
- **PowerShell 5.1+** (for scripting)
- **VS Code with MCP extension** (optional, for best experience)

## Common Issues & Solutions

- **Access Denied (Windows):**  
  Add a Windows Defender exclusion for `C:\Users\[your-username]\.local\bin\` or run VS Code as administrator.

- **Package Not Found:**  
  Make sure your MCP config uses the correct `--from` argument for the GitHub repo.

- **Server Connection Issues:**  
  Double-check SQL Server details, test connectivity, and check firewall settings.

## Testing Installation

```powershell
uv --version
uvx --from "git+https://github.com/varuns-sunrise/uvsqltool.git" uv-sql-server --help
```

---

## 🚀 Quick Start (MCP Server)

1. **Connect MCP server from GitHub:**
   ```sh
   uvx --from git+https://github.com/varuns-sunrise/uvsqltool.git uv-sql-server
   ```

2. **Set environment variables:**
   - `SQL_SERVER`: Your SQL Server name
   - `SQL_DATABASE`: Your database name
   - `SQL_USERNAME`: Your username
   - `SQL_PASSWORD`: Your password
   - `SQL_DRIVER`: ODBC Driver (e.g., "ODBC Driver 17 for SQL Server")
   - `SKIP_EXECUTION`: Set to "True" for training mode (SQL is generated, not executed)

3. **Run the MCP server:**
   - Use your MCP config or the command above to start the server.

## Example MCP Configuration

```json
{
  "servers": {
    "uv-sql-tool": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/varuns-sunrise/uvsqltool.git",
        "uv-sql-server"
      ],
      "env": {
        "SQL_SERVER": "your-server.database.windows.net",
        "SQL_DATABASE": "your_database",
        "SQL_USERNAME": "your_username",
        "SQL_PASSWORD": "your_password",
        "SQL_DRIVER": "ODBC Driver 17 for SQL Server",
        "SKIP_EXECUTION": "True"
      }
    }
  }
}
```

## Usage

- Use MCP tools to generate SQL for tables and stored procedures
- Generated table files will be named `{table_name}.sql` in the `generated_sql/` folder
- For training, set `SKIP_EXECUTION=True` to avoid executing SQL on the database

## Support
For support and questions:
- **Issues:** [GitHub Issues](https://github.com/varuns-sunrise/uvsqltool/issues)
- **Documentation:** [GitHub Repository](https://github.com/varuns-sunrise/uvsqltool)

---

*This README is simplified for MCP server usage. For advanced development, see the full documentation on GitHub.*