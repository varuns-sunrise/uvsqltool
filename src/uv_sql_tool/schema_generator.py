import pyodbc
from typing import Optional
from .config import SQLServerConfig, get_sql_config


def generate_create_table_sql(csv_file_path: str, table_name: str) -> str:
    # Function to generate SQL for creating a table from a CSV file
    return f"""
CREATE TABLE {table_name} (
    -- Define your columns here based on the CSV structure
    Id INT PRIMARY KEY,
    Name NVARCHAR(255),
    CreatedDate DATETIME
);
"""

def execute_sql_on_azure(
    sql: str, 
    config: Optional[SQLServerConfig] = None,
    server: Optional[str] = None,
    database: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs
) -> None:
    """
    Execute SQL on SQL Server with configurable credentials.
    
    Args:
        sql: SQL statement to execute
        config: SQLServerConfig object (if provided, other params are ignored)
        server: Server name (overrides config/env)
        database: Database name (overrides config/env)
        username: Username (overrides config/env)
        password: Password (overrides config/env)
        **kwargs: Additional connection parameters
    """
    if config is None:
        config = get_sql_config(
            server=server,
            database=database,
            username=username,
            password=password,
            **kwargs
        )
    
    connection_string = config.connection_string
    
    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                print(f"SQL executed successfully on {config.server}/{config.database}")
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def generate_stored_procedure(table_name: str, dictionary_path: str, reference_sp_path: str) -> str:
    # Function to generate a stored procedure based on the provided parameters
    return f"""
CREATE PROCEDURE [dbo].[MIG_001_{table_name}_StoredProcedure]
AS
BEGIN
    SET NOCOUNT ON;

    -- Logic for the stored procedure goes here
    SELECT * FROM {table_name};
END
"""