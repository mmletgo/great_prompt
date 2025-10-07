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
Get next 5-10 pending backend tasks.

### 2. Process Each Backend Task

**CRITICAL - COMPLETE DECOMPOSITION REQUIRED**:
- You MUST decompose ALL non-function tasks to function level
- DO NOT leave any task at module or service level
- DO NOT mark service tasks as "complete" without decomposing them
- Every service MUST be decomposed into its individual functions
- If a service seems "simple", it still has functions (at minimum: handler, validator, repository)

#### If task.type == "function":
- Mark as "ready"
- **Immediately invoke ContextGenerator** (see step 5)

#### If task.type == "module":
- **Decompose to Service level**
- Create service/controller tasks
- Save to task_registry (see step 4)
- **DO NOT mark module as complete - services must be decomposed next**

#### If task.type == "service":
- **MUST Decompose to Function/Endpoint level** (non-negotiable)
- Create tasks for ALL functions:
  - API endpoints (route handlers)
  - Service layer functions (business logic)
  - Data access functions (repository/ORM)
  - Validation functions
  - Utility functions
- A "simple" service still has minimum 5-10 functions
- Save to task_registry (see step 4)
- **For each new function task, invoke ContextGenerator** (see step 5)
- **DO NOT skip decomposition** - every service must create function tasks

### 3. Invoke BackendDecomposer Subagent
```
Create a BackendDecomposer subagent for backend_task_XXX.

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

Output format: Save to `.claude_tasks/decomposition_temp/backend_task_XXX.json`

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

Each decomposer saves its results to:
- `.claude_tasks/decomposition_temp/backend_task_XXX.json`

### 5. Integrate All Decomposition Results

After all decomposers complete:

#### 5.1 Read All Temporary Files
Read all files from `.claude_tasks/decomposition_temp/backend_task_*.json`

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

#### 5.4 Clean Up Temporary Files
After successful merge:
- Delete all `.claude_tasks/decomposition_temp/backend_task_*.json` files

### 6. Invoke Context Generator for Function Tasks (Parallel)

**After step 5 integration completes**, invoke context generators.

**Trigger condition**: For each task where `level == 3` AND `type == "function"`

**This includes**:
- Existing function tasks (already at level 3)
- Newly decomposed function tasks (just created in step 3-4)

**CRITICAL - BATCHED PARALLEL PROCESSING (NO SKIPPING)**:
- You MUST create ContextGenerator subagents for EVERY SINGLE function task in this batch
- Process in sub-batches of maximum 10 subagents at a time for manageability
- Count total function tasks FIRST, calculate number of sub-batches needed
- Process ALL sub-batches - DO NOT stop after first sub-batch
- Each sub-batch must complete before starting next sub-batch

**Batching Rules**:
1. Count total: `function_count = tasks where level==3 AND type=="function"`
2. Calculate batches: `num_batches = ceil(function_count / 10)`
3. **MANDATORY PARALLEL EXECUTION WITHIN EACH SUB-BATCH**:
   - Within each sub-batch, you MUST create ALL subagents AT THE SAME TIME
   - DO NOT process sub-batch items one by one
   - DO NOT wait for one subagent to finish before starting the next
   - Create 10 `<subagent_task>` blocks simultaneously in one response
   - Example: For sub-batch of 10, output 10 subagent blocks together, not sequentially
4. Track progress: "Processing batch X of Y (10 functions)..."
5. Verify completion: After ALL batches, confirm total = function_count

**Example - 32 function tasks**:
```
Total function tasks: 32
Sub-batches needed: 4 (10 + 10 + 10 + 2)

Processing sub-batch 1 of 4 (10 functions)...
  Creating ALL 10 ContextGenerator subagents SIMULTANEOUSLY:
  
  <subagent_task>Agent: @context-generator (backend_task_015 - authenticateUser)</subagent_task>
  <subagent_task>Agent: @context-generator (backend_task_016 - validateToken)</subagent_task>
  <subagent_task>Agent: @context-generator (backend_task_017 - refreshToken)</subagent_task>
  ... [ALL 10 subagent blocks in ONE response]
  
  ✓ Sub-batch 1 complete: 10/10 contexts generated

Processing sub-batch 2 of 4 (10 functions)...
  Creating 10 ContextGenerator subagents in parallel:
  - backend_task_020 (createSession)
  - backend_task_021 (updateLastLogin)
  ... (10 total)
  ✓ Sub-batch 2 complete: 10/10 contexts generated

Processing sub-batch 3 of 4 (10 functions)...
  ✓ Sub-batch 3 complete: 10/10 contexts generated

Processing sub-batch 4 of 4 (2 functions)...
  Creating 2 ContextGenerator subagents in parallel:
  - backend_task_040 (logLoginAttempt)
  - backend_task_041 (cleanupExpiredSessions)
  ✓ Sub-batch 4 complete: 2/2 contexts generated

✓ ALL batches complete: 32/32 contexts generated (100% coverage)
```

**FORBIDDEN - PARTIAL BATCH PROCESSING**:
- ❌ "Processing first batch, skipping remaining" 
- ❌ "Starting with batch 1, will continue later"
- ❌ "Key functions in batch 1, others optional"
- ❌ "Processing function 1... Processing function 2..." (串行执行)
- ❌ "Let me continue with function X" (one-by-one 处理)
- ✅ REQUIRED: "Creating ALL 10 subagents simultaneously in one response"
- ✅ REQUIRED: "ALL X batches processed" / "100% coverage across all batches"

**Verification Required**:
1. Count function tasks: `function_count = tasks where level==3 AND type=="function"`
2. Calculate sub-batches: `num_batches = ceil(function_count / 10)`
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
Processing backend batch...

backend_task_001 (Service: AuthenticationService):
  ✓ Analyzed requirements from architecture doc
  ✓ Saved to: .claude_tasks/decomposition_temp/backend_task_001.json
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
