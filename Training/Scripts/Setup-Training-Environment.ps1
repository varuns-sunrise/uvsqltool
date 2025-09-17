# UV SQL Tool - Training Environment Setup
# This script sets up a complete training environment for the UV SQL Tool

param(
    [switch]$ConfigureCredentials,
    [switch]$SkipVSCode,
    [switch]$SkipUV,
    [switch]$ValidateOnly,
    [switch]$NonInteractive,
    [string]$ConfigFile = "",
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
    Write-ColorOutput "🚀 $Title" -Color $Colors.Header
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
    Write-Header "UV SQL Tool - Training Environment Setup"
    Write-Host @"

This script sets up a complete training environment for the UV SQL Tool.

USAGE:
    .\Setup-Training-Environment.ps1 [OPTIONS]

OPTIONS:
    -ConfigureCredentials    Interactively configure SQL Server credentials
    -SkipVSCode             Skip VS Code installation and extension setup
    -SkipUV                 Skip UV package manager installation
    -ValidateOnly           Only validate the environment, don't make changes
    -NonInteractive         Run without user prompts (use defaults)
    -ConfigFile <path>      Specify a custom configuration file path
    -Help                   Show this help message

EXAMPLES:
    # Basic setup (recommended for first run)
    .\Setup-Training-Environment.ps1

    # Setup with interactive credential configuration
    .\Setup-Training-Environment.ps1 -ConfigureCredentials

    # Validation only (no changes made)
    .\Setup-Training-Environment.ps1 -ValidateOnly

    # Skip specific components
    .\Setup-Training-Environment.ps1 -SkipVSCode -SkipUV

"@
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
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

function Install-UVPackageManager {
    Write-Section "Installing UV Package Manager"
    
    if (Test-Command "uv") {
        $uvVersion = (uv --version 2>$null)
        Write-Success "UV is already installed: $uvVersion"
        return $true
    }
    
    if ($ValidateOnly) {
        Write-Error "UV package manager is not installed"
        return $false
    }
    
    Write-ColorOutput "📦 Installing UV package manager..." -Color $Colors.Info
    
    try {
        # Install UV using the recommended PowerShell method
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        if (Test-Command "uv") {
            $uvVersion = (uv --version 2>$null)
            Write-Success "UV installed successfully: $uvVersion"
            return $true
        } else {
            Write-Warning "UV installed but not found in PATH. You may need to restart your terminal."
            return $false
        }
    } catch {
        Write-Error "Failed to install UV: $_"
        Write-ColorOutput "Alternative installation methods:" -Color $Colors.Info
        Write-ColorOutput "  1. Using pip: pip install uv" -Color $Colors.Subtle
        Write-ColorOutput "  2. Using Scoop: scoop install uv" -Color $Colors.Subtle
        Write-ColorOutput "  3. Manual download from: https://github.com/astral-sh/uv/releases" -Color $Colors.Subtle
        return $false
    }
}

function Install-UVSQLTool {
    Write-Section "Installing UV SQL Tool"
    
    if (-not (Test-Command "uv")) {
        Write-Error "UV package manager is required but not found"
        return $false
    }
    
    try {
        # Check if tool is already installed
        $installedTools = uv tool list 2>$null
        if ($installedTools -match "uv-sql-tool") {
            Write-Success "UV SQL Tool is already installed"
            
            # Test the commands
            $uvSqlPath = Get-Command "uv-sql-tool" -ErrorAction SilentlyContinue
            if ($uvSqlPath) {
                $version = & $uvSqlPath.Source --version 2>$null
                Write-Success "UV SQL Tool version: $version"
                return $true
            }
        }
        
        if ($ValidateOnly) {
            Write-Error "UV SQL Tool is not installed"
            return $false
        }
        
        Write-ColorOutput "📦 Installing UV SQL Tool from GitHub..." -Color $Colors.Info
        
        # Install from GitHub
        uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "UV SQL Tool installed successfully"
            
            # Test the installation
            $uvSqlPath = Get-Command "uv-sql-tool" -ErrorAction SilentlyContinue
            if ($uvSqlPath) {
                $version = & $uvSqlPath.Source --version 2>$null
                Write-Success "Installation verified: $version"
                return $true
            } else {
                Write-Warning "Tool installed but not found in PATH. You may need to restart your terminal."
                return $false
            }
        } else {
            Write-Error "Failed to install UV SQL Tool"
            return $false
        }
    } catch {
        Write-Error "Error installing UV SQL Tool: $_"
        return $false
    }
}

