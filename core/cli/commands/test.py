"""DevAlex test command - Testing automation and tools"""

import sys
from pathlib import Path
from .base import BaseCommand

class TestCommand(BaseCommand):
    """Testing automation and quality assurance tools"""
    
    def _get_test_automation(self):
        """Get test automation with dynamic import"""
        tools_path = str(Path(__file__).parent.parent.parent.parent / "tools" / "testing")
        sys.path.insert(0, tools_path)
        from test_automation import TestAutomation
        return TestAutomation()
    
    @classmethod
    def register(cls, subparsers):
        """Register test command"""
        parser = subparsers.add_parser('test', help='Testing automation and QA tools')
        test_subparsers = parser.add_subparsers(dest='test_action', help='Test actions')
        
        # Setup testing framework
        setup_parser = test_subparsers.add_parser('setup', help='Setup testing framework')
        setup_parser.add_argument('language', choices=['python', 'javascript', 'typescript'], 
                                 help='Programming language')
        setup_parser.add_argument('--framework', help='Testing framework (pytest, jest, etc.)')
        
        # Generate tests for files
        generate_parser = test_subparsers.add_parser('generate', help='Generate tests for files')
        generate_parser.add_argument('files', nargs='+', help='Files to generate tests for')
        generate_parser.add_argument('--type', default='unit', choices=['unit', 'integration', 'e2e'],
                                   help='Type of tests to generate')
        generate_parser.add_argument('--save', action='store_true', help='Save generated tests to files')
        
        # Run comprehensive test suite
        run_parser = test_subparsers.add_parser('run', help='Run comprehensive test suite')
        run_parser.add_argument('--types', nargs='+', default=['unit'], 
                               choices=['unit', 'integration', 'e2e'], 
                               help='Types of tests to run')
        run_parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
        
        # Test analysis and reporting
        test_subparsers.add_parser('analyze', help='Analyze test coverage and performance')
        
        # Interactive test assistant
        test_subparsers.add_parser('assistant', help='Interactive test generation assistant')
        
        return parser
    
    def execute(self, args):
        """Execute test command"""
        if args.test_action == 'setup':
            self._setup_testing(args)
        elif args.test_action == 'generate':
            self._generate_tests(args)
        elif args.test_action == 'run':
            self._run_tests(args)
        elif args.test_action == 'analyze':
            self._analyze_tests()
        elif args.test_action == 'assistant':
            self._test_assistant()
        else:
            print("🧪 DevAlex Testing Automation")
            print("Usage: devalex test {setup|generate|run|analyze|assistant}")
            
    def _setup_testing(self, args):
        """Setup testing framework for project"""
        automation = self._get_test_automation()
        
        try:
            print(f"🧪 Setting up {args.language} testing framework...")
            if args.framework:
                print(f"Framework: {args.framework}")
                
            result = automation.setup_testing_framework(args.language, args.framework)
            
            print(f"✅ {result['framework']} testing setup complete!")
            
            if result.get('config_files'):
                print(f"\n📝 Configuration files created:")
                for config_file in result['config_files']:
                    print(f"   • {config_file}")
                    
            if result.get('directories'):
                print(f"\n📁 Test directories created:")
                for directory in result['directories']:
                    print(f"   • {directory}")
                    
            if result.get('next_steps'):
                print(f"\n🚀 Next steps:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
                    
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
    def _generate_tests(self, args):
        """Generate tests for specified files"""
        automation = self._get_test_automation()
        
        print(f"🔬 Generating {args.type} tests for {len(args.files)} files...")
        
        try:
            result = automation.generate_test_suite(args.files, args.type)
            
            print(f"✅ Test generation complete!")
            print(f"📊 Files processed: {result['files_processed']}")
            print(f"🧪 Tests generated: {result['tests_generated']}")
            
            if result['generated_tests']:
                print(f"\n📋 Generated Tests:")
                for i, test in enumerate(result['generated_tests'], 1):
                    print(f"   {i}. {test['source_file']} → {test['test_file']}")
                    
                    if args.save:
                        # Save test files
                        test_path = Path(test['test_file'])
                        test_path.parent.mkdir(parents=True, exist_ok=True)
                        test_path.write_text(test['generated_tests'])
                        print(f"      💾 Saved: {test['test_file']}")
                        
            framework = result.get('framework_setup')
            if framework and framework != 'unknown':
                print(f"\n🎯 Using {framework} framework")
            else:
                print(f"\n⚠️ No testing framework detected")
                print(f"   Run: devalex test setup <language>")
                
        except Exception as e:
            print(f"❌ Error generating tests: {e}")
            
    def _run_tests(self, args):
        """Run comprehensive test suite"""
        automation = self._get_test_automation()
        
        print(f"🚀 Running {', '.join(args.types)} tests...")
        if args.coverage:
            print("📊 Including coverage analysis...")
            
        try:
            result = automation.run_comprehensive_tests(args.types)
            
            print(f"✅ Test execution complete!")
            print(f"⏱️ Duration: {result['start_time']} → {result['end_time']}")
            
            # Show test results
            for test_type, test_result in result['test_results'].items():
                if 'error' in test_result:
                    print(f"❌ {test_type.title()} tests: {test_result['error']}")
                else:
                    print(f"✅ {test_type.title()} tests: Completed")
                    
            # Show coverage if available
            coverage = result.get('coverage', {})
            if coverage and not coverage.get('error'):
                print(f"\n📊 Code Coverage:")
                if coverage.get('overall_coverage'):
                    print(f"   Overall: {coverage['overall_coverage']:.1f}%")
                if coverage.get('line_coverage'):
                    print(f"   Lines: {coverage['line_coverage']:.1f}%")
                if coverage.get('function_coverage'):
                    print(f"   Functions: {coverage['function_coverage']:.1f}%")
                    
            # Show summary
            summary = result.get('summary', {})
            if summary:
                print(f"\n📈 Summary: {summary}")
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            
    def _analyze_tests(self):
        """Analyze test coverage and performance"""
        print("📊 Analyzing test coverage and performance...")
        
        automation = self._get_test_automation()
        
        try:
            # Generate coverage report
            coverage = automation._generate_coverage_report()
            
            print("📈 Test Analysis Report")
            print("=" * 40)
            
            if coverage.get('error'):
                print(f"❌ Coverage analysis failed: {coverage['error']}")
            else:
                print("Coverage Analysis:")
                print(f"   Overall Coverage: {coverage.get('overall_coverage', 0):.1f}%")
                print(f"   Line Coverage: {coverage.get('line_coverage', 0):.1f}%")
                print(f"   Branch Coverage: {coverage.get('branch_coverage', 0):.1f}%")
                print(f"   Function Coverage: {coverage.get('function_coverage', 0):.1f}%")
                
                if coverage.get('uncovered_files'):
                    print(f"\n📋 Files needing tests:")
                    for file in coverage['uncovered_files'][:5]:
                        print(f"   • {file}")
                        
                if coverage.get('report_location'):
                    print(f"\n📊 Full report: {coverage['report_location']}")
                    
            # Test recommendations
            print(f"\n💡 Recommendations:")
            print(f"   • Add tests for uncovered functions")
            print(f"   • Improve edge case testing")
            print(f"   • Add integration tests")
            print(f"   • Set up automated testing in CI/CD")
            
        except Exception as e:
            print(f"❌ Error analyzing tests: {e}")
            
    def _test_assistant(self):
        """Interactive test generation assistant"""
        print("🧙‍♂️ DevAlex Test Generation Assistant")
        print("=" * 50)
        print("I'll help you set up comprehensive testing for your project!")
        
        automation = self._get_test_automation()
        
        try:
            # Detect project type
            framework = automation._detect_test_framework()
            
            if framework == "unknown":
                print("🔍 No testing framework detected.")
                
                language = input("What language is your project? (python/javascript/typescript): ").strip().lower()
                if language not in ['python', 'javascript', 'typescript']:
                    print("❌ Unsupported language")
                    return
                    
                setup_choice = input(f"\nWould you like to set up testing for {language}? (Y/n): ")
                if setup_choice.lower() not in ['n', 'no']:
                    result = automation.setup_testing_framework(language)
                    print(f"✅ {result['framework']} setup complete!")
                    framework = result['framework']
            else:
                print(f"✅ Detected testing framework: {framework}")
                
            # Offer to generate tests for existing files
            print(f"\n🔍 Scanning for files that need tests...")
            
            # Find source files
            source_files = []
            for pattern in ['src/**/*.py', 'src/**/*.js', 'src/**/*.ts', '*.py', '*.js', '*.ts']:
                source_files.extend(Path('.').glob(pattern))
                
            if source_files:
                print(f"Found {len(source_files)} source files:")
                for i, file in enumerate(source_files[:10], 1):
                    print(f"   {i}. {file}")
                    
                if len(source_files) > 10:
                    print(f"   ... and {len(source_files) - 10} more")
                    
                generate_choice = input(f"\nGenerate tests for these files? (Y/n): ")
                if generate_choice.lower() not in ['n', 'no']:
                    file_list = [str(f) for f in source_files[:5]]  # Limit to first 5
                    result = automation.generate_test_suite(file_list, "unit")
                    print(f"✅ Generated {result['tests_generated']} test suites!")
            else:
                print("No source files found in common locations.")
                
            # Offer to run tests
            run_choice = input(f"\nRun existing tests? (Y/n): ")
            if run_choice.lower() not in ['n', 'no']:
                result = automation.run_comprehensive_tests(['unit'])
                print("✅ Test execution complete!")
                
        except KeyboardInterrupt:
            print("\n👋 Test assistant cancelled")
        except Exception as e:
            print(f"❌ Error in test assistant: {e}")