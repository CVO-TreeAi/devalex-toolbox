"""DevAlex install command"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from .base import BaseCommand
from ..utils.config import DevAlexConfig

class InstallCommand(BaseCommand):
    """Install DevAlex system"""
    
    @classmethod
    def register(cls, subparsers):
        """Register install command"""
        parser = subparsers.add_parser('install', help='Install DevAlex system')
        parser.add_argument('--force', action='store_true', 
                          help='Force reinstallation even if already installed')
        return parser
    
    def execute(self, args):
        """Execute install command"""
        if DevAlexConfig.is_installed() and not args.force:
            print("✅ DevAlex is already installed!")
            print("   Use --force to reinstall")
            return
            
        print("🚀 Installing DevAlex agentic toolbox...")
        print("="*50)
        
        # Ensure directories exist
        DevAlexConfig.ensure_directories()
        
        # Create system configuration
        self._create_system_config()
        
        # Copy templates from toolbox
        self._copy_templates()
        
        # Create CLI shortcuts
        self._create_cli_shortcuts()
        
        # Set up shell integration
        self._setup_shell_integration()
        
        print("✅ DevAlex system installed successfully!")
        print("\n🎉 Ready to supercharge your development!")
        print("    Run: devalex init my-project")
        
    def _create_system_config(self):
        """Create DevAlex system configuration"""
        print("⚙️ Creating system configuration...")
        
        config = {
            "version": DevAlexConfig.VERSION,
            "installed_at": datetime.now().isoformat(),
            "user": os.getenv("USER", "developer"),
            "toolbox_path": str(DevAlexConfig.TOOLBOX_ROOT),
            "system": {
                "auto_updates": True,
                "claude_code_integration": True,
                "agent_orchestration": True,
                "dependency_management": True
            },
            "project_defaults": DevAlexConfig.PROJECT_DEFAULTS,
            "triggers": DevAlexConfig.TRIGGERS
        }
        
        config_file = DevAlexConfig.CONFIG_DIR / "devalex.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"  ⚙️ Config created: {config_file}")
        
    def _copy_templates(self):
        """Copy project templates"""
        print("📋 Setting up project templates...")
        
        source_templates = DevAlexConfig.TOOLBOX_ROOT / "core" / "project-templates"
        if source_templates.exists():
            for template_dir in source_templates.iterdir():
                if template_dir.is_dir():
                    dest_dir = DevAlexConfig.TEMPLATES_DIR / template_dir.name
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)
                    shutil.copytree(template_dir, dest_dir)
                    print(f"  📋 Template: {template_dir.name}")
        
    def _create_cli_shortcuts(self):
        """Create CLI shortcuts for easy access"""
        print("🔗 Creating CLI shortcuts...")
        
        # Get the devalex script path
        devalex_script = DevAlexConfig.TOOLBOX_ROOT / "devalex"
        
        # Try to create symlink in /usr/local/bin
        try:
            symlink_path = Path("/usr/local/bin/devalex")
            if symlink_path.exists():
                symlink_path.unlink()
            symlink_path.symlink_to(devalex_script)
            print("  🔗 Created: /usr/local/bin/devalex")
        except PermissionError:
            print("  ⚠️ Cannot create /usr/local/bin symlink (no permissions)")
            print(f"     You can run: {devalex_script}")
            
    def _setup_shell_integration(self):
        """Set up shell integration"""
        print("🐚 Setting up shell integration...")
        
        # Shell configuration files to try
        shell_configs = [
            DevAlexConfig.HOME_DIR / ".zshrc",
            DevAlexConfig.HOME_DIR / ".bash_profile", 
            DevAlexConfig.HOME_DIR / ".bashrc"
        ]
        
        devalex_script = DevAlexConfig.TOOLBOX_ROOT / "devalex"
        alias_line = f'alias devalex="{devalex_script}"'
        
        for config_file in shell_configs:
            if config_file.exists():
                # Check if alias already exists
                content = config_file.read_text()
                if "alias devalex=" not in content:
                    with open(config_file, 'a') as f:
                        f.write(f"\n# DevAlex CLI shortcut\n{alias_line}\n")
                    print(f"  🐚 Added alias to: {config_file.name}")
                else:
                    print(f"  ✅ Alias already exists in: {config_file.name}")
                break