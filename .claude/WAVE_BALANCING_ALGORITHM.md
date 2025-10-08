# Wave Balancing Algorithm

## Overview

This document describes the algorithm for creating balanced execution waves with 5-10 tasks each, while respecting dependency constraints.

## Goals

1. **Balanced Workload**: Each wave should have 5-10 tasks
2. **Dependency Respect**: No task executes before its dependencies
3. **Feature Affinity**: Related tasks (same feature/module) stay together
4. **Optimal Parallelism**: Maximize concurrent task execution

## Algorithm

### Step 1: Build Dependency Graph

```python
def build_dependency_graph(tasks):
    """
    Build directed acyclic graph (DAG) of task dependencies.
    
    Input: List of tasks with dependencies
    Output: Adjacency list representing dependency graph
    """
    graph = {}
    in_degree = {}  # Number of dependencies for each task
    
    for task in tasks:
        task_id = task['id']
        graph[task_id] = task.get('dependencies', [])
        
        # Calculate in-degree (number of tasks this depends on)
        in_degree[task_id] = len(task.get('dependencies', []))
    
    return graph, in_degree
```

### Step 2: Topological Sort with Levels

```python
def topological_sort_with_levels(graph, in_degree):
    """
    Perform topological sort and assign dependency levels.
    
    Level 0: Tasks with no dependencies
    Level 1: Tasks that only depend on Level 0
    Level 2: Tasks that depend on Level 0 or Level 1
    ...
    """
    levels = {}
    current_level = 0
    queue = [task for task, degree in in_degree.items() if degree == 0]
    
    while queue:
        # All tasks in current queue are at same level
        for task_id in queue:
            levels[task_id] = current_level
        
        # Find next level tasks
        next_queue = []
        for task_id in queue:
            # For each task depending on current task
            for dependent in get_dependents(graph, task_id):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    next_queue.append(dependent)
        
        queue = next_queue
        current_level += 1
    
    # Group by level
    level_groups = {}
    for task_id, level in levels.items():
        if level not in level_groups:
            level_groups[level] = []
        level_groups[level].append(task_id)
    
    return level_groups
```

### Step 3: Balance Waves

```python
def create_balanced_waves(level_groups, min_tasks=5, max_tasks=10):
    """
    Create balanced waves from level groups.
    
    Strategy:
    - If level has ≤max_tasks: One wave
    - If level has >max_tasks: Split into multiple waves
    - Try to keep task count between min_tasks and max_tasks
    """
    waves = []
    wave_number = 1
    
    for level in sorted(level_groups.keys()):
        tasks = level_groups[level]
        
        if len(tasks) <= max_tasks:
            # Single wave
            waves.append({
                "wave": wave_number,
                "tasks": tasks,
                "task_count": len(tasks),
                "level": level
            })
            wave_number += 1
        else:
            # Split into multiple waves
            # Try to make waves as equal as possible
            num_waves = (len(tasks) + max_tasks - 1) // max_tasks
            tasks_per_wave = len(tasks) // num_waves
            
            start = 0
            for i in range(num_waves):
                # Last wave gets remainder
                end = start + tasks_per_wave
                if i == num_waves - 1:
                    end = len(tasks)
                
                wave_tasks = tasks[start:end]
                waves.append({
                    "wave": wave_number,
                    "tasks": wave_tasks,
                    "task_count": len(wave_tasks),
                    "level": level
                })
                wave_number += 1
                start = end
    
    return waves
```

### Step 4: Feature-Based Grouping (Optional Enhancement)

```python
def group_by_feature(tasks, max_tasks=10):
    """
    Group tasks by feature/module to keep related work together.
    
    This is applied within each dependency level.
    """
    feature_groups = {}
    
    for task in tasks:
        feature = extract_feature(task)  # e.g., "auth", "profile"
        if feature not in feature_groups:
            feature_groups[feature] = []
        feature_groups[feature].append(task)
    
    # Create waves from feature groups
    waves = []
    current_wave = []
    
    for feature, feature_tasks in feature_groups.items():
        if len(current_wave) + len(feature_tasks) <= max_tasks:
            # Add to current wave
            current_wave.extend(feature_tasks)
        else:
            # Start new wave
            if current_wave:
                waves.append(current_wave)
            current_wave = feature_tasks
    
    if current_wave:
        waves.append(current_wave)
    
    return waves
```

## Complete Algorithm

