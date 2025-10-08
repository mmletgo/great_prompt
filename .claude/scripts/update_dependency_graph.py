"""
Update task registry with dependency graph from analyzer output.

This script:
1. Reads dependency analysis JSON file
2. Adds all dependencies to task registry
3. Sets execution order (waves)
4. Validates dependency graph
5. Updates state to mark dependency phase complete

Usage:
    python update_dependency_graph.py --input dependency_graph.json
"""

import sys
import json
import argparse
from pathlib import Path
from task_registry_manager import TaskRegistryManager
from state_manager import StateManager


def validate_dependency_graph(dep_graph: dict, task_mgr: TaskRegistryManager):
    """
    Validate the dependency graph for correctness.

    Args:
        dep_graph: Dependency graph dictionary
        task_mgr: TaskRegistryManager instance

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    # Check required fields
    if "execution_order" not in dep_graph:
        errors.append("Missing 'execution_order' field in dependency graph")
        return False, errors

    # Validate waves
    execution_order = dep_graph["execution_order"]
    wave_numbers = set()
    all_wave_tasks = set()

    for wave in execution_order:
        if "wave" not in wave:
            errors.append(f"Wave missing 'wave' number: {wave}")
            continue

        wave_num = wave["wave"]
        wave_numbers.add(wave_num)

        if "tasks" not in wave:
            errors.append(f"Wave {wave_num} missing 'tasks' field")
            continue

        # Check task count (should be 5-10, except last wave)
        task_count = len(wave["tasks"])
        if task_count < 5 and wave_num != max(w["wave"] for w in execution_order):
            errors.append(
                f"Wave {wave_num} has only {task_count} tasks (should be 5-10)"
            )
        elif task_count > 10:
            errors.append(f"Wave {wave_num} has {task_count} tasks (should be 5-10)")

        # Collect all tasks
        all_wave_tasks.update(wave["tasks"])

    # Check wave numbers are sequential
    expected_waves = set(range(1, len(execution_order) + 1))
    if wave_numbers != expected_waves:
        errors.append(
            f"Wave numbers not sequential: {sorted(wave_numbers)} (expected {sorted(expected_waves)})"
        )

    # Get all tasks from registry
    registry = task_mgr._load_registry()

    def collect_all_task_ids(tasks_array):
        task_ids = set()
        for task in tasks_array:
            task_ids.add(task["id"])
            if task.get("subtasks"):
                task_ids.update(collect_all_task_ids(task["subtasks"]))
        return task_ids

    frontend_ids = collect_all_task_ids(registry.get("frontend_tasks", []))
    backend_ids = collect_all_task_ids(registry.get("backend_tasks", []))
    all_registry_tasks = frontend_ids | backend_ids

    # Check all tasks are included in waves
    missing_tasks = all_registry_tasks - all_wave_tasks
    if missing_tasks:
        errors.append(
            f"Tasks in registry but not in execution order: {sorted(list(missing_tasks)[:10])}"
        )

    extra_tasks = all_wave_tasks - all_registry_tasks
    if extra_tasks:
        errors.append(
            f"Tasks in execution order but not in registry: {sorted(list(extra_tasks)[:10])}"
        )

    # Validate cross-stack dependencies
    if "cross_stack_dependencies" in dep_graph:
        for task_id, deps in dep_graph["cross_stack_dependencies"].items():
            if task_id not in all_registry_tasks:
                errors.append(f"Dependency source task not found: {task_id}")
            for dep_id in deps:
                if dep_id not in all_registry_tasks:
                    errors.append(f"Dependency target task not found: {dep_id}")

    return len(errors) == 0, errors


def update_dependency_graph(input_file: str):
    """
    Update task registry with dependency graph from analyzer output.

    Args:
        input_file: Path to dependency graph JSON file
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Load dependency graph
    print(f"Loading dependency graph from {input_file}...")
    with open(input_path, "r", encoding="utf-8") as f:
        dep_graph = json.load(f)

    task_mgr = TaskRegistryManager()
    state_mgr = StateManager()

    # Validate dependency graph
    print("\nValidating dependency graph...")
    is_valid, errors = validate_dependency_graph(dep_graph, task_mgr)

    if not is_valid:
        print("\n❌ Dependency graph validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("✓ Dependency graph validation passed")

    # Add dependencies
    print("\nAdding dependencies to task registry...")
    dep_count = 0

    if "cross_stack_dependencies" in dep_graph:
        for task_id, deps in dep_graph["cross_stack_dependencies"].items():
            for dep_id in deps:
                try:
                    task_mgr.add_dependency(task_id, dep_id)
                    dep_count += 1
                except Exception as e:
                    print(
                        f"Warning: Failed to add dependency {task_id} -> {dep_id}: {e}"
                    )

    print(f"✓ Added {dep_count} dependencies")

    # Set execution order
    print("\nSetting execution order (waves)...")
    execution_order = dep_graph["execution_order"]

    try:
        task_mgr.set_execution_order(execution_order)
        print(f"✓ Set execution order with {len(execution_order)} waves")
    except Exception as e:
        print(f"Error: Failed to set execution order: {e}", file=sys.stderr)
        sys.exit(1)

    # Print wave summary
    print("\n=== Execution Plan Summary ===")
    for wave in execution_order:
        wave_num = wave["wave"]
        task_count = len(wave["tasks"])
        level = wave.get("level", "mixed")
        category = wave.get("category", "mixed")
        description = wave.get("description", "No description")

        print(f"Wave {wave_num}: {task_count} tasks (Level {level} - {category})")
        print(f"  {description}")

    # Mark dependency phase complete
    total_waves = len(execution_order)
    print(f"\nMarking dependency phase complete (total waves: {total_waves})...")

    try:
        state_mgr.complete_dependency_analysis(total_waves=total_waves)
        print("✓ Updated state.json: dependency_phase = completed")
    except Exception as e:
        print(f"Error: Failed to update state: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n✅ Dependency graph successfully updated!")
    print(f"   - task_registry.json: dependencies and execution order added")
    print(f"   - state.json: dependency_phase marked complete")
    print(f"\nNext command: /parallel-dev-fullstack")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update task registry with dependency graph"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to dependency graph JSON file (output from analyzer)",
    )

    args = parser.parse_args()

    update_dependency_graph(args.input)
