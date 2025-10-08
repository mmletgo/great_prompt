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

### 2. Analyze Batch Tasks (NO EXECUTION)

**CRITICAL - THIS IS ANALYSIS ONLY, DO NOT CREATE ANY TASKS IN THIS STEP**:
- Review each task in the batch to understand its type and requirements
- All actual task creation happens in step 3 (subagent parallel execution)
- DO NOT call add_subtask() or add_subtasks_batch() in this step
- DO NOT create any subagent_task blocks in this step
- This step is for planning and understanding what the decomposer subagents will do

**Understanding task decomposition requirements**:
- Level 1 (module) → must decompose to Level 2 (pages)
- Level 2 (page) → must decompose to Level 3 (components)
- Level 3 (component) → already at leaf level, mark as "ready"

**Task type analysis (for planning subagent work)**:

#### If task.type == "component" (Level 3):
- Already at leaf level
- Will be marked as "ready" (no decomposition needed)
- Context files will be generated later by `/generate-frontend-contexts`

#### If task.type == "module" (Level 1):
- Needs decomposition to Page level (Level 2)
- Subagent will analyze module and create page tasks
- Each page gets dot notation ID: parent="1" → pages="1.1", "1.2", etc.
- Each page references its wireframe file
- Parent status will change: pending → decomposed

#### If task.type == "page" (Level 2):
- Needs decomposition to Component level (Level 3)
- Subagent will analyze wireframe and create component tasks
- Each component gets dot notation ID: parent="1.1" → components="1.1.1", "1.1.2", etc.
- Must create tasks for EVERY component:
  - Page container component (always required)
  - Section components (header, main, sidebar, footer)
  - Shared/reusable components (buttons, inputs, cards)
  - State management components (if needed)
  - API integration components (if needed)
- A "simple" page still has minimum 5-10 components
- Parent status will change: pending → decomposed

### 3. Invoke FrontendDecomposer Subagents (Parallel)

**THIS IS WHERE ACTUAL EXECUTION HAPPENS**:
- Step 2 was analysis only
- Step 3 is where you create ALL decomposer subagents simultaneously
- This is the ONLY step where you create <subagent_task> blocks

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

#### 5.2 Integrate Using Python Script (Tree Structure)

**CRITICAL - Call the pre-built integration script**:

Run the integration script from `.claude/scripts/` directory:

```bash
cd .claude/scripts
python integrate_decomposition.py --category frontend
```

**What the script does automatically**:
1. Reads all files from `.claude_tasks/frontend_decomposition_temp/*.json`
2. For each decomposition file:
   - Calls `TaskRegistryManager.add_subtasks_batch(parent_id, subtasks)`
   - Automatically assigns dot notation IDs (e.g., "1.1", "1.1.1")
   - Sets parent_id correctly for all subtasks
   - Updates parent status to "decomposed"
   - Maintains hierarchical tree relationships
3. Validates tree structure integrity
4. Archives processed files to `.claude_tasks/frontend_decomposition_archive/`
5. Prints integration summary with task counts

**Expected output**:
```
=== Integration Phase (Python API) ===
Using TaskRegistryManager.add_subtasks_batch() to maintain tree structure...

Integrating frontend_task_001.json:
  Parent: "1" (Module: Authentication)
  ✓ Created 3 subtasks with IDs: 1.1, 1.2, 1.3
  ✓ Parent status: pending → decomposed
  ✓ Tree structure validated

Integrating frontend_task_002.json:
  Parent: "1.1" (Page: Login)
  ✓ Created 8 subtasks with IDs: 1.1.1, 1.1.2, ..., 1.1.8
  ✓ Parent status: pending → decomposed
  ✓ Tree structure validated

=== Integration Summary ===
Total new tasks: 11
By type: 8 components (ready), 3 pages (pending)
Tree hierarchy maintained with dot notation IDs
Archived 2 temp files
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
=== Decomposition Phase: {current_phase} ===
Resuming from checkpoint: frontend_task_XXX

Processing frontend batch (5-10 tasks)...

=== Decomposition Phase (Parallel) ===
Tasks needing decomposition: 3
Creating 3 FrontendDecomposer subagents in parallel...

frontend_task_001 (Module: Authentication):
  ✓ Analyzed wireframes
  ✓ Saved to: .claude_tasks/frontend_decomposition_temp/frontend_task_001.json
  ✓ Identified 3 pages
  
frontend_task_002 (Page: Login):
  ✓ Analyzed wireframe: designs/wireframes/login-page.md
  ✓ Saved to: .claude_tasks/frontend_decomposition_temp/frontend_task_002.json
  ✓ Identified 8 components

frontend_task_003 (Page: Signup):
  ✓ Analyzed wireframe: designs/wireframes/signup-page.md
  ✓ Saved to: .claude_tasks/frontend_decomposition_temp/frontend_task_003.json
  ✓ Identified 5 components

=== Integration Phase ===
Running: python integrate_decomposition.py --category frontend

[Script output will appear here showing integration progress]

✓ Processed [N] tasks in this batch
✓ [X] components ready (status="ready")
✓ [Y] pages need further decomposition (status="pending")

Updated checkpoint: frontend_task_XXX
Frontend decomposition: [in_progress | completed]

Next command: [/continue-decompose-frontend OR /generate-frontend-contexts OR /init-decompose-backend]
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
