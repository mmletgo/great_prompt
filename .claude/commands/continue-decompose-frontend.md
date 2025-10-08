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
Read state and task registry using tree structure.

**CRITICAL - LAYER-BY-LAYER DECOMPOSITION**:
- **Phase 1**: Decompose ALL Level 1 tasks to Level 2 first
- **Phase 2**: Only after Phase 1 is complete, decompose ALL Level 2 tasks to Level 3
- DO NOT mix Level 1 and Level 2 decomposition in the same batch

**Python example**:
```python
task_mgr = TaskRegistryManager()

# Get all pending tasks
pending_tasks = task_mgr.get_tasks_by_status("pending", category="frontend")

# Phase 1: Get Level 1 tasks (modules) that need decomposition
level1_tasks = [t for t in pending_tasks if t["level"] == 1]

if level1_tasks:
    # Still in Phase 1: decompose modules to pages
    batch = level1_tasks[:10]  # Process up to 10 modules
    current_phase = "Level 1 → Level 2 (Module → Page)"
else:
    # Phase 1 complete, move to Phase 2: decompose pages to components
    level2_tasks = [t for t in pending_tasks if t["level"] == 2]
    batch = level2_tasks[:10]  # Process up to 10 pages
    current_phase = "Level 2 → Level 3 (Page → Component)"
```

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
- **Immediately invoke ContextGenerator** (see step 6)
- Note: Only Level 3 components get context files; Level 2/1 integration tasks do not

#### If task.type == "module" (Level 1):
- **Decompose to Page level (Level 2)**
- Use `add_subtask()` to create page tasks under this module
- Each page gets dot notation ID based on parent (e.g., parent="1" → pages="1.1", "1.2", etc.)
- Reference corresponding wireframe file
- **DO NOT mark module as complete - pages must be decomposed next**
- Parent status automatically changes to "decomposed"

**Python example**:
```python
task_mgr = TaskRegistryManager()

# Create page tasks under module "1"
login_page_id = task_mgr.add_subtask("1", {
    "title": "Login Page",
    "type": "page",
    "route": "/login",
    "wireframe": "designs/wireframes/login.md"
})  # Returns "1.1"

signup_page_id = task_mgr.add_subtask("1", {
    "title": "Signup Page",
    "type": "page",
    "route": "/signup",
    "wireframe": "designs/wireframes/signup.md"
})  # Returns "1.2"
```

#### If task.type == "page" (Level 2):
- **MUST Decompose to Component level (Level 3)** (non-negotiable)
- Analyze wireframe to identify ALL UI components
- Use `add_subtasks_batch()` to create multiple component tasks at once
- Each component gets dot notation ID (e.g., parent="1.1" → components="1.1.1", "1.1.2", etc.)
- Create tasks for EVERY component:
  - Page container component (always required)
  - Section components (header, main, sidebar, footer)
  - Shared/reusable components (buttons, inputs, cards)
  - State management components (if needed)
  - API integration components (if needed)
- A "simple" page still has minimum 5-10 components
- **DO NOT skip decomposition** - every page must create component tasks
- Parent status automatically changes to "decomposed"

**Python example**:
```python
# Create component tasks under page "1.1"
component_ids = task_mgr.add_subtasks_batch("1.1", [
    {"title": "LoginForm", "type": "component"},
    {"title": "LoginHeader", "type": "component"},
    {"title": "SocialLoginButtons", "type": "component"},
    {"title": "ForgotPasswordLink", "type": "component"}
])  # Returns ["1.1.1", "1.1.2", "1.1.3", "1.1.4"]
```

**For each new component task, invoke ContextGenerator** (see step 5)

### 3. Invoke FrontendDecomposer Subagents (Parallel)

**CRITICAL - CREATE ALL DECOMPOSER SUBAGENTS IN PARALLEL**:
- You MUST create decomposer subagents for ALL tasks in the batch SIMULTANEOUSLY
- DO NOT process tasks one by one
- DO NOT wait for one decomposer to finish before creating the next
- Create all `<subagent_task>` blocks together in ONE response
- Example: If batch has 5 tasks → create 5 decomposer subagents at once

