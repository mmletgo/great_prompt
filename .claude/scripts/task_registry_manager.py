"""
Task Registry Manager - Manage .claude_tasks/task_registry.json operations
Provides atomic operations for task management.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class TaskRegistryManager:
    """Manager for task_registry.json operations."""

    def __init__(self, workspace_root: str = "."):
        """Initialize TaskRegistryManager.

        Args:
            workspace_root: Root directory of the workspace (default: current directory)
        """
        self.workspace_root = Path(workspace_root)
        self.registry_file = (
            self.workspace_root / ".claude_tasks" / "task_registry.json"
        )
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure .claude_tasks directory exists."""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_registry(self) -> Dict:
        """Load current registry from file."""
        if not self.registry_file.exists():
            return self._get_default_registry()

        with open(self.registry_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_registry(self, registry: Dict):
        """Save registry to file."""
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

    def _get_default_registry(self) -> Dict:
        """Get default registry structure."""
        return {
            "tasks": {},
            "frontend_metadata": {
                "framework": None,
                "language": None,
                "total_modules": 0,
                "total_pages": 0,
                "total_components": 0,
                "modules": [],
            },
            "backend_metadata": {
                "framework": None,
                "language": None,
                "database": None,
                "total_modules": 0,
                "total_services": 0,
                "total_functions": 0,
                "modules": [],
                "layers": {
                    "api": 0,
                    "service": 0,
                    "repository": 0,
                    "validation": 0,
                    "utility": 0,
                },
            },
            "dependency_graph": {
                "frontend_dependencies": {},
                "backend_dependencies": {},
                "cross_stack_dependencies": {},
                "execution_order": [],
            },
        }

    # Task Operations

    def add_task(self, task_id: str, task_data: Dict) -> Dict:
        """Add or update a task.

        Args:
            task_id: Unique task identifier
            task_data: Task data dictionary
        """
        registry = self._load_registry()

        # Ensure required fields
        task_data.setdefault("id", task_id)
        task_data.setdefault("status", "pending")
        task_data.setdefault("children", [])
        task_data.setdefault("dependencies", [])

        registry["tasks"][task_id] = task_data
        self._save_registry(registry)
        return registry

    def add_tasks_batch(self, tasks: Dict[str, Dict]) -> Dict:
        """Add multiple tasks at once.

        Args:
            tasks: Dictionary of {task_id: task_data}
        """
        registry = self._load_registry()

        for task_id, task_data in tasks.items():
            task_data.setdefault("id", task_id)
            task_data.setdefault("status", "pending")
            task_data.setdefault("children", [])
            task_data.setdefault("dependencies", [])
            registry["tasks"][task_id] = task_data

        self._save_registry(registry)
        return registry

    def update_task_status(
        self,
        task_id: str,
        status: str,
        completed_at: str = None,
        duration_minutes: float = None,
        test_coverage: int = None,
        implementation_file: str = None,
        test_file: str = None,
        error: str = None,
    ) -> Dict:
        """Update task status and related fields.

        Args:
            task_id: Task identifier
            status: New status ('completed', 'failed', 'in_progress', etc.)
            completed_at: ISO 8601 timestamp
            duration_minutes: Execution duration
            test_coverage: Test coverage percentage
            implementation_file: Path to implementation file
            test_file: Path to test file
            error: Error message if failed
        """
        registry = self._load_registry()

        if task_id not in registry["tasks"]:
            raise KeyError(f"Task {task_id} not found")

        task = registry["tasks"][task_id]
        task["status"] = status

        if completed_at:
            task["completed_at"] = completed_at
        elif status == "completed":
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"

        if duration_minutes is not None:
            task["duration_minutes"] = duration_minutes
        if test_coverage is not None:
            task["test_coverage"] = test_coverage
        if implementation_file:
            task["implementation_file"] = implementation_file
        if test_file:
            task["test_file"] = test_file
        if error:
            task["error"] = error
        elif status == "completed":
            task["error"] = None

        self._save_registry(registry)
        return registry

    def update_tasks_batch(self, updates: List[Dict]) -> Dict:
        """Update multiple tasks at once.

        Args:
            updates: List of dicts with 'task_id' and update fields
        """
        registry = self._load_registry()

        for update in updates:
            task_id = update.pop("task_id")
            if task_id in registry["tasks"]:
                registry["tasks"][task_id].update(update)

        self._save_registry(registry)
        return registry

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task data."""
        registry = self._load_registry()
        return registry["tasks"].get(task_id)

    def get_tasks_by_status(self, status: str) -> Dict[str, Dict]:
        """Get all tasks with specific status."""
        registry = self._load_registry()
        return {
            task_id: task
            for task_id, task in registry["tasks"].items()
            if task.get("status") == status
        }

    def get_tasks_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all tasks of specific category (frontend/backend)."""
        registry = self._load_registry()
        return {
            task_id: task
            for task_id, task in registry["tasks"].items()
            if task.get("category") == category
        }

    # Metadata Operations

    def init_frontend_metadata(self, framework: str, language: str = "TypeScript"):
        """Initialize frontend metadata."""
        registry = self._load_registry()
        registry["frontend_metadata"].update(
            {"framework": framework, "language": language}
        )
        self._save_registry(registry)
        return registry

    def init_backend_metadata(
        self, framework: str, database: str, language: str = "Python"
    ):
        """Initialize backend metadata."""
        registry = self._load_registry()
        registry["backend_metadata"].update(
            {"framework": framework, "database": database, "language": language}
        )
        self._save_registry(registry)
        return registry

    def update_frontend_counts(
        self,
        total_modules: int = None,
        total_pages: int = None,
        total_components: int = None,
    ):
        """Update frontend metadata counts."""
        registry = self._load_registry()
        metadata = registry["frontend_metadata"]

        if total_modules is not None:
            metadata["total_modules"] = total_modules
        if total_pages is not None:
            metadata["total_pages"] = total_pages
        if total_components is not None:
            metadata["total_components"] = total_components

        self._save_registry(registry)
        return registry

    def update_backend_counts(
        self,
        total_modules: int = None,
        total_services: int = None,
        total_functions: int = None,
        layer_counts: Dict[str, int] = None,
    ):
        """Update backend metadata counts."""
        registry = self._load_registry()
        metadata = registry["backend_metadata"]

        if total_modules is not None:
            metadata["total_modules"] = total_modules
        if total_services is not None:
            metadata["total_services"] = total_services
        if total_functions is not None:
            metadata["total_functions"] = total_functions
        if layer_counts:
            metadata["layers"].update(layer_counts)

        self._save_registry(registry)
        return registry

    # Dependency Operations

    def add_dependency(
        self, task_id: str, depends_on: str, dependency_type: str = "auto"
    ):
        """Add a dependency relationship.

        Args:
            task_id: Task that depends on another
            depends_on: Task ID that is depended upon
            dependency_type: 'frontend', 'backend', or 'cross_stack' (auto-detect if 'auto')
        """
        registry = self._load_registry()

        # Add to task's dependencies list
        if task_id in registry["tasks"]:
            if depends_on not in registry["tasks"][task_id]["dependencies"]:
                registry["tasks"][task_id]["dependencies"].append(depends_on)

        # Add to dependency graph
        if dependency_type == "auto":
            task_category = registry["tasks"][task_id]["category"]
            depends_category = registry["tasks"][depends_on]["category"]

            if task_category == "frontend" and depends_category == "backend":
                dependency_type = "cross_stack"
            elif task_category == "frontend":
                dependency_type = "frontend"
            else:
                dependency_type = "backend"

        graph_key = f"{dependency_type}_dependencies"
        if task_id not in registry["dependency_graph"][graph_key]:
            registry["dependency_graph"][graph_key][task_id] = []

        if depends_on not in registry["dependency_graph"][graph_key][task_id]:
            registry["dependency_graph"][graph_key][task_id].append(depends_on)

        self._save_registry(registry)
        return registry

    def set_execution_order(self, waves: List[Dict]):
        """Set the execution order (waves).

        Args:
            waves: List of wave dictionaries with 'wave', 'category', 'tasks' keys
        """
        registry = self._load_registry()
        registry["dependency_graph"]["execution_order"] = waves
        self._save_registry(registry)
        return registry

    def get_wave_tasks(self, wave_number: int) -> List[str]:
        """Get task IDs for a specific wave."""
        registry = self._load_registry()

        for wave in registry["dependency_graph"]["execution_order"]:
            if wave["wave"] == wave_number:
                return wave["tasks"]

        return []

    def get_total_waves(self) -> int:
        """Get total number of waves."""
        registry = self._load_registry()
        return len(registry["dependency_graph"]["execution_order"])

    # Query Operations

    def get_registry(self) -> Dict:
        """Get full registry."""
        return self._load_registry()

    def get_statistics(self) -> Dict:
        """Get statistics about tasks."""
        registry = self._load_registry()

        total_tasks = len(registry["tasks"])
        by_status = {}
        by_category = {}

        for task in registry["tasks"].values():
            status = task.get("status", "unknown")
            category = task.get("category", "unknown")

            by_status[status] = by_status.get(status, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1

        return {
            "total_tasks": total_tasks,
            "by_status": by_status,
            "by_category": by_category,
            "frontend_metadata": registry["frontend_metadata"],
            "backend_metadata": registry["backend_metadata"],
            "total_waves": len(registry["dependency_graph"]["execution_order"]),
        }


def main():
    """CLI interface for task registry management."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Manage task_registry.json")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--workspace", default=".", help="Workspace root directory")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--status", help="Task status")
    parser.add_argument("--args", nargs="*", help="Additional arguments")

    args = parser.parse_args()

    manager = TaskRegistryManager(args.workspace)

    # Execute command
    if args.command == "get_statistics":
        result = manager.get_statistics()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.command == "update_task_status" and args.task_id and args.status:
        result = manager.update_task_status(args.task_id, args.status)
        print(f"Updated {args.task_id} to {args.status}")
    elif hasattr(manager, args.command):
        method = getattr(manager, args.command)
        result = method()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
