#!/bin/bash
# Setup script for publishing UV SQL Tool to GitHub

echo "🚀 UV SQL Tool - Publishing Setup"
echo "================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

echo "📦 Building the package..."
uv build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo ""
echo "🔍 Testing local installation..."
uv tool install --force .

if [ $? -eq 0 ]; then
    echo "✅ Local installation successful!"
else
    echo "❌ Local installation failed."
    exit 1
fi

echo ""
echo "🔧 Testing commands..."
uv-sql-tool --version
uv-sql-tool --help

echo ""
echo "📋 Next steps for GitHub publishing:"
echo "1. Initialize git repository (if not done):"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: UV SQL Tool with configurable credentials'"
echo ""
echo "2. Create GitHub repository and push:"
echo "   git remote add origin https://github.com/varuns-sunrise/uvsqltool.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Create a release (optional):"
echo "   git tag v0.1.0"
echo "   git push origin v0.1.0"
echo ""
echo "4. Users can then install with:"
echo "   uv tool install git+https://github.com/varuns-sunrise/uvsqltool.git"
echo ""
echo "🎉 Your UV SQL Tool is ready for publishing!"
