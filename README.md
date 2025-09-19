# Data Migration Automation: Scenario, Solution & Benefits

## Scenario & Problem
Many customers migrating to Microsoft Dynamics Finance & Operations (F&O) cannot provide legacy data directly in a SQL database. Instead, they extract data into CSV files with unfriendly, technical column names. They also supply a mapping file to translate these legacy column names to logical English names. Manually creating SQL tables and stored procedures for each file and mapping is labor-intensive and error-prone for both the customer and migration team.

## Solution
The UV SQL Tool MCP Server automates the entire process:
- Generates SQL tables directly from customer CSV files.
- Automatically creates stored procedures to map legacy column names to logical English names using the provided mapping file.
- Supports training mode to generate and review SQL before execution.

## Key Benefits
- **Automation:** Instantly creates SQL tables and procedures, reducing manual effort.
- **Consistency:** Enforces standardized, readable naming conventions.
- **Speed:** Accelerates migration timelines by automating code generation.
- **Quality:** Minimizes human error, improving data quality.
- **Scalability:** Easily repeatable for multiple files and mappings.
- **Customer Empowerment:** Allows customers to provide data in simple CSV format without SQL expertise.
- **Documentation:** Automatically documents source files, mappings, and generated SQL for traceability.

---

# UV SQL Tool - MCP Server

A powerful Model Context Protocol (MCP) server for migrating legacy data into Microsoft Dynamics Finance & Operations (F&O).

## Dependencies & Prerequisites

### Option 1: Native Installation

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

### Option 2: Docker Installation

- **Docker Desktop** or **Docker Engine**
- **SQL Server Access** (same as above)
- No need to install UV, Python, or ODBC drivers manually - everything is included in the Docker image

## Common Issues & Solutions

- **Access Denied (Windows):**  
  Add a Windows Defender exclusion for `C:\Users\[your-username]\.local\bin\` or run VS Code as administrator.

- **Package Not Found:**  
  Make sure your MCP config uses the correct `--from` argument for the GitHub repo.

- **Server Connection Issues:**  
  Double-check SQL Server details, test connectivity, and check firewall settings.

## Testing Installation

### Native Installation
```powershell
uv --version
uvx --from "git+https://github.com/varuns-sunrise/uvsqltool.git" uv-sql-server --help
```

### Docker Installation
```bash
# Test Docker image build
docker build . -t uvsqlserver:latest

# Test running the container
docker run --rm uvsqlserver:latest --help
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

---

## 🐳 Docker Support

### Building the Docker Image

The project includes a Dockerfile that sets up a complete environment with all necessary ODBC drivers and dependencies.

```bash
# Build the Docker image
docker build . -t uvsqlserver:latest
```

### Running with Docker

```bash
# Run the container with environment variables
docker run --rm -i \
           -e SQL_SERVER="your-server.database.windows.net" \
           -e SQL_DATABASE="your_database" \
           -e SQL_USERNAME="your_username" \
           -e SQL_PASSWORD="your_password" \
           -e SQL_DRIVER="ODBC Driver 18 for SQL Server" \
           -e SKIP_EXECUTION="True" \
           uvsqlserver:latest
```

### Docker Features

- **Pre-installed ODBC Drivers**: Microsoft ODBC Driver 18 for SQL Server
- **Security**: Runs as non-root user (`sun_mcp`)
- **Python 3.13**: Latest Python with UV package manager
- **Ready-to-use**: All dependencies pre-installed and configured

### Docker Environment Variables

The Docker container supports the same environment variables as the native installation:
- `SQL_SERVER`: Your SQL Server instance
- `SQL_DATABASE`: Target database name
- `SQL_USERNAME`: Database username
- `SQL_PASSWORD`: Database password
- `SQL_DRIVER`: ODBC Driver (defaults to "ODBC Driver 18 for SQL Server")
- `SKIP_EXECUTION`: Set to "True" for training mode

---

## Example MCP Configuration

### Native Installation (using uvx)
```json
{
  "servers": {
    "uv-sql-tool": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/varuns-sunrise/uvsqltool.git",
        "uv-sql-server"
      ],
      "env": {
        "SQL_SERVER": "${input:SQL_SERVER}",
        "SQL_DATABASE": "${input:SQL_DATABASE}",
        "SQL_USERNAME": "${input:SQL_USERNAME}",
        "SQL_PASSWORD": "${input:SQL_PASSWORD}",
        "SQL_DRIVER": "${input:SQL_DRIVER}",
        "SKIP_EXECUTION": "True"
      }
    }
  },
  "inputs": [
    {
      "id": "SQL_SERVER",
      "type": "promptString",
      "description": "The SQL Server name (e.g., your-server.database.windows.net)",
      "password": false
    },
    {
      "id": "SQL_DATABASE",
      "type": "promptString",
      "description": "The SQL Database name",
      "password": false
    },
    {
      "id": "SQL_USERNAME",
      "type": "promptString",
      "description": "The SQL Server username",
      "password": false
    },
    {
      "id": "SQL_PASSWORD",
      "type": "promptString",
      "description": "The SQL Server password",
      "password": true
    },
    {
      "id": "SQL_DRIVER",
      "type": "pickString",
      "description": "The ODBC Driver for SQL Server",
      "options": [
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server"
      ],
      "default": "ODBC Driver 17 for SQL Server"
    }
  ]
}
```

### Docker Installation (recommended)
```json
{
  "servers": {
    "uv-sql-tool": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e",
        "SQL_SERVER=${input:SQL_SERVER}",
        "-e",
        "SQL_DATABASE=${input:SQL_DATABASE}",
        "-e",
        "SQL_USERNAME=${input:SQL_USERNAME}",
        "-e",
        "SQL_PASSWORD=${input:SQL_PASSWORD}",
        "-e",
        "SQL_DRIVER=${input:SQL_DRIVER}",
        "-e",
        "SKIP_EXECUTION=True",
        "uvsqlserver:latest"
      ]
    }
  },
  "inputs": [
    {
      "id": "SQL_SERVER",
      "type": "promptString",
      "description": "The SQL Server name (e.g., your-server.database.windows.net)",
      "password": false
    },
    {
      "id": "SQL_DATABASE",
      "type": "promptString",
      "description": "The SQL Database name",
      "password": false
    },
    {
      "id": "SQL_USERNAME",
      "type": "promptString",
      "description": "The SQL Server username",
      "password": false
    },
    {
      "id": "SQL_PASSWORD",
      "type": "promptString",
      "description": "The SQL Server password",
      "password": true
    },
    {
      "id": "SQL_DRIVER",
      "type": "pickString",
      "description": "The ODBC Driver for SQL Server",
      "options": [
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server"
      ],
      "default": "ODBC Driver 17 for SQL Server"
    }
  ]
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