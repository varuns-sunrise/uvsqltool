# UV SQL Tool - MCP Server
A powerful Model Context Protocol (MCP) server for migrating legacy data into Microsoft Dynamics Finance & Operations (F&O). This tool provides configurable SQL Server connectivity, schema generation, and automated migration utilities designed for enterprise environments with safe training modes.

## Overview
The UV SQL Tool streamlines data transformation and migration processes for Dynamics Finance & Operations implementations. It offers flexible configuration options for SQL Server connections, automated schema generation, and comprehensive migration utilities that integrate seamlessly with modern development workflows and AI assistants through MCP.

## 🚀 Quick Start for Teams

### Using the MCP Server (Recommended)
1. **Install the tool globally:**
   ```bash
   uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git
   ```

2. **Copy the training configuration:**
   Copy `Training/.vscode/mcp.json` to your Claude Desktop configuration or MCP client

3. **Update connection details:**
   Edit the `SQL_*` environment variables in the configuration

4. **Start using SQL tools safely:**
   The tool runs in safe mode by default (`SKIP_EXECUTION=true`) for training

### Training Mode Features
- ✅ **Safe by default**: SQL generation without execution
- ✅ **Team sharing**: Standardized configuration files
- ✅ **Easy setup**: One command installation with `uv tool install`
- ✅ **Environment control**: Toggle execution with environment variables

## Prerequisites
Before using the UV SQL Tool, ensure you have the following components configured. Prerequisites are organized into Required (essential for basic functionality) and Optional (enhances capabilities).

### 🔴 Required Prerequisites
These components are essential for the UV SQL Tool to function properly.

#### 1. 🐍 UV (Python Package Manager)
UV is a modern, fast Python package and project manager required for installing and running the tool.

**Installation on Windows:**
```powershell
# Using PowerShell (recommended)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: Using pip
pip install uv

# Alternative: Using Scoop
scoop install uv
```

**Verify installation:**
```bash
uv --version
```

#### 2. 🗄️ SQL Server Access
Access to a SQL Server instance for data operations.

**Requirements:**
- SQL Server instance (Express, Standard, or Enterprise edition)
- ODBC Driver 17 for SQL Server (or compatible driver)
- Appropriate connection credentials (username/password or Windows authentication)
- Network connectivity to the target SQL Server

**Install ODBC Driver:**
```powershell
# Download and install ODBC Driver 17 for SQL Server
# Visit: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

#### 3. 🔑 Database Credentials
Valid credentials for connecting to your SQL Server environment.

**Required Information:**
- Server name or IP address
- Database name
- Authentication method (SQL Server or Windows authentication)
- Username and password (if using SQL Server authentication)

### 🟡 Optional Prerequisites
These components enhance the UV SQL Tool experience but are not strictly required.

#### 4. 📝 VS Code (Recommended for Development)
Visual Studio Code with recommended extensions for an enhanced development experience.

**Installation:**
```powershell
# Using winget
winget install Microsoft.VisualStudioCode

# Using Chocolatey
choco install vscode
```

**Verify installation:**
```bash
code --version
```

#### 5. 🔧 Git for Windows
Git for version control and repository management.

**Installation:**
```powershell
# Using winget (recommended)
winget install --id Git.Git -e --source winget

# Using Chocolatey
choco install git

# Using Scoop
scoop install git
```

**Verify installation:**
```bash
git --version
```

#### 6. 🏢 Microsoft Dynamics Finance & Operations Environment
Access to D365 F&O environment for testing migrations.

**Requirements:**
- D365 F&O environment URL
- Valid user credentials with appropriate permissions
- API access permissions for data operations

## Installation

### Quick Installation (Recommended)
Install the UV SQL Tool directly from GitHub using UV:

```bash
# Install the latest version from main branch
uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git

# Install a specific version/tag
uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git@v0.1.0

# Install from a specific branch
uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git@feature-branch
```

### Development Installation
For contributors or advanced users who want to modify the tool:

```bash
# Clone the repository
git clone https://github.com/varuns-sunrise/uvsqltool.git
cd uvsqltool

