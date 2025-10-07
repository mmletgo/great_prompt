---
description: Show current project status and progress
---

# Check Project Status

## Your Task
Display current project status including decomposition and development progress.

## Steps

### 1. Load State Files
Read:
- `.claude_tasks/state.json`
- `.claude_tasks/task_registry.json`

### 2. Calculate Statistics
```python
decomposition_stats = {
    "status": state.decomposition_phase.status,
    "total_tasks": state.decomposition_phase.progress.total_tasks,
    "function_level_tasks": state.decomposition_phase.progress.function_level_tasks,
    "last_checkpoint": state.decomposition_phase.last_checkpoint
}

development_stats = {
    "status": state.development_phase.status,
    "completed": len(state.development_phase.completed_tasks),
    "in_progress": len(state.development_phase.in_progress_tasks),
    "failed": len(state.development_phase.failed_tasks)
}

task_type_counts = {
    "module": count tasks where type == "module",
    "class": count tasks where type == "class",
    "function": count tasks where type == "function"
}
```

### 3. Display Report
```
=== Project Status ===

Decomposition Phase: [STATUS]
  Total tasks: [N]
  Function-level: [N]
  Last checkpoint: [task_XXX]
  
Task Breakdown:
  Modules: [N]
  Classes: [N]
  Functions: [N]

Development Phase: [STATUS]
  Completed: [N]
  In Progress: [N]
  Failed: [N]

[If failed tasks exist:]
Failed Tasks:
  - task_XXX: [title]
  - task_YYY: [title]

[If dependency_graph exists:]
Dependency Graph:
  Total waves: [N]
  Max parallelism: [N]

---
Next Steps:
[Recommend appropriate next command based on current state]
```

## Next Step Recommendations
Based on current state:
- decomposition = "in_progress" → `/continue-decompose`
- decomposition = "completed" & no dependency_graph → `/build-deps`
- dependency_graph exists & development = "not_started" → `/parallel-dev`
- development = "in_progress" → "Development in progress..."
- failed_tasks > 0 → `/retry`
- development = "completed" → "All done! 🎉"
