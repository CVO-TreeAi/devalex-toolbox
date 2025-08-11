#!/usr/bin/env python3

"""
DevAlex Smart Dependency Management
Automatically manages dependencies across multiple ecosystems
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class SmartDependencyManager:
    """Smart dependency management across multiple ecosystems"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.dependency_config = self.project_path / ".devalex" / "dependencies.json"
        
    def detect_ecosystems(self) -> List[str]:
        """Detect which package ecosystems are present"""
        ecosystems = []
        
        ecosystem_files = {
            "package.json": "npm",
            "requirements.txt": "pip",
            "Pipfile": "pipenv", 
            "pyproject.toml": "poetry",
            "Cargo.toml": "cargo",
            "go.mod": "go",
            "pom.xml": "maven",
            "build.gradle": "gradle",
            "Gemfile": "bundler",
            "composer.json": "composer"
        }
        
        for filename, ecosystem in ecosystem_files.items():
            if (self.project_path / filename).exists():
                ecosystems.append(ecosystem)
                
        return ecosystems
        
    def update_all_dependencies(self) -> Dict[str, Any]:
        """Update dependencies across all detected ecosystems"""
        print("📦 DevAlex Smart Dependency Update")
        print("=" * 40)
        
        ecosystems = self.detect_ecosystems()
        results = {}
        
        for ecosystem in ecosystems:
            print(f"🔄 Updating {ecosystem} dependencies...")
            try:
                result = self._update_ecosystem(ecosystem)
                results[ecosystem] = {"status": "success", "details": result}
                print(f"  ✅ {ecosystem} updated successfully")
            except Exception as e:
                results[ecosystem] = {"status": "error", "error": str(e)}
                print(f"  ❌ {ecosystem} update failed: {e}")
                
        # Save update log
        self._save_update_log(results)
        
        return results
        
    def _update_ecosystem(self, ecosystem: str) -> str:
        """Update dependencies for specific ecosystem"""
        commands = {
            "npm": ["npm", "update"],
            "pip": ["pip", "install", "--upgrade", "-r", "requirements.txt"],
            "pipenv": ["pipenv", "update"],
            "poetry": ["poetry", "update"],
            "cargo": ["cargo", "update"],
            "go": ["go", "get", "-u", "all"],
            "maven": ["mvn", "versions:use-latest-releases"],
            "gradle": ["./gradlew", "refreshVersions"],
            "bundler": ["bundle", "update"],
            "composer": ["composer", "update"]
        }
        
        if ecosystem not in commands:
            raise ValueError(f"Unsupported ecosystem: {ecosystem}")
            
        cmd = commands[ecosystem]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        return result.stdout
        
    def check_security_vulnerabilities(self) -> Dict[str, Any]:
        """Check for security vulnerabilities across ecosystems"""
        print("🔒 DevAlex Security Vulnerability Check")
        print("=" * 40)
        
        ecosystems = self.detect_ecosystems()
        vulnerabilities = {}
        
        for ecosystem in ecosystems:
            print(f"🔍 Scanning {ecosystem} for vulnerabilities...")
            try:
                vulns = self._scan_ecosystem_security(ecosystem)
                vulnerabilities[ecosystem] = vulns
                if vulns:
                    print(f"  ⚠️ Found {len(vulns)} potential issues in {ecosystem}")
                else:
                    print(f"  ✅ No vulnerabilities found in {ecosystem}")
            except Exception as e:
                print(f"  ❌ Security scan failed for {ecosystem}: {e}")
                vulnerabilities[ecosystem] = {"error": str(e)}
                
        return vulnerabilities
        
    def _scan_ecosystem_security(self, ecosystem: str) -> List[Dict[str, Any]]:
        """Scan specific ecosystem for security issues"""
        security_commands = {
            "npm": ["npm", "audit", "--json"],
            "pip": ["safety", "check", "--json"] if self._command_exists("safety") else None,
            "cargo": ["cargo", "audit", "--json"] if self._command_exists("cargo-audit") else None,
            "go": ["nancy", "sleuth"] if self._command_exists("nancy") else None
        }
        
        cmd = security_commands.get(ecosystem)
        if not cmd:
            return []
            
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if ecosystem == "npm":
                audit_data = json.loads(result.stdout) if result.stdout else {}
                return audit_data.get("vulnerabilities", {})
            elif ecosystem == "pip" and result.returncode != 0:
                # Safety returns non-zero when vulnerabilities found
                return json.loads(result.stdout) if result.stdout else []
            else:
                return []
                
        except (subprocess.SubprocessError, json.JSONDecodeError):
            return []
            
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
            
    def _save_update_log(self, results: Dict[str, Any]):
        """Save dependency update log"""
        log_dir = self.project_path / ".devalex" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ecosystems": results,
            "project_path": str(self.project_path)
        }
        
        log_file = log_dir / f"dependency_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=2)
            
    def get_dependency_status(self) -> Dict[str, Any]:
        """Get current dependency status"""
        ecosystems = self.detect_ecosystems()
        
        status = {
            "detected_ecosystems": ecosystems,
            "total_ecosystems": len(ecosystems),
            "last_update": self._get_last_update_time(),
            "security_status": "unknown"
        }
        
        return status
        
    def _get_last_update_time(self) -> Optional[str]:
        """Get timestamp of last dependency update"""
        log_dir = self.project_path / ".devalex" / "logs"
        if not log_dir.exists():
            return None
            
        log_files = list(log_dir.glob("dependency_update_*.json"))
        if not log_files:
            return None
            
        latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
        try:
            with open(latest_log, 'r') as f:
                data = json.load(f)
            return data.get("timestamp")
        except (json.JSONDecodeError, FileNotFoundError):
            return None
            
    def install_security_tools(self) -> Dict[str, bool]:
        """Install security scanning tools for detected ecosystems"""
        print("🛡️ Installing security tools...")
        
        ecosystems = self.detect_ecosystems()
        results = {}
        
        security_tools = {
            "npm": [],  # npm audit is built-in
            "pip": ["safety"],
            "cargo": ["cargo-audit"],
            "go": ["nancy"]
        }
        
        for ecosystem in ecosystems:
            tools = security_tools.get(ecosystem, [])
            if not tools:
                results[ecosystem] = True  # No additional tools needed
                continue
                
            for tool in tools:
                try:
                    if ecosystem == "pip":
                        subprocess.run(["pip", "install", tool], check=True, capture_output=True)
                    elif ecosystem == "cargo":
                        subprocess.run(["cargo", "install", tool], check=True, capture_output=True)
                    elif ecosystem == "go":
                        subprocess.run(["go", "install", f"github.com/sonatypecommunity/{tool}@latest"], 
                                     check=True, capture_output=True)
                    
                    results[f"{ecosystem}_{tool}"] = True
                    print(f"  ✅ Installed {tool} for {ecosystem}")
                    
                except subprocess.CalledProcessError as e:
                    results[f"{ecosystem}_{tool}"] = False
                    print(f"  ❌ Failed to install {tool} for {ecosystem}: {e}")
                    
        return results