# Install in development mode
uv tool install --editable .
```

### Verify Installation
After installation, verify the tool is working correctly:

```bash
# Check version
uv-sql-tool --version

# View help
uv-sql-tool --help

# Test server component
uv-sql-server --help
```

## Configuration

### SQL Server Configuration
The UV SQL Tool supports multiple methods for configuring SQL Server credentials with the following precedence:

1. **Command line arguments** (highest priority)
2. **Configuration file** (specified with --config-file)
3. **Environment variables**
4. **Default values** (lowest priority)

#### Method 1: Environment Variables (Recommended for Production)
Set environment variables for secure credential management:

```powershell
# Windows PowerShell
$env:SQL_SERVER = "your-server.database.windows.net"
$env:SQL_DATABASE = "your_database"
$env:SQL_USERNAME = "your_username"
$env:SQL_PASSWORD = "your_password"
$env:SQL_ENCRYPT = "true"
$env:SQL_TRUSTED_CONNECTION = "false"
```

```bash
# Linux/macOS
export SQL_SERVER="your-server.database.windows.net"
export SQL_DATABASE="your_database"
export SQL_USERNAME="your_username"
export SQL_PASSWORD="your_password"
export SQL_ENCRYPT="true"
export SQL_TRUSTED_CONNECTION="false"
```

#### Method 2: Configuration File
Create a configuration file for persistent settings:

```bash
# Create a sample configuration file
uv-sql-tool config create-sample --output my-config.json
```

Edit the generated configuration file:

```json
{
  "sql_server": {
    "server": "your-server.database.windows.net",
    "database": "your_database",
    "username": "your_username",
    "password": "your_password",
    "driver": "ODBC Driver 17 for SQL Server",
    "port": null,
    "trusted_connection": false,
    "encrypt": true,
    "trust_server_certificate": false,
    "connection_timeout": 30,
    "command_timeout": 30
  }
}
```

#### Method 3: Command Line Arguments
Override configuration for one-time operations:

```bash
uv-sql-tool call-tool create_table \
  --server "your-server.database.windows.net" \
  --database "your_database" \
  --username "your_username" \
  --password "your_password" \
  --args '{"csv_file_path": "data.csv", "table_name": "MyTable"}'
```

### Configuration Management Commands
The tool provides built-in configuration management utilities:

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

## MCP Server Configuration

The UV SQL Tool can run as an MCP (Model Context Protocol) server, allowing integration with AI assistants like Claude Desktop.

### Training Configuration
For team sharing and safe training environments, use the provided configuration:

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
        "SQL_DATABASE": "D365Migration",
        "SQL_USERNAME": "your_username",
        "SQL_PASSWORD": "your_password",
        "SQL_TRUSTED_CONNECTION": "false",
        "SQL_ENCRYPT": "true",
        "SKIP_EXECUTION": "true"
      }
    }
  }
}
```

### Environment Variables for MCP

| Variable | Description | Default |
|----------|-------------|---------|
| `SKIP_EXECUTION` | Skip actual SQL execution (safe mode) | `false` |
| `SQL_SERVER` | SQL Server hostname/IP | Required |
| `SQL_DATABASE` | Database name | Required |
| `SQL_USERNAME` | Username for authentication | Required |
| `SQL_PASSWORD` | Password for authentication | Required |
| `SQL_ENCRYPT` | Use encrypted connection | `true` |
| `SQL_TRUSTED_CONNECTION` | Use Windows authentication | `false` |

### Safety Features
- **Training Mode**: Set `SKIP_EXECUTION=true` to generate SQL without executing
- **Team Sharing**: Standardized configuration files in `Training/` folder
- **Environment Control**: Easy toggle between safe and production modes

## Usage

### Command Line Interface
The UV SQL Tool provides a comprehensive CLI for data migration tasks:

#### List Available Tools
```bash
# Display all available SQL tools
uv-sql-tool list-tools
```

