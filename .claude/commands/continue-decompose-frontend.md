---
description: Continue frontend task decomposition (next batch)
---

# Continue Frontend Task Decomposition

## Your Task
Continue decomposing frontend tasks to component level (React/Vue/Angular components).

## Prerequisites
- `decomposition_phase.status == "in_progress"`
- `decomposition_phase.frontend_status == "in_progress"`

## Steps

### 1. Load State and Get Next Batch
Read state and task registry.
Get next 5-10 pending tasks.

### 2. Process Each Frontend Task
For each task in batch:

#### If task.type == "component":
- Mark status as "ready"
- Invoke FrontendContextGenerator

#### If task.type == "module":
- **Decompose to Page level**
- Create task for each page in this module
- Reference corresponding wireframe file

#### If task.type == "page":
- **Decompose to Component level**
- Analyze wireframe to identify UI components
- Create tasks for:
  - Page container component
  - Section components
  - Shared/reusable components
  - State management (if needed)
  - API integration (if needed)

### 3. Invoke FrontendDecomposer Subagent
```
Create a FrontendDecomposer subagent for frontend_task_XXX.

<subagent_task>
Agent: @frontend-decomposer
Input:
- Task ID: frontend_task_XXX
- Task type: [module/page]
- Design references: [list of wireframe files]
- Frontend spec: docs/front-end-spec.md

Task (if module):
1. List all pages in this module
2. Group related pages
3. Identify shared components across pages
4. Create page-level tasks

Task (if page):
1. Read corresponding wireframe file
2. Identify all UI components in layout
3. Classify components:
   - Container/Layout components
   - Presentational components
   - Form components
   - Interactive components (buttons, modals)
   - Data display components (tables, cards)
4. Identify state management needs
5. Identify API integration points
6. Create component-level tasks with hierarchy

Output format: JSON array of subtasks
[
  {
    "id": "frontend_task_XXX",
    "title": "ComponentName",
    "level": 3,
    "type": "component",
    "component_type": "container|presentational|form|etc",
    "parent_id": "parent_task",
    "props": ["prop1", "prop2"],
    "state": ["state1", "state2"],
    "hooks": ["useState", "useEffect"],
    "api_calls": ["GET /api/users"],
    "design_reference": "designs/wireframes/page.md"
  }
]
</subagent_task>
```

### 4. Save Decomposed Tasks to Registry
For each task decomposed by the FrontendDecomposer:

1. **Add new tasks to `task_registry.json`**:
   - Append each subtask to the `tasks` object
   - Update parent task's `children` array
   - Update parent task's `status` from "pending" to "decomposed"

2. **Update metadata**:
   - Increment `frontend_metadata.total_pages` or `total_components`
   - Update progress counters

Example update:
```json
{
  "tasks": {
    "frontend_task_001": {
      "status": "decomposed",
      "children": ["frontend_task_005", "frontend_task_006", "frontend_task_007"]
    },
    "frontend_task_005": {
      "id": "frontend_task_005",
      "title": "LoginPage",
      "level": 2,
      "type": "page",
      "category": "frontend",
      "status": "pending",
      "parent_id": "frontend_task_001",
      "children": [],
      "design_reference": "designs/wireframes/login-page.md"
    }
  },
  "frontend_metadata": {
    "total_modules": 4,
    "total_pages": 12,
    "total_components": 0
  }
}
```

### 5. Invoke Context Generator for Component Tasks
```
Create a ContextGenerator subagent for component task.

<subagent_task>
Agent: @context-generator
Input:
- Task ID: frontend_task_XXX
- Component metadata: from decomposer output
- Design reference: wireframe file
- Parent page context

Output: .claude_tasks/contexts/frontend_task_XXX_context.md
</subagent_task>
```

### 6. Update Checkpoint
Save progress after each batch:
- Update `state.json` with latest checkpoint
- Save `task_registry.json` with all new tasks

### 7. Check Completion
If all tasks are at component level (type == "component"):
- Set `decomposition_phase.frontend_status = "completed"`
- Output completion message

### 8. Output Summary
```
Resuming from checkpoint: frontend_task_XXX

Processing frontend batch (5-10 tasks)...

frontend_task_001 (Module: Authentication):
  ✓ Decomposed into 3 pages
  
frontend_task_002 (Page: Login):
  ✓ Analyzed wireframe: designs/wireframes/login-page.md
  ✓ Identified 8 components:
    - LoginContainer (container)
    - LoginForm (form)
    - EmailInput (form field)
    - PasswordInput (form field)
    - LoginButton (button)
    - ForgotPasswordLink (link)
    - SignupPrompt (text + link)
    - ErrorMessage (alert)

✓ Processed [N] tasks in this batch
✓ [X] components ready, [Y] tasks need decomposition

Updated checkpoint: frontend_task_XXX
Frontend decomposition: [in_progress | completed]

Next command: [/continue-decompose-frontend OR /init-decompose-backend]
```

## Component Level Hierarchy

### Level 1: Module
Example: "User Authentication Module"

### Level 2: Page
Example: "Login Page"

### Level 3: Component
Examples:
- LoginPageContainer (page wrapper)
- LoginForm (form container)
- EmailInput (form field)
- SubmitButton (button)

## Important Rules
- Each component task must reference its wireframe
- Include component props, state, and hooks in metadata
- Identify API calls needed by component
- Maximum 10 tasks per batch
- Save checkpoint after each batch
- Component names should follow framework conventions
