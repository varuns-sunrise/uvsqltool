# UV SQL Tool - Publishing Setup (PowerShell)

Write-Host "🚀 UV SQL Tool - Publishing Setup" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "❌ Error: pyproject.toml not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Building the package..." -ForegroundColor Yellow
uv build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Build failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔍 Testing local installation..." -ForegroundColor Yellow
uv tool install --force .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Local installation successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Local installation failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Testing commands..." -ForegroundColor Yellow
& "$env:USERPROFILE\.local\bin\uv-sql-tool.exe" --version
& "$env:USERPROFILE\.local\bin\uv-sql-tool.exe" --help

Write-Host ""
Write-Host "📋 Next steps for GitHub publishing:" -ForegroundColor Cyan
Write-Host "1. Initialize git repository (if not done):" -ForegroundColor White
Write-Host "   git init" -ForegroundColor Gray
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Initial commit: UV SQL Tool with configurable credentials'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Create GitHub repository and push:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/varuns-sunrise/uvsqltool.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Create a release (optional):" -ForegroundColor White
Write-Host "   git tag v0.1.0" -ForegroundColor Gray
Write-Host "   git push origin v0.1.0" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Users can then install with:" -ForegroundColor White
Write-Host "   uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git" -ForegroundColor Gray
Write-Host ""
Write-Host "🎉 Your UV SQL Tool is ready for publishing!" -ForegroundColor Green