**Process**:
1. Count tasks in batch that need decomposition (type == "module" or type == "page")
2. Output: "Creating [N] FrontendDecomposer subagents in parallel..."
3. Create ALL decomposer subagent blocks in one response
4. Each decomposer works independently and saves to its own temp file

**Example - 5 tasks in batch**:
```
Batch tasks needing decomposition: 5
Creating 5 FrontendDecomposer subagents in parallel...

<subagent_task>
Agent: @frontend-decomposer
Input: frontend_task_001 (module)
...
</subagent_task>

<subagent_task>
Agent: @frontend-decomposer
Input: frontend_task_002 (page)
...
</subagent_task>

<subagent_task>
Agent: @frontend-decomposer
Input: frontend_task_003 (page)
...
</subagent_task>

<subagent_task>
Agent: @frontend-decomposer
Input: frontend_task_004 (page)
...
</subagent_task>

<subagent_task>
Agent: @frontend-decomposer
Input: frontend_task_005 (module)
...
</subagent_task>

[All 5 decomposers work in parallel]
```

**For each task that needs decomposition, create this subagent**:
```
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

Output format: Save to `.claude_tasks/frontend_decomposition_temp/frontend_task_XXX.json`

**CRITICAL - Save to temporary file, do NOT return large JSON**:
```json
{
  "parent_task_id": "frontend_task_XXX",
  "parent_type": "module|page",
  "subtasks": [
    {
      "title": "ComponentName",
      "level": 3,
      "type": "component|page",
      "component_type": "container|presentational|form|etc",
      "props": ["prop1", "prop2"],
      "state": ["state1", "state2"],
      "hooks": ["useState", "useEffect"],
      "api_calls": ["GET /api/users"],
      "design_reference": "designs/wireframes/page.md"
    }
  ],
  "summary": {
    "total_subtasks": 8,
    "pages": 0,
    "components": 8
  }
}
```

**After saving file, output**: "✓ Saved frontend_task_XXX decomposition: 8 subtasks"
</subagent_task>
```

### 4. Wait for All Decomposers to Complete

**Wait for ALL decomposer subagents from step 3 to finish.**

**Verification**:
- Tasks needing decomposition: [N]
- Decomposer subagents created: [N]  ← must match
- ✓ All decomposers created simultaneously in one response

Each decomposer saves its results to:
- `.claude_tasks/frontend_decomposition_temp/frontend_task_XXX.json`

### 5. Integrate All Decomposition Results

After all decomposers complete:

#### 5.1 Read All Temporary Files
Read all files from `.claude_tasks/frontend_decomposition_temp/frontend_task_*.json`

#### 5.2 Assign Task IDs
For each subtask across all decomposition files:
1. Get current max task ID from task_registry.json (e.g., frontend_task_025)
2. Assign sequential IDs to new tasks:
   - frontend_task_026, frontend_task_027, ...
3. Build ID mapping: temp references → actual IDs

#### 5.3 Merge into task_registry.json
For each decomposition result:
1. **Add subtasks to `tasks` object**:
   - Use assigned IDs from step 5.2
   - Set `parent_id` to the decomposed task
   - Set `status` based on type:
     * `type == "component"` → status = "ready"
     * `type == "page"` → status = "pending"
   - Set `category` = "frontend"
   - Include all metadata (props, state, hooks, etc.)

2. **Update parent task**:
   - Set parent's `status` = "decomposed"
   - Set parent's `children` = [array of new task IDs]

3. **Update metadata counters**:
   - Increment `frontend_metadata.total_pages` by pages count
   - Increment `frontend_metadata.total_components` by components count

Example merged result:
```json
{
  "tasks": {
    "frontend_task_001": {
      "status": "decomposed",
      "children": ["frontend_task_026", "frontend_task_027", "frontend_task_028"]
    },
    "frontend_task_026": {
      "id": "frontend_task_026",
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
    "total_pages": 15,
    "total_components": 48
  }
}
```

