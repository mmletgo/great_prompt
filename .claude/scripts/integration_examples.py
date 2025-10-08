"""
Integration Task Examples - Demonstrating Level 2 and Level 1 integration workflows.

This script shows how to complete integration tasks after all child tasks are done.
"""

from utils import ProjectManager
from task_registry_manager import TaskRegistryManager


def example_1_check_integration_readiness():
    """Example 1: Check which tasks are ready for integration."""
    print("=== Example 1: Check Integration Readiness ===\n")

    manager = ProjectManager()

    # Check Level 2 frontend (pages ready for integration)
    print("Level 2 Frontend (Pages):")
    ready_pages = manager.get_integration_ready_tasks(level=2, category="frontend")
    for task in ready_pages:
        print(f"  ✓ {task['id']} ({task['title']}) - All components completed")

    if not ready_pages:
        print("  No pages ready for integration yet")

    print()

    # Check Level 2 backend (services ready for integration)
    print("Level 2 Backend (Services):")
    ready_services = manager.get_integration_ready_tasks(level=2, category="backend")
    for task in ready_services:
        print(f"  ✓ {task['id']} ({task['title']}) - All functions completed")

    if not ready_services:
        print("  No services ready for integration yet")

    print()

    # Check Level 1 (modules ready for integration)
    print("Level 1 (Modules):")
    ready_modules = manager.get_integration_ready_tasks(level=1)
    for task in ready_modules:
        category = task["category"]
        children_type = "pages" if category == "frontend" else "services"
        print(f"  ✓ {task['id']} ({task['title']}) - All {children_type} completed")

    if not ready_modules:
        print("  No modules ready for integration yet")

    print()


def example_2_integrate_page():
    """Example 2: Integrate a page from completed components."""
    print("=== Example 2: Integrate Page (Level 2 Frontend) ===\n")

    manager = ProjectManager()

    # Assume page "1.1" (LoginPage) has all components completed
    page_id = "1.1"

    print(f"Integrating page: {page_id}")
    print("Children (components): 1.1.1, 1.1.2, 1.1.3")
    print("Task: Assemble components into cohesive page\n")

    try:
        result = manager.complete_integration_task_full(
            task_id=page_id,
            integration_file="src/pages/auth/LoginPage.tsx",
            test_file="src/pages/auth/LoginPage.integration.test.tsx",
            test_coverage=88,
            duration_minutes=25.0,
        )

        print("✓ Page integration completed!")
        print(f"  Task ID: {result['task_id']}")
        print(f"  Level: {result['level']}")
        print(f"  Type: {result['type']}")
        print(f"  Updated: {', '.join(result['updated'])}")

    except ValueError as e:
        print(f"✗ Integration failed: {e}")

    print()


def example_3_integrate_service():
    """Example 3: Integrate a service from completed functions."""
    print("=== Example 3: Integrate Service (Level 2 Backend) ===\n")

    manager = ProjectManager()

    # Assume service "2.1" (AuthService) has all functions completed
    service_id = "2.1"

    print(f"Integrating service: {service_id}")
    print("Children (functions): 2.1.1, 2.1.2, 2.1.3, 2.1.4")
    print("Task: Orchestrate functions into cohesive service\n")

    try:
        result = manager.complete_integration_task_full(
            task_id=service_id,
            integration_file="src/services/auth/AuthService.ts",
            test_file="src/services/auth/AuthService.integration.test.ts",
            test_coverage=92,
            duration_minutes=35.0,
        )

        print("✓ Service integration completed!")
        print(f"  Task ID: {result['task_id']}")
        print(f"  Level: {result['level']}")
        print(f"  Type: {result['type']}")
        print(f"  Updated: {', '.join(result['updated'])}")

    except ValueError as e:
        print(f"✗ Integration failed: {e}")

    print()


