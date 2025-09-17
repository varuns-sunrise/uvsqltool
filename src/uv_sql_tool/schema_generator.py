import pyodbc
import os
import re
import csv
from typing import Optional, List, Tuple, Dict
from .config import SQLServerConfig, get_sql_config


def _detect_data_type(value: str) -> str:
    """Detect SQL data type based on value content."""
    if not value or value.strip() == '':
        return 'NVARCHAR(255)'  # Default for empty values
    
    value = value.strip()
    
    # Check for integer
    if re.match(r'^-?\d+$', value):
        num = int(value)
        if -2147483648 <= num <= 2147483647:
            return 'INT'
        else:
            return 'BIGINT'
    
    # Check for decimal/float
    if re.match(r'^-?\d+\.\d+$', value):
        return 'DECIMAL(18,4)'
    
    # Check for date patterns
    date_patterns = [
        r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
        r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
        r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
        r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
    ]
    for pattern in date_patterns:
        if re.match(pattern, value):
            return 'DATE'
    
    # Check for datetime patterns
    datetime_patterns = [
        r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',  # YYYY-MM-DD HH:MM:SS
        r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}',  # MM/DD/YYYY HH:MM:SS
    ]
    for pattern in datetime_patterns:
        if re.match(pattern, value):
            return 'DATETIME2'
    
    # Check for boolean
    if value.lower() in ['true', 'false', '1', '0', 'yes', 'no']:
        return 'BIT'
    
    # Default to string with appropriate length
    length = len(value)
    if length <= 50:
        return 'NVARCHAR(50)'
    elif length <= 255:
        return 'NVARCHAR(255)'
    elif length <= 4000:
        return 'NVARCHAR(4000)'
    else:
        return 'NVARCHAR(MAX)'


def _analyze_column_data_types(file_path: str, max_rows_to_analyze: int = 100) -> List[Tuple[str, str]]:
    """Analyze the file to determine column names and data types."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    columns = []
    data_types = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the header line
            header_line = file.readline().strip()
            if not header_line:
                raise ValueError("File appears to be empty or has no header")
            
            # Parse column names from header
            column_names = [col.strip() for col in header_line.split('|')]
            
            # Initialize data type tracking
            for col_name in column_names:
                data_types[col_name] = []
            
            # Analyze data rows
            rows_analyzed = 0
            for line in file:
                if rows_analyzed >= max_rows_to_analyze:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                values = [val.strip() for val in line.split('|')]
                
                # Ensure we have the right number of columns
                if len(values) != len(column_names):
                    continue
                
                # Analyze each value
                for i, value in enumerate(values):
                    if i < len(column_names):
                        detected_type = _detect_data_type(value)
                        data_types[column_names[i]].append(detected_type)
                
                rows_analyzed += 1
    
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    # Determine final data types for each column
    for col_name in column_names:
        type_counts = {}
        for dt in data_types[col_name]:
            type_counts[dt] = type_counts.get(dt, 0) + 1
        
        if not type_counts:
            # No data found, default to string
            final_type = 'NVARCHAR(255)'
        else:
            # Use the most common type, with precedence rules
            if any('NVARCHAR' in dt for dt in type_counts.keys()):
                # If any string types found, use the largest string type
                string_types = [dt for dt in type_counts.keys() if 'NVARCHAR' in dt]
                if 'NVARCHAR(MAX)' in string_types:
                    final_type = 'NVARCHAR(MAX)'
                elif 'NVARCHAR(4000)' in string_types:
                    final_type = 'NVARCHAR(4000)'
                elif 'NVARCHAR(255)' in string_types:
                    final_type = 'NVARCHAR(255)'
                else:
                    final_type = 'NVARCHAR(50)'
            else:
                # Use most common non-string type
                final_type = max(type_counts, key=type_counts.get)
        
        # Clean column name for SQL
        clean_col_name = re.sub(r'[^a-zA-Z0-9_]', '_', col_name)
        if clean_col_name[0].isdigit():
            clean_col_name = f"Col_{clean_col_name}"
        
        columns.append((clean_col_name, final_type))
    
    return columns


def generate_create_table_sql(csv_file_path: str, table_name: str) -> str:
    # Function to generate SQL for creating a table from a pipe-delimited text file
    # Always prefix table names with "src"
    prefixed_table_name = f"src{table_name}" if not table_name.startswith("src") else table_name
    
    try:
        # Analyze the file to determine column structure
        columns = _analyze_column_data_types(csv_file_path)
        
        if not columns:
            raise ValueError("No columns could be determined from the file")
        
        # Generate column definitions
        column_definitions = []
        for i, (col_name, data_type) in enumerate(columns):
            # Add PRIMARY KEY to first column if it looks like an ID
            if i == 0 and ('id' in col_name.lower() or col_name.lower().endswith('_id')):
                column_definitions.append(f"    {col_name} {data_type} PRIMARY KEY")
            else:
                column_definitions.append(f"    {col_name} {data_type}")
        
        columns_sql = ",\n".join(column_definitions)
        
        return f"""
