"""DevAlex init command"""

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from .base import BaseCommand
from ..utils.config import DevAlexConfig

class InitCommand(BaseCommand):
    """Initialize new DevAlex project"""
    
    @classmethod
    def register(cls, subparsers):
        """Register init command"""
        parser = subparsers.add_parser('init', help='Initialize new DevAlex project')
        parser.add_argument('name', help='Project name')
        parser.add_argument('--type', default='webapp',
                          choices=['webapp', 'api', 'mobile', 'ai', 'custom'],
                          help='Project type (default: webapp)')
        parser.add_argument('--no-git', action='store_true',
                          help='Skip git repository initialization')
        return parser
    
    def execute(self, args):
        """Execute init command"""
        if not DevAlexConfig.is_installed():
            print("❌ DevAlex not installed. Run: devalex install")
            sys.exit(1)
            
        print(f"\n🚀 Initializing DevAlex project: {args.name}")
        print("="*60)
        
        # Create project directory
        project_dir = Path.cwd() / args.name
        if project_dir.exists():
            print(f"❌ Project directory '{args.name}' already exists!")
            sys.exit(1)
            
        project_dir.mkdir()
        print(f"📁 Created project directory: {project_dir}")
        
        # Copy project template
        self._copy_project_template(project_dir, args.type)
        
        # Create project configuration
        self._create_project_config(project_dir, args.name, args.type)
        
        # Create Claude Code integration
        self._create_claude_code_integration(project_dir, args.name)
        
        # Initialize git repository
        if not args.no_git:
            self._initialize_git(project_dir, args.name)
        
        # Setup project structure
        self._setup_project_structure(project_dir)
        
        print(f"\n🎉 DevAlex project '{args.name}' is ready!")
        print("="*60)
        print("🔥 Next steps:")
        print(f"   1. cd {args.name}")
        print("   2. Open in Claude Code")
        print("   3. Say 'DevAlex' to activate the three amigos!")
        print("   4. Start building amazing things together! 🚀")
        
    def _copy_project_template(self, project_dir, project_type):
        """Copy project template"""
        print(f"🎨 Setting up {project_type} project template...")
        
        template_dir = DevAlexConfig.TEMPLATES_DIR / project_type
        if not template_dir.exists():
            # Use basic template if specific type doesn't exist
            template_dir = DevAlexConfig.TEMPLATES_DIR / "basic"
            if not template_dir.exists():
                # Create basic structure if no templates exist
                self._create_basic_structure(project_dir)
                return
        
        # Copy template files
        for item in template_dir.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(template_dir)
                dest_path = project_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                
        print("📋 Project template copied successfully!")
        
    def _create_basic_structure(self, project_dir):
        """Create basic project structure when no template exists"""
        print("📋 Creating basic project structure...")
        
        # Create basic directories
        dirs = [
            "core/agents",
            "core/dependency-management", 
            "src",
            "tests",
            "docs"
        ]
        
        for dir_name in dirs:
            (project_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
        # Create basic files
        (project_dir / "README.md").write_text(f"# {project_dir.name}\n\nDevAlex-powered project")
        (project_dir / "src" / "__init__.py").touch()
        (project_dir / "tests" / "__init__.py").touch()
        
    def _create_project_config(self, project_dir, project_name, project_type):
        """Create project-specific configuration"""
        print("⚙️ Creating project configuration...")
        
        config = {
            "name": project_name,
            "type": project_type,
            "created_at": datetime.now().isoformat(),
            "devalex_version": DevAlexConfig.VERSION,
            "three_amigos": ["user", "devalex", "claude_code"],
            **DevAlexConfig.PROJECT_DEFAULTS
        }
        
        config_file = project_dir / "devalex.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"  ⚙️ Created: devalex.json")
        
    def _create_claude_code_integration(self, project_dir, project_name):
        """Create Claude Code integration files"""
        print("🤖 Creating Claude Code integration...")
        
        # Create .cursorrules file
        cursorrules_content = f"""# DevAlex + Claude Code Integration Rules for {project_name}

## 🤖 DevAlex Activation

**IMPORTANT**: When the user mentions ANY of these triggers, activate DevAlex mode:
- "DevAlex", "devalex", "DEVALEX"  
- "devalx", "devlex" (common typos)
- "dev alex" (spaced version)

### DevAlex Mode Behavior:
1. **Always work as the "Three Amigos"**: User + DevAlex + Claude Code
2. **Use agent orchestration**: Reference core/agents/ configurations
3. **Follow project patterns**: Maintain consistency across the codebase
4. **Be proactive**: Suggest improvements, catch issues, optimize continuously
5. **Quality first**: Never compromise on code quality or security

## 🚀 DevAlex System Integration

### Development Process
1. **Planning**: Architecture + Security + Testing coordination
2. **Development**: Full implementation with best practices
3. **Validation**: Quality assurance + Security validation
4. **Evolution**: Continuous learning and improvement

### Commands
When user says "DevAlex [command]", execute:
- "DevAlex status" → Check system health
- "DevAlex planr generate" → Generate development roadmap
- "DevAlex security scan" → Run security analysis
- "DevAlex components list" → Show available components

## 🔥 The Three Amigos Partnership

**You (Claude Code) + DevAlex + User = Unstoppable Development Team**

### Your Role (Claude Code):
- Execute technical implementation
- Provide expert coding assistance  
- Maintain code quality and patterns
- Integrate with DevAlex toolbox

### DevAlex's Role:
- Orchestrate development workflows
- Manage dependencies and security
- Provide project templates and tools
- Ensure quality and consistency

### User's Role:
- Provide requirements and direction
- Make business decisions
- Review and approve changes
- Guide the development process

## 💡 Always Remember:

1. **Context is King**: Always understand the project structure
2. **Tools are Helpers**: Use DevAlex tools for enhanced productivity
3. **Quality First**: Never compromise on code quality or security
4. **Learn and Improve**: Every interaction makes the system smarter
5. **Three Amigos**: We work together, not in isolation

---

**DevAlex Version**: {DevAlexConfig.VERSION}
**Project**: {project_name}
**Ready to build amazing things together!** 🚀🤖✨"""

        cursorrules_file = project_dir / ".cursorrules"
        cursorrules_file.write_text(cursorrules_content)
        print("  📋 Created: .cursorrules")
        
        # Create project context file
        context_file = project_dir / f"{project_name}-claude.md"
        context_content = f"""# {project_name} - DevAlex Project Context

## Project Overview
This is a DevAlex-powered {project_name} project initialized on {datetime.now().strftime('%Y-%m-%d')}.

## DevAlex Integration
- **Version**: {DevAlexConfig.VERSION}
- **Type**: {project_name}
- **Three Amigos**: User + DevAlex + Claude Code

## Project Structure
- `core/` - DevAlex core system integration
- `src/` - Application source code
- `tests/` - Test suite
- `docs/` - Documentation

## Getting Started
1. Say "DevAlex" to activate agent coordination
2. Use "devalex status" to check system health
3. Run "devalex planr generate" for development roadmaps

## Development Workflow
1. Plan features with DevAlex agents
2. Implement with Claude Code assistance
3. Test and validate automatically
4. Deploy with confidence

*Updated: {datetime.now().isoformat()}*"""

        context_file.write_text(context_content)
        print(f"  📄 Created: {project_name}-claude.md")
        
    def _initialize_git(self, project_dir, project_name):
        """Initialize git repository"""
        print("📦 Initializing git repository...")
        
        try:
            # Initialize git
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True, check=True)
            
            # Create .gitignore
            gitignore_content = """# DevAlex specific
.devalex/
devalex_monitor.log
*.db
cache/
temp/
logs/

# Language specific
__pycache__/
node_modules/
target/
.env
.venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db"""

            (project_dir / ".gitignore").write_text(gitignore_content)
            
            # Initial commit
            subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True, check=True)
            subprocess.run(["git", "commit", "-m", f"🚀 Initial DevAlex setup for {project_name}"], 
                         cwd=project_dir, capture_output=True, check=True)
            print("  📦 Git repository initialized with initial commit")
            
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Git initialization failed: {e}")
            print("  You can initialize git manually later")
            
    def _setup_project_structure(self, project_dir):
        """Set up additional project structure"""
        print("🏗️ Setting up project structure...")
        
        # Create core directories if they don't exist
        core_dirs = [
            "core/agents/workflows",
            "core/dependency-management", 
            "tools/planr",
            "integrations/claude-code"
        ]
        
        for dir_name in core_dirs:
            (project_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
        # Create placeholder files
        (project_dir / "core" / "__init__.py").touch()
        (project_dir / "tools" / "__init__.py").touch()
        
        print("  🏗️ Project structure ready")