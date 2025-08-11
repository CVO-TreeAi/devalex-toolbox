"""DevAlex planr command"""

import sys
from pathlib import Path
from .base import BaseCommand

# Add tools to Python path
tools_path = str(Path(__file__).parent.parent.parent.parent / "tools" / "planr")
sys.path.insert(0, tools_path)
from auto_generator import AutoRoadmapGenerator

class PlanrCommand(BaseCommand):
    """AI-powered development roadmap generator"""
    
    @classmethod
    def register(cls, subparsers):
        """Register planr command"""
        parser = subparsers.add_parser('planr', help='AI-powered development roadmap generator')
        planr_subparsers = parser.add_subparsers(dest='planr_action', help='Planr actions')
        
        # Generate roadmap
        generate_parser = planr_subparsers.add_parser('generate', help='Generate development roadmap')
        generate_parser.add_argument('--prd', help='Path to PRD file')
        generate_parser.add_argument('--tech-stack', help='Path to tech stack file')
        
        # List templates
        planr_subparsers.add_parser('templates', help='List available roadmap templates')
        
        return parser
    
    def execute(self, args):
        """Execute planr command"""
        if args.planr_action == 'generate':
            self._generate_roadmap(args)
        elif args.planr_action == 'templates':
            self._list_templates()
        else:
            print("📋 DevAlex Planr - AI Development Roadmap Generator")
            print("Usage: devalex planr {generate|templates}")
            
    def _generate_roadmap(self, args):
        """Generate development roadmap"""
        generator = AutoRoadmapGenerator()
        result = generator.detect_and_generate_roadmap()
        
        print(f"\n📊 Roadmap Generation Results:")
        print(f"   Project: {result['project_name']}")
        print(f"   Type: {result['project_type']}")
        print(f"   Complexity: {result['complexity']}")
        print(f"   Story Points: {result['total_story_points']}")
        print(f"   Timeline: {result['estimated_timeline']}")
        
        print(f"\n📁 Files Generated:")
        for file_path in result['files_generated']:
            print(f"   • {file_path}")
            
        print(f"\n🚀 Next Steps:")
        print("   1. Review generated PRD and tech stack")
        print("   2. Open project in Claude Code")
        print("   3. Say 'DevAlex' to activate agent coordination")
        print("   4. Start implementing the roadmap!")
        
    def _list_templates(self):
        """List available roadmap templates"""
        print("📋 DevAlex Planr Templates:")
        
        templates = [
            "Auto-generation template - Analyzes project structure and generates appropriate roadmap",
            "Web application template - Full-stack web development roadmap",
            "API service template - Backend API development roadmap", 
            "Mobile app template - Native mobile development roadmap",
            "AI/ML project template - Data science and ML workflow roadmap"
        ]
        
        for template in templates:
            print(f"   • {template}")
            
        print(f"\n💡 Usage:")
        print("   devalex planr generate  # Auto-detects and generates roadmap")
        print("   devalex init <project>  # Includes automatic roadmap generation")