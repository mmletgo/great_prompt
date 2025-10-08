---
description: Execute parallel fullstack development with TDD
argument-hint: [workers]
---

# Execute Parallel Fullstack Development

## Your Task
Execute all frontend and backend tasks in parallel following the dependency graph.

## Prerequisites
- Fullstack dependency graph exists in task_registry.json
- Design artifacts available (wireframes, user flows)

## File Format References
This command reads and updates two central JSON files:
- **📄 [state.json Template](../.claude/templates/state.json.template)** - Global state tracking
- **📄 [task_registry.json Template](../.claude/templates/task_registry.json.template)** - Task definitions and dependencies

Refer to these templates for complete field definitions and usage examples.

## Steps

### 1. Load Configuration and Check State

#### 1.1 Load Task Registry
Read execution_order from task_registry.json.
Parse workers argument (default: 5).

#### 1.2 Check Existing State
Check if `.claude_tasks/state.json` exists:
- If exists: Resume from last completed wave
- If not exists: Start from Wave 1

**📄 State File Format**: See [state.json Template](../.claude/templates/state.json.template) for complete structure.

**Key fields used**:
- `development_phase.status`: "not_started" | "in_progress" | "completed"
- `development_phase.current_wave`: Current wave number
- `development_phase.completed_waves`: Number of completed waves
- `development_phase.completed_tasks`: Array of completed task IDs
- `development_phase.failed_tasks`: Array of failed task IDs
- `development_phase.workers`: Worker pool size
- `development_phase.wave_progress[N]`: Per-wave execution details

#### 1.3 Resume Logic
If resuming (state.json exists and development_phase.status == "in_progress"):
- Read `development_phase.current_wave` and `development_phase.completed_waves`
- Output: "🔄 Resuming from Wave {current_wave} (Waves 1-{completed_waves} already complete)"
- Output: "📊 Progress: {completed_tasks.length} tasks completed, {failed_tasks.length} failed"
- Skip completed waves (waves 1 to completed_waves)
- For current wave in progress:
  - Check task_registry.json for tasks with status="completed" in this wave
  - Read `wave_progress[current_wave].current_batch` to determine batch position
  - Only process remaining batches in current wave
  - Continue from first incomplete batch

