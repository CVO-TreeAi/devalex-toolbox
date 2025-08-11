"""DevAlex update command"""

import subprocess
from pathlib import Path
from .base import BaseCommand
from ..utils.config import DevAlexConfig

class UpdateCommand(BaseCommand):
    """Update DevAlex system and dependencies"""
    
    @classmethod
    def register(cls, subparsers):
        """Register update command"""
        parser = subparsers.add_parser('update', help='Update DevAlex system and dependencies')
        parser.add_argument('--system', action='store_true', help='Update DevAlex system only')
        parser.add_argument('--deps', action='store_true', help='Update project dependencies only')
        return parser
    
    def execute(self, args):
        """Execute update command"""
        print("🔄 DevAlex Update Manager")
        print("="*30)
        
        if not args.deps:
            self._update_system()
            
        if not args.system and DevAlexConfig.is_devalex_project():
            self._update_project_dependencies()
            
        print("✅ Update completed!")
        
    def _update_system(self):
        """Update DevAlex system"""
        print("🚀 Updating DevAlex system...")
        
        # Check if we're in a git repository (for development)
        if (DevAlexConfig.TOOLBOX_ROOT / ".git").exists():
            try:
                subprocess.run(["git", "pull"], cwd=DevAlexConfig.TOOLBOX_ROOT, check=True)
                print("  📦 DevAlex system updated from git")
            except subprocess.CalledProcessError:
                print("  ⚠️ Could not update from git")
        else:
            print("  ℹ️ System update not available (not a git repository)")
            
    def _update_project_dependencies(self):
        """Update project dependencies"""
        print("📦 Updating project dependencies...")
        
        # Update Python dependencies if present
        if Path("requirements.txt").exists():
            try:
                subprocess.run([
                    "pip", "install", "--upgrade", "-r", "requirements.txt"
                ], check=True)
                print("  🐍 Python dependencies updated")
            except subprocess.CalledProcessError:
                print("  ⚠️ Python dependency update failed")
                
        # Update Node.js dependencies if present
        if Path("package.json").exists():
            try:
                subprocess.run(["npm", "update"], check=True)
                print("  📦 Node.js dependencies updated")
            except subprocess.CalledProcessError:
                print("  ⚠️ Node.js dependency update failed")
                
        # Update Rust dependencies if present
        if Path("Cargo.toml").exists():
            try:
                subprocess.run(["cargo", "update"], check=True)
                print("  🦀 Rust dependencies updated")
            except subprocess.CalledProcessError:
                print("  ⚠️ Rust dependency update failed")