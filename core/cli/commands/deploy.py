"""DevAlex deploy command - Deployment and DevOps automation"""

import sys
from pathlib import Path
from .base import BaseCommand

class DeployCommand(BaseCommand):
    """Deployment and DevOps automation tools"""
    
    def _get_devops_automation(self):
        """Get DevOps automation with dynamic import"""
        tools_path = str(Path(__file__).parent.parent.parent.parent / "tools" / "deployment")
        sys.path.insert(0, tools_path)
        from devops_automation import DevOpsAutomation
        return DevOpsAutomation()
    
    @classmethod
    def register(cls, subparsers):
        """Register deploy command"""
        parser = subparsers.add_parser('deploy', help='Deployment and DevOps automation')
        deploy_subparsers = parser.add_subparsers(dest='deploy_action', help='Deploy actions')
        
        # Setup containerization
        docker_parser = deploy_subparsers.add_parser('docker', help='Setup Docker containerization')
        docker_parser.add_argument('app_type', choices=['webapp', 'api', 'fullstack', 'fastapi', 'django', 'react', 'nextjs'])
        docker_parser.add_argument('--language', default='python', help='Programming language')
        docker_parser.add_argument('--database', help='Database type (postgresql, mysql, mongodb)')
        docker_parser.add_argument('--no-compose', action='store_true', help='Skip docker-compose setup')
        
        # Setup deployment platform
        platform_parser = deploy_subparsers.add_parser('platform', help='Setup deployment platform')
        platform_parser.add_argument('platform', choices=['vercel', 'railway', 'render', 'aws', 'gcp', 'netlify'])
        platform_parser.add_argument('--app-type', help='Application type')
        
        # Setup CI/CD pipeline
        cicd_parser = deploy_subparsers.add_parser('cicd', help='Setup CI/CD pipeline')
        cicd_parser.add_argument('platform', choices=['github', 'gitlab', 'azure'])
        cicd_parser.add_argument('--include-tests', action='store_true', help='Include automated testing')
        cicd_parser.add_argument('--include-deploy', action='store_true', help='Include automated deployment')
        
        # Infrastructure as Code
        iac_parser = deploy_subparsers.add_parser('iac', help='Generate Infrastructure as Code')
        iac_parser.add_argument('provider', choices=['terraform', 'aws-cdk', 'pulumi'])
        iac_parser.add_argument('--cloud', choices=['aws', 'gcp', 'azure'], help='Cloud provider')
        
        # List supported platforms
        deploy_subparsers.add_parser('list', help='List supported deployment platforms')
        
        # Interactive deployment setup
        deploy_subparsers.add_parser('setup', help='Interactive deployment setup wizard')
        
        return parser
    
    def execute(self, args):
        """Execute deploy command"""
        if args.deploy_action == 'docker':
            self._setup_docker(args)
        elif args.deploy_action == 'platform':
            self._setup_platform(args)
        elif args.deploy_action == 'cicd':
            self._setup_cicd(args)
        elif args.deploy_action == 'iac':
            self._setup_iac(args)
        elif args.deploy_action == 'list':
            self._list_platforms()
        elif args.deploy_action == 'setup':
            self._interactive_setup()
        else:
            print("🚀 DevAlex Deployment & DevOps Automation")
            print("Usage: devalex deploy {docker|platform|cicd|iac|list|setup}")
            
    def _setup_docker(self, args):
        """Setup Docker containerization"""
        automation = self._get_devops_automation()
        
        config = {
            'database': args.database,
            'include_compose': not args.no_compose,
            'include_dev_compose': True,
            'include_redis': True
        }
        
        try:
            result = automation.setup_containerization(args.app_type, args.language, config)
            
            print(f"✅ Docker setup complete for {args.app_type} ({args.language})!")
            
            if result.get('files_created'):
                print(f"\n📝 Files created:")
                for file in result['files_created']:
                    print(f"   • {file}")
                    
            if result.get('next_steps'):
                print(f"\n🚀 Next steps:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
                    
            print(f"\n🐳 Your application is now containerized and ready for deployment!")
            
        except Exception as e:
            print(f"❌ Error setting up Docker: {e}")
            
    def _setup_platform(self, args):
        """Setup deployment platform"""
        automation = self._get_devops_automation()
        
        config = {
            'app_type': args.app_type or 'webapp'
        }
        
        try:
            result = automation.setup_deployment_platform(args.platform, config)
            
            print(f"✅ {args.platform.title()} deployment setup complete!")
            
            if result.get('files_created'):
                print(f"\n📝 Configuration files created:")
                for file in result['files_created']:
                    print(f"   • {file}")
                    
            if result.get('deployment_url'):
                print(f"\n🌐 Platform: {result['deployment_url']}")
                
            if result.get('next_steps'):
                print(f"\n🚀 Next steps:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
                    
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
    def _setup_cicd(self, args):
        """Setup CI/CD pipeline"""
        automation = self._get_devops_automation()
        
        config = {
            'include_tests': args.include_tests,
            'include_deploy': args.include_deploy
        }
        
        try:
            result = automation.setup_cicd_pipeline(args.platform, config)
            
            print(f"✅ {args.platform.title()} CI/CD pipeline setup complete!")
            
            if result.get('files_created'):
                print(f"\n📝 Pipeline files created:")
                for file in result['files_created']:
                    print(f"   • {file}")
                    
            if result.get('features'):
                print(f"\n🎯 Pipeline features:")
                for feature in result['features']:
                    print(f"   • {feature.replace('_', ' ').title()}")
                    
            if result.get('next_steps'):
                print(f"\n🚀 Next steps:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
                    
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
    def _setup_iac(self, args):
        """Setup Infrastructure as Code"""
        automation = self._get_devops_automation()
        
        config = {
            'cloud_provider': args.cloud or 'aws'
        }
        
        try:
            result = automation.generate_infrastructure_as_code(args.provider, config)
            
            print(f"✅ {args.provider.title()} Infrastructure as Code setup complete!")
            print(f"☁️ Target cloud: {config['cloud_provider'].upper()}")
            
            if result.get('files_created'):
                print(f"\n📝 IaC files created:")
                for file in result['files_created']:
                    print(f"   • {file}")
                    
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
    def _list_platforms(self):
        """List supported deployment platforms"""
        automation = self._get_devops_automation()
        platforms = automation.get_supported_platforms()
        
        print("🚀 Supported Deployment Platforms")
        print("=" * 50)
        
        ready_platforms = []
        coming_soon = []
        
        for platform_id, info in platforms.items():
            if info.get('ready', False):
                ready_platforms.append((platform_id, info))
            else:
                coming_soon.append((platform_id, info))
                
        if ready_platforms:
            print("\n✅ Ready to Use:")
            for platform_id, info in ready_platforms:
                print(f"   🚀 {platform_id}")
                print(f"      {info['name']}")
                print(f"      {info['description']}")
                print()
                
        if coming_soon:
            print("🚧 Coming Soon:")
            for platform_id, info in coming_soon:
                print(f"   🔨 {platform_id} - {info['name']}")
                
        print(f"\n💡 Usage Examples:")
        print(f"   devalex deploy docker fastapi --language python")
        print(f"   devalex deploy platform vercel")
        print(f"   devalex deploy cicd github --include-tests")
        
    def _interactive_setup(self):
        """Interactive deployment setup wizard"""
        print("🧙‍♂️ DevAlex Deployment Setup Wizard")
        print("=" * 50)
        print("I'll help you set up deployment for your project!")
        
        automation = self._get_devops_automation()
        
        try:
            # Detect project type
            print("\n🔍 Let's analyze your project...")
            
            project_type = input("What type of project is this? (webapp/api/fullstack) [webapp]: ").strip() or "webapp"
            language = input("What language? (python/javascript/typescript) [python]: ").strip() or "python"
            
            # Containerization setup
            containerize = input(f"\n🐳 Set up Docker containerization? (Y/n): ")
            if containerize.lower() not in ['n', 'no']:
                print("Setting up Docker...")
                
                config = {
                    'include_compose': True,
                    'include_dev_compose': True,
                    'include_redis': True
                }
                
                if project_type in ['webapp', 'fullstack']:
                    database = input("Database? (postgresql/mysql/mongodb) [postgresql]: ").strip() or "postgresql"
                    config['database'] = database
                    
                result = automation.setup_containerization(project_type, language, config)
                print("✅ Docker setup complete!")
                
            # Deployment platform
            print(f"\n🚀 Choose deployment platform:")
            print("1. Vercel (Frontend/JAMstack)")
            print("2. Railway (Full-stack)")
            print("3. Render (Full-stack)")
            print("4. AWS (Advanced)")
            print("5. Skip deployment setup")
            
            choice = input("Select option (1-5): ").strip()
            
            platform_map = {
                '1': 'vercel',
                '2': 'railway', 
                '3': 'render',
                '4': 'aws'
            }
            
            if choice in platform_map:
                platform = platform_map[choice]
                print(f"Setting up {platform} deployment...")
                
                try:
                    config = {'app_type': project_type}
                    result = automation.setup_deployment_platform(platform, config)
                    print(f"✅ {platform.title()} setup complete!")
                except Exception as e:
                    print(f"⚠️ {platform.title()} setup: {e}")
                    
            # CI/CD setup
            cicd_choice = input(f"\n⚙️ Set up CI/CD pipeline? (Y/n): ")
            if cicd_choice.lower() not in ['n', 'no']:
                print("Setting up GitHub Actions CI/CD...")
                
                config = {
                    'include_tests': True,
                    'include_deploy': True
                }
                
                try:
                    result = automation.setup_cicd_pipeline('github', config)
                    print("✅ CI/CD pipeline setup complete!")
                except Exception as e:
                    print(f"⚠️ CI/CD setup: {e}")
                    
            print(f"\n🎉 Deployment setup complete!")
            print(f"Your {project_type} project is now ready for production!")
            
        except KeyboardInterrupt:
            print("\n👋 Deployment setup cancelled")
        except Exception as e:
            print(f"❌ Error in deployment wizard: {e}")