#### Execute Migration Tools
```bash
# Create table with inline credentials
uv-sql-tool call-tool create_table \
  --server "myserver.database.windows.net" \
  --database "mydb" \
  --username "myuser" \
  --password "mypass" \
  --args '{"csv_file_path": "data.csv", "table_name": "customers"}'

# Use environment variables for credentials
uv-sql-tool call-tool create_table \
  --args '{"csv_file_path": "data.csv", "table_name": "customers"}'

# Use configuration file
uv-sql-tool call-tool create_table \
  --config-file "./prod-config.json" \
  --args '{"csv_file_path": "data.csv", "table_name": "customers"}'
```

#### Generate Stored Procedures
```bash
# Generate stored procedure from table schema
uv-sql-tool call-tool create_stored_procedure \
  --config-file "./config.json" \
  --args '{
    "table_name": "customers", 
    "dictionary_path": "./data-dictionary.json",
    "reference_sp_path": "./reference-procedures/"
  }'
```

### Server Mode (MCP Integration)
The UV SQL Tool can run as a Model Context Protocol (MCP) server for integration with AI development environments:

```bash
# Start the MCP server
uv-sql-server
```

The MCP server uses the same configuration methods as the CLI tool and provides programmatic access to all migration utilities.

## Automated Setup

### 🚀 Quick Setup Script
We've created an automated setup script for easy environment configuration:

```powershell
# Navigate to the project directory
cd path/to/uvsqltool

# Run the setup script
.\scripts\setup-publish.ps1
```

### What the Automated Setup Includes
The setup script automatically handles:

✅ **Package Building**
- Validates project structure
- Builds distribution packages
- Verifies build integrity

✅ **Local Installation Testing**
- Installs the tool locally
- Tests command functionality
- Validates all entry points

✅ **Command Verification**
- Tests version command
- Validates help system
- Confirms all CLI options

✅ **Development Guidance**
- Provides GitHub publishing instructions
- Suggests versioning workflow
- Offers deployment best practices

## VS Code Integration

### Recommended Extensions
For the best development experience with the UV SQL Tool, install these VS Code extensions:

Create `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-vscode.powershell",
    "GitHub.copilot",
    "GitHub.copilot-chat",
    "ms-vscode.vscode-json",
    "ms-azuretools.vscode-azureresourcegroups"
  ]
}
```

### MCP Server Configuration
Configure the UV SQL Tool as an MCP server in VS Code by creating `.vscode/mcp.json`:

```json
{
  "servers": {
    "uv-sql-tool": {
      "command": "uvx",
      "args": ["uv-sql-server"],
      "env": {
        "SQL_SERVER": "your-server.database.windows.net",
        "SQL_DATABASE": "your_database",
        "SQL_USERNAME": "your_username",
        "SQL_PASSWORD": "your_password",
        "SQL_ENCRYPT": "true",
        "SQL_TRUSTED_CONNECTION": "false"
      }
    }
  }
}
```

## Advanced Usage

### Batch Operations
Process multiple files or operations using configuration files:

```bash
# Process multiple CSV files
uv-sql-tool call-tool create_table \
  --config-file "./batch-config.json" \
  --args '{"csv_files": ["file1.csv", "file2.csv"], "table_prefix": "staging_"}'
```

### Integration with CI/CD
Use the UV SQL Tool in automated deployment pipelines:

```yaml
# GitHub Actions example
- name: Install UV SQL Tool
  run: uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git

- name: Run Migration
  run: |
    uv-sql-tool call-tool create_table \
      --server "${{ secrets.SQL_SERVER }}" \
      --database "${{ secrets.SQL_DATABASE }}" \
      --username "${{ secrets.SQL_USERNAME }}" \
      --password "${{ secrets.SQL_PASSWORD }}" \
      --args '{"csv_file_path": "migration-data.csv", "table_name": "production_data"}'
```

### Custom Migration Scripts
Extend the tool with custom migration logic:

