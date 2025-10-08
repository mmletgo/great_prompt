# Task Management Scripts

This directory contains Python scripts for managing `task_registry.json` and `state.json` files. These scripts provide atomic operations and ensure data consistency.

## 📦 Available Scripts

### 1. state_manager.py
Manages `.claude_tasks/state.json` operations.

**Key Operations:**
- Design Phase: `init_design_phase()`, `complete_wireframes()`
- Decomposition: `start_frontend_decomposition()`, `complete_frontend_decomposition()`, etc.
- Dependency: `complete_dependency_analysis()`
- Development: `start_development()`, `start_wave()`, `complete_task()`, `complete_wave()`

**Usage:**
```python
from state_manager import StateManager

manager = StateManager()  # Uses current directory

# Initialize design phase
manager.init_design_phase("designs/user-flows.md")

# Complete wireframes
manager.complete_wireframes(
    wireframes_count=8,
    validation_status="passed"
)

# Start development
manager.start_development(total_waves=10, workers=5)

# Complete a task
manager.complete_task("FE_auth_LoginForm")

# Complete a wave
manager.complete_wave(wave_number=1)
```

### 2. task_registry_manager.py
Manages `.claude_tasks/task_registry.json` operations.

**Key Operations:**
- Tasks: `add_task()`, `add_tasks_batch()`, `update_task_status()`
- Metadata: `init_frontend_metadata()`, `update_frontend_counts()`
- Dependencies: `add_dependency()`, `set_execution_order()`
- Queries: `get_tasks_by_status()`, `get_wave_tasks()`

**Usage:**
```python
from task_registry_manager import TaskRegistryManager

manager = TaskRegistryManager()

# Add a task
manager.add_task("FE_auth_LoginForm", {
    "name": "LoginForm Component",
    "category": "frontend",
    "type": "component",
    "module": "auth",
    "status": "pending"
})

# Update task status
manager.update_task_status(
    task_id="FE_auth_LoginForm",
    status="completed",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95
)

# Get pending tasks
pending = manager.get_tasks_by_status("pending")
```

### 3. utils.py
High-level utility functions combining both managers.

**Key Operations:**
- `complete_task_full()` - Complete Level 3 task (component/function)
- `complete_integration_task_full()` - Complete Level 2/1 integration task (page/service/module)
- `get_integration_ready_tasks()` - Get tasks ready for integration (all children completed)
- `complete_wave_full()` - Complete wave with validation
- `get_next_batch_tasks()` - Get next batch of pending tasks
- `check_resume_status()` - Check if development can resume
- `get_dashboard()` - Get comprehensive status

**Usage:**
```python
from utils import ProjectManager, print_dashboard

manager = ProjectManager()

# Complete a task (updates both files)
result = manager.complete_task_full(
    task_id="FE_auth_LoginForm",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95,
    duration_minutes=12.5
)

# Get next batch of tasks
next_batch = manager.get_next_batch_tasks(wave_number=1, batch_size=5)

# Complete a wave
result = manager.complete_wave_full(wave_number=1)

# Print dashboard
print_dashboard()
```

**CLI:**
```bash
# Print status dashboard
python utils.py dashboard
python utils.py dashboard /path/to/workspace
```

## 🎯 Common Workflows

### Workflow 1: Complete a Level 3 Development Task (Component/Function)
```python
from utils import ProjectManager

manager = ProjectManager()

# When Level 3 task (component or function) is completed
manager.complete_task_full(
    task_id="1.1.1",  # Dot notation (e.g., LoginForm component)
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95,
    duration_minutes=12.5
)
```

### Workflow 2: Complete a Level 2 Integration Task (Page/Service)
```python
from utils import ProjectManager

manager = ProjectManager()

# First, verify all child tasks are completed
integration_ready = manager.get_integration_ready_tasks(level=2, category="frontend")

if "1.1" in [t["id"] for t in integration_ready]:
    # Page "1.1" is ready (all components completed)
    manager.complete_integration_task_full(
        task_id="1.1",  # LoginPage
        integration_file="src/pages/auth/LoginPage.tsx",
        test_file="src/pages/auth/LoginPage.integration.test.tsx",
        test_coverage=88,
        duration_minutes=25.0
    )
```

### Workflow 3: Complete a Level 1 Integration Task (Module)
```python
from utils import ProjectManager

manager = ProjectManager()

# Verify all child pages/services are completed
integration_ready = manager.get_integration_ready_tasks(level=1, category="backend")

if "2" in [t["id"] for t in integration_ready]:
    # Module "2" is ready (all services completed)
    manager.complete_integration_task_full(
        task_id="2",  # User Management Module
        integration_file="src/modules/user-management/index.ts",
        test_file="src/modules/user-management/system.test.ts",
        test_coverage=85,
        duration_minutes=45.0
    )
```

### Workflow 4: Complete a Batch
```python
from utils import ProjectManager

manager = ProjectManager()

completed = ["FE_auth_LoginForm", "FE_auth_RegisterForm", "FE_auth_PasswordReset"]
failed = ["FE_auth_TwoFactorAuth"]  # If any failed

manager.complete_batch(
    wave_number=1,
    completed_tasks=completed,
    failed_tasks=failed
)
```

### Workflow 5: Complete a Wave
```python
from utils import ProjectManager

manager = ProjectManager()

# Validates all tasks completed before marking wave done
result = manager.complete_wave_full(wave_number=1)

if result['success']:
    print(f"Wave {result['wave']} completed!")
else:
    print(f"Error: {result['error']}")
    print(f"Incomplete tasks: {result['incomplete_tasks']}")
```

### Workflow 6: Resume Development
```python
from utils import ProjectManager

manager = ProjectManager()

# Check resume status
status = manager.check_resume_status()

if status['can_resume']:
    print(f"Resuming from wave {status['current_wave']}")
    print(f"Pending tasks: {status['pending_in_current_wave']}")
    
    # Get next batch
    next_batch = manager.get_next_batch_tasks(
        wave_number=status['current_wave'],
        batch_size=5
    )
else:
    print(f"Cannot resume: {status['reason']}")
```

## 📝 Integration with Commands

These scripts should be called by AI agents in commands instead of manually editing JSON files.

### Example: In parallel-dev-fullstack.md

**Old Approach (Manual JSON):**
```markdown
Update task_registry.json:
- Set task status to "completed"
- Add implementation_file path
- Record test_coverage

Update state.json:
- Add task_id to completed_tasks array
- Increment wave_progress.completed
```

**New Approach (Python Script):**
```markdown
Run Python script to complete task:

```python
from utils import ProjectManager

manager = ProjectManager()
manager.complete_task_full(
    task_id="FE_auth_LoginForm",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95,
    duration_minutes=12.5
)
```
```

## ✅ Benefits

1. **Atomic Operations**: Updates are consistent across both files
2. **Data Validation**: Scripts validate data before writing
3. **Error Prevention**: Reduces risk of JSON syntax errors or inconsistent states
4. **Convenience**: High-level functions like `complete_task_full()` handle multiple updates
5. **Type Safety**: Python type hints help prevent errors
6. **Extensibility**: Easy to add new operations or validations

## 🔧 Installation

No installation needed - these are pure Python 3 scripts with no external dependencies.

**Requirements:**
- Python 3.6+
- Standard library only (json, os, datetime, pathlib, typing)

## 📚 API Reference

See inline documentation in each script for detailed API reference.

Each class and method has comprehensive docstrings with:
- Parameter descriptions
- Return value descriptions
- Usage examples
- Error conditions
