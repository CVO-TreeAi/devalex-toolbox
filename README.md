# DevAlex Agentic Toolbox

**Your Personal Claude Code Supercharger**

DevAlex is a modular agentic toolbox that transforms any development environment into an AI-powered development powerhouse. Built specifically to enhance Claude Code workflows with intelligent agents, automated dependency management, and seamless project orchestration.

## 🚀 Quick Start

### Installation
```bash
# Install DevAlex globally
curl -sSL https://raw.githubusercontent.com/CVO-TreeAi/devalex-toolbox/main/install.sh | bash

# Or clone and install
git clone https://github.com/CVO-TreeAi/devalex-toolbox.git
cd devalex-toolbox
./install.sh
```

### Initialize Your First Project
```bash
devalex init my-awesome-project --type webapp
cd my-awesome-project
# Open in Claude Code and say "DevAlex, let's build!"
```

## 🎯 What is DevAlex?

DevAlex is **not just another tool** - it's your personal agentic development ecosystem that:

- **Orchestrates AI Agents** for complex development tasks
- **Manages Dependencies** automatically across all ecosystems
- **Generates Project Roadmaps** with AI-powered planning
- **Monitors Development Activity** in real-time
- **Integrates with Claude Code** for seamless AI workflows
- **Provides Component Libraries** for rapid development

## 🛠️ Core Tools

### 🤖 Agent Orchestration
Coordinate 6 specialized AI agents for complete development workflows:
- **Architecture Agent**: System design and patterns
- **Development Agent**: Full-stack implementation  
- **Testing Agent**: Comprehensive QA and testing
- **Security Agent**: Security review and validation
- **Operations Agent**: Deployment and infrastructure
- **Orchestrator Agent**: Multi-agent coordination

### 📋 Planr - AI Roadmap Generator
Transform PRDs and tech specs into detailed development roadmaps:
- Context-aware planning for large language models
- Automatic story-point estimation and batching
- Phase-based development with iterative builds
- Integration with existing project workflows

### 📦 Smart Dependency Management
Automated dependency management across ecosystems:
- Python (pip), Node.js (npm/yarn), Rust (cargo), Go (mod)
- Automated security scanning and vulnerability fixes
- Smart conflict resolution and update scheduling
- Zero-maintenance dependency updates

### 📊 Activity Monitor
Real-time development activity tracking:
- Tauri-based desktop application
- WebSocket real-time updates
- Productivity metrics and insights
- Integration with development tools

### 🧩 Component Library
Reusable component system with intelligent registry:
- Pattern recognition and suggestion
- Template generation and customization
- Cross-project component sharing
- Integration with Logic Registry

## 🔧 Integrations

### Claude Code (Primary)
- Custom `.cursorrules` generation
- Context file management (`[folder]-claude.md`)
- Agent workflow triggers
- Seamless AI development workflows

### IDEs & Editors
- VS Code extension
- Cursor integration
- Universal language server support

### Development Tools
- GitHub (issues, PRs, actions)
- Linear (project management)
- Slack/Discord notifications

## 🏗️ Architecture

```
devalex-toolbox/
├── core/                  # Core DevAlex system
│   ├── cli/              # Command-line interface
│   ├── agents/           # Agent orchestration
│   ├── dependency-management/  # Smart dependency handling
│   └── project-templates/      # Project initialization
├── tools/                # Modular tools
│   ├── planr/           # AI roadmap generator
│   ├── activity-monitor/ # Development tracking
│   ├── component-library/ # Component system
│   └── security-scanner/ # Security analysis
├── integrations/         # Third-party integrations
└── docs/                # Comprehensive documentation
```

## 🎮 Usage

### Basic Commands
```bash
# Project management
devalex init <name>           # Initialize new project
devalex status               # Check system status
devalex update               # Update dependencies

# Tool usage
devalex planr generate       # Generate development roadmap
devalex security scan        # Run security analysis
devalex components list      # List available components

# Agent coordination
devalex agents status        # Check agent system
devalex workflow run <name>  # Execute agent workflow
```

### Claude Code Integration
1. Initialize project with DevAlex
2. Open in Claude Code
3. Say "DevAlex" to activate agent coordination
4. Watch AI agents collaborate on your project

## 🚀 The Three Amigos

DevAlex creates the perfect development trinity:

- **You**: Vision, requirements, and decision-making
- **DevAlex**: Agent coordination and system management
- **Claude Code**: Expert implementation and coding assistance

Together, this creates an unstoppable development team that combines human creativity with AI-powered efficiency.

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Getting Started](docs/getting-started.md)
- [Tool Documentation](docs/tools/)
- [Integration Guides](docs/integrations/)
- [API Reference](docs/api/)

## 🤝 Contributing

DevAlex is designed for personal use but welcomes contributions:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with love for the Claude Code community and AI-native development.

---

**DevAlex v1.0.0** - *The Three Amigos: You + DevAlex + Claude Code*