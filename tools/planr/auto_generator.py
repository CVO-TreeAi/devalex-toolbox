#!/usr/bin/env python3

"""
DevAlex Planr - Auto Roadmap Generator
Automatically generates development roadmaps when DevAlex is activated in a project
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

class AutoRoadmapGenerator:
    """Automatically generates development roadmaps for projects"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.planr_dir = self.project_path / ".planr"
        
    def detect_and_generate_roadmap(self) -> Dict[str, Any]:
        """Auto-detect project type and generate appropriate roadmap"""
        print("🗺️ DevAlex Auto-Roadmap Generation")
        print("=" * 40)
        
        # Ensure .planr directory exists
        self.planr_dir.mkdir(exist_ok=True)
        
        # Analyze project structure
        project_analysis = self._analyze_project_structure()
        
        # Generate PRD if missing
        if not (self.planr_dir / "prd.md").exists():
            self._generate_prd(project_analysis)
            
        # Generate tech stack if missing  
        if not (self.planr_dir / "tech-stack.md").exists():
            self._generate_tech_stack(project_analysis)
            
        # Generate roadmap
        roadmap = self._generate_roadmap(project_analysis)
        
        print("✅ Auto-roadmap generation complete!")
        return roadmap
        
    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze project structure to understand requirements"""
        analysis = {
            "project_type": "unknown",
            "tech_stack": [],
            "complexity": "medium",
            "features": [],
            "existing_files": [],
            "dependencies": {}
        }
        
        # Check for common files and patterns
        file_patterns = {
            "package.json": "node_js",
            "requirements.txt": "python",
            "Cargo.toml": "rust", 
            "go.mod": "golang",
            "pom.xml": "java",
            "Gemfile": "ruby",
            "composer.json": "php"
        }
        
        for filename, tech in file_patterns.items():
            if (self.project_path / filename).exists():
                analysis["tech_stack"].append(tech)
                analysis["existing_files"].append(filename)
                
        # Analyze directory structure
        common_dirs = ["src", "lib", "app", "pages", "components", "api", "backend", "frontend"]
        for dir_name in common_dirs:
            if (self.project_path / dir_name).exists():
                analysis["features"].append(f"{dir_name}_structure")
                
        # Detect project type
        analysis["project_type"] = self._detect_project_type(analysis)
        
        # Analyze complexity
        analysis["complexity"] = self._assess_complexity(analysis)
        
        # Read existing documentation
        analysis["documentation"] = self._scan_documentation()
        
        return analysis
        
    def _detect_project_type(self, analysis: Dict[str, Any]) -> str:
        """Detect project type based on structure and files"""
        files = analysis["existing_files"]
        features = analysis["features"]
        
        # Web application patterns
        if "package.json" in files:
            if any(d in features for d in ["pages", "components", "src_structure"]):
                return "webapp"
            elif "api" in features or "backend" in features:
                return "api"
                
        # Python patterns
        if "requirements.txt" in files:
            if any(keyword in str(self.project_path).lower() for keyword in ["ml", "ai", "data", "model"]):
                return "ai"
            elif "api" in features:
                return "api"
            else:
                return "python_app"
                
        # Mobile patterns
        if any(file in files for file in ["pubspec.yaml", "ios", "android"]):
            return "mobile"
            
        # Default detection
        if len(analysis["tech_stack"]) > 0:
            return "webapp"
            
        return "custom"
        
    def _assess_complexity(self, analysis: Dict[str, Any]) -> str:
        """Assess project complexity"""
        complexity_score = 0
        
        # Multiple tech stacks increase complexity
        complexity_score += len(analysis["tech_stack"]) * 2
        
        # Multiple features increase complexity
        complexity_score += len(analysis["features"])
        
        # Complex patterns
        complex_patterns = ["microservice", "distributed", "kubernetes", "docker"]
        for pattern in complex_patterns:
            if any(pattern in str(f).lower() for f in analysis["existing_files"]):
                complexity_score += 5
                
        if complexity_score <= 5:
            return "simple"
        elif complexity_score <= 15:
            return "medium"
        else:
            return "complex"
            
    def _scan_documentation(self) -> List[str]:
        """Scan for existing documentation"""
        doc_files = []
        doc_patterns = ["*.md", "*.rst", "*.txt"]
        
        for pattern in doc_patterns:
            for file in self.project_path.glob(pattern):
                if file.is_file() and file.name.lower() not in ["license", "changelog"]:
                    doc_files.append(str(file))
                    
        return doc_files
        
    def _generate_prd(self, analysis: Dict[str, Any]):
        """Generate Product Requirements Document"""
        print("📋 Generating PRD...")
        
        project_name = self.project_path.name
        project_type = analysis["project_type"]
        
        prd_content = f"""# Product Requirements Document - {project_name}

