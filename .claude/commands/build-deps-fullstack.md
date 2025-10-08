---
description: Build fullstack dependency graph and execution plan
---

# Build Fullstack Dependency Graph

## Your Task
Analyze all frontend and backend tasks and build a comprehensive dependency graph.

## Prerequisites
Check that both frontend and backend decomposition are complete:
- `decomposition_phase.frontend_status == "completed"`
- `decomposition_phase.backend_status == "completed"`
- All frontend tasks are at component level (type == "component")
- All backend tasks are at function level (type == "function")

## Steps

### 1. Collect All Tasks
From task_registry.json (tree structure):
- All frontend component-level tasks (Level 3, type="component")
- All backend function-level tasks (Level 3, type="function")

**Python example**:
```python
task_mgr = TaskRegistryManager()

# Get all Level 3 tasks (leaf tasks ready for development)
frontend_components = task_mgr.get_tasks_by_level(3, category="frontend")
backend_functions = task_mgr.get_tasks_by_level(3, category="backend")

print(f"Frontend components: {len(frontend_components)}")
print(f"Backend functions: {len(backend_functions)}")
print(f"Total tasks: {len(frontend_components) + len(backend_functions)}")
```

### 2. Invoke Fullstack Dependency Analyzer
```
Create a FullstackDependencyAnalyzer subagent.

<subagent_task>
Agent: @fullstack-dependency-analyzer
Input:
- Frontend tasks: from task_registry
- Backend tasks: from task_registry
- Context files: .claude_tasks/contexts/

Task:
1. Analyze Frontend Dependencies:
   - Component hierarchy (parent/child)
   - Shared components used by multiple pages
   - State management dependencies
   - API calls to backend

2. Analyze Backend Dependencies:
   - Service layer dependencies
   - Data access dependencies
   - Utility function dependencies
   - Authentication middleware dependencies

3. Analyze Frontend-Backend Dependencies:
   - Match frontend API calls to backend endpoints
   - Identify backend functions required by frontend

4. Build Cross-Stack Dependency Graph:
   - Backend functions must complete before frontend components that use them
   - Shared components must complete before page components
   - Authentication backend must complete before protected frontend pages
   - **Use dot notation IDs** for all dependencies (e.g., "1.1.2" depends on "2.1.3")

5. Create Execution Waves with Balanced Task Distribution:
   
   **📄 Complete Algorithm Documentation**: [Wave Balancing Algorithm](../WAVE_BALANCING_ALGORITHM.md)
   
   **Wave Balancing Strategy**:
   - Target: 5-10 tasks per wave (optimal for parallel processing)
   - Use topological sort to respect dependencies
   - Group tasks at same dependency level into same wave
   - Split large groups across multiple waves to maintain 5-10 task limit
   - Prefer keeping related tasks together when possible
   
   **Wave Assignment Algorithm**:
   1. Topological sort all tasks by dependencies
   2. Group tasks by dependency level (tasks with no unmet dependencies = level 0)
   3. For each level:
      - If level has ≤10 tasks: Create one wave
      - If level has >10 tasks: Split into multiple waves of 5-10 tasks each
      - Keep backend/frontend of same feature together when splitting
   4. Assign wave numbers sequentially
   
   **Example Wave Distribution**:
   - Total tasks: 47 (20 backend, 27 frontend)
   - Level 0 (no deps): 12 tasks → Wave 1 (8 tasks), Wave 2 (4 tasks)
   - Level 1 (depends on level 0): 18 tasks → Wave 3 (9 tasks), Wave 4 (9 tasks)
   - Level 2 (depends on level 1): 17 tasks → Wave 5 (8 tasks), Wave 6 (9 tasks)
   - Result: 6 waves, each with 4-9 tasks

Output format:
{
  "frontend_dependencies": {...},
  "backend_dependencies": {...},
  "cross_stack_dependencies": {
    "1.2.3": ["2.1.1", "2.1.2"]  // Frontend task depends on backend tasks (dot notation IDs)
  },
  "execution_order": [
    {
      "wave": 1,
      "category": "backend",
      "tasks": ["2.1.1", "2.1.2", "2.2.1"]  // Dot notation IDs
    },
    {
      "wave": 2,
      "category": "backend",
      "tasks": ["2.3.1"]
    },
    {
      "wave": 3,
      "category": "frontend",
      "tasks": ["1.1.1"]
    },
    {
      "wave": 4,
      "category": "mixed",
      "tasks": ["1.2.1", "2.4.1"]
    }
  ]
}
</subagent_task>
```

### 3. Update Task Registry
Merge dependency graph into task_registry.json using Python scripts.

**📄 Script Reference**: See [.claude/scripts/README.md](../.claude/scripts/README.md)

