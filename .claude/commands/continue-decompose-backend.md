---
description: Continue backend task decomposition (next batch)
---

# Continue Backend Task Decomposition

## Your Task
Continue decomposing backend tasks to function/endpoint level.

## Prerequisites
- `decomposition_phase.status == "in_progress"`
- `decomposition_phase.backend_status == "in_progress"`

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

# Get all pending backend tasks
pending_tasks = task_mgr.get_tasks_by_status("pending", category="backend")

# Phase 1: Get Level 1 tasks (modules) that need decomposition
level1_tasks = [t for t in pending_tasks if t["level"] == 1]

if level1_tasks:
    # Still in Phase 1: decompose modules to services
    batch = level1_tasks[:10]  # Process up to 10 modules
    current_phase = "Level 1 → Level 2 (Module → Service)"
else:
    # Phase 1 complete, move to Phase 2: decompose services to functions
    level2_tasks = [t for t in pending_tasks if t["level"] == 2]
    batch = level2_tasks[:10]  # Process up to 10 services
    current_phase = "Level 2 → Level 3 (Service → Function)"
```

### 2. Analyze Batch Tasks (NO EXECUTION)

**CRITICAL - THIS IS ANALYSIS ONLY, DO NOT CREATE ANY TASKS IN THIS STEP**:
- Review each task in the batch to understand its type and requirements
- All actual task creation happens in step 3 (subagent parallel execution)
- DO NOT call add_subtask() or add_subtasks_batch() in this step
- DO NOT create any subagent_task blocks in this step
- This step is for planning and understanding what the decomposer subagents will do

**Understanding task decomposition requirements**:
- Level 1 (module) → must decompose to Level 2 (services)
- Level 2 (service) → must decompose to Level 3 (functions)
- Level 3 (function) → already at leaf level, mark as "ready"

**Task type analysis (for planning subagent work)**:

#### If task.type == "function" (Level 3):
- Already at leaf level
- Will be marked as "ready" (no decomposition needed)
- Context files will be generated later by `/generate-backend-contexts`

#### If task.type == "module" (Level 1):
- Needs decomposition to Service level (Level 2)
- Subagent will analyze module and create service tasks
- Each service gets dot notation ID: parent="1" → services="1.1", "1.2", etc.
- Parent status will change: pending → decomposed

#### If task.type == "service" (Level 2):
- Needs decomposition to Function level (Level 3)
- Subagent will analyze service and create function tasks
- Each function gets dot notation ID: parent="1.1" → functions="1.1.1", "1.1.2", etc.
- Must create tasks for ALL functions:
  - API endpoints (route handlers)
  - Service layer functions (business logic)
  - Data access functions (repository/ORM)
  - Validation functions
  - Utility functions
- A "simple" service still has minimum 5-10 functions
- Parent status will change: pending → decomposed

### 3. Invoke BackendDecomposer Subagents (Parallel)

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
1. Count tasks in batch that need decomposition (type == "module" or type == "service")
2. Output: "Creating [N] BackendDecomposer subagents in parallel..."
3. Create ALL decomposer subagent blocks in one response
4. Each decomposer works independently and saves to its own temp file

**Example - 4 tasks in batch**:
```
Batch tasks needing decomposition: 4
Creating 4 BackendDecomposer subagents in parallel...

<subagent_task>
Agent: @backend-decomposer
Input: backend_task_001 (module)
...
</subagent_task>

<subagent_task>
Agent: @backend-decomposer
Input: backend_task_002 (service)
...
</subagent_task>

<subagent_task>
Agent: @backend-decomposer
Input: backend_task_003 (service)
...
</subagent_task>

<subagent_task>
Agent: @backend-decomposer
Input: backend_task_004 (module)
...
</subagent_task>

[All 4 decomposers work in parallel]
```

**For each task that needs decomposition, create this subagent**:
```
<subagent_task>
Agent: @backend-decomposer
Input:
- Task ID: backend_task_XXX
- Task type: [module/service]
- API endpoints: from task metadata
- Database tables: from task metadata
- Architecture: docs/fullstack-architecture.md
- Frontend API calls: from frontend task registry

Task (if module):
1. Group related endpoints into services
2. Identify shared utilities
3. Create service-level tasks

Task (if service):
1. List all API endpoints for this service
2. For each endpoint, identify:
   - Route handler function
   - Request validation
   - Business logic functions
   - Data access functions
   - Response formatting
3. Identify database operations:
   - CRUD functions
   - Complex queries
   - Transactions
4. Identify middleware/decorators needed:
   - Authentication
   - Authorization
   - Rate limiting
   - Error handling

Output format: Save to `.claude_tasks/backend_decomposition_temp/backend_task_XXX.json`

