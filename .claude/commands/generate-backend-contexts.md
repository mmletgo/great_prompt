---
description: Generate context files for all backend function tasks
---

# Generate Backend Context Files

## Your Task
Generate comprehensive context files for all backend function-level tasks that are ready for context generation.

## Prerequisites
- `decomposition_phase.backend_status == "completed"` OR at least some function tasks exist
- Function-level tasks exist in task_registry.json (type == "function", level == 3)

## Steps

### 1. Load Task Registry
Read `.claude_tasks/task_registry.json` and filter tasks:
- `category == "backend"`
- `type == "function"`
- `level == 3`
- `status == "ready"` (not yet context-generated)

Count total tasks needing context generation.

### 2. Batch Processing Strategy

**Batching Rules**:
- Maximum 10 context generators per sub-batch
- Calculate: `num_batches = ceil(total_tasks / 10)`
- Process ALL batches sequentially
- Each sub-batch runs in parallel (all 10 subagents created simultaneously)

**Example**:
```
Total function tasks: 63
Sub-batches needed: 7 (10 + 10 + 10 + 10 + 10 + 10 + 3)
```

### 3. Invoke Context Generator Subagents (Batched Parallel)

For each sub-batch:

**CRITICAL - PARALLEL EXECUTION WITHIN SUB-BATCH**:
- Create ALL 10 (or remaining) subagents in ONE response
- DO NOT process one by one
- DO NOT wait for one to finish before creating next
- Output all `<subagent_task>` blocks together

**Example - Sub-batch of 10**:
```
Processing sub-batch 1 of 7 (10 functions)...
Creating ALL 10 ContextGenerator subagents SIMULTANEOUSLY:

<subagent_task>
Agent: @context-generator
Input:
- Task ID: backend_task_015
- Function: authenticateUser
- API spec: docs/prd.md
Task: Generate comprehensive context file
</subagent_task>

<subagent_task>
Agent: @context-generator
Input:
- Task ID: backend_task_016
- Function: validateToken
- API spec: docs/prd.md
Task: Generate comprehensive context file
</subagent_task>

... [8 more subagent blocks - ALL in ONE response]

[Wait for ALL 10 subagents to complete]
```

**For each function task, create this subagent**:
```
<subagent_task>
Agent: @context-generator
Input:
- Task ID: {task_id}
- Function metadata: from task_registry.json
- API spec: docs/prd.md
- Architecture: docs/fullstack-architecture.md
- Frontend dependencies: from task_registry.json

Task:
1. Read function metadata from task_registry.json:
   - Function name and type (endpoint/service/repository/validator/util)
   - Function signature
   - Input parameters
   - Return type
   - HTTP details (if endpoint)
   - Database operations
   - Dependencies

2. Read API specification:
   - Business requirements
   - Data models
   - Validation rules
   - Error cases

3. Analyze dependencies:
   - Other backend functions this depends on
   - Frontend components that call this function

4. Generate context file at: .claude_tasks/contexts/{task_id}_context.md

Output format:

# Task {task_id}: {FunctionName}

## Function Overview
**Type**: {Endpoint/Service/Repository/Validator/Util}
**Layer**: {API/Business Logic/Data Access/Validation/Utility}
**Purpose**: {Brief description}

## Function Specification

### Function Signature
```python
async def function_name(
    param1: Type,
    param2: Type,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReturnType:
    """
    Brief description of what function does.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        ReturnType: Description
    
    Raises:
        ValidationError: When validation fails
        DatabaseError: When database operation fails
        AuthenticationError: When authentication fails
    """
```

### Input Parameters
| Parameter | Type | Required | Description | Validation |
|-----------|------|----------|-------------|------------|
| param1 | str | Yes | Description | min_length=3, max_length=50 |
| param2 | int | No | Description | ≥0, ≤100 |
| db | Session | Yes | Database session | Dependency injection |
| current_user | User | Yes | Authenticated user | Auth required |

### Return Value
```python
# Success case
{
    "success": True,
    "data": {
        "id": 123,
        "field": "value"
    },
    "message": "Operation successful"
}

# Error case
{
    "success": False,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {}
    }
}
```

### HTTP Details (for endpoints)
- **Method**: POST/GET/PUT/DELETE/PATCH
- **Route**: `/api/v1/resource/{id}`
- **Content-Type**: `application/json`
- **Authentication**: Required/Optional/None
- **Authorization**: Required roles/permissions

**Status Codes**:
- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Authorization failed
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate resource
- `500 Internal Server Error`: Server error

**Request Body** (for POST/PUT/PATCH):
```json
{
  "field1": "value",
  "field2": 123,
  "nested": {
    "field3": true
  }
}
```

**Response Body**:
```json
{
  "id": 123,
  "field1": "value",
  "created_at": "2024-03-20T10:00:00Z",
  "updated_at": "2024-03-20T10:00:00Z"
}
```

## Business Logic

### Algorithm Steps
1. **Step 1**: Validate input parameters
   - Check param1 is not empty
   - Verify param2 is within range
   - Validate data format

2. **Step 2**: Authenticate and authorize
   - Verify user is authenticated
   - Check user has required permissions
   - Load user context

3. **Step 3**: Perform database operations
   - Query existing records
   - Check for conflicts
   - Execute transaction

4. **Step 4**: Process business logic
   - Calculate values
   - Apply business rules
   - Transform data

5. **Step 5**: Return response
   - Format success response
   - Include relevant data
   - Set appropriate status code

### Edge Cases
- **Empty input**: Return validation error
- **Duplicate resource**: Return 409 conflict
- **Permission denied**: Return 403 forbidden
- **Resource not found**: Return 404 not found
- **Database unavailable**: Return 503 service unavailable

## Database Operations

### Tables Accessed
- `users`: SELECT, UPDATE
- `sessions`: INSERT, DELETE
- `audit_logs`: INSERT

### Queries
```sql
-- Query 1: Check existing user
SELECT id, email, password_hash 
FROM users 
WHERE email = :email AND deleted_at IS NULL;

