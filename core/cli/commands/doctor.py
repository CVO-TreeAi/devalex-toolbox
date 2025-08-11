"""DevAlex doctor command"""

import subprocess
import sys
from pathlib import Path
from .base import BaseCommand
from ..utils.config import DevAlexConfig

class DoctorCommand(BaseCommand):
    """Diagnose and fix DevAlex issues"""
    
    @classmethod
    def register(cls, subparsers):
        """Register doctor command"""
        parser = subparsers.add_parser('doctor', help='Diagnose and fix DevAlex issues')
        parser.add_argument('--fix', action='store_true', help='Automatically fix issues when possible')
        return parser
    
    def execute(self, args):
        """Execute doctor command"""
        print("🩺 DevAlex Doctor - Diagnosing system...")
        print("="*50)
        
        issues_found = 0
        issues_fixed = 0
        
        # Check Python version
        issues_found += self._check_python_version()
        
        # Check DevAlex installation
        issues_found += self._check_devalex_installation(args.fix)
        
        # Check dependencies
        issues_found += self._check_dependencies()
        
        # Check project structure (if in project)
        if DevAlexConfig.is_devalex_project():
            issues_found += self._check_project_structure(args.fix)
            
        # Check git status
        issues_found += self._check_git_status()
        
        # Summary
        print("\n" + "="*50)
        if issues_found == 0:
            print("🎉 DevAlex is healthy! Ready to build amazing things!")
        else:
            print(f"⚠️ Found {issues_found} issues.")
            if args.fix and issues_fixed > 0:
                print(f"🔧 Fixed {issues_fixed} issues automatically.")
            else:
                print("   Run with --fix to attempt automatic repairs.")
                
    def _check_python_version(self):
        """Check Python version"""
        print("🐍 Checking Python version...")
        
        python_version = sys.version_info
        if python_version < (3, 9):
            print(f"  ❌ Python {python_version.major}.{python_version.minor} is too old (need 3.9+)")
            print("     Install Python 3.9+ from python.org")
            return 1
        else:
            print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
            return 0
            
    def _check_devalex_installation(self, fix):
        """Check DevAlex installation"""
        print("🤖 Checking DevAlex installation...")
        
        if DevAlexConfig.is_installed():
            print("  ✅ DevAlex: Installed")
            return 0
        else:
            print("  ❌ DevAlex: Not installed")
            if fix:
                print("  🔧 Running automatic installation...")
                from .install import InstallCommand
                install_cmd = InstallCommand()
                try:
                    # Create a mock args object
                    class Args:
                        force = False
                    install_cmd.execute(Args())
                    print("  ✅ DevAlex installed successfully")
                    return 0
                except Exception as e:
                    print(f"  ❌ Installation failed: {e}")
                    return 1
            else:
                print("     Run: devalex install")
                return 1
                
    def _check_dependencies(self):
        """Check required dependencies"""
        print("📦 Checking dependencies...")
        
        issues = 0
        
        # Check for required Python packages
        required_packages = ['requests', 'pyyaml']
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package}: Available")
            except ImportError:
                print(f"  ❌ {package}: Missing")
                print(f"     Install with: pip install {package}")
                issues += 1
                
        return issues
        
    def _check_project_structure(self, fix):
        """Check project structure (if in DevAlex project)"""
        print("🏗️ Checking project structure...")
        
        issues = 0
        
        # Check for core directories
        required_dirs = ["core", "src"]
        for dir_name in required_dirs:
            if Path(dir_name).exists():
                print(f"  ✅ {dir_name}/: Present")
            else:
                print(f"  ❌ {dir_name}/: Missing")
                if fix:
                    Path(dir_name).mkdir(parents=True, exist_ok=True)
                    print(f"  🔧 Created: {dir_name}/")
                else:
                    issues += 1
                    
        # Check for DevAlex configuration
        if Path("devalex.json").exists():
            print("  ✅ devalex.json: Present")
        else:
            print("  ❌ devalex.json: Missing")
            print("     This might not be a DevAlex project")
            issues += 1
            
        return issues
        
    def _check_git_status(self):
        """Check git repository status"""
        print("📦 Checking git status...")
        
        if not Path(".git").exists():
            print("  ℹ️ Not a git repository")
            return 0
            
        try:
            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"], 
                capture_output=True, text=True, check=True
            )
            
            if result.stdout.strip():
                print("  ⚠️ Uncommitted changes present")
                print("     Consider committing your changes")
                return 1
            else:
                print("  ✅ Git repository: Clean")
                return 0
                
        except subprocess.CalledProcessError:
            print("  ❌ Git status check failed")
            return 1