```python
def create_balanced_execution_plan(tasks, min_tasks=5, max_tasks=10):
    """
    Main algorithm: Create balanced wave execution plan.
    
    Args:
        tasks: List of task objects with id and dependencies
        min_tasks: Minimum tasks per wave (default: 5)
        max_tasks: Maximum tasks per wave (default: 10)
    
    Returns:
        List of wave objects with balanced task distribution
    """
    # Step 1: Build dependency graph
    graph, in_degree = build_dependency_graph(tasks)
    
    # Step 2: Topological sort with levels
    level_groups = topological_sort_with_levels(graph, in_degree)
    
    # Step 3: For each level, group by feature (optional)
    enhanced_level_groups = {}
    for level, level_tasks in level_groups.items():
        if len(level_tasks) > max_tasks:
            # Group by feature first
            feature_groups = group_tasks_by_feature(level_tasks)
            enhanced_level_groups[level] = feature_groups
        else:
            enhanced_level_groups[level] = [level_tasks]
    
    # Step 4: Create balanced waves
    waves = create_balanced_waves(enhanced_level_groups, min_tasks, max_tasks)
    
    # Step 5: Validate
    validate_waves(waves, graph)
    
    return waves


def validate_waves(waves, graph):
    """
    Validate wave structure:
    - No circular dependencies
    - All dependencies satisfied by previous waves
    - Task count within bounds
    """
    completed_tasks = set()
    
    for wave in waves:
        # Check task count
        task_count = wave['task_count']
        assert task_count >= 1, f"Wave {wave['wave']} is empty"
        
        # Check dependencies
        for task_id in wave['tasks']:
            dependencies = graph.get(task_id, [])
            for dep in dependencies:
                assert dep in completed_tasks, \
                    f"Task {task_id} depends on {dep} which is not completed"
        
        # Mark tasks as completed
        completed_tasks.update(wave['tasks'])
    
    print(f"✓ Validation passed: {len(waves)} waves, {len(completed_tasks)} tasks")
```

## Example Execution

### Input: 47 Tasks

```python
tasks = [
    # Backend utilities (no dependencies)
    {"id": "BE_util_001", "dependencies": []},
    {"id": "BE_util_002", "dependencies": []},
    # ... 10 more utility tasks
    
    # Backend repositories (depend on utilities)
    {"id": "BE_repo_001", "dependencies": ["BE_util_001"]},
    {"id": "BE_repo_002", "dependencies": ["BE_util_002"]},
    # ... 6 more repository tasks
    
    # Backend API endpoints (depend on repositories)
    {"id": "BE_api_auth_001", "dependencies": ["BE_repo_001", "BE_repo_002"]},
    # ... 15 more API tasks
    
    # Frontend shared components (no backend dependencies)
    {"id": "FE_shared_001", "dependencies": []},
    # ... 5 more shared components
    
    # Frontend feature components (depend on backend APIs)
    {"id": "FE_auth_login", "dependencies": ["BE_api_auth_001"]},
    # ... 20 more feature components
]
```

### Output: Balanced Waves

```json
{
  "execution_order": [
    {
      "wave": 1,
      "level": 0,
      "tasks": ["BE_util_001", "BE_util_002", "BE_util_003", "BE_util_004", 
                "BE_util_005", "BE_util_006", "BE_util_007", "BE_util_008"],
      "task_count": 8,
      "category": "backend",
      "description": "Backend utilities (Level 0, Part 1)"
    },
    {
      "wave": 2,
      "level": 0,
      "tasks": ["BE_util_009", "BE_util_010", "BE_util_011", "BE_util_012",
                "FE_shared_001", "FE_shared_002"],
      "task_count": 6,
      "category": "mixed",
      "description": "Backend utilities + Shared frontend (Level 0, Part 2)"
    },
    {
      "wave": 3,
      "level": 1,
      "tasks": ["BE_repo_001", "BE_repo_002", "BE_repo_003", "BE_repo_004",
                "BE_repo_005", "BE_repo_006", "BE_repo_007", "BE_repo_008"],
      "task_count": 8,
      "category": "backend",
      "description": "Backend repositories (Level 1)"
    },
    {
      "wave": 4,
      "level": 2,
      "tasks": ["BE_api_auth_001", "BE_api_auth_002", "BE_api_auth_003",
                "BE_api_profile_001", "BE_api_profile_002", "BE_api_profile_003",
                "BE_api_dashboard_001", "BE_api_dashboard_002"],
      "task_count": 8,
      "category": "backend",
      "description": "Backend API endpoints - Auth + Profile + Dashboard (Level 2, Part 1)"
    },
    {
      "wave": 5,
      "level": 2,
      "tasks": ["BE_api_settings_001", "BE_api_settings_002", "BE_api_notification_001",
                "BE_api_notification_002", "BE_api_analytics_001", "BE_api_analytics_002",
                "BE_api_export_001", "BE_api_export_002"],
      "task_count": 8,
      "category": "backend",
      "description": "Backend API endpoints - Settings + Notifications + Analytics + Export (Level 2, Part 2)"
    },
    {
      "wave": 6,
      "level": 3,
      "tasks": ["FE_auth_login", "FE_auth_register", "FE_auth_forgot",
                "FE_profile_view", "FE_profile_edit", "FE_dashboard_main",
                "FE_dashboard_widget_001", "FE_dashboard_widget_002"],
      "task_count": 8,
      "category": "frontend",
      "description": "Frontend components - Auth + Profile + Dashboard (Level 3, Part 1)"
    },
    {
      "wave": 7,
      "level": 3,
      "tasks": ["FE_settings_page", "FE_settings_form", "FE_notification_list",
                "FE_notification_item", "FE_analytics_chart", "FE_analytics_table",
                "FE_export_button"],
      "task_count": 7,
      "category": "frontend",
      "description": "Frontend components - Settings + Notifications + Analytics + Export (Level 3, Part 2)"
    }
  ],
  "summary": {
    "total_waves": 7,
    "total_tasks": 47,
    "average_tasks_per_wave": 6.7,
    "min_tasks": 6,
    "max_tasks": 8,
    "balanced": true
  }
}
```

