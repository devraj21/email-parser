#!/bin/bash
# simple_install.sh - Simple installation without editable mode

echo "🔧 Installing dependencies directly..."

# Activate virtual environment
source .venv/bin/activate

# Install core dependencies
echo "Installing core dependencies..."
uv pip install extract-msg python-dateutil

# Install development dependencies
echo "Installing development dependencies..."
uv pip install pytest pytest-asyncio pytest-cov black isort flake8 mypy pre-commit types-python-dateutil

# Test the installation
echo "Testing installation..."
python -c "
try:
    import extract_msg
    print('✅ extract_msg installed successfully')
except ImportError:
    print('❌ extract_msg installation failed')

try:
    from src.email_parser.parser import EmailParser
    parser = EmailParser()
    print('✅ EmailParser imported successfully')
except ImportError as e:
    print(f'❌ EmailParser import failed: {e}')

print('Installation test completed!')
"

echo ""
echo "🎉 Installation completed!"
echo ""
echo "Next steps:"
echo "1. source .venv/bin/activate"
echo "2. python tests/test_basic.py"
echo "3. python -m src.email_parser.main"