"""
Utility functions for task and state management.
Provides convenience wrappers for common operations.
"""

from state_manager import StateManager
from task_registry_manager import TaskRegistryManager
from typing import List, Dict, Optional
import json


class ProjectManager:
    """Combined manager for both state and task registry."""

    def __init__(self, workspace_root: str = "."):
        """Initialize managers.

        Args:
            workspace_root: Root directory of the workspace
        """
        self.state = StateManager(workspace_root)
        self.tasks = TaskRegistryManager(workspace_root)
        self.workspace_root = workspace_root

    def complete_task_full(
        self,
        task_id: str,
        implementation_file: str = None,
        test_file: str = None,
        test_coverage: int = None,
        duration_minutes: float = None,
    ):
        """Complete a task with full updates to both state and registry.

        This is the recommended method for marking tasks as completed.
        Updates both task_registry.json and state.json atomically.

        Args:
            task_id: Task identifier
            implementation_file: Path to implementation file
            test_file: Path to test file
            test_coverage: Test coverage percentage
            duration_minutes: Task execution duration
        """
        # Update task registry
        self.tasks.update_task_status(
            task_id=task_id,
            status="completed",
            implementation_file=implementation_file,
            test_file=test_file,
            test_coverage=test_coverage,
            duration_minutes=duration_minutes,
        )

        # Update state
        self.state.complete_task(task_id)

        return {
            "task_id": task_id,
            "status": "completed",
            "updated": ["task_registry.json", "state.json"],
        }

    def fail_task_full(self, task_id: str, error: str):
        """Mark a task as failed with full updates to both state and registry.

        Args:
            task_id: Task identifier
            error: Error message or description
        """
        # Update task registry
        self.tasks.update_task_status(task_id=task_id, status="failed", error=error)

        # Update state
        self.state.fail_task(task_id)

        return {
            "task_id": task_id,
            "status": "failed",
            "error": error,
            "updated": ["task_registry.json", "state.json"],
        }

    def complete_integration_task_full(
        self,
        task_id: str,
        integration_file: str = None,
        test_file: str = None,
        test_coverage: int = None,
        duration_minutes: float = None,
    ):
        """Complete an integration task (Level 1 or 2) with full updates.

        Integration tasks assemble their completed children into cohesive units.
        Examples:
        - Level 2 Frontend: Page integration (assemble components)
        - Level 2 Backend: Service integration (assemble functions)
        - Level 1 Frontend: Module integration (assemble pages)
        - Level 1 Backend: Module integration (assemble services)

        Args:
            task_id: Task identifier (e.g., "1.1" for page, "1" for module)
            integration_file: Path to integration file (e.g., page container, service class)
            test_file: Path to integration test file
            test_coverage: Integration test coverage percentage
            duration_minutes: Task execution duration
        """
        # Verify task exists and get its level
        task = self.tasks.find_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        level = task.get("level")
        if level not in [1, 2]:
            raise ValueError(
                f"Task {task_id} is Level {level}. Integration only applies to Level 1 or 2."
            )

        # Verify all children are completed
        if not self.tasks._all_children_completed(task):
            incomplete = self._get_incomplete_children(task)
            raise ValueError(
                f"Cannot complete integration task {task_id}: "
                f"Incomplete children: {incomplete}"
            )

        # Update task registry
        self.tasks.update_task_status(
            task_id=task_id,
            status="completed",
            implementation_file=integration_file,
            test_file=test_file,
            test_coverage=test_coverage,
            duration_minutes=duration_minutes,
        )

        # Update state
        self.state.complete_task(task_id)

        return {
            "task_id": task_id,
            "level": level,
            "type": "integration",
            "status": "completed",
            "updated": ["task_registry.json", "state.json"],
        }

    def _get_incomplete_children(self, task: Dict) -> List[str]:
        """Get list of incomplete child task IDs.

        Args:
            task: Parent task

        Returns:
            List of incomplete child task IDs
        """
        incomplete = []

        for child in task.get("subtasks", []):
            if child.get("status") != "completed":
                incomplete.append(child["id"])
            # Recursively check grandchildren
            incomplete.extend(self._get_incomplete_children(child))

        return incomplete

    def get_integration_ready_tasks(
        self, level: int, category: Optional[str] = None
    ) -> List[Dict]:
        """Get tasks ready for integration at specified level.

        Args:
            level: Level to check (1 or 2)
            category: Optional category filter ('frontend' or 'backend')

        Returns:
            List of tasks ready for integration (all children completed)
        """
        return self.tasks.get_integration_ready_tasks(level, category)

    def complete_batch(
        self,
        wave_number: int,
        completed_tasks: List[str],
        failed_tasks: List[str] = None,
    ):
        """Complete a batch of tasks.

        Args:
            wave_number: Current wave number
            completed_tasks: List of completed task IDs
            failed_tasks: List of failed task IDs (optional)
        """
        failed_tasks = failed_tasks or []

        # Update state for batch
        self.state.complete_batch(
            wave_number=wave_number,
            completed_count=len(completed_tasks),
            failed_count=len(failed_tasks),
        )

        return {
            "wave": wave_number,
            "completed": len(completed_tasks),
            "failed": len(failed_tasks),
            "updated": ["state.json"],
        }

    def complete_wave_full(self, wave_number: int):
        """Complete a wave with validation.

        Validates that all tasks in the wave are completed before marking
        the wave as complete.

        Args:
            wave_number: Wave number to complete
        """
        # Get wave tasks
        wave_tasks = self.tasks.get_wave_tasks(wave_number)

        # Check completion status
        completed = self.state.get_completed_tasks()
        failed = self.state.get_failed_tasks()

        incomplete = [t for t in wave_tasks if t not in completed and t not in failed]

        if incomplete:
            return {
                "success": False,
                "error": f"Wave {wave_number} has incomplete tasks",
                "incomplete_tasks": incomplete,
            }

        # Mark wave complete
        self.state.complete_wave(wave_number)

        return {
            "success": True,
            "wave": wave_number,
            "total_tasks": len(wave_tasks),
            "completed": len([t for t in wave_tasks if t in completed]),
            "failed": len([t for t in wave_tasks if t in failed]),
            "updated": ["state.json"],
        }

    def get_next_batch_tasks(self, wave_number: int, batch_size: int = 5) -> List[Dict]:
        """Get next batch of pending tasks from current wave.

        Args:
            wave_number: Current wave number
            batch_size: Number of tasks per batch (default: 5)

        Returns:
            List of task dictionaries ready for execution
        """
        # Get all wave tasks
        wave_tasks = self.tasks.get_wave_tasks(wave_number)

        # Get already completed/failed
        completed = self.state.get_completed_tasks()
        failed = self.state.get_failed_tasks()

        # Filter to pending tasks
        pending = [
            task_id
            for task_id in wave_tasks
            if task_id not in completed and task_id not in failed
        ]

        # Get next batch
        next_batch = pending[:batch_size]

        # Fetch full task data
        tasks = [self.tasks.get_task(tid) for tid in next_batch]

        return tasks

    def check_resume_status(self) -> Dict:
        """Check if development can be resumed and get resume info.

        Returns:
            Dictionary with resume status and details
        """
        if not self.state.is_resumable():
            return {
                "can_resume": False,
                "reason": "Development not in progress or not started",
            }

        current_wave = self.state.get_current_wave()
        completed_tasks = self.state.get_completed_tasks()
        failed_tasks = self.state.get_failed_tasks()
        wave_tasks = self.tasks.get_wave_tasks(current_wave)

        pending = [
            tid
            for tid in wave_tasks
            if tid not in completed_tasks and tid not in failed_tasks
        ]

        return {
            "can_resume": True,
            "current_wave": current_wave,
            "total_waves": self.tasks.get_total_waves(),
            "completed_tasks": len(completed_tasks),
            "failed_tasks": len(failed_tasks),
            "pending_in_current_wave": len(pending),
            "pending_task_ids": pending[:10],  # First 10 for preview
        }

    def get_dashboard(self) -> Dict:
        """Get comprehensive project status dashboard.

        Returns:
            Dictionary with complete project status
        """
        state = self.state.get_state()
        stats = self.tasks.get_statistics()
        resume = self.check_resume_status()

        return {
            "phases": {
                "design": state["design_phase"]["status"],
                "decomposition": state["decomposition_phase"]["status"],
                "dependency": state["dependency_phase"]["status"],
                "development": state["development_phase"]["status"],
            },
            "development": {
                "current_wave": state["development_phase"]["current_wave"],
                "completed_waves": state["development_phase"]["completed_waves"],
                "total_waves": state["development_phase"]["total_waves"],
                "workers": state["development_phase"]["workers"],
            },
            "tasks": stats,
            "resume": resume,
        }


