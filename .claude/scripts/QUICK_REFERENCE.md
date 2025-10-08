# Python Scripts - Quick Reference Card

## 🚀 Quick Start

```python
# Import the manager
from utils import ProjectManager

# Create instance
manager = ProjectManager()

# Complete a task (most common operation)
manager.complete_task_full(
    task_id="FE_auth_LoginForm",
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95,
    duration_minutes=12.5
)
```

## 📋 Common Operations

### Design Phase
```python
from state_manager import StateManager
state = StateManager()

# Initialize design
state.init_design_phase("designs/user-flows.md")

# Complete wireframes
state.complete_wireframes(
    wireframes_count=8,
    validation_status="passed"
)
```

### Decomposition Phase
```python
from task_registry_manager import TaskRegistryManager
tasks = TaskRegistryManager()

# Frontend
state.start_frontend_decomposition(total_modules=5)
tasks.init_frontend_metadata(framework="React", language="TypeScript")

# Backend
state.start_backend_decomposition(total_modules=4)
tasks.init_backend_metadata(framework="FastAPI", database="PostgreSQL")
```

### Development Phase
```python
from utils import ProjectManager
manager = ProjectManager()

# Start development
manager.state.start_development(total_waves=10, workers=5)

# Start wave
manager.state.start_wave(wave_number=1, category="backend", total_tasks=15)

# Complete task (updates both files)
manager.complete_task_full(
    task_id="backend_task_001",
    implementation_file="src/api/auth/login.py",
    test_file="tests/api/auth/test_login.py",
    test_coverage=95
)

# Complete batch
manager.complete_batch(
    wave_number=1,
    completed_tasks=["task1", "task2", "task3"],
    failed_tasks=[]
)

# Complete wave (with validation)
result = manager.complete_wave_full(wave_number=1)
```

### Resume & Status
```python
# Check resume status
status = manager.check_resume_status()
if status['can_resume']:
    current_wave = status['current_wave']
    next_batch = manager.get_next_batch_tasks(current_wave, batch_size=5)

# Print dashboard
from utils import print_dashboard
print_dashboard()
```

## 🎯 Key Functions by Use Case

### ✅ Complete a Task
```python
manager.complete_task_full(task_id, implementation_file, test_file, test_coverage)
```
**Updates**: task_registry.json + state.json

### ❌ Fail a Task
```python
manager.fail_task_full(task_id, error="Error message")
```
**Updates**: task_registry.json + state.json

### 📦 Complete a Batch
```python
manager.complete_batch(wave_number, completed_tasks, failed_tasks)
```
**Updates**: state.json (wave_progress counters)

### 🌊 Complete a Wave
```python
result = manager.complete_wave_full(wave_number)
if not result['success']:
    print(result['incomplete_tasks'])
```
**Validates**: All tasks completed before marking wave done

### 🔄 Resume Development
```python
status = manager.check_resume_status()
if status['can_resume']:
    next_batch = manager.get_next_batch_tasks(
        wave_number=status['current_wave'],
        batch_size=5
    )
```

### 📊 Get Status
```python
dashboard = manager.get_dashboard()
# or
print_dashboard()
```

## 📝 Task Operations

### Add Single Task
```python
tasks.add_task("FE_auth_LoginForm", {
    "name": "LoginForm Component",
    "category": "frontend",
    "type": "component",
    "status": "pending"
})
```

### Add Multiple Tasks
```python
tasks.add_tasks_batch({
    "task_001": {...},
    "task_002": {...}
})
```

### Update Task Status
```python
tasks.update_task_status(
    task_id="FE_auth_LoginForm",
    status="completed",
    implementation_file="...",
    test_coverage=95
)
```

### Query Tasks
```python
# By status
pending = tasks.get_tasks_by_status("pending")

# By category
frontend = tasks.get_tasks_by_category("frontend")

# Wave tasks
wave_tasks = tasks.get_wave_tasks(wave_number=1)

# Statistics
stats = tasks.get_statistics()
```

## 🔧 State Operations

### Phase Management
```python
state = StateManager()

# Design
state.init_design_phase("designs/user-flows.md")
state.complete_wireframes(count=8)

# Decomposition
state.start_frontend_decomposition(total_modules=5)
state.complete_frontend_decomposition()

# Development
state.start_development(total_waves=10, workers=5)
state.complete_wave(wave_number=1)
```

### Progress Tracking
```python
# Update progress
state.update_frontend_progress(total_pages=12, total_components=47)
state.update_backend_progress(total_services=8, total_functions=35)

# Complete tasks
state.complete_task("task_id")
state.fail_task("task_id")

# Batch progress
state.complete_batch(wave_number=1, completed_count=5, failed_count=0)
```

### Query State
```python
# Get full state
current_state = state.get_state()

# Get phase status
design_status = state.get_phase_status('design')

# Get current wave
current_wave = state.get_current_wave()

# Get completed/failed tasks
completed = state.get_completed_tasks()
failed = state.get_failed_tasks()

# Check resumable
can_resume = state.is_resumable()
```

## ⚙️ CLI Usage

### State Manager CLI
```bash
# Get state
python state_manager.py get_state --workspace .

# Complete wireframes
python state_manager.py complete_wireframes --workspace . --args 8 passed
```

### Task Registry CLI
```bash
# Get statistics
python task_registry_manager.py get_statistics --workspace .

# Update task status
python task_registry_manager.py update_task_status \
    --workspace . \
    --task-id FE_auth_LoginForm \
    --status completed
```

### Utils CLI
```bash
# Print dashboard
python utils.py dashboard
python utils.py dashboard /path/to/workspace
```

## 📦 Installation

**Requirements**: Python 3.6+ (no external dependencies)

**Usage**: Import scripts directly
```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager
from utils import ProjectManager
```

## 🔗 Resources

- **Full Documentation**: [.claude/scripts/README.md](README.md)
- **Examples**: [.claude/scripts/examples.py](examples.py)
- **Templates**: [.claude/templates/](../templates/)
- **Implementation**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## ⚠️ Important Notes

1. **Always use scripts** - Never manually edit JSON files
2. **Atomic operations** - Use `complete_task_full()` for coordinated updates
3. **Validate waves** - Use `complete_wave_full()` to ensure all tasks done
4. **Check resume** - Use `check_resume_status()` before resuming
5. **Dashboard** - Use `print_dashboard()` for quick status check

## 💡 Pro Tips

### Tip 1: Use ProjectManager for Most Operations
```python
# ✅ Good - High-level, atomic
from utils import ProjectManager
manager = ProjectManager()
manager.complete_task_full(...)

# ⚠️ Okay - But need to coordinate both managers
state = StateManager()
tasks = TaskRegistryManager()
state.complete_task(...)
tasks.update_task_status(...)
```

### Tip 2: Validate Before Completing Wave
```python
# ✅ Good - Validates all tasks complete
result = manager.complete_wave_full(wave_number=3)
if not result['success']:
    print(f"Incomplete: {result['incomplete_tasks']}")

# ❌ Bad - No validation
state.complete_wave(wave_number=3)
```

### Tip 3: Check Resume Status First
```python
# ✅ Good - Check before getting tasks
status = manager.check_resume_status()
if status['can_resume']:
    tasks = manager.get_next_batch_tasks(...)

# ❌ Bad - Assume can resume
tasks = manager.get_next_batch_tasks(...)
```

### Tip 4: Use Dashboard for Debugging
```python
# Quick status check
from utils import print_dashboard
print_dashboard()

# Or get structured data
dashboard = manager.get_dashboard()
```

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: ✅ Production Ready
