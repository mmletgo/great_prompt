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

#### If task.type == "function":
- Mark as "ready"
- **Immediately invoke ContextGenerator** (see step 5)

#### If task.type == "module":
- **Decompose to Service level**
- Create service/controller tasks
- Save to task_registry (see step 4)

#### If task.type == "service":
- **Decompose to Function/Endpoint level**
- Create tasks for:
  - API endpoints (route handlers)
  - Service layer functions (business logic)
  - Data access functions (repository/ORM)
  - Validation functions
  - Utility functions
- Save to task_registry (see step 4)
- **For each new function task, invoke ContextGenerator** (see step 5)

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

**CRITICAL - NO PARTIAL PROCESSING**: 
- You MUST create ContextGenerator subagents for EVERY SINGLE function task in this batch
- Count total function tasks FIRST, then verify you created exactly that many subagents
- DO NOT split into "first batch" / "core functions" / "remaining functions"
- DO NOT process only "important" tasks - ALL tasks are equally important
- If batch has 25 function tasks → create 25 subagents simultaneously
- If you cannot handle all tasks at once, that indicates a system error

**Verification Required**:
1. Count function tasks: `function_count = tasks where level==3 AND type=="function"`
2. Create subagents: MUST equal `function_count` 
3. Output: "Creating {function_count} ContextGenerator subagents in parallel..."
4. Confirm: "✓ All {function_count} context files generated"

**For ALL function-level tasks in the batch, create subagents at once**:
```
Create ContextGenerator subagents for ALL function tasks in parallel.

For each function task (level == 3):

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

**Example**: If this batch has 8 function-level tasks, create 8 ContextGenerator subagents simultaneously:
- Subagent 1: backend_task_010 (loginUser) → contexts/backend_task_010_context.md
- Subagent 2: backend_task_011 (validateCredentials) → contexts/backend_task_011_context.md
- Subagent 3: backend_task_012 (findUserByEmail) → contexts/backend_task_012_context.md
- Subagent 4: backend_task_013 (comparePassword) → contexts/backend_task_013_context.md
- Subagent 5: backend_task_014 (generateJWT) → contexts/backend_task_014_context.md
- Subagent 6: backend_task_015 (createSession) → contexts/backend_task_015_context.md
- Subagent 7: backend_task_016 (updateLastLogin) → contexts/backend_task_016_context.md
- Subagent 8: backend_task_017 (logLoginAttempt) → contexts/backend_task_017_context.md

**Wait for ALL context generators to complete before proceeding to step 6.**

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
  - ContextGenerator subagents created: [X]
  - Context files generated: [X]
  ✓ ALL function tasks have context (100% coverage)

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
