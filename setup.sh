#!/bin/bash
# Setup script for clocky - remote clock wrapper

echo "Setting up clocky..."
echo ""

# Create a symlink in ~/.local/bin or /usr/local/bin
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/clocky.py"

# Try to create in ~/.local/bin first
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$SCRIPT_PATH" "$HOME/.local/bin/clocky"
    echo "✓ Created symlink: $HOME/.local/bin/clocky"
    echo ""
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        echo "✓ $HOME/.local/bin is in your PATH"
    else
        echo "⚠ Add $HOME/.local/bin to your PATH to use 'clocky' command"
        echo "  Add this to your ~/.bashrc or ~/.zshrc:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
elif command -v sudo &> /dev/null; then
    sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/clocky
    echo "✓ Created symlink: /usr/local/bin/clocky (requires sudo)"
else
    echo "✗ Could not create symlink automatically"
    echo ""
    echo "Please manually create a symlink:"
    echo "  ln -s $SCRIPT_PATH ~/.local/bin/clocky"
    echo ""
    exit 1
fi

echo ""
echo "✓ Clocky has been installed!"
echo ""
echo "Get started with:"
echo "  clocky          # Show today's summary"
echo "  clocky week     # Show the week's summary"
echo "  clocky help     # Show all available commands"
echo ""
