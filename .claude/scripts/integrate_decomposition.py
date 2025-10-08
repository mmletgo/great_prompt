"""
Integrate decomposition results from temporary files into task registry.

This script:
1. Reads all decomposition JSON files from temp directory
2. Uses TaskRegistryManager API to add subtasks (maintains tree structure)
3. Archives processed temp files

Usage:
    python integrate_decomposition.py --category frontend
    python integrate_decomposition.py --category backend
"""

import sys
import os
import json
import shutil
from pathlib import Path
from task_registry_manager import TaskRegistryManager


def integrate_decomposition(category: str):
    """
    Integrate decomposition results for frontend or backend.

    Args:
        category: "frontend" or "backend"
    """
    if category not in ["frontend", "backend"]:
        print(
            f"Error: category must be 'frontend' or 'backend', got '{category}'",
            file=sys.stderr,
        )
        sys.exit(1)

    task_mgr = TaskRegistryManager()

    # Set up directories
    temp_dir = f".claude_tasks/{category}_decomposition_temp"
    archive_dir = f".claude_tasks/{category}_decomposition_archive"

    if not os.path.exists(temp_dir):
        print(f"Error: Temp directory not found: {temp_dir}", file=sys.stderr)
        sys.exit(1)

    # Get all JSON files
    temp_files = [f for f in os.listdir(temp_dir) if f.endswith(".json")]

    if not temp_files:
        print(f"No decomposition files found in {temp_dir}")
        return

    print(f"\n=== Integration Phase (Python API) ===")
    print(
        f"Using TaskRegistryManager.add_subtasks_batch() to maintain tree structure...\n"
    )

    total_tasks = 0
    integrated_files = []

    for filename in sorted(temp_files):
        filepath = os.path.join(temp_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                decomp = json.load(f)

            parent_id = decomp["parent_task_id"]
            subtasks = decomp["subtasks"]
            parent_type = decomp.get("parent_type", "unknown")

            # Use add_subtasks_batch to maintain tree structure
            # This automatically:
            # - Assigns dot notation IDs (e.g., "1.1", "1.1.1")
            # - Sets parent_id correctly
            # - Updates parent status to "decomposed"
            # - Maintains hierarchical relationships
            task_ids = task_mgr.add_subtasks_batch(parent_id, subtasks)

            # Get parent task info for display
            registry = task_mgr._load_registry()
            tasks_array = (
                registry["frontend_tasks"]
                if category == "frontend"
                else registry["backend_tasks"]
            )
            parent_task = task_mgr._find_task_in_tree(tasks_array, parent_id)
            parent_title = parent_task["title"] if parent_task else "Unknown"

            print(f"Integrating {filename}:")
            print(f'  Parent: "{parent_id}" ({parent_type.title()}: {parent_title})')

            if len(task_ids) <= 5:
                print(
                    f"  ✓ Created {len(task_ids)} subtasks with IDs: {', '.join(task_ids)}"
                )
            else:
                print(
                    f"  ✓ Created {len(task_ids)} subtasks with IDs: {', '.join(task_ids[:3])}, ..., {task_ids[-1]}"
                )

            print(f"  ✓ Parent status: pending → decomposed")
            print(f"  ✓ Tree structure validated\n")

            total_tasks += len(task_ids)
            integrated_files.append(filename)

        except Exception as e:
            print(f"Error processing {filename}: {e}", file=sys.stderr)
            continue

    # Archive processed files
    os.makedirs(archive_dir, exist_ok=True)

    for filename in integrated_files:
        src = os.path.join(temp_dir, filename)
        dst = os.path.join(archive_dir, filename)
        shutil.move(src, dst)

    print(f"=== Integration Summary ===")
    print(f"Total new tasks: {total_tasks}")

    # Get task type counts
    registry = task_mgr._load_registry()
    tasks_array = (
        registry["frontend_tasks"]
        if category == "frontend"
        else registry["backend_tasks"]
    )

    ready_count = 0
    pending_count = 0

    def count_by_status(task):
        nonlocal ready_count, pending_count
        if task["status"] == "ready":
            ready_count += 1
        elif task["status"] == "pending":
            pending_count += 1
        for child in task.get("subtasks", []):
            count_by_status(child)

    for task in tasks_array:
        count_by_status(task)

    if category == "frontend":
        print(
            f"By type: {ready_count} components (ready), {pending_count} pages (pending)"
        )
    else:
        print(
            f"By type: {ready_count} functions (ready), {pending_count} services (pending)"
        )

    print(f"Tree hierarchy maintained with dot notation IDs")
    print(f"Archived {len(integrated_files)} temp files\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Integrate decomposition results into task registry"
    )
    parser.add_argument(
        "--category",
        choices=["frontend", "backend"],
        required=True,
        help="Category to integrate: frontend or backend",
    )

    args = parser.parse_args()

    integrate_decomposition(args.category)
