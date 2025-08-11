#!/usr/bin/env python3

"""
DevAlex Agent Orchestration System
Manages AI agents for comprehensive development workflows
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from .xml_prompts import XMLPromptTemplates

@dataclass
class AgentConfig:
    """Configuration for a DevAlex agent"""
    role: str
    goal: str
    backstory: str
    verbose: bool = True
    allow_delegation: bool = True
    allow_code_execution: bool = True
    tools: List[str] = None
    llm: str = "claude-3-5-sonnet"
    max_iter: int = 25
    memory: bool = True
    step_callback: Optional[str] = None
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []

@dataclass 
class TaskConfig:
    """Configuration for a DevAlex task"""
    description: str
    agent: str
    expected_output: str
    tools: List[str] = None
    async_execution: bool = False
    context: List[str] = None
    output_file: Optional[str] = None
    callback: Optional[str] = None
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []
        if self.context is None:
            self.context = []

class DevAlexAgentSystem:
    """Manages DevAlex agent orchestration for development workflows"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.agents_path = self.project_path / "core" / "agents"
        self.configs_path = self.agents_path / "configs"
        self.workflows_path = self.agents_path / "workflows"
        self.tools_path = self.agents_path / "tools"
        
    def initialize_agent_system(self):
        """Initialize the DevAlex agent system"""
        print("🤖 Initializing DevAlex Agent System")
        print("=" * 50)
        
        # Create directory structure
        self._create_directory_structure()
        
        # Create the six core agents
        self._create_core_agents()
        
        # Create agent workflows
        self._create_agent_workflows()
        
        # Create coordination system
        self._create_coordination_system()
        
        print("✅ DevAlex Agent System initialized")
        
    def _create_directory_structure(self):
        """Create agent system directory structure"""
        print("📁 Creating agent directory structure...")
        
        directories = [
            self.agents_path,
            self.configs_path,
            self.workflows_path,
            self.tools_path,
            self.agents_path / "coordination"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _create_core_agents(self):
        """Create the six core DevAlex agents"""
        print("🤖 Creating core agent configurations...")
        
        # Define the six core agents
        agents = {
            "architecture": AgentConfig(
                role="Senior Software Architect",
                goal="Design robust, scalable, and maintainable system architectures following SOLID principles and best practices",
                backstory="""You are a seasoned software architect with 15+ years of experience designing 
                large-scale systems. You specialize in Domain-Driven Design, microservices architecture, 
                and creating systems that can evolve over time. You always consider scalability, security, 
                and maintainability in your designs.""",
                tools=["system_design", "uml_generator", "architecture_validator"],
                allow_delegation=True
            ),
            
            "development": AgentConfig(
                role="Full-Stack Development Expert",
                goal="Implement complete features with clean, testable, and well-documented code across the entire stack",
                backstory="""You are an expert full-stack developer with deep knowledge of modern frameworks, 
                databases, APIs, and frontend technologies. You write clean, efficient code following best 
                practices and design patterns. You always consider performance, security, and user experience.""",
                tools=["code_generator", "test_runner", "code_analyzer", "documentation_generator"],
                allow_delegation=True
            ),
            
            "testing": AgentConfig(
                role="Quality Assurance Specialist",
                goal="Ensure comprehensive testing coverage with unit, integration, and end-to-end tests",
                backstory="""You are a testing expert who believes in test-driven development and comprehensive 
                quality assurance. You create robust test suites that catch bugs early and ensure code reliability. 
                You're experienced with various testing frameworks and methodologies.""",
                tools=["test_generator", "coverage_analyzer", "performance_tester", "bug_tracker"],
                allow_delegation=False
            ),
            
            "security": AgentConfig(
                role="Cybersecurity Expert",
                goal="Identify security vulnerabilities and implement robust security measures throughout the system",
                backstory="""You are a cybersecurity specialist with expertise in application security, 
                penetration testing, and secure coding practices. You understand OWASP guidelines and 
                can identify potential security risks before they become problems.""",
                tools=["security_scanner", "vulnerability_detector", "crypto_validator", "auth_analyzer"],
                allow_delegation=False
            ),
            
            "operations": AgentConfig(
                role="DevOps Engineering Expert",
                goal="Design and implement robust deployment pipelines, monitoring, and infrastructure management",
                backstory="""You are a DevOps engineer with expertise in cloud infrastructure, containerization, 
                CI/CD pipelines, and system monitoring. You ensure applications are deployable, scalable, 
                and maintainable in production environments.""",
                tools=["deployment_manager", "infrastructure_analyzer", "monitoring_setup", "scaling_optimizer"],
                allow_delegation=True
            ),
            
            "orchestrator": AgentConfig(
                role="Development Orchestration Coordinator",
                goal="Coordinate multi-agent workflows and ensure all agents work together effectively toward project goals",
                backstory="""You are an expert project coordinator who understands how different development 
                disciplines work together. You orchestrate complex workflows, manage dependencies between tasks, 
                and ensure all agents collaborate effectively to deliver high-quality software.""",
                tools=["workflow_manager", "task_coordinator", "progress_tracker", "team_communicator"],
                allow_delegation=True,
                max_iter=50
            )
        }
        
        # Save agent configurations
        agents_config = {}
        for agent_name, agent_config in agents.items():
            config_file = self.configs_path / f"{agent_name}_agent.yml"
            config_dict = asdict(agent_config)
            
            with open(config_file, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
            
            agents_config[agent_name] = config_dict
            print(f"  🤖 Created: {agent_name} agent")
        
        # Create master agents config
        master_config = self.configs_path / "agents.yml"
        with open(master_config, 'w') as f:
            yaml.dump(agents_config, f, default_flow_style=False)
        
    def _create_agent_workflows(self):
        """Create agent workflow definitions"""
        print("🔄 Creating agent workflows...")
        
        workflows = {
            "feature_development": {
                "description": "Complete feature development workflow",
                "agents": ["architecture", "development", "testing", "security"],
                "coordinator": "orchestrator",
                "steps": [
                    {
                        "name": "architecture_design",
                        "agent": "architecture",
                        "description": "Design feature architecture and integration points"
                    },
                    {
                        "name": "implementation",
                        "agent": "development", 
                        "description": "Implement feature with clean, testable code",
                        "depends_on": ["architecture_design"]
                    },
                    {
                        "name": "testing",
                        "agent": "testing",
                        "description": "Create comprehensive test suite",
                        "depends_on": ["implementation"]
                    },
                    {
                        "name": "security_review",
                        "agent": "security",
                        "description": "Security analysis and vulnerability assessment",
                        "depends_on": ["implementation"]
                    },
                    {
                        "name": "coordination",
                        "agent": "orchestrator",
                        "description": "Coordinate all agents and finalize feature",
                        "depends_on": ["testing", "security_review"]
                    }
                ]
            },
            
            "project_initialization": {
                "description": "New project setup and architecture planning",
                "agents": ["architecture", "security", "operations"],
                "coordinator": "orchestrator", 
                "steps": [
                    {
                        "name": "requirements_analysis",
                        "agent": "orchestrator",
                        "description": "Analyze project requirements and create development roadmap"
                    },
                    {
                        "name": "system_design",
                        "agent": "architecture",
                        "description": "Design overall system architecture",
                        "depends_on": ["requirements_analysis"]
                    },
                    {
                        "name": "security_foundation",
                        "agent": "security",
                        "description": "Establish security foundation and best practices",
                        "depends_on": ["system_design"]
                    },
                    {
                        "name": "deployment_setup",
                        "agent": "operations",
                        "description": "Setup deployment pipeline and infrastructure",
                        "depends_on": ["system_design"]
                    }
                ]
            },
            
            "code_review": {
                "description": "Comprehensive code review workflow",
                "agents": ["development", "testing", "security"],
                "coordinator": "orchestrator",
                "steps": [
                    {
                        "name": "code_analysis",
                        "agent": "development",
                        "description": "Analyze code quality, patterns, and best practices"
                    },
                    {
                        "name": "test_coverage",
                        "agent": "testing", 
                        "description": "Review test coverage and quality",
                        "depends_on": ["code_analysis"]
                    },
                    {
                        "name": "security_scan",
                        "agent": "security",
                        "description": "Scan for security vulnerabilities",
                        "depends_on": ["code_analysis"]
                    },
                    {
                        "name": "review_summary",
                        "agent": "orchestrator",
                        "description": "Compile comprehensive review results",
                        "depends_on": ["test_coverage", "security_scan"]
                    }
                ]
            }
        }
        
        for workflow_name, workflow_config in workflows.items():
            workflow_file = self.workflows_path / f"{workflow_name}.yml"
            with open(workflow_file, 'w') as f:
                yaml.dump(workflow_config, f, default_flow_style=False)
            print(f"  🔄 Created: {workflow_name} workflow")
            
    def _create_coordination_system(self):
        """Create agent coordination system"""
        print("🎯 Creating agent coordination system...")
        
        coordination_config = {
            "coordination_rules": {
                "max_concurrent_agents": 3,
                "timeout_minutes": 30,
                "retry_attempts": 2,
                "communication_protocol": "async_message_passing"
            },
            "agent_priorities": {
                "orchestrator": 1,
                "architecture": 2,
                "security": 2,
                "development": 3,
                "testing": 4,
                "operations": 5
            },
            "escalation_rules": [
                {
                    "condition": "agent_timeout",
                    "action": "escalate_to_orchestrator"
                },
                {
                    "condition": "security_issue_found", 
                    "action": "immediate_security_review"
                },
                {
                    "condition": "test_coverage_below_threshold",
                    "action": "require_additional_testing"
                }
            ]
        }
        
        coordination_file = self.agents_path / "coordination" / "rules.yml"
        with open(coordination_file, 'w') as f:
            yaml.dump(coordination_config, f, default_flow_style=False)
        
        print("  🎯 Agent coordination rules created")
        
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        if not self.configs_path.exists():
            return {"status": "not_initialized", "agents": []}
        
        agents = []
        for config_file in self.configs_path.glob("*_agent.yml"):
            agent_name = config_file.stem.replace("_agent", "")
            agents.append({
                "name": agent_name,
                "status": "ready",
                "config_file": str(config_file)
            })
            
        return {
            "status": "ready" if agents else "not_initialized",
            "agents": agents,
            "workflows": list(self.workflows_path.glob("*.yml")) if self.workflows_path.exists() else []
        }
        
    def run_workflow(self, workflow_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run an agent workflow"""
        workflow_file = self.workflows_path / f"{workflow_name}.yml"
        if not workflow_file.exists():
            return {"error": f"Workflow {workflow_name} not found"}
        
        print(f"🚀 Running workflow: {workflow_name}")
        # This would integrate with actual CrewAI execution in full implementation
        return {
            "workflow": workflow_name,
            "status": "simulated",
            "message": "Workflow execution is under development"
        }