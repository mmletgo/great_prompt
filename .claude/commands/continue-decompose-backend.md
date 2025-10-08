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

### 2. Process Each Backend Task

**CRITICAL - COMPLETE DECOMPOSITION REQUIRED**:
- You MUST decompose ALL non-function tasks to function level
- DO NOT leave any task at module or service level
- DO NOT mark service tasks as "complete" without decomposing them
- Every service MUST be decomposed into its individual functions
- If a service seems "simple", it still has functions (at minimum: handler, validator, repository)

#### If task.type == "function":
- Mark as "ready"
- Note: Context generation will be handled by `/generate-backend-contexts` command later

#### If task.type == "module" (Level 1):
- **Decompose to Service level (Level 2)**
- Use `add_subtask()` to create service tasks under this module
- Each service gets dot notation ID based on parent (e.g., parent="1" → services="1.1", "1.2", etc.)
- **DO NOT mark module as complete - services must be decomposed next**
- Parent status automatically changes to "decomposed"

**Python example**:
```python
task_mgr = TaskRegistryManager()

# Create service tasks under module "1"
auth_api_id = task_mgr.add_subtask("1", {
    "title": "Authentication API Layer",
    "type": "service",
    "description": "API endpoints for auth"
})  # Returns "1.1"

auth_service_id = task_mgr.add_subtask("1", {
    "title": "Authentication Service Layer",
    "type": "service",
    "description": "Business logic for auth"
})  # Returns "1.2"
```

#### If task.type == "service" (Level 2):
- **MUST Decompose to Function/Endpoint level (Level 3)** (non-negotiable)
- Use `add_subtasks_batch()` to create multiple function tasks at once
- Each function gets dot notation ID (e.g., parent="1.1" → functions="1.1.1", "1.1.2", etc.)
- Create tasks for ALL functions:
  - API endpoints (route handlers)
  - Service layer functions (business logic)
  - Data access functions (repository/ORM)
  - Validation functions
  - Utility functions
- A "simple" service still has minimum 5-10 functions
- **DO NOT skip decomposition** - every service must create function tasks
- Parent status automatically changes to "decomposed"

**Python example**:
```python
# Create function tasks under service "1.1"
function_ids = task_mgr.add_subtasks_batch("1.1", [
    {"title": "login_endpoint", "type": "function", "http_method": "POST", "route": "/api/auth/login"},
    {"title": "signup_endpoint", "type": "function", "http_method": "POST", "route": "/api/auth/signup"},
    {"title": "logout_endpoint", "type": "function", "http_method": "POST", "route": "/api/auth/logout"},
    {"title": "verify_token", "type": "function", "description": "JWT verification utility"}
])  # Returns ["1.1.1", "1.1.2", "1.1.3", "1.1.4"]
```

### 3. Invoke BackendDecomposer Subagents (Parallel)

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

#### 5.2 Assign Task IDs
For each subtask across all decomposition files:
1. Get current max task ID from task_registry.json (e.g., backend_task_042)
2. Assign sequential IDs to new tasks:
   - backend_task_043, backend_task_044, ...
3. Build ID mapping for dependencies:
   - If subtask has `dependencies: ["validate_email", "hash_password"]`
   - Look up these function names in all decomposition results
   - Replace with actual task IDs: `["backend_task_045", "backend_task_046"]`

#### 5.3 Merge into task_registry.json
For each decomposition result:
1. **Add subtasks to `tasks` object**:
   - Use assigned IDs from step 5.2
   - Set `parent_id` to the decomposed task
   - Set `status` based on type:
     * `type == "function"` → status = "ready"
     * `type == "service"` → status = "pending"
   - Set `category` = "backend"
   - Resolve dependency references to task IDs
   - Include all metadata (http_method, route, function_signature, etc.)

2. **Update parent task**:
   - Set parent's `status` = "decomposed"
   - Set parent's `children` = [array of new task IDs]

3. **Update metadata counters**:
   - Increment `backend_metadata.total_services` by services count
   - Increment `backend_metadata.total_functions` by functions count
   - Update `by_layer` counters (endpoint, service, repository, etc.)

Example merged result:
```json
{
  "tasks": {
    "backend_task_001": {
      "status": "decomposed",
      "children": ["backend_task_043", "backend_task_044", "backend_task_045"]
    },
    "backend_task_043": {
      "id": "backend_task_043",
      "title": "loginUser",
      "level": 3,
      "type": "function",
      "function_type": "endpoint",
      "category": "backend",
      "status": "ready",
      "parent_id": "backend_task_001",
      "http_method": "POST",
      "route": "/api/auth/login",
      "dependencies": ["backend_task_044", "backend_task_045"]
    }
  },
  "backend_metadata": {
    "total_modules": 4,
    "total_services": 8,
    "total_functions": 47,
    "by_layer": {
      "endpoint": 12,
      "service": 18,
      "repository": 10,
      "validator": 4,
      "util": 3
    }
  }
}
```

