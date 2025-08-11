"""DevAlex components command"""

import sys
from pathlib import Path
from .base import BaseCommand

class ComponentsCommand(BaseCommand):
    """Component library management"""
    
    def _get_registry(self):
        """Get component registry with dynamic import"""
        tools_path = str(Path(__file__).parent.parent.parent.parent / "tools" / "component-library")
        sys.path.insert(0, tools_path)
        from registry import ComponentRegistry
        return ComponentRegistry()
    
    @classmethod
    def register(cls, subparsers):
        """Register components command"""
        parser = subparsers.add_parser('components', help='Component library management')
        comp_subparsers = parser.add_subparsers(dest='comp_action', help='Component actions')
        
        # List components
        comp_subparsers.add_parser('list', help='List available components')
        
        # Search components
        search_parser = comp_subparsers.add_parser('search', help='Search components')
        search_parser.add_argument('query', help='Search query')
        
        # Generate component
        generate_parser = comp_subparsers.add_parser('generate', help='Generate component')
        generate_parser.add_argument('component_id', help='Component ID to generate')
        generate_parser.add_argument('--language', default='python', help='Target language')
        
        # Initialize registry
        comp_subparsers.add_parser('init', help='Initialize component registry')
        
        # Show categories
        comp_subparsers.add_parser('categories', help='List component categories')
        
        return parser
    
    def execute(self, args):
        """Execute components command"""
        if args.comp_action == 'list':
            self._list_components()
        elif args.comp_action == 'search':
            self._search_components(args.query)
        elif args.comp_action == 'generate':
            self._generate_component(args.component_id, args.language)
        elif args.comp_action == 'init':
            self._init_registry()
        elif args.comp_action == 'categories':
            self._show_categories()
        else:
            print("🧩 DevAlex Component Library")
            print("Usage: devalex components {list|search|generate|init|categories}")
            
    def _list_components(self):
        """List available components"""
        registry = self._get_registry()
        components = registry.list_components()
        
        if not components:
            print("🧩 No components found. Run: devalex components init")
            return
            
        print("🧩 Available DevAlex Components:")
        print("=" * 40)
        
        by_category = {}
        for component in components:
            category = component.get("category", "other")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(component)
            
        for category, comps in sorted(by_category.items()):
            print(f"\n📂 {category.title()}")
            for comp in comps:
                points = comp.get("story_points", "?")
                languages = ", ".join(comp.get("languages", []))
                print(f"   • {comp['id']} - {comp['name']} ({points} pts)")
                print(f"     Languages: {languages}")
                print(f"     {comp['description']}")
        
    def _search_components(self, query):
        """Search components"""
        registry = self._get_registry()
        results = registry.search_components(query)
        
        if not results:
            print(f"🔍 No components found matching: {query}")
            return
            
        print(f"🔍 Search Results for: {query}")
        print("=" * 30)
        
        for component in results:
            points = component.get("story_points", "?")
            print(f"   • {component['id']} - {component['name']} ({points} pts)")
            print(f"     {component['description']}")
        
    def _generate_component(self, component_id, language):
        """Generate component"""
        registry = self._get_registry()
        
        try:
            code = registry.generate_component(component_id, language)
            print(f"🏗️ Generated {component_id} component in {language}:")
            print("=" * 50)
            print(code)
            
            # Optionally save to file
            component = registry.get_component(component_id)
            if component:
                ext = {"python": "py", "typescript": "ts", "javascript": "js"}.get(language, "py")
                filename = f"{component_id}.{ext}"
                
                save = input(f"\nSave to {filename}? (y/N): ").lower().strip()
                if save == 'y':
                    Path(filename).write_text(code)
                    print(f"✅ Saved to {filename}")
                    
        except ValueError as e:
            print(f"❌ {e}")
            
    def _init_registry(self):
        """Initialize component registry"""
        registry = self._get_registry()
        registry.initialize_registry()
        print("✅ Component registry initialized with default components")
        
    def _show_categories(self):
        """Show component categories"""
        registry = self._get_registry()
        categories = registry.get_categories()
        
        if not categories:
            print("📂 No categories found. Run: devalex components init")
            return
            
        print("📂 Component Categories:")
        for category in categories:
            print(f"   • {category}")
            
        print(f"\nTotal categories: {len(categories)}")