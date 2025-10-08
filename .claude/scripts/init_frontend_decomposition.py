#!/usr/bin/env python3
"""
Frontend Decomposition Initialization Script
Initializes frontend task decomposition for AI Mind Map PM
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class FrontendDecompositionInitializer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.state_file = os.path.join(self.base_dir, '.claude_tasks', 'state.json')
        self.registry_file = os.path.join(self.base_dir, '.claude_tasks', 'task_registry.json')

    def load_state(self) -> Dict[str, Any]:
        """Load current state from state.json"""
        with open(self.state_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_registry(self) -> Dict[str, Any]:
        """Load current task registry"""
        with open(self.registry_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_state(self, state: Dict[str, Any]):
        """Save state to state.json"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def save_registry(self, registry: Dict[str, Any]):
        """Save task registry to task_registry.json"""
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

    def initialize_frontend_decomposition(self):
        """Initialize frontend decomposition with 8 root modules"""
        state = self.load_state()
        registry = self.load_registry()

        # Update state to show frontend decomposition in progress
        state['decomposition_phase']['frontend_status'] = 'in_progress'
        state['decomposition_phase']['current_module'] = 'authentication'
        state['metadata']['updated_at'] = datetime.now().isoformat()

        # Define the 8 frontend modules
        modules = [
            {
                "id": "1",
                "title": "Authentication Module",
                "type": "module",
                "status": "pending",
                "description": "User authentication, registration, email verification, and password management",
                "estimated_pages": 3,
                "key_components": ["AuthForm", "SocialLogin", "EmailVerification", "PasswordReset"],
                "wireframes": ["authentication-page.md", "email-verification-page.md"],
                "user_flows": ["User Registration & Authentication Flow"]
            },
            {
                "id": "2",
                "title": "Core Navigation & Layout Module",
                "type": "module",
                "status": "pending",
                "description": "Global toolbar, breadcrumb navigation, hierarchical navigation, responsive layout",
                "estimated_pages": 1,
                "key_components": ["GlobalToolbar", "BreadcrumbNav", "ThemeToggle", "ResponsiveLayout"],
                "wireframes": [],
                "user_flows": ["Hierarchical Navigation Flow", "Error Recovery & Undo Flow"]
            },
            {
                "id": "3",
                "title": "Mind Map Canvas Module",
                "type": "module",
                "status": "pending",
                "description": "Interactive canvas with pan, zoom, node rendering, and grid system",
                "estimated_pages": 1,
                "key_components": ["MindMapCanvas", "CanvasControls", "NodeRenderer", "GridBackground"],
                "wireframes": [],
                "user_flows": ["All navigation flows"]
            },
            {
                "id": "4",
                "title": "Project Management Module",
                "type": "module",
                "status": "pending",
                "description": "Project list mind map, project nodes, details panel, CRUD operations",
                "estimated_pages": 2,
                "key_components": ["ProjectListMindMap", "ProjectNode", "ProjectDetailsPanel", "FloatingActionButton"],
                "wireframes": ["project-list-mind-map.md", "project-details-panel.md"],
                "user_flows": ["Project List Management Flow", "Hierarchical Navigation Flow"]
            },
            {
                "id": "5",
                "title": "AI Creation Module",
                "type": "module",
                "status": "pending",
                "description": "AI-guided project creation with chat interface and real-time generation",
                "estimated_pages": 1,
                "key_components": ["AICreationView", "ChatInterface", "ConversationManager", "ProjectDetailsGenerator"],
                "wireframes": ["ai-creation-view.md"],
                "user_flows": ["AI-Guided Project Creation Flow"]
            },
            {
                "id": "6",
                "title": "Task Management Module",
                "type": "module",
                "status": "pending",
                "description": "Project detail mind map, task nodes, CRUD operations, status management",
                "estimated_pages": 3,
                "key_components": ["ProjectDetailMindMap", "TaskNode", "TaskDetailsPanel", "TaskCreationForm"],
                "wireframes": ["project-detail-mind-map.md", "task-details-panel.md", "task-creation-form.md"],
                "user_flows": ["Task Management Flow", "Hierarchical Navigation Flow"]
            },
            {
                "id": "7",
                "title": "Task Detail Module",
                "type": "module",
                "status": "pending",
                "description": "Task detail mind map, detail node management, context panels",
                "estimated_pages": 2,
                "key_components": ["TaskDetailMindMap", "DetailNode", "TaskContextPanel", "DetailEditor"],
                "wireframes": ["task-detail-mind-map.md", "task-context-panel.md"],
                "user_flows": ["Task Detail Management Flow", "Hierarchical Navigation Flow"]
            },
            {
                "id": "8",
                "title": "Dependency Management Module",
                "type": "module",
                "status": "pending",
                "description": "Task dependency creation, visualization, management, and status impact",
                "estimated_pages": 2,
                "key_components": ["DependencyManager", "ConnectionMode", "DependencyPanel", "StatusImpactCalculator"],
                "wireframes": ["dependency-management-panel.md", "context-menu.md"],
                "user_flows": ["Dependency Management Flow", "Task Status Management Flow"]
            }
        ]

        # Add modules to registry
        registry['frontend_tasks'] = modules
        registry['frontend_metadata']['total_modules'] = len(modules)
        registry['frontend_metadata']['last_updated'] = datetime.now().isoformat()

        # Save files
        self.save_state(state)
        self.save_registry(registry)

        return {
            "modules_created": len(modules),
            "total_estimated_pages": sum(m['estimated_pages'] for m in modules),
            "modules": modules
        }

    def print_summary(self, result: Dict[str, Any]):
        """Print initialization summary"""
        print("\n" + "="*80)
        print("🎯 FRONTEND DECOMPOSITION INITIALIZATION COMPLETE")
        print("="*80)

        print(f"\n📊 SUMMARY:")
        print(f"   • Modules created: {result['modules_created']}")
        print(f"   • Estimated total pages: {result['total_estimated_pages']}")

        print(f"\n🏗️  FRONTEND MODULES (Level 1):")
        for module in result['modules']:
            print(f"   [{module['id']}] {module['title']}")
            print(f"       • Status: {module['status']}")
            print(f"       • Estimated pages: {module['estimated_pages']}")
            print(f"       • Key components: {', '.join(module['key_components'][:3])}...")
            print()

        print(f"🔧 TECH STACK:")
        print(f"   • Framework: Next.js with TypeScript")
        print(f"   • UI Library: shadcn/ui")
        print(f"   • CSS: Tailwind CSS")
        print(f"   • State Management: Zustand")

        print(f"\n📍 CURRENT STATUS:")
        print(f"   • decomposition_phase.frontend_status: in_progress")
        print(f"   • Current module: authentication")

        print(f"\n🚀 NEXT COMMAND:")
        print(f"   /continue-decompose-frontend")
        print(f"   (This will decompose modules → pages → components)")

        print("\n" + "="*80)

def main():
    """Main execution function"""
    initializer = FrontendDecompositionInitializer()
    result = initializer.initialize_frontend_decomposition()
    initializer.print_summary(result)

if __name__ == "__main__":
    main()