#### 5.4 Temporary File Cleanup Responsibility
**The deletion of temporary files (.claude_tasks/frontend_decomposition_temp/frontend_task_*.json) MUST be performed by you only after confirming that all tasks have been successfully merged into task_registry.json. The Python integration script MUST NOT delete temporary files directly.**

### 6. Invoke Context Generator for Component Tasks (Parallel)

**After step 5 integration completes**, invoke context generators.

**CRITICAL - ONLY FOR LEVEL 3 IMPLEMENTATION TASKS**:
- Context generation is ONLY for Level 3 implementation tasks (`type == "component"`)
- DO NOT generate contexts for Level 2 page integration tasks (they dynamically fetch child states)
- DO NOT generate contexts for Level 1 module integration tasks (they dynamically fetch child states)
- Integration tasks will get their "context" at execution time from child task states

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
3. **MANDATORY PARALLEL EXECUTION WITHIN EACH SUB-BATCH**:
   - Within each sub-batch, you MUST create ALL subagents AT THE SAME TIME
   - DO NOT process sub-batch items one by one
   - DO NOT wait for one subagent to finish before starting the next
   - Create 10 `<subagent_task>` blocks simultaneously in one response
   - Example: For sub-batch of 10, output 10 subagent blocks together, not sequentially
4. Track progress: "Processing batch X of Y (10 components)..."
5. Verify completion: After ALL batches, confirm total = component_count

**Example - 25 component tasks**:
```
Total component tasks: 25
Sub-batches needed: 3 (10 + 10 + 5)

Processing sub-batch 1 of 3 (10 components)...
  Creating ALL 10 ContextGenerator subagents SIMULTANEOUSLY:
  
  <subagent_task>Agent: @context-generator (frontend_task_008 - LoginForm)</subagent_task>
  <subagent_task>Agent: @context-generator (frontend_task_009 - EmailInput)</subagent_task>
  <subagent_task>Agent: @context-generator (frontend_task_010 - PasswordInput)</subagent_task>
  ... [ALL 10 subagent blocks in ONE response]
  
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
- ❌ "Processing component 1... Processing component 2..." (串行执行)
- ❌ "Let me continue with component X" (one-by-one 处理)
- ✅ REQUIRED: "Creating ALL 10 subagents simultaneously in one response"
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

**CRITICAL - PARALLEL EXECUTION FORMAT**:
- For each sub-batch, create ALL subagent_task blocks in ONE response
- DO NOT create subagents one-by-one across multiple responses
- Output 10 `<subagent_task>` blocks together, then wait for all to complete

```
For each sub-batch of up to 10 component tasks (create ALL simultaneously):

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
**Wait for ALL sub-batches to complete before proceeding to step 7.**

### 7. Update Checkpoint
Save progress after each batch:
- Update `state.json` with latest checkpoint
- Save `task_registry.json` with all new tasks

### 8. Check Completion
If all tasks are at component level (type == "component"):
- Set `decomposition_phase.frontend_status = "completed"`
- Output completion message

### 9. Output Summary
```
=== Decomposition Phase: {current_phase} ===
Resuming from checkpoint: frontend_task_XXX

Processing frontend batch (5-10 tasks)...

=== Decomposition Phase (Parallel) ===
Tasks needing decomposition: 3
Creating 3 FrontendDecomposer subagents in parallel...

frontend_task_001 (Module: Authentication):
  ✓ Decomposed into 3 pages
  
frontend_task_002 (Page: Login):
  ✓ Analyzed wireframe: designs/wireframes/login-page.md
  ✓ Saved to: .claude_tasks/frontend_decomposition_temp/frontend_task_002.json
  ✓ Identified 8 components

=== Integration Phase (Python Script) ===
Generated: .claude_tasks/integrate_frontend_tasks.py
Executing integration script...

✓ Integrated frontend_task_001.json: 3 subtasks
✓ Integrated frontend_task_002.json: 8 subtasks
✓ Integrated frontend_task_003.json: 5 subtasks

=== Integration Summary ===
Total new tasks: 16
New pages: 3
New components: 13
Updated task_registry.json
Archived 3 temp files

Next available ID: frontend_task_042

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