def print_dashboard(workspace_root: str = "."):
    """Print a formatted project status dashboard."""
    manager = ProjectManager(workspace_root)
    dashboard = manager.get_dashboard()

    print("=" * 60)
    print("PROJECT STATUS DASHBOARD")
    print("=" * 60)

    print("\n📊 PHASES:")
    for phase, status in dashboard["phases"].items():
        emoji = (
            "✅" if status == "completed" else "🔄" if status == "in_progress" else "⏳"
        )
        print(f"  {emoji} {phase.capitalize()}: {status}")

    print("\n🚀 DEVELOPMENT PROGRESS:")
    dev = dashboard["development"]
    print(f"  Wave: {dev['current_wave']}/{dev['total_waves']}")
    print(f"  Completed Waves: {dev['completed_waves']}")
    print(f"  Workers: {dev['workers']}")

    print("\n📋 TASKS:")
    tasks = dashboard["tasks"]
    print(f"  Total: {tasks['total_tasks']}")
    print(f"  By Status:")
    for status, count in tasks["by_status"].items():
        emoji = "✅" if status == "completed" else "❌" if status == "failed" else "⏳"
        print(f"    {emoji} {status}: {count}")

    print("\n🏗️  STRUCTURE:")
    print(
        f"  Frontend: {tasks['frontend_metadata']['total_components']} components, "
        f"{tasks['frontend_metadata']['total_pages']} pages"
    )
    print(
        f"  Backend: {tasks['backend_metadata']['total_functions']} functions, "
        f"{tasks['backend_metadata']['total_services']} services"
    )

    if dashboard["resume"]["can_resume"]:
        print("\n🔄 RESUME STATUS: ✅ Can Resume")
        print(f"  Current Wave: {dashboard['resume']['current_wave']}")
        print(f"  Pending Tasks: {dashboard['resume']['pending_in_current_wave']}")
    else:
        print("\n🔄 RESUME STATUS: ❌ Cannot Resume")
        print(f"  Reason: {dashboard['resume']['reason']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        workspace = sys.argv[2] if len(sys.argv) > 2 else "."
        print_dashboard(workspace)
    else:
        print("Usage: python utils.py dashboard [workspace_root]")