**Python commands**:
```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager

state_mgr = StateManager()
task_mgr = TaskRegistryManager()

# Add dependencies using dot notation IDs
# Frontend component depends on backend function
task_mgr.add_dependency("1.2.3", "2.1.1")  # LoginForm depends on login_endpoint

# Backend function depends on another backend function
task_mgr.add_dependency("2.1.1", "2.2.1")  # login_endpoint depends on validate_credentials

# Set execution order (from analyzer output)
waves = [
    {"wave": 1, "category": "backend", "tasks": ["2.1.1", "2.1.2", "2.1.3"]},
    {"wave": 2, "category": "backend", "tasks": ["2.2.1", "2.2.2"]},
    {"wave": 3, "category": "frontend", "tasks": ["1.1.1", "1.1.2"]},
    # ... more waves with dot notation IDs
]
task_mgr.set_execution_order(waves)

# Mark dependency phase complete
total_waves = len(waves)
state_mgr.complete_dependency_analysis(total_waves=total_waves)
```

This updates:
- `task_registry.json`: dependency_graph.execution_order array
- `state.json`: dependency_phase status and total_waves

### 4. Validate
Ensure:
- No circular dependencies
- Backend endpoints complete before frontend components that call them
- Shared components complete before dependent components
- All tasks included in execution order
- **Each wave has 5-10 tasks** (except possibly last wave)
- Tasks within wave have no mutual dependencies

### 5. Output Summary
```
=== Fullstack Dependency Graph ===

Frontend Tasks: [N]
Backend Tasks: [M]
Total Tasks: [N+M]

Dependency Analysis:
✓ Frontend internal dependencies: [X]
✓ Backend internal dependencies: [Y]
✓ Cross-stack dependencies: [Z]

Execution Plan (Balanced Distribution):
  Wave 1: 8 tasks (backend utils, validators)
  Wave 2: 6 tasks (backend repositories)
  Wave 3: 9 tasks (backend API endpoints)
  Wave 4: 7 tasks (shared frontend components)
  Wave 5: 10 tasks (frontend components with API)
  Wave 6: 7 tasks (frontend page containers)
  ...
  
Total Waves: [W]
Tasks per Wave: 5-10 (balanced)
Average: [AVG] tasks/wave

Cross-Stack Dependencies Examples:
- 1.2.3 (LoginForm) depends on:
  - 2.1.1 (POST /api/auth/login)
  - 2.1.2 (validate_credentials)

✓ Updated task_registry.json with fullstack dependency graph
✓ Ready for parallel development

Next command: /parallel-dev-fullstack [N]
```

## Important Rules
- Backend APIs must complete before frontend components that use them
- Authentication/authorization backends have highest priority
- Shared frontend components before specific page components
- Database layer before service layer
- Service layer before API endpoints

## Wave Balancing Rules

### Target: 5-10 Tasks Per Wave

**Why 5-10 tasks?**
- Minimum 5: Enough parallelism to utilize worker pool efficiently
- Maximum 10: Manageable batch size, faster feedback cycles
- Balanced workload: Prevents bottlenecks and idle workers

**Balancing Algorithm**:

1. **Topological Sort**: Order all tasks by dependencies
   ```
   Level 0: No dependencies (can start immediately)
   Level 1: Depends only on Level 0
   Level 2: Depends on Level 0 or Level 1
   ...
   ```

2. **Group by Dependency Level**: Tasks at same level can execute in parallel
   ```
   Level 0: [task_001, task_002, ..., task_012]  (12 tasks)
   Level 1: [task_013, task_014, ..., task_030]  (18 tasks)
   Level 2: [task_031, task_032, ..., task_047]  (17 tasks)
   ```

3. **Split Large Groups**: If level has >10 tasks, split into multiple waves
   ```
   Level 0 (12 tasks) → Wave 1 (8 tasks), Wave 2 (4 tasks)
   Level 1 (18 tasks) → Wave 3 (9 tasks), Wave 4 (9 tasks)
   Level 2 (17 tasks) → Wave 5 (8 tasks), Wave 6 (9 tasks)
   ```

4. **Feature Affinity**: When splitting, keep related tasks together
   ```
   Level 1 Auth tasks (9 tasks) → Wave 3
   Level 1 Profile tasks (9 tasks) → Wave 4
   ```

**Example Output**:
```json
{
  "execution_order": [
    {
      "wave": 1,
      "category": "backend",
      "tasks": ["BE_util_001", "BE_util_002", "BE_validator_001", ...],
      "task_count": 8,
      "description": "Backend utilities and validators"
    },
    {
      "wave": 2,
      "category": "backend",
      "tasks": ["BE_repo_001", "BE_repo_002", ...],
      "task_count": 6,
      "description": "Backend repositories"
    },
    {
      "wave": 3,
      "category": "backend",
      "tasks": ["BE_api_auth_001", "BE_api_auth_002", ...],
      "task_count": 9,
      "description": "Auth API endpoints"
    },
    {
      "wave": 4,
      "category": "mixed",
      "tasks": ["BE_api_profile_001", ..., "FE_shared_001", ...],
      "task_count": 7,
      "description": "Profile APIs + Shared components"
    }
  ]
}
```

**Validation Checks**:
- ✓ Each wave has 5-10 tasks (except last wave may have <5)
- ✓ No task depends on another task in same wave
- ✓ All dependencies satisfied by previous waves
- ✓ Total tasks = sum of all wave tasks
