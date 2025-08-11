#!/usr/bin/env python3

"""
DevAlex AI Code Generation
AI-powered code generation and assistant tools
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

class AICodeGenerator:
    """AI-powered code generation assistant"""
    
    def __init__(self):
        self.generators = {
            "function": self._generate_function,
            "class": self._generate_class,
            "component": self._generate_component,
            "test": self._generate_test,
            "api": self._generate_api_endpoint,
            "schema": self._generate_schema,
            "config": self._generate_config,
            "dockerfile": self._generate_dockerfile,
            "workflow": self._generate_workflow
        }
        
    def generate_code(self, code_type: str, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on description and context"""
        print(f"🤖 Generating {code_type} code...")
        print(f"Description: {description}")
        
        if code_type not in self.generators:
            raise ValueError(f"Unsupported code type: {code_type}")
            
        return self.generators[code_type](description, context)
        
    def _generate_function(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate function code from description"""
        language = context.get('language', 'python')
        
        # Extract function details from description
        function_info = self._parse_function_description(description)
        
        if language == 'python':
            return self._generate_python_function(function_info, context)
        elif language == 'typescript':
            return self._generate_typescript_function(function_info, context)
        elif language == 'javascript':
            return self._generate_javascript_function(function_info, context)
        else:
            raise ValueError(f"Unsupported language: {language}")
            
    def _generate_class(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate class code from description"""
        language = context.get('language', 'python')
        
        # Extract class details
        class_info = self._parse_class_description(description)
        
        if language == 'python':
            return self._generate_python_class(class_info, context)
        elif language == 'typescript':
            return self._generate_typescript_class(class_info, context)
        else:
            raise ValueError(f"Unsupported language: {language}")
            
    def _generate_component(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate UI component from description"""
        framework = context.get('framework', 'react')
        
        component_info = self._parse_component_description(description)
        
        if framework == 'react':
            return self._generate_react_component(component_info, context)
        elif framework == 'vue':
            return self._generate_vue_component(component_info, context)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
            
    def _generate_test(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test code for given functionality"""
        language = context.get('language', 'python')
        test_framework = context.get('test_framework', 'pytest' if language == 'python' else 'jest')
        
        if language == 'python' and test_framework == 'pytest':
            return self._generate_pytest_test(description, context)
        elif language in ['javascript', 'typescript'] and test_framework == 'jest':
            return self._generate_jest_test(description, context)
        else:
            raise ValueError(f"Unsupported combination: {language} + {test_framework}")
            
    def _generate_api_endpoint(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API endpoint code"""
        framework = context.get('framework', 'fastapi')
        
        endpoint_info = self._parse_api_description(description)
        
        if framework == 'fastapi':
            return self._generate_fastapi_endpoint(endpoint_info, context)
        elif framework == 'express':
            return self._generate_express_endpoint(endpoint_info, context)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
            
    def _parse_function_description(self, description: str) -> Dict[str, Any]:
        """Parse function description to extract details"""
        info = {
            "name": "",
            "parameters": [],
            "return_type": "Any",
            "description": description,
            "is_async": False
        }
        
        # Extract function name (look for patterns like "function called", "named", etc.)
        name_patterns = [
            r"function (?:called |named )?(\w+)",
            r"(\w+) function",
            r"create (?:a )?(\w+)",
            r"implement (?:a )?(\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, description.lower())
            if match:
                info["name"] = match.group(1)
                break
                
        if not info["name"]:
            # Generate name from description
            words = re.findall(r'\w+', description.lower())
            if words:
                info["name"] = "_".join(words[:3])
                
        # Look for parameters
        if "parameters" in description.lower() or "arguments" in description.lower():
            param_match = re.search(r"(?:parameters?|arguments?|takes?)[:\s]+(.+?)(?:\.|$)", description.lower())
            if param_match:
                param_text = param_match.group(1)
                # Simple parameter extraction
                params = [p.strip() for p in param_text.split(',')]
                info["parameters"] = [{"name": p, "type": "Any"} for p in params if p]
                
        # Check for async indicators
        if any(word in description.lower() for word in ["async", "await", "promise", "asynchronous"]):
            info["is_async"] = True
            
        return info
        
    def _generate_python_function(self, function_info: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Python function code"""
        
        # Build function signature
        params = []
        for param in function_info["parameters"]:
            param_str = f"{param['name']}: {param['type']}"
            params.append(param_str)
            
        param_str = ", ".join(params)
        
        async_keyword = "async " if function_info["is_async"] else ""
        return_annotation = f" -> {function_info['return_type']}" if function_info['return_type'] != "Any" else ""
        
        function_code = f'''{async_keyword}def {function_info["name"]}({param_str}){return_annotation}:
    """
    {function_info["description"]}
    
    Args:
{chr(10).join([f'        {p["name"]}: {p["type"]} - Parameter description' for p in function_info["parameters"]])}
    
    Returns:
        {function_info["return_type"]}: Return value description
    """
    # TODO: Implement function logic
    pass'''
        
        test_code = f'''def test_{function_info["name"]}():
    """Test {function_info["name"]} function"""
    # TODO: Implement test cases
    assert True  # Placeholder'''
    
        return {
            "code": function_code,
            "test": test_code,
            "type": "python_function",
            "filename": f"{function_info['name']}.py",
            "test_filename": f"test_{function_info['name']}.py",
            "imports": ["from typing import Any"] if function_info["return_type"] != "Any" else [],
            "function_info": function_info
        }
        
    def _generate_react_component(self, component_info: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate React component code"""
        
        component_name = component_info["name"]
        props = component_info.get("props", [])
        
        # Build props interface
        props_interface = ""
        if props:
            props_interface = f'''interface {component_name}Props {{
{chr(10).join([f'  {prop["name"]}: {prop["type"]};' for prop in props])}
}}

'''
        
        # Build component
        props_param = f"props: {component_name}Props" if props else ""
        
        react_fc_type = f"React.FC<{component_name}Props>" if props else "React.FC"
        component_code = f'''{props_interface}const {component_name}: {react_fc_type} = ({props_param}) => {{
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">{component_name}</h2>
      {{/* TODO: Implement component logic */}}
      <p>Component: {component_name}</p>
    </div>
  );
}};

export default {component_name};'''

        test_code = f'''import {{ render, screen }} from '@testing-library/react';
import {component_name} from './{component_name}';

describe('{component_name}', () => {{
  test('renders component', () => {{
    render(<{component_name} />);
    expect(screen.getByText('{component_name}')).toBeInTheDocument();
  }});
}});'''
        
        return {
            "code": component_code,
            "test": test_code,
            "type": "react_component",
            "filename": f"{component_name}.tsx",
            "test_filename": f"{component_name}.test.tsx",
            "imports": ["import React from 'react';"],
            "component_info": component_info
        }
        
    def _generate_fastapi_endpoint(self, endpoint_info: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate FastAPI endpoint code"""
        
        method = endpoint_info.get("method", "GET").upper()
        path = endpoint_info.get("path", f"/{endpoint_info['name']}")
        
        # Generate request/response models if needed
        models_code = ""
        if endpoint_info.get("request_model"):
            models_code += f'''class {endpoint_info["name"]}Request(BaseModel):
    # TODO: Define request fields
    pass

'''
        
        if endpoint_info.get("response_model"):
            models_code += f'''class {endpoint_info["name"]}Response(BaseModel):
    # TODO: Define response fields
    pass

'''
        
        # Generate endpoint function
        decorator = f'@router.{method.lower()}("{path}"'
        if endpoint_info.get("response_model"):
            decorator += f', response_model={endpoint_info["name"]}Response'
        decorator += ')'
        
        endpoint_code = f'''{models_code}{decorator}
async def {endpoint_info["name"]}():
    """
    {endpoint_info["description"]}
    """
    # TODO: Implement endpoint logic
    return {{"message": "Endpoint {endpoint_info['name']} implemented"}}'''
        
        test_code = f'''def test_{endpoint_info["name"]}(client):
    """Test {endpoint_info["name"]} endpoint"""
    response = client.{method.lower()}("{path}")
    assert response.status_code == 200
    # TODO: Add more specific assertions'''
        
        return {
            "code": endpoint_code,
            "test": test_code,
            "type": "fastapi_endpoint",
            "filename": f"{endpoint_info['name']}_endpoint.py",
            "test_filename": f"test_{endpoint_info['name']}_endpoint.py",
            "imports": ["from fastapi import APIRouter", "from pydantic import BaseModel"],
            "endpoint_info": endpoint_info
        }
        
    def _parse_component_description(self, description: str) -> Dict[str, Any]:
        """Parse component description"""
        info = {
            "name": "",
            "props": [],
            "description": description
        }
        
        # Extract component name
        name_patterns = [
            r"component (?:called |named )?(\w+)",
            r"(\w+) component",
            r"create (?:a )?(\w+)",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, description.lower())
            if match:
                name = match.group(1)
                # Capitalize first letter for component names
                info["name"] = name.capitalize() + "Component" if not name.endswith("Component") else name.capitalize()
                break
                
        if not info["name"]:
            words = re.findall(r'\w+', description)
            if words:
                info["name"] = "".join(word.capitalize() for word in words[:2]) + "Component"
                
        return info
        
    def _parse_api_description(self, description: str) -> Dict[str, Any]:
        """Parse API endpoint description"""
        info = {
            "name": "",
            "method": "GET",
            "path": "",
            "description": description,
            "request_model": False,
            "response_model": False
        }
        
        # Extract HTTP method
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        for method in methods:
            if method.lower() in description.lower():
                info["method"] = method
                break
                
        # Extract endpoint name
        name_patterns = [
            r"endpoint (?:called |named )?(\w+)",
            r"(\w+) endpoint",
            r"create (?:an? )?(\w+)",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, description.lower())
            if match:
                info["name"] = match.group(1)
                break
                
        if not info["name"]:
            words = re.findall(r'\w+', description.lower())
            if words:
                info["name"] = "_".join(words[:2])
                
        # Generate path
        info["path"] = f"/{info['name'].replace('_', '-')}"
        
        # Check for request/response models
        if any(word in description.lower() for word in ["request", "payload", "body"]):
            info["request_model"] = True
        if any(word in description.lower() for word in ["response", "return", "output"]):
            info["response_model"] = True
            
        return info
        
    def _parse_class_description(self, description: str) -> Dict[str, Any]:
        """Parse class description"""
        info = {
            "name": "",
            "methods": [],
            "attributes": [],
            "description": description,
            "inheritance": None
        }
        
        # Extract class name
        name_patterns = [
            r"class (?:called |named )?(\w+)",
            r"(\w+) class",
            r"create (?:a )?(\w+)",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, description.lower())
            if match:
                name = match.group(1)
                info["name"] = name.capitalize()
                break
                
        if not info["name"]:
            words = re.findall(r'\w+', description)
            if words:
                info["name"] = "".join(word.capitalize() for word in words[:2])
                
        return info
        
    def _generate_python_class(self, class_info: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Python class code"""
        
        class_name = class_info["name"]
        
        class_code = f'''class {class_name}:
    """
    {class_info["description"]}
    """
    
    def __init__(self):
        """Initialize {class_name} instance"""
        # TODO: Initialize instance attributes
        pass
    
    def __str__(self) -> str:
        """String representation of {class_name}"""
        return f"{class_name}()"
    
    def __repr__(self) -> str:
        """Developer representation of {class_name}"""
        return self.__str__()'''

        test_code = f'''import pytest
from .{class_name.lower()} import {class_name}

class Test{class_name}:
    """Test suite for {class_name} class"""
    
    def test_initialization(self):
        """Test {class_name} initialization"""
        instance = {class_name}()
        assert isinstance(instance, {class_name})
    
    def test_string_representation(self):
        """Test string representation"""
        instance = {class_name}()
        assert str(instance) == "{class_name}()"'''
        
        return {
            "code": class_code,
            "test": test_code,
            "type": "python_class",
            "filename": f"{class_name.lower()}.py",
            "test_filename": f"test_{class_name.lower()}.py",
            "imports": [],
            "class_info": class_info
        }
        
    # Placeholder methods for additional generators
    def _generate_typescript_function(self, function_info: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate TypeScript function - placeholder"""
        return {"code": "// TypeScript function generator - Coming soon!", "type": "typescript_function"}
        
    def _generate_schema(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate database schema - placeholder"""
        return {"code": "-- Database schema generator - Coming soon!", "type": "schema"}
        
    def _generate_config(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate configuration file - placeholder"""
        return {"code": "# Configuration generator - Coming soon!", "type": "config"}
        
    def _generate_dockerfile(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Dockerfile - placeholder"""
        return {"code": "# Dockerfile generator - Coming soon!", "type": "dockerfile"}
        
    def _generate_workflow(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate CI/CD workflow - placeholder"""
        return {"code": "# Workflow generator - Coming soon!", "type": "workflow"}
        
    def get_available_generators(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available code generators"""
        return {
            "function": {
                "name": "Function Generator",
                "description": "Generate functions from natural language descriptions",
                "languages": ["python", "typescript", "javascript"],
                "ready": True
            },
            "class": {
                "name": "Class Generator", 
                "description": "Generate classes with methods and attributes",
                "languages": ["python", "typescript"],
                "ready": True
            },
            "component": {
                "name": "UI Component Generator",
                "description": "Generate UI components for web frameworks",
                "frameworks": ["react", "vue"],
                "ready": True
            },
            "test": {
                "name": "Test Generator",
                "description": "Generate test cases for existing code",
                "frameworks": ["pytest", "jest"],
                "ready": False
            },
            "api": {
                "name": "API Endpoint Generator",
                "description": "Generate REST API endpoints",
                "frameworks": ["fastapi", "express"],
                "ready": True
            },
            "schema": {
                "name": "Database Schema Generator",
                "description": "Generate database schemas and migrations",
                "databases": ["postgresql", "mysql", "mongodb"],
                "ready": False
            }
        }