**CRITICAL - Save to temporary file, do NOT return large JSON**:
```json
{
  "parent_task_id": "backend_task_XXX",
  "parent_type": "module|service",
  "subtasks": [
    {
      "title": "login_user",
      "level": 3,
      "type": "function|service",
      "function_type": "endpoint|service|repository|validator|util",
      "http_method": "POST",
      "route": "/api/auth/login",
      "function_signature": "async def login_user(credentials: LoginRequest) -> LoginResponse",
      "input_params": {
        "email": "string",
        "password": "string"
      },
      "return_type": "LoginResponse",
      "database_operations": ["SELECT from users", "INSERT into sessions"],
      "dependencies": ["validate_email", "hash_password", "generate_jwt"],
      "error_cases": ["InvalidCredentials", "AccountLocked"]
    }
  ],
  "summary": {
    "total_subtasks": 12,
    "services": 0,
    "functions": 12,
    "by_type": {
      "endpoint": 3,
      "service": 5,
      "repository": 2,
      "validator": 1,
      "util": 1
    }
  }
}
```

**After saving file, output**: "✓ Saved backend_task_XXX decomposition: 12 functions"
</subagent_task>
```

### 4. Wait for All Decomposers to Complete

**Wait for ALL decomposer subagents from step 3 to finish.**

**Verification**:
- Tasks needing decomposition: [N]
- Decomposer subagents created: [N]  ← must match
- ✓ All decomposers created simultaneously in one response

Each decomposer saves its results to:
- `.claude_tasks/backend_decomposition_temp/backend_task_XXX.json`

### 5. Integrate All Decomposition Results

After all decomposers complete:

#### 5.1 Read All Temporary Files
Read all files from `.claude_tasks/backend_decomposition_temp/backend_task_*.json`

#### 5.2 Integrate Using Python Script (Tree Structure)

**CRITICAL - Call the pre-built integration script**:

Run the integration script from `.claude/scripts/` directory:

```bash
cd .claude/scripts
python integrate_decomposition.py --category backend
```

**What the script does automatically**:
1. Reads all files from `.claude_tasks/backend_decomposition_temp/*.json`
2. For each decomposition file:
   - Calls `TaskRegistryManager.add_subtasks_batch(parent_id, subtasks)`
   - Automatically assigns dot notation IDs (e.g., "1.1", "1.1.1")
   - Sets parent_id correctly for all subtasks
   - Updates parent status to "decomposed"
   - Maintains hierarchical tree relationships
3. Validates tree structure integrity
4. Archives processed files to `.claude_tasks/backend_decomposition_archive/`
5. Prints integration summary with task counts

**Expected output**:
```
=== Integration Phase (Python API) ===
Using TaskRegistryManager.add_subtasks_batch() to maintain tree structure...

Integrating backend_task_001.json:
  Parent: "2.1" (Service: AuthenticationService)
  ✓ Created 12 subtasks with IDs: 2.1.1, 2.1.2, 2.1.3, ..., 2.1.12
  ✓ Parent status: pending → decomposed
  ✓ Tree structure validated

Integrating backend_task_002.json:
  Parent: "2.2" (Service: UserManagementService)
  ✓ Created 8 subtasks with IDs: 2.2.1, 2.2.2, ..., 2.2.8
  ✓ Parent status: pending → decomposed
  ✓ Tree structure validated

=== Integration Summary ===
Total new tasks: 20
By type: 12 functions (ready), 8 services (pending)
Tree hierarchy maintained with dot notation IDs
Archived 2 temp files
```

### 6. Update Checkpoint
Save progress after each batch:
- Update `state.json` with latest checkpoint
- Save `task_registry.json` with all new tasks

### 7. Output Summary
```
=== Decomposition Phase: {current_phase} ===
Processing backend batch...

=== Decomposition Phase (Parallel) ===
Tasks needing decomposition: 3
Creating 3 BackendDecomposer subagents in parallel...

backend_task_001 (Service: AuthenticationService):
  ✓ Analyzed requirements from architecture doc
  ✓ Saved to: .claude_tasks/backend_decomposition_temp/backend_task_001.json
  ✓ Identified 12 functions (3 endpoints, 5 services, 2 repositories, 1 validator, 1 util)

backend_task_002 (Service: UserManagementService):
  ✓ Analyzed requirements
  ✓ Saved to: .claude_tasks/backend_decomposition_temp/backend_task_002.json
  ✓ Identified 8 functions

backend_task_003 (Module: DataAccessLayer):
  ✓ Analyzed module structure
  ✓ Saved to: .claude_tasks/backend_decomposition_temp/backend_task_003.json
  ✓ Identified 6 services

=== Integration Phase ===
Running: python integrate_decomposition.py --category backend

[Script output will appear here showing integration progress]

✓ Processed [N] tasks
✓ [X] functions ready (status="ready")
✓ [Y] services need further decomposition (status="pending")

Next command: [/continue-decompose-backend OR /generate-backend-contexts OR /build-deps-fullstack]
```

## Backend Function Types

1. **Endpoint** - Route handler
2. **Service** - Business logic
3. **Repository** - Data access
4. **Validator** - Input validation
5. **Util** - Helper functions
6. **Middleware** - Request/response processing

## Important Rules
- Include HTTP method and route for endpoints
- Specify request/response schemas
- List all database operations
- Identify authentication/authorization needs
- Maximum 10 tasks per batch
- Follow RESTful conventions
