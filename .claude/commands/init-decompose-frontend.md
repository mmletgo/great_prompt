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

### 3. Create Task Registry with Tree Structure
Create `.claude_tasks/task_registry.json` with tree-based structure.

**📄 Task Registry Format**: See [task_registry.json Template](../templates/task_registry.json.template)

**Tree Structure**:
- `frontend_tasks` array (empty initially)
- `backend_tasks` array (empty)
- `frontend_metadata` with framework info
- `backend_metadata` (empty)
- Tasks use dot notation IDs: "1", "2", "1.1", "1.2.3"

### 4. Create Root Tasks for Each Module
Use Python scripts to create Level 1 root tasks:

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

# Create root task for each module
module_1_id = task_mgr.add_root_task("frontend", {
    "title": "Authentication Module",
    "type": "module",
    "description": "Login, Signup, Password Reset pages"
})  # Returns "1"

module_2_id = task_mgr.add_root_task("frontend", {
    "title": "User Profile Module",
    "type": "module",
    "description": "Profile View, Edit Profile, Avatar Upload"
})  # Returns "2"

# ... create more root tasks for other modules
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

Created frontend root tasks (Level 1 modules):
  - ID: "1" - [Module Name] (estimated [M] pages)
  - ID: "2" - [Module Name] (estimated [M] pages)
  - ID: "3" - [Module Name] (estimated [M] pages)
  ...

Frontend framework: [React/Vue/Angular/etc]
UI library: [Material-UI/Ant Design/etc]

📊 Tree Structure:
frontend_tasks/
  ├─ [1] Authentication Module (pending)
  ├─ [2] User Profile Module (pending)
  ├─ [3] Dashboard Module (pending)
  └─ ...

Checkpoint saved with [N] root modules
Status: decomposition_phase = in_progress (frontend)

Next command: /continue-decompose-frontend
```

## Important Rules
- Modules should align with wireframe groupings
- Include reference to relevant wireframe files
- Extract tech stack from architecture document
- Each module should represent a logical feature area

## Next Steps
After initialization:
1. Use `/continue-decompose-frontend` to decompose modules → pages → components
2. Use `/generate-frontend-contexts` to generate context files for all components
3. Then proceed to backend or build dependency graph

````
