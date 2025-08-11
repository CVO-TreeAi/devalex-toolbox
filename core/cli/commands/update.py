"""DevAlex update command"""

import subprocess
import sys
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
        """Update project dependencies using smart dependency manager"""
        if not DevAlexConfig.is_devalex_project():
            print("  ℹ️ Not a DevAlex project, skipping dependency update")
            return
            
        try:
            # Import dependency manager when needed
            core_path = str(Path(__file__).parent.parent.parent)
            sys.path.insert(0, core_path)
            from dependency_management.manager import SmartDependencyManager
            
            dependency_manager = SmartDependencyManager()
            results = dependency_manager.update_all_dependencies()
            
            # Show summary
            successful = sum(1 for r in results.values() if r.get("status") == "success")
            total = len(results)
            
            print(f"\n📊 Dependency Update Summary:")
            print(f"   ✅ {successful}/{total} ecosystems updated successfully")
            
            if successful < total:
                failed = total - successful
                print(f"   ❌ {failed} ecosystems had issues")
                
        except Exception as e:
            print(f"  ⚠️ Smart dependency update failed: {e}")
            print("  Falling back to basic updates...")
            self._basic_dependency_update()
            
    def _basic_dependency_update(self):
        """Basic dependency updates as fallback"""
        # Update Python dependencies if present
        if Path("requirements.txt").exists():
            try:
                subprocess.run([
                    "pip", "install", "--upgrade", "-r", "requirements.txt"
                ], check=True, capture_output=True)
                print("  🐍 Python dependencies updated")
            except subprocess.CalledProcessError:
                print("  ⚠️ Python dependency update failed")
                
        # Update Node.js dependencies if present
        if Path("package.json").exists():
            try:
                subprocess.run(["npm", "update"], check=True, capture_output=True)
                print("  📦 Node.js dependencies updated")
            except subprocess.CalledProcessError:
                print("  ⚠️ Node.js dependency update failed")