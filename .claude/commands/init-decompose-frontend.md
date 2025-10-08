---
description: Initialize frontend task decomposition from wireframes
---

# Initialize Frontend Task Decomposition

## Your Task
Initialize frontend task decomposition based on completed design artifacts.

## Prerequisites
Check that design phase is complete:
- `designs/user-flows.md` exists
- `designs/wireframes/` directory has wireframe files
- `design_phase.status == "completed"`

Also check input documents:
- `docs/prd.md` (必需)
- `docs/fullstack-architecture.md` (可选)
- `docs/front-end-spec.md` (可选)

## Steps

### 1. Analyze Design Artifacts
Read and analyze:
- All wireframes in `designs/wireframes/`
- User flows in `designs/user-flows.md`
- Frontend spec in `docs/front-end-spec.md`
- Architecture in `docs/fullstack-architecture.md`

### 2. Identify Frontend Modules
Group pages and components into logical modules (aim for 4-8 modules):

Examples:
- Authentication Module (Login, Signup, Password Reset)
- User Profile Module (Profile View, Edit Profile, Avatar Upload)
- Dashboard Module (Main Dashboard, Widgets)
- Navigation Module (Header, Sidebar, Mobile Menu)
- Shared Components Module (Buttons, Forms, Modals)

### 3. Create Task Registry
Create `.claude_tasks/task_registry.json` with initial structure.

**📄 Task Registry Format**: See [task_registry.json Template](../templates/task_registry.json.template)

**Initialize with**:
- Empty `tasks` object
- `frontend_metadata` with framework and counters at 0
- Empty `backend_metadata`
- Empty `dependency_graph`

### 4. Update State
Use Python scripts to update both state.json and task_registry.json:

**📄 Script Reference**: See [.claude/scripts/README.md](../.claude/scripts/README.md)

**Python commands**:
```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager

state_mgr = StateManager()
task_mgr = TaskRegistryManager()

# Initialize frontend decomposition
state_mgr.start_frontend_decomposition(total_modules=5)

# Initialize frontend metadata
task_mgr.init_frontend_metadata(
    framework="React",
    language="TypeScript"
)
```

**Updates applied**:

### 5. Output Summary
Print:
```
Analyzed design artifacts:
✓ designs/user-flows.md
✓ designs/wireframes/ ([N] pages)
✓ docs/front-end-spec.md
✓ docs/fullstack-architecture.md

Identified frontend modules:
  - frontend_task_001: [Module Name] ([M] pages)
  - frontend_task_002: [Module Name] ([M] pages)
  ...

Frontend framework: [React/Vue/Angular/etc]
UI library: [Material-UI/Ant Design/etc]

Checkpoint saved: frontend_task_XXX
Status: decomposition_phase = in_progress (frontend)

Next command: /continue-decompose-frontend
```

## Important Rules
- Modules should align with wireframe groupings
- Include reference to relevant wireframe files
- Extract tech stack from architecture document
- Create 4-8 frontend modules maximum
- Each module should represent a logical feature area

## Next Steps
After initialization, use `/continue-decompose-frontend` which will:
- Invoke @frontend-decomposer agent to decompose modules → pages → components
- Generate context files for each component using @context-generator

````
