#!/usr/bin/env python3

"""
DevAlex DevOps and Deployment Automation
Comprehensive deployment, containerization, and DevOps tools
"""

import json
import shutil
import subprocess
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

class DevOpsAutomation:
    """Comprehensive DevOps and deployment automation"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.platforms = {
            "docker": self._setup_docker,
            "vercel": self._setup_vercel,
            "railway": self._setup_railway,
            "render": self._setup_render,
            "aws": self._setup_aws,
            "gcp": self._setup_gcp,
            "azure": self._setup_azure,
            "netlify": self._setup_netlify
        }
        
    def setup_containerization(self, app_type: str, language: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up Docker containerization for the project"""
        print(f"🐳 Setting up Docker containerization for {app_type} ({language})...")
        
        result = {
            "containerization_type": "docker",
            "app_type": app_type,
            "language": language,
            "files_created": [],
            "next_steps": []
        }
        
        # Generate Dockerfile
        dockerfile_content = self._generate_dockerfile(app_type, language, config)
        dockerfile_path = self.project_path / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)
        result["files_created"].append("Dockerfile")
        
        # Generate .dockerignore
        dockerignore_content = self._generate_dockerignore(language)
        dockerignore_path = self.project_path / ".dockerignore"
        dockerignore_path.write_text(dockerignore_content)
        result["files_created"].append(".dockerignore")
        
        # Generate docker-compose.yml for development
        if config.get("include_compose", True):
            compose_content = self._generate_docker_compose(app_type, language, config)
            compose_path = self.project_path / "docker-compose.yml"
            compose_path.write_text(compose_content)
            result["files_created"].append("docker-compose.yml")
            
        # Generate development docker-compose override
        if config.get("include_dev_compose", True):
            dev_compose_content = self._generate_dev_docker_compose(app_type, config)
            dev_compose_path = self.project_path / "docker-compose.dev.yml"
            dev_compose_path.write_text(dev_compose_content)
            result["files_created"].append("docker-compose.dev.yml")
            
        # Add Docker scripts
        self._create_docker_scripts(app_type)
        result["files_created"].extend(["scripts/docker-build.sh", "scripts/docker-run.sh"])
        
        result["next_steps"] = [
            "docker build -t myapp .",
            "docker run -p 8000:8000 myapp",
            "docker-compose up -d  # For full stack"
        ]
        
        return result
        
    def setup_deployment_platform(self, platform: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up deployment for specific platform"""
        print(f"🚀 Setting up deployment for {platform}...")
        
        if platform not in self.platforms:
            raise ValueError(f"Unsupported platform: {platform}")
            
        return self.platforms[platform](config)
        
    def setup_cicd_pipeline(self, platform: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up CI/CD pipeline"""
        print(f"⚙️ Setting up CI/CD pipeline for {platform}...")
        
        if platform == "github":
            return self._setup_github_actions(config)
        elif platform == "gitlab":
            return self._setup_gitlab_ci(config)
        elif platform == "azure":
            return self._setup_azure_pipelines(config)
        else:
            raise ValueError(f"Unsupported CI/CD platform: {platform}")
            
    def generate_infrastructure_as_code(self, provider: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Infrastructure as Code templates"""
        print(f"🏗️ Generating {provider} infrastructure templates...")
        
        if provider == "terraform":
            return self._generate_terraform(config)
        elif provider == "aws-cdk":
            return self._generate_aws_cdk(config)
        elif provider == "pulumi":
            return self._generate_pulumi(config)
        else:
            raise ValueError(f"Unsupported IaC provider: {provider}")
            
    def _generate_dockerfile(self, app_type: str, language: str, config: Dict[str, Any]) -> str:
        """Generate optimized Dockerfile based on app type and language"""
        
        if language == "python":
            return self._generate_python_dockerfile(app_type, config)
        elif language in ["javascript", "typescript"]:
            return self._generate_node_dockerfile(app_type, config)
        elif language == "rust":
            return self._generate_rust_dockerfile(app_type, config)
        elif language == "go":
            return self._generate_go_dockerfile(app_type, config)
        else:
            return self._generate_generic_dockerfile(language, config)
            
    def _generate_python_dockerfile(self, app_type: str, config: Dict[str, Any]) -> str:
        """Generate optimized Python Dockerfile"""
        
        python_version = config.get('python_version', '3.11')
        
        if app_type == "fastapi":
            return f'''# Multi-stage build for FastAPI application
FROM python:{python_version}-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PIP_NO_CACHE_DIR=1 \\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:{python_version}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python{python_version}/site-packages /usr/local/lib/python{python_version}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]'''

        elif app_type == "django":
            return f'''FROM python:{python_version}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]'''

        else:
            return f'''FROM python:{python_version}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]'''
            
    def _generate_node_dockerfile(self, app_type: str, config: Dict[str, Any]) -> str:
        """Generate optimized Node.js Dockerfile"""
        
        node_version = config.get('node_version', '18')
        
        if app_type in ["react", "nextjs", "vue"]:
            return f'''# Multi-stage build for Node.js frontend
FROM node:{node_version}-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock* ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:{node_version}-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

USER nextjs

EXPOSE 3000

CMD ["npm", "start"]'''

        else:  # Express/API
            return f'''FROM node:{node_version}-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app
USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD node healthcheck.js

CMD ["node", "server.js"]'''
            
    def _generate_dockerignore(self, language: str) -> str:
        """Generate .dockerignore file"""
        
        common_ignores = '''# Git
.git
.gitignore

# Documentation
README.md
CHANGELOG.md
LICENSE

# CI/CD
.github
.gitlab-ci.yml
.travis.yml

# IDE
.vscode
.idea
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/'''

        if language == "python":
            return common_ignores + '''

# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
.env
venv/
.venv/
dist/
build/
*.egg-info/'''

        elif language in ["javascript", "typescript"]:
            return common_ignores + '''

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity
coverage/
.env
.env.local
.env.production
build/
dist/'''

        else:
            return common_ignores
            
    def _generate_docker_compose(self, app_type: str, language: str, config: Dict[str, Any]) -> str:
        """Generate docker-compose.yml for full application stack"""
        
        compose_config = {
            "version": "3.8",
            "services": {},
            "volumes": {},
            "networks": {
                "app-network": {
                    "driver": "bridge"
                }
            }
        }
        
        # Add main application service
        if app_type in ["fullstack", "backend", "api"]:
            compose_config["services"]["app"] = {
                "build": ".",
                "ports": ["8000:8000"],
                "environment": [
                    "DATABASE_URL=postgresql://postgres:password@db:5432/appdb",
                    "REDIS_URL=redis://redis:6379"
                ],
                "depends_on": ["db", "redis"],
                "networks": ["app-network"]
            }
            
        # Add database service
        database = config.get("database", "postgresql")
        if database == "postgresql":
            compose_config["services"]["db"] = {
                "image": "postgres:14-alpine",
                "environment": [
                    "POSTGRES_DB=appdb",
                    "POSTGRES_USER=postgres",
                    "POSTGRES_PASSWORD=password"
                ],
                "ports": ["5432:5432"],
                "volumes": ["postgres_data:/var/lib/postgresql/data"],
                "networks": ["app-network"]
            }
            compose_config["volumes"]["postgres_data"] = {}
            
        elif database == "mysql":
            compose_config["services"]["db"] = {
                "image": "mysql:8",
                "environment": [
                    "MYSQL_DATABASE=appdb",
                    "MYSQL_ROOT_PASSWORD=password"
                ],
                "ports": ["3306:3306"],
                "volumes": ["mysql_data:/var/lib/mysql"],
                "networks": ["app-network"]
            }
            compose_config["volumes"]["mysql_data"] = {}
            
        # Add Redis for caching
        if config.get("include_redis", True):
            compose_config["services"]["redis"] = {
                "image": "redis:7-alpine",
                "ports": ["6379:6379"],
                "networks": ["app-network"]
            }
            
        # Add frontend service for fullstack apps
        if app_type == "fullstack" and config.get("frontend"):
            compose_config["services"]["frontend"] = {
                "build": "./frontend",
                "ports": ["3000:3000"],
                "environment": [
                    "REACT_APP_API_URL=http://localhost:8000"
                ],
                "depends_on": ["app"],
                "networks": ["app-network"]
            }
            
        return yaml.dump(compose_config, default_flow_style=False)
        
    def _create_docker_scripts(self, app_type: str):
        """Create Docker utility scripts"""
        scripts_dir = self.project_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # Build script
        build_script = '''#!/bin/bash
set -e

echo "🐳 Building Docker image..."

# Build the main application
docker build -t myapp:latest .

echo "✅ Docker build complete!"
echo "Run with: docker run -p 8000:8000 myapp:latest"
'''
        
        (scripts_dir / "docker-build.sh").write_text(build_script)
        
        # Run script
        run_script = '''#!/bin/bash
set -e

echo "🚀 Starting application with Docker..."

# Stop any existing containers
docker-compose down

# Start the full stack
docker-compose up -d

echo "✅ Application started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Stop with: docker-compose down"
'''
        
        (scripts_dir / "docker-run.sh").write_text(run_script)
        
        # Make scripts executable
        import stat
        for script in ["docker-build.sh", "docker-run.sh"]:
            script_path = scripts_dir / script
            script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
            
    def _setup_github_actions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up GitHub Actions CI/CD pipeline"""
        
        workflows_dir = self.project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # CI/CD workflow
        workflow_config = {
            "name": "CI/CD Pipeline",
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main"]}
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {"name": "Set up Node.js", "uses": "actions/setup-node@v3", "with": {"node-version": "18"}},
                        {"name": "Install dependencies", "run": "npm install"},
                        {"name": "Run tests", "run": "npm test"},
                        {"name": "Run linting", "run": "npm run lint"}
                    ]
                },
                "build": {
                    "needs": "test",
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {"name": "Build application", "run": "npm run build"}
                    ]
                },
                "deploy": {
                    "needs": ["test", "build"],
                    "runs-on": "ubuntu-latest",
                    "if": "github.ref == 'refs/heads/main'",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {"name": "Deploy to production", "run": "echo 'Add deployment steps here'"}
                    ]
                }
            }
        }
        
        workflow_path = workflows_dir / "ci-cd.yml"
        workflow_path.write_text(yaml.dump(workflow_config, default_flow_style=False))
        
        return {
            "platform": "github-actions",
            "files_created": [".github/workflows/ci-cd.yml"],
            "features": ["automated_testing", "build_validation", "deployment"],
            "next_steps": [
                "Push to GitHub to trigger first workflow",
                "Configure deployment secrets in GitHub",
                "Customize deployment steps for your platform"
            ]
        }
        
    # Placeholder methods for additional platform setups
    def _setup_docker(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self.setup_containerization(
            config.get('app_type', 'webapp'),
            config.get('language', 'python'),
            config
        )
        
    def _setup_vercel(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Setup Vercel deployment"""
        vercel_config = {
            "version": 2,
            "builds": [
                {"src": "*.js", "use": "@vercel/node"}
            ],
            "routes": [
                {"src": "/(.*)", "dest": "/"}
            ]
        }
        
        (self.project_path / "vercel.json").write_text(json.dumps(vercel_config, indent=2))
        
        return {
            "platform": "vercel",
            "files_created": ["vercel.json"],
            "deployment_url": "https://vercel.com",
            "next_steps": ["Install Vercel CLI", "Run 'vercel --prod'"]
        }
        
    def _setup_railway(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "railway", "status": "placeholder"}
        
    def _setup_render(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "render", "status": "placeholder"}
        
    def _setup_aws(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "aws", "status": "placeholder"}
        
    def _setup_gcp(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "gcp", "status": "placeholder"}
        
    def _setup_azure(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "azure", "status": "placeholder"}
        
    def _setup_netlify(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "netlify", "status": "placeholder"}
        
    def _setup_gitlab_ci(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "gitlab-ci", "status": "placeholder"}
        
    def _setup_azure_pipelines(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"platform": "azure-pipelines", "status": "placeholder"}
        
    def _generate_terraform(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"iac": "terraform", "status": "placeholder"}
        
    def _generate_aws_cdk(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"iac": "aws-cdk", "status": "placeholder"}
        
    def _generate_pulumi(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {"iac": "pulumi", "status": "placeholder"}
        
    def _generate_dev_docker_compose(self, app_type: str, config: Dict[str, Any]) -> str:
        """Generate development docker-compose override"""
        return '''version: '3.8'

services:
  app:
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
    
  db:
    ports:
      - "5432:5432"
    
  redis:
    ports:
      - "6379:6379"
'''
    
    def get_supported_platforms(self) -> Dict[str, Dict[str, Any]]:
        """Get list of supported deployment platforms"""
        return {
            "docker": {
                "name": "Docker Containerization",
                "description": "Containerize your application with Docker",
                "ready": True
            },
            "vercel": {
                "name": "Vercel",
                "description": "Deploy frontend applications to Vercel",
                "ready": True
            },
            "github": {
                "name": "GitHub Actions",
                "description": "Set up CI/CD with GitHub Actions",
                "ready": True
            },
            "railway": {
                "name": "Railway",
                "description": "Deploy full-stack applications to Railway",
                "ready": False
            },
            "aws": {
                "name": "Amazon Web Services",
                "description": "Deploy to AWS with infrastructure automation",
                "ready": False
            }
        }