"""DevAlex code command - AI-powered code generation"""

import sys
from pathlib import Path
from .base import BaseCommand

class CodeCommand(BaseCommand):
    """AI-powered code generation and assistance"""
    
    def _get_code_generator(self):
        """Get code generator with dynamic import"""
        tools_path = str(Path(__file__).parent.parent.parent.parent / "tools" / "code-generation")
        sys.path.insert(0, tools_path)
        from ai_generator import AICodeGenerator
        return AICodeGenerator()
    
    @classmethod
    def register(cls, subparsers):
        """Register code command"""
        parser = subparsers.add_parser('code', help='AI-powered code generation')
        code_subparsers = parser.add_subparsers(dest='code_action', help='Code actions')
        
        # Generate code from description
        generate_parser = code_subparsers.add_parser('generate', help='Generate code from description')
        generate_parser.add_argument('type', choices=['function', 'class', 'component', 'test', 'api', 'schema'], 
                                   help='Type of code to generate')
        generate_parser.add_argument('description', help='Description of what to generate')
        generate_parser.add_argument('--language', default='python', help='Programming language')
        generate_parser.add_argument('--framework', help='Framework (react, fastapi, etc.)')
        generate_parser.add_argument('--save', action='store_true', help='Save generated code to files')
        generate_parser.add_argument('--test', action='store_true', help='Also generate tests')
        
        # List available generators
        code_subparsers.add_parser('list', help='List available code generators')
        
        # Interactive code generation
        code_subparsers.add_parser('assistant', help='Interactive code generation assistant')
        
        # Quick templates
        template_parser = code_subparsers.add_parser('template', help='Generate from predefined templates')
        template_parser.add_argument('template_name', help='Template name')
        template_parser.add_argument('--name', help='Name for the generated code')
        
        return parser
    
    def execute(self, args):
        """Execute code command"""
        if args.code_action == 'generate':
            self._generate_code(args)
        elif args.code_action == 'list':
            self._list_generators()
        elif args.code_action == 'assistant':
            self._interactive_assistant()
        elif args.code_action == 'template':
            self._generate_from_template(args)
        else:
            print("🤖 DevAlex AI Code Generation")
            print("Usage: devalex code {generate|list|assistant|template}")
            
    def _generate_code(self, args):
        """Generate code from description"""
        generator = self._get_code_generator()
        
        # Build context
        context = {
            'language': args.language,
            'framework': args.framework,
            'generate_test': args.test
        }
        
        try:
            print(f"🤖 Generating {args.type} code...")
            print(f"Description: {args.description}")
            print(f"Language: {args.language}")
            if args.framework:
                print(f"Framework: {args.framework}")
            print()
            
            result = generator.generate_code(args.type, args.description, context)
            
            print("✅ Code generated successfully!")
            print("=" * 60)
            print(result['code'])
            
            if result.get('test') and args.test:
                print("\n" + "=" * 30 + " TESTS " + "=" * 30)
                print(result['test'])
                
            if args.save:
                self._save_generated_code(result, args)
                
            # Show additional info
            if result.get('imports'):
                print(f"\n📦 Required imports:")
                for imp in result['imports']:
                    print(f"   {imp}")
                    
            print(f"\n💡 Generated {result['type']} ready for use!")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
    def _list_generators(self):
        """List available code generators"""
        generator = self._get_code_generator()
        generators = generator.get_available_generators()
        
        print("🤖 Available AI Code Generators")
        print("=" * 50)
        
        ready_generators = []
        coming_soon = []
        
        for gen_id, info in generators.items():
            if info.get('ready', False):
                ready_generators.append((gen_id, info))
            else:
                coming_soon.append((gen_id, info))
                
        # Show ready generators
        if ready_generators:
            print("\n✅ Ready to Use:")
            for gen_id, info in ready_generators:
                print(f"   🤖 {gen_id}")
                print(f"      {info['name']}")
                print(f"      {info['description']}")
                
                if info.get('languages'):
                    print(f"      Languages: {', '.join(info['languages'])}")
                if info.get('frameworks'):
                    print(f"      Frameworks: {', '.join(info['frameworks'])}")
                print()
                
        # Show coming soon
        if coming_soon:
            print("🚧 Coming Soon:")
            for gen_id, info in coming_soon:
                print(f"   🔨 {gen_id} - {info['name']}")
                
        print(f"\n💡 Usage: devalex code generate <type> \"<description>\"")
        print(f"   Example: devalex code generate function \"calculate fibonacci number\"")
        
    def _interactive_assistant(self):
        """Interactive code generation assistant"""
        print("🧙‍♂️ DevAlex AI Code Assistant")
        print("=" * 50)
        print("I'll help you generate code from natural language descriptions!")
        print()
        
        generator = self._get_code_generator()
        
        while True:
            print("What would you like to generate?")
            print("1. Function")
            print("2. Class")  
            print("3. React Component")
            print("4. API Endpoint")
            print("5. Exit")
            
            try:
                choice = input("\nSelect option (1-5): ").strip()
                
                if choice == '5':
                    print("👋 Goodbye! Happy coding!")
                    break
                    
                if choice not in ['1', '2', '3', '4']:
                    print("❌ Invalid choice, please try again.")
                    continue
                    
                # Map choices to types
                type_map = {
                    '1': 'function',
                    '2': 'class', 
                    '3': 'component',
                    '4': 'api'
                }
                
                code_type = type_map[choice]
                
                # Get description
                description = input(f"\nDescribe the {code_type} you want to create: ").strip()
                if not description:
                    print("❌ Description is required.")
                    continue
                    
                # Get language/framework
                context = {}
                
                if code_type in ['function', 'class']:
                    language = input("Language (python/typescript/javascript) [python]: ").strip() or "python"
                    context['language'] = language
                elif code_type == 'component':
                    framework = input("Framework (react/vue) [react]: ").strip() or "react"
                    context['framework'] = framework
                    context['language'] = 'typescript'
                elif code_type == 'api':
                    framework = input("Framework (fastapi/express) [fastapi]: ").strip() or "fastapi"
                    context['framework'] = framework
                    
                # Generate code
                try:
                    result = generator.generate_code(code_type, description, context)
                    
                    print(f"\n✅ Generated {code_type}:")
                    print("=" * 60)
                    print(result['code'])
                    
                    # Ask to save
                    save = input(f"\nSave to {result['filename']}? (y/N): ").lower().strip()
                    if save == 'y':
                        self._save_code_to_file(result)
                        
                except Exception as e:
                    print(f"❌ Error generating code: {e}")
                    
                print("\n" + "-" * 60)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Happy coding!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    def _generate_from_template(self, args):
        """Generate code from predefined templates"""
        templates = {
            "crud-api": {
                "description": "Complete CRUD API with database models",
                "type": "api",
                "language": "python"
            },
            "auth-system": {
                "description": "User authentication system with JWT",
                "type": "function",
                "language": "python"
            },
            "dashboard-component": {
                "description": "Dashboard component with charts and metrics",
                "type": "component",
                "framework": "react"
            },
            "data-processor": {
                "description": "Data processing pipeline with validation",
                "type": "class",
                "language": "python"
            }
        }
        
        if args.template_name not in templates:
            print(f"❌ Template '{args.template_name}' not found")
            print(f"Available templates: {', '.join(templates.keys())}")
            return
            
        template = templates[args.template_name]
        generator = self._get_code_generator()
        
        # Build context
        context = {
            'language': template.get('language', 'python'),
            'framework': template.get('framework')
        }
        
        # Use custom name if provided
        description = template['description']
        if args.name:
            description = f"{template['description']} named {args.name}"
            
        try:
            result = generator.generate_code(template['type'], description, context)
            
            print(f"✅ Generated {args.template_name} template:")
            print("=" * 60)
            print(result['code'])
            
            # Auto-save templates
            self._save_code_to_file(result)
            
        except Exception as e:
            print(f"❌ Error generating template: {e}")
            
    def _save_generated_code(self, result, args):
        """Save generated code to files"""
        try:
            # Save main code
            filename = result.get('filename', f"generated_{args.type}.py")
            Path(filename).write_text(result['code'])
            print(f"💾 Code saved to: {filename}")
            
            # Save test if available
            if result.get('test') and args.test:
                test_filename = result.get('test_filename', f"test_{filename}")
                Path(test_filename).write_text(result['test'])
                print(f"🧪 Test saved to: {test_filename}")
                
        except Exception as e:
            print(f"❌ Error saving files: {e}")
            
    def _save_code_to_file(self, result):
        """Save code result to file"""
        try:
            filename = result.get('filename', 'generated_code.py')
            Path(filename).write_text(result['code'])
            print(f"💾 Saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")