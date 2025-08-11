#!/usr/bin/env python3

"""
DevAlex XML Prompt Templates
XML-structured prompts for optimal Claude performance
Following Anthropic's best practices for structured prompting
"""

from typing import Dict, Any, List
from datetime import datetime

class XMLPromptTemplates:
    """XML-structured prompt templates for DevAlex agents"""
    
    @staticmethod
    def tech_stack_analysis_prompt(project_context: Dict[str, Any], user_requirements: Dict[str, Any]) -> str:
        """Generate XML-structured prompt for tech stack analysis"""
        return f"""<tech_analysis_request>
<project_context>
<project_name>{project_context.get('name', 'Unknown')}</project_name>
<project_type>{user_requirements.get('type', 'webapp')}</project_type>
<target_devices>{', '.join(user_requirements.get('devices', ['web']))}</target_devices>
<description>{user_requirements.get('description', '')}</description>
<existing_tech>{project_context.get('detected_languages', [])}</existing_tech>
<package_managers>{project_context.get('package_managers', [])}</package_managers>
</project_context>

<analysis_requirements>
<recommend_stack>true</recommend_stack>
<consider_compatibility>true</consider_compatibility>
<apply_open_source_bias>true</apply_open_source_bias>
<provide_reasoning>true</provide_reasoning>
<include_alternatives>true</include_alternatives>
<estimate_complexity>true</estimate_complexity>
</analysis_requirements>

<output_format>
Please analyze the project context and provide recommendations in the following structure:
1. Recommended technology stack with justification
2. Compatibility warnings (if any)
3. Alternative options for each component
4. Security considerations
5. Development complexity estimate
6. Learning curve assessment
</output_format>
</tech_analysis_request>"""

    @staticmethod
    def agent_coordination_prompt(task_description: str, available_agents: List[str], context: Dict[str, Any]) -> str:
        """Generate XML prompt for agent coordination"""
        return f"""<agent_coordination_request>
<task>
<description>{task_description}</description>
<priority>{context.get('priority', 'medium')}</priority>
<deadline>{context.get('deadline', 'flexible')}</deadline>
</task>

<available_agents>
{chr(10).join([f'<agent name="{agent}" status="available" />' for agent in available_agents])}
</available_agents>

<project_context>
<type>{context.get('project_type', 'webapp')}</type>
<phase>{context.get('development_phase', 'planning')}</phase>
<tech_stack>{context.get('tech_stack', {})}</tech_stack>
</project_context>

<coordination_requirements>
<sequence_planning>true</sequence_planning>
<parallel_execution>where_possible</parallel_execution>
<quality_gates>enforce</quality_gates>
<progress_tracking>detailed</progress_tracking>
</coordination_requirements>

<output_format>
Provide a structured coordination plan:
1. Agent assignment and sequencing
2. Task breakdown and dependencies
3. Quality checkpoints
4. Risk mitigation strategies
5. Success criteria
</output_format>
</agent_coordination_request>"""

    @staticmethod
    def security_analysis_prompt(tech_stack: Dict[str, Any], project_type: str) -> str:
        """Generate XML prompt for security analysis"""
        return f"""<security_analysis_request>
<tech_stack>
<frontend>{tech_stack.get('frontend', 'none')}</frontend>
<backend>{tech_stack.get('backend', 'none')}</backend>
<database>{tech_stack.get('database', 'none')}</database>
<hosting>{tech_stack.get('hosting', 'none')}</hosting>
<auth>{tech_stack.get('auth', 'none')}</auth>
</tech_stack>

<project_profile>
<type>{project_type}</type>
<data_sensitivity>{tech_stack.get('data_sensitivity', 'medium')}</data_sensitivity>
<user_scale>{tech_stack.get('expected_users', 'small')}</user_scale>
<compliance_requirements>{tech_stack.get('compliance', [])}</compliance_requirements>
</project_profile>

<analysis_scope>
<vulnerability_assessment>true</vulnerability_assessment>
<attack_surface_analysis>true</attack_surface_analysis>
<compliance_check>true</compliance_check>
<best_practices_review>true</best_practices_review>
</analysis_scope>

<output_format>
Provide comprehensive security analysis:
1. Potential vulnerabilities by component
2. Attack vectors and mitigation strategies
3. Security best practices for the stack
4. Compliance considerations
5. Security implementation roadmap
</output_format>
</security_analysis_request>"""

    @staticmethod
    def component_generation_prompt(component_type: str, language: str, requirements: Dict[str, Any]) -> str:
        """Generate XML prompt for component code generation"""
        return f"""<component_generation_request>
<component_spec>
<type>{component_type}</type>
<language>{language}</language>
<framework>{requirements.get('framework', 'none')}</framework>
<purpose>{requirements.get('purpose', '')}</purpose>
</component_spec>

<requirements>
<functionality>{requirements.get('functionality', [])}</functionality>
<patterns>{requirements.get('patterns', ['standard'])}</patterns>
<testing>{requirements.get('include_tests', True)}</testing>
<documentation>{requirements.get('include_docs', True)}</documentation>
</requirements>

<constraints>
<code_style>{requirements.get('code_style', 'standard')}</code_style>
<dependencies>{requirements.get('allowed_deps', 'minimal')}</dependencies>
<performance>{requirements.get('performance_level', 'standard')}</performance>
<accessibility>{requirements.get('accessibility', True)}</accessibility>
</constraints>

<output_format>
Generate complete, production-ready component code including:
1. Main component implementation
2. Type definitions (if applicable)
3. Unit tests
4. Usage documentation
5. Integration examples
</output_format>
</component_generation_request>"""

    @staticmethod
    def roadmap_generation_prompt(project_analysis: Dict[str, Any]) -> str:
        """Generate XML prompt for development roadmap creation"""
        return f"""<roadmap_generation_request>
<project_analysis>
<type>{project_analysis.get('project_type', 'webapp')}</type>
<complexity>{project_analysis.get('complexity', 'medium')}</complexity>
<features>{project_analysis.get('features', [])}</features>
<tech_stack>{project_analysis.get('tech_stack', [])}</tech_stack>
<team_size>{project_analysis.get('team_size', 'small')}</team_size>
</project_analysis>

<deliverables>
<prd>true</prd>
<technical_design>true</technical_design>
<development_phases>true</development_phases>
<testing_strategy>true</testing_strategy>
<deployment_plan>true</deployment_plan>
</deliverables>

<estimation_parameters>
<story_points>true</story_points>
<time_estimates>true</time_estimates>
<resource_requirements>true</resource_requirements>
<risk_assessment>true</risk_assessment>
</estimation_parameters>

<output_format>
Create comprehensive development roadmap:
1. Product Requirements Document (PRD)
2. Technical architecture design
3. Phased development plan with milestones
4. Testing and QA strategy
5. Deployment and operations plan
6. Risk mitigation strategies
</output_format>
</roadmap_generation_request>"""

    @staticmethod
    def mcp_validation_prompt(tech_stack: Dict[str, Any], validation_context: str) -> str:
        """Generate XML prompt for MCP-based validation"""
        return f"""<mcp_validation_request>
<tech_stack>
{chr(10).join([f'<{category}>{tech}</{category}>' for category, tech in tech_stack.items() if tech and isinstance(tech, str)])}
</tech_stack>

<validation_context>
<source>{validation_context}</source>
<focus_areas>
<security>true</security>
<compatibility>true</compatibility>
<best_practices>true</best_practices>
<performance>true</performance>
</focus_areas>
</validation_context>

<analysis_depth>comprehensive</analysis_depth>

<output_format>
Provide structured validation results:
1. Security assessment findings
2. Compatibility warnings
3. Best practice recommendations  
4. Performance considerations
5. Actionable improvement suggestions
</output_format>
</mcp_validation_request>"""