## Project Overview
**Project Name**: {project_name}  
**Project Type**: {project_type}  
**Complexity**: {analysis["complexity"]}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Vision Statement
{self._generate_vision_statement(project_name, project_type)}

## Technology Stack
{self._format_tech_stack(analysis["tech_stack"])}

## Functional Requirements

### Core Features
{self._generate_core_features(project_type)}

### User Stories
{self._generate_user_stories(project_type)}

### Technical Requirements
{self._generate_technical_requirements(analysis)}

## Non-Functional Requirements

### Performance
- Response time: < 200ms for API calls
- Page load time: < 2 seconds
- Support for {self._get_user_scale(analysis["complexity"])} concurrent users

### Security
- Authentication and authorization
- Input validation and sanitization
- HTTPS/SSL encryption
- OWASP compliance

### Scalability
- Horizontal scaling capability
- Database optimization
- Caching strategy
- Load balancing

## Success Criteria
{self._generate_success_criteria(project_type)}

## Timeline Estimates
Based on project complexity ({analysis["complexity"]}):
- **Planning Phase**: 1-2 weeks
- **Development Phase**: {self._estimate_dev_time(analysis["complexity"])}
- **Testing Phase**: 2-3 weeks  
- **Deployment Phase**: 1 week

## Story Point Estimates
{self._generate_story_points(analysis)}

---
*Auto-generated by DevAlex Planr*"""

        prd_file = self.planr_dir / "prd.md"
        prd_file.write_text(prd_content)
        print(f"  📋 PRD generated: {prd_file}")
        
    def _generate_tech_stack(self, analysis: Dict[str, Any]):
        """Generate technical stack document"""
        print("⚙️ Generating Tech Stack...")
        
        tech_stack_content = f"""# Technical Stack - {self.project_path.name}

## Technology Choices
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Detected Technologies
{self._format_detailed_tech_stack(analysis)}

## Architecture Pattern
**Recommended**: {self._recommend_architecture(analysis)}

## Development Environment
- **Version Control**: Git
- **Code Quality**: ESLint, Prettier, Black (language-specific)
- **Testing**: Jest, PyTest, or language-appropriate frameworks
- **CI/CD**: GitHub Actions
- **Containerization**: Docker (recommended)

## Database Strategy
{self._recommend_database(analysis)}

## Deployment Strategy  
{self._recommend_deployment(analysis)}

## Security Considerations
- Authentication: OAuth 2.1 + JWT
- Authorization: RBAC (Role-Based Access Control)
- Data encryption: AES-256
- Transport security: TLS 1.3
- Input validation: Comprehensive sanitization

## Monitoring & Observability
- Logging: Structured logging with correlation IDs
- Metrics: Application and business metrics
- Health checks: Ready/live endpoints
- Error tracking: Comprehensive error reporting

## DevAlex Integration
- **Agent Orchestration**: All 6 DevAlex agents available
- **Auto-dependency management**: Enabled
- **Security scanning**: Automated
- **Code quality**: Continuous monitoring
- **Claude Code integration**: Optimized .cursorrules