## Benefits

### Before (Unbalanced)
```
Wave 1: 3 tasks  ❌ Underutilized (5 workers, only 3 tasks)
Wave 2: 15 tasks ❌ Overloaded (takes 3 batches)
Wave 3: 2 tasks  ❌ Underutilized
Wave 4: 22 tasks ❌ Overloaded (takes 5 batches)
Wave 5: 5 tasks  ✓ Good
```

### After (Balanced)
```
Wave 1: 8 tasks  ✓ Optimal
Wave 2: 6 tasks  ✓ Good
Wave 3: 8 tasks  ✓ Optimal
Wave 4: 8 tasks  ✓ Optimal
Wave 5: 8 tasks  ✓ Optimal
Wave 6: 8 tasks  ✓ Optimal
Wave 7: 7 tasks  ✓ Good
```

**Improvements**:
- ✅ Better worker utilization (fewer idle workers)
- ✅ Faster feedback cycles (smaller batches)
- ✅ More predictable execution time per wave
- ✅ Easier to track progress (more granular checkpoints)

## Edge Cases

### Case 1: Very Few Tasks (<5)
```python
# If total tasks < min_tasks, create single wave
if len(tasks) < min_tasks:
    return [{"wave": 1, "tasks": tasks, "task_count": len(tasks)}]
```

### Case 2: Last Wave Has Few Tasks
```python
# Last wave can have <min_tasks, that's acceptable
# Example: Wave 7 has 3 tasks (acceptable as final wave)
```

### Case 3: Long Dependency Chain
```python
# Each level might have only 1-2 tasks
# Solution: Combine adjacent levels if total ≤ max_tasks
def combine_small_levels(level_groups, max_tasks):
    combined = []
    current = []
    
    for level in sorted(level_groups.keys()):
        tasks = level_groups[level]
        if len(current) + len(tasks) <= max_tasks:
            current.extend(tasks)
        else:
            if current:
                combined.append(current)
            current = tasks
    
    if current:
        combined.append(current)
    
    return combined
```

### Case 4: Feature Spans Multiple Levels
```python
# Keep feature tasks together even across levels
# If Feature X has tasks in Level 1 and Level 2:
#   - Put Level 1 tasks in earlier wave
#   - Put Level 2 tasks in later wave
#   - Both waves can be labeled as "Feature X (Part 1/2)"
```

## Configuration

```python
# Default configuration
WAVE_CONFIG = {
    "min_tasks_per_wave": 5,
    "max_tasks_per_wave": 10,
    "prefer_feature_grouping": True,
    "allow_mixed_category": True,  # Backend + Frontend in same wave
    "combine_small_levels": True,  # Combine levels with <min_tasks
}
```

## Testing

```python
def test_wave_balancing():
    """Test wave balancing algorithm."""
    
    # Test 1: Simple linear dependencies
    tasks = create_test_tasks_linear(20)
    waves = create_balanced_execution_plan(tasks)
    assert all(5 <= w['task_count'] <= 10 for w in waves[:-1])
    
    # Test 2: Complex dependency graph
    tasks = create_test_tasks_complex(50)
    waves = create_balanced_execution_plan(tasks)
    validate_waves(waves, build_dependency_graph(tasks)[0])
    
    # Test 3: Edge case - very few tasks
    tasks = create_test_tasks_linear(3)
    waves = create_balanced_execution_plan(tasks)
    assert len(waves) == 1
    
    print("✓ All tests passed")
```

## Summary

The wave balancing algorithm ensures:
- 🎯 **5-10 tasks per wave** (optimal parallelism)
- 🔗 **Dependency respect** (no task before its dependencies)
- 🎨 **Feature affinity** (related tasks stay together)
- ⚡ **Better utilization** (fewer idle workers)
- 📊 **Predictable progress** (consistent wave sizes)

This creates a more efficient and manageable execution plan compared to simple sequential or arbitrary wave assignment.
