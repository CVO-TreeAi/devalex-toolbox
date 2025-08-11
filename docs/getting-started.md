# DevAlex Getting Started Guide

Welcome to DevAlex - your personal Claude Code supercharger!

## What is DevAlex?

DevAlex is an agentic toolbox that transforms your development environment into an AI-powered development powerhouse. It's designed specifically to enhance Claude Code workflows with:

- **AI Agent Orchestration** for complex development tasks
- **Automated Dependency Management** across all ecosystems  
- **AI-Powered Project Planning** with roadmap generation
- **Real-time Development Monitoring** and insights
- **Intelligent Component Libraries** for rapid development

## The Three Amigos Concept

DevAlex creates the perfect development trinity:

- **🧑‍💻 You**: Vision, requirements, and decision-making
- **🤖 DevAlex**: Agent coordination and system management
- **🎯 Claude Code**: Expert implementation and coding assistance

## Quick Start

### 1. Create Your First Project

```bash
devalex init my-awesome-project --type webapp
cd my-awesome-project
```

This creates a DevAlex-powered project with:
- Complete project structure
- Claude Code integration (`.cursorrules`)
- Agent orchestration setup
- Dependency management system

### 2. Open in Claude Code

Open your project in Claude Code. You'll see DevAlex has created:
- **`.cursorrules`**: Claude Code integration rules
- **`my-awesome-project-claude.md`**: Project context file
- **`devalex.json`**: Project configuration

### 3. Activate DevAlex

In Claude Code, simply say:
- **"DevAlex"** - Activate the three amigos
- **"DevAlex help me build a user authentication system"**
- **"DevAlex review the code quality"**
- **"DevAlex plan the next sprint"**

## Core Commands

### Project Management
```bash
devalex init <name>           # Initialize new project
devalex status               # Check system status
devalex update               # Update dependencies
devalex doctor               # Diagnose issues
```

### Tool Usage
```bash
devalex planr generate       # Generate development roadmap
devalex security scan        # Run security analysis
devalex components list      # List available components
devalex agents status        # Check agent system
```

## Development Workflow

### 1. Planning Phase
```bash
# Generate AI-powered roadmap
devalex planr generate --prd ./docs/requirements.md --tech-stack ./docs/tech.md
```

### 2. Development Phase
In Claude Code:
- Say **"DevAlex feature user-dashboard"**
- Watch agents coordinate implementation
- Get real-time assistance and code reviews

### 3. Quality Assurance
```bash
# Run comprehensive security scan
devalex security scan

# Check agent system health
devalex agents status

# Validate component consistency
devalex components validate
```

### 4. Deployment
```bash
# Update all dependencies
devalex update

# Run final health check
devalex doctor
```

## Project Structure

DevAlex creates this structure:

```
my-project/
├── .cursorrules              # Claude Code integration
├── devalex.json             # DevAlex configuration
├── my-project-claude.md     # Project context
├── core/                    # Core system
│   ├── agents/             # Agent configurations
│   └── dependency-management/
├── src/                     # Application code
├── tools/                   # DevAlex tool integrations
├── tests/                   # Test suite
└── docs/                    # Documentation
```

## Integration with Claude Code

DevAlex seamlessly integrates with Claude Code through:

### Activation Triggers
- "DevAlex", "devalex", "DEVALEX"
- "devalx", "devlex" (common typos)
- "dev alex" (spaced version)

### Context Awareness
- Project-specific `.cursorrules`
- Dynamic context files (`[folder]-claude.md`)
- Agent workflow integration

### Enhanced Workflows
- Feature development coordination
- Code quality reviews
- Security validation
- Architecture decisions

## Examples

### Build a Web App
```bash
devalex init ecommerce-site --type webapp
cd ecommerce-site
# Open in Claude Code
# Say: "DevAlex help me build a product catalog with search"
```

### Create an API
```bash
devalex init user-api --type api
cd user-api
# Open in Claude Code
# Say: "DevAlex create REST endpoints for user management"
```

### AI/ML Project
```bash
devalex init ml-pipeline --type ai
cd ml-pipeline
# Open in Claude Code
# Say: "DevAlex help me build a data processing pipeline"
```

## Best Practices

### 1. Start with Planning
Always begin with `devalex planr generate` for complex features

### 2. Use Agent Coordination
Let DevAlex agents handle their specialties:
- Architecture decisions
- Security reviews  
- Testing strategies
- Deployment planning

### 3. Keep Context Updated
DevAlex maintains context files - keep them current for best results

### 4. Regular Health Checks
Run `devalex doctor` regularly to catch issues early

### 5. Stay Updated
Use `devalex update` to keep dependencies current and secure

## Next Steps

1. **Explore Tools**: Try `devalex planr`, `devalex security`, `devalex components`
2. **Customize Agents**: Modify agent configurations in `core/agents/`
3. **Build Components**: Create reusable components with `devalex components generate`
4. **Monitor Progress**: Use the activity monitor for insights
5. **Join Community**: Share your experiences and improvements

## Getting Help

- **System Issues**: `devalex doctor`
- **Documentation**: Check `docs/` directory
- **Community**: GitHub Issues and Discussions
- **Claude Code Integration**: Say "DevAlex help" in Claude Code

---

**Ready to supercharge your development with the three amigos?** 🚀🤖✨