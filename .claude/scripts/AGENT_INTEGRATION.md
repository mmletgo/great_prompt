# Agent Integration Guide

This guide explains how to integrate Python state management scripts into agent prompts.

## Overview

Previously, agents were instructed to manually edit `state.json` and `task_registry.json` files. This approach was error-prone and led to inconsistencies. Now, agents should use Python scripts for all state updates.

## Key Principles

1. **Never Manual JSON Edits**: Agents should never be instructed to manually edit JSON files
2. **Use Python Scripts**: All state updates must go through the Python API
3. **Atomic Operations**: Use high-level functions that update multiple files atomically
4. **Validation**: Let scripts handle validation and error checking
5. **Consistent Language**: Use consistent terminology when referring to operations

## Before & After Examples

### Example 1: Completing a Task

#### ❌ Before (Manual JSON)
```markdown
After completing the task:

1. Update task_registry.json:
```json
{
  "tasks": {
    "FE_auth_LoginForm": {
      "status": "completed",
      "implementation_file": "src/components/auth/LoginForm.tsx",
      "test_file": "src/components/auth/LoginForm.test.tsx",
      "test_coverage": 95,
      "completed_at": "2024-03-20T10:30:00Z"
    }
  }
}
```

2. Update state.json:
```json
{
  "development_phase": {
    "completed_tasks": ["FE_auth_LoginForm", ...]
  }
}
```
```

#### ✅ After (Python Script)
```markdown
After completing the task, run the following Python script:

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

This automatically updates both task_registry.json and state.json.
```

### Example 2: Starting a Phase

#### ❌ Before (Manual JSON)
```markdown
Initialize frontend decomposition by creating state.json:

```json
{
  "decomposition_phase": {
    "status": "in_progress",
    "frontend_status": "in_progress",
    "progress": {
      "frontend": {
        "total_modules": 5
      }
    }
  },
  "metadata": {
    "last_updated": "2024-03-20T10:00:00Z"
  }
}
```
```

#### ✅ After (Python Script)
```markdown
Initialize frontend decomposition:

```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager

state = StateManager()
tasks = TaskRegistryManager()

# Start decomposition
state.start_frontend_decomposition(total_modules=5)

# Initialize metadata
tasks.init_frontend_metadata(
    framework="React",
    language="TypeScript"
)
```
```

## Agent-Specific Guidelines

### @backend-developer Agent

When implementing a backend task:

```markdown
## Task Completion

After implementing and testing the function:

1. **Update State**:
```python
from utils import ProjectManager

manager = ProjectManager()
manager.complete_task_full(
    task_id="{task_id}",
    implementation_file="{implementation_path}",
    test_file="{test_path}",
    test_coverage={coverage_percent},
    duration_minutes={duration}
)
```

2. **Report Status**:
✓ Task {task_id} completed
  Implementation: {implementation_path}
  Tests: {test_path}
  Coverage: {coverage_percent}%
```

### @frontend-developer Agent

Similar pattern for frontend tasks:

```markdown
## Task Completion

After implementing the component with tests:

```python
from utils import ProjectManager

manager = ProjectManager()
manager.complete_task_full(
    task_id="{task_id}",
    implementation_file="{component_path}",
    test_file="{test_path}",
    test_coverage={coverage_percent},
    duration_minutes={duration}
)
```
```

### @fullstack-dependency-analyzer Agent

When completing dependency analysis:

```markdown
## Save Dependency Graph

After analyzing dependencies:

```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager

state = StateManager()
tasks = TaskRegistryManager()

# Save execution order
waves = [
    {"wave": 1, "category": "backend", "tasks": ["task_001", ...]},
    {"wave": 2, "category": "backend", "tasks": ["task_010", ...]},
    # ... more waves
]
tasks.set_execution_order(waves)

# Mark dependency phase complete
total_waves = len(waves)
state.complete_dependency_analysis(total_waves=total_waves)
```
```

### Orchestrator Agents

For agents that manage batches/waves:

```markdown
## Batch Management

After a batch completes:

```python
from utils import ProjectManager

manager = ProjectManager()

# Get completed and failed task IDs from batch
completed = [...]  # List of completed task IDs
failed = [...]     # List of failed task IDs

# Update batch progress
manager.complete_batch(
    wave_number={wave_number},
    completed_tasks=completed,
    failed_tasks=failed
)
```

## Wave Completion

After all tasks in wave complete:

```python
result = manager.complete_wave_full(wave_number={wave_number})

