# UV SQL Tool - Environment Validation Script
# This script validates that all components are properly installed and configured

param(
    [switch]$Detailed,
    [switch]$Help
)

# Color definitions for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
    Emphasis = "White"
    Subtle = "Gray"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [switch]$NoNewline
    )
    
    if ($NoNewline) {
        Write-Host $Message -ForegroundColor $Color -NoNewline
    } else {
        Write-Host $Message -ForegroundColor $Color
    }
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-ColorOutput "🔍 $Title" -Color $Colors.Header
    Write-ColorOutput ("=" * ($Title.Length + 3)) -Color $Colors.Header
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-ColorOutput "📋 $Title" -Color $Colors.Info
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" -Color $Colors.Success
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" -Color $Colors.Warning
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" -Color $Colors.Error
}

function Show-Help {
    Write-Header "UV SQL Tool - Environment Validation"
    Write-Host @"

This script validates that your UV SQL Tool training environment is properly configured.

USAGE:
    .\Validate-Environment.ps1 [OPTIONS]

OPTIONS:
    -Detailed    Show detailed information about each component
    -Help        Show this help message

EXAMPLES:
    # Basic validation
    .\Validate-Environment.ps1

    # Detailed validation with full information
    .\Validate-Environment.ps1 -Detailed

"@
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Test-SystemRequirements {
    Write-Section "System Requirements"
    
    $results = @{}
    
    # Check PowerShell version
    $psVersion = $PSVersionTable.PSVersion
    if ($psVersion.Major -ge 5) {
        Write-Success "PowerShell version: $psVersion"
        $results.PowerShell = $true
    } else {
        Write-Error "PowerShell version $psVersion is too old (minimum 5.0 required)"
        $results.PowerShell = $false
    }
    
    # Check Windows version
    $osVersion = [System.Environment]::OSVersion.Version
    if ($osVersion.Major -ge 10) {
        Write-Success "Windows version: $($osVersion.ToString())"
        $results.WindowsVersion = $true
    } else {
        Write-Warning "Windows version: $($osVersion.ToString()) - Windows 10+ recommended"
        $results.WindowsVersion = $false
    }
    
    # Check .NET Framework
    try {
        $dotnetVersion = [System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
        Write-Success ".NET Framework: $dotnetVersion"
        $results.DotNet = $true
    } catch {
        Write-Warning ".NET Framework information not available"
        $results.DotNet = $false
    }
    
    return $results
}

function Test-CoreTools {
    Write-Section "Core Tools"
    
    $results = @{}
    
    # Test UV
    if (Test-Command "uv") {
        $uvVersion = (uv --version 2>$null)
        Write-Success "UV Package Manager: $uvVersion"
        $results.UV = $true
        
        if ($Detailed) {
            $uvInfo = uv --help 2>$null | Select-Object -First 5
            Write-ColorOutput "  UV Help Preview:" -Color $Colors.Subtle
            $uvInfo | ForEach-Object { Write-ColorOutput "    $_" -Color $Colors.Subtle }
        }
    } else {
        Write-Error "UV Package Manager not found"
        Write-ColorOutput "  Install with: irm https://astral.sh/uv/install.ps1 | iex" -Color $Colors.Subtle
        $results.UV = $false
    }
    
    # Test UV SQL Tool
    if (Test-Command "uv-sql-tool") {
        try {
            $uvSqlVersion = (uv-sql-tool --version 2>$null)
            Write-Success "UV SQL Tool: $uvSqlVersion"
            $results.UVSQLTool = $true
            
            if ($Detailed) {
                $uvSqlHelp = uv-sql-tool --help 2>$null | Select-Object -First 10
                Write-ColorOutput "  UV SQL Tool Commands:" -Color $Colors.Subtle
                $uvSqlHelp | ForEach-Object { Write-ColorOutput "    $_" -Color $Colors.Subtle }
            }
        } catch {
            Write-Error "UV SQL Tool found but not working properly"
            $results.UVSQLTool = $false
        }
    } else {
        Write-Error "UV SQL Tool not found"
        Write-ColorOutput "  Install with: uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git" -Color $Colors.Subtle
        $results.UVSQLTool = $false
    }
    
    # Test UV SQL Server
    if (Test-Command "uv-sql-server") {
        Write-Success "UV SQL Server: Available"
        $results.UVSQLServer = $true
    } else {
        Write-Error "UV SQL Server not found"
        $results.UVSQLServer = $false
    }
    
    return $results
}

function Test-DevelopmentTools {
    Write-Section "Development Tools"
    
    $results = @{}
    
    # Test Git
    if (Test-Command "git") {
        $gitVersion = (git --version 2>$null)
        Write-Success "Git: $gitVersion"
        $results.Git = $true
        
        if ($Detailed) {
            $gitConfig = git config --list 2>$null | Select-Object -First 5
            Write-ColorOutput "  Git Configuration (first 5 items):" -Color $Colors.Subtle
            $gitConfig | ForEach-Object { Write-ColorOutput "    $_" -Color $Colors.Subtle }
        }
    } else {
        Write-Warning "Git not found (recommended for development)"
        Write-ColorOutput "  Install with: winget install --id Git.Git -e" -Color $Colors.Subtle
        $results.Git = $false
    }
    
    # Test VS Code
    if (Test-Command "code") {
        $codeVersion = (code --version 2>$null | Select-Object -First 1)
        Write-Success "VS Code: $codeVersion"
        $results.VSCode = $true
        
        if ($Detailed) {
            $installedExtensions = code --list-extensions 2>$null | Measure-Object
            Write-ColorOutput "  VS Code Extensions: $($installedExtensions.Count) installed" -Color $Colors.Subtle
        }
    } else {
        Write-Warning "VS Code not found (recommended for development)"
        Write-ColorOutput "  Install with: winget install Microsoft.VisualStudioCode" -Color $Colors.Subtle
        $results.VSCode = $false
    }
    
    return $results
}

function Test-VSCodeExtensions {
    Write-Section "VS Code Extensions"
    
    $results = @{}
    
    if (-not (Test-Command "code")) {
        Write-Warning "VS Code not available - skipping extension check"
        return @{ VSCodeExtensions = $false }
    }
    
    $requiredExtensions = @(
        "ms-python.python",
        "ms-vscode.powershell", 
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-vscode.vscode-json",
        "ms-mssql.mssql"
    )
    
    $installedExtensions = code --list-extensions 2>$null
    $missingExtensions = @()
    $installedCount = 0
    
    foreach ($extension in $requiredExtensions) {
        if ($installedExtensions -contains $extension) {
            Write-Success "$extension"
            $installedCount++
        } else {
            Write-Warning "$extension - Not installed"
            $missingExtensions += $extension
        }
    }
    
    if ($missingExtensions.Count -eq 0) {
        Write-Success "All required extensions are installed"
        $results.VSCodeExtensions = $true
    } else {
        Write-Warning "$($missingExtensions.Count) required extensions missing"
        if ($Detailed) {
            Write-ColorOutput "  Missing extensions:" -Color $Colors.Subtle
            $missingExtensions | ForEach-Object { Write-ColorOutput "    $_" -Color $Colors.Subtle }
            Write-ColorOutput "  Install with: code --install-extension <extension-id>" -Color $Colors.Subtle
        }
        $results.VSCodeExtensions = $false
    }
    
    return $results
}

function Test-ProjectConfiguration {
    Write-Section "Project Configuration"
    
    $results = @{}
    
    # Check .vscode directory
    if (Test-Path ".vscode") {
        Write-Success ".vscode directory exists"
        $results.VSCodeDirectory = $true
    } else {
        Write-Warning ".vscode directory not found"
        $results.VSCodeDirectory = $false
    }
    
    # Check extensions.json
    if (Test-Path ".vscode\extensions.json") {
        try {
            $extensionsConfig = Get-Content ".vscode\extensions.json" | ConvertFrom-Json
            if ($extensionsConfig.recommendations) {
                Write-Success "VS Code extensions configuration: $($extensionsConfig.recommendations.Count) recommendations"
                $results.ExtensionsConfig = $true
            } else {
                Write-Warning "VS Code extensions configuration invalid"
                $results.ExtensionsConfig = $false
            }
        } catch {
            Write-Error "VS Code extensions configuration is invalid JSON"
            $results.ExtensionsConfig = $false
        }
    } else {
        Write-Warning "VS Code extensions configuration not found"
        $results.ExtensionsConfig = $false
    }
    
    # Check MCP configuration
    if (Test-Path ".vscode\mcp.json") {
        try {
            $mcpConfig = Get-Content ".vscode\mcp.json" | ConvertFrom-Json
            if ($mcpConfig.servers."uv-sql-tool") {
                Write-Success "MCP configuration found and valid"
                
                $env = $mcpConfig.servers."uv-sql-tool".env
                if ($env.SQL_SERVER -ne "your-server.database.windows.net") {
                    Write-Success "MCP credentials appear to be configured"
                    $results.MCPCredentials = $true
                } else {
                    Write-Warning "MCP credentials are using default values"
                    $results.MCPCredentials = $false
                }
                $results.MCPConfig = $true
            } else {
                Write-Warning "MCP configuration missing UV SQL Tool server"
                $results.MCPConfig = $false
                $results.MCPCredentials = $false
            }
        } catch {
            Write-Error "MCP configuration is invalid JSON: $_"
            $results.MCPConfig = $false
            $results.MCPCredentials = $false
        }
    } else {
        Write-Warning "MCP configuration not found"
        $results.MCPConfig = $false
        $results.MCPCredentials = $false
    }
    
    return $results
}

function Test-UVToolList {
    Write-Section "UV Tool Installation"
    
    $results = @{}
    
    if (-not (Test-Command "uv")) {
        Write-Warning "UV not available - skipping tool list check"
        return @{ UVToolList = $false }
    }
    
    try {
        $uvTools = uv tool list 2>$null
        if ($uvTools -match "uv-sql-tool") {
            Write-Success "UV SQL Tool is properly installed via UV"
            $results.UVToolList = $true
            
            if ($Detailed) {
                Write-ColorOutput "  UV Tool List:" -Color $Colors.Subtle
                $uvTools | ForEach-Object { Write-ColorOutput "    $_" -Color $Colors.Subtle }
            }
        } else {
            Write-Warning "UV SQL Tool not found in UV tool list"
            $results.UVToolList = $false
        }
    } catch {
        Write-Error "Failed to check UV tool list: $_"
        $results.UVToolList = $false
    }
    
    return $results
}

function Test-SQLServerConnectivity {
    Write-Section "SQL Server Connectivity"
    
    $results = @{}
    
    # Check if ODBC drivers are available
    try {
        $odbcDrivers = Get-OdbcDriver | Where-Object { $_.Name -like "*SQL Server*" }
        if ($odbcDrivers) {
            Write-Success "SQL Server ODBC drivers found: $($odbcDrivers.Count) drivers"
            $results.ODBCDrivers = $true
            
            if ($Detailed) {
                Write-ColorOutput "  Available ODBC Drivers:" -Color $Colors.Subtle
                $odbcDrivers | ForEach-Object { Write-ColorOutput "    $($_.Name)" -Color $Colors.Subtle }
            }
        } else {
            Write-Warning "No SQL Server ODBC drivers found"
            Write-ColorOutput "  Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server" -Color $Colors.Subtle
            $results.ODBCDrivers = $false
        }
    } catch {
        Write-Warning "Could not check ODBC drivers: $_"
        $results.ODBCDrivers = $false
    }
    
    # Test connection if credentials are configured
    if (Test-Path ".vscode\mcp.json") {
        try {
            $mcpConfig = Get-Content ".vscode\mcp.json" | ConvertFrom-Json
            $env = $mcpConfig.servers."uv-sql-tool".env
            
            if ($env.SQL_SERVER -ne "your-server.database.windows.net") {
                Write-ColorOutput "Testing SQL Server connection..." -Color $Colors.Info
                
                if (Test-Command "uv-sql-tool") {
                    $testResult = uv-sql-tool config test --config-file ".vscode\mcp.json" 2>$null
                    if ($LASTEXITCODE -eq 0) {
                        Write-Success "SQL Server connection test successful"
                        $results.SQLConnection = $true
                    } else {
                        Write-Warning "SQL Server connection test failed"
                        $results.SQLConnection = $false
                    }
                } else {
                    Write-Warning "Cannot test connection - UV SQL Tool not available"
                    $results.SQLConnection = $false
                }
            } else {
                Write-Warning "Cannot test connection - default credentials in use"
                $results.SQLConnection = $false
            }
        } catch {
            Write-Warning "Cannot test connection - MCP configuration error: $_"
            $results.SQLConnection = $false
        }
    } else {
        Write-Warning "Cannot test connection - no MCP configuration found"
        $results.SQLConnection = $false
    }
    
    return $results
}

function Show-ValidationSummary {
    param([hashtable]$AllResults)
    
    Write-Header "Validation Summary"
    
    $categories = @{
        "System Requirements" = @("PowerShell", "WindowsVersion", "DotNet")
        "Core Tools" = @("UV", "UVSQLTool", "UVSQLServer", "UVToolList")
        "Development Tools" = @("Git", "VSCode")
        "VS Code Configuration" = @("VSCodeExtensions", "VSCodeDirectory", "ExtensionsConfig")
        "MCP Configuration" = @("MCPConfig", "MCPCredentials")
        "SQL Server" = @("ODBCDrivers", "SQLConnection")
    }
    
    $overallSuccess = 0
    $overallTotal = 0
    
    foreach ($category in $categories.Keys) {
        $categoryItems = $categories[$category]
        $categorySuccess = 0
        $categoryTotal = $categoryItems.Count
        
        Write-Host ""
        Write-ColorOutput "📋 $category" -Color $Colors.Info
        
        foreach ($item in $categoryItems) {
            $overallTotal++
            if ($AllResults.ContainsKey($item)) {
                if ($AllResults[$item]) {
                    Write-Success "  $item"
                    $categorySuccess++
                    $overallSuccess++
                } else {
                    Write-Warning "  $item - Needs attention"
                }
            } else {
                Write-ColorOutput "  $item - Not checked" -Color $Colors.Subtle
            }
        }
        
        $categoryPercent = [math]::Round(($categorySuccess / $categoryTotal) * 100)
        Write-ColorOutput "  Category Status: $categorySuccess/$categoryTotal ($categoryPercent%)" -Color $Colors.Emphasis
    }
    
    Write-Host ""
    Write-Header "Overall Results"
    
    $overallPercent = [math]::Round(($overallSuccess / $overallTotal) * 100)
    Write-ColorOutput "Overall Status: $overallSuccess/$overallTotal components ready ($overallPercent%)" -Color $Colors.Emphasis
    
    if ($overallPercent -ge 90) {
        Write-Success "🎉 Excellent! Your environment is ready for UV SQL Tool training."
    } elseif ($overallPercent -ge 70) {
        Write-Warning "⚠️  Good! Your environment is mostly ready with some minor issues."
    } else {
        Write-Error "❌ Your environment needs significant setup before training."
    }
    
    Write-Host ""
    Write-ColorOutput "Next Steps:" -Color $Colors.Info
    if ($overallPercent -lt 100) {
        Write-ColorOutput "1. Run the setup script: .\scripts\Setup-Training-Environment.ps1" -Color $Colors.Subtle
        Write-ColorOutput "2. Address any remaining issues shown above" -Color $Colors.Subtle
        Write-ColorOutput "3. Re-run this validation script" -Color $Colors.Subtle
    } else {
        Write-ColorOutput "1. Open this folder in VS Code: code ." -Color $Colors.Subtle
        Write-ColorOutput "2. Start using UV SQL Tool: uv-sql-tool --help" -Color $Colors.Subtle
        Write-ColorOutput "3. Begin your training exercises!" -Color $Colors.Subtle
    }
    
    Write-Host ""
    Write-ColorOutput "For help:" -Color $Colors.Info
    Write-ColorOutput "- Setup guide: .\scripts\Setup-Training-Environment.ps1 -Help" -Color $Colors.Subtle
    Write-ColorOutput "- Documentation: README.md" -Color $Colors.Subtle
    Write-ColorOutput "- Repository: https://github.com/varuns-sunrise/uvsqltool" -Color $Colors.Subtle
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Header "UV SQL Tool - Environment Validation"

# Run all validation tests
$allResults = @{}

$systemResults = Test-SystemRequirements
$coreResults = Test-CoreTools
$devResults = Test-DevelopmentTools
$extensionResults = Test-VSCodeExtensions
$configResults = Test-ProjectConfiguration
$uvResults = Test-UVToolList
$sqlResults = Test-SQLServerConnectivity

# Combine all results
$allResults += $systemResults
$allResults += $coreResults
$allResults += $devResults
$allResults += $extensionResults
$allResults += $configResults
$allResults += $uvResults
$allResults += $sqlResults

# Show summary
Show-ValidationSummary -AllResults $allResults

# Exit with appropriate code based on critical components
$criticalComponents = @("UV", "UVSQLTool", "PowerShell")
$criticalFailures = 0
foreach ($component in $criticalComponents) {
    if ($allResults.ContainsKey($component) -and -not $allResults[$component]) {
        $criticalFailures++
    }
}

exit $criticalFailures
