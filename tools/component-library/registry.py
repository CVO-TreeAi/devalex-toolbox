#!/usr/bin/env python3

"""
DevAlex Component Library Registry
Manages reusable components across DevAlex projects
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class ComponentRegistry:
    """Registry for managing reusable development components"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.registry_dir = self.project_path / ".devalex" / "components"
        self.registry_file = self.registry_dir / "registry.json"
        
    def initialize_registry(self):
        """Initialize the component registry"""
        print("🧩 Initializing DevAlex Component Registry")
        print("=" * 40)
        
        # Create registry directory
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        
        # Create default registry
        if not self.registry_file.exists():
            self._create_default_registry()
            
        # Create component templates
        self._create_component_templates()
        
        print("✅ Component registry initialized")
        
    def _create_default_registry(self):
        """Create default component registry"""
        default_registry = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "components": {
                "authentication": {
                    "name": "Authentication Component",
                    "description": "User authentication with JWT tokens",
                    "category": "security",
                    "languages": ["python", "javascript", "typescript"],
                    "frameworks": ["fastapi", "express", "react"],
                    "files": ["auth.py", "auth.js", "useAuth.tsx"],
                    "dependencies": ["jwt", "bcrypt"],
                    "story_points": 8
                },
                "api-client": {
                    "name": "API Client Component", 
                    "description": "Type-safe API client with error handling",
                    "category": "networking",
                    "languages": ["typescript", "python"],
                    "frameworks": ["axios", "requests"],
                    "files": ["apiClient.ts", "api_client.py"],
                    "dependencies": ["axios", "requests"],
                    "story_points": 5
                },
                "database-model": {
                    "name": "Database Model Component",
                    "description": "Base database model with common fields",
                    "category": "database",
                    "languages": ["python", "typescript"],
                    "frameworks": ["sqlalchemy", "prisma", "mongoose"],
                    "files": ["base_model.py", "baseModel.ts"],
                    "dependencies": ["sqlalchemy", "prisma"],
                    "story_points": 3
                },
                "form-validation": {
                    "name": "Form Validation Component",
                    "description": "Reusable form validation with error handling",
                    "category": "ui",
                    "languages": ["typescript", "javascript"],
                    "frameworks": ["react", "vue", "svelte"],
                    "files": ["FormValidator.tsx", "useFormValidation.ts"],
                    "dependencies": ["yup", "zod"],
                    "story_points": 4
                },
                "error-boundary": {
                    "name": "Error Boundary Component",
                    "description": "React error boundary with fallback UI",
                    "category": "ui",
                    "languages": ["typescript", "javascript"],
                    "frameworks": ["react"],
                    "files": ["ErrorBoundary.tsx", "ErrorFallback.tsx"],
                    "dependencies": ["react"],
                    "story_points": 2
                }
            }
        }
        
        with open(self.registry_file, 'w') as f:
            json.dump(default_registry, f, indent=2)
            
    def _create_component_templates(self):
        """Create component templates"""
        templates_dir = self.registry_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Authentication template
        auth_template = '''"""
DevAlex Authentication Component
Provides JWT-based authentication with secure token handling
"""

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

class AuthenticationManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
'''
        
        (templates_dir / "auth.py").write_text(auth_template)
        
        # API Client template
        api_client_template = '''/**
 * DevAlex API Client Component
 * Type-safe API client with comprehensive error handling
 */

import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

export interface ApiError {
  message: string;
  status: number;
  code?: string;
}

export class ApiClient {
  private client: AxiosInstance;
  
  constructor(baseURL: string, token?: string) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
      }
    });
    
    this.setupInterceptors();
  }
  
  private setupInterceptors() {
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError) => {
        const apiError: ApiError = {
          message: error.message,
          status: error.response?.status || 0,
          code: error.code
        };
        return Promise.reject(apiError);
      }
    );
  }
  
  async get<T>(url: string): Promise<T> {
    const response = await this.client.get<T>(url);
    return response.data;
  }
  
  async post<T>(url: string, data: any): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }
  
  async put<T>(url: string, data: any): Promise<T> {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }
  
  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}
'''
        
        (templates_dir / "apiClient.ts").write_text(api_client_template)
        
    def list_components(self) -> List[Dict[str, Any]]:
        """List all available components"""
        if not self.registry_file.exists():
            return []
            
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)
            
        components = []
        for comp_id, comp_data in registry.get("components", {}).items():
            components.append({
                "id": comp_id,
                **comp_data
            })
            
        return components
        
    def search_components(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search components by query and category"""
        all_components = self.list_components()
        
        results = []
        for component in all_components:
            # Match query in name or description
            if query.lower() in component["name"].lower() or query.lower() in component["description"].lower():
                if not category or component.get("category") == category:
                    results.append(component)
                    
        return results
        
    def get_component(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get specific component by ID"""
        components = self.list_components()
        for component in components:
            if component["id"] == component_id:
                return component
        return None
        
    def generate_component(self, component_id: str, target_language: str = "python") -> str:
        """Generate component code for specific language"""
        component = self.get_component(component_id)
        if not component:
            raise ValueError(f"Component {component_id} not found")
            
        template_file = self.registry_dir / "templates" / f"{component_id}.py"
        if target_language != "python":
            # Look for language-specific template
            lang_extensions = {
                "typescript": "ts",
                "javascript": "js", 
                "python": "py"
            }
            ext = lang_extensions.get(target_language, "py")
            template_file = self.registry_dir / "templates" / f"{component_id}.{ext}"
            
        if template_file.exists():
            return template_file.read_text()
        else:
            return f"# {component['name']} template not found for {target_language}"
            
    def add_component(self, component_id: str, component_data: Dict[str, Any]) -> bool:
        """Add new component to registry"""
        if not self.registry_file.exists():
            self.initialize_registry()
            
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)
            
        registry["components"][component_id] = component_data
        
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
            
        return True
        
    def get_categories(self) -> List[str]:
        """Get all available component categories"""
        components = self.list_components()
        categories = set()
        for component in components:
            if "category" in component:
                categories.add(component["category"])
        return sorted(list(categories))
        
    def calculate_total_story_points(self, component_ids: List[str]) -> int:
        """Calculate total story points for a list of components"""
        total = 0
        for comp_id in component_ids:
            component = self.get_component(comp_id)
            if component and "story_points" in component:
                total += component["story_points"]
        return total