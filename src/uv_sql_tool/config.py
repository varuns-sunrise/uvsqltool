"""Configuration management for UV SQL Tool."""

import os
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SQLServerConfig:
    """SQL Server connection configuration."""
    server: str
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    driver: str = "ODBC Driver 17 for SQL Server"
    port: Optional[int] = None
    trusted_connection: bool = False
    encrypt: bool = True
    trust_server_certificate: bool = False
    connection_timeout: int = 30
    command_timeout: int = 30

    @property
    def connection_string(self) -> str:
        """Generate ODBC connection string from configuration."""
        parts = [
            f"Driver={{{self.driver}}}",
            f"Server={self.server}"
        ]
        
        if self.port:
            parts[-1] += f",{self.port}"
            
        parts.append(f"Database={self.database}")
        
        if self.trusted_connection:
            parts.append("Trusted_Connection=yes")
        elif self.username and self.password:
            parts.extend([
                f"UID={self.username}",
                f"PWD={self.password}"
            ])
        
        if self.encrypt:
            parts.append("Encrypt=yes")
        
        if self.trust_server_certificate:
            parts.append("TrustServerCertificate=yes")
            
        parts.extend([
            f"Connection Timeout={self.connection_timeout}",
            f"Command Timeout={self.command_timeout}"
        ])
        
        return ";".join(parts) + ";"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SQLServerConfig':
        """Create configuration from dictionary."""
        return cls(**data)

    @classmethod
    def from_env(cls) -> 'SQLServerConfig':
        """Create configuration from environment variables."""
        return cls(
            server=os.getenv("SQL_SERVER", "localhost"),
            database=os.getenv("SQL_DATABASE", "master"),
            username=os.getenv("SQL_USERNAME"),
            password=os.getenv("SQL_PASSWORD"),
            driver=os.getenv("SQL_DRIVER", "ODBC Driver 17 for SQL Server"),
            port=int(os.getenv("SQL_PORT")) if os.getenv("SQL_PORT") else None,
            trusted_connection=os.getenv("SQL_TRUSTED_CONNECTION", "false").lower() == "true",
            encrypt=os.getenv("SQL_ENCRYPT", "true").lower() == "true",
            trust_server_certificate=os.getenv("SQL_TRUST_SERVER_CERT", "false").lower() == "true",
            connection_timeout=int(os.getenv("SQL_CONNECTION_TIMEOUT", "30")),
            command_timeout=int(os.getenv("SQL_COMMAND_TIMEOUT", "30"))
        )

    @classmethod
    def from_config_file(cls, config_path: Optional[str] = None) -> 'SQLServerConfig':
        """Create configuration from JSON config file."""
        if config_path is None:
            # Look for config in common locations
            possible_paths = [
                "uv-sql-config.json",
                os.path.expanduser("~/.uv-sql-config.json"),
                os.path.join(os.getcwd(), "config.json")
            ]
            config_path = next((p for p in possible_paths if os.path.exists(p)), None)
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                return cls.from_dict(data.get("sql_server", {}))
        
        # Fallback to environment variables if no config file
        return cls.from_env()


def get_sql_config(
    config_path: Optional[str] = None,
    server: Optional[str] = None,
    database: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs
) -> SQLServerConfig:
    """
    Get SQL Server configuration with precedence:
    1. Explicit parameters
    2. Config file
    3. Environment variables
    4. Defaults
    """
    # Start with config file or environment
    config = SQLServerConfig.from_config_file(config_path)
    
    # Override with explicit parameters
    if server is not None:
        config.server = server
    if database is not None:
        config.database = database
    if username is not None:
        config.username = username
    if password is not None:
        config.password = password
    
    # Apply any additional kwargs
    for key, value in kwargs.items():
        if hasattr(config, key) and value is not None:
            setattr(config, key, value)
    
    return config


def create_sample_config(output_path: str = "uv-sql-config.json") -> None:
    """Create a sample configuration file."""
    sample_config = {
        "sql_server": {
            "server": "your-server.database.windows.net",
            "database": "your_database",
            "username": "your_username",
            "password": "your_password",
            "driver": "ODBC Driver 17 for SQL Server",
            "port": None,
            "trusted_connection": False,
            "encrypt": True,
            "trust_server_certificate": False,
            "connection_timeout": 30,
            "command_timeout": 30
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"Sample configuration created at: {output_path}")
    print("Please edit the file with your actual SQL Server credentials.")