class XMLPromptBuilder:
    """Builder class for constructing XML prompts dynamically"""
    
    def __init__(self):
        self.elements = []
        
    def add_context(self, name: str, content: Dict[str, Any]) -> 'XMLPromptBuilder':
        """Add context section to prompt"""
        context_xml = f"<{name}>\n"
        for key, value in content.items():
            if isinstance(value, list):
                context_xml += f"<{key}>{', '.join(str(v) for v in value)}</{key}>\n"
            else:
                context_xml += f"<{key}>{value}</{key}>\n"
        context_xml += f"</{name}>"
        self.elements.append(context_xml)
        return self
        
    def add_requirements(self, requirements: List[str]) -> 'XMLPromptBuilder':
        """Add requirements section"""
        req_xml = "<requirements>\n"
        for req in requirements:
            req_xml += f"<requirement>{req}</requirement>\n"
        req_xml += "</requirements>"
        self.elements.append(req_xml)
        return self
        
    def add_output_format(self, format_description: str) -> 'XMLPromptBuilder':
        """Add output format specification"""
        format_xml = f"<output_format>\n{format_description}\n</output_format>"
        self.elements.append(format_xml)
        return self
        
    def build(self, root_tag: str = "prompt_request") -> str:
        """Build the final XML prompt"""
        return f"<{root_tag}>\n" + "\n\n".join(self.elements) + f"\n</{root_tag}>"

# Example usage functions
def create_tech_analysis_prompt(project_info: Dict[str, Any], requirements: Dict[str, Any]) -> str:
    """Convenience function to create tech analysis prompt"""
    return XMLPromptTemplates.tech_stack_analysis_prompt(project_info, requirements)

def create_agent_workflow_prompt(task: str, agents: List[str], context: Dict[str, Any]) -> str:
    """Convenience function to create agent workflow prompt"""
    return XMLPromptTemplates.agent_coordination_prompt(task, agents, context)