#!/usr/bin/env python3

"""
DevAlex Tech Stack Advisor Agent
Intelligent technology stack recommendation and validation system
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
import subprocess
import re
from .mcp_integration import MCPIntegration
from .xml_prompts import XMLPromptTemplates

class TechStackAdvisor:
    """Intelligent tech stack advisor with learning capabilities"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.advisor_dir = Path.home() / ".devalex" / "tech_advisor"
        self.preferences_file = self.advisor_dir / "user_preferences.json"
        self.patterns_file = self.advisor_dir / "learned_patterns.json"
        self.compatibility_db = self.advisor_dir / "compatibility.json"
        
        # Ensure advisor directory exists
        self.advisor_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize MCP integration
        self.mcp_integration = MCPIntegration()
        
    def analyze_and_recommend(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user requirements and recommend optimal tech stack"""
        print("🔍 DevAlex Tech Stack Advisor")
        print("=" * 40)
        
        # Parse user requirements
        requirements = self._parse_requirements(user_input)
        
        # Load user preferences and patterns
        preferences = self._load_user_preferences()
        patterns = self._load_learned_patterns()
        
        # Analyze existing files in project
        project_context = self._analyze_project_context()
        
        # Generate tech stack recommendations
        recommendations = self._generate_recommendations(
            requirements, preferences, patterns, project_context
        )
        
        # Validate compatibility
        validated_stack = self._validate_compatibility(recommendations)
        
        # Fill in missing pieces
        complete_stack = self._fill_missing_pieces(validated_stack, requirements)
        
        # Check licenses and open source preference
        final_stack = self._apply_open_source_bias(complete_stack)
        
        # Validate with MCP integrations
        mcp_validation = self._validate_with_mcp(final_stack)
        
        # Learn from this interaction
        self._learn_from_interaction(requirements, final_stack)
        
        return {
            "recommended_stack": final_stack,
            "reasoning": self._generate_reasoning(final_stack, requirements),
            "alternatives": self._suggest_alternatives(final_stack),
            "warnings": self._check_compatibility_warnings(final_stack),
            "estimated_complexity": self._estimate_complexity(final_stack),
            "mcp_validation": mcp_validation
        }
        
    def _parse_requirements(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and normalize user requirements"""
        requirements = {
            "project_type": user_input.get("type", "webapp"),
            "target_devices": user_input.get("devices", ["web"]),
            "user_specified": {},
            "constraints": {},
            "preferences": {}
        }
        
        # Extract explicit tech mentions
        tech_mentions = user_input.get("description", "").lower()
        
        # Frontend frameworks
        frontend_patterns = {
            "react": ["react", "jsx", "tsx"],
            "vue": ["vue", "nuxt"],
            "svelte": ["svelte", "sveltekit"],
            "angular": ["angular", "@angular"],
            "nextjs": ["next.js", "nextjs", "next"],
            "remix": ["remix"],
            "solid": ["solidjs", "solid"]
        }
        
        # Backend frameworks
        backend_patterns = {
            "fastapi": ["fastapi", "fast api"],
            "django": ["django"],
            "flask": ["flask"],
            "express": ["express", "node.js", "nodejs"],
            "nestjs": ["nest.js", "nestjs"],
            "spring": ["spring", "spring boot"],
            "rails": ["rails", "ruby on rails"],
            "laravel": ["laravel"],
            "rust": ["rust", "actix", "warp", "axum"],
            "go": ["golang", "go", "gin", "echo"]
        }
        
        # Databases
        database_patterns = {
            "postgresql": ["postgres", "postgresql", "pg"],
            "mysql": ["mysql"],
            "mongodb": ["mongo", "mongodb"],
            "sqlite": ["sqlite"],
            "redis": ["redis"],
            "supabase": ["supabase"],
            "firebase": ["firebase", "firestore"],
            "planetscale": ["planetscale"],
            "turso": ["turso"],
            "neon": ["neon"]
        }
        
        # Cloud/Hosting
        hosting_patterns = {
            "vercel": ["vercel"],
            "netlify": ["netlify"], 
            "aws": ["aws", "amazon web services"],
            "gcp": ["google cloud", "gcp"],
            "azure": ["azure"],
            "railway": ["railway"],
            "fly.io": ["fly.io", "fly"],
            "render": ["render"],
            "cloudflare": ["cloudflare", "workers"]
        }
        
        # Detect mentioned technologies
        for category, patterns in [
            ("frontend", frontend_patterns),
            ("backend", backend_patterns),
            ("database", database_patterns),
            ("hosting", hosting_patterns)
        ]:
            for tech, keywords in patterns.items():
                if any(keyword in tech_mentions for keyword in keywords):
                    if category not in requirements["user_specified"]:
                        requirements["user_specified"][category] = []
                    requirements["user_specified"][category].append(tech)
                    
        # Detect constraints
        if "mobile" in tech_mentions or "ios" in tech_mentions or "android" in tech_mentions:
            requirements["target_devices"].append("mobile")
            
        if "desktop" in tech_mentions or "electron" in tech_mentions or "tauri" in tech_mentions:
            requirements["target_devices"].append("desktop")
            
        if "real-time" in tech_mentions or "websocket" in tech_mentions:
            requirements["constraints"]["realtime"] = True
            
        if "offline" in tech_mentions:
            requirements["constraints"]["offline"] = True
            
        return requirements
        
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load learned user preferences"""
        if not self.preferences_file.exists():
            return self._create_default_preferences()
            
        try:
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self._create_default_preferences()
            
    def _create_default_preferences(self) -> Dict[str, Any]:
        """Create default preferences with open source bias"""
        preferences = {
            "language_preferences": {
                "python": 0.9,
                "typescript": 0.8,
                "javascript": 0.7,
                "rust": 0.6,
                "go": 0.5
            },
            "framework_preferences": {
                "frontend": {
                    "react": 0.9,
                    "nextjs": 0.8,
                    "svelte": 0.7,
                    "vue": 0.6
                },
                "backend": {
                    "fastapi": 0.9,
                    "express": 0.8,
                    "nestjs": 0.7,
                    "django": 0.6
                }
            },
            "database_preferences": {
                "postgresql": 0.9,
                "sqlite": 0.8,
                "mongodb": 0.6
            },
            "hosting_preferences": {
                "vercel": 0.9,
                "railway": 0.8,
                "fly.io": 0.7,
                "render": 0.7,
                "netlify": 0.6
            },
            "open_source_bias": 0.9,
            "license_preferences": ["MIT", "Apache-2.0", "BSD-3-Clause"],
            "avoid_licenses": ["GPL", "AGPL"],
            "complexity_preference": "medium",  # simple, medium, complex
            "learning_rate": 0.1
        }
        
        # Save default preferences
        with open(self.preferences_file, 'w') as f:
            json.dump(preferences, f, indent=2)
            
        return preferences
        
    def _load_learned_patterns(self) -> Dict[str, Any]:
        """Load learned patterns from past projects"""
        if not self.patterns_file.exists():
            return {"successful_combinations": {}, "failed_combinations": {}, "usage_frequency": {}}
            
        try:
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"successful_combinations": {}, "failed_combinations": {}, "usage_frequency": {}}
            
    def _analyze_project_context(self) -> Dict[str, Any]:
        """Analyze existing files in project directory"""
        context = {
            "existing_files": [],
            "detected_languages": set(),
            "detected_frameworks": set(),
            "package_managers": set(),
            "config_files": []
        }
        
        # Scan for existing files
        for file_path in self.project_path.rglob("*"):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                context["existing_files"].append(str(file_path.relative_to(self.project_path)))
                
                # Detect languages by extension
                ext = file_path.suffix.lower()
                language_map = {
                    ".py": "python",
                    ".js": "javascript", 
                    ".ts": "typescript",
                    ".tsx": "typescript",
                    ".jsx": "javascript",
                    ".rs": "rust",
                    ".go": "go",
                    ".java": "java",
                    ".rb": "ruby",
                    ".php": "php"
                }
                
                if ext in language_map:
                    context["detected_languages"].add(language_map[ext])
                    
        # Detect package managers
        if (self.project_path / "package.json").exists():
            context["package_managers"].add("npm")
        if (self.project_path / "requirements.txt").exists():
            context["package_managers"].add("pip")
        if (self.project_path / "Cargo.toml").exists():
            context["package_managers"].add("cargo")
        if (self.project_path / "go.mod").exists():
            context["package_managers"].add("go")
            
        # Convert sets to lists for JSON serialization
        context["detected_languages"] = list(context["detected_languages"])
        context["detected_frameworks"] = list(context["detected_frameworks"])
        context["package_managers"] = list(context["package_managers"])
        
        return context
        
    def _generate_recommendations(self, requirements: Dict[str, Any], preferences: Dict[str, Any], 
                                patterns: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tech stack recommendations based on analysis"""
        recommendations = {
            "frontend": None,
            "backend": None,
            "database": None,
            "hosting": None,
            "tools": [],
            "confidence_scores": {}
        }
        
        project_type = requirements["project_type"]
        user_specified = requirements["user_specified"]
        devices = requirements["target_devices"]
        
        # Use user-specified technologies first
        for category in ["frontend", "backend", "database", "hosting"]:
            if category in user_specified and user_specified[category]:
                recommendations[category] = user_specified[category][0]  # Use first mentioned
                recommendations["confidence_scores"][category] = 0.9
                
        # Fill in missing pieces based on project type and preferences
        if not recommendations["frontend"] and project_type in ["webapp", "mobile"]:
            if "mobile" in devices:
                recommendations["frontend"] = "react-native"
            else:
                # Choose based on preferences
                frontend_prefs = preferences.get("framework_preferences", {}).get("frontend", {})
                recommendations["frontend"] = max(frontend_prefs.items(), key=lambda x: x[1])[0]
            recommendations["confidence_scores"]["frontend"] = 0.8
            
        if not recommendations["backend"]:
            # Choose based on detected languages or preferences
            if "python" in context["detected_languages"]:
                recommendations["backend"] = "fastapi"
            elif "typescript" in context["detected_languages"] or "javascript" in context["detected_languages"]:
                recommendations["backend"] = "express"
            else:
                backend_prefs = preferences.get("framework_preferences", {}).get("backend", {})
                recommendations["backend"] = max(backend_prefs.items(), key=lambda x: x[1])[0]
            recommendations["confidence_scores"]["backend"] = 0.7
            
        if not recommendations["database"]:
            # Choose based on project complexity and preferences
            db_prefs = preferences.get("database_preferences", {})
            if requirements.get("constraints", {}).get("realtime"):
                recommendations["database"] = "postgresql"  # Better for real-time
            else:
                recommendations["database"] = max(db_prefs.items(), key=lambda x: x[1])[0]
            recommendations["confidence_scores"]["database"] = 0.7
            
        if not recommendations["hosting"]:
            hosting_prefs = preferences.get("hosting_preferences", {})
            recommendations["hosting"] = max(hosting_prefs.items(), key=lambda x: x[1])[0]
            recommendations["confidence_scores"]["hosting"] = 0.6
            
        # Add essential tools based on stack
        recommendations["tools"] = self._suggest_tools(recommendations, requirements)
        
        return recommendations
        
    def _suggest_tools(self, stack: Dict[str, Any], requirements: Dict[str, Any]) -> List[str]:
        """Suggest essential tools based on tech stack"""
        tools = []
        
        # Version control (always)
        tools.append("git")
        
        # Package managers based on stack
        if stack["frontend"] in ["react", "nextjs", "vue", "svelte"]:
            tools.append("npm")
        if stack["backend"] in ["fastapi", "django", "flask"]:
            tools.append("pip")
        if stack["backend"] in ["express", "nestjs"]:
            tools.append("npm")
            
        # Development tools
        if "typescript" in str(stack).lower():
            tools.append("typescript")
            
        # Testing frameworks
        if stack["frontend"] in ["react", "nextjs"]:
            tools.append("jest")
            tools.append("testing-library")
        if stack["backend"] in ["fastapi", "django"]:
            tools.append("pytest")
        if stack["backend"] in ["express", "nestjs"]:
            tools.append("jest")
            
        # Linting and formatting
        tools.extend(["eslint", "prettier"] if "javascript" in str(stack) or "typescript" in str(stack) else [])
        tools.extend(["black", "flake8"] if stack["backend"] in ["fastapi", "django", "flask"] else [])
        
        # Deployment tools
        if stack["hosting"] == "vercel":
            tools.append("vercel-cli")
        elif stack["hosting"] == "railway":
            tools.append("railway-cli")
            
        # Database tools
        if stack["database"] == "postgresql":
            tools.append("psql")
        elif stack["database"] == "mongodb":
            tools.append("mongosh")
            
        return list(set(tools))  # Remove duplicates
        
    def _validate_compatibility(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Validate technology compatibility using known compatibility rules"""
        compatibility_issues = []
        validated_stack = recommendations.copy()
        
        # Load compatibility database
        compatibility_rules = self._load_compatibility_rules()
        
        # Check frontend-backend compatibility
        frontend = recommendations.get("frontend")
        backend = recommendations.get("backend")
        
        if frontend and backend:
            compatibility_key = f"{frontend}+{backend}"
            if compatibility_key in compatibility_rules.get("incompatible_combinations", []):
                compatibility_issues.append(f"{frontend} and {backend} have known compatibility issues")
                
        # Check database compatibility
        database = recommendations.get("database")
        if backend and database:
            # Check if backend supports database
            backend_db_support = compatibility_rules.get("backend_database_support", {})
            if backend in backend_db_support:
                supported_dbs = backend_db_support[backend]
                if database not in supported_dbs:
                    compatibility_issues.append(f"{backend} has limited support for {database}")
                    
        validated_stack["compatibility_issues"] = compatibility_issues
        return validated_stack
        
    def _load_compatibility_rules(self) -> Dict[str, Any]:
        """Load or create compatibility rules database"""
        if not self.compatibility_db.exists():
            return self._create_default_compatibility_rules()
            
        try:
            with open(self.compatibility_db, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self._create_default_compatibility_rules()
            
    def _create_default_compatibility_rules(self) -> Dict[str, Any]:
        """Create default compatibility rules"""
        rules = {
            "incompatible_combinations": [
                "react+django",  # Usually separate apps
                "vue+flask"      # Less common combination
            ],
            "backend_database_support": {
                "fastapi": ["postgresql", "mysql", "sqlite", "mongodb"],
                "django": ["postgresql", "mysql", "sqlite"],
                "flask": ["postgresql", "mysql", "sqlite", "mongodb"],
                "express": ["postgresql", "mysql", "mongodb", "sqlite"],
                "nestjs": ["postgresql", "mysql", "mongodb", "sqlite"]
            },
            "hosting_compatibility": {
                "vercel": ["nextjs", "react", "vue", "svelte", "express"],
                "netlify": ["react", "vue", "svelte", "gatsby"],
                "railway": ["fastapi", "django", "express", "nestjs"],
                "fly.io": ["fastapi", "django", "express", "nestjs", "rust", "go"]
            },
            "successful_combinations": [
                "react+fastapi+postgresql+vercel",
                "nextjs+postgresql+vercel", 
                "svelte+fastapi+sqlite+railway",
                "vue+express+mongodb+netlify"
            ]
        }
        
        with open(self.compatibility_db, 'w') as f:
            json.dump(rules, f, indent=2)
            
        return rules
        
    def _fill_missing_pieces(self, stack: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligently fill in missing tech stack pieces"""
        complete_stack = stack.copy()
        
        # Fill based on detected patterns and requirements
        project_type = requirements["project_type"]
        devices = requirements["target_devices"]
        constraints = requirements.get("constraints", {})
        
        # Add CSS framework if frontend is specified
        if complete_stack.get("frontend") and not complete_stack.get("css"):
            css_recommendations = {
                "react": "tailwindcss",
                "nextjs": "tailwindcss", 
                "vue": "tailwindcss",
                "svelte": "tailwindcss",
                "angular": "angular-material"
            }
            complete_stack["css"] = css_recommendations.get(complete_stack["frontend"], "tailwindcss")
            
        # Add state management for complex frontends
        if complete_stack.get("frontend") in ["react", "nextjs"] and project_type != "simple":
            complete_stack["state_management"] = "zustand"
        elif complete_stack.get("frontend") == "vue":
            complete_stack["state_management"] = "pinia"
            
        # Add ORM/Database layer
        if complete_stack.get("backend") and complete_stack.get("database"):
            orm_recommendations = {
                "fastapi": {"postgresql": "sqlalchemy", "sqlite": "sqlalchemy", "mongodb": "motor"},
                "django": {"postgresql": "django-orm", "mysql": "django-orm", "sqlite": "django-orm"},
                "express": {"postgresql": "prisma", "mysql": "prisma", "mongodb": "mongoose"},
                "nestjs": {"postgresql": "typeorm", "mysql": "typeorm", "mongodb": "mongoose"}
            }
            
            backend = complete_stack["backend"]
            database = complete_stack["database"]
            if backend in orm_recommendations and database in orm_recommendations[backend]:
                complete_stack["orm"] = orm_recommendations[backend][database]
                
        # Add authentication if not specified
        if not complete_stack.get("auth") and project_type in ["webapp", "mobile"]:
            if complete_stack.get("database") == "supabase":
                complete_stack["auth"] = "supabase-auth"
            elif complete_stack.get("database") == "firebase":
                complete_stack["auth"] = "firebase-auth"
            else:
                complete_stack["auth"] = "jwt"
                
        # Add real-time capabilities if required
        if constraints.get("realtime") and not complete_stack.get("realtime"):
            if complete_stack.get("backend") in ["fastapi", "express", "nestjs"]:
                complete_stack["realtime"] = "websockets"
            else:
                complete_stack["realtime"] = "sse"  # Server-Sent Events
                
        return complete_stack
        
    def _apply_open_source_bias(self, stack: Dict[str, Any]) -> Dict[str, Any]:
        """Apply open source bias and check licenses"""
        preferences = self._load_user_preferences()
        open_source_bias = preferences.get("open_source_bias", 0.9)
        
        if open_source_bias < 0.5:
            return stack  # User doesn't prefer open source
            
        # Check for proprietary alternatives and suggest open source
        open_source_alternatives = {
            "firebase": "supabase",
            "auth0": "supabase-auth",
            "mongodb-atlas": "postgresql",
            "vercel": "railway",  # Both good, but railway is more open
        }
        
        improved_stack = stack.copy()
        replacements = []
        
        for category, tech in stack.items():
            if tech and isinstance(tech, str) and tech in open_source_alternatives:
                alternative = open_source_alternatives[tech]
                improved_stack[category] = alternative
                replacements.append(f"Replaced {tech} with {alternative} (open source preference)")
                
        improved_stack["open_source_replacements"] = replacements
        return improved_stack
        
    def _learn_from_interaction(self, requirements: Dict[str, Any], final_stack: Dict[str, Any]):
        """Learn from user interaction to improve future recommendations"""
        patterns = self._load_learned_patterns()
        
        # Create combination signature
        combo_key = f"{final_stack.get('frontend', 'none')}+{final_stack.get('backend', 'none')}+{final_stack.get('database', 'none')}"
        
        # Update usage frequency
        if "usage_frequency" not in patterns:
            patterns["usage_frequency"] = {}
            
        patterns["usage_frequency"][combo_key] = patterns["usage_frequency"].get(combo_key, 0) + 1
        
        # Update project type associations
        if "project_type_associations" not in patterns:
            patterns["project_type_associations"] = {}
            
        project_type = requirements["project_type"]
        if project_type not in patterns["project_type_associations"]:
            patterns["project_type_associations"][project_type] = {}
            
        patterns["project_type_associations"][project_type][combo_key] = \
            patterns["project_type_associations"][project_type].get(combo_key, 0) + 1
            
        # Save updated patterns
        with open(self.patterns_file, 'w') as f:
            json.dump(patterns, f, indent=2)
            
    def _generate_reasoning(self, stack: Dict[str, Any], requirements: Dict[str, Any]) -> List[str]:
        """Generate human-readable reasoning for recommendations"""
        reasoning = []
        
        # Frontend reasoning
        if stack.get("frontend"):
            frontend = stack["frontend"]
            if "mobile" in requirements["target_devices"]:
                reasoning.append(f"Chose {frontend} for cross-platform mobile development")
            else:
                reasoning.append(f"Selected {frontend} based on your past preferences and project requirements")
                
        # Backend reasoning
        if stack.get("backend"):
            backend = stack["backend"]
            reasoning.append(f"Recommended {backend} for optimal performance and developer experience")
            
        # Database reasoning
        if stack.get("database"):
            db = stack["database"]
            if requirements.get("constraints", {}).get("realtime"):
                reasoning.append(f"Selected {db} for real-time capabilities")
            else:
                reasoning.append(f"Chose {db} for reliability and ecosystem support")
                
        # Open source reasoning
        if "open_source_replacements" in stack and stack["open_source_replacements"]:
            reasoning.append("Favored open source alternatives based on your preferences")
            
        return reasoning
        
    def _suggest_alternatives(self, stack: Dict[str, Any]) -> Dict[str, List[str]]:
        """Suggest alternative technologies for each category"""
        alternatives = {}
        
        alternative_map = {
            "react": ["vue", "svelte", "angular"],
            "nextjs": ["remix", "gatsby", "sveltekit"],
            "fastapi": ["django", "flask", "express"],
            "express": ["fastapi", "nestjs", "koa"],
            "postgresql": ["mysql", "sqlite", "supabase"],
            "mongodb": ["postgresql", "mysql", "firebase"],
            "vercel": ["netlify", "railway", "fly.io"],
            "tailwindcss": ["styled-components", "emotion", "chakra-ui"]
        }
        
        for category, tech in stack.items():
            if tech and isinstance(tech, str) and tech in alternative_map:
                alternatives[category] = alternative_map[tech]
                
        return alternatives
        
    def _check_compatibility_warnings(self, stack: Dict[str, Any]) -> List[str]:
        """Check for potential compatibility warnings"""
        warnings = []
        
        # Check for complex combinations
        if stack.get("frontend") == "react" and stack.get("backend") == "django":
            warnings.append("React + Django requires careful CORS configuration")
            
        # Check for version compatibility
        if stack.get("database") == "mongodb" and stack.get("backend") == "django":
            warnings.append("Django has limited native MongoDB support - consider PostgreSQL")
            
        # Check for hosting compatibility
        hosting = stack.get("hosting")
        backend = stack.get("backend")
        
        if hosting == "netlify" and backend in ["fastapi", "django"]:
            warnings.append("Netlify is optimized for static sites - consider Vercel or Railway for full-stack apps")
            
        return warnings
        
    def _estimate_complexity(self, stack: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate project complexity based on tech stack"""
        complexity_scores = {
            "frontend": {
                "react": 3, "nextjs": 4, "vue": 3, "svelte": 2, "angular": 5
            },
            "backend": {
                "fastapi": 3, "django": 4, "flask": 2, "express": 3, "nestjs": 4
            },
            "database": {
                "sqlite": 1, "postgresql": 3, "mysql": 3, "mongodb": 4
            }
        }
        
        total_score = 0
        component_count = 0
        
        for category in ["frontend", "backend", "database"]:
            tech = stack.get(category)
            if tech and category in complexity_scores and tech in complexity_scores[category]:
                total_score += complexity_scores[category][tech]
                component_count += 1
                
        avg_complexity = total_score / max(component_count, 1)
        
        if avg_complexity <= 2:
            complexity_level = "simple"
        elif avg_complexity <= 3.5:
            complexity_level = "medium"
        else:
            complexity_level = "complex"
            
        return {
            "level": complexity_level,
            "score": avg_complexity,
            "estimated_dev_time": {
                "simple": "2-4 weeks",
                "medium": "6-10 weeks", 
                "complex": "12+ weeks"
            }[complexity_level]
        }
        
    def interactive_tech_selection(self) -> Dict[str, Any]:
        """Interactive tech stack selection with user"""
        print("🛠️ Interactive Tech Stack Advisor")
        print("Let's build your perfect tech stack together!\n")
        
        # Gather basic requirements
        project_type = input("What type of project? (webapp/api/mobile/desktop) [webapp]: ").strip() or "webapp"
        project_description = input("Brief description of your project: ").strip()
        
        devices = ["web"]
        if input("Will this run on mobile? (y/N): ").lower().startswith('y'):
            devices.append("mobile")
        if input("Will this run on desktop? (y/N): ").lower().startswith('y'):
            devices.append("desktop")
            
        # Build requirements
        user_input = {
            "type": project_type,
            "description": project_description,
            "devices": devices
        }
        
        # Get recommendations
        recommendations = self.analyze_and_recommend(user_input)
        
        # Present recommendations
        print(f"\n🎯 Recommended Tech Stack:")
        print("=" * 30)
        
        stack = recommendations["recommended_stack"]
        for category, tech in stack.items():
            if tech and category not in ["tools", "compatibility_issues", "open_source_replacements"]:
                confidence = recommendations.get("confidence_scores", {}).get(category, "unknown")
                print(f"  {category.title()}: {tech} (confidence: {confidence:.1f})")
                
        # Show reasoning
        print(f"\n💡 Why these choices:")
        for reason in recommendations["reasoning"]:
            print(f"  • {reason}")
            
        # Show alternatives
        alternatives = recommendations["alternatives"]
        if alternatives:
            print(f"\n🔄 Alternatives to consider:")
            for category, alts in alternatives.items():
                print(f"  {category}: {', '.join(alts)}")
                
        # Show warnings
        warnings = recommendations["warnings"]
        if warnings:
            print(f"\n⚠️ Compatibility notes:")
            for warning in warnings:
                print(f"  • {warning}")
                
        # Confirm with user
        if input(f"\nProceed with this stack? (Y/n): ").lower() not in ['n', 'no']:
            return recommendations
        else:
            print("Tech stack selection cancelled.")
            return None
            
    def _validate_with_mcp(self, tech_stack: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tech stack using MCP integrations"""
        print("🔍 Running MCP validations...")
        
        try:
            # Get available integrations
            available_integrations = self.mcp_integration.get_available_integrations()
            active_integrations = [name for name, available in available_integrations.items() if available]
            
            if not active_integrations:
                return {
                    "status": "no_integrations",
                    "message": "No MCP integrations available",
                    "validated_by": [],
                    "security_issues": [],
                    "recommendations": []
                }
                
            print(f"  🔌 Active integrations: {', '.join(active_integrations)}")
            
            # Run MCP validation
            validation_results = self.mcp_integration.validate_tech_stack(tech_stack)
            
            # Display results
            if validation_results.get("security_issues"):
                print(f"  🛡️ Security insights: {len(validation_results['security_issues'])} found")
                
            if validation_results.get("recommendations"):
                print(f"  💡 MCP recommendations: {len(validation_results['recommendations'])} provided")
                
            validation_results["status"] = "success"
            validation_results["active_integrations"] = active_integrations
            
            return validation_results
            
        except Exception as e:
            print(f"  ⚠️ MCP validation failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "validated_by": [],
                "security_issues": [],
                "recommendations": []
            }
            
    def generate_xml_analysis_prompt(self, user_input: Dict[str, Any], project_context: Dict[str, Any]) -> str:
        """Generate XML-structured prompt for external LLM analysis"""
        return XMLPromptTemplates.tech_stack_analysis_prompt(project_context, user_input)
        
    def get_structured_recommendations(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Get recommendations with XML prompt ready for LLM integration"""
        
        # Parse requirements
        requirements = self._parse_requirements(user_input)
        
        # Analyze project context
        project_context = self._analyze_project_context()
        project_context['name'] = self.project_path.name
        
        # Generate XML prompt for potential LLM analysis
        xml_prompt = self.generate_xml_analysis_prompt(user_input, project_context)
        
        # Get our internal recommendations
        internal_analysis = self.analyze_and_recommend(user_input)
        
        return {
            "xml_prompt": xml_prompt,
            "internal_analysis": internal_analysis,
            "project_context": project_context,
            "ready_for_llm": True,
            "prompt_format": "xml_structured"
        }