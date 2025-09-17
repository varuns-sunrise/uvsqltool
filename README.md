# UV SQL Tool

## Overview
The UV SQL Tool is designed for data transformation and migration into Dynamics Finance & Operations (F&O). It provides a set of utilities for executing SQL operations, generating schemas, and managing database migrations.

## Installation

### Install from GitHub (Recommended)
You can install this tool directly from GitHub using UV:

```bash
# Install the latest version from main branch
uv tool install git+https://github.com/yourusername/uv-sql-tool.git

# Install a specific version/tag
uv tool install git+https://github.com/yourusername/uv-sql-tool.git@v0.1.0

# Install from a specific branch
uv tool install git+https://github.com/yourusername/uv-sql-tool.git@feature-branch
```

### Install for Development
If you want to contribute or modify the tool:

```bash
# Clone the repository
git clone https://github.com/yourusername/uv-sql-tool.git
cd uv-sql-tool

# Install in development mode
uv tool install --editable .
```

### Verify Installation
After installation, verify it works:

```bash
uv-sql-tool --help
uv-sql-server --help
```

## Usage

### SQL Server Configuration

The UV SQL Tool supports multiple ways to configure SQL Server credentials:

#### 1. Environment Variables (Recommended for Production)
```bash
export SQL_SERVER="your-server.database.windows.net"
export SQL_DATABASE="your_database"
export SQL_USERNAME="your_username"
export SQL_PASSWORD="your_password"
export SQL_ENCRYPT="true"
export SQL_TRUSTED_CONNECTION="false"
```

#### 2. Configuration File
Create a configuration file using:
```bash
uv-sql-tool config create-sample --output my-config.json
```

Edit the generated file:
```json
{
  "sql_server": {
    "server": "your-server.database.windows.net",
    "database": "your_database", 
    "username": "your_username",
    "password": "your_password",
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": false,
    "encrypt": true,
    "trust_server_certificate": false,
    "connection_timeout": 30,
    "command_timeout": 30
  }
}
```

#### 3. Command Line Arguments
```bash
uv-sql-tool call-tool create_table \
  --server "your-server.database.windows.net" \
  --database "your_database" \
  --username "your_username" \
  --password "your_password" \
  --args '{"csv_file_path": "data.csv", "table_name": "MyTable"}'
```

### Configuration Management Commands

```bash
# Create a sample configuration file
uv-sql-tool config create-sample

# Test your SQL Server connection
uv-sql-tool config test --server "your-server" --database "your_db"

# Show current configuration (passwords hidden)
uv-sql-tool config show

# Test with config file
uv-sql-tool config test --config-file ./my-config.json
```

### Command Line Interface
```bash
# List available SQL tools
uv-sql-tool list-tools

# Call a specific tool with inline credentials
uv-sql-tool call-tool create_table \
  --server "myserver.database.windows.net" \
  --database "mydb" \
  --username "myuser" \
  --password "mypass" \
  --args '{"csv_file_path": "data.csv", "table_name": "customers"}'

# Call a tool using environment variables
uv-sql-tool call-tool create_table \
  --args '{"csv_file_path": "data.csv", "table_name": "customers"}'

# Call a tool using config file
uv-sql-tool call-tool create_table \
  --config-file "./prod-config.json" \
  --args '{"csv_file_path": "data.csv", "table_name": "customers"}'
```

### Server Mode
```bash
# Start the MCP server (uses environment variables or config file)
uv-sql-server
```

### Configuration Precedence
1. **Command line arguments** (highest priority)
2. **Configuration file** (specified with --config-file)
3. **Environment variables**
4. **Default values** (lowest priority)

## Project Structure
```
uv-sql-tool/
├── src/
│   └── uv_sql_tool/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── tools.py
│       ├── schema_generator.py
│       └── server.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.