-- Query 2: Create session
INSERT INTO sessions (user_id, token, expires_at, created_at)
VALUES (:user_id, :token, :expires_at, NOW());

-- Query 3: Log action
INSERT INTO audit_logs (user_id, action, ip_address, created_at)
VALUES (:user_id, :action, :ip_address, NOW());
```

### Transaction Scope
```python
async with db.begin():
    # All operations in single transaction
    user = await create_user(db, user_data)
    session = await create_session(db, user.id)
    await log_action(db, user.id, "register")
    # Commit or rollback together
```

### Indexes Required
- `users.email` - Unique index for fast lookup
- `sessions.token` - Index for token validation
- `sessions.expires_at` - Index for cleanup queries
- `audit_logs.user_id` - Index for user activity queries

## Dependencies

### Backend Dependencies
| Task ID | Function | What It Provides |
|---------|----------|------------------|
| backend_task_020 | validate_email | Email validation |
| backend_task_021 | hash_password | Password hashing |
| backend_task_022 | generate_token | JWT token generation |

### Frontend Dependencies
| Task ID | Component | How It Uses This |
|---------|-----------|------------------|
| frontend_task_050 | LoginForm | Calls this endpoint on submit |
| frontend_task_055 | AuthProvider | Uses token from response |

## Error Handling

### Error Case 1: Validation Error
```python
if not is_valid_email(email):
    raise ValidationError(
        code="INVALID_EMAIL",
        message="Email format is invalid",
        field="email"
    )
```
**HTTP Code**: 400 Bad Request  
**Recovery**: User corrects input and retries

### Error Case 2: Authentication Failed
```python
if not verify_password(password, user.password_hash):
    raise AuthenticationError(
        code="INVALID_CREDENTIALS",
        message="Email or password is incorrect"
    )
```
**HTTP Code**: 401 Unauthorized  
**Recovery**: User provides correct credentials

### Error Case 3: Database Error
```python
try:
    await db.execute(query)
    await db.commit()
except DatabaseError as e:
    await db.rollback()
    raise ServerError(
        code="DATABASE_ERROR",
        message="Failed to save data",
        details=str(e)
    )
```
**HTTP Code**: 500 Internal Server Error  
**Recovery**: Log error, alert ops team, return generic error

### Error Case 4: Rate Limit Exceeded
```python
if is_rate_limited(ip_address):
    raise RateLimitError(
        code="RATE_LIMIT_EXCEEDED",
        message="Too many requests, try again later",
        retry_after=60
    )
