#!/bin/bash

# DevAlex Agentic Toolbox Installation Script
# Install DevAlex globally for Claude Code enhancement

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
DEVALEX_REPO="https://github.com/CVO-TreeAi/devalex-toolbox.git"
INSTALL_DIR="$HOME/devalex-toolbox"
BIN_DIR="/usr/local/bin"

# Print banner
print_banner() {
    echo -e "${PURPLE}"
    echo "    ████████▄     ▄████████  ▄█    █▄       ▄████████  ▄█          ▄████████ ▀████    ▐████▀ "
    echo "    ███   ▀███   ███    ███ ███    ███     ███    ███ ███         ███    ███   ███▌   ████▀  "
    echo "    ███    ███   ███    █▀  ███    ███     ███    ███ ███         ███    █▀     ███  ▐███    "
    echo "    ███    ███  ▄███▄▄▄     ███    ███     ███    ███ ███        ▄███▄▄▄        ▀███▄███▀    "
    echo "    ███    ███ ▀▀███▀▀▀     ███    ███   ▀███████████ ███       ▀▀███▀▀▀        ████▀██▄     "
    echo "    ███    ███   ███    █▄  ███    ███     ███    ███ ███         ███    █▄    ▐███  ▀███    "
    echo "    ███   ▄███   ███    ███ ███    ███     ███    ███ ███▌    ▄   ███    ███  ▄███     ███▄  "
    echo "    ████████▀    ██████████  ▀██████▀      ███    █▀  █████▄▄██   ██████████ ████       ███▄ "
    echo "                                                      ▀                                      "
    echo -e "${NC}"
    echo -e "${CYAN}    🤖 Your Personal Claude Code Supercharger${NC}"
    echo -e "${CYAN}    Installing DevAlex Agentic Toolbox...${NC}"
    echo ""
}

# Check requirements
check_requirements() {
    echo -e "${BLUE}🔍 Checking system requirements...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is required but not installed${NC}"
        echo -e "${YELLOW}   Install Python 3.9+ from https://python.org${NC}"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ $(echo "$python_version < 3.9" | bc -l 2>/dev/null || echo "1") -eq 1 ]]; then
        echo -e "${RED}❌ Python $python_version found, but 3.9+ is required${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Python $python_version found${NC}"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git is required but not installed${NC}"
        echo -e "${YELLOW}   Install Git from https://git-scm.com${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Git found${NC}"
    
    echo ""
}

# Clone or update repository
install_devalex() {
    echo -e "${BLUE}📦 Installing DevAlex toolbox...${NC}"
    
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${YELLOW}⚠️  DevAlex already exists at $INSTALL_DIR${NC}"
        read -p "Do you want to update it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}🔄 Updating DevAlex...${NC}"
            cd "$INSTALL_DIR"
            git pull origin main
            echo -e "${GREEN}✅ DevAlex updated${NC}"
        else
            echo -e "${YELLOW}ℹ️  Using existing installation${NC}"
        fi
    else
        echo -e "${BLUE}📥 Cloning DevAlex repository...${NC}"
        git clone "$DEVALEX_REPO" "$INSTALL_DIR"
        echo -e "${GREEN}✅ DevAlex cloned${NC}"
    fi
    
    echo ""
}

# Make CLI executable
setup_cli() {
    echo -e "${BLUE}🔗 Setting up CLI...${NC}"
    
    # Make devalex script executable
    chmod +x "$INSTALL_DIR/devalex"
    echo -e "${GREEN}✅ CLI made executable${NC}"
    
    # Try to create symlink in /usr/local/bin
    if [ -w "$BIN_DIR" ]; then
        ln -sf "$INSTALL_DIR/devalex" "$BIN_DIR/devalex"
        echo -e "${GREEN}✅ Created symlink: $BIN_DIR/devalex${NC}"
    else
        echo -e "${YELLOW}⚠️  Cannot create symlink in $BIN_DIR (no permissions)${NC}"
        echo -e "${YELLOW}   You can create it manually with:${NC}"
        echo -e "${YELLOW}   sudo ln -sf $INSTALL_DIR/devalex $BIN_DIR/devalex${NC}"
    fi
    
    echo ""
}

# Add to shell configuration
setup_shell() {
    echo -e "${BLUE}🐚 Setting up shell integration...${NC}"
    
    # Determine shell config file
    if [ -n "$ZSH_VERSION" ] && [ -f "$HOME/.zshrc" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        echo -e "${YELLOW}⚠️  Could not find shell configuration file${NC}"
        echo -e "${YELLOW}   Add this to your shell config manually:${NC}"
        echo -e "${YELLOW}   export PATH=\"$INSTALL_DIR:\$PATH\"${NC}"
        return
    fi
    
    # Add to PATH if not already there
    if ! grep -q "devalex-toolbox" "$SHELL_CONFIG" 2>/dev/null; then
        echo "" >> "$SHELL_CONFIG"
        echo "# DevAlex Agentic Toolbox" >> "$SHELL_CONFIG"
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$SHELL_CONFIG"
        echo -e "${GREEN}✅ Added to $SHELL_CONFIG${NC}"
    else
        echo -e "${GREEN}✅ Already configured in $SHELL_CONFIG${NC}"
    fi
    
    echo ""
}

# Install Python dependencies
install_dependencies() {
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    
    # Install basic dependencies
    pip3 install --user requests pyyaml 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Could not install Python dependencies${NC}"
        echo -e "${YELLOW}   You may need to install them manually:${NC}"
        echo -e "${YELLOW}   pip3 install requests pyyaml${NC}"
    }
    
    echo -e "${GREEN}✅ Dependencies installed${NC}"
    echo ""
}

# Run DevAlex install
run_devalex_install() {
    echo -e "${BLUE}🚀 Running DevAlex installation...${NC}"
    
    # Run devalex install command
    "$INSTALL_DIR/devalex" install --force
    
    echo ""
}

# Print success message
print_success() {
    echo -e "${GREEN}🎉 DevAlex installation completed successfully!${NC}"
    echo ""
    echo -e "${CYAN}🔥 Next steps:${NC}"
    echo -e "   1. Restart your terminal or run: ${YELLOW}source ~/.zshrc${NC} (or your shell config)"
    echo -e "   2. Test installation: ${YELLOW}devalex --version${NC}"
    echo -e "   3. Create your first project: ${YELLOW}devalex init my-project${NC}"
    echo -e "   4. Open in Claude Code and say: ${YELLOW}DevAlex${NC}"
    echo ""
    echo -e "${PURPLE}🤖 The Three Amigos are ready: You + DevAlex + Claude Code${NC}"
    echo -e "${CYAN}Ready to build amazing things together! 🚀${NC}"
}

# Main installation process
main() {
    print_banner
    check_requirements
    install_devalex
    setup_cli
    setup_shell
    install_dependencies
    run_devalex_install
    print_success
}

# Run main function
main "$@"