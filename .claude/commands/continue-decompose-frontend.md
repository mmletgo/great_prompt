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
- **Immediately invoke ContextGenerator** (see step 5)

#### If task.type == "module":
- **Decompose to Page level**
- Create task for each page in this module
- Reference corresponding wireframe file
- Save to task_registry (see step 4)

#### If task.type == "page":
- **Decompose to Component level**
- Analyze wireframe to identify UI components
- Create tasks for:
  - Page container component
  - Section components
  - Shared/reusable components
  - State management (if needed)
  - API integration (if needed)
- Save to task_registry (see step 4)
- **For each new component task, invoke ContextGenerator** (see step 5)

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

### 5. Invoke Context Generator for Component Tasks (Parallel)

**Trigger condition**: For each task where `level == 3` AND `type == "component"`

**This includes**:
- Existing component tasks (already at level 3)
- Newly decomposed component tasks (just created in step 3-4)

**CRITICAL - NO PARTIAL PROCESSING**: 
- You MUST create ContextGenerator subagents for EVERY SINGLE component task in this batch
- Count total component tasks FIRST, then verify you created exactly that many subagents
- DO NOT split into "first batch" / "core components" / "remaining components"
- DO NOT process only "important" tasks - ALL tasks are equally important
- If batch has 18 component tasks → create 18 subagents simultaneously
- If you cannot handle all tasks at once, that indicates a system error

**Verification Required**:
1. Count component tasks: `component_count = tasks where level==3 AND type=="component"`
2. Create subagents: MUST equal `component_count` 
3. Output: "Creating {component_count} ContextGenerator subagents in parallel..."
4. Confirm: "✓ All {component_count} context files generated"

**For ALL component-level tasks in the batch, create subagents at once**:
```
Create ContextGenerator subagents for ALL component tasks in parallel.

For each component task (level == 3):

<subagent_task>
Agent: @context-generator
Input:
- Task ID: frontend_task_XXX
- Component metadata: from decomposer output or task_registry
- Design reference: designs/wireframes/[page-name].md
- Parent page context: from parent task

Task:
1. Read component metadata from task_registry
2. Read design reference (wireframe file)
3. Extract component requirements:
   - Props and their types
   - State variables
   - Hooks needed
   - API calls
   - Event handlers
4. Generate comprehensive context file

Output: .claude_tasks/contexts/frontend_task_XXX_context.md with:

# Task XXX: [ComponentName]

## Component Overview
[Description from wireframe]

## Component Specification
### Props
- prop1: type - description
- prop2: type - description

### State
- state1: type - initial value

### Hooks
- useState: [what state]
- useEffect: [what side effect]

### Events
- onClick: [behavior]
- onChange: [behavior]

### API Calls
- GET /api/endpoint: [purpose]

## UI States
- Default state
- Loading state
- Error state
- Success state
- Empty state

## Parent Context
[Information from parent page/container]

## Design Reference
See: designs/wireframes/[page-name].md

## TDD Test Cases
### Test Case 1: Rendering
[Test code]

### Test Case 2: User Interaction
[Test code]

### Test Case 3: API Integration
[Test code]

## Accessibility
- ARIA labels
- Keyboard navigation
- Screen reader support

## Related Files
- Target file: src/components/[path]/ComponentName.tsx
- Test file: src/components/[path]/ComponentName.test.tsx
- Story file: src/components/[path]/ComponentName.stories.tsx
</subagent_task>
```

**Example**: If this batch has 5 component-level tasks, create 5 ContextGenerator subagents simultaneously:
- Subagent 1: frontend_task_008 (LoginForm) → contexts/frontend_task_008_context.md
- Subagent 2: frontend_task_009 (EmailInput) → contexts/frontend_task_009_context.md
- Subagent 3: frontend_task_010 (PasswordInput) → contexts/frontend_task_010_context.md
- Subagent 4: frontend_task_011 (LoginButton) → contexts/frontend_task_011_context.md
- Subagent 5: frontend_task_012 (ErrorMessage) → contexts/frontend_task_012_context.md

**Wait for ALL context generators to complete before proceeding to step 6.**

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

Context Generation Verification:
  - Component tasks in batch: [X]
  - ContextGenerator subagents created: [X]
  - Context files generated: [X]
  ✓ ALL component tasks have context (100% coverage)

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