CREATE TABLE {prefixed_table_name} (
{columns_sql}
);

-- Table created from file: {csv_file_path}
-- Columns analyzed: {len(columns)}
-- Column details:
{chr(10).join([f'-- {col_name}: {data_type}' for col_name, data_type in columns])}
"""
    
    except Exception as e:
        # Fallback to basic structure if file analysis fails
        return f"""
-- ERROR: Could not analyze file {csv_file_path}: {str(e)}
-- Creating basic table structure as fallback

CREATE TABLE {prefixed_table_name} (
    Id INT PRIMARY KEY,
    Data NVARCHAR(MAX)
);

-- Please review the source file and adjust the table structure as needed
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

def _parse_mapping_file(dictionary_path: str) -> List[Dict[str, str]]:
    """Parse the mapping CSV file to get column mappings."""
    if not os.path.exists(dictionary_path):
        raise FileNotFoundError(f"Dictionary file not found: {dictionary_path}")
    
    mappings = []
    
    # Try different encodings
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings_to_try:
        try:
            with open(dictionary_path, 'r', encoding=encoding) as file:
                # Try to detect if it's CSV or pipe-delimited
                first_line = file.readline()
                file.seek(0)  # Reset to beginning
                
                if ',' in first_line and '|' not in first_line:
                    # CSV format
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Handle different possible column names
                        spanish_col = row.get('SGE Column Name') or row.get('Spanish Column Name') or row.get('Source Column')
                        english_col = row.get('English Column Name') or row.get('Target Column') or row.get('English Name')
                        field_type = row.get('Field type') or row.get('Data Type') or row.get('Type')
                        
                        if spanish_col and english_col:
                            mappings.append({
                                'spanish_name': spanish_col.strip(),
                                'english_name': english_col.strip(),
                                'field_type': field_type.strip() if field_type else 'String'
                            })
                else:
                    # Assume pipe-delimited and convert to CSV-like structure
                    lines = file.readlines()
                    if not lines:
                        raise ValueError("Empty dictionary file")
                    
                    # Parse header
                    header = [col.strip() for col in lines[0].strip().split('|')]
                    for line in lines[1:]:
                        if line.strip():  # Skip empty lines
                            values = [val.strip() for val in line.strip().split('|')]
                            if len(values) >= 3:  # At least 3 columns
                                row_dict = dict(zip(header, values))
                                spanish_col = row_dict.get('SGE Column Name') or (values[2] if len(values) > 2 else None)
                                english_col = row_dict.get('English Column Name') or (values[3] if len(values) > 3 else None)
                                field_type = row_dict.get('Field type') or (values[1] if len(values) > 1 else 'String')
                                
                                if spanish_col and english_col:
                                    mappings.append({
                                        'spanish_name': spanish_col.strip(),
                                        'english_name': english_col.strip(),
                                        'field_type': field_type.strip() if field_type else 'String'
                                    })
            
            # If we got here without exception and have mappings, we succeeded
            if mappings:
                break
                
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except Exception as e:
            # If it's not an encoding error, raise it
            raise Exception(f"Error reading dictionary file {dictionary_path}: {str(e)}")
    
    if not mappings:
        raise Exception(f"Could not parse dictionary file {dictionary_path} with any supported encoding")
    
    return mappings


def _get_sql_data_type(field_type: str) -> str:
    """Convert field type to SQL data type."""
    field_type = field_type.lower().strip()
    
    if field_type in ['number', 'numeric', 'float', 'decimal']:
        return 'FLOAT'
    elif field_type in ['int', 'integer']:
        return 'INT'
    elif field_type in ['date', 'datetime']:
        return 'NVARCHAR(MAX)'  # Keep as string for flexibility in date parsing
    elif field_type in ['bit', 'boolean', 'bool']:
        return 'BIT'
    else:
        return 'NVARCHAR(MAX)'  # Default for strings