function Test-VSCodeInstallation {
    Write-Section "Checking VS Code Installation"
    
    if (Test-Command "code") {
        $codeVersion = (code --version 2>$null | Select-Object -First 1)
        Write-Success "VS Code is installed: $codeVersion"
        return $true
    } else {
        if ($ValidateOnly -or $SkipVSCode) {
            Write-Warning "VS Code is not installed (skipped)"
            return $false
        }
        
        Write-ColorOutput "📝 VS Code not found. Installation recommendations:" -Color $Colors.Info
        Write-ColorOutput "  1. Using winget: winget install Microsoft.VisualStudioCode" -Color $Colors.Subtle
        Write-ColorOutput "  2. Using Chocolatey: choco install vscode" -Color $Colors.Subtle
        Write-ColorOutput "  3. Download from: https://code.visualstudio.com/" -Color $Colors.Subtle
        
        if (-not $NonInteractive) {
            $response = Read-Host "Would you like to install VS Code now? (y/N)"
            if ($response -eq "y" -or $response -eq "Y") {
                Install-VSCode
            }
        }
        return $false
    }
}

function Install-VSCode {
    Write-ColorOutput "📝 Installing VS Code..." -Color $Colors.Info
    
    try {
        if (Test-Command "winget") {
            winget install Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements
        } else {
            Write-Warning "winget not available. Please install VS Code manually from https://code.visualstudio.com/"
            return $false
        }
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        if (Test-Command "code") {
            Write-Success "VS Code installed successfully"
            return $true
        } else {
            Write-Warning "VS Code installed but not found in PATH. You may need to restart your terminal."
            return $false
        }
    } catch {
        Write-Error "Failed to install VS Code: $_"
        return $false
    }
}

