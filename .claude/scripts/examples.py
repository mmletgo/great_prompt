"""
Example usage of state management scripts.

This file demonstrates common workflows using the Python scripts
for managing state.json and task_registry.json.
"""

from state_manager import StateManager
from task_registry_manager import TaskRegistryManager
from utils import ProjectManager, print_dashboard


def example_1_design_phase():
    """Example 1: Complete Design Phase"""
    print("=== Example 1: Design Phase ===\n")

    state = StateManager()

    # Initialize after user flows generated
    print("1. Initializing design phase...")
    state.init_design_phase("designs/user-flows.md")
    print("✓ Design phase initialized\n")

    # Complete wireframes
    print("2. Completing wireframes...")
    state.complete_wireframes(
        wireframes_count=8,
        validation_status="passed",
        validation_report="designs/WIREFRAME_VALIDATION.md",
    )
    print("✓ Wireframes completed\n")


def example_2_decomposition_phase():
    """Example 2: Decomposition Phase"""
    print("=== Example 2: Decomposition Phase ===\n")

    state = StateManager()
    tasks = TaskRegistryManager()

    # Start frontend decomposition
    print("1. Starting frontend decomposition...")
    state.start_frontend_decomposition(total_modules=5)
    tasks.init_frontend_metadata(framework="React", language="TypeScript")
    print("✓ Frontend decomposition started\n")

    # Update progress
    print("2. Updating frontend progress...")
    state.update_frontend_progress(total_pages=12, total_components=47)
    tasks.update_frontend_counts(total_pages=12, total_components=47)
    print("✓ Progress updated\n")

    # Complete frontend
    print("3. Completing frontend decomposition...")
    state.complete_frontend_decomposition()
    print("✓ Frontend decomposition complete\n")

    # Start backend decomposition
    print("4. Starting backend decomposition...")
    state.start_backend_decomposition(total_modules=4)
    tasks.init_backend_metadata(
        framework="FastAPI", database="PostgreSQL", language="Python"
    )
    print("✓ Backend decomposition started\n")

    # Complete backend
    print("5. Completing backend decomposition...")
    state.complete_backend_decomposition()
    print("✓ Backend decomposition complete\n")


def example_3_development_phase():
    """Example 3: Development Phase with Task Completion"""
    print("=== Example 3: Development Phase ===\n")

    manager = ProjectManager()

    # Start development
    print("1. Starting development...")
    manager.state.start_development(total_waves=10, workers=5)
    print("✓ Development started with 10 waves, 5 workers\n")

    # Start wave 1
    print("2. Starting Wave 1...")
    manager.state.start_wave(
        wave_number=1, category="backend", total_tasks=15, total_batches=3
    )
    print("✓ Wave 1 started (15 tasks, 3 batches)\n")

    # Complete a task
    print("3. Completing task backend_task_001...")
    manager.complete_task_full(
        task_id="backend_task_001",
        implementation_file="src/api/auth/login.py",
        test_file="tests/api/auth/test_login.py",
        test_coverage=95,
        duration_minutes=12.5,
    )
    print("✓ Task completed (both files updated)\n")

    # Complete a batch
    print("4. Completing Batch 1...")
    completed = [
        "backend_task_001",
        "backend_task_002",
        "backend_task_003",
        "backend_task_004",
        "backend_task_005",
    ]
    manager.complete_batch(wave_number=1, completed_tasks=completed, failed_tasks=[])
    print(f"✓ Batch 1 complete ({len(completed)} tasks)\n")

    # Complete wave
    print("5. Completing Wave 1...")
    # Note: In reality, need to complete all tasks first
    # This is just for demonstration
    result = manager.complete_wave_full(wave_number=1)
    if result["success"]:
        print(
            f"✓ Wave 1 complete: {result['completed']}/{result['total_tasks']} tasks\n"
        )
    else:
        print(f"⚠ Wave 1 has incomplete tasks: {result['incomplete_tasks']}\n")


