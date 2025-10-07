---
description: Initialize frontend task decomposition from wireframes
argument-hint: [batch_size]
---

# Initialize Frontend Task Decomposition

## Your Task
Initialize frontend task decomposition based on completed design artifacts.

## Prerequisites
Check that design phase is complete:
- `designs/user-flows.md` exists
- `designs/wireframes/` directory has wireframe files
- `design_phase.status == "wireframes_completed"`

Also check input documents:
- `docs/prd.md`
- `docs/fullstack-architecture.md`
- `docs/front-end-spec.md`

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
Create `.claude_tasks/task_registry.json`:
```json
{
  "tasks": {
    "frontend_task_001": {
      "id": "frontend_task_001",
      "title": "[Module Name]",
      "level": 1,
      "type": "module",
      "category": "frontend",
      "status": "pending",
      "parent_id": null,
      "children": [],
      "dependencies": [],
      "context_file": "contexts/frontend_task_001_context.md",
      "design_references": [
        "designs/wireframes/page1.md",
        "designs/wireframes/page2.md"
      ]
    }
  },
  "frontend_metadata": {
    "total_pages": 0,
    "total_components": 0,
    "framework": "extracted from architecture doc"
  },
  "dependency_graph": {
    "execution_order": []
  }
}
```

### 4. Update State
Update `.claude_tasks/state.json`:
```json
{
  "design_phase": {
    "status": "completed"
  },
  "decomposition_phase": {
    "status": "in_progress",
    "focus": "frontend",
    "current_level": 1,
    "last_checkpoint": "frontend_task_XXX",
    "progress": {
      "total_tasks": 0,
      "decomposed_tasks": 0,
      "component_level_tasks": 0
    }
  }
}
```

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
