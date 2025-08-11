"""DevAlex agents command"""

import sys
from pathlib import Path
from .base import BaseCommand

class AgentsCommand(BaseCommand):
    """Agent orchestration management"""
    
    @classmethod
    def register(cls, subparsers):
        """Register agents command"""
        parser = subparsers.add_parser('agents', help='Agent orchestration management')
        agents_subparsers = parser.add_subparsers(dest='agents_action', help='Agent actions')
        
        # Status
        agents_subparsers.add_parser('status', help='Show agent system status')
        
        # List agents
        agents_subparsers.add_parser('list', help='List available agents')
        
        # Initialize agents
        agents_subparsers.add_parser('init', help='Initialize agent system')
        
        # Run workflow
        workflow_parser = agents_subparsers.add_parser('run', help='Run agent workflow')
        workflow_parser.add_argument('workflow', help='Workflow name')
        
        return parser
    
    def execute(self, args):
        """Execute agents command"""
        if args.agents_action == 'status':
            self._show_status()
        elif args.agents_action == 'list':
            self._list_agents()
        elif args.agents_action == 'init':
            self._init_agents()
        elif args.agents_action == 'run':
            self._run_workflow(args.workflow)
        else:
            print("🤖 DevAlex Agent Orchestration")
            print("Usage: devalex agents {status|list|init|run}")
            
    def _show_status(self):
        """Show agent system status"""
        # Import agent system when needed
        core_path = str(Path(__file__).parent.parent.parent)
        sys.path.insert(0, core_path)
        from agents.system import DevAlexAgentSystem
        
        agent_system = DevAlexAgentSystem()
        status = agent_system.get_agent_status()
        
        print("🤖 Agent System Status:")
        print(f"   Status: {status['status'].title()}")
        print(f"   Agents: {len(status['agents'])} configured")
        print(f"   Workflows: {len(status['workflows'])} available")
        
        if status['agents']:
            print("\n🤖 Configured Agents:")
            for agent in status['agents']:
                print(f"   • {agent['name'].title()} Agent - {agent['status']}")
        
    def _list_agents(self):
        """List available agents"""
        # Import agent system when needed
        core_path = str(Path(__file__).parent.parent.parent)
        sys.path.insert(0, core_path)
        from agents.system import DevAlexAgentSystem
        
        agent_descriptions = {
            "architecture": "System design and patterns",
            "development": "Full-stack implementation", 
            "testing": "Comprehensive QA and testing",
            "security": "Security review and validation",
            "operations": "Deployment and infrastructure",
            "orchestrator": "Multi-agent coordination"
        }
        
        agent_system = DevAlexAgentSystem()
        status = agent_system.get_agent_status()
        
        print("🤖 Available DevAlex Agents:")
        
        if status['status'] == 'not_initialized':
            print("   ⚠️  Agent system not initialized")
            print("   Run: devalex agents init")
            return
            
        for agent in status['agents']:
            name = agent['name']
            description = agent_descriptions.get(name, "Specialized agent")
            print(f"   • {name.title()} Agent - {description}")
            
    def _run_workflow(self, workflow):
        """Run agent workflow"""
        # Import agent system when needed
        core_path = str(Path(__file__).parent.parent.parent)
        sys.path.insert(0, core_path)
        from agents.system import DevAlexAgentSystem
        
        agent_system = DevAlexAgentSystem()
        result = agent_system.run_workflow(workflow)
        
        if 'error' in result:
            print(f"❌ {result['error']}")
            return
            
        print(f"🚀 Running workflow: {workflow}")
        print(f"   Status: {result['status']}")
        print(f"   Message: {result['message']}")
        
    def _init_agents(self):
        """Initialize agent system"""
        print("🤖 Initializing DevAlex Agent System...")
        
        # Import agent system when needed
        core_path = str(Path(__file__).parent.parent.parent)
        sys.path.insert(0, core_path)
        from agents.system import DevAlexAgentSystem
        
        agent_system = DevAlexAgentSystem()
        agent_system.initialize_agent_system()
        print("✅ Agent system initialized!")