def example_4_resume_capability():
    """Example 4: Check Resume Status"""
    print("=== Example 4: Resume Capability ===\n")

    manager = ProjectManager()

    # Check if can resume
    print("1. Checking resume status...")
    status = manager.check_resume_status()

    if status["can_resume"]:
        print("✓ Can resume development")
        print(f"  Current Wave: {status['current_wave']}")
        print(f"  Total Waves: {status['total_waves']}")
        print(f"  Completed Tasks: {status['completed_tasks']}")
        print(f"  Failed Tasks: {status['failed_tasks']}")
        print(f"  Pending in Current Wave: {status['pending_in_current_wave']}\n")

        # Get next batch
        print("2. Getting next batch of tasks...")
        next_batch = manager.get_next_batch_tasks(
            wave_number=status["current_wave"], batch_size=5
        )
        print(f"✓ Retrieved {len(next_batch)} tasks for next batch\n")
    else:
        print(f"⚠ Cannot resume: {status['reason']}\n")


def example_5_dashboard():
    """Example 5: Status Dashboard"""
    print("=== Example 5: Status Dashboard ===\n")

    # Print comprehensive dashboard
    print_dashboard()


def example_6_task_registry_operations():
    """Example 6: Task Registry Operations"""
    print("=== Example 6: Task Registry Operations ===\n")

    tasks = TaskRegistryManager()

    # Add a task
    print("1. Adding a task...")
    tasks.add_task(
        "FE_auth_LoginForm",
        {
            "name": "LoginForm Component",
            "category": "frontend",
            "type": "component",
            "module": "auth",
            "parent_page": "LoginPage",
            "status": "pending",
        },
    )
    print("✓ Task FE_auth_LoginForm added\n")

    # Add tasks in batch
    print("2. Adding multiple tasks in batch...")
    batch = {
        "FE_auth_RegisterForm": {
            "name": "RegisterForm Component",
            "category": "frontend",
            "type": "component",
            "module": "auth",
        },
        "FE_auth_PasswordReset": {
            "name": "PasswordReset Component",
            "category": "frontend",
            "type": "component",
            "module": "auth",
        },
    }
    tasks.add_tasks_batch(batch)
    print(f"✓ Added {len(batch)} tasks in batch\n")

    # Update task status
    print("3. Updating task status...")
    tasks.update_task_status(
        task_id="FE_auth_LoginForm",
        status="completed",
        implementation_file="src/components/auth/LoginForm.tsx",
        test_file="src/components/auth/LoginForm.test.tsx",
        test_coverage=95,
        duration_minutes=15.0,
    )
    print("✓ Task status updated\n")

    # Get statistics
    print("4. Getting statistics...")
    stats = tasks.get_statistics()
    print(f"  Total Tasks: {stats['total_tasks']}")
    print(f"  By Status: {stats['by_status']}")
    print(f"  By Category: {stats['by_category']}")
    print(f"  Total Waves: {stats['total_waves']}\n")


if __name__ == "__main__":
    import sys

    examples = {
        "1": ("Design Phase", example_1_design_phase),
        "2": ("Decomposition Phase", example_2_decomposition_phase),
        "3": ("Development Phase", example_3_development_phase),
        "4": ("Resume Capability", example_4_resume_capability),
        "5": ("Status Dashboard", example_5_dashboard),
        "6": ("Task Registry Operations", example_6_task_registry_operations),
    }

    if len(sys.argv) < 2:
        print("Usage: python examples.py <example_number>")
        print("\nAvailable examples:")
        for num, (name, _) in examples.items():
            print(f"  {num}. {name}")
        print("\nOr run all: python examples.py all")
        sys.exit(1)

    arg = sys.argv[1]

    if arg.lower() == "all":
        for num, (name, func) in examples.items():
            func()
            print()
    elif arg in examples:
        _, func = examples[arg]
        func()
    else:
        print(f"Unknown example: {arg}")
        sys.exit(1)
