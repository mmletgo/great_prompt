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

**CRITICAL - ENSURE ALL WIREFRAMES ARE INCLUDED**:

**Step 2.1: List ALL wireframe files**
First, list every wireframe file in `designs/wireframes/` directory:
```
✓ login.md
✓ signup.md
✓ forgot-password.md
✓ user-profile.md
✓ edit-profile.md
...
(Total: [N] wireframe files)
```

**Step 2.2: Group wireframes into modules**
Group all wireframes into logical modules (aim for 4-8 modules).
**Every wireframe MUST be assigned to exactly one module.**

Example grouping:
```
1. Authentication Module:
   - login.md
   - signup.md
   - forgot-password.md
   - reset-password.md

2. User Profile Module:
   - user-profile.md
   - edit-profile.md
   - avatar-upload.md

3. Dashboard Module:
   - main-dashboard.md
   - dashboard-widgets.md

4. Navigation Module:
   - header.md
   - sidebar.md
   - mobile-menu.md

5. Shared Components Module:
   - buttons.md
   - forms.md
   - modals.md
```

**Verification**: Count wireframes = Count assigned
- Total wireframes found: [N]
- Total wireframes assigned: [N]
- ✓ All wireframes accounted for

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
# CRITICAL: Include wireframes field with ALL wireframe files for this module
module_1_id = task_mgr.add_root_task("frontend", {
    "title": "Authentication Module",
    "type": "module",
    "description": "Login, Signup, Password Reset pages",
    "wireframes": [
        "designs/wireframes/login.md",
        "designs/wireframes/signup.md",
        "designs/wireframes/forgot-password.md",
        "designs/wireframes/reset-password.md"
    ]
})  # Returns "1"

module_2_id = task_mgr.add_root_task("frontend", {
    "title": "User Profile Module",
    "type": "module",
    "description": "Profile View, Edit Profile, Avatar Upload",
    "wireframes": [
        "designs/wireframes/user-profile.md",
        "designs/wireframes/edit-profile.md",
        "designs/wireframes/avatar-upload.md"
    ]
})  # Returns "2"

# ... create more root tasks for other modules
# IMPORTANT: Every wireframe file must appear in exactly one module's wireframes array
```

**Updates applied**:

### 5. Output Summary
Print:
```
Analyzed design artifacts:
✓ designs/user-flows.md
✓ designs/wireframes/ ([N] wireframe files found)
✓ docs/front-end-spec.md
✓ docs/fullstack-architecture.md

Created frontend root tasks (Level 1 modules):
  - ID: "1" - [Module Name] ([X] wireframes)
    Wireframes: login.md, signup.md, forgot-password.md, reset-password.md
  - ID: "2" - [Module Name] ([Y] wireframes)
    Wireframes: user-profile.md, edit-profile.md, avatar-upload.md
  - ID: "3" - [Module Name] ([Z] wireframes)
    Wireframes: main-dashboard.md, dashboard-widgets.md
  ...

Frontend framework: [React/Vue/Angular/etc]
UI library: [Material-UI/Ant Design/etc]

📊 Tree Structure:
frontend_tasks/
  ├─ [1] Authentication Module (pending) - 4 wireframes
  ├─ [2] User Profile Module (pending) - 3 wireframes
  ├─ [3] Dashboard Module (pending) - 2 wireframes
  └─ ...

✅ Wireframe Coverage Verification:
  Total wireframes found: [N]
  Total wireframes assigned: [N]
  ✓ All wireframes accounted for (100%)

Checkpoint saved with [N] root modules
Status: decomposition_phase = in_progress (frontend)

Next command: /continue-decompose-frontend
```

## Important Rules
- **CRITICAL**: Every wireframe file MUST be assigned to exactly one module
- Verify wireframe count: files found = files assigned
- Modules should align with wireframe groupings
- Each module's `wireframes` array must list all its wireframe files
- Extract tech stack from architecture document
- Each module should represent a logical feature area
- If a wireframe doesn't fit any existing module, create a new module for it

## Next Steps
After initialization:
1. Use `/continue-decompose-frontend` to decompose modules → pages → components
2. Use `/generate-frontend-contexts` to generate context files for all components
3. Then proceed to backend or build dependency graph

````