function Install-VSCodeExtensions {
    Write-Section "Installing VS Code Extensions"
    
    if (-not (Test-Command "code")) {
        Write-Warning "VS Code not found, skipping extension installation"
        return $false
    }
    
    if ($ValidateOnly) {
        # Just check if extensions file exists
        if (Test-Path ".vscode\extensions.json") {
            Write-Success "VS Code extensions configuration found"
            return $true
        } else {
            Write-Warning "VS Code extensions configuration not found"
            return $false
        }
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
    $installCount = 0
    
    foreach ($extension in $requiredExtensions) {
        if ($installedExtensions -contains $extension) {
            Write-ColorOutput "  ✓ $extension" -Color $Colors.Success
        } else {
            Write-ColorOutput "  📦 Installing $extension..." -Color $Colors.Info
            code --install-extension $extension --force 2>$null
            if ($LASTEXITCODE -eq 0) {
                $installCount++
                Write-ColorOutput "  ✅ $extension installed" -Color $Colors.Success
            } else {
                Write-ColorOutput "  ❌ Failed to install $extension" -Color $Colors.Error
            }
        }
    }
    
    if ($installCount -gt 0) {
        Write-Success "Installed $installCount VS Code extensions"
    } else {
        Write-Success "All required VS Code extensions are already installed"
    }
    
    return $true
}

function Test-MCPConfiguration {
    Write-Section "Checking MCP Configuration"
    
    if (Test-Path ".vscode\mcp.json") {
        try {
            $mcpConfig = Get-Content ".vscode\mcp.json" | ConvertFrom-Json
            if ($mcpConfig.servers."uv-sql-tool") {
                Write-Success "MCP configuration found and valid"
                
                # Check if credentials are configured
                $env = $mcpConfig.servers."uv-sql-tool".env
                if ($env.SQL_SERVER -ne "your-server.database.windows.net") {
                    Write-Success "MCP configuration appears to be customized"
                } else {
                    Write-Warning "MCP configuration uses default values - credentials need to be configured"
                }
                return $true
            } else {
                Write-Warning "MCP configuration exists but UV SQL Tool server not found"
                return $false
            }
        } catch {
            Write-Error "MCP configuration file is invalid JSON: $_"
            return $false
        }
    } else {
        Write-Warning "MCP configuration file not found"
        if (-not $ValidateOnly) {
            Write-ColorOutput "Creating MCP configuration template..." -Color $Colors.Info
            Create-MCPConfiguration
        }
        return $false
    }
}

function Create-MCPConfiguration {
    if (-not (Test-Path ".vscode")) {
        New-Item -ItemType Directory -Path ".vscode" -Force | Out-Null
    }
    
    $mcpTemplate = @{
        servers = @{
            "uv-sql-tool" = @{
                command = "uvx"
                args = @("uv-sql-server")
                env = @{
                    SQL_SERVER = "your-server.database.windows.net"
                    SQL_DATABASE = "your_database"
                    SQL_USERNAME = "your_username"
                    SQL_PASSWORD = "your_password"
                    SQL_DRIVER = "ODBC Driver 17 for SQL Server"
                    SQL_PORT = ""
                    SQL_TRUSTED_CONNECTION = "false"
                    SQL_ENCRYPT = "true"
                    SQL_TRUST_SERVER_CERTIFICATE = "false"
                    SQL_CONNECTION_TIMEOUT = "30"
                    SQL_COMMAND_TIMEOUT = "30"
                }
            }
        }
    }
    
    $mcpTemplate | ConvertTo-Json -Depth 4 | Set-Content ".vscode\mcp.json"
    Write-Success "MCP configuration template created at .vscode\mcp.json"
}

function Configure-Credentials {
    Write-Section "Configuring SQL Server Credentials"
    
    if ($ValidateOnly) {
        Write-ColorOutput "Skipping credential configuration in validation mode" -Color $Colors.Info
        return $true
    }
    
    if ($NonInteractive) {
        Write-Warning "Skipping credential configuration in non-interactive mode"
        return $false
    }
    
    Write-ColorOutput "Please provide your SQL Server connection details:" -Color $Colors.Info
    
    $server = Read-Host "SQL Server (e.g., myserver.database.windows.net)"
    $database = Read-Host "Database name"
    $username = Read-Host "Username"
    $password = Read-Host "Password" -AsSecureString
    
    # Convert secure string to plain text
    $passwordText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    
    # Update MCP configuration
    if (Test-Path ".vscode\mcp.json") {
        try {
            $mcpConfig = Get-Content ".vscode\mcp.json" | ConvertFrom-Json
            $mcpConfig.servers."uv-sql-tool".env.SQL_SERVER = $server
            $mcpConfig.servers."uv-sql-tool".env.SQL_DATABASE = $database
            $mcpConfig.servers."uv-sql-tool".env.SQL_USERNAME = $username
            $mcpConfig.servers."uv-sql-tool".env.SQL_PASSWORD = $passwordText
            
            $mcpConfig | ConvertTo-Json -Depth 4 | Set-Content ".vscode\mcp.json"
            Write-Success "MCP configuration updated with your credentials"
            
            # Test the connection
            Write-ColorOutput "Testing connection..." -Color $Colors.Info
            $testResult = Test-SQLConnection -Server $server -Database $database -Username $username -Password $passwordText
            if ($testResult) {
                Write-Success "Connection test successful!"
            } else {
                Write-Warning "Connection test failed. Please verify your credentials."
            }
            
            return $true
        } catch {
            Write-Error "Failed to update MCP configuration: $_"
            return $false
        }
    } else {
        Write-Error "MCP configuration file not found"
        return $false
    }
}

function Test-SQLConnection {
    param(
        [string]$Server,
        [string]$Database, 
        [string]$Username,
        [string]$Password
    )
    
    try {
        if (Test-Command "uv-sql-tool") {
            $result = uv-sql-tool config test --server $Server --database $Database --username $Username --password $Password 2>$null
            return $LASTEXITCODE -eq 0
        } else {
            Write-Warning "UV SQL Tool not available for connection testing"
            return $false
        }
    } catch {
        return $false
    }
}

function Test-Prerequisites {
    Write-Section "Checking Prerequisites"
    
    $results = @{}
    
    # Check if running as administrator
    if (Test-Administrator) {
        Write-Success "Running as Administrator"
        $results.Administrator = $true
    } else {
        Write-Warning "Not running as Administrator - some operations may fail"
        $results.Administrator = $false
    }
    
    # Check Git
    if (Test-Command "git") {
        $gitVersion = (git --version 2>$null)
        Write-Success "Git is available: $gitVersion"
        $results.Git = $true
    } else {
        Write-Warning "Git not found - recommended for development"
        Write-ColorOutput "  Install with: winget install --id Git.Git -e" -Color $Colors.Subtle
        $results.Git = $false
    }
    
    # Check PowerShell version
    $psVersion = $PSVersionTable.PSVersion
    if ($psVersion.Major -ge 5) {
        Write-Success "PowerShell version: $psVersion"
        $results.PowerShell = $true
    } else {
        Write-Warning "PowerShell version $psVersion may not support all features"
        $results.PowerShell = $false
    }
    
    return $results
}

function Show-Summary {
    param([hashtable]$Results)
    
    Write-Header "Environment Setup Summary"
    
    $successCount = 0
    $totalCount = 0
    
    foreach ($key in $Results.Keys) {
        $totalCount++
        if ($Results[$key]) {
            $successCount++
            Write-Success "$key - Configured"
        } else {
            Write-Warning "$key - Needs attention"
        }
    }
    
    Write-Host ""
    Write-ColorOutput "Overall Status: $successCount/$totalCount components ready" -Color $Colors.Emphasis
    
    if ($successCount -eq $totalCount) {
        Write-Success "🎉 Your UV SQL Tool training environment is ready!"
        Write-Host ""
        Write-ColorOutput "Next steps:" -Color $Colors.Info
        Write-ColorOutput "1. Open this folder in VS Code: code ." -Color $Colors.Subtle
        Write-ColorOutput "2. Test the tool: uv-sql-tool --help" -Color $Colors.Subtle
        Write-ColorOutput "3. Configure your SQL Server credentials in .vscode\mcp.json" -Color $Colors.Subtle
        Write-ColorOutput "4. Start using the UV SQL Tool for your migrations!" -Color $Colors.Subtle
    } else {
        Write-Warning "Some components need attention. Please review the issues above."
        Write-Host ""
        Write-ColorOutput "For help:" -Color $Colors.Info
        Write-ColorOutput "- Run with -Help for detailed options" -Color $Colors.Subtle
        Write-ColorOutput "- Check the README.md for troubleshooting" -Color $Colors.Subtle
        Write-ColorOutput "- Visit: https://github.com/varuns-sunrise/uvsqltool" -Color $Colors.Subtle
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Header "UV SQL Tool - Training Environment Setup"

# Check basic prerequisites
$prereqResults = Test-Prerequisites

# Main setup flow
$setupResults = @{}

# UV Package Manager
if (-not $SkipUV) {
    $setupResults.UV = Install-UVPackageManager
    if ($setupResults.UV) {
        $setupResults.UVSQLTool = Install-UVSQLTool
    } else {
        $setupResults.UVSQLTool = $false
    }
} else {
    Write-Section "Skipping UV installation (as requested)"
    $setupResults.UV = Test-Command "uv"
    $setupResults.UVSQLTool = Test-Command "uv-sql-tool"
}

# VS Code and Extensions
if (-not $SkipVSCode) {
    $setupResults.VSCode = Test-VSCodeInstallation
    if ($setupResults.VSCode) {
        $setupResults.VSCodeExtensions = Install-VSCodeExtensions
    } else {
        $setupResults.VSCodeExtensions = $false
    }
} else {
    Write-Section "Skipping VS Code setup (as requested)"
    $setupResults.VSCode = Test-Command "code"
    $setupResults.VSCodeExtensions = $false
}

# MCP Configuration
$setupResults.MCPConfiguration = Test-MCPConfiguration

# Credential Configuration
if ($ConfigureCredentials) {
    $setupResults.Credentials = Configure-Credentials
} else {
    $setupResults.Credentials = $true # Don't fail on this
}

# Combine all results
$allResults = $prereqResults + $setupResults

# Show summary
Show-Summary -Results $allResults

# Exit with appropriate code
$failureCount = ($allResults.Values | Where-Object { $_ -eq $false }).Count
exit $failureCount