def example_4_integrate_module():
    """Example 4: Integrate a module from completed pages/services."""
    print("=== Example 4: Integrate Module (Level 1) ===\n")

    manager = ProjectManager()

    # Assume module "1" (Auth Module) has all pages completed
    module_id = "1"

    print(f"Integrating module: {module_id}")
    print("Children (pages): 1.1, 1.2, 1.3")
    print("Task: Create complete user flow across pages\n")

    try:
        result = manager.complete_integration_task_full(
            task_id=module_id,
            integration_file="src/modules/auth/index.tsx",
            test_file="src/modules/auth/e2e.test.tsx",
            test_coverage=85,
            duration_minutes=45.0,
        )

        print("✓ Module integration completed!")
        print(f"  Task ID: {result['task_id']}")
        print(f"  Level: {result['level']}")
        print(f"  Type: {result['type']}")
        print(f"  Updated: {', '.join(result['updated'])}")

    except ValueError as e:
        print(f"✗ Integration failed: {e}")

    print()


def example_5_full_integration_workflow():
    """Example 5: Complete integration workflow (bottom-up)."""
    print("=== Example 5: Full Integration Workflow ===\n")

    manager = ProjectManager()

    print("Phase 1: Level 3 Implementation (Leaf Nodes)")
    print("-" * 50)
    # Simulate completing Level 3 tasks
    level3_tasks = [
        ("1.1.1", "LoginForm.tsx", 95),
        ("1.1.2", "SocialButtons.tsx", 90),
        ("1.1.3", "LoginHeader.tsx", 88),
    ]

    for task_id, impl_file, coverage in level3_tasks:
        print(f"  ✓ Completed {task_id}: {impl_file} ({coverage}% coverage)")

    print()

    print("Phase 2: Level 2 Integration (Assemble Components → Page)")
    print("-" * 50)
    # Check if page ready
    ready_pages = manager.get_integration_ready_tasks(level=2, category="frontend")

    if ready_pages:
        page = ready_pages[0]
        print(f"  Page {page['id']} ready for integration")
        print(f"    Children: {', '.join([c['id'] for c in page['subtasks']])}")
        print(f"  ✓ Integrating page: {page['id']}")
        # manager.complete_integration_task_full(...) would be called here
    else:
        print("  No pages ready yet (simulated)")

    print()

    print("Phase 3: Level 1 Integration (Assemble Pages → Module)")
    print("-" * 50)
    # Check if module ready
    ready_modules = manager.get_integration_ready_tasks(level=1, category="frontend")

    if ready_modules:
        module = ready_modules[0]
        print(f"  Module {module['id']} ready for integration")
        print(f"    Children: {', '.join([c['id'] for c in module['subtasks']])}")
        print(f"  ✓ Integrating module: {module['id']}")
        # manager.complete_integration_task_full(...) would be called here
    else:
        print("  No modules ready yet (simulated)")

    print()


def example_6_error_handling():
    """Example 6: Error handling when children not completed."""
    print("=== Example 6: Error Handling ===\n")

    manager = ProjectManager()

    print("Attempting to integrate page with incomplete children:")
    print("  Page: 1.2 (RegisterPage)")
    print("  Children: 1.2.1 (✓ completed), 1.2.2 (⏳ in_progress)")
    print()

    try:
        manager.complete_integration_task_full(
            task_id="1.2",
            integration_file="src/pages/auth/RegisterPage.tsx",
        )
        print("✓ Integration succeeded")

    except ValueError as e:
        print(f"✗ Integration failed (expected): {e}")
        print()
        print("Solution: Complete all child tasks first:")
        print("  1. Complete task 1.2.2")
        print("  2. Retry integration of task 1.2")

    print()


def main():
    """Run all examples."""
    import sys

    if len(sys.argv) > 1:
        example_num = sys.argv[1]

        examples = {
            "1": example_1_check_integration_readiness,
            "2": example_2_integrate_page,
            "3": example_3_integrate_service,
            "4": example_4_integrate_module,
            "5": example_5_full_integration_workflow,
            "6": example_6_error_handling,
        }

        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Example {example_num} not found")
            print(f"Available examples: {', '.join(examples.keys())}")
    else:
        # Run all examples
        example_1_check_integration_readiness()
        example_2_integrate_page()
        example_3_integrate_service()
        example_4_integrate_module()
        example_5_full_integration_workflow()
        example_6_error_handling()


if __name__ == "__main__":
    main()