```
**HTTP Code**: 429 Too Many Requests  
**Recovery**: User waits and retries

## Security Considerations

### Authentication
- **Required**: Yes
- **Method**: JWT Bearer token in Authorization header
- **Token format**: `Authorization: Bearer <token>`
- **Token validation**: Verify signature, check expiration, validate claims

### Authorization
- **Required permissions**: `user:write`, `session:create`
- **Role-based**: User must have "user" role minimum
- **Resource-based**: User can only access own data

### Input Sanitization
- Strip HTML tags from text inputs
- Escape SQL special characters (use parameterized queries)
- Validate email format with regex
- Limit string lengths to prevent buffer overflow
- Check for script injection in user-provided content

### Data Protection
- Never return password hashes in responses
- Redact sensitive fields in logs
- Use HTTPS for all API calls
- Encrypt tokens at rest
- Implement CORS properly

### Rate Limiting
- Per IP: 100 requests per minute
- Per user: 1000 requests per hour
- Login endpoint: 5 attempts per 15 minutes

## Performance Considerations

### Expected Performance
- **Response time**: <200ms (p95)
- **Throughput**: 100 req/s per instance
- **Database query time**: <50ms
- **Memory usage**: <100MB per request

### Optimization Strategies

#### Database Optimization
```python
# Use select_related to avoid N+1 queries
user = await db.query(User).options(
    selectinload(User.profile),
    selectinload(User.roles)
).filter_by(id=user_id).first()
```

#### Caching
```python
# Cache frequently accessed data
@cache(ttl=300)  # 5 minutes
async def get_user_permissions(user_id: int):
    return await db.query(Permission).join(UserRole).filter(...)
```

#### Connection Pooling
```python
# Reuse database connections
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)
```

### Monitoring
- Log response times
- Track error rates
- Monitor database query performance
- Alert on slow queries (>100ms)

## TDD Test Cases

### Test Case 1: Success Path
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_function_success(client: AsyncClient, db_session):
    """Test successful function execution."""
    # Arrange
    request_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    
    # Act
    response = await client.post("/api/auth/login", json=request_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data["data"]
    assert data["data"]["user"]["email"] == request_data["email"]
```

### Test Case 2: Validation Error
```python
@pytest.mark.asyncio
async def test_invalid_email_format(client: AsyncClient):
    """Test validation fails for invalid email."""
    # Arrange
    request_data = {
        "email": "not-an-email",
        "password": "password"
    }
    
    # Act
    response = await client.post("/api/auth/login", json=request_data)
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_EMAIL"
```

### Test Case 3: Authentication Failed
```python
@pytest.mark.asyncio
async def test_wrong_password(client: AsyncClient, test_user):
    """Test authentication fails with wrong password."""
    # Arrange
    request_data = {
        "email": test_user.email,
        "password": "WrongPassword"
    }
    
    # Act
    response = await client.post("/api/auth/login", json=request_data)
    
    # Assert
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_CREDENTIALS"
```

### Test Case 4: Database Error
```python
@pytest.mark.asyncio
async def test_database_error(client: AsyncClient, monkeypatch):
    """Test graceful handling of database errors."""
    # Arrange
    async def mock_execute(*args, **kwargs):
        raise DatabaseError("Connection lost")
    
    monkeypatch.setattr("sqlalchemy.engine.execute", mock_execute)
    request_data = {"email": "test@example.com", "password": "password"}
    
    # Act
    response = await client.post("/api/auth/login", json=request_data)
    
    # Assert
    assert response.status_code == 500
    data = response.json()
    assert data["error"]["code"] == "DATABASE_ERROR"
```

### Test Case 5: Authorization Check
```python
@pytest.mark.asyncio
async def test_requires_authentication(client: AsyncClient):
    """Test endpoint requires authentication."""
    # Act - No auth header
    response = await client.get("/api/protected-resource")
    
    # Assert
    assert response.status_code == 401
```

### Test Case 6: Rate Limiting
```python
@pytest.mark.asyncio
async def test_rate_limit_exceeded(client: AsyncClient):
    """Test rate limiting prevents abuse."""
    # Arrange
    request_data = {"email": "test@example.com", "password": "wrong"}
    
    # Act - Make 6 requests (limit is 5)
    responses = []
    for _ in range(6):
        response = await client.post("/api/auth/login", json=request_data)
        responses.append(response)
    
    # Assert
    assert responses[-1].status_code == 429
    assert "retry_after" in responses[-1].json()["error"]
```

## Related Files

### Implementation
- **Target file**: `src/{layer}/{module}/{function_name}.py`
- **Models**: `src/models/{model_name}.py`
- **Schemas**: `src/schemas/{schema_name}.py`

### Testing
- **Test file**: `tests/{layer}/{module}/test_{function_name}.py`
- **Fixtures**: `tests/fixtures/{resource}_fixtures.py`
- **Mocks**: `tests/mocks/{service}_mocks.py`

