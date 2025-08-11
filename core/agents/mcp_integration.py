#!/usr/bin/env python3

"""
DevAlex MCP Integration
Model Context Protocol integrations for enhanced tech validation
"""

import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class MCPIntegration:
    """MCP integration for tech stack validation"""
    
    def __init__(self):
        self.integrations = {
            "context7": self._context7_integration,
            "mcpref": self._mcpref_integration, 
            "semgrep": self._semgrep_integration
        }
        
    def validate_tech_stack(self, tech_stack: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tech stack using available MCP integrations"""
        validation_results = {
            "validated_by": [],
            "security_issues": [],
            "compatibility_warnings": [],
            "recommendations": [],
            "license_issues": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Try each MCP integration
        for integration_name, integration_func in self.integrations.items():
            try:
                result = integration_func(tech_stack)
                if result:
                    validation_results["validated_by"].append(integration_name)
                    validation_results = self._merge_results(validation_results, result)
            except Exception as e:
                print(f"  ⚠️ {integration_name} validation failed: {e}")
                
        return validation_results
        
    def _merge_results(self, base_results: Dict, new_results: Dict) -> Dict:
        """Merge validation results from different MCP sources"""
        for key in ["security_issues", "compatibility_warnings", "recommendations", "license_issues"]:
            if key in new_results:
                base_results[key].extend(new_results[key])
                
        return base_results
        
    def _context7_integration(self, tech_stack: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Context7 MCP integration for contextual tech validation"""
        try:
            # Check if context7 MCP is available
            context7_available = self._check_mcp_available("context7")
            if not context7_available:
                return None
                
            results = {
                "security_issues": [],
                "compatibility_warnings": [],
                "recommendations": []
            }
            
            # Validate each tech component through context7
            for category, tech in tech_stack.items():
                if tech and category not in ["tools", "compatibility_issues"]:
                    context_result = self._query_context7(f"security analysis {tech}")
                    if context_result:
                        # Parse context7 response for security concerns
                        if "vulnerability" in context_result.lower() or "security" in context_result.lower():
                            results["security_issues"].append(f"{tech}: {context_result[:100]}...")
                            
                        # Check for compatibility issues
                        if "deprecated" in context_result.lower() or "compatibility" in context_result.lower():
                            results["compatibility_warnings"].append(f"{tech}: May have compatibility issues")
                            
            return results if any(results.values()) else None
            
        except Exception as e:
            print(f"Context7 integration error: {e}")
            return None
            
    def _mcpref_integration(self, tech_stack: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """MCPRef integration for reference validation"""
        try:
            # Check if mcpref MCP is available
            mcpref_available = self._check_mcp_available("mcpref")
            if not mcpref_available:
                return None
                
            results = {
                "recommendations": [],
                "compatibility_warnings": []
            }
            
            # Query mcpref for each technology
            for category, tech in tech_stack.items():
                if tech and category not in ["tools", "compatibility_issues"]:
                    ref_result = self._query_mcpref(f"best practices {tech} {category}")
                    if ref_result:
                        results["recommendations"].append(f"{tech}: {ref_result[:100]}...")
                        
                        # Check for version compatibility warnings
                        if "version" in ref_result.lower() or "outdated" in ref_result.lower():
                            results["compatibility_warnings"].append(f"{tech}: Check version compatibility")
                            
            return results if any(results.values()) else None
            
        except Exception as e:
            print(f"MCPRef integration error: {e}")
            return None
            
    def _semgrep_integration(self, tech_stack: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Semgrep MCP integration for security analysis"""
        try:
            # Check if semgrep is available
            semgrep_available = self._check_semgrep_available()
            if not semgrep_available:
                return None
                
            results = {
                "security_issues": [],
                "recommendations": []
            }
            
            # Create temporary config for each technology
            for category, tech in tech_stack.items():
                if tech and category not in ["tools", "compatibility_issues"]:
                    security_issues = self._run_semgrep_tech_analysis(tech, category)
                    if security_issues:
                        results["security_issues"].extend(security_issues)
                        
            # Add general security recommendations
            security_recommendations = self._get_security_recommendations(tech_stack)
            results["recommendations"].extend(security_recommendations)
            
            return results if any(results.values()) else None
            
        except Exception as e:
            print(f"Semgrep integration error: {e}")
            return None
            
    def _check_mcp_available(self, mcp_name: str) -> bool:
        """Check if specific MCP integration is available"""
        try:
            # This is a placeholder - in real implementation, this would check
            # for MCP server availability via the MCP protocol
            result = subprocess.run(
                ["which", f"mcp-{mcp_name}"], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _check_semgrep_available(self) -> bool:
        """Check if Semgrep is available"""
        try:
            result = subprocess.run(
                ["semgrep", "--version"], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _query_context7(self, query: str) -> Optional[str]:
        """Query Context7 MCP server"""
        try:
            # Placeholder for actual MCP communication
            # In real implementation, this would use the MCP protocol
            # to communicate with the context7 server
            
            # Simulate context7 response based on query
            if "fastapi" in query.lower():
                return "FastAPI has good security practices but ensure proper input validation"
            elif "react" in query.lower():
                return "React requires careful XSS protection and dependency management"
            elif "postgresql" in query.lower():
                return "PostgreSQL is secure but ensure proper connection encryption"
                
            return None
        except Exception:
            return None
            
    def _query_mcpref(self, query: str) -> Optional[str]:
        """Query MCPRef MCP server"""
        try:
            # Placeholder for actual MCP communication
            # In real implementation, this would use the MCP protocol
            
            # Simulate mcpref response
            if "fastapi" in query.lower():
                return "FastAPI best practice: Use Pydantic models for validation and implement proper error handling"
            elif "react" in query.lower():
                return "React best practice: Use functional components with hooks and implement proper state management"
            elif "postgresql" in query.lower():
                return "PostgreSQL best practice: Use connection pooling and implement proper indexing strategies"
                
            return None
        except Exception:
            return None
            
    def _run_semgrep_tech_analysis(self, tech: str, category: str) -> List[str]:
        """Run Semgrep analysis for specific technology"""
        security_issues = []
        
        try:
            # Create technology-specific rules
            tech_rules = self._get_tech_security_rules(tech, category)
            
            if tech_rules:
                # In real implementation, this would run actual Semgrep analysis
                # For now, simulate based on technology
                if tech in ["react", "nextjs", "vue"]:
                    security_issues.append(f"{tech}: Ensure XSS protection is properly configured")
                    security_issues.append(f"{tech}: Validate all user inputs on frontend")
                    
                elif tech in ["fastapi", "django", "flask"]:
                    security_issues.append(f"{tech}: Implement proper CORS configuration")
                    security_issues.append(f"{tech}: Use parameterized queries to prevent SQL injection")
                    
                elif tech in ["postgresql", "mysql"]:
                    security_issues.append(f"{tech}: Ensure database connections are encrypted")
                    security_issues.append(f"{tech}: Implement proper access controls")
                    
        except Exception as e:
            print(f"Semgrep analysis error for {tech}: {e}")
            
        return security_issues
        
    def _get_tech_security_rules(self, tech: str, category: str) -> Optional[Dict]:
        """Get security rules for specific technology"""
        # This would return actual Semgrep rules in real implementation
        rules_map = {
            "react": {"rules": ["react-xss", "react-dangerous-props"]},
            "fastapi": {"rules": ["python-sql-injection", "python-cors-issues"]},
            "postgresql": {"rules": ["database-security", "sql-injection"]},
            "nextjs": {"rules": ["nextjs-security", "javascript-xss"]}
        }
        
        return rules_map.get(tech.lower())
        
    def _get_security_recommendations(self, tech_stack: Dict[str, Any]) -> List[str]:
        """Get general security recommendations for the tech stack"""
        recommendations = []
        
        # Frontend security
        if any(tech in str(tech_stack).lower() for tech in ["react", "vue", "angular", "nextjs"]):
            recommendations.append("Implement Content Security Policy (CSP) headers")
            recommendations.append("Use HTTPS for all production deployments")
            recommendations.append("Implement proper authentication and session management")
            
        # Backend security
        if any(tech in str(tech_stack).lower() for tech in ["fastapi", "django", "flask", "express"]):
            recommendations.append("Implement rate limiting to prevent abuse")
            recommendations.append("Use environment variables for sensitive configuration")
            recommendations.append("Implement proper logging and monitoring")
            
        # Database security
        if any(tech in str(tech_stack).lower() for tech in ["postgresql", "mysql", "mongodb"]):
            recommendations.append("Use database connection pooling")
            recommendations.append("Implement database backup and recovery procedures")
            recommendations.append("Use least privilege principle for database access")
            
        return recommendations
        
    def get_available_integrations(self) -> Dict[str, bool]:
        """Get status of available MCP integrations"""
        status = {}
        
        for integration_name in self.integrations.keys():
            if integration_name == "semgrep":
                status[integration_name] = self._check_semgrep_available()
            else:
                status[integration_name] = self._check_mcp_available(integration_name)
                
        return status