if result['success']:
    print(f"✓ Wave {result['wave']} complete!")
    print(f"  Tasks: {result['completed']}/{result['total_tasks']}")
else:
    print(f"❌ Incomplete tasks: {result['incomplete_tasks']}")
    # Handle incomplete tasks...
```
```

## Common Patterns

### Pattern 1: Check Resume Status

At the start of development commands:

```markdown
## Initialization

Check if development can be resumed:

```python
from utils import ProjectManager

manager = ProjectManager()
status = manager.check_resume_status()

if status['can_resume']:
    print(f"🔄 Resuming from wave {status['current_wave']}")
    print(f"   Completed: {status['completed_tasks']} tasks")
    print(f"   Pending: {status['pending_in_current_wave']} tasks")
    
    # Get next batch
    next_batch = manager.get_next_batch_tasks(
        wave_number=status['current_wave'],
        batch_size=5
    )
else:
    print("🚀 Starting fresh")
    manager.state.start_development(total_waves=10, workers=5)
```
```

### Pattern 2: Get Next Batch

When processing waves in batches:

```markdown
## Batch Processing

Get next batch of pending tasks:

```python
from utils import ProjectManager

manager = ProjectManager()

# Get next batch
next_batch = manager.get_next_batch_tasks(
    wave_number={current_wave},
    batch_size=5
)

print(f"Next batch: {len(next_batch)} tasks")
for task in next_batch:
    print(f"  - {task['id']}: {task['name']}")
```
```

### Pattern 3: Status Dashboard

For status/monitoring commands:

```markdown
## Project Status

Display comprehensive project status:

```python
from utils import print_dashboard

print_dashboard()
```

Or get structured data:

```python
from utils import ProjectManager

manager = ProjectManager()
dashboard = manager.get_dashboard()

# Access specific fields
print(f"Current phase: {dashboard['phases']['development']}")
print(f"Current wave: {dashboard['development']['current_wave']}")
print(f"Total tasks: {dashboard['tasks']['total_tasks']}")
```
```

## Migration Checklist

When updating agent prompts:

- [ ] Remove all manual JSON editing instructions
- [ ] Add Python script imports at the top
- [ ] Replace JSON examples with Python function calls
- [ ] Add error handling for script operations
- [ ] Include validation (especially for wave completion)
- [ ] Add status reporting after operations
- [ ] Test with actual state files

## Error Handling

Agents should handle potential errors:

```markdown
## Error Handling

Wrap script operations in try-except:

```python
from utils import ProjectManager

manager = ProjectManager()

try:
    manager.complete_task_full(
        task_id="{task_id}",
        implementation_file="{path}",
        test_coverage=95
    )
    print(f"✓ Task {task_id} completed")
except Exception as e:
    print(f"❌ Error completing task: {e}")
    # Report to user or retry
```
```

## Best Practices

1. **Always Use ProjectManager**: For operations that affect multiple files
2. **Validate Wave Completion**: Use `complete_wave_full()` not `complete_wave()`
3. **Check Resume Status**: Before starting development
4. **Report Operations**: Print confirmations after state updates
5. **Use Structured Output**: Print task IDs, counts, and status
6. **Handle Failures**: Distinguish between completed and failed tasks

## Testing Agent Integration

Test checklist for updated agents:

1. **Test Task Completion**:
   - Verify both files updated
   - Check timestamps set
   - Validate task status

2. **Test Batch Processing**:
   - Multiple tasks in one batch
   - Batch counters increment
   - Failed tasks tracked

3. **Test Wave Completion**:
   - Validation catches incomplete waves
   - Wave progress recorded
   - Next wave starts correctly

4. **Test Resume**:
   - Can detect resumable state
   - Gets correct next batch
   - Skips completed waves

## Template for New Agents

When creating new agents that interact with state:

```markdown
---
agent: @new-agent
---

# New Agent

## Initialization

```python
from utils import ProjectManager

manager = ProjectManager()
```

## Main Task

[Agent's main task description]

## State Updates

After completing work:

```python
# Update state as appropriate for this agent
manager.complete_task_full(...)
# or
manager.complete_batch(...)
# or
manager.state.complete_[phase_name](...)
```

## Output

Print status:
```
✓ [Operation] complete
  [Details]
```
```

## References

- **Full API**: [.claude/scripts/README.md](README.md)
- **Examples**: [.claude/scripts/examples.py](examples.py)
- **Quick Reference**: [.claude/scripts/QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Templates**: [.claude/templates/](../templates/)

---

**Status**: Ready for Agent Integration  
**Version**: 1.0  
**Last Updated**: 2025-10-08
