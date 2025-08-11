"""DevAlex scaffold command - Advanced project generation"""

import sys
import json
from pathlib import Path
from .base import BaseCommand

class ScaffoldCommand(BaseCommand):
    """Advanced project scaffolding and generation"""
    
    def _get_scaffolding_generator(self):
        """Get scaffolding generator with dynamic import"""
        tools_path = str(Path(__file__).parent.parent.parent.parent / "tools" / "scaffolding")
        sys.path.insert(0, tools_path)
        from advanced_generator import AdvancedProjectGenerator
        return AdvancedProjectGenerator()
    
    @classmethod
    def register(cls, subparsers):
        """Register scaffold command"""
        parser = subparsers.add_parser('scaffold', help='Advanced project scaffolding')
        scaffold_subparsers = parser.add_subparsers(dest='scaffold_action', help='Scaffold actions')
        
        # List available templates
        scaffold_subparsers.add_parser('list', help='List available project templates')
        
        # Generate project from template
        generate_parser = scaffold_subparsers.add_parser('generate', help='Generate project from template')
        generate_parser.add_argument('template', help='Template name')
        generate_parser.add_argument('name', help='Project name')
        generate_parser.add_argument('--frontend', help='Frontend framework (react, vue, svelte)')
        generate_parser.add_argument('--backend', help='Backend framework (fastapi, django, express)')
        generate_parser.add_argument('--database', help='Database (postgresql, mysql, mongodb)')
        generate_parser.add_argument('--auth', help='Authentication system (jwt, oauth, supabase)')
        generate_parser.add_argument('--skip-install', action='store_true', help='Skip dependency installation')
        
        # Interactive project creator
        scaffold_subparsers.add_parser('create', help='Interactive project creation wizard')
        
        # Show template details
        show_parser = scaffold_subparsers.add_parser('show', help='Show template details')
        show_parser.add_argument('template', help='Template name to show details for')
        
        return parser
    
    def execute(self, args):
        """Execute scaffold command"""
        if args.scaffold_action == 'list':
            self._list_templates()
        elif args.scaffold_action == 'generate':
            self._generate_project(args)
        elif args.scaffold_action == 'create':
            self._interactive_create()
        elif args.scaffold_action == 'show':
            self._show_template(args.template)
        else:
            print("🏗️ DevAlex Advanced Scaffolding")
            print("Usage: devalex scaffold {list|generate|create|show}")
            
    def _list_templates(self):
        """List available project templates"""
        generator = self._get_scaffolding_generator()
        templates = generator.get_available_templates()
        
        print("🏗️ Available Project Templates")
        print("=" * 50)
        
        ready_templates = []
        coming_soon = []
        
        for template_id, info in templates.items():
            if info.get('ready', False):
                ready_templates.append((template_id, info))
            else:
                coming_soon.append((template_id, info))
                
        # Show ready templates
        if ready_templates:
            print("\n✅ Ready to Use:")
            for template_id, info in ready_templates:
                features = ", ".join(info['features'][:4])
                print(f"   📦 {template_id}")
                print(f"      {info['name']}")
                print(f"      {info['description']}")
                print(f"      Features: {features}")
                print()
                
        # Show coming soon templates
        if coming_soon:
            print("🚧 Coming Soon:")
            for template_id, info in coming_soon:
                print(f"   🔨 {template_id} - {info['name']}")
                
        print(f"\n💡 Usage: devalex scaffold generate <template> <project-name>")
        print(f"   Example: devalex scaffold generate fullstack-webapp my-awesome-app")
        
    def _generate_project(self, args):
        """Generate project from template"""
        generator = self._get_scaffolding_generator()
        
        # Build configuration from arguments
        config = {
            'frontend': args.frontend,
            'backend': args.backend,
            'database': args.database,
            'auth': args.auth,
            'skip_install': args.skip_install
        }
        
        # Remove None values
        config = {k: v for k, v in config.items() if v is not None}
        
        try:
            print(f"🚀 Generating {args.template} project: {args.name}")
            print("This may take a few minutes...")
            
            result = generator.generate_project(args.name, args.template, config)
            
            print(f"\n✅ Project '{args.name}' generated successfully!")
            print(f"📁 Type: {result['type']}")
            
            if 'features' in result:
                print(f"🎯 Features: {', '.join(result['features'])}")
                
            if 'structure' in result:
                print(f"🏗️ Structure: {result['structure']}")
                
            if 'next_steps' in result:
                print(f"\n🚀 Next Steps:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
                    
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("Please check that all dependencies are available")
            
    def _interactive_create(self):
        """Interactive project creation wizard"""
        print("🧙‍♂️ DevAlex Interactive Project Creator")
        print("=" * 50)
        
        # Get project details
        project_name = input("Project name: ").strip()
        if not project_name:
            print("❌ Project name is required")
            return
            
        # Show template options
        generator = self._get_scaffolding_generator()
        templates = generator.get_available_templates()
        ready_templates = [(k, v) for k, v in templates.items() if v.get('ready', False)]
        
        print(f"\nAvailable templates:")
        for i, (template_id, info) in enumerate(ready_templates, 1):
            print(f"  {i}. {info['name']} - {info['description']}")
            
        try:
            choice = int(input(f"\nSelect template (1-{len(ready_templates)}): "))
            if 1 <= choice <= len(ready_templates):
                template_id = ready_templates[choice - 1][0]
            else:
                print("❌ Invalid choice")
                return
        except ValueError:
            print("❌ Invalid input")
            return
            
        # Get configuration options
        config = {}
        
        if template_id == 'fullstack-webapp':
            print(f"\nConfiguration options for Full-Stack Web App:")
            
            frontend = input("Frontend framework (react/vue/svelte) [react]: ").strip() or "react"
            config['frontend'] = frontend
            
            backend = input("Backend framework (fastapi/django/express) [fastapi]: ").strip() or "fastapi"
            config['backend'] = backend
            
            database = input("Database (postgresql/mysql/mongodb) [postgresql]: ").strip() or "postgresql"
            config['database'] = database
            
            auth = input("Authentication (jwt/oauth/supabase) [jwt]: ").strip() or "jwt"
            config['auth'] = auth
            
        elif template_id == 'api-service':
            print(f"\nConfiguration options for API Service:")
            
            framework = input("Framework (fastapi/django/express) [fastapi]: ").strip() or "fastapi"
            config['framework'] = framework
            
            database = input("Database (postgresql/mysql/mongodb) [postgresql]: ").strip() or "postgresql"
            config['database'] = database
            
        # Generate project
        try:
            print(f"\n🚀 Creating {template_id} project: {project_name}")
            print("This may take a few minutes...")
            
            result = generator.generate_project(project_name, template_id, config)
            
            print(f"\n🎉 Project '{project_name}' created successfully!")
            print(f"📁 Type: {result['type']}")
            
            if 'next_steps' in result:
                print(f"\n🚀 Next Steps:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
                    
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            
    def _show_template(self, template_name):
        """Show detailed information about a template"""
        generator = self._get_scaffolding_generator()
        templates = generator.get_available_templates()
        
        if template_name not in templates:
            print(f"❌ Template '{template_name}' not found")
            self._list_templates()
            return
            
        template_info = templates[template_name]
        
        print(f"📦 Template: {template_name}")
        print("=" * 50)
        print(f"Name: {template_info['name']}")
        print(f"Description: {template_info['description']}")
        print(f"Status: {'✅ Ready' if template_info.get('ready') else '🚧 Coming Soon'}")
        
        if template_info.get('features'):
            print(f"\nFeatures:")
            for feature in template_info['features']:
                print(f"  • {feature.replace('_', ' ').title()}")
                
        if template_info.get('ready'):
            print(f"\n💡 Usage:")
            print(f"   devalex scaffold generate {template_name} my-project-name")
            
            if template_name == 'fullstack-webapp':
                print(f"\n🔧 Options:")
                print(f"   --frontend react|vue|svelte")
                print(f"   --backend fastapi|django|express")
                print(f"   --database postgresql|mysql|mongodb")
                print(f"   --auth jwt|oauth|supabase")
        else:
            print(f"\n🚧 This template is under development")
            print(f"   Check back in future DevAlex updates!")