### Documentation
- **API docs**: Auto-generated from docstrings
- **OpenAPI spec**: `docs/openapi.yaml`

### Dependencies
- **Services**: {list of service layer files}
- **Repositories**: {list of repository files}
- **Validators**: {list of validator files}
- **Utils**: {list of utility files}
- **Types**: {type definition files}

## Success Criteria

### Functional Requirements
- ✅ All parameters validated
- ✅ Business logic correct
- ✅ Database operations work
- ✅ Error handling comprehensive
- ✅ Authentication/authorization enforced

### Quality Requirements
- ✅ Test coverage ≥80%
- ✅ No type errors
- ✅ No security vulnerabilities
- ✅ Passes linting
- ✅ API documentation complete

### Performance Requirements
- ✅ Response time <200ms (p95)
- ✅ No N+1 query problems
- ✅ Proper indexing used
- ✅ Caching implemented
- ✅ Rate limiting working

## Dependencies on Other Tasks
{list of task IDs this function depends on}

## Tasks Depending on This
{list of task IDs that depend on this function}
</subagent_task>
```

**Wait for all subagents in current sub-batch to complete before proceeding to next sub-batch.**

### 4. Verify Context Generation

After each sub-batch completes:
```
✓ Sub-batch {i} complete: {count}/{count} contexts generated

Verification:
  - backend_task_015: ✓ Context file created
  - backend_task_016: ✓ Context file created
  - backend_task_017: ✓ Context file created
  ...
```

### 5. Update Task Status

Use Python script to mark tasks as context-generated:

```python
from task_registry_manager import TaskRegistryManager

task_mgr = TaskRegistryManager()

# Update all tasks in batch
completed_tasks = [
    "backend_task_015",
    "backend_task_016",
    # ... all tasks in sub-batch
]

for task_id in completed_tasks:
    task_mgr.update_task_status(
        task_id=task_id,
        status="context_ready"  # Ready for development
    )
```

### 6. Summary Output

After ALL sub-batches complete:

```
=== Backend Context Generation Summary ===

Total function tasks: 63
Sub-batches processed: 7

Sub-batch Results:
  Sub-batch 1: 10/10 contexts ✓
  Sub-batch 2: 10/10 contexts ✓
  Sub-batch 3: 10/10 contexts ✓
  Sub-batch 4: 10/10 contexts ✓
  Sub-batch 5: 10/10 contexts ✓
  Sub-batch 6: 10/10 contexts ✓
  Sub-batch 7: 3/3 contexts ✓

✓ ALL contexts generated: 63/63 (100% coverage)

Context files by type:
  Endpoints: 18 contexts
  Services: 25 contexts
  Repositories: 12 contexts
  Validators: 5 contexts
  Utils: 3 contexts

Context files created in: .claude_tasks/contexts/
  - backend_task_015_context.md (authenticateUser)
  - backend_task_016_context.md (validateToken)
  - backend_task_017_context.md (refreshToken)
  ... (63 total)

Updated task statuses: 63 tasks → "context_ready"

✓ Backend functions ready for TDD development

Next command: /build-deps-fullstack
```

## Important Rules

### Parallel Execution
- ✅ REQUIRED: Create ALL subagents in sub-batch simultaneously
- ✅ REQUIRED: Process ALL sub-batches (no skipping)
- ✅ REQUIRED: 100% coverage across all function tasks
- ❌ FORBIDDEN: Processing tasks one by one
- ❌ FORBIDDEN: Skipping sub-batches
- ❌ FORBIDDEN: Partial processing

### Verification
- Count total function tasks before starting
- Calculate number of sub-batches needed
- Track progress after each sub-batch
- Verify 100% completion at end

### Quality
- All context files must follow template format
- Include all required sections
- Provide comprehensive TDD test cases
- Include security considerations
- Document database operations

## Edge Cases

### No Tasks Need Context
```
No function tasks found needing context generation.
All tasks either:
  - Already have contexts (status = "context_ready")
  - Not yet decomposed to function level
  
Recommendation: Run /continue-decompose-backend first
```

### Partial Generation
```
If interrupted mid-batch:
- Already generated contexts remain valid
- Re-run command to generate remaining
- Command automatically skips tasks with status = "context_ready"
```

### Missing Specifications
```
Warning: backend_task_XXX references missing API specification
  Expected: docs/prd.md section on {feature}
  Action: Creating context with available information
  TODO: Update context after specification is added
```
