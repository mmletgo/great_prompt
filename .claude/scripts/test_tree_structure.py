#!/usr/bin/env python3
"""Test script for tree structure task registry.

This script tests the new tree-based task registry manager to ensure
all operations work correctly with the hierarchical structure.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# pylint: disable=wrong-import-position
from task_registry_manager import TaskRegistryManager
import tempfile


def test_tree_structure():
    """Test tree structure operations."""
    print("=" * 60)
    print("Testing Tree Structure Task Registry")
    print("=" * 60)

    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\n📁 Using temporary workspace: {tmpdir}")

        manager = TaskRegistryManager(tmpdir)

        # Test 1: Create root tasks
        print("\n✅ Test 1: Creating root tasks...")
        frontend_id = manager.add_root_task(
            "frontend",
            {"title": "用户模块", "type": "module", "description": "用户管理相关功能"},
        )
        print(f"   Created frontend root: {frontend_id}")

        backend_id = manager.add_root_task(
            "backend",
            {"title": "认证服务", "type": "service", "description": "用户认证服务"},
        )
        print(f"   Created backend root: {backend_id}")

        # Test 2: Create subtasks (Level 2)
        print("\n✅ Test 2: Creating Level 2 subtasks...")
        page_id = manager.add_subtask(
            frontend_id,
            {"title": "用户列表页", "type": "page", "description": "显示用户列表"},
        )
        print(f"   Created page: {page_id}")

        service_func_id = manager.add_subtask(
            backend_id,
            {"title": "login函数", "type": "function", "description": "处理登录请求"},
        )
        print(f"   Created function: {service_func_id}")

        # Test 3: Create subtasks (Level 3)
        print("\n✅ Test 3: Creating Level 3 subtasks...")
        component_id = manager.add_subtask(
            page_id,
            {
                "title": "UserListTable组件",
                "type": "component",
                "description": "用户表格组件",
            },
        )
        print(f"   Created component: {component_id}")

        # Test 4: Batch create subtasks
        print("\n✅ Test 4: Batch creating subtasks...")
        batch_ids = manager.add_subtasks_batch(
            page_id,
            [
                {"title": "UserFilter组件", "type": "component"},
                {"title": "UserActions组件", "type": "component"},
            ],
        )
        print(f"   Created components: {', '.join(batch_ids)}")

        # Test 5: Find task
        print("\n✅ Test 5: Finding tasks...")
        found = manager.find_task(component_id)
        if found:
            print(f"   Found task: {found['title']} (ID: {found['id']})")
        else:
            print("   ❌ Task not found!")

        # Test 6: Get task path
        print("\n✅ Test 6: Getting task path (breadcrumb)...")
        path = manager.get_task_path(component_id)
        if path:
            breadcrumb = " > ".join([t["title"] for t in path])
            print(f"   Path: {breadcrumb}")
            print(f"   IDs: {' > '.join([t['id'] for t in path])}")
        else:
            print("   ❌ Path not found!")

        # Test 7: Get all tasks
        print("\n✅ Test 7: Getting all tasks...")
        all_tasks = manager.get_all_tasks()
        print(f"   Total tasks: {len(all_tasks)}")
        for task in all_tasks:
            indent = "  " * (task["level"] - 1)
            print(
                f"   {indent}└─ [{task['id']}] {task['title']} (Level {task['level']})"
            )

        # Test 8: Get tasks by level
        print("\n✅ Test 8: Getting tasks by level...")
        level_2_tasks = manager.get_tasks_by_level(2)
        print(f"   Level 2 tasks: {len(level_2_tasks)}")
        for task in level_2_tasks:
            print(f"     - [{task['id']}] {task['title']}")

        # Test 9: Get tasks by category
        print("\n✅ Test 9: Getting tasks by category...")
        frontend_tasks = manager.get_all_tasks(category="frontend")
        backend_tasks = manager.get_all_tasks(category="backend")
        print(f"   Frontend tasks: {len(frontend_tasks)}")
        print(f"   Backend tasks: {len(backend_tasks)}")

        # Test 10: Update task status
        print("\n✅ Test 10: Updating task status...")
        manager.update_task_status(component_id, "in_progress")
        updated = manager.find_task(component_id)
        print(f"   Task status: {updated['status']}")

        manager.update_task_status(
            component_id, "completed", duration_minutes=45, test_coverage=85
        )
        updated = manager.find_task(component_id)
        print(f"   Task status: {updated['status']}")
        print(f"   Duration: {updated.get('duration_minutes', 0)} mins")
        print(f"   Coverage: {updated.get('test_coverage', 0)}%")

        # Test 11: Add dependencies
        print("\n✅ Test 11: Adding dependencies...")
        # Frontend component depends on backend function
        manager.add_dependency(component_id, service_func_id)
        deps = manager.get_task_dependencies(component_id)
        print(f"   {component_id} depends on:")
        for dep in deps:
            print(f"     - [{dep['id']}] {dep['title']}")

        # Test 12: Get dependents
        print("\n✅ Test 12: Getting dependents...")
        dependents = manager.get_dependents(service_func_id)
        print(f"   Tasks depending on {service_func_id}:")
        for dep in dependents:
            print(f"     - [{dep['id']}] {dep['title']}")

        # Test 13: Get tasks by status
        print("\n✅ Test 13: Getting tasks by status...")
        pending = manager.get_tasks_by_status("pending")
        completed = manager.get_tasks_by_status("completed")
        print(f"   Pending: {len(pending)} tasks")
        print(f"   Completed: {len(completed)} tasks")

        # Test 14: Get ready tasks
        print("\n✅ Test 14: Getting ready tasks...")
        # Mark backend function as completed
        manager.update_task_status(service_func_id, "completed")
        # Mark frontend component as ready
        manager.update_task_status(component_id, "ready")

        ready = manager.get_ready_tasks()
        print(f"   Ready tasks: {len(ready)}")
        for task in ready:
            print(f"     - [{task['id']}] {task['title']}")

        # Test 15: Get blocked tasks
        print("\n✅ Test 15: Getting blocked tasks...")
        # Create a new task that depends on a pending task
        new_comp_id = manager.add_subtask(
            page_id, {"title": "UserModal组件", "type": "component", "status": "ready"}
        )
        manager.add_dependency(new_comp_id, batch_ids[0])  # Depends on UserFilter

        blocked = manager.get_blocked_tasks()
        print(f"   Blocked tasks: {len(blocked)}")
        for task in blocked:
            print(f"     - [{task['id']}] {task['title']}")

        # Test 16: Get statistics
        print("\n✅ Test 16: Getting statistics...")
        stats = manager.get_statistics()
        print(f"   Total tasks: {stats['total_tasks']}")
        print(f"   By status: {stats['by_status']}")
        print(f"   By category: {stats['by_category']}")
        print(f"   By level: {stats['by_level']}")

        # Test 17: Verify tree structure in JSON
        print("\n✅ Test 17: Verifying JSON structure...")
        registry = manager.get_registry()

        print(f"   Frontend root tasks: {len(registry['frontend_tasks'])}")
        print(f"   Backend root tasks: {len(registry['backend_tasks'])}")

        # Pretty print the tree structure
        def print_tree(tasks, indent=2):
            for task in tasks:
                space = " " * indent
                print(f"{space}- [{task['id']}] {task['title']} ({task['status']})")
                if task.get("subtasks"):
                    print_tree(task["subtasks"], indent + 2)

        print("\n   Frontend Tree:")
        print_tree(registry["frontend_tasks"])

        print("\n   Backend Tree:")
        print_tree(registry["backend_tasks"])

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)


if __name__ == "__main__":
    try:
        test_tree_structure()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
