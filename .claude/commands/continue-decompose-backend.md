---
description: Continue backend task decomposition (next batch)
argument-hint: [batch_size]
---

# Continue Backend Task Decomposition

## Your Task
Continue decomposing backend tasks to function/endpoint level.

## Steps

### 1. Load State and Get Next Batch
Get next 5-10 pending backend tasks.

### 2. Process Each Backend Task

#### If task.type == "function":
- Mark as "ready"
- Invoke BackendContextGenerator

#### If task.type == "module":
- **Decompose to Service level**
- Create service/controller tasks

#### If task.type == "service":
- **Decompose to Function/Endpoint level**
- Create tasks for:
  - API endpoints (route handlers)
  - Service layer functions (business logic)
  - Data access functions (repository/ORM)
  - Validation functions
  - Utility functions

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

### 4. Invoke Context Generator
```
Create a ContextGenerator for function task.

<subagent_task>
Agent: @context-generator
Input:
- Task metadata: from decomposer
- API spec: from PRD
- Architecture: docs/fullstack-architecture.md

Output: .claude_tasks/contexts/backend_task_XXX_context.md with:
- Function signature
- Request/Response schemas
- Database operations
- Business logic steps
- Error handling
- Security considerations
- TDD test cases
</subagent_task>
```

### 5. Output Summary
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
