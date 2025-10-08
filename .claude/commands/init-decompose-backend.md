---
description: Initialize backend task decomposition based on PRD and architecture
---

# Initialize Backend Task Decomposition

## Your Task
Initialize backend API and service task decomposition based on PRD and architecture.

## Prerequisites
Check that frontend decomposition is complete (recommended but optional):
- `decomposition_phase.frontend_status == "completed"` (if frontend already decomposed)
- OR skip if doing backend-first development

Check input documents:
- `docs/prd.md`
- `docs/fullstack-architecture.md`

## Steps

### 1. Analyze Backend Requirements
Read and analyze:
- `docs/prd.md` - Extract data models, business logic, API requirements
- `docs/fullstack-architecture.md` - Extract backend tech stack, architecture patterns
- Frontend task registry - Extract API calls needed by frontend

### 2. Identify Backend Modules

**CRITICAL - ENSURE ALL API ENDPOINTS ARE INCLUDED**:

**Step 2.1: Extract ALL API endpoints**
List all API endpoints from:
- PRD document (explicitly mentioned APIs)
- Frontend task registry (API calls from frontend tasks)
- Architecture document (API design specifications)

Example list:
```
API Endpoints Found:
1. POST /api/auth/login
2. POST /api/auth/signup
3. POST /api/auth/logout
4. POST /api/auth/refresh-token
5. GET /api/users/:id
6. PUT /api/users/:id
7. DELETE /api/users/:id
8. POST /api/users/:id/avatar
...
(Total: [N] API endpoints)
```

**Step 2.2: Group endpoints into backend modules**
Group all endpoints into logical modules (aim for 4-8 modules).
**Every API endpoint MUST be assigned to exactly one module.**

Example grouping:
```
1. Authentication Service:
   - POST /api/auth/login
   - POST /api/auth/signup
   - POST /api/auth/logout
   - POST /api/auth/refresh-token
   Tables: users, sessions

2. User Management Service:
   - GET /api/users/:id
   - PUT /api/users/:id
   - DELETE /api/users/:id
   - POST /api/users/:id/avatar
   Tables: users, profiles, avatars

3. Data Persistence Layer:
   - [Repository methods - not exposed as REST endpoints]
   Tables: all tables

...
```

**Verification**: Count endpoints = Count assigned
- Total endpoints found: [N]
- Total endpoints assigned: [N]
- ✓ All API endpoints accounted for

### 3. Create Backend Root Tasks with Tree Structure
Create root tasks in tree-based registry:

**📄 Task Registry Format**: See [task_registry.json Template](../templates/task_registry.json.template)

**Tree Structure**:
- Tasks stored in `backend_tasks` array
- Root tasks (Level 1) get IDs: "1", "2", "3", etc.
- Subtasks use dot notation: "1.1", "1.2", "1.1.1", etc.
- Each task has `subtasks` array for children

### 4. Update State and Create Root Tasks
Use Python scripts to initialize and create tasks:

**📄 Script Reference**: See [.claude/scripts/README.md](../.claude/scripts/README.md)

**Python commands**:
```python
from state_manager import StateManager
from task_registry_manager import TaskRegistryManager

state_mgr = StateManager()
task_mgr = TaskRegistryManager()

# Initialize backend decomposition
state_mgr.start_backend_decomposition(total_modules=4)

# Initialize backend metadata
task_mgr.init_backend_metadata(
    framework="FastAPI",
    database="PostgreSQL",
    language="Python"
)

# Create root task for each backend module/service
auth_service_id = task_mgr.add_root_task("backend", {
    "title": "Authentication Service",
    "type": "service",
    "description": "Login, Signup, JWT, Session management",
    "api_endpoints": [
        "POST /api/auth/login",
        "POST /api/auth/signup",
        "POST /api/auth/logout"
    ],
    "database_tables": ["users", "sessions"]
})  # Returns "1"

user_service_id = task_mgr.add_root_task("backend", {
    "title": "User Management Service",
    "type": "service",
    "description": "CRUD operations for user profiles",
    "api_endpoints": [
        "GET /api/users/:id",
        "PUT /api/users/:id",
        "DELETE /api/users/:id"
    ],
    "database_tables": ["users", "profiles"]
})  # Returns "2"

# ... create more root tasks for other services
```

**Updates applied**:
- `decomposition_phase.status = "in_progress"`
- `decomposition_phase.backend_status = "in_progress"`
- Tree structure created with root tasks
- Metadata timestamps automatically set

### 5. Output Summary
```
Analyzed backend requirements:
✓ docs/prd.md (extracted [N] API requirements)
✓ docs/fullstack-architecture.md
✓ Frontend tasks (extracted [M] API calls from frontend)

Created backend root tasks (Level 1 modules):
  - ID: "1" - Authentication Service ([X] endpoints)
    - Endpoints: POST /auth/login, POST /auth/signup, POST /auth/logout, POST /auth/refresh-token
    - Tables: users, sessions
  - ID: "2" - User Management Service ([Y] endpoints)
    - Endpoints: GET /users/:id, PUT /users/:id, DELETE /users/:id, POST /users/:id/avatar
    - Tables: users, profiles, avatars
  - ID: "3" - Data Persistence Layer (repository layer)
    - Endpoints: [Internal repository methods]
    - Tables: all tables
  ...

Backend framework: [FastAPI/Express/Django/etc]
Database: [PostgreSQL/MongoDB/etc]

📊 Tree Structure:
backend_tasks/
  ├─ [1] Authentication Service (pending) - 4 endpoints
  ├─ [2] User Management Service (pending) - 4 endpoints
  ├─ [3] Data Persistence Layer (pending) - repository layer
  └─ ...

✅ API Endpoint Coverage Verification:
  Total endpoints found: [N]
  Total endpoints assigned: [N]
  ✓ All API endpoints accounted for (100%)

Checkpoint saved with [N] root modules
Status: decomposition_phase = in_progress (backend)

Next command: /continue-decompose-backend
```

## Important Rules
- **CRITICAL**: Every API endpoint MUST be assigned to exactly one module
- Verify endpoint count: endpoints found = endpoints assigned
- Extract API requirements from PRD, architecture doc, AND frontend tasks
- Align backend modules with business domains
- Each module's `api_endpoints` array must list all its endpoints
- Include database table requirements for each module
- Reference architecture tech stack
- If an endpoint doesn't fit any existing module, create a new module for it

## Next Steps
After initialization:
1. Use `/continue-decompose-backend` to decompose modules → services → functions
2. Use `/generate-backend-contexts` to generate context files for all functions
3. Then build dependency graph with `/build-deps-fullstack`

````
