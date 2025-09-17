# UV SQL Tool - Reusable Prompt Template

## Quick Setup Prompt

Use this prompt to create both a source table and staging stored procedure for D365 F&O data migration:

---

**PROMPT:**

Please help me create a complete data migration setup using the UV SQL Tool. I need:

1. **Create Source Table**: Generate a table from my pipe-delimited data file
2. **Create Staging Procedure**: Generate a stored procedure that maps Spanish column names to English column names

**My Files:**
- Data file: `[PATH_TO_YOUR_PIPE_DELIMITED_FILE]`
- Mapping dictionary: `[PATH_TO_YOUR_MAPPING_CSV_FILE]`
- Table name: `[YOUR_TABLE_NAME]`

**Requirements:**
- Source table should be prefixed with "src" (e.g., `srcItems`)
- Staging procedure should be prefixed with "stg" (e.g., `stgItems_StoredProcedure`)
- Column names in staging table should have no spaces
- Add DATAAREAID column with default value 'USMF'
- Skip execution (training mode) - just generate SQL files

**Expected Output:**
1. Source table SQL file: `src[TableName]_create_table_[timestamp].sql`
2. Staging procedure SQL file: `stg[TableName]_StoredProcedure.sql`

Please use the UV SQL Tool's `create_table` and `create_stored_procedure` functions.

---

## Example Usage

**For Items Civic Migration:**

Please help me create a complete data migration setup using the UV SQL Tool. I need:

1. **Create Source Table**: Generate a table from my pipe-delimited data file
2. **Create Staging Procedure**: Generate a stored procedure that maps Spanish column names to English column names

**My Files:**
- Data file: `Data/Samples/Items_cvic.txt`
- Mapping dictionary: `Data/Mapping/ItemCivicDictionary.csv`
- Table name: `ItemsCivic`

**Requirements:**
- Source table should be prefixed with "src" (e.g., `srcItemsCivic`)
- Staging procedure should be prefixed with "stg" (e.g., `stgItemsCivic_StoredProcedure`)
- Column names in staging table should have no spaces
- Add DATAAREAID column with default value 'USMF'
- Skip execution (training mode) - just generate SQL files

**Expected Output:**
1. Source table SQL file: `srcItemsCivic_create_table_[timestamp].sql`
2. Staging procedure SQL file: `stgItemsCivic_StoredProcedure.sql`

Please use the UV SQL Tool's `create_table` and `create_stored_procedure` functions.

---

## Command Line Alternative

If you prefer using the command line directly:

```bash
# Step 1: Create source table
uv-sql-tool call-tool create_table \
  --args '{
    "csv_file_path": "[PATH_TO_YOUR_PIPE_DELIMITED_FILE]",
    "table_name": "[YOUR_TABLE_NAME]"
  }'

# Step 2: Create staging procedure
uv-sql-tool call-tool create_stored_procedure \
  --args '{
    "table_name": "[YOUR_TABLE_NAME]",
    "dictionary_path": "[PATH_TO_YOUR_MAPPING_CSV_FILE]"
  }'
```

## File Structure Requirements

### Data File Format
- Pipe-delimited text file (|)
- First row contains column headers
- Subsequent rows contain data

### Mapping Dictionary Format
- CSV file with columns:
  - `SGE Column Name` (Spanish source column names)
  - `English Column Name` (target English column names)  
  - `Field type` (String, Number, Date, etc.)

## Generated Outputs

### Source Table Features
- Automatically detects data types from file content
- Cleans column names (replaces special characters with underscores)
- Adds "src" prefix to table name
- Includes detailed comments about source file and column mappings

### Staging Procedure Features
- Creates stored procedure with "stg" prefix
- Drops and recreates staging table
- Maps Spanish column names to English (without spaces)
- Adds DATAAREAID column with 'USMF' value
- Includes row count logging
- Comprehensive error handling

## Configuration

Make sure your `mcp.json` has:
```json
{
  "skip_execution": true,
  "description": "Configuration file for UV SQL Tool MCP Server",
  "settings": {
    "log_level": "INFO",
    "default_database": "D365Migration"
  }
}
```

## Tips

1. **File Paths**: Use relative paths from the workspace root
2. **Table Names**: Use PascalCase (e.g., ItemsCivic, CustomerData)
3. **Testing**: Always review generated SQL before executing in production
4. **Encoding**: Tool handles multiple file encodings automatically
5. **Spaces**: English column names will have spaces removed automatically

---

*Save this template and customize the bracketed placeholders for your specific migration needs.*
