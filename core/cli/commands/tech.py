"""DevAlex tech stack advisor command"""

import sys
from pathlib import Path
from .base import BaseCommand

class TechCommand(BaseCommand):
    """Tech stack advisor and validation"""
    
    def _get_tech_advisor(self):
        """Get tech advisor with dynamic import"""
        core_path = str(Path(__file__).parent.parent.parent)
        sys.path.insert(0, core_path)
        from agents.tech_advisor import TechStackAdvisor
        return TechStackAdvisor()
    
    @classmethod
    def register(cls, subparsers):
        """Register tech command"""
        parser = subparsers.add_parser('tech', help='Tech stack advisor and validation')
        tech_subparsers = parser.add_subparsers(dest='tech_action', help='Tech actions')
        
        # Interactive advisor
        tech_subparsers.add_parser('advisor', help='Interactive tech stack advisor')
        
        # Analyze current project
        tech_subparsers.add_parser('analyze', help='Analyze current project tech stack')
        
        # Validate compatibility
        validate_parser = tech_subparsers.add_parser('validate', help='Validate tech stack compatibility')
        validate_parser.add_argument('--frontend', help='Frontend framework')
        validate_parser.add_argument('--backend', help='Backend framework')
        validate_parser.add_argument('--database', help='Database system')
        validate_parser.add_argument('--hosting', help='Hosting platform')
        
        # Show preferences
        tech_subparsers.add_parser('preferences', help='Show learned preferences')
        
        # Reset learning
        tech_subparsers.add_parser('reset', help='Reset learned patterns and preferences')
        
        # MCP status
        tech_subparsers.add_parser('mcp', help='Show MCP integration status')
        
        # XML prompt generation
        tech_subparsers.add_parser('xml', help='Generate XML-structured prompt for LLM analysis')
        
        return parser
    
    def execute(self, args):
        """Execute tech command"""
        if args.tech_action == 'advisor':
            self._run_interactive_advisor()
        elif args.tech_action == 'analyze':
            self._analyze_project()
        elif args.tech_action == 'validate':
            self._validate_stack(args)
        elif args.tech_action == 'preferences':
            self._show_preferences()
        elif args.tech_action == 'reset':
            self._reset_learning()
        elif args.tech_action == 'mcp':
            self._show_mcp_status()
        elif args.tech_action == 'xml':
            self._generate_xml_prompt()
        else:
            print("🛠️ DevAlex Tech Stack Advisor")
            print("Usage: devalex tech {advisor|analyze|validate|preferences|reset|mcp|xml}")
            
    def _run_interactive_advisor(self):
        """Run interactive tech stack advisor"""
        advisor = self._get_tech_advisor()
        result = advisor.interactive_tech_selection()
        
        if result:
            print(f"\n✅ Tech stack analysis complete!")
            print(f"   Estimated complexity: {result['estimated_complexity']['level']}")
            print(f"   Development time: {result['estimated_complexity']['estimated_dev_time']}")
        
    def _analyze_project(self):
        """Analyze current project's tech stack"""
        advisor = self._get_tech_advisor()
        
        # Simulate project analysis
        user_input = {
            "type": "webapp",
            "description": f"Analyzing existing project in {Path.cwd().name}",
            "devices": ["web"]
        }
        
        result = advisor.analyze_and_recommend(user_input)
        
        print("🔍 Current Project Analysis")
        print("=" * 30)
        
        stack = result["recommended_stack"]
        print("Detected/Recommended Technologies:")
        for category, tech in stack.items():
            if tech and category not in ["tools", "compatibility_issues", "open_source_replacements"]:
                print(f"  • {category.title()}: {tech}")
                
        # Show tools
        if stack.get("tools"):
            print(f"\nRecommended Tools:")
            for tool in stack["tools"][:10]:  # Show first 10 tools
                print(f"  • {tool}")
                
        # Show warnings
        warnings = result.get("warnings", [])
        if warnings:
            print(f"\n⚠️ Potential Issues:")
            for warning in warnings:
                print(f"  • {warning}")
                
        # Show MCP validation results
        mcp_validation = result.get("mcp_validation", {})
        if mcp_validation.get("status") == "success":
            validated_by = mcp_validation.get("validated_by", [])
            if validated_by:
                print(f"\n🔍 MCP Validation (by {', '.join(validated_by)}):")
                
                security_issues = mcp_validation.get("security_issues", [])
                if security_issues:
                    print(f"  🛡️ Security Insights:")
                    for issue in security_issues[:3]:  # Show first 3
                        print(f"    • {issue}")
                        
                mcp_recommendations = mcp_validation.get("recommendations", [])
                if mcp_recommendations:
                    print(f"  💡 MCP Recommendations:")
                    for rec in mcp_recommendations[:3]:  # Show first 3
                        print(f"    • {rec}")
        elif mcp_validation.get("status") == "no_integrations":
            print(f"\n🔌 MCP Status: No integrations available")
            print(f"   Install context7, mcpref, or semgrep for enhanced validation")
                
    def _validate_stack(self, args):
        """Validate specified tech stack"""
        advisor = self._get_tech_advisor()
        
        # Build stack from arguments
        stack = {}
        if args.frontend:
            stack["frontend"] = args.frontend
        if args.backend:
            stack["backend"] = args.backend
        if args.database:
            stack["database"] = args.database
        if args.hosting:
            stack["hosting"] = args.hosting
            
        if not stack:
            print("❌ Please specify at least one technology to validate")
            print("   Example: devalex tech validate --frontend react --backend fastapi")
            return
            
        print("🔍 Validating Tech Stack Compatibility")
        print("=" * 40)
        
        for category, tech in stack.items():
            print(f"  {category.title()}: {tech}")
            
        # Validate compatibility
        validated = advisor._validate_compatibility(stack)
        issues = validated.get("compatibility_issues", [])
        
        if not issues:
            print(f"\n✅ No compatibility issues found!")
        else:
            print(f"\n⚠️ Potential Compatibility Issues:")
            for issue in issues:
                print(f"  • {issue}")
                
        # Suggest improvements
        complete_stack = advisor._fill_missing_pieces(validated, {"project_type": "webapp", "target_devices": ["web"]})
        
        print(f"\n💡 Suggested Additions:")
        for category, tech in complete_stack.items():
            if category not in stack and tech and category not in ["tools", "compatibility_issues"]:
                print(f"  • {category.title()}: {tech}")
                
    def _show_preferences(self):
        """Show learned user preferences"""
        advisor = self._get_tech_advisor()
        preferences = advisor._load_user_preferences()
        patterns = advisor._load_learned_patterns()
        
        print("🧠 Your Learned Tech Preferences")
        print("=" * 35)
        
        # Language preferences
        lang_prefs = preferences.get("language_preferences", {})
        if lang_prefs:
            print("\n📝 Language Preferences:")
            sorted_langs = sorted(lang_prefs.items(), key=lambda x: x[1], reverse=True)
            for lang, score in sorted_langs[:5]:
                print(f"  • {lang}: {score:.1f}/1.0")
                
        # Framework preferences
        framework_prefs = preferences.get("framework_preferences", {})
        if framework_prefs:
            print(f"\n🛠️ Framework Preferences:")
            for category, frameworks in framework_prefs.items():
                print(f"  {category.title()}:")
                sorted_frameworks = sorted(frameworks.items(), key=lambda x: x[1], reverse=True)
                for fw, score in sorted_frameworks[:3]:
                    print(f"    • {fw}: {score:.1f}/1.0")
                    
        # Usage patterns
        usage_freq = patterns.get("usage_frequency", {})
        if usage_freq:
            print(f"\n📊 Most Used Combinations:")
            sorted_combos = sorted(usage_freq.items(), key=lambda x: x[1], reverse=True)
            for combo, count in sorted_combos[:5]:
                print(f"  • {combo.replace('+', ' + ')}: {count} times")
                
        # Settings
        print(f"\n⚙️ Settings:")
        print(f"  • Open Source Bias: {preferences.get('open_source_bias', 0.9):.1f}/1.0")
        print(f"  • Complexity Preference: {preferences.get('complexity_preference', 'medium')}")
        print(f"  • Learning Rate: {preferences.get('learning_rate', 0.1):.1f}/1.0")
        
    def _reset_learning(self):
        """Reset learned patterns and preferences"""
        advisor = self._get_tech_advisor()
        
        confirm = input("⚠️ This will reset all learned preferences and patterns. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Reset cancelled.")
            return
            
        # Reset files by deleting them (they'll be recreated with defaults)
        if advisor.preferences_file.exists():
            advisor.preferences_file.unlink()
            
        if advisor.patterns_file.exists():
            advisor.patterns_file.unlink()
            
        if advisor.compatibility_db.exists():
            advisor.compatibility_db.unlink()
            
        print("✅ Tech advisor learning reset. Fresh start!")
        print("   Preferences will be rebuilt based on your future interactions.")
        
    def _show_mcp_status(self):
        """Show MCP integration status"""
        advisor = self._get_tech_advisor()
        
        print("🔌 MCP Integration Status")
        print("=" * 30)
        
        try:
            # Get integration status
            available_integrations = advisor.mcp_integration.get_available_integrations()
            
            if not available_integrations:
                print("❌ No MCP integrations configured")
                return
                
            print("Available Integrations:")
            for integration, available in available_integrations.items():
                status_icon = "✅" if available else "❌"
                print(f"  {status_icon} {integration.title()}: {'Available' if available else 'Not available'}")
                
            active_count = sum(1 for available in available_integrations.values() if available)
            total_count = len(available_integrations)
            
            print(f"\nSummary: {active_count}/{total_count} integrations active")
            
            if active_count == 0:
                print("\n💡 Getting Started with MCP:")
                print("   • Install Semgrep: pip install semgrep")
                print("   • Set up Context7 MCP server")
                print("   • Configure MCPRef integration")
                print("   • Restart DevAlex to detect changes")
            else:
                print(f"\n🎉 {active_count} MCP integration(s) ready for tech validation!")
                
        except Exception as e:
            print(f"❌ Error checking MCP status: {e}")
            print("   MCP integrations may not be properly configured")
            
    def _generate_xml_prompt(self):
        """Generate XML-structured prompt for LLM analysis"""
        advisor = self._get_tech_advisor()
        
        print("📋 XML Prompt Generator")
        print("=" * 30)
        
        # Get user input for prompt generation
        project_type = input("Project type (webapp/api/mobile/desktop) [webapp]: ").strip() or "webapp"
        description = input("Brief project description: ").strip() or "A new project"
        
        user_input = {
            "type": project_type,
            "description": description,
            "devices": ["web"] if project_type == "webapp" else ["web", "mobile"]
        }
        
        try:
            # Generate structured recommendations with XML prompt
            result = advisor.get_structured_recommendations(user_input)
            
            print(f"\n📋 Generated XML-Structured Prompt:")
            print("=" * 50)
            print(result["xml_prompt"])
            
            print(f"\n💾 Prompt saved to clipboard (if available)")
            
            # Save to file option
            save_file = input(f"\nSave XML prompt to file? (y/N): ").lower().strip()
            if save_file == 'y':
                from pathlib import Path
                filename = f"tech_analysis_prompt_{project_type}.xml"
                Path(filename).write_text(result["xml_prompt"])
                print(f"✅ XML prompt saved to: {filename}")
                print("   Use this with Claude or other LLMs for enhanced tech analysis!")
                
        except Exception as e:
            print(f"❌ Error generating XML prompt: {e}")