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

Output format: JSON array of function-level tasks
[
  {
    "id": "backend_task_XXX",
    "title": "login_user",
    "level": 3,
    "type": "function",
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
]
</subagent_task>
```

### 4. Save Decomposed Tasks to Registry
For each task decomposed by the BackendDecomposer:

1. **Add new tasks to `task_registry.json`**:
   - Append each subtask to the `tasks` object
   - Update parent task's `children` array
   - Update parent task's `status` from "pending" to "decomposed"

2. **Update metadata**:
   - Increment `backend_metadata.total_functions`
   - Update progress counters

Example update:
```json
{
  "tasks": {
    "backend_task_001": {
      "status": "decomposed",
      "children": ["backend_task_010", "backend_task_011", "backend_task_012"]
    },
    "backend_task_010": {
      "id": "backend_task_010",
      "title": "loginUser",
      "level": 3,
      "type": "function",
      "function_type": "endpoint",
      "category": "backend",
      "status": "ready",
      "parent_id": "backend_task_001",
      "http_method": "POST",
      "route": "/api/auth/login",
      "dependencies": ["backend_task_011", "backend_task_012"]
    }
  },
  "backend_metadata": {
    "total_modules": 4,
    "total_functions": 35
  }
}
```

### 5. Invoke Context Generator for Function Tasks (Parallel)

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
3. Process each batch sequentially, but within each batch create all 10 subagents simultaneously
4. Track progress: "Processing batch X of Y (10 functions)..."
5. Verify completion: After ALL batches, confirm total = function_count

**Example - 32 function tasks**:
```
Total function tasks: 32
Sub-batches needed: 4 (10 + 10 + 10 + 2)

Processing sub-batch 1 of 4 (10 functions)...
  Creating 10 ContextGenerator subagents in parallel:
  - backend_task_010 (loginUser)
  - backend_task_011 (validateCredentials)
  - backend_task_012 (findUserByEmail)
  ... (10 total)
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
```
For each sub-batch of up to 10 function tasks:

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
**Wait for ALL sub-batches to complete before proceeding to step 6.**

### 6. Update Checkpoint
Save progress after each batch:
- Update `state.json` with latest checkpoint
- Save `task_registry.json` with all new tasks

### 7. Output Summary
```
Processing backend batch...

backend_task_001 (Service: AuthenticationService):
  ✓ Decomposed into 12 functions:
    - login_user (POST /api/auth/login) [endpoint]
    - validate_credentials (email, password) [validator]
    - check_account_status (user_id) [service]
    - generate_access_token (user) [util]
    - generate_refresh_token (user) [util]
    - create_session (user_id, token) [repository]
    - hash_password (password) [util]
    - compare_password (plain, hashed) [util]
    ...

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
