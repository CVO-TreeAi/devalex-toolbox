# DevAlex Installation Guide

## Quick Installation

### One-Line Install
```bash
curl -sSL https://raw.githubusercontent.com/CVO-TreeAi/devalex-toolbox/main/install.sh | bash
```

### Manual Installation
```bash
git clone https://github.com/CVO-TreeAi/devalex-toolbox.git
cd devalex-toolbox
./install.sh
```

## Requirements

- **Python 3.9+** - Download from [python.org](https://python.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **Claude Code** - For optimal AI integration

## Installation Process

The installer will:

1. **Check Requirements** - Verify Python 3.9+ and Git
2. **Clone Repository** - Download DevAlex to `~/devalex-toolbox`
3. **Setup CLI** - Create `devalex` command
4. **Shell Integration** - Add to your PATH
5. **Install Dependencies** - Install Python packages
6. **System Setup** - Run `devalex install`

## Verification

After installation, verify everything works:

```bash
# Check version
devalex --version

# Check system status  
devalex status

# Run health check
devalex doctor
```

## Troubleshooting

### Permission Issues
If you see permission errors:
```bash
sudo ln -sf ~/devalex-toolbox/devalex /usr/local/bin/devalex
```

### Python Issues
If Python dependencies fail:
```bash
pip3 install --user requests pyyaml
```

### Shell Integration
If `devalex` command not found, add to shell config:
```bash
echo 'export PATH="$HOME/devalex-toolbox:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Uninstallation

To remove DevAlex:
```bash
rm -rf ~/devalex-toolbox ~/.devalex
rm -f /usr/local/bin/devalex
# Remove PATH entry from shell config
```

## Next Steps

1. **Initialize Project**: `devalex init my-project`
2. **Open Claude Code**: Start development
3. **Activate DevAlex**: Say "DevAlex" in Claude Code
4. **Build Amazing Things**: Let the three amigos work together!