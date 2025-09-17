# MCP Server COOK BOOK / RUN BOOK

## 1. What is an MCP Server?
- **MCP (Model Context Protocol) Server**: A standard interface for connecting automation tools to AI assistants, CI/CD, or team workflows.
- **Purpose**: Centralizes logic, configuration, and safe execution for data migration, transformation, or other automation tasks.

---

## 2. Key Components of an MCP Server
- **Tool Logic**: Python scripts or modules that perform the actual work (e.g., SQL generation, schema migration).
- **Server Wrapper**: A Python entry point (`server.py`) that exposes your tools via MCP protocol.
- **Configuration**: JSON or environment variable-based settings for credentials, safe mode, etc.
- **GitHub Repository**: Hosts your code, making it easy to install and share via MCP.

---

## 3. Steps to Create Your Own MCP Server

### Step 1: Organize Your Codebase
- Place all tool logic in a `src/your_tool/` directory.
- Add a `server.py` that wraps your tools and exposes MCP endpoints.
- Include a `tools.py` for input schemas and tool registration.

### Step 2: Add MCP Protocol Support
- Use a standard MCP server wrapper (see `server.py` in this repo).
- Ensure your server can read configuration from environment variables and/or JSON files.
- Implement safe mode (`SKIP_EXECUTION`) for training and testing.

### Step 3: Prepare for GitHub Distribution
- Add a `pyproject.toml` for Python packaging.
- Include a clear `README.md` with setup, usage, and troubleshooting.
- Add `.gitignore` for build artifacts and sensitive files.
- Optionally, add scripts for setup and publishing (`scripts/`).

### Step 4: MCP Configuration Example
Create a `.vscode/mcp.json` or share a config snippet:

```json
{
  "servers": {
    "my-mcp-tool": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/your-org/your-mcp-tool.git",
        "your-mcp-server"
      ],
      "env": {
        "SQL_SERVER": "your-server",
        "SQL_DATABASE": "your-db",
        "SKIP_EXECUTION": "True"
      }
    }
  }
}
```

### Step 5: Share and Use
- Push your repo to GitHub.
- Team members can connect using MCP with the `--from` argument:
  ```sh
  uvx --from git+https://github.com/your-org/your-mcp-tool.git your-mcp-server
  ```
- Update environment variables or config files as needed.

---

## 4. Best Practices
- **Safe Defaults**: Always support a training mode (`SKIP_EXECUTION=True`).
- **Clear Schemas**: Define tool input schemas in `tools.py` for validation and discoverability.
- **Documentation**: Keep your README concise and focused on MCP usage.
- **Troubleshooting**: Document common issues and solutions.
- **Versioning**: Tag releases in GitHub for reproducible installs.

---

## 5. Example Directory Structure

```
your-mcp-tool/
├── src/
│   └── your_tool/
│       ├── __init__.py
│       ├── server.py
│       ├── tools.py
│       └── logic.py
├── scripts/
│   └── setup-publish.ps1
├── pyproject.toml
├── README.md
├── .gitignore
└── .vscode/
    └── mcp.json
```

---

## 6. Troubleshooting & Support
- **Access Denied**: Add Windows Defender exclusion or run VS Code as administrator.
- **Package Not Found**: Check your MCP config and GitHub repo URL.
- **Connection Issues**: Verify credentials, test connectivity, check firewall.

---

## 7. Sharing with Others
- Use GitHub for version control and distribution.
- Document the MCP config and environment variables in your README.
- Encourage team members to fork, clone, and contribute improvements.

---

## 8. Next Steps
1. Fork or clone the template MCP server repo.
2. Add your own tool logic and configuration.
3. Push to GitHub and share the MCP config.
4. Test with your team and iterate!

---

*This COOK BOOK empowers your team to build, share, and maintain MCP servers for any development or migration workflow. For more details, see the full documentation or reach out for support!*