---
*Auto-generated by DevAlex Planr*"""

        tech_stack_file = self.planr_dir / "tech-stack.md"
        tech_stack_file.write_text(tech_stack_content)
        print(f"  ⚙️ Tech Stack generated: {tech_stack_file}")
        
    def _generate_roadmap(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate development roadmap using the template"""
        print("🗺️ Generating Development Roadmap...")
        
        # Load the roadmap template
        template_path = Path(__file__).parent / "templates" / "roadmap-template.md"
        if not template_path.exists():
            # Use the one from .planr in the main project
            template_path = self.project_path / ".." / ".." / ".planr" / "roadmap-template.md"
            
        if template_path.exists():
            template_content = template_path.read_text()
        else:
            template_content = self._get_default_roadmap_template()
            
        # Replace template variables
        roadmap_content = template_content.replace("<PROJECT_NAME>", self.project_path.name)
        roadmap_content = roadmap_content.replace("<PRD_PATH>", ".planr/prd.md")
        roadmap_content = roadmap_content.replace("<TECH_STACK_PATH>", ".planr/tech-stack.md")
        roadmap_content = roadmap_content.replace("<DATE>", f"{datetime.now().strftime('%B %Y')} capabilities")
        roadmap_content = roadmap_content.replace("<MAX_CONTEXT_TOKENS>", "Context Window: 200k, Max Output Tokens: 100k")
        
        # Add actual analysis results
        roadmap_content = self._customize_roadmap_with_analysis(roadmap_content, analysis)
        
        roadmap_file = self.planr_dir / "roadmap.md"
        roadmap_file.write_text(roadmap_content)
        print(f"  🗺️ Roadmap generated: {roadmap_file}")
        
        return {
            "project_name": self.project_path.name,
            "project_type": analysis["project_type"],
            "complexity": analysis["complexity"],
            "total_story_points": self._calculate_total_story_points(analysis),
            "estimated_timeline": self._estimate_dev_time(analysis["complexity"]),
            "files_generated": [
                str(self.planr_dir / "prd.md"),
                str(self.planr_dir / "tech-stack.md"), 
                str(self.planr_dir / "roadmap.md")
            ]
        }
        
    # Helper methods for content generation
    def _generate_vision_statement(self, project_name: str, project_type: str) -> str:
        statements = {
            "webapp": f"Create a modern, responsive web application that delivers exceptional user experience while maintaining high performance and security standards.",
            "api": f"Build a robust, scalable API that provides reliable data access and business logic execution for client applications.",
            "mobile": f"Develop a native mobile application that provides seamless user experience across devices with offline capabilities.",
            "ai": f"Implement an AI/ML solution that processes data intelligently and provides actionable insights to users.",
            "custom": f"Deliver a custom solution that meets specific business requirements while following software engineering best practices."
        }
        return statements.get(project_type, statements["custom"])
        
    def _generate_core_features(self, project_type: str) -> str:
        features = {
            "webapp": """1. **User Interface**: Responsive, accessible web interface
2. **User Management**: Authentication and user profiles  
3. **Core Functionality**: Main application features
4. **Data Management**: CRUD operations for primary entities
5. **Integration**: External API integrations as needed""",
            "api": """1. **Authentication**: Secure API authentication
2. **Core Endpoints**: RESTful API endpoints for all operations
3. **Data Validation**: Input validation and sanitization
4. **Error Handling**: Comprehensive error responses
5. **Documentation**: OpenAPI/Swagger documentation""",
            "mobile": """1. **User Interface**: Native mobile UI/UX
2. **Authentication**: Secure user authentication
3. **Core Features**: Main application functionality
4. **Offline Support**: Local data storage and sync
5. **Push Notifications**: Real-time user engagement""",
            "ai": """1. **Data Pipeline**: Data ingestion and preprocessing
2. **Model Training**: ML model development and training
3. **Inference API**: Model serving and prediction endpoints
4. **Monitoring**: Model performance monitoring
5. **User Interface**: Results visualization and interaction"""
        }
        return features.get(project_type, features["webapp"])
        
    def _generate_user_stories(self, project_type: str) -> str:
        stories = {
            "webapp": """As a user, I want to:
- **US-001**: Register and authenticate securely
- **US-002**: Access the main application features  
- **US-003**: Manage my profile and preferences
- **US-004**: Perform core business operations
- **US-005**: Receive notifications and updates""",
            "api": """As a client application, I want to:
- **US-001**: Authenticate securely with the API
- **US-002**: Access data through RESTful endpoints
- **US-003**: Receive consistent error responses
- **US-004**: Have comprehensive API documentation
- **US-005**: Monitor API performance and usage""",
            "mobile": """As a mobile user, I want to:
- **US-001**: Install and set up the app easily
- **US-002**: Use the app offline when needed
- **US-003**: Receive push notifications
- **US-004**: Have a smooth, native user experience
- **US-005**: Sync data across devices""",
            "ai": """As a user, I want to:
- **US-001**: Upload data for processing
- **US-002**: Receive accurate AI predictions
- **US-003**: Understand how predictions are made
- **US-004**: Track model performance over time
- **US-005**: Export results and insights"""
        }
        return stories.get(project_type, stories["webapp"])
        
    def _calculate_total_story_points(self, analysis: Dict[str, Any]) -> int:
        """Calculate estimated story points based on complexity"""
        base_points = {
            "simple": 20,
            "medium": 50, 
            "complex": 100
        }
        
        points = base_points.get(analysis["complexity"], 50)
        
        # Add points for additional tech stacks
        points += len(analysis["tech_stack"]) * 5
        
        # Add points for features
        points += len(analysis["features"]) * 3
        
        return points
        
    def _estimate_dev_time(self, complexity: str) -> str:
        estimates = {
            "simple": "2-4 weeks",
            "medium": "6-10 weeks",
            "complex": "12-20 weeks"
        }
        return estimates.get(complexity, "6-10 weeks")
        
    def _get_default_roadmap_template(self) -> str:
        """Return default roadmap template if file not found"""
        return f"""# DevAlex AI-Optimized Development Roadmap

Project: <PROJECT_NAME>

Phase 1 - Requirements Ingestion  
- Load <PRD_PATH> and <TECH_STACK_PATH>
- Summarize product vision, key user stories, constraints, and high-level architecture choices.

Phase 2 - Development Planning
Total story points: [TO_BE_CALCULATED]
Context window capacity: <MAX_CONTEXT_TOKENS>
Batching decision: [TO_BE_DETERMINED]

Phase 3 - Iterative Build
For each development batch:
1. Load batch requirements and current codebase
2. Design or update database schema
3. Implement backend services and API endpoints
4. Build or adjust frontend components  
5. Refine UX details and run batch-level tests
6. Merge with main branch and update internal context

Phase 4 - Final Integration
- Run batches into one cohesive codebase
- Perform end-to-end verification against all PRD requirements
- Optimize performance and resolve residual issues
- Update documentation and deployment instructions
- Declare the application deployment ready

Generated by DevAlex Planr on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    def _customize_roadmap_with_analysis(self, roadmap_content: str, analysis: Dict[str, Any]) -> str:
        """Customize roadmap with actual project analysis"""
        total_points = self._calculate_total_story_points(analysis)
        
        roadmap_content = roadmap_content.replace("[TO_BE_CALCULATED]", str(total_points))
        roadmap_content = roadmap_content.replace("[TO_BE_DETERMINED]", 
            "HOLISTIC" if total_points < 100 else "BATCHED")
            
        return roadmap_content
        
    def _format_tech_stack(self, tech_stack: List[str]) -> str:
        if not tech_stack:
            return "- To be determined based on requirements"
        return "\n".join([f"- {tech.replace('_', ' ').title()}" for tech in tech_stack])
        
    def _format_detailed_tech_stack(self, analysis: Dict[str, Any]) -> str:
        tech_details = {
            "node_js": "**Frontend/Backend**: Node.js with Express/Fastify",
            "python": "**Backend**: Python with FastAPI/Django",
            "rust": "**Systems**: Rust for high-performance components", 
            "golang": "**Backend**: Go for scalable microservices",
            "java": "**Enterprise**: Java with Spring Boot",
            "ruby": "**Web**: Ruby on Rails",
            "php": "**Web**: PHP with Laravel/Symfony"
        }
        
        if not analysis["tech_stack"]:
            return "- Technology stack to be determined based on specific requirements"
            
        return "\n".join([tech_details.get(tech, f"- {tech}") for tech in analysis["tech_stack"]])
        
    def _recommend_architecture(self, analysis: Dict[str, Any]) -> str:
        if analysis["complexity"] == "simple":
            return "Monolithic architecture with clean separation of concerns"
        elif analysis["complexity"] == "medium":
            return "Modular monolith with potential for microservices evolution"  
        else:
            return "Microservices architecture with domain-driven design"
            
    def _recommend_database(self, analysis: Dict[str, Any]) -> str:
        return """**Primary Database**: PostgreSQL for ACID compliance and complex queries
