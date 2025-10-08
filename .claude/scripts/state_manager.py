"""
State Manager - Manage .claude_tasks/state.json operations
Provides atomic operations for updating project state.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class StateManager:
    """Manager for state.json operations."""

    def __init__(self, workspace_root: str = "."):
        """Initialize StateManager.

        Args:
            workspace_root: Root directory of the workspace (default: current directory)
        """
        self.workspace_root = Path(workspace_root)
        self.state_file = self.workspace_root / ".claude_tasks" / "state.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure .claude_tasks directory exists."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> Dict:
        """Load current state from file."""
        if not self.state_file.exists():
            return self._get_default_state()

        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_state(self, state: Dict):
        """Save state to file."""
        state["metadata"]["last_updated"] = datetime.utcnow().isoformat() + "Z"

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _get_default_state(self) -> Dict:
        """Get default state structure."""
        now = datetime.utcnow().isoformat() + "Z"
        return {
            "design_phase": {
                "status": "not_started",
                "user_flows_file": None,
                "wireframes_generated": False,
                "wireframes_count": 0,
                "validation_status": "not_started",
            },
            "decomposition_phase": {
                "status": "not_started",
                "frontend_status": "not_started",
                "backend_status": "not_started",
                "last_checkpoint": None,
                "progress": {
                    "frontend": {
                        "total_modules": 0,
                        "total_pages": 0,
                        "total_components": 0,
                    },
                    "backend": {
                        "total_modules": 0,
                        "total_services": 0,
                        "total_functions": 0,
                    },
                },
            },
            "dependency_phase": {
                "status": "not_started",
                "total_waves": 0,
                "frontend_internal_dependencies": False,
                "backend_internal_dependencies": False,
                "cross_stack_dependencies": False,
                "execution_order_generated": False,
            },
            "development_phase": {
                "status": "not_started",
                "current_wave": 0,
                "completed_waves": 0,
                "total_waves": 0,
                "completed_tasks": [],
                "failed_tasks": [],
                "workers": 5,
                "wave_progress": {},
            },
            "metadata": {"created_at": now, "last_updated": now, "version": "1.0"},
        }

    # Design Phase Operations

    def init_design_phase(self, user_flows_file: str = "designs/user-flows.md"):
        """Initialize design phase after user flows are generated."""
        state = self._load_state()
        state["design_phase"].update(
            {
                "status": "user_flows_completed",
                "user_flows_file": user_flows_file,
                "wireframes_generated": False,
                "wireframes_count": 0,
            }
        )
        self._save_state(state)
        return state

    def complete_wireframes(
        self,
        wireframes_count: int,
        validation_status: str = "passed",
        validation_report: str = "designs/WIREFRAME_VALIDATION.md",
    ):
        """Mark wireframes as completed."""
        state = self._load_state()
        state["design_phase"].update(
            {
                "status": "completed",
                "wireframes_generated": True,
                "wireframes_count": wireframes_count,
                "wireframes_directory": "designs/wireframes/",
                "validation_status": validation_status,
                "validation_report": validation_report,
            }
        )
        self._save_state(state)
        return state

    # Decomposition Phase Operations

    def start_frontend_decomposition(self, total_modules: int):
        """Start frontend decomposition phase."""
        state = self._load_state()
        state["decomposition_phase"].update(
            {"status": "in_progress", "frontend_status": "in_progress"}
        )
        state["decomposition_phase"]["progress"]["frontend"][
            "total_modules"
        ] = total_modules
        self._save_state(state)
        return state

    def update_frontend_progress(
        self,
        total_pages: int = None,
        total_components: int = None,
        last_processed_module: str = None,
    ):
        """Update frontend decomposition progress."""
        state = self._load_state()
        frontend_progress = state["decomposition_phase"]["progress"]["frontend"]

        if total_pages is not None:
            frontend_progress["total_pages"] = total_pages
        if total_components is not None:
            frontend_progress["total_components"] = total_components
        if last_processed_module is not None:
            frontend_progress["last_processed_module"] = last_processed_module

        self._save_state(state)
        return state

    def complete_frontend_decomposition(self):
        """Mark frontend decomposition as completed."""
        state = self._load_state()
        state["decomposition_phase"]["frontend_status"] = "completed"

        # Check if backend also completed
        if state["decomposition_phase"]["backend_status"] == "completed":
            state["decomposition_phase"]["status"] = "completed"

        self._save_state(state)
        return state

    def start_backend_decomposition(self, total_modules: int):
        """Start backend decomposition phase."""
        state = self._load_state()
        state["decomposition_phase"].update(
            {"status": "in_progress", "backend_status": "in_progress"}
        )
        state["decomposition_phase"]["progress"]["backend"][
            "total_modules"
        ] = total_modules
        self._save_state(state)
        return state

    def update_backend_progress(
        self,
        total_services: int = None,
        total_functions: int = None,
        last_processed_module: str = None,
    ):
        """Update backend decomposition progress."""
        state = self._load_state()
        backend_progress = state["decomposition_phase"]["progress"]["backend"]

        if total_services is not None:
            backend_progress["total_services"] = total_services
        if total_functions is not None:
            backend_progress["total_functions"] = total_functions
        if last_processed_module is not None:
            backend_progress["last_processed_module"] = last_processed_module

        self._save_state(state)
        return state

    def complete_backend_decomposition(self):
        """Mark backend decomposition as completed."""
        state = self._load_state()
        state["decomposition_phase"]["backend_status"] = "completed"

        # Check if frontend also completed
        if state["decomposition_phase"]["frontend_status"] == "completed":
            state["decomposition_phase"]["status"] = "completed"

        self._save_state(state)
        return state

    # Dependency Phase Operations

    def complete_dependency_analysis(self, total_waves: int):
        """Mark dependency analysis as completed."""
        state = self._load_state()
        state["dependency_phase"].update(
            {
                "status": "completed",
                "total_waves": total_waves,
                "frontend_internal_dependencies": True,
                "backend_internal_dependencies": True,
                "cross_stack_dependencies": True,
                "execution_order_generated": True,
            }
        )
        self._save_state(state)
        return state

    # Development Phase Operations

    def start_development(self, total_waves: int, workers: int = 5):
        """Start development phase."""
        state = self._load_state()
        state["development_phase"].update(
            {
                "status": "in_progress",
                "current_wave": 1,
                "completed_waves": 0,
                "total_waves": total_waves,
                "workers": workers,
                "completed_tasks": [],
                "failed_tasks": [],
            }
        )
        self._save_state(state)
        return state

    def start_wave(
        self,
        wave_number: int,
        category: str,
        total_tasks: int,
        total_batches: int = None,
    ):
        """Start a new wave."""
        state = self._load_state()

        wave_key = str(wave_number)
        state["development_phase"]["wave_progress"][wave_key] = {
            "status": "in_progress",
            "category": category,
            "tasks": total_tasks,
            "completed": 0,
            "failed": 0,
            "started_at": datetime.utcnow().isoformat() + "Z",
        }

        if total_batches is not None:
            state["development_phase"]["wave_progress"][wave_key].update(
                {"current_batch": 1, "total_batches": total_batches}
            )

        state["development_phase"]["current_wave"] = wave_number
        self._save_state(state)
        return state

    def complete_task(self, task_id: str):
        """Mark a task as completed."""
        state = self._load_state()

        # Add to completed_tasks if not already there
        if task_id not in state["development_phase"]["completed_tasks"]:
            state["development_phase"]["completed_tasks"].append(task_id)

        # Remove from failed_tasks if it was there
        if task_id in state["development_phase"]["failed_tasks"]:
            state["development_phase"]["failed_tasks"].remove(task_id)

        self._save_state(state)
        return state

    def fail_task(self, task_id: str):
        """Mark a task as failed."""
        state = self._load_state()

        # Add to failed_tasks if not already there
        if task_id not in state["development_phase"]["failed_tasks"]:
            state["development_phase"]["failed_tasks"].append(task_id)

        # Remove from completed_tasks if it was there
        if task_id in state["development_phase"]["completed_tasks"]:
            state["development_phase"]["completed_tasks"].remove(task_id)

        self._save_state(state)
        return state

    def complete_batch(
        self, wave_number: int, completed_count: int, failed_count: int = 0
    ):
        """Update progress after batch completion."""
        state = self._load_state()

        wave_key = str(wave_number)
        wave_progress = state["development_phase"]["wave_progress"][wave_key]

        wave_progress["completed"] += completed_count
        wave_progress["failed"] += failed_count

        if "current_batch" in wave_progress:
            wave_progress["current_batch"] += 1

        self._save_state(state)
        return state

    def complete_wave(self, wave_number: int):
        """Mark a wave as completed."""
        state = self._load_state()

        wave_key = str(wave_number)
        wave_progress = state["development_phase"]["wave_progress"][wave_key]

        wave_progress["status"] = "completed"
        wave_progress["completed_at"] = datetime.utcnow().isoformat() + "Z"

        # Calculate duration
        if "started_at" in wave_progress:
            start = datetime.fromisoformat(
                wave_progress["started_at"].replace("Z", "+00:00")
            )
            end = datetime.fromisoformat(
                wave_progress["completed_at"].replace("Z", "+00:00")
            )
            duration_minutes = (end - start).total_seconds() / 60
            wave_progress["duration_minutes"] = round(duration_minutes, 1)

        state["development_phase"]["completed_waves"] = wave_number

        # Move to next wave or complete development
        if wave_number < state["development_phase"]["total_waves"]:
            state["development_phase"]["current_wave"] = wave_number + 1
        else:
            state["development_phase"]["status"] = "completed"

        self._save_state(state)
        return state

    # Query Operations

    def get_state(self) -> Dict:
        """Get current state."""
        return self._load_state()

    def get_phase_status(self, phase: str) -> str:
        """Get status of a specific phase.

        Args:
            phase: 'design', 'decomposition', 'dependency', or 'development'
        """
        state = self._load_state()
        return state[f"{phase}_phase"]["status"]

    def get_current_wave(self) -> int:
        """Get current wave number."""
        state = self._load_state()
        return state["development_phase"]["current_wave"]

    def get_completed_tasks(self) -> List[str]:
        """Get list of completed task IDs."""
        state = self._load_state()
        return state["development_phase"]["completed_tasks"]

    def get_failed_tasks(self) -> List[str]:
        """Get list of failed task IDs."""
        state = self._load_state()
        return state["development_phase"]["failed_tasks"]

    def is_resumable(self) -> bool:
        """Check if development can be resumed."""
        state = self._load_state()
        return (
            state["development_phase"]["status"] == "in_progress"
            and state["development_phase"]["current_wave"] > 0
        )


def main():
    """CLI interface for state management."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Manage state.json")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--workspace", default=".", help="Workspace root directory")
    parser.add_argument("--args", nargs="*", help="Command arguments")

    args = parser.parse_args()

    manager = StateManager(args.workspace)

    # Execute command
    if hasattr(manager, args.command):
        method = getattr(manager, args.command)
        if args.args:
            result = method(*args.args)
        else:
            result = method()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