#### 5.4 Temporary File Cleanup Responsibility
**The deletion of temporary files (.claude_tasks/backend_decomposition_temp/backend_task_*.json) MUST be performed by you only after confirming that all tasks have been successfully merged into task_registry.json. The Python integration script MUST NOT delete temporary files directly.**

### 6. Update Checkpoint
3. For each sub-batch (1 to num_batches):
   - Output: "Processing sub-batch {i} of {num_batches} ({size} functions)..."
   - Create subagents: up to 10 per sub-batch
   - Confirm: "✓ Sub-batch {i} complete: {size}/{size} contexts generated"
4. Final verification: "✓ ALL {num_batches} batches complete: {function_count}/{function_count} contexts (100% coverage)"

**For ALL function-level tasks, process in sub-batches of 10**:

**CRITICAL - PARALLEL EXECUTION FORMAT**:
- For each sub-batch, create ALL subagent_task blocks in ONE response
- DO NOT create subagents one-by-one across multiple responses
- Output 10 `<subagent_task>` blocks together, then wait for all to complete

```
For each sub-batch of up to 10 function tasks (create ALL simultaneously):

<subagent_task>
Agent: @context-generator
Input:
- Task ID: backend_task_XXX
- Function metadata: from decomposer output or task_registry
- API spec: from docs/prd.md
- Architecture: docs/fullstack-architecture.md

Task:
1. Read function metadata from task_registry
2. Extract function requirements:
   - Function signature
   - Input parameters and types
   - Return type
   - Business logic steps
   - Database operations
   - Dependencies
   - Error cases
3. Generate comprehensive context file

Output: .claude_tasks/contexts/backend_task_XXX_context.md with:

# Task XXX: [FunctionName]

## Function Overview
[Description and purpose]

## Function Specification
### Function Signature
```typescript
async function functionName(params): Promise<ReturnType>
```

### Input Parameters
- param1: type - description - validation rules
- param2: type - description - validation rules

### Return Value
- type: ReturnType
- success case: {...}
- error case: {...}

### HTTP Details (if endpoint)
- Method: POST/GET/PUT/DELETE
- Route: /api/resource
- Status codes: 200, 400, 401, 500

## Business Logic
1. Step 1: [detailed description]
2. Step 2: [detailed description]
3. ...

## Database Operations
- SELECT from table WHERE condition
- INSERT into table VALUES (...)
- UPDATE table SET ... WHERE ...

## Dependencies
- backend_task_YYY: [what it provides]
- backend_task_ZZZ: [what it provides]

## Error Handling
### Error Case 1: [ErrorType]
- Condition: [when it occurs]
- HTTP Code: 400
- Message: "..."
- Recovery: [how to handle]

## Security Considerations
- Authentication required: Yes/No
- Authorization: [required permissions]
- Input sanitization: [what to sanitize]
- Rate limiting: [limits]

## Performance
- Expected response time: <200ms
- Database indexes needed: [list]
- Caching strategy: [if any]

## TDD Test Cases
### Test Case 1: Success Path
```typescript
// Test code
```

### Test Case 2: Validation Error
```typescript
// Test code
```

### Test Case 3: Database Error
```typescript
// Test code
```

## Related Files
- Target file: src/[layer]/[module]/functionName.ts
- Test file: src/[layer]/[module]/functionName.test.ts
- Dependencies: [list of imported files]
</subagent_task>
```

**Wait for current sub-batch to complete before proceeding to next sub-batch.**
**Wait for ALL sub-batches to complete before proceeding to step 7.**

### 7. Update Checkpoint
Save progress after each batch:
- Update `state.json` with latest checkpoint
- Save `task_registry.json` with all new tasks

### 8. Output Summary
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

=== Integration Phase (Python Script) ===
Generated: .claude_tasks/integrate_backend_tasks.py
Executing integration script...

✓ Integrated backend_task_001.json: 12 functions
✓ Integrated backend_task_002.json: 8 functions
✓ Integrated backend_task_003.json: 6 functions

=== Integration Summary ===
Total new tasks: 26
New services: 0
New functions: 26
By type: {'endpoint': 7, 'service': 11, 'repository': 5, 'validator': 2, 'util': 1}
Resolved 47 dependencies
Updated task_registry.json
Archived 3 temp files

Next available ID: backend_task_069

✓ Processed [N] tasks
✓ [X] functions ready, [Y] services need decomposition

Context Generation Verification:
  - Function tasks in batch: [X]
  - Sub-batches processed: [Y] (max 10 per sub-batch)
  - Sub-batch 1: 10/10 contexts ✓
  - Sub-batch 2: 10/10 contexts ✓
  - Sub-batch 3: 7/7 contexts ✓
  - Total contexts generated: [X]
  ✓ ALL sub-batches complete: [X]/[X] contexts (100% coverage)

Next command: [/continue-decompose-backend OR /build-deps-fullstack]
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
