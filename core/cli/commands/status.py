"""DevAlex status command"""

import json
from pathlib import Path
from .base import BaseCommand
from ..utils.config import DevAlexConfig

class StatusCommand(BaseCommand):
    """Show DevAlex system status"""
    
    @classmethod
    def register(cls, subparsers):
        """Register status command"""
        parser = subparsers.add_parser('status', help='Show DevAlex system status')
        return parser
    
    def execute(self, args):
        """Execute status command"""
        print("📊 DevAlex System Status")
        print("="*40)
        
        # Check system installation
        if DevAlexConfig.is_installed():
            print("✅ DevAlex system: Installed")
            
            config_file = DevAlexConfig.CONFIG_DIR / "devalex.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print(f"📦 Version: {config.get('version', 'Unknown')}")
                print(f"📅 Installed: {config.get('installed_at', 'Unknown')[:19]}")
            
            # Check templates
            templates = list(DevAlexConfig.TEMPLATES_DIR.glob("*")) if DevAlexConfig.TEMPLATES_DIR.exists() else []
            print(f"📋 Templates: {len(templates)} available")
            
        else:
            print("❌ DevAlex system: Not installed")
            print("   Run: devalex install")
            
        # Check current project
        if DevAlexConfig.is_devalex_project():
            print("\n🎯 Current Project Status")
            with open("devalex.json", 'r') as f:
                project_config = json.load(f)
            print(f"📁 Project: {project_config.get('name', 'Unknown')}")
            print(f"🏗️ Type: {project_config.get('type', 'Unknown')}")
            print(f"📅 Created: {project_config.get('created_at', 'Unknown')[:19]}")
            
            # Check agents status
            if Path("core/agents").exists():
                print("🤖 Agents: Ready")
            else:
                print("❌ Agents: Not configured")
                
        else:
            print("\n📁 Current Directory: Not a DevAlex project")
            print("   Run: devalex init <project-name>")