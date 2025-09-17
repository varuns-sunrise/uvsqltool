"""
Command-line interface for UV SQL Tool MCP server.
Provides argument parsing, config management, and tool invocation for migration tasks.
"""

import argparse
import sys
import json
from . import __version__
from .config import get_sql_config, create_sample_config, SQLServerConfig


def add_sql_config_args(parser):
    """
    Add SQL Server configuration arguments to a parser.
    """
    sql_group = parser.add_argument_group('SQL Server Configuration')
    sql_group.add_argument('--server', type=str, help='SQL Server name')
    sql_group.add_argument('--database', type=str, help='Database name')
    sql_group.add_argument('--username', type=str, help='Username')
    sql_group.add_argument('--password', type=str, help='Password')
    sql_group.add_argument('--config-file', type=str, help='Path to configuration file')
    sql_group.add_argument('--trusted-connection', action='store_true', 
                          help='Use Windows authentication')
    sql_group.add_argument('--encrypt', action='store_true', default=True,
                          help='Use encrypted connection (default: True)')
    return sql_group


def main():
    """
    Main entrypoint for the CLI tool.
    Handles argument parsing and command dispatch.
    """
    parser = argparse.ArgumentParser(
        description="UV SQL Tool Command Line Interface",
        prog="uv-sql-tool"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_subparsers = config_parser.add_subparsers(dest='config_action')
    
    # Create sample config
    create_config_parser = config_subparsers.add_parser(
        'create-sample', 
        help='Create a sample configuration file'
    )
    create_config_parser.add_argument(
        '--output', '-o', 
        type=str, 
        default='uv-sql-config.json',
        help='Output path for configuration file'
    )
    
    # Test connection
    test_parser = config_subparsers.add_parser('test', help='Test SQL Server connection')
    add_sql_config_args(test_parser)
    
    # Show current config
    show_config_parser = config_subparsers.add_parser('show', help='Show current configuration')
    add_sql_config_args(show_config_parser)

    # Example command: list-tools
    list_tools_parser = subparsers.add_parser('list-tools', help='List all available SQL tools')

    # Example command: call-tool
    call_tool_parser = subparsers.add_parser('call-tool', help='Call a specific SQL tool')
    call_tool_parser.add_argument('name', type=str, help='Name of the tool to call')
    call_tool_parser.add_argument('--args', type=str, help='Arguments for the tool in JSON format')
    add_sql_config_args(call_tool_parser)

    args = parser.parse_args()

    if args.command == 'config':
        handle_config_command(args)
    elif args.command == 'list-tools':
        # Logic to list tools would go here
        print("Listing all available SQL tools...")
        print("Available tools:")
        print("  - schema-generator: Generate database schemas")
        print("  - data-migrator: Migrate legacy data")
        print("  - sql-executor: Execute SQL operations")
    elif args.command == 'call-tool':
        # Logic to call a tool would go here
        print(f"Calling tool: {args.name} with arguments: {args.args}")
        
        # Get SQL config from arguments
        config = get_sql_config(
            config_path=getattr(args, 'config_file', None),
            server=getattr(args, 'server', None),
            database=getattr(args, 'database', None),
            username=getattr(args, 'username', None),
            password=getattr(args, 'password', None),
            trusted_connection=getattr(args, 'trusted_connection', False),
            encrypt=getattr(args, 'encrypt', True)
        )
        print(f"Using SQL Server: {config.server}/{config.database}")
    else:
        parser.print_help()
        sys.exit(1)


def handle_config_command(args):
    """Handle configuration-related commands."""
    if args.config_action == 'create-sample':
        create_sample_config(args.output)
    elif args.config_action == 'test':
        test_connection(args)
    elif args.config_action == 'show':
        show_configuration(args)
    else:
        print("Available config commands: create-sample, test, show")


def test_connection(args):
    """Test SQL Server connection with provided configuration."""
    try:
        config = get_sql_config(
            config_path=getattr(args, 'config_file', None),
            server=getattr(args, 'server', None),
            database=getattr(args, 'database', None),
            username=getattr(args, 'username', None),
            password=getattr(args, 'password', None),
            trusted_connection=getattr(args, 'trusted_connection', False),
            encrypt=getattr(args, 'encrypt', True)
        )
        
        print(f"Testing connection to {config.server}/{config.database}...")
        
        # Test with a simple query
        from .schema_generator import execute_sql_on_azure
        execute_sql_on_azure("SELECT 1 as test", config)
        print("✅ Connection successful!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)


def show_configuration(args):
    """Show current configuration (without sensitive data)."""
    config = get_sql_config(
        config_path=getattr(args, 'config_file', None),
        server=getattr(args, 'server', None),
        database=getattr(args, 'database', None),
        username=getattr(args, 'username', None),
        password=getattr(args, 'password', None),
        trusted_connection=getattr(args, 'trusted_connection', False),
        encrypt=getattr(args, 'encrypt', True)
    )
    
    print("Current SQL Server Configuration:")
    print(f"  Server: {config.server}")
    print(f"  Database: {config.database}")
    print(f"  Username: {config.username if config.username else '(not set)'}")
    print(f"  Password: {'***' if config.password else '(not set)'}")
    print(f"  Driver: {config.driver}")
    print(f"  Trusted Connection: {config.trusted_connection}")
    print(f"  Encrypt: {config.encrypt}")
    print(f"  Trust Server Certificate: {config.trust_server_certificate}")
    print(f"  Connection Timeout: {config.connection_timeout}")
    print(f"  Command Timeout: {config.command_timeout}")

if __name__ == "__main__":
    main()