```python
# Example: Custom migration script
from uv_sql_tool import get_sql_config, execute_sql_on_azure

# Load configuration
config = get_sql_config()

# Execute custom SQL
custom_sql = """
CREATE TABLE custom_migration (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data NVARCHAR(MAX),
    created_date DATETIME DEFAULT GETDATE()
)
"""

execute_sql_on_azure(custom_sql, config)
```

## Troubleshooting

### Common Issues

#### 1. Installation Failures
**Problem:** UV tool installation fails
**Solution:**
```bash
# Verify UV is installed
uv --version

# Try alternative installation
uv tool install --force git+https://github.com/varuns-sunrise/uvsqltool.git

# Check for dependency issues
uv tool install --verbose git+https://github.com/varuns-sunrise/uvsqltool.git
```

#### 2. Connection Issues
**Problem:** Cannot connect to SQL Server
**Solution:**
```bash
# Test connection with configuration
uv-sql-tool config test --server "your-server" --database "your-db"

# Verify credentials
uv-sql-tool config show

# Check network connectivity
telnet your-server 1433
```

#### 3. Permission Errors
**Problem:** Insufficient database permissions
**Solution:**
- Verify user has CREATE TABLE permissions
- Check database role assignments
- Ensure proper schema access rights

#### 4. ODBC Driver Issues
**Problem:** ODBC driver not found
**Solution:**
```powershell
# Install ODBC Driver 17 for SQL Server
# Download from Microsoft: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Verify driver installation
odbcad32.exe
```

### Getting Help
If you encounter issues not covered in this guide:

1. **Check the GitHub Issues:** Visit the [Issues page](https://github.com/varuns-sunrise/uvsqltool/issues)
2. **Review Documentation:** Ensure you've followed all prerequisites
3. **Test with Minimal Configuration:** Try the simplest possible setup first
4. **Enable Verbose Logging:** Use `--verbose` flags where available

## Contributing

### Development Setup
To contribute to the UV SQL Tool:

```bash
# Fork and clone the repository
git clone https://github.com/your-username/uvsqltool.git
cd uvsqltool

# Install in development mode
uv tool install --editable .

# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Format code
uv run black src/
uv run ruff check src/
```

### Submission Guidelines
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Project Structure
```
uvsqltool/
├── .github/
│   └── workflows/
│       └── release.yml          # GitHub Actions for releases
├── .vscode/
│   ├── extensions.json          # Recommended VS Code extensions
│   └── mcp.json                 # MCP server configuration template
├── scripts/
│   ├── setup-publish.ps1        # PowerShell setup script
│   └── setup-publish.sh         # Bash setup script
├── src/
│   └── uv_sql_tool/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Main entry point for server
│       ├── cli.py               # Command-line interface
│       ├── config.py            # Configuration management
│       ├── schema_generator.py  # SQL schema generation utilities
│       ├── server.py            # MCP server implementation
│       └── tools.py             # Core migration tools
├── .gitignore                   # Git ignore patterns
├── LICENSE                      # MIT License
├── pyproject.toml              # Project configuration and dependencies
└── README.md                   # This file
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support
For support and questions:

- **Issues:** [GitHub Issues](https://github.com/varuns-sunrise/uvsqltool/issues)
- **Documentation:** [GitHub Repository](https://github.com/varuns-sunrise/uvsqltool)
- **Author:** Varun Shah (varun.shah@sunrise.co)

---

## Quick Reference

### Installation
```bash
uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git
```

### Basic Configuration
```bash
uv-sql-tool config create-sample
uv-sql-tool config test --server "your-server" --database "your-db"
```

### Basic Usage
```bash
uv-sql-tool list-tools
uv-sql-tool call-tool create_table --args '{"csv_file_path": "data.csv", "table_name": "mytable"}'
```

### Environment Variables
```powershell
$env:SQL_SERVER = "your-server"
$env:SQL_DATABASE = "your-database"
$env:SQL_USERNAME = "your-username"
$env:SQL_PASSWORD = "your-password"
```