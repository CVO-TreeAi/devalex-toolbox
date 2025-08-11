#!/usr/bin/env python3

"""
DevAlex Core CLI
Main command-line interface for DevAlex agentic toolbox
"""

import argparse
import sys
from pathlib import Path

from .commands.init import InitCommand
from .commands.status import StatusCommand
from .commands.update import UpdateCommand
from .commands.install import InstallCommand
from .commands.doctor import DoctorCommand
from .commands.planr import PlanrCommand
from .commands.agents import AgentsCommand
from .commands.security import SecurityCommand
from .commands.components import ComponentsCommand
from .commands.tech import TechCommand
from .commands.scaffold import ScaffoldCommand
from .commands.code import CodeCommand
from .commands.test import TestCommand
from .commands.deploy import DeployCommand
from .utils.banner import print_banner
from .utils.config import DevAlexConfig

def create_parser():
    """Create the main argument parser"""
    parser = argparse.ArgumentParser(
        description="DevAlex - Your Personal Claude Code Supercharger",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  devalex init my-project --type webapp    # Create new project
  devalex scaffold generate fullstack-webapp myapp  # Generate full project
  devalex code generate function "calculate fibonacci"  # AI code generation
  devalex test setup python               # Setup testing framework
  devalex deploy docker fastapi           # Setup Docker containerization
  devalex status                           # Check system status
  devalex tech advisor                     # Interactive tech stack advisor
  devalex planr generate                   # Generate development roadmap

The Three Amigos: You + DevAlex + Claude Code = Unstoppable! 🚀
        """
    )
    
    # Add version
    parser.add_argument('--version', action='version', 
                       version=f'DevAlex {DevAlexConfig.VERSION}')
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Register all commands
    InitCommand.register(subparsers)
    StatusCommand.register(subparsers)
    UpdateCommand.register(subparsers)
    InstallCommand.register(subparsers)
    DoctorCommand.register(subparsers)
    PlanrCommand.register(subparsers)
    AgentsCommand.register(subparsers)
    SecurityCommand.register(subparsers)
    ComponentsCommand.register(subparsers)
    TechCommand.register(subparsers)
    ScaffoldCommand.register(subparsers)
    CodeCommand.register(subparsers)
    TestCommand.register(subparsers)
    DeployCommand.register(subparsers)
    
    return parser

def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show banner for main commands (not subcommands)
    if args.command in ['status', 'install', 'doctor']:
        print_banner()
    
    # Handle no command provided
    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'init':
            InitCommand().execute(args)
        elif args.command == 'status':
            StatusCommand().execute(args)
        elif args.command == 'update':
            UpdateCommand().execute(args)
        elif args.command == 'install':
            InstallCommand().execute(args)
        elif args.command == 'doctor':
            DoctorCommand().execute(args)
        elif args.command == 'planr':
            PlanrCommand().execute(args)
        elif args.command == 'agents':
            AgentsCommand().execute(args)
        elif args.command == 'security':
            SecurityCommand().execute(args)
        elif args.command == 'components':
            ComponentsCommand().execute(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 DevAlex interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ DevAlex error: {e}")
        print("🩺 Try running: devalex doctor")
        sys.exit(1)

if __name__ == "__main__":
    main()