**Caching**: Redis for session management and frequent data
**Search**: Elasticsearch for full-text search (if needed)
**Analytics**: Consider time-series DB for metrics and monitoring"""

    def _recommend_deployment(self, analysis: Dict[str, Any]) -> str:
        return """**Containerization**: Docker with multi-stage builds
**Orchestration**: Kubernetes or Docker Swarm
**Cloud Platform**: AWS/Azure/GCP with auto-scaling
**CI/CD**: GitHub Actions with automated testing
**Monitoring**: Prometheus + Grafana for observability"""
        
    def _generate_technical_requirements(self, analysis: Dict[str, Any]) -> str:
        return f"""### System Architecture
- **Pattern**: {self._recommend_architecture(analysis)}
- **Database**: Relational with caching layer
- **API Design**: RESTful with OpenAPI specification
- **Authentication**: OAuth 2.1 with JWT tokens

### Development Standards
- **Code Quality**: Automated linting and formatting
- **Testing**: Minimum 80% code coverage
- **Documentation**: Comprehensive API and code documentation
- **Version Control**: Git with feature branch workflow"""

    def _generate_success_criteria(self, project_type: str) -> str:
        return """### Technical Success Metrics
- **Performance**: 99.9% uptime, <200ms API response time
- **Quality**: >90% test coverage, zero critical security issues
- **Usability**: User satisfaction score >4.5/5
- **Maintenance**: <2 hour deployment time, automated rollbacks

### Business Success Metrics  
- **User Adoption**: Target user engagement metrics
- **Performance**: System reliability and scalability metrics
- **Quality**: Bug report reduction and resolution time"""

    def _generate_story_points(self, analysis: Dict[str, Any]) -> str:
        total_points = self._calculate_total_story_points(analysis)
        return f"""**Total Estimated Story Points**: {total_points}
**Breakdown by Phase**:
- Requirements & Architecture: {int(total_points * 0.15)} points
- Core Development: {int(total_points * 0.60)} points  
- Testing & QA: {int(total_points * 0.15)} points
- Deployment & Documentation: {int(total_points * 0.10)} points

*1 story point = 1 day human effort = 1 second AI agent effort*"""

    def _get_user_scale(self, complexity: str) -> str:
        scales = {
            "simple": "100-500",
            "medium": "1,000-10,000", 
            "complex": "10,000+"
        }
        return scales.get(complexity, "1,000-10,000")