def generate_stored_procedure(table_name: str, dictionary_path: str) -> str:
    # Function to generate a stored procedure based on the provided parameters
    # Always prefix stored procedure names with "stg"
    prefixed_sp_name = f"stg{table_name}" if not table_name.startswith("stg") else table_name
    
    # For the table reference in the SELECT statement, determine the proper table name
    # If the input table_name already starts with "stg", we assume it's a procedure name reference,
    # so we need to derive the table name by removing "stg" and adding "src"
    if table_name.startswith("stg"):
        # Remove "stg" prefix and add "src" prefix for table reference
        base_name = table_name[3:]  # Remove "stg" prefix
        prefixed_table_name = f"src{base_name}"
    else:
        # Normal case: add "src" prefix to table name
        prefixed_table_name = f"src{table_name}" if not table_name.startswith("src") else table_name
    
    try:
        # Parse the mapping file
        mappings = _parse_mapping_file(dictionary_path)
        
        if not mappings:
            raise ValueError("No column mappings found in dictionary file")
        
        # Generate CREATE TABLE statement for staging table
        create_table_columns = []
        for mapping in mappings:
            english_name = mapping['english_name']
            # Remove spaces from English column names
            clean_english_name = english_name.replace(' ', '')
            sql_type = _get_sql_data_type(mapping['field_type'])
            create_table_columns.append(f"        [{clean_english_name}] {sql_type}")
        
        # Add DATAAREAID column
        create_table_columns.append("        [DATAAREAID] NVARCHAR(4)")
        
        create_table_sql = ",\n".join(create_table_columns)
        
        # Generate INSERT column list (English names without spaces)
        insert_columns = [f"[{mapping['english_name'].replace(' ', '')}]" for mapping in mappings]
        insert_columns.append("[DATAAREAID]")
        insert_columns_sql = ", ".join(insert_columns)
        
        # Generate SELECT statement with column mappings
        select_mappings = []
        for mapping in mappings:
            spanish_name = mapping['spanish_name']
            english_name = mapping['english_name']
            # Clean the Spanish column name to match what was created in the source table
            clean_spanish_name = re.sub(r'[^a-zA-Z0-9_]', '_', spanish_name)
            if clean_spanish_name[0].isdigit():
                clean_spanish_name = f"Col_{clean_spanish_name}"
            
            # Remove spaces from English column names for the AS clause
            clean_english_name = english_name.replace(' ', '')
            select_mappings.append(f"        [{clean_spanish_name}] AS [{clean_english_name}]")
        
        # Add DATAAREAID mapping
        select_mappings.append("        'USMF' AS [DATAAREAID]")
        
        select_sql = ",\n".join(select_mappings)
        
        return f"""
CREATE PROCEDURE [dbo].[{prefixed_sp_name}_StoredProcedure]
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Drop staging table if it exists
    IF OBJECT_ID('dbo.{prefixed_sp_name}', 'U') IS NOT NULL
        DROP TABLE dbo.{prefixed_sp_name};

    -- Create staging table with English column names
    CREATE TABLE dbo.{prefixed_sp_name} (
{create_table_sql}
    );

    -- Insert data with column mapping from Spanish to English
    INSERT INTO dbo.{prefixed_sp_name} (
        {insert_columns_sql}
    )
    SELECT
{select_sql}
    FROM dbo.{prefixed_table_name};
    
    -- Log completion
    PRINT 'Data migration completed for {prefixed_sp_name}';
    PRINT 'Rows processed: ' + CAST(@@ROWCOUNT AS NVARCHAR(10));
END

-- Generated from dictionary: {dictionary_path}
-- Source table: dbo.{prefixed_table_name}
-- Target table: dbo.{prefixed_sp_name}
-- Columns mapped: {len(mappings)}
"""
    
    except Exception as e:
        # Fallback to basic stored procedure if mapping fails
        return f"""
-- ERROR: Could not parse dictionary file {dictionary_path}: {str(e)}
-- Creating basic stored procedure as fallback

CREATE PROCEDURE [dbo].[{prefixed_sp_name}_StoredProcedure]
AS
BEGIN
    SET NOCOUNT ON;

    -- Basic stored procedure logic (dictionary parsing failed)
    -- Dictionary path: {dictionary_path}
    SELECT * FROM dbo.{prefixed_table_name};
END

-- Please review the dictionary file and ensure it has the correct format
-- Expected columns: 'SGE Column Name', 'English Column Name', 'Field type'
"""