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

**CRITICAL - COMPLETE DECOMPOSITION REQUIRED**:
- You MUST decompose ALL non-component tasks to component level
- DO NOT leave any task at module or page level
- DO NOT mark page tasks as "complete" without decomposing them
- Every page MUST be decomposed into its individual components
- If a page seems "simple", it still has components (at minimum: container, content, buttons)

#### If task.type == "component":
- Mark status as "ready"
- **Immediately invoke ContextGenerator** (see step 5)

#### If task.type == "module":
- **Decompose to Page level**
- Create task for each page in this module
- Reference corresponding wireframe file
- Save to task_registry (see step 4)
- **DO NOT mark module as complete - pages must be decomposed next**

#### If task.type == "page":
- **MUST Decompose to Component level** (non-negotiable)
- Analyze wireframe to identify ALL UI components (no matter how small)
- Create tasks for EVERY component:
  - Page container component (always required)
  - Section components (header, main, sidebar, footer)
  - Shared/reusable components (buttons, inputs, cards)
  - State management components (if needed)
  - API integration components (if needed)
- A "simple" page still has minimum 5-10 components
- Save to task_registry (see step 4)
- **For each new component task, invoke ContextGenerator** (see step 5)
- **DO NOT skip decomposition** - every page must create component tasks

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

**CRITICAL - BATCHED PARALLEL PROCESSING (NO SKIPPING)**:
- You MUST create ContextGenerator subagents for EVERY SINGLE component task in this batch
- Process in sub-batches of maximum 10 subagents at a time for manageability
- Count total component tasks FIRST, calculate number of sub-batches needed
- Process ALL sub-batches - DO NOT stop after first sub-batch
- Each sub-batch must complete before starting next sub-batch

**Batching Rules**:
1. Count total: `component_count = tasks where level==3 AND type=="component"`
2. Calculate batches: `num_batches = ceil(component_count / 10)`
3. Process each batch sequentially, but within each batch create all 10 subagents simultaneously
4. Track progress: "Processing batch X of Y (10 components)..."
5. Verify completion: After ALL batches, confirm total = component_count

**Example - 25 component tasks**:
```
Total component tasks: 25
Sub-batches needed: 3 (10 + 10 + 5)

Processing sub-batch 1 of 3 (10 components)...
  Creating 10 ContextGenerator subagents in parallel:
  - frontend_task_008 (LoginForm)
  - frontend_task_009 (EmailInput)
  - frontend_task_010 (PasswordInput)
  ... (10 total)
  ✓ Sub-batch 1 complete: 10/10 contexts generated

Processing sub-batch 2 of 3 (10 components)...
  Creating 10 ContextGenerator subagents in parallel:
  - frontend_task_018 (DashboardHeader)
  - frontend_task_019 (StatsCard)
  ... (10 total)
  ✓ Sub-batch 2 complete: 10/10 contexts generated

Processing sub-batch 3 of 3 (5 components)...
  Creating 5 ContextGenerator subagents in parallel:
  - frontend_task_028 (SettingsForm)
  ... (5 total)
  ✓ Sub-batch 3 complete: 5/5 contexts generated

✓ ALL batches complete: 25/25 contexts generated (100% coverage)
```

**FORBIDDEN - PARTIAL BATCH PROCESSING**:
- ❌ "Processing first batch, skipping remaining" 
- ❌ "Starting with batch 1, will continue later"
- ❌ "Key components in batch 1, others optional"
- ✅ REQUIRED: "ALL X batches processed" / "100% coverage across all batches"

**Verification Required**:
1. Count component tasks: `component_count = tasks where level==3 AND type=="component"`
2. Calculate sub-batches: `num_batches = ceil(component_count / 10)`
3. For each sub-batch (1 to num_batches):
   - Output: "Processing sub-batch {i} of {num_batches} ({size} components)..."
   - Create subagents: up to 10 per sub-batch
   - Confirm: "✓ Sub-batch {i} complete: {size}/{size} contexts generated"
4. Final verification: "✓ ALL {num_batches} batches complete: {component_count}/{component_count} contexts (100% coverage)"

**For ALL component-level tasks, process in sub-batches of 10**:
```
For each sub-batch of up to 10 component tasks:

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

**Wait for current sub-batch to complete before proceeding to next sub-batch.**
**Wait for ALL sub-batches to complete before proceeding to step 6.**

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
  - Sub-batches processed: [Y] (max 10 per sub-batch)
  - Sub-batch 1: 10/10 contexts ✓
  - Sub-batch 2: 10/10 contexts ✓
  - Sub-batch 3: 5/5 contexts ✓
  - Total contexts generated: [X]
  ✓ ALL sub-batches complete: [X]/[X] contexts (100% coverage)

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