If starting fresh (state.json doesn't exist or development_phase.status == "not_started"):
- Output: "🚀 Starting fullstack development from Wave 1"
- Initialize state.json with development_phase structure
- Set `development_phase.status = "in_progress"`
- Set `development_phase.current_wave = 1`
- Set `development_phase.completed_waves = 0`
- Start from Wave 1, Batch 1

### 2. Process Each Wave (Serial Waves, Parallel Batches)

**Wave Execution Model**:
- Waves are executed SERIALLY (one wave at a time, respecting dependencies)
- Within each wave, tasks are divided into BATCHES
- Batch size = worker count (e.g., workers=5 means 5 tasks per batch)
- Batches execute SERIALLY (one batch at a time within wave)
- Tasks within a batch execute in PARALLEL
- Wait for current batch to complete before creating next batch
- Wait for current wave to complete before starting next wave

For each wave in execution_order:

#### 2.1 Identify Wave Category
Determine task types in current wave:
- Backend tasks: Use @backend-developer
- Frontend tasks: Use @frontend-developer
- Mixed wave: Use appropriate developer for each task type

#### 2.2 Create Developer Subagents for Wave

**State Management via Python Scripts**:
After EACH subagent task completes, use Python scripts to update state:

**📄 Script Reference**: See [.claude/scripts/README.md](../.claude/scripts/README.md) for complete API documentation.

**For Successful Task Completion**:
```python
from utils import ProjectManager

manager = ProjectManager()
manager.complete_task_full(
    task_id="FE_auth_LoginForm",  # Task ID from task_registry.json
    implementation_file="src/components/auth/LoginForm.tsx",
    test_file="src/components/auth/LoginForm.test.tsx",
    test_coverage=95,  # Percentage
    duration_minutes=12.5
)
```

**For Failed Task**:
```python
from utils import ProjectManager

manager = ProjectManager()
manager.fail_task_full(
    task_id="FE_auth_LoginForm",
    error="Test coverage below 80% threshold"
)
```

This automatically updates both:
- `task_registry.json`: Task status, files, coverage, duration
- `state.json`: Adds task_id to completed_tasks or failed_tasks array

#### 2.3 Batch Completion
After each batch completes, update batch progress:

```python
from utils import ProjectManager

manager = ProjectManager()

# After batch completes
completed = ["FE_auth_LoginForm", "FE_auth_RegisterForm", "FE_auth_PasswordReset"]
failed = []  # Task IDs that failed in this batch

manager.complete_batch(
    wave_number=3,
    completed_tasks=completed,
    failed_tasks=failed
)
```

This updates `state.json`:
- Increments `wave_progress[N].completed` counter
- Increments `wave_progress[N].current_batch` counter

**CRITICAL - BATCH EXECUTION WITHIN WAVE**:
- Divide wave tasks into batches of size = worker count
- Process batches SERIALLY (one batch at a time)
- Within each batch, create ALL `<subagent_task>` blocks in ONE response
- Wait for current batch to complete before creating next batch
- Continue until ALL tasks in wave are processed (100% wave coverage)

**Execution Rules**:
1. Count tasks in wave: `wave_task_count = tasks in current wave`
2. Calculate batches: `num_batches = ceil(wave_task_count / workers)`
3. **Process batches SERIALLY**:
   - Batch 1: Create `workers` subagent blocks in ONE response
   - Wait for Batch 1 to complete
   - Batch 2: Create next `workers` subagent blocks in ONE response
   - Wait for Batch 2 to complete
   - Continue until all batches complete
4. Proceed to next wave

**CRITICAL - How to Create Parallel Subagents in Batches**:

For a wave with 10 tasks and workers=5, you create 2 batches:

```
Wave 3: Backend Service Layer (10 tasks, workers=5)
Calculated: 10 / 5 = 2 batches

Batch 1/2: Creating 5 developer subagents SIMULTANEOUSLY:

<subagent_task>
Agent: @backend-developer
Input: backend_task_020
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_021
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_022
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_023
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_024
[... full task details ...]
</subagent_task>

[Wait for ALL 5 subagents in Batch 1 to complete]

✓ Batch 1/2 complete: 5/5 tasks finished

Batch 2/2: Creating 5 developer subagents SIMULTANEOUSLY:

<subagent_task>
Agent: @backend-developer
Input: backend_task_025
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_026
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_027
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_028
[... full task details ...]
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input: backend_task_029
[... full task details ...]
</subagent_task>

[Wait for ALL 5 subagents in Batch 2 to complete]

✓ Batch 2/2 complete: 5/5 tasks finished
```

**CRITICAL**: 
- Batch 1: Create 5 `<subagent_task>` blocks in ONE response, then WAIT
- Batch 2: After Batch 1 completes, create next 5 blocks in ONE response
- DO NOT create all 10 subagents at once
- DO NOT create subagents one by one
- Each batch's blocks must be in the SAME response
- Process batches SERIALLY, not in parallel

**Example - Wave 3 has 27 tasks, workers=5**:
```
Wave 3: Backend Service Layer (27 tasks, workers=5)
Calculated: ceil(27 / 5) = 6 batches

Batch 1/6: Creating 5 developer subagents:

<subagent_task>
Agent: @backend-developer
Input:
- Task ID: backend_task_020
- Context: .claude_tasks/contexts/backend_task_020_context.md
Task: Implement validateUserCredentials function with TDD
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input:
- Task ID: backend_task_021
- Context: .claude_tasks/contexts/backend_task_021_context.md
Task: Implement hashPassword function with TDD
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input:
- Task ID: backend_task_022
- Context: .claude_tasks/contexts/backend_task_022_context.md
Task: Implement generateJWT function with TDD
</subagent_task>

<subagent_task>
Agent: @backend-developer
Input:
- Task ID: backend_task_024
- Context: .claude_tasks/contexts/backend_task_024_context.md
Task: Implement generateRefreshToken function with TDD
</subagent_task>

[Wait for ALL 5 subagents in Batch 1 to complete]

**Update State After Batch 1**:
```python
from utils import ProjectManager
manager = ProjectManager()
manager.complete_batch(
    wave_number=3,
    completed_tasks=["backend_task_020", "backend_task_021", "backend_task_022", "backend_task_023", "backend_task_024"],
    failed_tasks=[]  # Add any failed task IDs here
)
```

✓ Batch 1/6 complete: 5/5 tasks (backend_task_020-024)

Batch 2/6: Creating 5 developer subagents:
[5 <subagent_task> blocks for backend_task_025-029]

[Wait for Batch 2 to complete]

**Update State After Batch 2**:
```python
manager.complete_batch(
    wave_number=3,
    completed_tasks=["backend_task_025", "backend_task_026", "backend_task_027", "backend_task_028", "backend_task_029"],
    failed_tasks=[]
)
```

✓ Batch 2/6 complete: 5/5 tasks (backend_task_025-029)

Batch 3/6: Creating 5 developer subagents:
[5 <subagent_task> blocks for backend_task_030-034]

[Wait for Batch 3 to complete]
✓ Batch 3/6 complete: 5/5 tasks (backend_task_030-034)

Batch 4/6: Creating 5 developer subagents:
[5 <subagent_task> blocks for backend_task_035-039]

[Wait for Batch 4 to complete]
✓ Batch 4/6 complete: 5/5 tasks (backend_task_035-039)

Batch 5/6: Creating 5 developer subagents:
[5 <subagent_task> blocks for backend_task_040-044]

[Wait for Batch 5 to complete]
✓ Batch 5/6 complete: 5/5 tasks (backend_task_040-044)

Batch 6/6: Creating 2 developer subagents:
[2 <subagent_task> blocks for backend_task_045-046]

[Wait for Batch 6 to complete]

**Update State After Batch 6**:
```python
manager.complete_batch(
    wave_number=3,
    completed_tasks=["backend_task_045", "backend_task_046"],
    failed_tasks=[]
)
```

✓ Batch 6/6 complete: 2/2 tasks (backend_task_045-046)

**Complete Wave 3**:
```python
result = manager.complete_wave_full(wave_number=3)
if result['success']:
    print(f"✓ Wave 3 complete: {result['completed']}/{result['total_tasks']} tasks")
else:
    print(f"❌ Wave 3 incomplete: {result['incomplete_tasks']}")
```

✓ Wave 3 complete: 27/27 tasks across 6 batches (100% coverage)

[Now proceed to Wave 4]
```

**FORBIDDEN - INCORRECT EXECUTION PATTERNS**:
- ❌ "Creating ALL wave tasks at once" (should be batched by worker count)
- ❌ "Creating tasks one by one" (should create batch_size tasks together)
- ❌ "Creating one subagent per batch" (batch should have worker_count subagents)
- ❌ "Processing next batch before current batch completes" (batches must be serial)
- ❌ "Proceeding to next wave before current wave completes" (breaks dependencies)
- ❌ "Skipping tasks in a wave" (incomplete coverage)
- ❌ Example of WRONG pattern (creating all 27 at once):
  ```
  Wave 3: Creating ALL 27 subagents:
  [27 <subagent_task> blocks]
  [This ignores batch concept!]
  ```
- ❌ Example of WRONG pattern (one by one):
  ```
  <subagent_task>Agent: @backend-developer (task_020)</subagent_task>
  [wait] <subagent_task>Agent: @backend-developer (task_021)</subagent_task>
  [This is too slow!]
  ```
- ✅ REQUIRED: Divide wave into batches of size = worker count
- ✅ REQUIRED: Create batch_size `<subagent_task>` blocks in ONE response
- ✅ REQUIRED: Wait for current batch to complete before next batch
- ✅ REQUIRED: Process all batches until wave complete (100% coverage)

**Verification Required**:
1. **At startup**:
   - Use Python script to check resume status:
     ```python
     from utils import ProjectManager
     manager = ProjectManager()
     status = manager.check_resume_status()
     if status['can_resume']:
         print(f"🔄 Resuming from wave {status['current_wave']}")
     else:
         print("🚀 Starting fresh")
     ```
   - Skip waves 1 to completed_waves if resuming

2. For each wave:
   - Count tasks: `wave_task_count = tasks in wave [N]`
   - Calculate batches: `num_batches = ceil(wave_task_count / workers)`
   - Output: "Wave [N]: {wave_task_count} tasks, workers={workers}, {num_batches} batches"
   - Initialize wave:
     ```python
     manager.start_wave(
         wave_number=N,
         category="backend",  # or "frontend" or "mixed"
         total_tasks=wave_task_count,
         total_batches=num_batches
     )
     ```

3. For each batch in wave:
   - Calculate batch size: `batch_size = min(workers, remaining_tasks)`
   - Output: "Batch {i}/{num_batches}: Creating {batch_size} developer subagents:"
   - **Create {batch_size} complete `<subagent_task>` blocks in ONE response**
   - Each block must be complete with full task details
   - ALL {batch_size} blocks must be in the SAME response
   - Wait for ALL subagents in current batch to complete
   - **After each task completes, use Python script** (shown in section 2.2)
   - **After batch completes, use Python script**:
     ```python
     manager.complete_batch(
         wave_number=N,
         completed_tasks=[list of completed task IDs],
         failed_tasks=[list of failed task IDs]
     )
     ```
   - Confirm: "✓ Batch {i}/{num_batches} complete: {batch_size}/{batch_size} tasks"
   - Confirm: "💾 State saved: {completed} total tasks completed"

4. After all batches in wave:
   - **Use Python script to complete wave**:
     ```python
     result = manager.complete_wave_full(wave_number=N)
     if result['success']:
         print(f"✓ Wave {N} complete: {result['completed']}/{result['total_tasks']} tasks")
     else:
         print(f"❌ Wave {N} has incomplete tasks: {result['incomplete_tasks']}")
     ```
   - Confirm: "✓ Wave [N] complete: {wave_task_count}/{wave_task_count} tasks across {num_batches} batches (100% coverage)"
   - Confirm: "💾 Wave [N] saved to state.json"

5. Proceed to next wave

**For backend tasks:**
```
<subagent_task>
Agent: @backend-developer
Input:
- Task ID: backend_XXX
- Context file: .claude_tasks/contexts/backend_task_XXX_context.md
- Task type: [API/Service/Repository/Validation/Utility]
- Dependencies: [list of completed dependency task IDs]
- PRD reference: docs/prd.md
- Architecture: docs/fullstack-architecture.md

Task:
Execute TDD workflow for this backend function:

1. RED Phase:
   - Read context file for function specification
   - Write comprehensive test cases (pytest/jest)
   - Tests should fail initially
   - Cover: happy path, edge cases, error handling
   - For API layer: include integration tests
   - For Repository layer: include database mocks

2. GREEN Phase:
   - Implement the function to pass all tests
   - Follow clean architecture principles
   - Respect layer boundaries (API → Service → Repository)
   - Use type hints/TypeScript types
   - Handle errors appropriately

3. REFACTOR Phase:
   - Optimize code quality
   - Add comprehensive docstrings/comments
   - Ensure proper error handling
   - Verify all tests still pass
   - For APIs: generate OpenAPI/Swagger docs

Output format:
- Implementation file: [path from context]
- Test file: [test path from context]
- Coverage report: indicate test coverage %
- API documentation (if API layer)

Success criteria:
✓ All tests pass
✓ Code follows project conventions
✓ Proper error handling
✓ Documentation complete
</subagent_task>
```

**For frontend tasks:**
```
<subagent_task>
Agent: @frontend-developer
Input:
- Task ID: frontend_XXX
- Context file: .claude_tasks/contexts/frontend_task_XXX_context.md
- Task type: [Page/Component]
- Design reference: designs/wireframes/[page].md
- Dependencies: [list of completed dependency task IDs]
- UX spec: docs/front-end-spec.md

Task:
Execute TDD workflow for this frontend component:

1. RED Phase:
   - Read context file for component specification
   - Read wireframe for visual design
   - Write component tests (testing-library/jest)
   - Tests should fail initially
   - Test: rendering, user interactions, state changes, API calls

2. GREEN Phase:
   - Implement React/Vue component
   - Match wireframe design
   - Implement all interactive behaviors
   - Handle all component states (loading, error, success, empty)
   - Integrate with API endpoints (if applicable)
   - Follow design system from front-end-spec.md

3. REFACTOR Phase:
   - Optimize component structure
   - Add accessibility attributes (ARIA labels, etc.)
   - Ensure responsive design
   - Add PropTypes/TypeScript types
   - Verify against wireframe

4. VERIFY Phase:
   - All tests pass
   - Visual matches wireframe
   - Interactions work correctly
   - Accessible (keyboard nav, screen readers)

Output format:
- Component file: [path from context]
- Test file: [test path from context]
- Storybook story (optional): [story path]
- Coverage report: indicate test coverage %

Success criteria:
✓ All tests pass
✓ Matches wireframe design
✓ Proper state management
✓ Accessibility compliant
✓ Responsive design
</subagent_task>
```

#### 2.3 Execute Batches Within Wave

**Batch Execution Model**:
- Within each batch, ALL tasks execute in PARALLEL
- Worker pool controls concurrent execution (e.g., workers=5 means 5 tasks run simultaneously)
- Remaining tasks in batch are queued and execute as workers become available
- Wait for ALL tasks in current batch to complete before starting next batch
- This provides manageable parallelism while ensuring progress tracking

**Execution Flow Example** (Wave with 27 tasks, workers=5):
```
Batch 1: 10 tasks created simultaneously
  Worker Pool Status:
    [Slot 1] backend_task_020 - Running (2.3 min)
    [Slot 2] backend_task_021 - Running (2.1 min)
    [Slot 3] backend_task_022 - Running (1.8 min)
    [Slot 4] backend_task_023 - Running (2.5 min)
    [Slot 5] backend_task_024 - Running (2.0 min)
    [Queue]  backend_task_025, 026, 027, 028, 029
    
  As tasks complete, queued tasks fill empty slots:
    ✓ backend_task_022 completed (1.8 min)
    [Slot 3] backend_task_025 - Running (now fills slot 3)
    
    ✓ backend_task_021 completed (2.1 min)
    [Slot 2] backend_task_026 - Running (now fills slot 2)
    
  ... continue until all 10 tasks complete
  
✓ Batch 1 complete: 10/10 tasks

[Now start Batch 2, not before]

Batch 2: 10 tasks created simultaneously
  ... same execution pattern
  
✓ Batch 2 complete: 10/10 tasks

Batch 3: 7 tasks created simultaneously
  ... same execution pattern
  
✓ Batch 3 complete: 7/7 tasks

✓ Wave complete: 27/27 tasks
```

#### 2.4 Verify Batch Results and Update State

After each batch completes:

**Verify Results**:
- ✓ Check all tests pass for tasks in batch
- ✓ Verify implementations match specifications
- ✓ For frontend: verify against wireframes
- ✓ For backend API: verify OpenAPI docs generated
- ✓ Confirm no breaking changes to dependencies

**Update Task Status**:
For each task in batch, update task_registry.json:
- Set `status = "completed"` or `"failed"`
- Add `completed_at` timestamp (ISO 8601)
- Add `duration_minutes`, `test_coverage` percentage
- Add `implementation_file`, `test_file` paths
- Add `error` message if failed

**Update State Progress**:
After batch verification, update state.json:
- Append completed task IDs to `development_phase.completed_tasks` array
- Append failed task IDs to `development_phase.failed_tasks` array
- Increment `development_phase.wave_progress[N].completed` by batch_size
- Increment `development_phase.wave_progress[N].current_batch`
- Update `metadata.last_updated` timestamp

**📄 See**: [task_registry.json Template](../.claude/templates/task_registry.json.template#update-task-status-after-completion) and [state.json Template](../.claude/templates/state.json.template#development_phase) for complete field definitions.

#### 2.5 Update Progress After Wave

After all batches in wave complete:

**Update Wave Status**:
Update state.json development_phase:
- Increment `completed_waves` (from N to N+1)
- Increment `current_wave` (from N to N+1)
- Set `wave_progress[N].status = "completed"`
- Add `wave_progress[N].completed_at` timestamp
- Add `wave_progress[N].duration_minutes`
- Initialize `wave_progress[N+1]` with status="pending"
- Update `metadata.last_updated` timestamp

**📄 See**: [state.json Template](../.claude/templates/state.json.template#wave_progress-per-wave) for wave_progress field definitions.

**Save and Log**:
- Save task_registry.json with all task statuses
- Save state.json with development_phase.completed_waves updated
- Output: "✅ Wave 3 complete and saved to state.json"
- Output: "📊 Progress: {development_phase.completed_tasks.length} tasks completed, {development_phase.failed_tasks.length} failed"
- Output: "⏭️  Ready to proceed to Wave 4"
- Proceed to next wave

### 3. Cross-Stack Integration Validation

After all waves complete, verify cross-stack integration:

#### 3.1 API Contract Validation
For each frontend → backend dependency:
```
Frontend component: frontend_008 (LoginForm)
  → Calls: POST /api/auth/login
Backend endpoint: backend_009 (login_api)
  → Implements: POST /api/auth/login

Verify:
✓ Endpoint path matches
✓ Request body structure matches
✓ Response structure matches
✓ Error responses handled
✓ Authentication/authorization correct
```

#### 3.2 Component Integration Check
- Verify shared components used correctly
- Check parent-child component relationships
- Validate state management flow
- Confirm routing/navigation works

#### 3.3 Generate Integration Report
Create `.claude_tasks/integration_report.md`:
```markdown
# Cross-Stack Integration Report

## API Integrations Verified
1. LoginForm → POST /api/auth/login ✓
2. ProfileEditor → GET /api/users/:id ✓
3. ProductCard → GET /api/products ✓
...

## Component Dependencies
- Button (shared) ← Used by 15 components ✓
- Form (shared) ← Used by 8 components ✓
...

## Issues Found
- [List any integration issues]

## Recommendations
- [Integration improvements]
```

### 4. Optional: End-to-End User Flow Tests

After cross-stack integration validation, optionally create E2E tests:

```
<subagent_task>
Agent: @integration-tester (optional custom agent)
Input:
- User flows: designs/user-flows.md
- Completed frontend components: [list]
- Completed backend endpoints: [list]
- Wireframes: designs/wireframes/

Task:
Create end-to-end tests for each user flow:

1. Browse Products Flow:
   - Test: Navigate to product list
   - Test: Apply filters
   - Test: View product details
   - Test: Add to cart
   - Verify: All API calls successful
   - Verify: UI updates correctly

2. Checkout Flow:
   - Test: View cart
   - Test: Update quantities
   - Test: Proceed to checkout
   - Test: Enter payment info
   - Test: Complete order
   - Verify: Order confirmation received

Output:
- E2E test suite (Cypress/Playwright)
- Test results report
</subagent_task>
```

### 5. Output Summary
```
=== Fullstack Parallel Development Summary ===

Session Info:
  Start mode: [Fresh start | Resumed from Wave N]
  State file: state.json [Created | Updated]
  Task registry: task_registry.json [Updated]

Design Phase:
  User flows: ✓ designs/user-flows.md
  Wireframes: ✓ designs/wireframes/ ([N] pages)

Backend Development:
  Total functions: [N]
  ✓ Completed: [N]
  ✗ Failed: [0]
  
  By Layer:
  - API Layer: [X] functions ✓
  - Service Layer: [Y] functions ✓
  - Repository Layer: [Z] functions ✓
  - Validation Layer: [W] functions ✓
  - Utility Layer: [V] functions ✓
  
Frontend Development:
  Total components: [M]
  ✓ Completed: [M]
  ✗ Failed: [0]
  
  By Type:
  - Pages: [A] components ✓
  - Shared Components: [B] components ✓
  - Feature Components: [C] components ✓

Execution Timeline:
  Wave 1 (Backend Utils + Shared Components): [N] tasks
    - Batches: [B] batches (size = workers)
    - Batch 1: {batch_size}/{batch_size} tasks ✓ (state saved)
    - Batch 2: {batch_size}/{batch_size} tasks ✓ (state saved)
    - ... (all batches)
    ✓ Wave 1 complete: [N]/[N] (100% coverage)
    💾 Wave 1 saved to state.json
    
  Wave 2 (Backend Repositories): [M] tasks
    - Batches: [B] batches
    - Batch processing details...
    ✓ Wave 2 complete: [M]/[M] (100% coverage)
    
  Wave 3 (Backend Services): [K] tasks
    - Batches: [B] batches
    - Batch 1: 10/10 tasks ✓
    - Batch 2: 10/10 tasks ✓
    - Batch 3: 7/7 tasks ✓
    ✓ Wave 3 complete: [K]/[K] (100% coverage)
    
  Wave 4 (Backend APIs): [L] tasks
    - Batches and completion details...
    ✓ Wave 4 complete: [L]/[L] (100% coverage)
    
  Wave 5 (Frontend Basic Components): [P] tasks
    ✓ Wave 5 complete: [P]/[P] (100% coverage)
    
  Wave 6 (Frontend API Components): [Q] tasks
    ✓ Wave 6 complete: [Q]/[Q] (100% coverage)
    
  Wave 7 (Frontend Pages): [R] tasks
    ✓ Wave 7 complete: [R]/[R] (100% coverage)
    
  Wave 8 (Integration Tests): [S] tests
    ✓ Wave 8 complete: [S]/[S] (100% coverage)

✓ ALL WAVES: Serial execution with batched parallelism, 100% task coverage
✓ Total execution: [T] tasks across [M] waves
💾 Final state saved: state.json (development_phase.completed_waves: [M], status: "completed")
💾 All task statuses saved: task_registry.json

Cross-Stack Integration:
  ✓ API contracts validated: [N] integrations
  ✓ Component dependencies verified
  ✓ User flow coverage: 100%

Test Coverage:
  Backend: [X]% (target: >80%)
  Frontend: [Y]% (target: >80%)

Parallel Execution Verification:
  ✓ Waves executed serially (respecting dependencies)
  ✓ Batches within waves executed serially
  ✓ Tasks within batches executed in parallel
  ✓ Worker pool utilized efficiently (workers=[N])
  ✓ No tasks skipped, 100% coverage
  Total waves: [M]
  Total tasks: [T]
  Average wave size: [N] tasks
  Average batch size: ~10 tasks
  Execution model: Serial waves → Serial batches → Parallel tasks
  
Failed Tasks (if any):
  [List of failed tasks with reasons]

Next Steps:
  1. Review any failed tasks
  2. Run full test suite: npm test && pytest
  3. Start development servers
  4. Manual testing against wireframes
  5. Check integration_report.md
  6. Prepare for deployment
```

### 6. Generate Development Report
Create `DEVELOPMENT_REPORT.md`:
```markdown
### 6. Generate Development Report
Create `.claude_tasks/DEVELOPMENT_REPORT.md`:
```markdown
# Fullstack Development Report

Generated: [TIMESTAMP]

## Project Overview
- PRD: docs/prd.md
- Architecture: docs/fullstack-architecture.md
- User Flows: designs/user-flows.md
- Wireframes: designs/wireframes/ ([N] pages)

## Backend Summary

### Completed Endpoints
#### Authentication API
- POST /api/auth/login - User login
- POST /api/auth/register - User registration
- POST /api/auth/logout - User logout
- GET /api/auth/verify - Token verification

#### User API
- GET /api/users/:id - Get user profile
- PUT /api/users/:id - Update user profile
- DELETE /api/users/:id - Delete user account

#### [Other API Groups]
...

### Database Schema
#### Tables Created
- `users`: id, email, password_hash, created_at, updated_at
- `sessions`: id, user_id, token, expires_at
- `[other_tables]`: [schema]

### Service Layer Functions
- UserService: [N] functions
- AuthService: [M] functions
- [OtherServices]: [K] functions

### Test Coverage
- API Layer: [X]% coverage
- Service Layer: [Y]% coverage
- Repository Layer: [Z]% coverage
- Total Backend: [W]% coverage

## Frontend Summary

### Completed Pages
#### Authentication Pages
- Login Page (3 components)
  - LoginForm
  - SocialLoginButtons
  - LoginHeader
- Register Page (4 components)
  - RegisterForm
  - TermsCheckbox
  - PasswordStrengthIndicator
  - RegisterButton

#### Dashboard Pages
- Main Dashboard (8 components)
  - DashboardHeader
  - StatsCards
  - ActivityFeed
  - QuickActions
  - ...

### Component Library
#### Shared Components ([N] total)
- Button (Primary, Secondary, Text variants)
- Input (Text, Email, Password, Number)
- Card, Modal, Tooltip, Dropdown
- ...

#### Page-Specific Components ([M] total)
- [List by page]

### Design System Compliance
- ✓ All components follow front-end-spec.md
- ✓ Consistent naming conventions
- ✓ Responsive design (mobile, tablet, desktop)
- ✓ Accessibility (ARIA labels, keyboard nav)

### Test Coverage
- Component tests: [X]% coverage
- Integration tests: [Y] tests
- Total Frontend: [Z]% coverage

## Cross-Stack Integration

### API Integrations ([N] total)
1. LoginForm → POST /api/auth/login ✓
2. RegisterForm → POST /api/auth/register ✓
3. ProfileEditor → GET /api/users/:id ✓
4. ProfileEditor → PUT /api/users/:id ✓
...

### Verification Status
- ✓ All API contracts match
- ✓ Request/response schemas validated
- ✓ Error handling tested
- ✓ Authentication flows working

## Execution Metrics

### Development Timeline
- Total waves: [N]
- Total tasks: [M]
- Average wave time: [X] minutes
- Total development time: [Y] hours

### Parallel Efficiency
- Maximum parallelism: [N] tasks
- Average parallelism: [M] tasks
- Worker utilization: [X]%

## Test Results

### Backend Tests
- Total tests: [N]
- Passed: [M]
- Failed: [0]
- Coverage: [X]%

### Frontend Tests
- Total tests: [N]
- Passed: [M]
- Failed: [0]
- Coverage: [Y]%

### Integration Tests
- User flow tests: [N]
- API integration tests: [M]
- All tests: ✓ PASSED

## Known Issues

[List any failed tasks or issues]
- None / [Issue description]

## Deployment Checklist

### Backend
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] API documentation generated (Swagger/OpenAPI)
- [ ] Health check endpoint implemented
- [ ] Logging configured
- [ ] Error monitoring setup

### Frontend
- [ ] Build successful (npm run build)
- [ ] Environment variables configured
- [ ] API base URL configured
- [ ] Static assets optimized
- [ ] Service worker configured (if PWA)
- [ ] Analytics setup

### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing (if implemented)
- [ ] Manual testing completed

### Documentation
- [ ] API documentation complete
- [ ] Component documentation (Storybook)
- [ ] README updated
- [ ] Deployment guide ready

## Next Steps

1. **Code Review**
   - Review failed tasks (if any)
   - Check code quality
   - Verify test coverage

2. **Manual Testing**
   - Test all user flows against wireframes
   - Test responsive design
   - Test accessibility
   - Cross-browser testing

3. **Performance Testing**
   - API response times
   - Frontend rendering performance
   - Database query optimization

4. **Deployment Preparation**
   - Complete deployment checklist
   - Prepare production environment
   - Plan rollout strategy

5. **Monitoring Setup**
   - Application monitoring
   - Error tracking
   - Performance monitoring
   - User analytics
```

## Important Rules
- **CRITICAL**: Waves execute SERIALLY (one at a time, respecting dependencies)
- **RESUME CAPABILITY**: Check state.json.development_phase at startup, skip completed waves
- **BATCHING**: Within each wave, divide tasks into batches of size = workers
- **BATCH PARALLELISM**: Within each batch, ALL tasks execute in PARALLEL
- **BATCH COMPLETION**: Wait for current batch to complete before starting next batch
- **WAVE COMPLETION**: Wait for current wave to complete before starting next wave
- **STATE PERSISTENCE**: 
  - Update task_registry.json: set task.status after each task completes
  - Update state.json: append to development_phase.completed_tasks after each task
  - Update state.json: increment wave_progress counters after each batch
  - Update state.json: increment development_phase.completed_waves after each wave
- **Verify counts**: For each batch, tasks in batch = subagents created = tasks completed
- Use @backend-developer for all backend tasks (API, Service, Repository, Validation, Utility layers)
- Use @frontend-developer for all frontend tasks (Pages and Components)
- Dependencies are managed by execution_order (from build-deps-fullstack)
- Worker limit controls concurrent execution within each batch
- Save state after each wave completion
- Verify all tests pass before marking tasks complete
- Generate comprehensive cross-stack integration report
- Verify frontend components match wireframe designs
- Ensure all API contracts are validated
- Update task_registry.json after each wave
- Report 100% task coverage across all waves and batches
```

## Important Rules
- Backend APIs before dependent frontend components
- Follow dependency graph strictly
- Save state after each wave
- Generate comprehensive test coverage
- Create integration tests for user flows
- Verify frontend matches wireframes
