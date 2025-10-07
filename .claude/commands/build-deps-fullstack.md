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
From task_registry.json:
- All frontend component-level tasks
- All backend function-level tasks

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

5. Create Execution Waves:
   Wave 1: Independent backend utilities, validators
   Wave 2: Backend repositories, core services
   Wave 3: Backend API endpoints
   Wave 4: Shared frontend components (no API calls)
   Wave 5: Frontend components with API integration
   Wave 6: Frontend page containers
   ...

Output format:
{
  "frontend_dependencies": {...},
  "backend_dependencies": {...},
  "cross_stack_dependencies": {
    "frontend_task_XXX": ["backend_task_YYY"]
  },
  "execution_order": [
    {
      "wave": 1,
      "category": "backend",
      "tasks": ["backend_task_001", "backend_task_002"]
    },
    {
      "wave": 2,
      "category": "backend",
      "tasks": ["backend_task_010"]
    },
    {
      "wave": 3,
      "category": "frontend",
      "tasks": ["frontend_task_001"]
    },
    {
      "wave": 4,
      "category": "mixed",
      "tasks": ["frontend_task_005", "backend_task_020"]
    }
  ]
}
</subagent_task>
```

### 3. Update Task Registry
Merge dependency graph into task_registry.json.

### 4. Validate
Ensure:
- No circular dependencies
- Backend endpoints complete before frontend components that call them
- Shared components complete before dependent components
- All tasks included in execution order

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

Execution Plan:
  Wave 1: [N] backend tasks (utils, validators)
  Wave 2: [M] backend tasks (repositories)
  Wave 3: [K] backend tasks (API endpoints)
  Wave 4: [L] frontend tasks (shared components)
  Wave 5: [P] mixed tasks (components + endpoints)
  Wave 6: [Q] frontend tasks (page containers)
  ...
  
Total Waves: [W]
Max Parallelism: [P] tasks (wave [X])

Cross-Stack Dependencies Examples:
- frontend_task_123 (LoginForm) depends on:
  - backend_task_045 (POST /api/auth/login)
  - backend_task_046 (validate_credentials)

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
