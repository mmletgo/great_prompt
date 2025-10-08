"""
Task Registry Manager - Manage .claude_tasks/task_registry.json operations
Provides atomic operations for task management with tree structure support.

Tree Structure:
- Tasks organized as nested tree (frontend_tasks and backend_tasks arrays)
- Task IDs use dot notation: "1", "1.1", "1.1.2"
- Subtasks nested in parent's "subtasks" array
- Each task has "parent_id" field (except root tasks)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


class TaskRegistryManager:
    """Manager for task_registry.json operations with tree structure support."""

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
        """Get default registry structure (tree-based)."""
        return {
            "frontend_tasks": [],
            "backend_tasks": [],
            "frontend_metadata": {
                "framework": None,
                "language": None,
                "total_modules": 0,
                "total_pages": 0,
                "total_components": 0,
            },
            "backend_metadata": {
                "framework": None,
                "language": None,
                "database": None,
                "total_modules": 0,
                "total_services": 0,
                "total_functions": 0,
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

    # Tree Navigation Operations

    def _find_task_in_tree(self, tasks: List[Dict], task_id: str) -> Optional[Dict]:
        """Find task by ID in tree structure using depth-first search.

        Args:
            tasks: Array of tasks (or subtasks)
            task_id: Task ID to search for (dot notation like "1.2.3")

        Returns:
            Task dict if found, None otherwise
        """
        for task in tasks:
            if task["id"] == task_id:
                return task

            # Recursively search subtasks
            if task.get("subtasks"):
                found = self._find_task_in_tree(task["subtasks"], task_id)
                if found:
                    return found

        return None

    def find_task(self, task_id: str) -> Optional[Dict]:
        """Find task by ID across frontend and backend trees.

        Args:
            task_id: Task ID in dot notation (e.g., "1.2.3")

        Returns:
            Task dict if found, None otherwise
        """
        registry = self._load_registry()

        # Search frontend tree
        task = self._find_task_in_tree(registry["frontend_tasks"], task_id)
        if task:
            return task

        # Search backend tree
        task = self._find_task_in_tree(registry["backend_tasks"], task_id)
        return task

    def _get_all_tasks_recursive(
        self,
        tasks: List[Dict],
        level: Optional[int] = None,
        category: Optional[str] = None,
    ) -> List[Dict]:
        """Get all tasks from tree recursively.

        Args:
            tasks: Array of tasks to traverse
            level: Filter by level (1, 2, 3) if provided
            category: Filter by category if provided

        Returns:
            Flat list of all matching tasks
        """
        results = []

        for task in tasks:
            # Check filters
            if level is not None and task.get("level") != level:
                pass  # Skip this task but continue to subtasks
            elif category is not None and task.get("category") != category:
                pass
            else:
                results.append(task)

            # Recursively get subtasks
            if task.get("subtasks"):
                results.extend(
                    self._get_all_tasks_recursive(task["subtasks"], level, category)
                )

        return results

    def get_all_tasks(
        self, level: Optional[int] = None, category: Optional[str] = None
    ) -> List[Dict]:
        """Get all tasks from both trees.

        Args:
            level: Filter by level (1=module, 2=page/service, 3=component/function)
            category: Filter by category ('frontend' or 'backend')

        Returns:
            Flat list of all matching tasks
        """
        registry = self._load_registry()
        tasks = []

        if category is None or category == "frontend":
            tasks.extend(
                self._get_all_tasks_recursive(
                    registry["frontend_tasks"], level, "frontend"
                )
            )

        if category is None or category == "backend":
            tasks.extend(
                self._get_all_tasks_recursive(
                    registry["backend_tasks"], level, "backend"
                )
            )

        return tasks

    def _get_task_path_recursive(
        self, tasks: List[Dict], task_id: str, path: List[Dict]
    ) -> Optional[List[Dict]]:
        """Get path from root to task (breadcrumb trail).

        Args:
            tasks: Array of tasks to search
            task_id: Target task ID
            path: Current path (used in recursion)

        Returns:
            List of task dicts from root to target, or None if not found
        """
        for task in tasks:
            current_path = path + [task]

            if task["id"] == task_id:
                return current_path

            if task.get("subtasks"):
                result = self._get_task_path_recursive(
                    task["subtasks"], task_id, current_path
                )
                if result:
                    return result

        return None

    def get_task_path(self, task_id: str) -> Optional[List[Dict]]:
        """Get full path from root to task (breadcrumb).

        Args:
            task_id: Target task ID

        Returns:
            List of ancestor tasks [root, parent, ..., target] or None
        """
        registry = self._load_registry()

        # Search frontend tree
        path = self._get_task_path_recursive(registry["frontend_tasks"], task_id, [])
        if path:
            return path

        # Search backend tree
        path = self._get_task_path_recursive(registry["backend_tasks"], task_id, [])
        return path

    def _assign_task_id(self, parent_id: Optional[str], sibling_count: int) -> str:
        """Assign ID to new task based on parent and sibling count.

        Args:
            parent_id: ID of parent task (None for Level 1 root)
            sibling_count: Number of existing siblings

        Returns:
            New task ID in dot notation
        """
        if parent_id is None:
            # Level 1: Root module
            return str(sibling_count + 1)
        else:
            # Level 2-3: Append to parent ID
            return f"{parent_id}.{sibling_count + 1}"

    # Task Operations (Tree-based)

    def add_root_task(self, category: str, task_data: Dict) -> str:
        """Add a new root task (Level 1 module).

        Args:
            category: 'frontend' or 'backend'
            task_data: Task data dict (should include title, type, etc.)

        Returns:
            Assigned task ID
        """
        registry = self._load_registry()

        # Get appropriate tasks array
        tasks_array = (
            registry["frontend_tasks"]
            if category == "frontend"
            else registry["backend_tasks"]
        )

        # Assign ID
        task_id = self._assign_task_id(None, len(tasks_array))

        # Build task object
        task = {
            "id": task_id,
            "level": 1,
            "category": category,
            "status": "pending",
            "dependencies": [],
            "subtasks": [],
            **task_data,
        }

        # Add to array
        tasks_array.append(task)

        self._save_registry(registry)
        return task_id

    def add_subtask(self, parent_id: str, task_data: Dict) -> str:
        """Add a new subtask to a parent task.

        Args:
            parent_id: ID of parent task (e.g., "1" or "1.2")
            task_data: Task data dict (should include title, type, etc.)

        Returns:
            Assigned task ID

        Raises:
            ValueError: If parent task not found
        """
        registry = self._load_registry()

        # Find parent task
        parent = self._find_task_in_tree(registry["frontend_tasks"], parent_id)
        if not parent:
            parent = self._find_task_in_tree(registry["backend_tasks"], parent_id)

        if not parent:
            raise ValueError(f"Parent task {parent_id} not found")

        # Assign ID based on parent and sibling count
        task_id = self._assign_task_id(parent_id, len(parent["subtasks"]))

        # Build task object
        task = {
            "id": task_id,
            "parent_id": parent_id,
            "level": parent["level"] + 1,
            "category": parent["category"],
            "status": "pending",
            "dependencies": [],
            "subtasks": [],
            **task_data,
        }

        # Add to parent's subtasks
        parent["subtasks"].append(task)

        # Update parent status if it was pending
        if parent["status"] == "pending":
            parent["status"] = "decomposed"

        self._save_registry(registry)
        return task_id

    def add_subtasks_batch(self, parent_id: str, subtasks: List[Dict]) -> List[str]:
        """Add multiple subtasks to a parent at once.

        Args:
            parent_id: ID of parent task
            subtasks: List of task data dicts

        Returns:
            List of assigned task IDs
        """
        task_ids = []
        for task_data in subtasks:
            task_id = self.add_subtask(parent_id, task_data)
            task_ids.append(task_id)
        return task_ids

    def update_task(self, task_id: str, updates: Dict) -> Dict:
        """Update task fields in-place in the tree.

        Args:
            task_id: Task ID in dot notation
            updates: Dictionary of fields to update

        Returns:
            Updated registry

        Raises:
            ValueError: If task not found
        """
        registry = self._load_registry()

        # Find task in tree
        task = self._find_task_in_tree(registry["frontend_tasks"], task_id)
        if not task:
            task = self._find_task_in_tree(registry["backend_tasks"], task_id)

        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Update fields
        task.update(updates)

        # Auto-update timestamps
        if updates.get("status") == "completed" and "completed_at" not in updates:
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"

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
            task_id: Task identifier (dot notation)
            status: New status ('completed', 'failed', 'in_progress', etc.)
            completed_at: ISO 8601 timestamp
            duration_minutes: Execution duration
            test_coverage: Test coverage percentage
            implementation_file: Path to implementation file
            test_file: Path to test file
            error: Error message if failed

        Returns:
            Updated registry
        """
        updates = {"status": status}

        if completed_at:
            updates["completed_at"] = completed_at
        if duration_minutes is not None:
            updates["duration_minutes"] = duration_minutes
        if test_coverage is not None:
            updates["test_coverage"] = test_coverage
        if implementation_file:
            updates["implementation_file"] = implementation_file
        if test_file:
            updates["test_file"] = test_file
        if error:
            updates["error"] = error
        elif status == "completed":
            updates["error"] = None

        return self.update_task(task_id, updates)

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task data by ID.

        Args:
            task_id: Task ID in dot notation

        Returns:
            Task dict if found, None otherwise
        """
        return self.find_task(task_id)

    def get_tasks_by_status(
        self, status: str, category: Optional[str] = None
    ) -> List[Dict]:
        """Get all tasks with specific status.

        Args:
            status: Status to filter by
            category: Optional category filter ('frontend' or 'backend')

        Returns:
            List of tasks matching status
        """
        all_tasks = self.get_all_tasks(category=category)
        return [task for task in all_tasks if task.get("status") == status]

    def get_tasks_by_level(
        self, level: int, category: Optional[str] = None
    ) -> List[Dict]:
        """Get all tasks at specific level.

        Args:
            level: Level to filter by (1=module, 2=page/service, 3=component/function)
            category: Optional category filter

        Returns:
            List of tasks at specified level
        """
        return self.get_all_tasks(level=level, category=category)

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

    def add_dependency(self, task_id: str, depends_on_task_id: str) -> Dict:
        """Add a dependency relationship.

        Args:
            task_id: Task that depends on another (dot notation)
            depends_on_task_id: Task being depended upon (dot notation)

        Returns:
            Updated registry

        Raises:
            ValueError: If either task not found
        """
        registry = self._load_registry()

        # Find both tasks
        task = self.find_task(task_id)
        depends_on = self.find_task(depends_on_task_id)

        if not task:
            raise ValueError(f"Task {task_id} not found")
        if not depends_on:
            raise ValueError(f"Task {depends_on_task_id} not found")

        # Add dependency if not already present
        if depends_on_task_id not in task.get("dependencies", []):
            if "dependencies" not in task:
                task["dependencies"] = []
            task["dependencies"].append(depends_on_task_id)

        self._save_registry(registry)
        return registry

    def remove_dependency(self, task_id: str, depends_on_task_id: str) -> Dict:
        """Remove a dependency relationship.

        Args:
            task_id: Task that depends on another
            depends_on_task_id: Task to remove from dependencies

        Returns:
            Updated registry
        """
        registry = self._load_registry()

        task = self.find_task(task_id)
        if task and depends_on_task_id in task.get("dependencies", []):
            task["dependencies"].remove(depends_on_task_id)

        self._save_registry(registry)
        return registry

    def get_task_dependencies(self, task_id: str) -> List[Dict]:
        """Get all tasks that a task depends on.

        Args:
            task_id: Task ID to get dependencies for

        Returns:
            List of task dicts that this task depends on
        """
        task = self.find_task(task_id)
        if not task:
            return []

        dependencies = []
        for dep_id in task.get("dependencies", []):
            dep_task = self.find_task(dep_id)
            if dep_task:
                dependencies.append(dep_task)

        return dependencies

    def get_dependents(self, task_id: str) -> List[Dict]:
        """Get all tasks that depend on this task.

        Args:
            task_id: Task ID to get dependents for

        Returns:
            List of task dicts that depend on this task
        """
        all_tasks = self.get_all_tasks()
        dependents = []

        for task in all_tasks:
            if task_id in task.get("dependencies", []):
                dependents.append(task)

        return dependents

    def get_blocked_tasks(self) -> List[Dict]:
        """Get all tasks that are blocked by incomplete dependencies.

        Returns:
            List of tasks with incomplete dependencies
        """
        all_tasks = self.get_all_tasks()
        blocked = []

        for task in all_tasks:
            if task.get("status") in ["completed", "in_progress"]:
                continue

            dependencies = self.get_task_dependencies(task["id"])
            if dependencies:
                incomplete_deps = [
                    dep for dep in dependencies if dep.get("status") != "completed"
                ]
                if incomplete_deps:
                    blocked.append(task)

        return blocked

    def get_ready_tasks(self) -> List[Dict]:
        """Get all tasks that are ready to work on (no blocking dependencies).

        Returns:
            List of tasks with status 'ready' and all dependencies completed
        """
        all_tasks = self.get_all_tasks()
        ready = []

        for task in all_tasks:
            if task.get("status") != "ready":
                continue

            dependencies = self.get_task_dependencies(task["id"])
            if not dependencies:
                ready.append(task)
            else:
                all_deps_complete = all(
                    dep.get("status") == "completed" for dep in dependencies
                )
                if all_deps_complete:
                    ready.append(task)

        return ready

    def get_integration_ready_tasks(
        self, level: int, category: Optional[str] = None
    ) -> List[Dict]:
        """Get tasks at specified level that are ready for integration.

        A task is ready for integration when ALL its child subtasks are completed.

        Args:
            level: Level to check (1 or 2)
            category: Optional category filter ('frontend' or 'backend')

        Returns:
            List of tasks ready for integration (all children completed)
        """
        if level not in [1, 2]:
            raise ValueError("Integration only applies to Level 1 and 2 tasks")

        tasks_at_level = self.get_tasks_by_level(level, category)
        ready_for_integration = []

        for task in tasks_at_level:
            # Skip if already completed or in progress
            if task.get("status") in ["completed", "in_progress"]:
                continue

            # Check if all subtasks are completed
            subtasks = task.get("subtasks", [])
            if not subtasks:
                # No subtasks means not decomposed yet
                continue

            all_children_complete = self._all_children_completed(task)

            if all_children_complete:
                ready_for_integration.append(task)

        return ready_for_integration

    def _all_children_completed(self, task: Dict) -> bool:
        """Recursively check if all descendants are completed.

        Args:
            task: Task to check

        Returns:
            True if all descendants completed, False otherwise
        """
        subtasks = task.get("subtasks", [])

        if not subtasks:
            # Leaf node - check its own status
            return task.get("status") == "completed"

        # Check all children recursively
        for child in subtasks:
            if not self._all_children_completed(child):
                return False

        return True

    def set_execution_order(self, waves: List[Dict]):
        """Set the execution order (waves) - LEGACY METHOD.

        NOTE: With tree structure, execution order is now determined by tree levels
        and dependencies. This method is kept for backward compatibility.

        Args:
            waves: List of wave dictionaries with 'wave', 'category', 'tasks' keys
        """
        registry = self._load_registry()

        # Store in metadata for reference
        if "execution_order" not in registry:
            registry["execution_order"] = []

        registry["execution_order"] = waves
        self._save_registry(registry)
        return registry

    def get_wave_tasks(self, wave_number: int) -> List[str]:
        """Get task IDs for a specific wave - LEGACY METHOD.

        NOTE: With tree structure, use get_tasks_by_level() instead.
        """
        registry = self._load_registry()

        for wave in registry.get("execution_order", []):
            if wave["wave"] == wave_number:
                return wave["tasks"]

        return []

    def get_total_waves(self) -> int:
        """Get total number of waves - LEGACY METHOD.

        NOTE: With tree structure, max level represents depth.
        """
        registry = self._load_registry()
        return len(registry.get("execution_order", []))

    # Query Operations

    def get_registry(self) -> Dict:
        """Get full registry."""
        return self._load_registry()

    def get_statistics(self) -> Dict:
        """Get statistics about tasks using tree structure."""
        registry = self._load_registry()

        all_tasks = self.get_all_tasks()

        total_tasks = len(all_tasks)
        by_status = {}
        by_category = {}
        by_level = {}

        for task in all_tasks:
            status = task.get("status", "unknown")
            category = task.get("category", "unknown")
            level = task.get("level", 0)

            by_status[status] = by_status.get(status, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1
            by_level[level] = by_level.get(level, 0) + 1

        return {
            "total_tasks": total_tasks,
            "by_status": by_status,
            "by_category": by_category,
            "by_level": by_level,
            "frontend_metadata": registry.get("frontend_metadata", {}),
            "backend_metadata": registry.get("backend_metadata", {}),
            "frontend_root_tasks": len(registry.get("frontend_tasks", [])),
            "backend_root_tasks": len(registry.get("backend_tasks", [])),
        }


def main():
    """CLI interface for task registry management."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Manage task_registry.json (Tree Structure)"
    )
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--workspace", default=".", help="Workspace root directory")
    parser.add_argument("--task-id", help="Task ID (dot notation, e.g., '1.2.3')")
    parser.add_argument("--parent-id", help="Parent task ID for subtask operations")
    parser.add_argument("--category", help="Task category (frontend/backend)")
    parser.add_argument("--status", help="Task status")
    parser.add_argument(
        "--level",
        type=int,
        help="Task level (1=module, 2=page/service, 3=component/function)",
    )
    parser.add_argument("--json", help="JSON data for task operations")
    parser.add_argument("--args", nargs="*", help="Additional arguments")

    args = parser.parse_args()

    manager = TaskRegistryManager(args.workspace)

    try:
        # Execute command
        if args.command == "get_statistics":
            result = manager.get_statistics()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "get_all_tasks":
            result = manager.get_all_tasks(level=args.level, category=args.category)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "find_task" and args.task_id:
            result = manager.find_task(args.task_id)
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Task {args.task_id} not found", file=sys.stderr)
                sys.exit(1)

        elif args.command == "get_task_path" and args.task_id:
            result = manager.get_task_path(args.task_id)
            if result:
                # Print breadcrumb
                path_str = " > ".join([t.get("title", t["id"]) for t in result])
                print(f"Path: {path_str}")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Task {args.task_id} not found", file=sys.stderr)
                sys.exit(1)

        elif args.command == "add_root_task" and args.category and args.json:
            task_data = json.loads(args.json)
            task_id = manager.add_root_task(args.category, task_data)
            print(f"Created root task: {task_id}")

        elif args.command == "add_subtask" and args.parent_id and args.json:
            task_data = json.loads(args.json)
            task_id = manager.add_subtask(args.parent_id, task_data)
            print(f"Created subtask: {task_id}")

        elif args.command == "update_task_status" and args.task_id and args.status:
            manager.update_task_status(args.task_id, args.status)
            print(f"Updated {args.task_id} to {args.status}")

        elif args.command == "get_tasks_by_status" and args.status:
            result = manager.get_tasks_by_status(args.status, args.category)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "get_tasks_by_level" and args.level:
            result = manager.get_tasks_by_level(args.level, args.category)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "get_ready_tasks":
            result = manager.get_ready_tasks()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "get_blocked_tasks":
            result = manager.get_blocked_tasks()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == "get_integration_ready_tasks" and args.level:
            result = manager.get_integration_ready_tasks(args.level, args.category)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif hasattr(manager, args.command):
            method = getattr(manager, args.command)
            result = method()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            print("\nAvailable commands:", file=sys.stderr)
            print("  get_statistics", file=sys.stderr)
            print(
                "  get_all_tasks [--level N] [--category frontend|backend]",
                file=sys.stderr,
            )
            print("  find_task --task-id ID", file=sys.stderr)
            print("  get_task_path --task-id ID", file=sys.stderr)
            print(
                "  add_root_task --category frontend|backend --json '{...}'",
                file=sys.stderr,
            )
            print("  add_subtask --parent-id ID --json '{...}'", file=sys.stderr)
            print("  update_task_status --task-id ID --status STATUS", file=sys.stderr)
            print(
                "  get_tasks_by_status --status STATUS [--category ...]",
                file=sys.stderr,
            )
            print("  get_tasks_by_level --level N [--category ...]", file=sys.stderr)
            print("  get_ready_tasks", file=sys.stderr)
            print("  get_blocked_tasks", file=sys.stderr)
            print(
                "  get_integration_ready_tasks --level N [--category ...]",
                file=sys.stderr,
            )
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
